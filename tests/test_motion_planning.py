import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "templates/hyperframes/motion-plan.example.json"
CATALOG = ROOT / "templates/hyperframes/motion-catalog.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class MotionPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_module("validate_motion_plan", ROOT / "scripts/validate_motion_plan.py")
        cls.plan = json.loads(PLAN.read_text(encoding="utf-8"))
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_illustrative_plan_validates_against_local_catalog(self):
        self.assertEqual([], self.validator.validate_plan(self.plan, self.catalog))

    def test_unknown_template_and_variable_are_rejected(self):
        plan = json.loads(json.dumps(self.plan))
        plan["scenes"][0]["templateId"] = "missing"
        errors = self.validator.validate_plan(plan, self.catalog)
        self.assertTrue(any("unknown catalog id" in item for item in errors))

        plan = json.loads(json.dumps(self.plan))
        plan["scenes"][0]["variables"]["secret"] = "not catalogued"
        errors = self.validator.validate_plan(plan, self.catalog)
        self.assertTrue(any("not declared" in item for item in errors))

    def test_mixed_or_reversed_timing_rejected(self):
        for timing in ({"startCue": "one", "endSeconds": 2}, {"startSeconds": 2, "endSeconds": 1}):
            plan = json.loads(json.dumps(self.plan))
            plan["scenes"][0]["timing"] = timing
            self.assertTrue(any("timing" in item for item in self.validator.validate_plan(plan, self.catalog)))

    def test_second_language_quote_requires_credit(self):
        plan = json.loads(json.dumps(self.plan))
        plan["scenes"][0] = {
            "id": "verified", "templateId": "verified-card",
            "timing": {"startSeconds": 0, "endSeconds": 2},
            "sourceQuote": "نص من المستخدم", "intent": "عرض النص", "layoutMode": "overlay",
            "requiredInformation": ["النص"], "forbiddenInformation": ["إضافة ادعاء"],
            "variables": {"card": {"text": "نص المستخدم", "reference": "مرجع واضح", "second": "translation"}},
        }
        errors = self.validator.validate_plan(plan, self.catalog)
        self.assertTrue(any("secondCredit" in item for item in errors))

    def test_catalog_entries_reference_local_compositions_and_audit_selectors(self):
        for item in self.catalog["templates"]:
            self.assertTrue((ROOT / "templates/hyperframes" / item["source"]).is_file())
            self.assertTrue(item["layoutAudit"]["subjectSelectors"])
            self.assertTrue(item["layoutAudit"]["frameSelectors"])
            self.assertTrue((ROOT / "templates/hyperframes" / item["preview"]).is_file())
            self.assertEqual("schematic-only-not-a-render", item["previewStatus"])

    def test_cli_accepts_example(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_motion_plan.py"), str(PLAN)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


class MotionTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.syncer = load_module("sync_motion_tokens", ROOT / "scripts/sync_motion_tokens.py")

    def test_sync_is_deterministic_and_check_is_read_only(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "motion-tokens.json"
            output = Path(temp) / "motion-tokens.css"
            source.write_text(json.dumps({"version": 1, "tokens": {"bg": "#010203", "ink": "#ffffff", "accent": "#aBcDeF"}}), encoding="utf-8")
            self.assertFalse(self.syncer.sync(source, output))
            self.assertEqual(self.syncer.render_css({"bg": "#010203", "ink": "#ffffff", "accent": "#abcdef"}), output.read_text(encoding="utf-8"))
            self.assertTrue(self.syncer.sync(source, output, check=True))
            source.write_text(json.dumps({"version": 1, "tokens": {"bg": "#010204", "ink": "#ffffff", "accent": "#abcdef"}}), encoding="utf-8")
            with self.assertRaises(self.syncer.TokenError):
                self.syncer.sync(source, output, check=True)

    def test_refuses_invalid_tokens_and_unmarked_output(self):
        with tempfile.TemporaryDirectory() as temp:
            source, output = Path(temp) / "tokens.json", Path(temp) / "tokens.css"
            source.write_text('{"version":1,"tokens":{"bg":"red","ink":"#ffffff","accent":"#000000"}}', encoding="utf-8")
            with self.assertRaises(self.syncer.TokenError):
                self.syncer.sync(source, output)
            source.write_text('{"version":1,"tokens":{"bg":"#000000","ink":"#ffffff","accent":"#123456"}}', encoding="utf-8")
            output.write_text(":root { color: red }", encoding="utf-8")
            with self.assertRaises(self.syncer.TokenError):
                self.syncer.sync(source, output)
            self.assertEqual(":root { color: red }", output.read_text(encoding="utf-8"))

    def test_existing_shared_tokens_match_source_and_are_linked(self):
        css = ROOT / "templates/hyperframes/motion-tokens.css"
        index = ROOT / "templates/hyperframes/index.html"
        self.assertTrue(self.syncer.sync(ROOT / "templates/hyperframes/motion-tokens.json", css, check=True))
        self.assertIn('href="motion-tokens.css"', index.read_text(encoding="utf-8"))
        self.assertNotIn("--bg: #111317", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
