#!/usr/bin/env python3
"""Small, deterministic measurements for a local reference-video excerpt.

These measurements describe pixels/audio levels only. They are not quality,
semantic, originality, rights, or listening judgments.
"""
from __future__ import annotations

import math
from typing import Iterable


def luminance_samples(raw: bytes, *, width: int = 64, height: int = 36,
                      start: float = 0.0, fps: float = 2.0) -> list[dict[str, float]]:
    """Summarize consecutive 8-bit grayscale frames supplied by FFmpeg."""
    if width <= 0 or height <= 0 or not math.isfinite(start) or start < 0 or not math.isfinite(fps) or fps <= 0:
        raise ValueError("Invalid luminance sample dimensions or timing.")
    frame_size = width * height
    if len(raw) % frame_size:
        raise ValueError("Incomplete grayscale frame in FFmpeg output.")
    rows = []
    for index in range(0, len(raw), frame_size):
        frame_index = index // frame_size
        mean = sum(raw[index:index + frame_size]) / frame_size
        rows.append({"time_s": round(start + frame_index / fps, 3), "mean_luma_0_255": round(mean, 2)})
    return rows


def audio_level_track(read_frames, *, sample_rate: int, start: float = 0.0,
                      hop: int = 512) -> dict[str, list]:
    """Read mono signed-16-bit PCM in bounded hops and return RMS/onset summaries.

    `read_frames(n)` is the standard `wave.Wave_read.readframes` method. RMS
    windows are grouped into approximate 250 ms buckets; onset candidates are
    simple positive-RMS-change peaks, not a beat detector.
    """
    if sample_rate <= 0 or hop <= 0 or not math.isfinite(start) or start < 0:
        raise ValueError("Invalid audio sample rate or timing.")
    rms_track: list[tuple[float, float, int]] = []
    index = 0
    while True:
        block = read_frames(hop)
        if not block:
            break
        if len(block) % 2:
            raise ValueError("Audio PCM is not aligned to signed 16-bit samples.")
        count = len(block) // 2
        # FFmpeg writes little-endian PCM WAV for analyze_ref.py.
        squares = 0
        for offset in range(0, len(block), 2):
            sample = int.from_bytes(block[offset:offset + 2], "little", signed=True) / 32768.0
            squares += sample * sample
        rms_track.append((start + index / sample_rate, math.sqrt(squares / count), count))
        index += count

    quarter_seconds = 0.25
    buckets: dict[int, list[float]] = {}
    for time_s, rms, count in rms_track:
        bucket = int((time_s - start) / quarter_seconds)
        state = buckets.setdefault(bucket, [0.0, 0.0])
        state[0] += (rms * rms) * count
        state[1] += count
    rms_250ms = []
    for bucket, (sum_squares, count) in sorted(buckets.items()):
        rms = math.sqrt(sum_squares / count) if count else 0.0
        dbfs = 20 * math.log10(max(rms, 1e-9))
        rms_250ms.append({"time_s": round(start + bucket * quarter_seconds, 3), "rms_dbfs": round(dbfs, 2)})

    rises = [max(0.0, rms_track[i][1] - rms_track[i - 1][1])
             for i in range(1, len(rms_track))]
    if rises:
        mean = sum(rises) / len(rises)
        sd = math.sqrt(sum((value - mean) ** 2 for value in rises) / len(rises))
        threshold = mean + 2.5 * sd
    else:
        threshold = math.inf
    onsets = []
    for i in range(1, len(rises) - 1):
        if rises[i] > threshold and rises[i] >= rises[i - 1] and rises[i] >= rises[i + 1]:
            onsets.append(round(rms_track[i + 1][0], 3))
    return {"rms_every_approx_0_25s": rms_250ms, "onset_candidates_s": onsets}


def beat_offsets(cuts_s: Iterable[float], *, bpm: float, phase_s: float = 0.0) -> list[dict[str, float]]:
    """Report signed distance from each cut to its nearest user-specified beat."""
    if not math.isfinite(bpm) or bpm <= 0 or not math.isfinite(phase_s):
        raise ValueError("BPM must be positive and phase must be finite.")
    period = 60.0 / bpm
    result = []
    for cut in cuts_s:
        if not math.isfinite(cut):
            raise ValueError("Cut times must be finite.")
        offset = ((cut - phase_s + period / 2) % period) - period / 2
        result.append({"cut_s": round(cut, 3), "nearest_beat_offset_ms": round(offset * 1000, 1)})
    return result


def make_text_report(data: dict) -> str:
    """Render compact human-readable observations without a score or verdict."""
    lines = ["Reference measurements · descriptive signals only"]
    video = data.get("video", {})
    luma = video.get("luminance_every_approx_0_5s", [])
    lines.append("Luminance mean (0–255) every ~0.5 s: " +
                 (" ".join(f"{row['time_s']:.2f}s={row['mean_luma_0_255']:.1f}" for row in luma) or "none"))
    audio = data.get("audio", {})
    levels = audio.get("rms_every_approx_0_25s", [])
    lines.append("Audio RMS (dBFS) every ~0.25 s: " +
                 (" ".join(f"{row['time_s']:.2f}s={row['rms_dbfs']:.1f}" for row in levels) or "no audio"))
    onsets = audio.get("onset_candidates_s", [])
    lines.append("Transient candidates (s; not a beat detector): " +
                 (" ".join(f"{time_s:.3f}" for time_s in onsets) or "none"))
    cuts = data.get("scene_cuts_s", [])
    lines.append("Scene-cut candidates (s): " + (" ".join(f"{time_s:.3f}" for time_s in cuts) or "none"))
    alignment = data.get("beat_alignment")
    if alignment:
        lines.append(f"User-specified beat grid: {alignment['bpm']:.3f} BPM; phase {alignment['phase_s']:.3f} s")
        lines.append("Cut offset from nearest beat (ms): " +
                     (" ".join(f"{row['nearest_beat_offset_ms']:+.1f}" for row in alignment["cut_offsets"]) or "no cuts"))
    lines += ["", "These measurements do not judge quality, content, sync, rights, or what sounds good.",
              "Inspect the actual reference and listen to it; BPM/phase are inputs, not inferred results."]
    return "\n".join(lines) + "\n"
