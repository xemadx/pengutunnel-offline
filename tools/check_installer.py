#!/usr/bin/env python3
"""Checks bootstrap integrity gates without running the ELF or installing services."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def run(script, args, expected, env=None):
    result = subprocess.run(["bash", str(script), "--verify-only", *args],
                            text=True, capture_output=True, env=env, timeout=30)
    assert (result.returncode == 0) == expected, result.stdout + result.stderr
    return result


run(ROOT / "install.sh", [], True)
with tempfile.TemporaryDirectory(prefix="pengu-bootstrap-check-") as temporary:
    work = Path(temporary)
    package = work / "package"
    package.mkdir()
    for name in ("pengutunnel.offline.elf", "install-offline.sh"):
        shutil.copyfile(ROOT / name, package / name)
    with (package / "pengutunnel.offline.elf").open("r+b") as stream:
        original = stream.read(1)
        stream.seek(0)
        stream.write(bytes([original[0] ^ 1]))
    assert "checksum mismatch" in run(ROOT / "install.sh", ["--source-dir", str(package)], False).stderr
    with (package / "pengutunnel.offline.elf").open("r+b") as stream:
        stream.write(original)
    with (package / "install-offline.sh").open("ab") as stream:
        stream.write(b"\n# changed\n")
    assert "checksum mismatch" in run(ROOT / "install.sh", ["--source-dir", str(package)], False).stderr
    shutil.copyfile(ROOT / "install-offline.sh", package / "install-offline.sh")
    run(ROOT / "install.sh", ["--source-dir", str(package)], True)
    run(ROOT / "install.sh", ["--ref", "../bad"], False)
    run(ROOT / "install.sh", ["--source-dir", str(work / "missing")], False)

    # Exercise the remote-fetch branch with a local curl fixture. No network or root changes.
    isolated = work / "bootstrap"
    isolated.mkdir()
    shutil.copyfile(ROOT / "install.sh", isolated / "install.sh")
    commands = work / "commands"
    commands.mkdir()
    curl = commands / "curl"
    curl.write_text('''#!/usr/bin/env bash
set -euo pipefail
url=""; output=""
while (($#)); do
  case "$1" in
    --output) output="$2"; shift 2 ;;
    https://*) url="$1"; shift ;;
    *) shift ;;
  esac
done
[[ "$url" == https://raw.githubusercontent.com/xemadx/pengutunnel-offline/deadbeef/* ]]
printf '%s\\n' "$url" >> "$CHECK_REQUESTS"
cp -- "$CHECK_PACKAGE/${url##*/}" "$output"
''')
    curl.chmod(0o755)
    env = dict(os.environ, PATH=f"{commands}:{os.environ['PATH']}",
               CHECK_PACKAGE=str(package), CHECK_REQUESTS=str(work / "requests"))
    run(isolated / "install.sh", ["--ref", "deadbeef"], True, env)
    assert len((work / "requests").read_text().splitlines()) == 2
print("PASS: local package, both tamper gates, invalid ref, missing files, remote-fetch fixture")
