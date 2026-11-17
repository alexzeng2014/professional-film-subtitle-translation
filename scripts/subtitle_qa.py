#!/usr/bin/env python3
"""Audit SRT, ASS, or WebVTT subtitles for technical and readability issues.

The technical-health score produced here is not an overall translation score.
Semantic accuracy, voice, and subtext still require the rubric in
references/quality-rubric.md.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


TIMING_SRT = re.compile(
    r"^\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*"
    r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})(?:\s+.*)?$"
)
TIMING_ASS = re.compile(r"^\s*(\d+):(\d{2}):(\d{2})[.](\d{1,2})\s*$")
ASS_TAG = re.compile(r"\{[^}]*\}")
HTML_TAG = re.compile(r"</?[^>]+>")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]")
LATIN_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")


@dataclass
class Cue:
    index: int | str
    start_ms: int
    end_ms: int
    text: str
    raw_text: str = ""

    @property
    def duration_s(self) -> float:
        return (self.end_ms - self.start_ms) / 1000.0

    @property
    def lines(self) -> list[str]:
        return [line.strip() for line in self.text.splitlines() if line.strip()]


@dataclass
class Issue:
    code: str
    severity: str
    message: str
    cue: str | int | None = None
    value: float | int | str | None = None


@dataclass
class Audit:
    path: str
    format: str
    encoding: str
    cue_count: int
    first_start_ms: int | None
    last_end_ms: int | None
    span_s: float | None
    mean_cps: float | None
    max_cps: float | None
    cues_over_cps: int
    issues: list[Issue] = field(default_factory=list)
    technical_score: int = 100
    status: str = "PASS"
    settings: dict[str, float | int | str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        data = asdict(self)
        counts: dict[str, int] = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        for issue in self.issues:
            counts[issue.severity] = counts.get(issue.severity, 0) + 1
        data["issue_counts"] = counts
        return data


def read_text_with_fallback(path: Path) -> tuple[str, str]:
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
    raise ValueError(f"Unable to decode {path} as UTF-8, UTF-16, GB18030, Big5, or CP1252")


def parse_time_parts(parts: tuple[str, ...], ms_digits: int) -> int:
    hours, minutes, seconds, fraction = parts
    raw_fraction = fraction.ljust(3, "0") if ms_digits == 3 else fraction.ljust(3, "0")
    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(raw_fraction[:3])
    )


def parse_srt(text: str) -> list[Cue]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cues: list[Cue] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        index: int | str = len(cues) + 1
        if re.fullmatch(r"\d+", line) and i + 1 < len(lines):
            index = int(line)
            i += 1
            line = lines[i].strip()

        match = TIMING_SRT.match(line)
        if not match:
            raise ValueError(f"Invalid or missing SRT timing near line {i + 1}: {line!r}")

        groups = match.groups()
        start_ms = parse_time_parts(groups[:4], 3)
        end_ms = parse_time_parts(groups[4:8], 3)
        i += 1

        text_lines: list[str] = []
        while i < len(lines) and lines[i].strip() != "":
            text_lines.append(lines[i])
            i += 1

        raw_text = "\n".join(text_lines)
        normalized = normalize_text(raw_text)
        cues.append(Cue(index=index, start_ms=start_ms, end_ms=end_ms, text=normalized, raw_text=raw_text))

    return cues


def parse_ass_time(value: str) -> int:
    match = TIMING_ASS.match(value)
    if not match:
        raise ValueError(f"Invalid ASS time: {value!r}")
    hours, minutes, seconds, centiseconds = match.groups()
    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(centiseconds.ljust(2, "0")) * 10
    )


def parse_ass(text: str) -> list[Cue]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    in_events = False
    fields: list[str] = []
    cues: list[Cue] = []

    for line_number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.lower() == "[events]":
            in_events = True
            continue
        if in_events and stripped.startswith("[") and stripped.endswith("]"):
            break
        if not in_events or not stripped:
            continue
        if stripped.lower().startswith("format:"):
            fields = [part.strip().lower() for part in stripped.split(":", 1)[1].split(",")]
            continue
        if not stripped.lower().startswith("dialogue:"):
            continue

        if not fields:
            fields = [
                "layer",
                "start",
                "end",
                "style",
                "name",
                "marginl",
                "marginr",
                "marginv",
                "effect",
                "text",
            ]

        body = stripped.split(":", 1)[1].lstrip()
        values = body.split(",", len(fields) - 1)
        if len(values) != len(fields):
            raise ValueError(f"ASS Dialogue field count mismatch at line {line_number}")
        row = dict(zip(fields, values))
        raw_text = row.get("text", "")
        cues.append(
            Cue(
                index=len(cues) + 1,
                start_ms=parse_ass_time(row["start"]),
                end_ms=parse_ass_time(row["end"]),
                text=normalize_text(raw_text),
                raw_text=raw_text,
            )
        )

    return cues


def parse_vtt_time(value: str) -> int:
    value = value.strip()
    match = re.fullmatch(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.](\d{3})", value)
    if not match:
        raise ValueError(f"Invalid WebVTT time: {value!r}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    milliseconds = int(match.group(4))
    return hours * 3_600_000 + minutes * 60_000 + seconds * 1_000 + milliseconds


def parse_vtt(text: str) -> list[Cue]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cues: list[Cue] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line or line == "WEBVTT" or line.startswith(("NOTE", "STYLE", "REGION")):
            i += 1
            continue

        cue_id: str | int = len(cues) + 1
        if "-->" not in line:
            cue_id = line
            i += 1
            if i >= len(lines):
                break
            line = lines[i].strip()

        if "-->" not in line:
            i += 1
            continue

        start_raw, end_raw = [part.strip().split()[0] for part in line.split("-->", 1)]
        start_ms = parse_vtt_time(start_raw)
        end_ms = parse_vtt_time(end_raw)
        i += 1

        text_lines: list[str] = []
        while i < len(lines) and lines[i].strip() != "":
            text_lines.append(lines[i])
            i += 1
        raw_text = "\n".join(text_lines)
        cues.append(
            Cue(
                index=cue_id,
                start_ms=start_ms,
                end_ms=end_ms,
                text=normalize_text(raw_text),
                raw_text=raw_text,
            )
        )

    return cues


def normalize_text(text: str) -> str:
    text = text.replace(r"\N", "\n").replace(r"\n", "\n").replace(r"\h", " ")
    text = ASS_TAG.sub("", text)
    text = HTML_TAG.sub("", text)
    text = text.replace("\u00a0", " ")
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def reading_units(text: str) -> int:
    plain = ASS_TAG.sub("", text)
    cjk_count = len(CJK.findall(plain))
    latin_words = len(LATIN_WORD.findall(plain))
    numbers = len(NUMBER.findall(plain))
    return cjk_count + latin_words + numbers


def choose_thresholds(language: str) -> tuple[float, int]:
    normalized = language.lower()
    if normalized in {"zh", "zh-hans", "zh-hant", "ja", "ko", "cjk"}:
        return 12.0, 18
    return 20.0, 42


def add_issue(
    issues: list[Issue],
    code: str,
    severity: str,
    message: str,
    cue: Cue | None = None,
    value: float | int | str | None = None,
) -> None:
    issues.append(Issue(code=code, severity=severity, message=message, cue=cue.index if cue else None, value=value))


def audit_cues(
    cues: list[Cue],
    *,
    language: str,
    max_cps: float | None,
    max_line_chars: int | None,
    max_lines: int,
    min_duration: float,
    max_duration: float,
    min_gap_ms: int,
) -> tuple[list[Issue], dict[str, float | int | str], list[float]]:
    defaults_cps, defaults_chars = choose_thresholds(language)
    cps_limit = max_cps if max_cps is not None else defaults_cps
    char_limit = max_line_chars if max_line_chars is not None else defaults_chars
    issues: list[Issue] = []
    cps_values: list[float] = []
    over_cps = 0
    previous_start_ms: int | None = None

    for cue in cues:
        if previous_start_ms is not None and cue.start_ms < previous_start_ms:
            add_issue(issues, "OUT_OF_ORDER", "P1", "Cue start time is earlier than the preceding cue.", cue)
        previous_start_ms = cue.start_ms
        if cue.end_ms <= cue.start_ms:
            add_issue(issues, "NON_POSITIVE_DURATION", "P0", "Cue has zero or negative duration.", cue)
            continue
        if not cue.text:
            add_issue(issues, "EMPTY_TEXT", "P0", "Cue contains no text.", cue)
            continue

        duration = cue.duration_s
        units = reading_units(cue.text)
        cps = units / duration if duration > 0 else math.inf
        cps_values.append(cps)

        if duration < min_duration:
            add_issue(
                issues,
                "SHORT_DURATION",
                "P2",
                f"Cue is shorter than {min_duration:.2f}s.",
                cue,
                round(duration, 2),
            )
        if duration > max_duration:
            add_issue(
                issues,
                "LONG_DURATION",
                "P2",
                f"Cue is longer than {max_duration:.2f}s.",
                cue,
                round(duration, 2),
            )
        if cps > cps_limit:
            over_cps += 1
            severity = "P1" if cps > cps_limit * 1.45 else "P2"
            add_issue(
                issues,
                "HIGH_CPS",
                severity,
                f"Reading speed {cps:.1f} exceeds limit {cps_limit:.1f} units/s.",
                cue,
                round(cps, 1),
            )

        lines = cue.lines
        if len(lines) > max_lines:
            add_issue(
                issues,
                "TOO_MANY_LINES",
                "P2",
                f"Cue has {len(lines)} text lines; maximum is {max_lines}.",
                cue,
                len(lines),
            )
        for line in lines:
            if len(line) > char_limit:
                add_issue(
                    issues,
                    "LONG_LINE",
                    "P2",
                    f"Line has {len(line)} characters; limit is {char_limit}.",
                    cue,
                    len(line),
                )

        if "\ufffd" in cue.text:
            add_issue(issues, "REPLACEMENT_CHAR", "P0", "Text contains the Unicode replacement character.", cue)
        if any(unicodedata.category(char) in {"Cc", "Cf"} and char not in "\n\t" for char in cue.text):
            add_issue(issues, "CONTROL_CHAR", "P1", "Text contains an unexpected control character.", cue)
        if "  " in cue.text:
            add_issue(issues, "DOUBLE_SPACE", "P3", "Text contains repeated spaces.", cue)
        if re.search(r"\{\\[^}]+}", cue.raw_text):
            add_issue(issues, "ASS_TAG_IN_PLAIN_TEXT", "P1", "Raw text appears to contain an ASS override tag.", cue)
        if re.search(r"[!?！？]{2,}", cue.text):
            add_issue(issues, "REPEATED_TERMINAL_PUNCT", "P3", "Repeated terminal punctuation may be unintended.", cue)

    for previous, current in zip(cues, cues[1:]):
        if previous.end_ms > current.start_ms:
            add_issue(
                issues,
                "OVERLAP",
                "P1",
                f"Overlaps the following cue by {previous.end_ms - current.start_ms} ms.",
                previous,
                previous.end_ms - current.start_ms,
            )
        gap = current.start_ms - previous.end_ms
        if min_gap_ms > 0 and 0 <= gap < min_gap_ms:
            add_issue(
                issues,
                "SHORT_GAP",
                "P3",
                f"Gap to the next cue is only {gap} ms.",
                previous,
                gap,
            )
        if previous.text and current.text and previous.text == current.text:
            add_issue(
                issues,
                "DUPLICATE_ADJACENT",
                "P3",
                "Identical text appears in adjacent cues; verify that the repetition is intentional.",
                current,
            )

    check_delimiters_across_cues(cues, issues, "“", "”", "UNBALANCED_QUOTES", "Chinese quotation marks")
    check_delimiters_across_cues(cues, issues, "(", ")", "UNBALANCED_PARENS", "Parentheses")
    check_delimiters_across_cues(cues, issues, "（", "）", "UNBALANCED_FULLWIDTH_PARENS", "Full-width parentheses")

    durations = [cue.duration_s for cue in cues if cue.end_ms > cue.start_ms]
    cps_over = sum(1 for value in cps_values if value > cps_limit)
    settings: dict[str, float | int | str] = {
        "language_profile": language,
        "max_cps": cps_limit,
        "max_line_chars": char_limit,
        "max_lines": max_lines,
        "min_duration_s": min_duration,
        "max_duration_s": max_duration,
        "min_gap_ms": min_gap_ms,
        "mean_duration_s": round(statistics.fmean(durations), 2) if durations else 0,
        "median_cps": round(statistics.median(cps_values), 1) if cps_values else 0,
        "cues_over_cps": cps_over,
    }
    return issues, settings, cps_values


def check_delimiters_across_cues(
    cues: list[Cue],
    issues: list[Issue],
    opening: str,
    closing: str,
    code: str,
    label: str,
) -> None:
    depth = 0
    opening_cue: Cue | None = None

    for cue in cues:
        opens = cue.text.count(opening)
        closes = cue.text.count(closing)
        if closes > depth + opens:
            add_issue(issues, f"{code}_EARLY_CLOSE", "P2", f"{label} close without a matching open.", cue)
        depth = max(0, depth + opens - closes)
        if depth > 0 and opening_cue is None:
            opening_cue = cue
        if depth == 0 and opening_cue is not None:
            opening_cue = None

    if depth > 0 and opening_cue is not None:
        add_issue(issues, code, "P2", f"{label} remain open at the end of the subtitle.", opening_cue)


def calculate_technical_score(issues: list[Issue], cue_count: int) -> int:
    counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1

    # Blockers and major defects remain individual deductions. Moderate and
    # cosmetic findings are normalized by project size so a large subtitle is
    # not automatically pushed to zero by a small percentage of long lines.
    score = 100.0
    score -= min(80, counts["P0"] * 40)
    score -= min(45, counts["P1"] * 10)
    if cue_count > 0:
        score -= min(25, (counts["P2"] / cue_count) * 50)
        score -= min(10, (counts["P3"] / cue_count) * 20)
    return max(0, int(round(score)))


def detect_subtitle_format(path: Path, text: str) -> str:
    suffix = path.suffix.lower()
    if suffix == ".srt":
        return "SRT"
    if suffix in {".ass", ".ssa"}:
        return "ASS"
    if suffix == ".vtt":
        return "WebVTT"

    stripped = text.lstrip("\ufeff \t\r\n")
    if stripped.startswith("WEBVTT"):
        return "WebVTT"
    if "[Script Info]" in text[:2000] or "[Events]" in text[:4000]:
        return "ASS"
    if "-->" in text[:5000] and re.search(r"\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}\s*-->", text[:5000]):
        return "SRT"
    raise ValueError(f"Unsupported or unrecognized subtitle format: {path.suffix or '(no extension)'}")


def audit_file(
    path: Path,
    *,
    language: str,
    max_cps: float | None,
    max_line_chars: int | None,
    max_lines: int,
    min_duration: float,
    max_duration: float,
    min_gap_ms: int,
) -> Audit:
    text, encoding = read_text_with_fallback(path)
    format_name = detect_subtitle_format(path, text)
    if format_name == "SRT":
        cues = parse_srt(text)
    elif format_name == "ASS":
        cues = parse_ass(text)
    elif format_name == "WebVTT":
        cues = parse_vtt(text)
    else:
        raise ValueError(f"Unsupported subtitle format: {format_name}")

    issues, settings, cps_values = audit_cues(
        cues,
        language=language,
        max_cps=max_cps,
        max_line_chars=max_line_chars,
        max_lines=max_lines,
        min_duration=min_duration,
        max_duration=max_duration,
        min_gap_ms=min_gap_ms,
    )
    if not cues:
        add_issue(issues, "EMPTY_SUBTITLE", "P0", "Subtitle file contains no parseable cues.")
    score = calculate_technical_score(issues, len(cues))
    severities = {issue.severity for issue in issues}
    status = "FAIL" if severities & {"P0", "P1"} else "WARN" if issues else "PASS"
    first_start = min((cue.start_ms for cue in cues), default=None)
    last_end = max((cue.end_ms for cue in cues), default=None)
    span_s = (last_end - first_start) / 1000 if first_start is not None and last_end is not None else None

    return Audit(
        path=str(path),
        format=format_name,
        encoding=encoding,
        cue_count=len(cues),
        first_start_ms=first_start,
        last_end_ms=last_end,
        span_s=round(span_s, 3) if span_s is not None else None,
        mean_cps=round(statistics.fmean(cps_values), 1) if cps_values else None,
        max_cps=round(max(cps_values), 1) if cps_values else None,
        cues_over_cps=settings["cues_over_cps"],
        issues=issues,
        technical_score=score,
        status=status,
        settings=settings,
    )


def format_time(ms: int | None) -> str:
    if ms is None:
        return "-"
    hours, remainder = divmod(ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def render_markdown(report: Audit) -> str:
    data = report.to_dict()
    counts = data["issue_counts"]
    lines = [
        "# Subtitle Technical Audit",
        "",
        f"- File: `{report.path}`",
        f"- Format: {report.format}",
        f"- Encoding: {report.encoding}",
        f"- Cue count: {report.cue_count}",
        f"- Time span: {format_time(report.first_start_ms)} to {format_time(report.last_end_ms)}",
        f"- Mean reading speed: {report.mean_cps if report.mean_cps is not None else '-'} units/s",
        f"- Maximum reading speed: {report.max_cps if report.max_cps is not None else '-'} units/s",
        f"- Cues over CPS limit: {report.cues_over_cps}",
        f"- Issues: P0={counts['P0']}, P1={counts['P1']}, P2={counts['P2']}, P3={counts['P3']}",
        f"- Technical-health score: {report.technical_score}/100",
        f"- Technical status: **{report.status}**",
        "",
        "> This score covers mechanics and readability only. It is not the semantic translation score.",
        "",
        "## Settings",
        "",
    ]
    for key, value in report.settings.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Issues", ""])
    if not report.issues:
        lines.append("No automated issues found.")
    else:
        lines.append("| Severity | Code | Cue | Value | Message |")
        lines.append("|---|---|---:|---:|---|")
        for issue in sorted(report.issues, key=lambda item: ({"P0": 0, "P1": 1, "P2": 2, "P3": 3}[item.severity], str(item.cue))):
            value = "" if issue.value is None else str(issue.value)
            lines.append(f"| {issue.severity} | {issue.code} | {issue.cue or ''} | {value} | {issue.message} |")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit SRT, ASS, or WebVTT subtitles.")
    parser.add_argument("input", type=Path, help="Subtitle file to audit")
    parser.add_argument("--format", choices=("md", "json"), default="md", help="Report format")
    parser.add_argument("--output", type=Path, help="Write report to this path instead of stdout")
    parser.add_argument("--language", default="auto", help="zh, zh-Hant, ja, ko, latin, or auto")
    parser.add_argument("--max-cps", type=float, help="Override maximum reading units per second")
    parser.add_argument("--max-line-chars", type=int, help="Override maximum characters per line")
    parser.add_argument("--max-lines", type=int, default=2, help="Maximum text lines per cue")
    parser.add_argument("--min-duration", type=float, default=0.8, help="Minimum cue duration in seconds")
    parser.add_argument("--max-duration", type=float, default=7.0, help="Maximum cue duration in seconds")
    parser.add_argument("--min-gap-ms", type=int, default=0, help="Warn when a gap is below this value; 0 disables")
    parser.add_argument("--no-fail", action="store_true", help="Return exit code 0 even when P0/P1 issues exist")
    return parser


def main() -> int:
    configure_stdio()
    args = build_parser().parse_args()
    try:
        report = audit_file(
            args.input,
            language=args.language,
            max_cps=args.max_cps,
            max_line_chars=args.max_line_chars,
            max_lines=args.max_lines,
            min_duration=args.min_duration,
            max_duration=args.max_duration,
            min_gap_ms=args.min_gap_ms,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        rendered = json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
    else:
        rendered = render_markdown(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(rendered)

    if args.no_fail:
        return 0
    return 1 if report.status == "FAIL" else 0


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (AttributeError, ValueError):
                pass


if __name__ == "__main__":
    raise SystemExit(main())
