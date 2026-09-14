"""Run with python -B scripts/test_memory.py; fixtures stay in temporary directories."""
import importlib.util
import contextlib
import io
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('memory', Path(__file__).with_name('memory.py'))
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def put(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        return target

    def call(self, action, *args):
        return memory.main([action, '--workspace', str(self.root), *args])

    def test_empty_read_operations_do_not_create_memory(self):
        self.assertTrue(self.call('status')['empty'])
        self.assertEqual(self.call('list')['entries'], [])
        self.assertEqual(self.call('check')['issues'], [])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_pagination_search_unicode_and_stale_selection(self):
        path = self.put('.workspace-memory/MEMORY.md', '# Memory\n\n## Decisions\n- **Auth:** Separate keys.\n  Keep signing private.\n- **Testing:** Isolate databases.\n- বাংলা তথ্য\n')
        before = path.read_bytes()
        page = self.call('list', '--limit', '1')
        self.assertTrue(page['has_more'])
        self.assertEqual(len(page['entries']), 1)
        selected = page['entries'][0]['id']
        self.assertIn('Keep signing private.', self.call('show', '--id', selected)['entry']['text'])
        second = self.call('list', '--limit', '1', '--page', '2')
        self.assertIn('Testing', second['entries'][0]['summary'])
        self.assertEqual(len(self.call('search', '--query', 'বাংলা')['entries']), 1)
        self.assertEqual(path.read_bytes(), before)
        path.write_text(before.decode().replace('Separate keys.', 'Rotate keys.'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.call('show', '--id', selected)

    def test_scaffolding_excluded_and_structural_issues_found(self):
        self.put('.workspace-memory/MEMORY.md', '# Workspace Memory\n> Instructions\n<!-- hidden -->\n## Core\n- Keep boundaries.\n## Memory Index\n- [Auth](topics/auth.md)\n- [Missing](topics/missing.md)\n')
        self.put('.workspace-memory/topics/auth.md', '# Auth\n- Keep boundaries.\n')
        self.put('.workspace-memory/topics/other.md', '# Other\n- Another fact.\n')
        self.put('.workspace-memory/topics/README.md', '# Guidance\n- Not a fact.\n')
        entries = self.call('list')['entries']
        self.assertEqual(len(entries), 3)
        kinds = {item['kind'] for item in self.call('check')['issues']}
        self.assertEqual(kinds, {'broken-index-link', 'unindexed-topic', 'exact-duplicate'})

    def test_outside_index_link_not_followed(self):
        self.put('.workspace-memory/MEMORY.md', '# Memory\n## Memory Index\n- [Outside](../../outside.md)\n')
        self.assertEqual(self.call('check')['issues'][0]['kind'], 'unsafe-index-link')
        with self.assertRaises(ValueError):
            memory.safe(self.root, self.root / '../outside.md')

    def test_symlink_refused(self):
        outside = self.put('elsewhere.md', '- Must not read.\n')
        folder = self.root / '.workspace-memory/topics'
        folder.mkdir(parents=True)
        try:
            (folder / 'linked.md').symlink_to(outside)
        except OSError:
            self.skipTest('Creating symlinks is unavailable on this host')
        with self.assertRaisesRegex(ValueError, 'Linked'):
            self.call('list')

    def test_invalid_arguments_and_no_matching_topic(self):
        for args in [('search',), ('show',), ('list', '--limit', '0'), ('list', '--query', 'x')]:
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.call(*args)
        with self.assertRaisesRegex(ValueError, 'No matching'):
            self.call('list', '--topic', 'missing')

    def test_fenced_headings_not_parsed_as_entries(self):
        self.put('.workspace-memory/MEMORY.md', '# Memory\n## Decisions\n- Use this workflow:\n  ```text\n  # not a heading\n  - not a second fact\n  ```\n- Next fact.\n')
        result = self.call('list')['entries']
        self.assertEqual(len(result), 2)
        self.assertIn('not a second fact', self.call('show', '--id', result[0]['id'])['entry']['text'])

    def test_nested_index_sections_are_not_knowledge(self):
        self.put('.workspace-memory/MEMORY.md', '# Memory\n## Memory Index\n### Backend\n- [Auth](topics/auth.md)\n## Decisions\n- Keep this fact.\n')
        result = self.call('list')['entries']
        self.assertEqual(len(result), 1)
        self.assertIn('Keep this fact', result[0]['summary'])

    def test_directory_access_failure_is_not_empty_memory(self):
        (self.root / '.workspace-memory/topics').mkdir(parents=True)
        def denied(*args, **kwargs):
            kwargs['onerror'](PermissionError('Cannot read topic directory'))
            return iter(())
        with patch.object(memory.os, 'walk', side_effect=denied):
            with self.assertRaises(PermissionError):
                self.call('list')

    def test_status_rejects_incomplete_or_reversed_markers(self):
        begin, end = '<!-- workspace-memory:begin -->', '<!-- workspace-memory:end -->'
        for text in (begin, end + begin, begin + end + begin):
            self.put('.workspace-memory/AGENTS.md', text)
            self.assertFalse(self.call('status')['managed_rule_present'])
        self.put('.workspace-memory/AGENTS.md', begin + '\nMemory rule\n' + end)
        self.assertTrue(self.call('status')['managed_rule_present'])

    def test_pause_status_does_not_create_or_list_control_as_knowledge(self):
        self.assertFalse(self.call('status')['writes_paused'])
        self.assertEqual(list(self.root.iterdir()), [])
        marker = self.put('.workspace-memory/PAUSED', 'Writes paused')
        self.assertTrue(self.call('status')['writes_paused'])
        self.assertEqual(self.call('list')['entries'], [])
        self.assertEqual(marker.read_text(), 'Writes paused')
        marker.unlink()
        self.assertFalse(self.call('status')['writes_paused'])

    def test_host_specific_status_and_override_scope(self):
        self.put('.workspace-memory/AGENTS.md', '<!-- workspace-memory:begin -->\nRule\n<!-- workspace-memory:end -->')
        rule = '<!-- workspace-memory:begin -->\nRead .workspace-memory/AGENTS.md\n<!-- workspace-memory:end -->'
        for filename in ('AGENTS.md', 'CLAUDE.md', 'GEMINI.md', '.github/copilot-instructions.md'):
            self.put(filename, rule)
        self.put('AGENTS.override.md', 'Unrelated Codex override')
        for host, filename in (('claude', 'CLAUDE.md'), ('gemini', 'GEMINI.md'),
                               ('opencode', 'AGENTS.md'), ('cursor', 'AGENTS.md'),
                               ('copilot', '.github/copilot-instructions.md'),
                               ('generic', 'AGENTS.md'), ('codex', 'AGENTS.override.md')):
            result = self.call('status', '--harness', host)
            self.assertEqual(Path(result['instruction_file']).relative_to(self.root).as_posix(), filename)
            self.assertTrue(result['managed_rule_present'])
            self.assertEqual(result['setup_complete'], host != 'codex')

    def test_custom_instruction_path_and_invalid_options(self):
        self.put('.workspace-memory/AGENTS.md', '<!-- workspace-memory:begin -->\nRule\n<!-- workspace-memory:end -->')
        rule = '<!-- workspace-memory:begin -->\nRead .workspace-memory/AGENTS.md\n<!-- workspace-memory:end -->'
        self.put('.claude/CLAUDE.md', rule)
        self.assertTrue(self.call('status', '--instruction-file', '.claude/CLAUDE.md')['setup_complete'])
        for path in ('../outside.md', str(self.root / 'absolute.md')):
            with self.assertRaises(ValueError):
                self.call('status', '--instruction-file', path)
        for args in (('list', '--harness', 'claude'), ('check', '--instruction-file', 'AGENTS.md')):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.call(*args)

    def test_loader_requires_rule_and_neither_is_saved_knowledge(self):
        self.put('AGENTS.md', '<!-- workspace-memory:begin -->\nRead .workspace-memory/AGENTS.md\n<!-- workspace-memory:end -->')
        status = self.call('status')
        self.assertTrue(status['loader_present'])
        self.assertFalse(status['setup_complete'])
        self.put('.workspace-memory/AGENTS.md', '<!-- workspace-memory:begin -->\n- Instruction, not knowledge.\n<!-- workspace-memory:end -->')
        self.assertTrue(self.call('status')['setup_complete'])
        self.assertTrue(self.call('status')['empty'])
        self.assertEqual(self.call('list')['entries'], [])
        self.assertEqual(self.call('check')['issues'], [])
        self.put('AGENTS.md', '<!-- workspace-memory:begin -->\nUnrelated block\n<!-- workspace-memory:end -->')
        self.assertFalse(self.call('status')['setup_complete'])

    def test_cli_returns_bounded_json_for_large_memory(self):
        content = '# Memory\n## Decisions\n' + ''.join(
            '- Fact %d: %s\n' % (i, 'Important verified detail. ' * 40) for i in range(200))
        path = self.put('.workspace-memory/MEMORY.md', content)
        run = subprocess.run([sys.executable, '-B', str(Path(memory.__file__)),
                              'list', '--workspace', str(self.root), '--limit', '5'],
                             capture_output=True, text=True, check=True)
        result = json.loads(run.stdout)
        self.assertEqual(len(result['entries']), 5)
        self.assertTrue(result['has_more'])
        self.assertLess(len(run.stdout.encode()), path.stat().st_size // 10)
        self.assertEqual(path.read_text(encoding='utf-8'), content)


if __name__ == '__main__':
    unittest.main()
