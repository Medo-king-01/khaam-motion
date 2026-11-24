"""The HyperFrames starter is pinned to what the skill owns, offline-capable."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'templates' / 'hyperframes'
PINNED_REGISTRY_COMMIT = 'add940201ebe5903c540232210e8f79264ef3a86'
GSAP_SNAPSHOT_COMMIT = '5e6c35ff8eedea12d4f229129def635277d8b0f2'


class HyperframesTemplateTest(unittest.TestCase):
    def test_registry_is_pinned_to_the_vendored_snapshot_commit(self):
        cfg = json.loads((TEMPLATE / 'hyperframes.json').read_text(encoding='utf-8'))
        registry = cfg['registry']
        self.assertIn(PINNED_REGISTRY_COMMIT, registry)
        self.assertNotIn('/main', registry)
        self.assertNotIn('refs/heads', registry)

    def test_no_remote_script_or_stylesheet_is_loaded(self):
        html = (TEMPLATE / 'index.html').read_text(encoding='utf-8')
        remote_tags = re.findall(r'<(?:script|link)[^>]*(?:src|href)\s*=\s*"https?://', html, re.I)
        self.assertEqual(remote_tags, [])

    def test_gsap_is_the_vendored_copy_byte_for_byte(self):
        template_js = TEMPLATE / 'vendor' / 'gsap.min.js'
        snapshot_js = ROOT / 'integrations' / 'gsap' / 'dist' / 'gsap.min.js'
        self.assertTrue(template_js.is_file())
        self.assertEqual(
            hashlib.sha256(template_js.read_bytes()).hexdigest(),
            hashlib.sha256(snapshot_js.read_bytes()).hexdigest(),
        )

    def test_gsap_notice_records_provenance(self):
        notice = (TEMPLATE / 'vendor' / 'GSAP-NOTICE.md').read_text(encoding='utf-8')
        self.assertIn(GSAP_SNAPSHOT_COMMIT, notice)
        self.assertIn('GSAP Standard License', notice)
        self.assertIn('3d1bea374ab1b703cc5c4105358eec63c4465efdc573931dc116e34a0a190c1b', notice)


if __name__ == '__main__':
    unittest.main()
