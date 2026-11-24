"""Vendored integrations are part of the skill (built-in), not optional add-ons."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = [
    'anything2explainer', 'awesome-canvas', 'awesome-lottie', 'creative', 'css-doodle',
    'drei', 'gl-transitions', 'gsap', 'helios', 'html-video', 'hyperframes', 'lottie-web',
    'lucide-icons', 'magicui', 'mojs', 'motion-canvas', 'particles.js', 'recharts',
    'simple-icons', 'tabler-icons', 'three.js', 'tsparticles',
]
PROVENANCE = [
    'KHAAM-INTEGRATION.md', 'README.md', 'UPSTREAM_LICENSE', 'UPSTREAM_README.md',
    'LICENSE', 'LICENSE.md', 'NOTICE.md',
]


class IntegrationsBuiltInTest(unittest.TestCase):
    def test_all_vendored_integrations_exist_and_are_non_empty(self):
        for name in VENDOR:
            d = ROOT / 'integrations' / name
            self.assertTrue(d.is_dir(), name)
            self.assertTrue(any(True for _ in d.iterdir()), '%s is empty' % name)

    def test_each_snapshot_carries_provenance_or_licence_paperwork(self):
        for name in VENDOR:
            d = ROOT / 'integrations' / name
            self.assertTrue(any((d / c).is_file() for c in PROVENANCE), name)

    def test_khaam_integration_notes_record_snapshot_commits(self):
        notes = sorted((ROOT / 'integrations').glob('*/KHAAM-INTEGRATION.md'))
        self.assertGreaterEqual(len(notes), 21)
        for note in notes:
            self.assertIn('Snapshot commit', note.read_text(encoding='utf-8'), str(note))

    def test_docs_declare_integrations_built_in_not_optional(self):
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        setup = (ROOT / 'reference' / 'setup-and-integrations.md').read_text(encoding='utf-8')
        self.assertIn('## Built-in integrations (part of the skill)', skill)
        section = skill.split('## Built-in integrations', 1)[1].split('## 0.', 1)[0]
        self.assertNotIn('use when relevant', section)
        self.assertIn('part of the skill, not optional add-ons', agents)
        self.assertIn('Built-in integrations', setup)
        self.assertIn('`integrations/`', readme)

    def test_preflight_reports_vendored_integrations_complete(self):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home, USERPROFILE=home)
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'preflight.py')],
                cwd=home, env=env, capture_output=True, text=True, check=True)
            report = json.loads(result.stdout)
            v = report['integrations_vendored']
            self.assertTrue(v['complete'])
            self.assertEqual(v['missing'], [])
            self.assertEqual(v['expected'], len(VENDOR))
            self.assertEqual(v['present'], len(VENDOR))


if __name__ == '__main__':
    unittest.main()
