#!/usr/bin/env python3
"""Convert SRT to a conservative, configurable ASS subtitle.

This script changes presentation only. It does not alter dialogue, cue order, or
translation. Always inspect the rendered output when styling matters.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TIMING_RE = re.compile(
    r"^\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*"
    r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})(?:\s+.*)?$"
)


@dataclass
class Cue:
    index: int
    start_ms: int
    end_ms: int
    text: str


def read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig"), "utf-8-sig"
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16"
    for encoding in ("utf-8", "gb18030", "big5", "cp1252"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to decode {path}")


def parse_time(groups: tuple[str, str, str, str]) -> int:
    hours, minutes, seconds, fraction = groups
    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(fraction.ljust(3, "0")[:3])
    )


def parse_srt(text: str) -> list[Cue]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cues: list[Cue] = []
    i = 0

    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue

        if re.fullmatch(r"\d+", lines[i].strip()):
            index = int(lines[i].strip())
            i += 1
        else:
            index = len(cues) + 1

        if i >= len(lines):
            raise ValueError("Unexpected end of SRT before timing line")
        match = TIMING_RE.match(lines[i])
        if not match:
            raise ValueError(f"Invalid SRT timing near line {i + 1}: {lines[i]!r}")
        groups = match.groups()
        start_ms = parse_time(groups[:4])
        end_ms = parse_time(groups[4:8])
        i += 1

        text_lines: list[str] = []
        while i < len(lines) and lines[i].strip() != "":
            text_lines.append(lines[i])
            i += 1
        if not text_lines:
            raise ValueError(f"Empty subtitle cue {index}")

        cues.append(Cue(index=index, start_ms=start_ms, end_ms=end_ms, text="\n".join(text_lines).strip()))

    return cues


def ass_time(ms: int) -> str:
    centiseconds = int((ms + 5) // 10)
    hours, remainder = divmod(centiseconds, 360_000)
    minutes, remainder = divmod(remainder, 6_000)
    seconds, hundredths = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{hundredths:02d}"


def escape_ass_text(text: str) -> str:
    # Braces introduce override blocks in ASS. Full-width braces preserve the
    # author's literal display without creating fragile escape sequences.
    text = text.replace("{", "｛").replace("}", "｝")
    return text.replace("\n", r"\N")


def build_ass(
    cues: list[Cue],
    *,
    title: str,
    font: str,
    font_size: int,
    play_res_x: int,
    play_res_y: int,
    primary: str,
    outline_colour: str,
    outline: float,
    shadow: float,
    alignment: int,
    margin_l: int,
    margin_r: int,
    margin_v: int,
) -> str:
    lines = [
        "[Script Info]",
        f"Title: {title}",
        "ScriptType: v4.00+",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "YCbCr Matrix: TV.709",
        f"PlayResX: {play_res_x}",
        f"PlayResY: {play_res_y}",
        "",
        "[V4+ Styles]",
        (
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding"
        ),
        (
            f"Style: Default,{font},{font_size},{primary},&H000000FF,"
            f"{outline_colour},&H80000000,0,0,0,0,100,100,0,0,1,"
            f"{outline},{shadow},{alignment},{margin_l},{margin_r},{margin_v},1"
        ),
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for cue in cues:
        lines.append(
            f"Dialogue: 0,{ass_time(cue.start_ms)},{ass_time(cue.end_ms)},Default,,0,0,0,,"
            f"{escape_ass_text(cue.text)}"
        )
    return "\n".join(lines) + "\n"


def count_ass_dialogues(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("Dialogue:"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert SRT to ASS with a conservative cinema style.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default="Film Subtitle")
    parser.add_argument("--font", default="SimSun", help="Installed font family, default SimSun / 宋体")
    parser.add_argument("--font-size", type=int, default=56)
    parser.add_argument("--play-res-x", type=int, default=1920)
    parser.add_argument("--play-res-y", type=int, default=1080)
    parser.add_argument("--primary-colour", default="&H00FFFFFF", help="ASS &HAABBGGRR colour")
    parser.add_argument("--outline-colour", default="&H00000000", help="ASS &HAABBGGRR colour")
    parser.add_argument("--outline", type=float, default=2.3)
    parser.add_argument("--shadow", type=float, default=0.7)
    parser.add_argument("--alignment", type=int, choices=range(1, 10), default=2)
    parser.add_argument("--margin-l", type=int, default=80)
    parser.add_argument("--margin-r", type=int, default=80)
    parser.add_argument("--margin-v", type=int, default=58)
    parser.add_argument("--encoding", choices=("utf-8", "utf-8-sig"), default="utf-8-sig")
    return parser


def main() -> int:
    configure_stdio()
    args = build_parser().parse_args()
    try:
        source, source_encoding = read_text(args.input)
        cues = parse_srt(source)
        output_text = build_ass(
            cues,
            title=args.title,
            font=args.font,
            font_size=args.font_size,
            play_res_x=args.play_res_x,
            play_res_y=args.play_res_y,
            primary=args.primary_colour,
            outline_colour=args.outline_colour,
            outline=args.outline,
            shadow=args.shadow,
            alignment=args.alignment,
            margin_l=args.margin_l,
            margin_r=args.margin_r,
            margin_v=args.margin_v,
        )
        event_count = count_ass_dialogues(output_text)
        if event_count != len(cues):
            raise ValueError(f"ASS event verification failed: expected {len(cues)}, wrote {event_count}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_text, encoding=args.encoding)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Read {len(cues)} cues from {args.input} ({source_encoding})")
    print(f"Wrote {event_count} ASS events to {args.output}")
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
