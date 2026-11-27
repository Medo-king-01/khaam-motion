import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def verify_snapshot_manifest(directory: Path) -> int:
    manifest = directory / 'UPSTREAM-MANIFEST.sha256'
    rows = manifest.read_text(encoding='utf-8').splitlines()
    for row in rows:
        expected, relative = row.split('  ', 1)
        path = directory / relative
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise AssertionError(f'upstream snapshot checksum mismatch: {path}')
    return len(rows)


class ExternalMotionCapabilitiesTest(unittest.TestCase):
    def test_reelforge_upstream_gallery_is_pinned_and_checksummed(self):
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        guide = (ROOT / 'reference' / 'verified-motion-workflow.md').read_text(encoding='utf-8')
        snapshot = ROOT / 'reference' / 'reelforge-gallery'
        index = json.loads((snapshot / 'gallery-index.json').read_text(encoding='utf-8'))

        self.assertIn('reference/reelforge-gallery/', skill)
        self.assertIn('740bf70dc1f068734e054e922c0a602e50f69ebd', guide)
        self.assertIn('not yet verified in Khaam', guide)
        self.assertEqual(len(index['entries']), 31)
        self.assertEqual(len(list((snapshot / 'fragments').rglob('*.html'))), 31)
        self.assertTrue((snapshot / 'UPSTREAM_LICENSE').is_file())
        self.assertTrue((snapshot / 'UPSTREAM_NOTICE').is_file())
        self.assertEqual(verify_snapshot_manifest(snapshot), 68)

    def test_tegaki_template_is_optional_pinned_project_local_remotion(self):
        template = ROOT / 'templates' / 'remotion' / 'tegaki'
        package = json.loads((template / 'package.json').read_text(encoding='utf-8'))
        source = (template / 'src' / 'ArabicHandwriting.tsx').read_text(encoding='utf-8')
        docs = (ROOT / 'reference' / 'tegaki.md').read_text(encoding='utf-8')
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        helper = (ROOT / 'scripts' / 'use_remotion_template.py').read_text(encoding='utf-8')

        self.assertEqual(package['dependencies']['tegaki'], '1.1.0')
        self.assertEqual(package['dependencies']['remotion'], '4.0.529')
        self.assertIn('tegaki', helper)
        self.assertIn('time={{ mode: \'controlled\'', source)
        self.assertIn('useCurrentFrame', source)
        self.assertIn('direction="rtl"', source)
        self.assertIn('npm install --save-exact tegaki@1.1.0', docs)
        self.assertIn('never part of required setup', skill)
        self.assertIn('reference/tegaki-upstream/examples/remotion/', docs)
        self.assertTrue((ROOT / 'reference' / 'tegaki-upstream' / 'UPSTREAM_LICENSE').is_file())
        for path in ('src/index.ts', 'src/Root.tsx', 'src/ArabicHandwriting.tsx', 'KHAAM-INTEGRATION.md', 'package-lock.json'):
            self.assertTrue((template / path).is_file(), path)

    def test_tegaki_upstream_remotion_examples_and_licenses_are_checksummed(self):
        snapshot = ROOT / 'reference' / 'tegaki-upstream'
        self.assertTrue((snapshot / 'SOURCE-NOTICE.md').is_file())
        self.assertTrue((snapshot / 'FONTS-LICENSE.md').is_file())
        self.assertTrue((snapshot / 'examples' / 'remotion' / 'src' / 'Root.tsx').is_file())
        self.assertEqual(verify_snapshot_manifest(snapshot), 41)


if __name__ == '__main__':
    unittest.main()
