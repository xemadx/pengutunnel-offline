#!/usr/bin/env python3
"""Reproduce the r3 DNS correction from the exact reviewed r2 ELF.

This patches a shipped binary; it is not a compiler for the original engine.
The DNS fast path builds sockaddr_in. An unspecified "udp" listener can
instead open an IPv6 dual-stack socket, whose sockaddr_in6 source address is
misread as 0.0.0.0 by that fast path. Resolve and listen with "udp4" so the
socket family matches the existing sender. IPv6 DNS is explicitly unsupported.
No functions, stack frames, call sites, Go stack maps or file sizes are added.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

INPUT_SHA256 = "5d58cdde3483029a70c8b52b9434c4fe4bb4fbc093e47c5c38aba4be9361fb52"
OUTPUT_SHA256 = "495044c59b0d9515e0ca9b741e81cecabb04a0698a7ad252259de0e52906a250"
EDITS = [
    (0x18DB3A1, "488d05cac16700", "488d0570040000"),
    (0x18DB3C8, "488d05a3c16700", "488d0549040000"),
    (0x18DB3A8, "bb03000000", "bb04000000"),
    (0x18DB3C0, "bb03000000", "bb04000000"),
    (0x18DB818, "cccccccc", "75647034"),
]


def patch(data: bytes) -> tuple[bytes, dict]:
    if hashlib.sha256(data).hexdigest() != INPUT_SHA256:
        raise ValueError("Wrong input: only the exact reviewed v5.1.3-r2 ELF is accepted")
    output = bytearray(data)
    edits = []
    for address, before_hex, after_hex in EDITS:
        offset = address - 0x400000
        before, after = bytes.fromhex(before_hex), bytes.fromhex(after_hex)
        if len(before) != len(after) or output[offset:offset + len(before)] != before:
            raise ValueError(f"Patch precondition failed at {address:#x}")
        output[offset:offset + len(after)] = after
        edits.append(dict(address=hex(address), offset=offset, before=before_hex, after=after_hex))
    # Check both RIP-relative references, the immutable literal and the final file.
    for address in (0x18DB3A1, 0x18DB3C8):
        offset = address - 0x400000
        destination = address + 7 + struct.unpack_from("<i", output, offset + 3)[0]
        if destination != 0x18DB818:
            raise ValueError("Invalid udp4 string reference")
    actual = hashlib.sha256(output).hexdigest()
    if actual != OUTPUT_SHA256:
        raise ValueError("Unexpected output digest")
    return bytes(output), dict(input_sha256=INPUT_SHA256, output_sha256=actual,
                              output_bytes=len(output), edits=edits,
                              purpose="Match DNS listener socket family to its IPv4 batch sender")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Exact v5.1.3-r2 offline ELF")
    parser.add_argument("output", type=Path, help="A new destination file")
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    output, metadata = patch(args.input.read_bytes())
    with args.output.open("xb") as stream:
        stream.write(output)
    args.output.chmod(0o755)
    if args.metadata:
        with args.metadata.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(metadata, stream, indent=2)
            stream.write("\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
