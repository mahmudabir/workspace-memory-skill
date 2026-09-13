"""Create a new file from a reviewed source/template, byte for byte.

No Markdown parsing, generated headings, substitutions, or overwrites.
Python 3.9+; standard library only.
"""
import argparse
import json
from pathlib import Path
import sys


def create_file(source, destination):
    source, destination = Path(source), Path(destination)
    content = source.read_bytes()
    # Require the caller to choose and prepare the destination directory explicitly.
    # Exclusive creation preserves any existing file, including an empty one.
    with destination.open('xb') as output:
        output.write(content)
    if destination.read_bytes() != content:
        raise OSError('Created file does not match the reviewed source')
    return {'created': str(destination.absolute()), 'bytes': len(content)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(create_file(args.source, args.destination), ensure_ascii=True))
    except OSError as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=True), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
