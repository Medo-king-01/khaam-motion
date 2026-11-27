from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RequiredSoundLibrarySetupTest(unittest.TestCase):
    def test_setup_requires_verified_library_before_first_video(self):
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        start = (ROOT / 'START-HERE.md').read_text(encoding='utf-8')
        compatibility = (ROOT / 'reference' / 'agent-compatibility.md').read_text(encoding='utf-8')
        sound = (ROOT / 'reference' / 'sound-library.md').read_text(encoding='utf-8')

        self.assertIn('Required sound library setup (before the first video)', skill)
        self.assertIn('scripts/install_sounds.py', skill)
        self.assertIn('Required sound-library setup, before the first video.', start)
        self.assertIn('scripts/install_sounds.py all', start)
        self.assertIn('required to complete standard setup', compatibility)
        self.assertIn('not an optional add-on', sound)
        self.assertIn('khaam_sound_library.installed: true', sound)
        self.assertNotIn('Offer the sound library (once)', start)
        self.assertNotIn('sounds_choice', skill + start + sound)

    def test_shipped_real_recording_pack_remains_available(self):
        bundled = ROOT / 'sounds' / 'library'
        recordings = list(bundled.glob('*.flac'))
        self.assertEqual(len(recordings), 33)
        self.assertTrue((bundled / 'MANIFEST.md').is_file())
        self.assertTrue((ROOT / 'scripts' / 'install_sounds.py').is_file())


if __name__ == '__main__':
    unittest.main()
