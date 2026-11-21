from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AdaptiveDirectionTest(unittest.TestCase):
    def test_entrypoint_references_existing_guide(self):
        entrypoint = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        path = ROOT / 'reference' / 'adaptive-direction.md'
        self.assertTrue(path.is_file())
        self.assertIn('reference/adaptive-direction.md', entrypoint)
        guide = path.read_text(encoding='utf-8')
        for linked_guide in ('reference/arabic-typography.md', 'reference/hyperframes.md', 'reference/film-sound.md'):
            self.assertIn(linked_guide, guide)
            self.assertTrue((ROOT / linked_guide).is_file())

    def test_no_new_approval_or_music_default(self):
        guide = (ROOT / 'reference' / 'adaptive-direction.md').read_text(encoding='utf-8')
        self.assertIn('no music unless requested', guide)
        self.assertIn('not isolated letters', guide)
        self.assertIn('mark precisely what remains unverified', guide)
        self.assertIn('rather than creating motion for its own sake', guide)


if __name__ == '__main__':
    unittest.main()
