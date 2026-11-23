"""The mg-styles-15 integration: our guide, its wiring, and the pinned source."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'reference' / 'mg-styles-15.md'
JURY = ROOT / 'reference' / 'review-jury.md'
CACHE = ROOT / '.cache' / 'creative-tools' / 'mg-styles-15'


class MgStylesGuideTest(unittest.TestCase):
    def test_guides_exist_and_are_wired_into_the_routing_docs(self):
        for path in (GUIDE, JURY):
            self.assertTrue(path.is_file())
        for doc in ('SKILL.md', 'AGENTS.md', 'reference/external-creative-tools.md'):
            text = (ROOT / doc).read_text(encoding='utf-8')
            self.assertIn('reference/mg-styles-15.md', text,
                          f'{doc} must route style direction to reference/mg-styles-15.md')
            self.assertIn('reference/review-jury.md', text,
                          f'{doc} must route the jury pass to reference/review-jury.md')

    def test_guide_covers_licences_and_hard_limits(self):
        text = GUIDE.read_text(encoding='utf-8')
        for token in ('MIT', 'VCSL', 'Open Font License',
                      '46fd009ff0988be7ab1d9a64dfe14e501c6c2521',
                      'e980b4b289fb133dfece3112660b6d041a0559bfafadc9196ea9cd4e2eb037c9',
                      'Never execute its scripts', '.cache/creative-tools/mg-styles-15/',
                      'HyperFrames', 'dir="rtl"', 'mgaudio', 'film-sound.md'):
            self.assertIn(token, text, f'guide must mention: {token}')

    def test_jury_guide_credits_its_mit_source_and_keeps_our_qa_mandatory(self):
        text = JURY.read_text(encoding='utf-8')
        self.assertIn('rubric.md', text)
        self.assertIn('MIT', text)
        self.assertIn('Vincentwei1021', text)
        self.assertIn('check_mix.py', text, 'the jury pass must not replace our internal checks')
        self.assertIn('check_pace.py', text)

    def test_guide_pin_matches_the_verified_installer(self):
        setup_py = (ROOT / 'integrations' / 'creative' / 'setup.py').read_text(encoding='utf-8')
        m = re.search(r"MGSTYLES_REVISION = '([0-9a-f]{40})'", setup_py)
        self.assertIsNotNone(m, 'setup.py must pin the mg-styles-15 commit')
        self.assertIn(m.group(1), GUIDE.read_text(encoding='utf-8'),
                      'the guide must state the same pinned commit as the verified installer')
        self.assertIn('MGSTYLES_SHA256', setup_py, 'the installer must verify the download')
        for excluded in ("'videos'", "'lib'", "'assets'", "'site'"):
            self.assertIn(excluded, setup_py,
                          f'the installer must exclude {excluded} from the extracted cache')

    def test_no_upstream_prompt_text_is_copied_into_this_skill(self):
        # an idea boundary: our docs paraphrase in our words and never ship an upstream prompt body
        for path in (GUIDE, JURY, ROOT / 'reference' / 'external-creative-tools.md'):
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('You are the director, motion designer, engineer', text)
            self.assertNotIn('one-continuous-shot brand explainer', text.lower())

    @unittest.skipUnless(CACHE.is_dir(), 'Optional mg-styles-15 source not cached')
    def test_cached_library_is_the_pinned_release(self):
        marker = CACHE / '.khaam-revision'
        self.assertTrue(marker.is_file())
        self.assertEqual(marker.read_text(encoding='utf-8').strip(),
                         '46fd009ff0988be7ab1d9a64dfe14e501c6c2521')
        self.assertEqual(len(list((CACHE / 'prompts').glob('*.md'))), 15)
        self.assertTrue((CACHE / 'rubric.md').is_file())
        self.assertTrue((CACHE / 'template.md').is_file())
        self.assertTrue((CACHE / 'LICENSE').is_file())
        self.assertFalse((CACHE / 'videos').exists(), 'the 441 MB videos must not be cached')
        self.assertFalse((CACHE / 'lib').exists(), 'mgaudio must not be cached')
        self.assertFalse((CACHE / 'assets').exists(), 'unverified textures must not be cached')


if __name__ == '__main__':
    unittest.main()
