import hashlib
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'reference' / 'huashu-design-upstream'


class HuashuDesignAdaptationTest(unittest.TestCase):
    def test_source_snapshot_is_complete_and_pinned(self):
        rows = (UPSTREAM / 'UPSTREAM-MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
        self.assertEqual(len(rows), 31)
        for row in rows:
            expected, relative = row.split('  ', 1)
            self.assertEqual(
                hashlib.sha256((UPSTREAM / relative).read_bytes()).hexdigest(),
                expected,
                relative,
            )
        notice = (UPSTREAM / 'SOURCE-NOTICE.md').read_text(encoding='utf-8')
        self.assertIn('59065698ad63f87ea1532c126c87f488d4f93fd6', notice)
        self.assertIn('MIT', notice)
        self.assertTrue((UPSTREAM / 'LICENSE').is_file())

    def test_guide_preserves_khaam_workflow_and_limits_upstream(self):
        guide = (ROOT / 'reference' / 'huashu-design.md').read_text(encoding='utf-8')
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('reference/huashu-design.md', skill)
        self.assertIn('No compulsory three-direction ceremony', guide)
        self.assertIn('no-music-by-default', guide)
        self.assertIn('Arabic typography', guide)
        self.assertIn('not tested Khaam components', guide)
        self.assertIn('reference/verified-motion-workflow.md', guide)

    def test_selected_original_examples_and_overviews_are_present(self):
        expected = [
            'assets/style-specimens/sheet-info.jpg',
            'assets/style-specimens/sheet-ppt.jpg',
            'assets/style-specimens/info/06-data-humanism.html',
            'assets/style-specimens/info/06-data-humanism.jpg',
            'assets/style-specimens/paradigm/04-one-semantic-color.html',
            'assets/style-specimens/paradigm/04-one-semantic-color.jpg',
            'references/design-styles.md',
            'references/animation-best-practices.md',
            'references/camera-language.md',
        ]
        for relative in expected:
            self.assertTrue((UPSTREAM / relative).is_file(), relative)


if __name__ == '__main__':
    unittest.main()
