"""Bounded workspace memory inspection and usage-summary metadata updates.

Python 3.9+, standard library only. Normal inspection actions are read-only;
summary metadata is the only writable surface.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def safe(root, path):
    """Reject redirected paths, including Windows junctions, before reading."""
    path = Path(os.path.abspath(path))
    if not path.is_relative_to(root):
        raise ValueError("Path is outside workspace")
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink() or getattr(part, 'is_junction', lambda: False)():
            raise ValueError("Linked memory paths are unsupported")
        if part.exists() and part.resolve() != part:
            raise ValueError("Redirected memory paths are unsupported")
    return path


def raise_walk_error(error):
    raise error


def repository_root(workspace):
    """Keep a checkout's memory independent of project selection or subdirectory."""
    root = Path(workspace).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Workspace must be a directory')
    for candidate in (root, *root.parents):
        marker = candidate / '.git'
        if marker.is_dir() or marker.is_file():
            return candidate
    return root


def files(root):
    index = safe(root, root / '.workspace-memory/MEMORY.md')
    directory = safe(root, root / '.workspace-memory/topics')
    found = [index] if index.is_file() else []
    if directory.is_dir():
        for base, dirs, names in os.walk(directory, followlinks=False, onerror=raise_walk_error):
            for name in dirs:
                safe(root, Path(base) / name)
            for name in names:
                if name.lower().endswith('.md') and name.lower() != 'readme.md':
                    found.append(safe(root, Path(base) / name))
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())


def managed_block(text):
    begin, end = '<!-- workspace-memory:begin -->', '<!-- workspace-memory:end -->'
    if text.count(begin) != 1 or text.count(end) != 1:
        return ''
    start, stop = text.index(begin), text.index(end)
    return text[start + len(begin):stop].strip() if start < stop else ''


def read(path):
    return path.read_text(encoding='utf-8-sig')


def entries(root, path):
    """Conservative Markdown blocks: top-level bullets or prose paragraphs."""
    heading, block, start, fence, comment = '', [], 0, None, False
    index_level = None
    relative = path.relative_to(root).as_posix()

    def emit():
        text = '\n'.join(block).rstrip()
        digest = hashlib.sha256((relative + '\0' + heading + '\0' + str(start) + '\0' + text).encode()).hexdigest()[:20]
        return {'id': digest, 'file': relative, 'heading': heading,
                'line': start, 'text': text}

    for number, raw in enumerate(read(path).splitlines(), 1):
        line = raw
        if comment:
            if '-->' not in line:
                continue
            line = line.split('-->', 1)[1]
            comment = False
        while '<!--' in line:
            before, rest = line.split('<!--', 1)
            if '-->' in rest:
                line = before + rest.split('-->', 1)[1]
            else:
                line, comment = before, True
                break
        if fence:
            if block:
                block.append(raw)
            if re.match(r'^\s*' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$', line):
                fence = None
            continue
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            fence = marker[1]
            if block:
                block.append(raw)
            continue
        title = re.match(r'^#{1,6}\s+(.+)', line)
        if title or not line.strip():
            if block:
                yield emit()
                block = []
            if title:
                heading = title[1].strip()
                level = len(line) - len(line.lstrip('#'))
                if index_level is not None and level <= index_level:
                    index_level = None
                if heading.casefold() in ('memory index', 'index'):
                    index_level = level
            continue
        if index_level is not None or line.startswith('>'):
            continue
        bullet = re.match(r'^(?:[-+*]|\d+[.)])\s+', line)
        if bullet and block:
            yield emit()
            block = []
        if not block:
            start = number
        block.append(line)
    if block:
        yield emit()


def scan(root, selected):
    for path in selected:
        yield from entries(root, path)


SUMMARY_NAME = '.workspace-memory/SUMMARY.md'


def summary_path(root):
    return safe(root, root / SUMMARY_NAME)


def summary_rows(root):
    """Return cached source usage counts without reading knowledge content."""
    path = summary_path(root)
    if path.exists() and not path.is_file():
        raise ValueError('Summary path is not a regular file')
    if not path.is_file():
        return {'path': SUMMARY_NAME, 'exists': False, 'total_entries': 0,
                'total_uses': 0, 'sources': []}
    text = read(path)
    total_entries = re.search(r'^- Total entries:\s*(\d+)\s*$', text, re.M)
    total_uses = re.search(r'^- Total uses:\s*(\d+)\s*$', text, re.M)
    sources = []
    table = re.compile(r'^\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*$', re.M)
    for match in table.finditer(text):
        sources.append({'source': match[1], 'entries': int(match[2]),
                        'uses': int(match[3])})
    if total_entries is None or total_uses is None:
        raise ValueError('Summary is malformed; refresh it before use')
    return {'path': SUMMARY_NAME, 'exists': True,
            'total_entries': int(total_entries[1]), 'total_uses': int(total_uses[1]),
            'sources': sources}


def render_summary(sources):
    total_entries = sum(item['entries'] for item in sources)
    total_uses = sum(item['uses'] for item in sources)
    template = (Path(__file__).resolve().parents[1] / 'assets' / 'SUMMARY.md').read_text(
        encoding='utf-8')
    rows = '\n'.join(f"| `{item['source']}` | {item['entries']} | {item['uses']} |"
                     for item in sources)
    return (template.replace('{{TOTAL_ENTRIES}}', str(total_entries))
            .replace('{{TOTAL_USES}}', str(total_uses))
            .replace('{{SOURCE_ROWS}}', rows))


def refresh_summary(root, used_ids=None):
    """Reconcile source entry counts and optionally record one use per entry ID."""
    all_files = files(root)
    selected = all_files
    current = {path.relative_to(root).as_posix(): list(entries(root, path))
               for path in selected}
    try:
        old = summary_rows(root)
    except ValueError as error:
        if not str(error).startswith('Summary is malformed'):
            raise
        # The next managed update replaces a hand-edited or legacy malformed file.
        old = {'path': SUMMARY_NAME, 'exists': False, 'total_entries': 0,
               'total_uses': 0, 'sources': []}
    if not current or not any(current.values()):
        if old['exists']:
            path = summary_path(root)
            path.unlink()
            return dict(summary_rows(root), updated=True)
        return dict(old, updated=False)
    uses = {item['source']: item['uses'] for item in old['sources']}
    if used_ids:
        by_id = {entry['id']: entry for path_entries in current.values()
                 for entry in path_entries}
        if len(set(used_ids)) != len(used_ids):
            raise ValueError('record-use IDs must be unique within one use event')
        missing = [entry_id for entry_id in used_ids if entry_id not in by_id]
        if missing:
            raise ValueError('Entry missing or changed; refresh list/search before recording use')
        for entry_id in used_ids:
            source = by_id[entry_id]['file']
            uses[source] = uses.get(source, 0) + 1
    sources = [{'source': source, 'entries': len(items), 'uses': max(0, uses.get(source, 0))}
               for source, items in sorted(current.items())]
    total_entries = sum(item['entries'] for item in sources)
    total_uses = sum(item['uses'] for item in sources)
    if (old['exists'] and old['total_entries'] == total_entries
            and old['total_uses'] == total_uses and old['sources'] == sources):
        return dict(old, updated=False)
    path = summary_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    try:
        temporary.write_text(render_summary(sources), encoding='utf-8')
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    result = summary_rows(root)
    result['updated'] = True
    return result


def check(root, selected, all_files):
    issues, known, linked, seen = [], set(all_files), set(), {}
    index = root / '.workspace-memory/MEMORY.md'
    if all_files and index not in known:
        issues.append({'kind': 'missing-index', 'file': '.workspace-memory/MEMORY.md'})
    # Index links are needed even when checking one topic.
    if index in known:
        for value in re.findall(r'\[[^\]]*\]\(([^)]+)\)', read(index)):
            url = urlsplit(value.strip().strip('<>'))
            if url.scheme or url.netloc:
                continue
            if not url.path:
                continue
            target = Path(os.path.abspath(index.parent / unquote(url.path)))
            try:
                safe(root, target)
                if target != index and not target.is_relative_to(root / '.workspace-memory/topics'):
                    raise ValueError('Outside memory')
            except ValueError:
                issues.append({'kind': 'unsafe-index-link', 'target': value})
                continue
            linked.add(target)
            if not target.is_file():
                issues.append({'kind': 'broken-index-link', 'target': value})
    for path in selected:
        relative = path.relative_to(root).as_posix()
        if path != index and path not in linked:
            issues.append({'kind': 'unindexed-topic', 'file': relative})
        if path == index and (path.stat().st_size > 8192 or len(read(path).splitlines()) > 100):
            issues.append({'kind': 'large-index', 'file': relative})
        for entry in entries(root, path):
            normalized = re.sub(r'\s+', ' ', entry['text']).strip()
            if normalized in seen:
                issues.append({'kind': 'exact-duplicate', 'ids': [seen[normalized], entry['id']]})
            else:
                seen[normalized] = entry['id']
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['status', 'list', 'search', 'show', 'check',
                                            'summary', 'record-use', 'refresh-summary'])
    parser.add_argument('--workspace', required=True, help='Repository directory or subdirectory; non-Git workspace root')
    parser.add_argument('--harness', choices=['codex', 'claude', 'gemini', 'opencode', 'cursor', 'copilot', 'generic'])
    parser.add_argument('--instruction-file', help='Verified workspace-relative instruction file for status')
    parser.add_argument('--topic')
    parser.add_argument('--query')
    parser.add_argument('--id')
    parser.add_argument('--entry-id', action='append',
                        help='Current entry ID; repeat for each entry used in one event')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--page', type=int, default=1)
    parser.add_argument('--brief', action='store_true',
                        help='Summary actions only: omit per-source rows from output')
    args = parser.parse_args(argv)
    if args.brief and args.action not in ('summary', 'record-use', 'refresh-summary'):
        parser.error('--brief applies only to summary, record-use, or refresh-summary')
    if not 1 <= args.limit <= 100 or args.page < 1:
        parser.error('limit must be 1..100 and page must be positive')
    if args.action == 'search' and not (args.query and args.query.strip()):
        parser.error('search requires --query')
    if args.action == 'show' and not args.id:
        parser.error('show requires --id from list/search')
    if args.action == 'record-use' and not args.entry_id:
        parser.error('record-use requires at least one --entry-id from list/search')
    if args.query is not None and args.action != 'search':
        parser.error('--query applies only to search')
    if args.id is not None and args.action != 'show':
        parser.error('--id applies only to show')
    if args.entry_id is not None and args.action != 'record-use':
        parser.error('--entry-id applies only to record-use')
    if args.topic is not None and args.action in ('summary', 'record-use', 'refresh-summary'):
        parser.error('--topic does not apply to summary updates')
    if (args.limit != 20 or args.page != 1) and args.action not in ('list', 'search', 'check'):
        parser.error('pagination applies only to list/search/check')
    if (args.harness or args.instruction_file) and args.action != 'status':
        parser.error('--harness and --instruction-file apply only to status')
    root = repository_root(args.workspace)
    if args.action == 'summary':
        summary = summary_rows(root)
        if args.brief:
            summary.pop('sources')
        return {'workspace': str(root), 'action': args.action,
                'summary': summary}
    all_files = files(root)
    selected = all_files
    if args.topic:
        selected = [p for p in all_files if args.topic.casefold() in p.relative_to(root).as_posix().casefold()]
        if not selected:
            raise ValueError('No matching topic file; use agent retrieval for heading-based topics')
    result = {'workspace': str(root), 'action': args.action}
    if args.action == 'record-use':
        result['summary'] = refresh_summary(root, args.entry_id)
    elif args.action == 'refresh-summary':
        result['summary'] = refresh_summary(root)
    elif args.action == 'status':
        harness = args.harness or 'generic'
        if args.instruction_file:
            relative = Path(args.instruction_file)
            if relative.is_absolute() or relative.drive or '..' in relative.parts:
                raise ValueError('Instruction file must be workspace-relative without traversal')
            instructions = safe(root, root / relative)
        else:
            filename = {'claude': 'CLAUDE.md', 'gemini': 'GEMINI.md', 'copilot': '.github/copilot-instructions.md'}.get(harness, 'AGENTS.md')
            instructions = safe(root, root / filename)
            if harness == 'codex':
                override = safe(root, root / 'AGENTS.override.md')
                if override.is_file() and read(override).strip():
                    instructions = override
        pause_marker = safe(root, root / '.workspace-memory/PAUSED')
        result['writes_paused'] = pause_marker.exists()
        result['session_usage'] = 'Not observable by helper; use conversation state'
        result['harness'] = harness
        result['instruction_scope'] = 'Selected loader and fixed rule target only; imports and host execution not evaluated'
        instruction_text = read(instructions) if instructions.is_file() else ''
        rule_file = safe(root, root / '.workspace-memory/AGENTS.md')
        rule_text = read(rule_file) if rule_file.is_file() else ''
        loader_present = '.workspace-memory/AGENTS.md' in managed_block(instruction_text)
        rule_present = bool(managed_block(rule_text))
        index = root / '.workspace-memory/MEMORY.md'
        result.update(index_exists=index in all_files,
                      index_bytes=index.stat().st_size if index in all_files else 0,
                      topic_files=sum(p != index for p in selected),
                      memory_files=len(selected), empty=not any(scan(root, selected)),
                      loader_present=loader_present, managed_rule_present=rule_present,
                      setup_complete=loader_present and rule_present,
                      rule_file=str(rule_file),
                      instruction_file= str(instructions), audit=False)
    elif args.action == 'check':
        issues = check(root, selected, all_files)
        offset = (args.page - 1) * args.limit
        result.update(issues=issues[offset:offset + args.limit], total=len(issues),
                      has_more=len(issues) > offset + args.limit,
                      scope='Structural checks only; no factual verification or semantic deduplication')
    elif args.action == 'show':
        match = next((e for e in scan(root, selected) if e['id'] == args.id), None)
        if match is None:
            raise ValueError('Entry missing or changed; refresh list/search before selecting')
        result['entry'] = match
    else:
        words = args.query.casefold().split() if args.query else []
        offset, matches, output = (args.page - 1) * args.limit, 0, []
        for entry in scan(root, selected):
            haystack = (entry['file'] + ' ' + entry['heading'] + ' ' + entry['text']).casefold()
            if not all(word in haystack for word in words):
                continue
            matches += 1
            if matches <= offset:
                continue
            if len(output) == args.limit:
                break
            entry['summary'] = re.sub(r'\s+', ' ', entry.pop('text'))[:240]
            entry['number'] = matches
            output.append(entry)
        result.update(entries=output, page=args.page, has_more=matches > offset + args.limit)
    if args.brief:
        result['summary'].pop('sources')
    return result


if __name__ == '__main__':
    try:
        print(json.dumps(main(), ensure_ascii=True, separators=(',', ':')))
    except (OSError, ValueError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=True), file=sys.stderr)
        sys.exit(1)
