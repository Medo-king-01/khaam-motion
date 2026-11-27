import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'reference' / 'animated-diagrams-upstream'


def verify_manifest() -> int:
    rows = (UPSTREAM / 'UPSTREAM-MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
    for row in rows:
        expected, relative = row.split('  ', 1)
        actual = hashlib.sha256((UPSTREAM / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f'upstream source checksum mismatch: {relative}')
    return len(rows)


class AnimatedDiagramsIntegrationTest(unittest.TestCase):
    def test_skill_routes_diagram_requests_to_khaam_workflow(self):
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        guide = (ROOT / 'reference' / 'animated-diagrams.md').read_text(encoding='utf-8')
        self.assertIn('reference/animated-diagrams.md', skill)
        self.assertIn('sequence, flowchart', skill.lower())
        self.assertIn('Khaam\'s HyperFrames starter', guide)
        self.assertIn('never use the upstream SRT helper', guide)
        self.assertIn('convert Mermaid text to SVG, validate diagram semantics, or sanitize SVG', guide)
        self.assertIn('scripts/cues.py', guide)

    def test_upstream_source_subset_and_licenses_are_pinned(self):
        notice = (UPSTREAM / 'SOURCE-NOTICE.md').read_text(encoding='utf-8')
        self.assertIn('3de812d90c94baa4f9761684f36c3c322f1fb38c', notice)
        self.assertTrue((UPSTREAM / 'LICENSE').is_file())
        self.assertTrue((UPSTREAM / 'NOTICE').is_file())
        self.assertTrue((UPSTREAM / 'licenses' / 'THIRD_PARTY.md').is_file())
        self.assertTrue((UPSTREAM / 'references' / 'diagram-svg-authoring.md').is_file())
        self.assertTrue((UPSTREAM / 'examples' / 'arabic-architecture' / 'index.html').is_file())
        self.assertEqual(verify_manifest(), 26)

    def test_upstream_code_to_svg_helper_runs_on_a_local_test_source(self):
        helper = ROOT / 'scripts' / 'diagram_code_to_svg.py'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'sample.py'
            output = Path(tmp) / 'sample.svg'
            source.write_text('def answer():\n    return 42\n', encoding='utf-8')
            subprocess.run(
                [sys.executable, str(helper), str(source), '--start', '1', '--end', '2', '-o', str(output)],
                check=True, capture_output=True, text=True,
            )
            svg = output.read_text(encoding='utf-8')
        self.assertIn('id="line-1"', svg)
        self.assertIn('class="tok-kw"', svg)
        self.assertIn('id="code-hl"', svg)

    def test_upstream_svg_prep_helper_normalizes_a_local_sequence_fixture(self):
        helper = UPSTREAM / 'scripts' / 'svg_prep.py'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'sequence.svg'
            output = Path(tmp) / 'normalized.svg'
            source.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50" viewBox="0 0 100 50">'
                '<line class="messageLine0" x1="10" y1="20" x2="90" y2="20"/>'
                '<text class="messageText" x="50" y="15">call</text></svg>',
                encoding='utf-8',
            )
            subprocess.run(
                [sys.executable, str(helper), str(source), '--from', 'mermaid-seq', '-o', str(output)],
                check=True, capture_output=True, text=True,
            )
            svg = output.read_text(encoding='utf-8')
        self.assertIn('id="msg-01"', svg)
        self.assertIn('data-dir="ltr"', svg)
        self.assertIn('id="msgtext-01"', svg)
        self.assertNotIn('width="100"', svg)


if __name__ == '__main__':
    unittest.main()
