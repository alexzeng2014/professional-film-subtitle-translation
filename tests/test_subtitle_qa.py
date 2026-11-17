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


if __name__ == "__main__":
    unittest.main()
