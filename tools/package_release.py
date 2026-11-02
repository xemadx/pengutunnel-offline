#!/usr/bin/env python3
"""Package reviewed bytes reproducibly; this does not compile the upstream core."""
import argparse
import gzip
import hashlib
import io
import os
from pathlib import Path
import shutil
import tarfile
from check_package import ROOT, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    manifest = verify()
    args.output.mkdir(parents=True, exist_ok=True)
    version = manifest["package_version"]
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", "0"))
    archive = args.output / f"pengutunnel-offline-{version}-linux-amd64.tar.gz"
    names = sorted([*manifest["files"], "offline-package-manifest.json"])
    with archive.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch) as compressed:
        with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as tar:
            for name in names:
                data = (ROOT / name).read_bytes()
                info = tarfile.TarInfo(f"pengutunnel-offline/{name}")
                info.size = len(data)
                info.mtime = epoch
                info.mode = 0o755 if name.endswith((".sh", ".elf")) else 0o644
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(data))
    assets = [archive]
    for name in ("install.sh", "install-offline.sh", "pengutunnel.offline.elf", "offline-package-manifest.json"):
        destination = args.output / name
        shutil.copyfile(ROOT / name, destination)
        assets.append(destination)
    sums = args.output / "SHA256SUMS"
    sums.write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in sorted(assets)), encoding="utf-8", newline="\n")
    print(f"Packaged {version}: {archive}")


if __name__ == "__main__":
    main()
