#!/usr/bin/env python3
"""Align two subtitle versions by time for human comparison and merge review.

Alignment is a review aid, not an automatic winner. Segmentation differences can
make a combined cue match several cues or only part of one.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from subtitle_qa import Cue, parse_ass, parse_srt, parse_vtt, read_text_with_fallback


@dataclass
class Pair:
    a_index: int | str
    a_start_ms: int
    a_end_ms: int
    a_text: str
    b_index: int | str | None
    b_start_ms: int | None
    b_end_ms: int | None
    b_text: str | None
    overlap_ms: int
    midpoint_delta_ms: int | None
    text_similarity: float | None
    status: str
    candidate_count: int


def load_cues(path: Path) -> tuple[list[Cue], str, str]:
    text, encoding = read_text_with_fallback(path)
    suffix = path.suffix.lower()
    if suffix == ".srt":
        return parse_srt(text), "SRT", encoding
    if suffix in {".ass", ".ssa"}:
        return parse_ass(text), "ASS", encoding
    if suffix == ".vtt":
        return parse_vtt(text), "WebVTT", encoding
    stripped = text.lstrip("\ufeff \t\r\n")
    if stripped.startswith("WEBVTT"):
        return parse_vtt(text), "WebVTT", encoding
    if "[Script Info]" in text[:2000] or "[Events]" in text[:4000]:
        return parse_ass(text), "ASS", encoding
    if "-->" in text[:5000]:
        return parse_srt(text), "SRT", encoding
    raise ValueError(f"Unsupported or unrecognized subtitle format: {suffix or '(no extension)'}")


def normalized_text(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    return text.lower()


def text_similarity(a: str, b: str) -> float:
    left = normalized_text(a)
    right = normalized_text(b)
    if not left or not right:
        return 0.0
    return difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()


def overlap_ms(a: Cue, b: Cue) -> int:
    return max(0, min(a.end_ms, b.end_ms) - max(a.start_ms, b.start_ms))


def midpoint(cue: Cue) -> float:
    return (cue.start_ms + cue.end_ms) / 2


def score_candidate(
    a: Cue,
    b: Cue,
    *,
    max_gap_ms: int,
    text_weight: float,
) -> tuple[float, int, int, float] | None:
    overlap = overlap_ms(a, b)
    distance = abs(midpoint(a) - midpoint(b))
    if overlap == 0 and distance > max_gap_ms:
        return None

    shorter_duration = max(1, min(a.end_ms - a.start_ms, b.end_ms - b.start_ms))
    overlap_ratio = overlap / shorter_duration
    similarity = text_similarity(a.text, b.text)
    score = overlap_ratio * 10_000 + similarity * text_weight - distance
    return score, overlap, int(round(distance)), similarity


def align(
    a_cues: list[Cue],
    b_cues: list[Cue],
    *,
    max_gap_ms: int,
    text_weight: float,
    minimum_overlap_ratio: float,
) -> tuple[list[Pair], list[Cue]]:
    pairs: list[Pair] = []
    used_b: set[int] = set()
    last_b_index = -1

    for a in a_cues:
        candidates: list[tuple[float, int, int, float, int, Cue]] = []
        for b_position, b in enumerate(b_cues):
            if b_position <= last_b_index or b_position in used_b:
                continue
            scored = score_candidate(a, b, max_gap_ms=max_gap_ms, text_weight=text_weight)
            if scored is None:
                continue
            score, overlap, distance, similarity = scored
            shorter_duration = max(1, min(a.end_ms - a.start_ms, b.end_ms - b.start_ms))
            if overlap / shorter_duration < minimum_overlap_ratio and overlap > 0:
                continue
            candidates.append((score, overlap, distance, similarity, b_position, b))

        if not candidates:
            pairs.append(
                Pair(
                    a_index=a.index,
                    a_start_ms=a.start_ms,
                    a_end_ms=a.end_ms,
                    a_text=a.text,
                    b_index=None,
                    b_start_ms=None,
                    b_end_ms=None,
                    b_text=None,
                    overlap_ms=0,
                    midpoint_delta_ms=None,
                    text_similarity=None,
                    status="unmatched_a",
                    candidate_count=0,
                )
            )
            continue

        candidates.sort(key=lambda item: item[0], reverse=True)
        best = candidates[0]
        ambiguous = len(candidates) > 1 and abs(best[0] - candidates[1][0]) < 1.0
        _, overlap, distance, similarity, b_position, b = best
        used_b.add(b_position)
        last_b_index = b_position
        pairs.append(
            Pair(
                a_index=a.index,
                a_start_ms=a.start_ms,
                a_end_ms=a.end_ms,
                a_text=a.text,
                b_index=b.index,
                b_start_ms=b.start_ms,
                b_end_ms=b.end_ms,
                b_text=b.text,
                overlap_ms=overlap,
                midpoint_delta_ms=distance,
                text_similarity=round(similarity, 4),
                status="ambiguous" if ambiguous else "matched",
                candidate_count=len(candidates),
            )
        )

    unmatched_b = [b for position, b in enumerate(b_cues) if position not in used_b]
    return pairs, unmatched_b


def format_tsv_text(text: str | None) -> str:
    if text is None:
        return ""
    return " / ".join(line.strip() for line in text.splitlines() if line.strip()).replace("\t", " ")


def build_tsv(pairs: list[Pair], unmatched_b: list[Cue]) -> str:
    lines = [
        "\t".join(
            [
                "status",
                "a_index",
                "a_start_ms",
                "a_end_ms",
                "a_text",
                "b_index",
                "b_start_ms",
                "b_end_ms",
                "b_text",
                "overlap_ms",
                "midpoint_delta_ms",
                "text_similarity",
            ]
        )
    ]
    for pair in pairs:
        lines.append(
            "\t".join(
                [
                    pair.status,
                    str(pair.a_index),
                    str(pair.a_start_ms),
                    str(pair.a_end_ms),
                    format_tsv_text(pair.a_text),
                    "" if pair.b_index is None else str(pair.b_index),
                    "" if pair.b_start_ms is None else str(pair.b_start_ms),
                    "" if pair.b_end_ms is None else str(pair.b_end_ms),
                    format_tsv_text(pair.b_text),
                    str(pair.overlap_ms),
                    "" if pair.midpoint_delta_ms is None else str(pair.midpoint_delta_ms),
                    "" if pair.text_similarity is None else f"{pair.text_similarity:.4f}",
                ]
            )
        )
    for b in unmatched_b:
        lines.append(
            "\t".join(
                [
                    "unmatched_b",
                    "",
                    "",
                    "",
                    "",
                    str(b.index),
                    str(b.start_ms),
                    str(b.end_ms),
                    format_tsv_text(b.text),
                    "",
                    "",
                    "",
                ]
            )
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Align two subtitle versions by time.")
    parser.add_argument("a", type=Path, help="Version A, often the timing master")
    parser.add_argument("b", type=Path, help="Version B, often a comparison or translation")
    parser.add_argument("--json-out", type=Path, help="Write detailed JSON alignment")
    parser.add_argument("--tsv-out", type=Path, help="Write human-readable TSV alignment")
    parser.add_argument("--max-gap-ms", type=int, default=3000, help="Maximum midpoint distance when overlap is zero")
    parser.add_argument(
        "--minimum-overlap-ratio",
        type=float,
        default=0.05,
        help="Minimum overlap relative to the shorter cue when overlap exists",
    )
    parser.add_argument(
        "--text-weight",
        type=float,
        default=0.0,
        help="Text-similarity weight for same-language versions; keep 0 for different languages",
    )
    return parser


def main() -> int:
    configure_stdio()
    args = build_parser().parse_args()
    try:
        a_cues, a_format, a_encoding = load_cues(args.a)
        b_cues, b_format, b_encoding = load_cues(args.b)
        pairs, unmatched_b = align(
            a_cues,
            b_cues,
            max_gap_ms=args.max_gap_ms,
            text_weight=args.text_weight,
            minimum_overlap_ratio=args.minimum_overlap_ratio,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    matched = sum(1 for pair in pairs if pair.status == "matched")
    ambiguous = sum(1 for pair in pairs if pair.status == "ambiguous")
    unmatched_a = sum(1 for pair in pairs if pair.status == "unmatched_a")
    result = {
        "a": {
            "path": str(args.a),
            "format": a_format,
            "encoding": a_encoding,
            "cue_count": len(a_cues),
        },
        "b": {
            "path": str(args.b),
            "format": b_format,
            "encoding": b_encoding,
            "cue_count": len(b_cues),
        },
        "settings": {
            "max_gap_ms": args.max_gap_ms,
            "minimum_overlap_ratio": args.minimum_overlap_ratio,
            "text_weight": args.text_weight,
        },
        "summary": {
            "matched": matched,
            "ambiguous": ambiguous,
            "unmatched_a": unmatched_a,
            "unmatched_b": len(unmatched_b),
        },
        "pairs": [asdict(pair) for pair in pairs],
        "unmatched_b": [asdict(cue) for cue in unmatched_b],
    }

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.tsv_out:
        args.tsv_out.parent.mkdir(parents=True, exist_ok=True)
        args.tsv_out.write_text(build_tsv(pairs, unmatched_b), encoding="utf-8-sig")

    print(f"Version A: {len(a_cues)} cues ({a_format}, {a_encoding})")
    print(f"Version B: {len(b_cues)} cues ({b_format}, {b_encoding})")
    print(
        f"Matched: {matched}; ambiguous: {ambiguous}; "
        f"unmatched A: {unmatched_a}; unmatched B: {len(unmatched_b)}"
    )
    return 0


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (AttributeError, ValueError):
                pass


if __name__ == "__main__":
    raise SystemExit(main())
