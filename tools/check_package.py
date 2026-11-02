#!/usr/bin/env python3
"""Check every distributed byte and bootstrap integrity pin without running ELF."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from patch_core import EDITS, INPUT_SHA256, patch

ROOT = Path(__file__).resolve().parent.parent


def verify():
    manifest = json.loads((ROOT / "offline-package-manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files"].items():
        parts = PurePosixPath(name)
        if parts.is_absolute() or ".." in parts.parts:
            raise ValueError(f"Invalid manifest path: {name}")
        path = ROOT / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Package integrity mismatch: {name}")
    bootstrap = (ROOT / "install.sh").read_text(encoding="utf-8")
    for key, name in (("CORE_SHA", "pengutunnel.offline.elf"), ("MANAGER_SHA", "install-offline.sh")):
        pin = re.search(rf'^{key}="([0-9a-f]{{64}})"$', bootstrap, re.M)
        if not pin or pin.group(1) != manifest["files"][name]:
            raise ValueError(f"Bootstrap {key} does not match the distribution")
    for name in ("install.sh", "install-offline.sh"):
        if f'PACKAGE_VERSION="{manifest["package_version"]}"' not in (ROOT / name).read_text(encoding="utf-8"):
            raise ValueError("Package tag differs between manifest and scripts")
    current = (ROOT / "pengutunnel.offline.elf").read_bytes()
    previous = bytearray(current)
    for address, before_hex, after_hex in EDITS:
        offset = address - 0x400000
        after = bytes.fromhex(after_hex)
        if previous[offset:offset + len(after)] != after:
            raise ValueError("DNS correction bytes differ")
        previous[offset:offset + len(after)] = bytes.fromhex(before_hex)
    if hashlib.sha256(previous).hexdigest() != INPUT_SHA256 or patch(bytes(previous))[0] != current:
        raise ValueError("Published core does not reproduce from the reviewed r2 input")
    return manifest


if __name__ == "__main__":
    m = verify()
    print(f'PASS: {len(m["files"])} distribution digests and both bootstrap pins ({m["package_version"]})')
