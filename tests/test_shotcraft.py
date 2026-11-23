"""The video-shotcraft integration: our guide, its wiring, and the pinned source."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'reference' / 'shotcraft.md'
SHOTCRAFT = ROOT / '.cache' / 'creative-tools' / 'video-shotcraft'


class ShotcraftGuideTest(unittest.TestCase):
    def test_guide_exists_and_is_wired_into_the_routing_docs(self):
        self.assertTrue(GUIDE.is_file())
        for doc in ('SKILL.md', 'AGENTS.md', 'reference/external-creative-tools.md'):
            self.assertIn('reference/shotcraft.md', (ROOT / doc).read_text(encoding='utf-8'),
                          f'{doc} must route product/UI promos to reference/shotcraft.md')

    def test_guide_covers_licences_and_hard_limits(self):
        text = GUIDE.read_text(encoding='utf-8')
        for token in ('Apache-2.0', 'Remotion', 'ATTRIBUTION',
                      '59f3e9b9e936ff2bce0e18446226d770a3f2f61f',
                      'Never execute its scripts', '.cache/creative-tools/video-shotcraft/',
                      'HyperFrames', 'dir="rtl"'):
            self.assertIn(token, text, f'guide must mention: {token}')

    def test_guide_pin_matches_the_verified_installer(self):
        setup_py = (ROOT / 'integrations' / 'creative' / 'setup.py').read_text(encoding='utf-8')
        m = re.search(r"SHOTCRAFT_REVISION = '([0-9a-f]{40})'", setup_py)
        self.assertIsNotNone(m, 'setup.py must pin the shotcraft commit')
        self.assertIn(m.group(1), GUIDE.read_text(encoding='utf-8'),
                      'the guide must state the same pinned commit as the verified installer')
        self.assertIn('SHOTCRAFT_SHA256', setup_py, 'the installer must verify the download')

    def test_guide_does_not_copy_upstream_card_text(self):
        # an idea boundary: our guide paraphrases in our words and never ships a card body
        text = GUIDE.read_text(encoding='utf-8')
        self.assertNotIn('动效核心', text)
        self.assertNotIn('参数表', text)

    @unittest.skipUnless(SHOTCRAFT.is_dir(), 'Optional video-shotcraft source not cached')
    def test_cached_library_is_the_pinned_release(self):
        marker = SHOTCRAFT / '.khaam-revision'
        self.assertTrue(marker.is_file())
        self.assertEqual(marker.read_text(encoding='utf-8').strip(),
                         '59f3e9b9e936ff2bce0e18446226d770a3f2f61f')
        cards = [p for p in (SHOTCRAFT / 'references' / 'shots').rglob('*.md')
                 if p.name != 'ATTRIBUTION.md']
        self.assertEqual(len(cards), 124)


if __name__ == '__main__':
    unittest.main()
