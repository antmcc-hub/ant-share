"""Run the pinned OSV CLI on Linux or macOS without a persistent installation."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import urllib.request

VERSION = "2.7.1"
# Published release asset digests, checked 12 Nov 2026.
DIGESTS = {
    "darwin_amd64": "b8420d5485ba792626315f1bf9a5a2046e971d38eea75bf9090c38852dbc3b1b",
    "darwin_arm64": "b22c02877a811c8f78956e8643efa554932b7378f590d13f8e97d4e9448a29f3",
    "linux_amd64": "fb7dab19a8bd9bbe5c3189f09d4b7ee1820c9553a23bac202648a56efd2f6ee8",
    "linux_arm64": "983d22fbad9724514e3fcc6acc83b5fa64c5ffa6b0d9f510028f22c1b223ff81",
}


def asset_name(system, machine):
    arch = {"arm64": "arm64", "aarch64": "arm64",
            "x86_64": "amd64", "amd64": "amd64"}.get(machine.lower())
    target = system.lower() + "_" + str(arch)
    if target not in DIGESTS:
        raise ValueError("Unsupported runner platform")
    return target


def download(directory, target):
    url = ("https://github.com/google/osv-scanner/releases/download/v" + VERSION
           + "/osv-scanner_" + target)
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(128 * 1024 * 1024 + 1)
    if len(data) > 128 * 1024 * 1024 or hashlib.sha256(data).hexdigest() != DIGESTS[target]:
        raise ValueError("OSV release checksum mismatch")
    binary = Path(directory) / "osv-scanner"
    binary.write_bytes(data)
    binary.chmod(0o700)
    return binary


def main():
    try:
        target = asset_name(platform.system(), platform.machine())
        with tempfile.TemporaryDirectory(prefix="security-osv-", dir=os.getenv("RUNNER_TEMP")) as directory:
            binary = download(directory, target)
            output = Path(directory) / "main-results.json"
            result = subprocess.run([str(binary), "scan", "source", "--recursive", "--allow-no-lockfiles",
                                     "--format=json", "--output-file=" + str(output), "."], check=False)
            report = json.loads(output.read_text())
            if not isinstance(report, dict) or "results" not in report:
                raise ValueError("No complete OSV report")
            print("OSV weekly full scan exit:", result.returncode)
            return result.returncode
    except (OSError, ValueError, KeyError):
        print("OSV weekly scan unavailable; refusing a clean result", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
