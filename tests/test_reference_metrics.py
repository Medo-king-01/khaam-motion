import math
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import reference_metrics


class ReferenceMetricsTest(unittest.TestCase):
    def test_luminance_samples_are_timed_and_reject_partial_frame(self):
        # Two 2x2 grayscale frames: means 10 and 100.
        rows = reference_metrics.luminance_samples(bytes([10] * 4 + [100] * 4),
                                                   width=2, height=2, start=3.0, fps=2.0)
        self.assertEqual(rows, [
            {"time_s": 3.0, "mean_luma_0_255": 10.0},
            {"time_s": 3.5, "mean_luma_0_255": 100.0},
        ])
        with self.assertRaises(ValueError):
            reference_metrics.luminance_samples(b"\x00", width=2, height=2)

    def test_audio_rms_windows_and_transient_candidates(self):
        hop = 512
        pattern = [0] * 100
        for onset in (10, 30, 50, 70):
            pattern[onset:onset + 2] = [16000, 16000]
        blocks = [b"\x00\x00" * hop if amplitude == 0 else
                  b"".join(int(amplitude).to_bytes(2, "little", signed=True) for _ in range(hop))
                  for amplitude in pattern]
        iterator = iter(blocks)
        result = reference_metrics.audio_level_track(lambda _: next(iterator, b""), sample_rate=16000, start=2.0, hop=hop)
        self.assertTrue(result["rms_every_approx_0_25s"])
        self.assertLess(result["rms_every_approx_0_25s"][0]["rms_dbfs"], -100)
        self.assertTrue(all(t >= 2.0 for t in result["onset_candidates_s"]))
        self.assertTrue(result["onset_candidates_s"])

    def test_beat_offset_uses_supplied_grid_without_inference(self):
        rows = reference_metrics.beat_offsets([1.0, 1.25], bpm=120, phase_s=0.0)
        self.assertEqual(rows[0]["nearest_beat_offset_ms"], 0.0)
        self.assertEqual(rows[1]["nearest_beat_offset_ms"], -250.0)
        with self.assertRaises(ValueError):
            reference_metrics.beat_offsets([1.0], bpm=0)

    def test_text_report_labels_signals_as_non_judgment(self):
        text = reference_metrics.make_text_report({"video": {}, "audio": {}, "scene_cuts_s": []})
        self.assertIn("not a beat detector", text)
        self.assertIn("do not judge quality", text)
        self.assertIn("no audio", text)

    def test_feature_is_routed_through_existing_khaam_analyzer_and_docs(self):
        analyzer = (ROOT / "scripts" / "analyze_ref.py").read_text(encoding="utf-8")
        guide = (ROOT / "reference" / "visual-reference-tools.md").read_text(encoding="utf-8")
        self.assertIn("--metrics", analyzer)
        self.assertIn("--bpm", analyzer)
        self.assertIn("measurements.json", guide)
        self.assertIn("does not copy Herk source", guide)


if __name__ == "__main__":
    unittest.main()
