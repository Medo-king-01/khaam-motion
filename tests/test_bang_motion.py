"""The bang-motion integration: our guide, its wiring, and the pinned source."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'reference' / 'bang-motion.md'
CACHE = ROOT / '.cache' / 'creative-tools' / 'bang-motion'


class BangMotionGuideTest(unittest.TestCase):
    def test_guide_exists_and_is_wired_into_the_routing_docs(self):
        self.assertTrue(GUIDE.is_file())
        for doc in ('SKILL.md', 'AGENTS.md', 'reference/external-creative-tools.md'):
            self.assertIn('reference/bang-motion.md', (ROOT / doc).read_text(encoding='utf-8'),
                          f'{doc} must route openers/promos to reference/bang-motion.md')

    def test_guide_covers_licences_and_hard_limits(self):
        text = GUIDE.read_text(encoding='utf-8')
        for token in ('MIT', 'c1aa65e921c970d858705fcb4a53a8294d1a4131',
                      'de5a744da80faf97b53ad0909f57cf21751ccf0124435b7f4e6fff7ecbcc39a9',
                      'Never install, register or enable', '.cache/creative-tools/bang-motion/',
                      'HyperFrames', 'film-sound.md', 'arabic-typography.md'):
            self.assertIn(token, text, f'guide must mention: {token}')

    def test_guide_pin_matches_the_verified_installer(self):
        setup_py = (ROOT / 'integrations' / 'creative' / 'setup.py').read_text(encoding='utf-8')
        m = re.search(r"BANG_REVISION = '([0-9a-f]{40})'", setup_py)
        self.assertIsNotNone(m, 'setup.py must pin the bang-motion commit')
        self.assertIn(m.group(1), GUIDE.read_text(encoding='utf-8'),
                      'the guide must state the same pinned commit as the verified installer')
        self.assertIn('BANG_SHA256', setup_py, 'the installer must verify the download')
        for excluded in ("'docs'", "'.claude-plugin'", "'icon.png'"):
            self.assertIn(excluded, setup_py,
                          f'the installer must exclude {excluded} from the extracted cache')

    def test_guide_paraphrases_in_our_words(self):
        # an idea boundary: our guide paraphrases; it never ships an upstream body
        text = GUIDE.read_text(encoding='utf-8')
        self.assertNotIn('Larangan struktural', text)
        self.assertNotIn('Hukum #1', text)
        self.assertNotIn('tidak boleh menyentuh sendi', text)

    @unittest.skipUnless(CACHE.is_dir(), 'Optional bang-motion source not cached')
    def test_cached_library_is_the_pinned_release(self):
        marker = CACHE / '.khaam-revision'
        self.assertTrue(marker.is_file())
        self.assertEqual(marker.read_text(encoding='utf-8').strip(),
                         'c1aa65e921c970d858705fcb4a53a8294d1a4131')
        self.assertEqual(len(list((CACHE / 'references').glob('*.md'))), 8)
        self.assertTrue((CACHE / 'SKILL.md').is_file())
        self.assertTrue((CACHE / 'LICENSE').is_file())
        self.assertFalse((CACHE / 'docs').exists(), 'the gallery screenshots must not be cached')
        self.assertFalse((CACHE / '.claude-plugin').exists(), 'plugin metadata must not be cached')


if __name__ == '__main__':
    unittest.main()
