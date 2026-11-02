"""Trusted parent promotion for explicitly named, bounded engine exports."""
import os
import stat
import json


def export(g):
    label = json.loads((g["ROOT"] / "package/offline-package-manifest.json").read_text(encoding="utf-8"))["package_version"]
    result = g["execute"]("a", ["/usr/bin/python3", "/package/tools/export_engine.py",
                                "--output", "/scratch/export", "--label", label], timeout=210)
    if result.get("exit") != 0:
        raise AssertionError(result)
    source = g["SCR"] / "export"
    destination = g["OUT"]
    source_fd = os.open(source, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    destination_fd = os.open(destination, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    total = 0
    try:
        for name, limit in ((f"engine-functions-{label}.tsv", 5000000),
                            (f"engine-assembly-{label}.asm.gz", 80000000),
                            (f"engine-analysis-{label}.json", 10000)):
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=source_fd)
            try:
                before = os.fstat(fd)
                if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > limit:
                    raise ValueError("Unsafe export: " + name)
                data = bytearray()
                while len(data) < before.st_size:
                    block = os.read(fd, min(1048576, before.st_size - len(data)))
                    if not block:
                        raise ValueError("Short export")
                    data.extend(block)
                after = os.fstat(fd)
                if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_nlink) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_nlink):
                    raise ValueError("Changed export")
            finally:
                os.close(fd)
            total += len(data)
            if total > 85000000:
                raise ValueError("Export total limit")
            output = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=destination_fd)
            with os.fdopen(output, "wb") as stream:
                stream.write(data)
    finally:
        os.close(source_fd)
        os.close(destination_fd)
    return result
