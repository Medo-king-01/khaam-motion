"""Smoke tests for optional local tools; skip cleanly after a cache reset."""
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
CREATIVE = ROOT / 'integrations' / 'creative'
AUDIO = ROOT / '.cache' / 'creative-tools' / 'audio-env' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
SHOTCRAFT = ROOT / '.cache' / 'creative-tools' / 'video-shotcraft'


class OptionalCreativeTest(unittest.TestCase):
    @unittest.skipUnless((CREATIVE / 'node_modules' / 'three').exists(), 'Node dependencies not installed')
    def test_node_cpu_smoke(self):
        subprocess.run(['node', str(CREATIVE / 'smoke.mjs')], cwd=ROOT, check=True, timeout=60, capture_output=True, text=True)

    @unittest.skipUnless(AUDIO.is_file(), 'Optional audio environment not installed')
    def test_librosa_onsets_with_existing_script(self):
        with tempfile.TemporaryDirectory() as temp:
            audio = Path(temp) / 'pulse.wav'
            output = Path(temp) / 'onsets.json'
            sample_rate = 22050
            with wave.open(str(audio), 'wb') as w:
                w.setparams((1, 2, sample_rate, sample_rate * 3, 'NONE', 'not compressed'))
                values = []
                for i in range(sample_rate * 3):
                    delta = min(abs(i - n) for n in (8000, 22050, 36000, 50000))
                    value = int(16000 * math.sin(i * .45) * (1 - delta / 250)) if delta < 250 else 0
                    values.append(struct.pack('<h', value))
                w.writeframes(b''.join(values))
            env = dict(os.environ, NUMBA_CACHE_DIR=str(Path(temp) / 'numba'))
            subprocess.run([str(AUDIO), str(ROOT / 'scripts' / 'audio_tag.py'), str(audio), '--onsets', '--json', str(output)],
                           cwd=ROOT, env=env, check=True, timeout=90, capture_output=True, text=True)
            self.assertGreater(len(json.loads(output.read_text())[str(audio)]['onsets']), 0)

    @unittest.skipUnless(SHOTCRAFT.is_dir(), 'Optional video-shotcraft source not installed')
    def test_shotcraft_reference_source(self):
        self.assertTrue((SHOTCRAFT / 'SKILL.md').is_file())
        self.assertGreater(len(list((SHOTCRAFT / 'references' / 'shots').rglob('*.md'))), 100)


if __name__ == '__main__':
    unittest.main()
