"""motion_sound.py: real-recording suggestions for Alansari motion IDs — sound v2 first."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'motion_sound.py'


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


class MotionSoundTest(unittest.TestCase):
    def test_check_passes(self):
        result = run('--check')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertTrue(json.loads(result.stdout)['ok'])

    def test_known_motion_resolves_to_its_category_and_file(self):
        for motion, category in [('M-001', 'TXT'), ('M-006', 'EMP'), ('M-011', 'CAP'),
                                 ('M-016', 'TRN'), ('M-021', 'CAM'), ('M-026', 'FX'),
                                 ('M-031', 'SOC'), ('M-036', 'LGO'), ('M-201', 'PER'),
                                 ('M-214', 'AUD'), ('M-226', 'SCR'), ('M-241', 'TRK'),
                                 ('M-249', 'D3'), ('M-259', 'TIM'), ('M-1000', 'SOC')]:
            out = json.loads(run(motion).stdout)
            self.assertEqual(out['motion'], motion)
            self.assertEqual(out['category'], category)
            self.assertTrue((ROOT / out['category_file']).is_file(), out['category_file'])

    def test_word_pop_suggests_real_recordings_not_sx_mp3s(self):
        out = json.loads(run('M-012').stdout)
        self.assertTrue(out['real_candidates'])
        for candidate in out['real_candidates']:
            self.assertTrue(candidate.startswith('sounds/library/'))
            self.assertTrue((ROOT / candidate).is_file(), candidate)
        self.assertIn('sound v2', out['note'])

    def test_audio_family_gets_silence_guidance_not_invented_sounds(self):
        out = json.loads(run('M-214').stdout)
        self.assertEqual(out['real_candidates'], [])
        self.assertIn('voice IS the audio', out['note'])

    def test_design_families_are_not_motions(self):
        out = json.loads(run('CS-02').stdout)
        self.assertEqual(out['real_candidates'], [])
        self.assertIn('not a motion family', out['note'])

    def test_invalid_id_exits_2(self):
        result = run('banana')
        self.assertEqual(result.returncode, 2)
        result = run('M-9999')
        self.assertEqual(result.returncode, 2)

    def test_unpadded_input_normalizes(self):
        self.assertEqual(json.loads(run('M-12').stdout)['motion'], 'M-012')


if __name__ == '__main__':
    unittest.main()
