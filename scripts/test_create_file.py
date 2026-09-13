import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('create_file', Path(__file__).with_name('create_file.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CreateFileTests(unittest.TestCase):
    def test_copies_arbitrary_structure_and_encoding_verbatim(self):
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder) / 'sample', Path(folder) / 'output'
            for content in [b'', b'\xef\xbb\xbf# Changed\r\n\r\n| table |\r\n', 'বাংলা\n{"new": [1, 2]}'.encode()]:
                source.write_bytes(content)
                module.create_file(source, destination)
                self.assertEqual(destination.read_bytes(), content)
                destination.unlink()

    def test_existing_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder) / 'sample', Path(folder) / 'output'
            source.write_bytes(b'new')
            destination.write_bytes(b'existing knowledge')
            with self.assertRaises(FileExistsError):
                module.create_file(source, destination)
            self.assertEqual(destination.read_bytes(), b'existing knowledge')

    def test_missing_source_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'output'
            with self.assertRaises(FileNotFoundError):
                module.create_file(Path(folder) / 'missing', destination)
            self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
