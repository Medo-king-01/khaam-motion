import contextlib
import hashlib
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = ImageDraw = None

import reference_board
import taste_notes
import visual_ledger
import visual_reference


@unittest.skipUnless(Image is not None, "Pillow is an optional dependency for image helpers")
class VisualImageToolsTest(unittest.TestCase):
    def _img(self, path: Path, color="#eeeeee", accent="#174a7e"):
        image = Image.new("RGB", (120, 180), color)
        draw = ImageDraw.Draw(image)
        draw.rectangle((22, 20, 96, 88), fill=accent)
        image.save(path)
        return path

    def test_reference_measure_and_same_frame_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            a = self._img(tmp / "reference.png")
            b = self._img(tmp / "result.png")
            measured = visual_reference.measure(a)
            self.assertEqual(measured["size"], [120, 180])
            self.assertEqual(len(measured["edge_density_by_vertical_band"]), 10)
            self.assertGreater(len(measured["palette"]), 0)
            metrics = visual_reference.similarity(measured, visual_reference.measure(b))
            self.assertTrue(metrics["same_aspect_ratio"])
            self.assertLess(metrics["palette_distance"], 0.01)
            self.assertGreater(metrics["layout_cosine"], 0.99)
            card = tmp / "comparison.png"
            visual_reference.make_comparison_card(Image.open(a), Image.open(b), card)
            self.assertTrue(card.is_file())
            with self.assertRaises(FileExistsError):
                visual_reference.make_comparison_card(Image.open(a), Image.open(b), card)

    def test_reference_board_is_local_and_preserves_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            refs = tmp / "refs"
            refs.mkdir()
            a, b = self._img(refs / "one.png"), self._img(refs / "two.png", "#fff4e0", "#bc382d")
            original = hashlib.sha256(a.read_bytes()).hexdigest()
            expanded = reference_board.expand_sources([str(refs), str(a)])
            self.assertEqual(len(expanded), 2)
            board, source_map = reference_board.build_board(
                expanded, tmp / "board.jpg", title="test", labels=["one", "two"], cols=2,
            )
            self.assertTrue(board.is_file())
            self.assertIn(original, source_map.read_text(encoding="utf-8"))
            self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(), original)
            with self.assertRaises(FileExistsError):
                reference_board.build_board(expanded, board, title="again", labels=["one", "two"])

    def test_visual_ledger_stores_descriptors_not_source_path_and_only_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            frame = self._img(tmp / "private-frame.png")
            ledger = tmp / "visual-ledger.jsonl"
            visual_ledger.add_record(
                str(frame), project="sample", version="1", style="editorial",
                motif="one route", motion="draw then hold", aspect="9:16",
                source="approved reference A", note="", ledger=ledger,
            )
            text = ledger.read_text(encoding="utf-8")
            if os.name == "posix":
                self.assertEqual(ledger.stat().st_mode & 0o777, 0o600)
            self.assertNotIn(str(frame), text)
            self.assertNotIn("private-frame.png", text)
            rows = visual_ledger.read_rows(ledger)
            reports = visual_ledger.check_frame(str(frame), rows, motif="one route", last=12)
            self.assertEqual(reports[0]["signals"], ["close palette", "similar coarse layout", "same named motif"])
            with self.assertRaises(visual_ledger.LedgerError):
                visual_ledger.add_record(
                    str(frame), project="sample", version="1", style="editorial",
                    motif="one route", motion="draw then hold", aspect="9:16",
                    source="", note="", ledger=ledger,
                )


@unittest.skipUnless(Image is not None, "Pillow is an optional dependency for image helpers")
class VisualToolsCliTest(unittest.TestCase):
    def test_all_four_helpers_accept_documented_local_workflows(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            frame = Image.new("RGB", (96, 144), "#f3ead8")
            ImageDraw.Draw(frame).ellipse((22, 18, 74, 88), fill="#365b75")
            reference, candidate = tmp / "reference.png", tmp / "candidate.png"
            frame.save(reference)
            frame.save(candidate)

            board_out = tmp / "board.png"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(reference_board.main([str(reference), str(candidate), "--out", str(board_out)]), 0)
            self.assertTrue(board_out.exists())

            card_out = tmp / "compare.png"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(visual_reference.main([
                    "compare", "--reference", str(reference), "--result", str(candidate), "--out", str(card_out),
                ]), 0)
            self.assertTrue(card_out.exists())

            ledger = tmp / "visual.jsonl"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(visual_ledger.main([
                    "add", str(candidate), "--project", "cli-smoke", "--style", "editorial",
                    "--motif", "one circle", "--motion", "fade", "--ledger", str(ledger),
                ]), 0)
                self.assertEqual(visual_ledger.main(["check", str(candidate), "--motif", "one circle", "--ledger", str(ledger)]), 0)
            self.assertEqual(len(visual_ledger.read_rows(ledger)), 1)

            notes = tmp / "user-taste.md"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(taste_notes.main([
                    "--file", str(notes), "add", "--kind", "preference",
                    "--statement", "«العنوان أقصر»", "--scope", "hooks", "--topic", "Arabic",
                    "--evidence", "user's words",
                ]), 0)
                self.assertEqual(taste_notes.main(["--file", str(notes), "show", "--topic", "Arabic"]), 0)
            self.assertIn("«العنوان أقصر»", notes.read_text(encoding="utf-8"))


class VisualToolsRoutingTest(unittest.TestCase):
    def test_skill_routes_tools_and_docs_keep_them_optional(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        guide = (ROOT / "reference" / "visual-reference-tools.md").read_text(encoding="utf-8")
        for name in ("reference_board.py", "visual_reference.py", "visual_ledger.py", "taste_notes.py"):
            self.assertIn(name, skill)
            self.assertIn(name, guide)
        self.assertIn("None of the helpers below accesses the network", guide)
        self.assertIn("never blocks a render", guide)
        self.assertIn("existing `user-taste.md`", guide)


class TasteNotesTest(unittest.TestCase):
    def test_add_show_and_supersede_preserve_existing_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "user-taste.md"
            path.write_text("# Existing user taste\n\nDo not overwrite me.\n", encoding="utf-8")
            pref = taste_notes.add_note(
                path, kind="preference", statement="«العناوين أقصر»", scope="explainer hooks",
                topics=["Arabic", "hooks"], evidence="user said this in the project chat",
                next_time="keep the title to one line",
            )
            observed = taste_notes.add_note(
                path, kind="observed", statement="The quiet opening held attention in one pilot.",
                scope="pilot A only", topics=["opening"], evidence="project LOG.md, render v2",
            )
            self.assertEqual(pref["id"], "T0001")
            self.assertEqual(observed["id"], "T0002")
            active = taste_notes.select_notes(path, topic="hooks", include_superseded=False)
            self.assertEqual([r["id"] for r in active], ["T0001"])
            taste_notes.supersede_note(path, "T0001", "User later preferred a longer explanatory title.")
            all_rows = taste_notes.select_notes(path, topic="hooks", include_superseded=True)
            self.assertEqual(all_rows[0]["status"], "superseded")
            text = path.read_text(encoding="utf-8")
            if os.name == "posix":
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertIn("Do not overwrite me.", text)
            self.assertIn("KHAAM_TASTE_NOTES_V1:START", text)

    def test_corrupt_markers_fail_without_mutating_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "taste.md"
            original = "# Legacy\n\n<!-- KHAAM_TASTE_NOTES_V1:START -->\n"
            path.write_text(original, encoding="utf-8")
            with self.assertRaises(taste_notes.TasteNoteError):
                taste_notes.add_note(path, kind="preference", statement="Shorter", scope="hooks",
                                     topics=["copy"], evidence="user said so")
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_preferences_require_scope_evidence_and_search_topics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "taste.md"
            with self.assertRaises(taste_notes.TasteNoteError):
                taste_notes.add_note(path, kind="preference", statement="No evidence", scope="hooks",
                                     topics=["copy"], evidence="")
            self.assertFalse(path.exists())
            row = taste_notes.add_note(path, kind="verified", statement="Actual user taste is uncertain.",
                                       scope="none", topics=["sound"], evidence="two project observations")
            self.assertEqual([x["id"] for x in taste_notes.select_notes(path, topic="sound", include_superseded=False)], [row["id"]])


if __name__ == "__main__":
    unittest.main()
