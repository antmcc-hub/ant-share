"""Synthetic scanner transport only; no network, credentials or package execution."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("weekly", ROOT / "scripts/osv_weekly.py")
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)


class WeeklyTests(unittest.TestCase):
    def test_empty_inventory_is_supported_but_findings_and_errors_fail(self):
        for code in [0, 1, 127]:
            with tempfile.TemporaryDirectory() as parent:
                def scan(argv, check):
                    output = next(a.split("=", 1)[1] for a in argv if a.startswith("--output-file="))
                    Path(output).write_text(json.dumps({"results": None}))
                    self.assertIn("--recursive", argv)
                    self.assertIn("--allow-no-lockfiles", argv)
                    return SimpleNamespace(returncode=code)
                with patch.dict(os.environ, RUNNER_TEMP=parent):
                    with patch.object(weekly, "download", return_value=Path("/synthetic/osv")):
                        with patch.object(weekly.subprocess, "run", side_effect=scan):
                            self.assertEqual(weekly.main(), code)
                self.assertEqual(list(Path(parent).iterdir()), [])

    def test_missing_or_malformed_report_cannot_pass(self):
        for report in [None, "bad", "{}"]:
            with tempfile.TemporaryDirectory() as parent:
                def scan(argv, check):
                    if report is not None:
                        output = next(a.split("=", 1)[1] for a in argv if a.startswith("--output-file="))
                        Path(output).write_text(report)
                    return SimpleNamespace(returncode=0)
                with patch.dict(os.environ, RUNNER_TEMP=parent):
                    with patch.object(weekly, "download", return_value=Path("/synthetic/osv")):
                        with patch.object(weekly.subprocess, "run", side_effect=scan):
                            self.assertEqual(weekly.main(), 2)
                self.assertEqual(list(Path(parent).iterdir()), [])

    def test_checksum_failure_is_closed_and_cleans_scratch(self):
        with tempfile.TemporaryDirectory() as parent:
            with patch.dict(os.environ, RUNNER_TEMP=parent):
                with patch.object(weekly, "download", side_effect=ValueError("checksum")):
                    self.assertEqual(weekly.main(), 2)
            self.assertEqual(list(Path(parent).iterdir()), [])

    def test_all_supported_runner_architectures_and_unknown_refusal(self):
        for system, machine, target in [
            ("Linux", "x86_64", "linux_amd64"), ("Linux", "aarch64", "linux_arm64"),
            ("Darwin", "x86_64", "darwin_amd64"), ("Darwin", "arm64", "darwin_arm64")]:
            self.assertEqual(weekly.asset_name(system, machine), target)
        with self.assertRaises(ValueError):
            weekly.asset_name("Windows", "AMD64")

    def test_corrupt_release_never_becomes_an_executable(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(weekly.urllib.request, "urlopen", return_value=io.BytesIO(b"wrong")):
                with self.assertRaises(ValueError):
                    weekly.download(directory, "linux_amd64")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_valid_release_is_pinned_and_executable(self):
        data = b"synthetic executable"
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(weekly.DIGESTS, linux_amd64=hashlib.sha256(data).hexdigest()):
                with patch.object(weekly.urllib.request, "urlopen", return_value=io.BytesIO(data)) as read:
                    binary = weekly.download(directory, "linux_amd64")
            self.assertEqual(binary.read_bytes(), data)
            self.assertTrue(binary.stat().st_mode & 0o100)
            self.assertIn("/v2.7.1/osv-scanner_linux_amd64", read.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
