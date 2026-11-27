"""Product-launch guidance is wired in without replacing Khaam's workflow."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'reference' / 'product-launch-films.md'
BRIEF = ROOT / 'templates' / 'product-launch-brief.md'
SOURCE_COMMIT = 'edbfb105382f21507bad895d8b5f6e0faa67487c'


class ProductLaunchFilmGuideTest(unittest.TestCase):
    def test_guide_and_optional_brief_exist_and_are_routed(self):
        self.assertTrue(GUIDE.is_file())
        self.assertTrue(BRIEF.is_file())
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('reference/product-launch-films.md', skill)
        self.assertIn('templates/product-launch-brief.md', skill)

    def test_source_provenance_and_adaptation_boundary_are_explicit(self):
        guide = GUIDE.read_text(encoding='utf-8')
        changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        for text in (guide, changelog):
            self.assertIn(SOURCE_COMMIT, text)
            self.assertIn('MIT', text)
        for token in ('لا يضيف هذا الدليل بوابة موافقة', 'العربية/RTL', 'sound v2', 'الإثبات',
                      'الملف النهائي المشفر', 'تسجيل حي'):
            self.assertIn(token, guide, f'guide must preserve or address: {token}')

    def test_cursor_choreography_covers_travel_click_feedback_and_result(self):
        guide = GUIDE.read_text(encoding='utf-8')
        for token in ('كوريوغرافيا المؤشر والنقرة', 'انتقال مقصود', 'وصول وتحويم',
                      'ضغطة قابلة للقراءة', 'استجابة المنتج', '05-camera-3d-cursor.md',
                      'scripts/cues.py', 'لا تولّد SFX للنقرة'):
            self.assertIn(token, guide, f'cursor guidance must cover: {token}')

    def test_hyperframes_cursor_starter_is_deterministic_and_wired(self):
        template = ROOT / 'templates' / 'hyperframes' / 'compositions' / 'product-cursor-demo.html'
        self.assertTrue(template.is_file())
        text = template.read_text(encoding='utf-8')
        for token in ('data-composition-id="product-cursor-demo"', 'window.__timelines["product-cursor-demo"]',
                      'TRAVEL', 'CLICK', 'pl-ripple', 'labelDone', 'window.cue',
                      'verified and is authorized', 'GSAP'):
            self.assertIn(token, text)
        self.assertNotIn('https://', text)
        self.assertNotIn('tl.call(', text, 'UI state must remain reversible on arbitrary frame seeks')

    def test_click_audio_uses_the_real_khaam_recording_and_sound_policy(self):
        guide = GUIDE.read_text(encoding='utf-8')
        manifest = (ROOT / 'sounds' / 'library' / 'MANIFEST.md').read_text(encoding='utf-8')
        self.assertTrue((ROOT / 'sounds' / 'library' / 'button-click.flac').is_file())
        self.assertIn('"lib": "button-click"', guide)
        self.assertIn('an interface button click', manifest)
        self.assertIn('لا تولّد SFX للنقرة', guide)
        self.assertIn('check_mix.py', guide)

    def test_guide_keeps_existing_gates_engine_and_sound_policy_authoritative(self):
        guide = GUIDE.read_text(encoding='utf-8')
        for token in ('بوابات Khaam الحالية A/B/C', 'HyperFrames', 'لا صوت', 'تسجيلات حقيقية',
                      'لا تثبّت', 'قصد المستخدم'):
            self.assertIn(token, guide, f'guide must preserve Khaam policy: {token}')
        self.assertIn('بوابة اعتماد جديدة', BRIEF.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
