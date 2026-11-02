#!/usr/bin/env python3
"""Pin the manager digest and regenerate the distributable file manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="A new package tag, e.g. v5.1.3-r4")
    args = parser.parse_args()
    if args.version:
        if not re.fullmatch(r"v\d+\.\d+\.\d+-r[1-9]\d*", args.version):
            raise SystemExit("Invalid release tag")
        for name in ("install.sh", "install-offline.sh"):
            path = ROOT / name
            text = path.read_text(encoding="utf-8")
            text, count = re.subn(r'PACKAGE_VERSION="[^"]+"', f'PACKAGE_VERSION="{args.version}"', text)
            if count != 1:
                raise SystemExit(f"Missing package version in {name}")
            path.write_text(text, encoding="utf-8", newline="\n")
    manager_sha = hashlib.sha256((ROOT / "install-offline.sh").read_bytes()).hexdigest()
    bootstrap = ROOT / "install.sh"
    text = bootstrap.read_text(encoding="utf-8")
    text, count = re.subn(r'MANAGER_SHA="[^"]+"', f'MANAGER_SHA="{manager_sha}"', text)
    if count != 1:
        raise SystemExit("Missing bootstrap digest")
    bootstrap.write_text(text, encoding="utf-8", newline="\n")
    version = re.search(r'PACKAGE_VERSION="([^"]+)"', text).group(1)
    files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode().split("\0")
    hashes = {}
    for name in sorted(set(files)):
        if not name or name == "offline-package-manifest.json":
            continue
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"Not a regular distribution file: {name}")
        data = path.read_bytes()
        if path.suffix != ".elf" and b"\r\n" in data:
            data = data.replace(b"\r\n", b"\n")
            path.write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()
    manifest = dict(package_version=version, core_version="v5.1.3", platform="linux-amd64",
                    core_sha256=hashes["pengutunnel.offline.elf"], files=hashes)
    (ROOT / "offline-package-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Pinned {len(hashes)} files for {version}; manager {manager_sha}")


if __name__ == "__main__":
    main()
