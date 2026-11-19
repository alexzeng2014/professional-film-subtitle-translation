import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "srt_to_ass.py"


class SrtToAssTests(unittest.TestCase):
    def test_cli_writes_utf8_without_bom_and_crlf(self):
        source = """1
00:00:00,000 --> 00:00:02,000
第一句

2
00:00:02,000 --> 00:00:04,000
Second line
"""
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.srt"
            output_path = Path(directory) / "output.ass"
            input_path.write_text(source, encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(input_path), str(output_path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            raw = output_path.read_bytes()
            self.assertTrue(raw.startswith(b"[Script Info]"))
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
            self.assertIn(b"\r\n", raw)
            self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
            self.assertEqual(raw.count(b"Dialogue:"), 2)


if __name__ == "__main__":
    unittest.main()
