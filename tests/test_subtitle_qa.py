import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import subtitle_qa


class SubtitleQATests(unittest.TestCase):
    def test_detects_mixed_chinese_variant_and_final_period(self):
        source = """1
00:00:00,000 --> 00:00:03,000
我们在说话。

2
00:00:03,000 --> 00:00:06,000
我們這國說話
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mixed.srt"
            path.write_text(source, encoding="utf-8")
            report = subtitle_qa.audit_file(
                path,
                language="zh-Hans",
                max_cps=None,
                max_line_chars=None,
                max_lines=2,
                min_duration=0.8,
                max_duration=7.0,
                min_gap_ms=0,
            )

        codes = {issue.code for issue in report.issues}
        self.assertIn("MIXED_CHINESE_SCRIPT", codes)
        self.assertIn("CHINESE_FINAL_PERIOD", codes)

    def test_auto_detects_cjk_reading_profile(self):
        source = """1
00:00:00,000 --> 00:00:03,000
这句话很短
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chinese.srt"
            path.write_text(source, encoding="utf-8")
            report = subtitle_qa.audit_file(
                path,
                language="auto",
                max_cps=None,
                max_line_chars=None,
                max_lines=2,
                min_duration=0.8,
                max_duration=7.0,
                min_gap_ms=0,
            )

        self.assertEqual(report.settings["language_profile"], "zh")
        self.assertEqual(report.settings["max_cps"], 12.0)

    def test_flags_utf8_bom_in_ass(self):
        source = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,SimSun,56,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2.3,0.7,2,80,80,58,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:03.00,Default,,0,0,0,,测试
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bom.ass"
            path.write_bytes(b"\xef\xbb\xbf" + source.encode("utf-8"))
            report = subtitle_qa.audit_file(
                path,
                language="zh-Hans",
                max_cps=None,
                max_line_chars=None,
                max_lines=2,
                min_duration=0.8,
                max_duration=7.0,
                min_gap_ms=0,
            )

        codes = {issue.code for issue in report.issues}
        self.assertIn("UTF8_BOM", codes)
        self.assertEqual(report.status, "FAIL")


if __name__ == "__main__":
    unittest.main()
