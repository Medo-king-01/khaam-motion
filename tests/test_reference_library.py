import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reference_library', ROOT / 'integrations/creative/reference_library.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReferenceLibraryTest(unittest.TestCase):
    def test_search_both_sources_without_emitting_prompt_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for name in module.SOURCES:
                folder = base / name / 'prompts'
                folder.mkdir(parents=True)
                (folder / 'example.md').write_text('# Kinetic typography\nsecret text about product\n', encoding='utf-8')
                (folder / 'other.md').write_text('# Other\nno match\n', encoding='utf-8')
            found = module.search('KINETIC product', 10, base)
            self.assertEqual(len(found), 2)
            self.assertEqual({r['source'] for r in found}, set(module.SOURCES))
            self.assertTrue(all('github.com/' in r['upstream'] for r in found))
            self.assertNotIn('secret text', str(found))
            self.assertEqual(len(module.search('kinetic', 1, base)), 1)
            self.assertEqual(module.search('absent', 10, base), [])
            with self.assertRaises(ValueError):
                module.search(' ', 10, base)

    def test_installer_does_not_overwrite_unrecognized_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target = base / next(iter(module.SOURCES))
            target.mkdir()
            (target / 'keep').write_text('safe')
            with self.assertRaises(SystemExit):
                module.install_all(base)
            self.assertEqual((target / 'keep').read_text(), 'safe')


if __name__ == '__main__':
    unittest.main()
