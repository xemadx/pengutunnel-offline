#!/usr/bin/env python3
"""Export every Go function boundary and every .text instruction, not Go source."""
import argparse
import bisect
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
from check_package import ROOT


def inventory(data):
    if data[:6] != b"\x7fELF\x02\x01":
        raise ValueError("Expected ELF64 little-endian")
    section_offset = struct.unpack_from("<Q", data, 40)[0]
    size, count, name_index = struct.unpack_from("<HHH", data, 58)
    headers = [struct.unpack_from("<IIQQQQIIQQ", data, section_offset + i * size) for i in range(count)]
    names_header = headers[name_index]
    names = data[names_header[4]:names_header[4] + names_header[5]]
    sections = {names[h[0]:].split(b"\0", 1)[0].decode(): h for h in headers}
    p = sections[".gopclntab"][4]
    number = struct.unpack_from("<Q", data, p + 8)[0]
    if number > 100000:
        raise ValueError("Function table limit")
    text, fnames, _, _, _, table = struct.unpack_from("<QQQQQQ", data, p + 24)
    text = text or sections[".text"][3]
    functions = []
    for i in range(number):
        entry, offset = struct.unpack_from("<II", data, p + table + i * 8)
        name_offset = struct.unpack_from("<i", data, p + table + offset + 4)[0]
        start = p + fnames + name_offset
        end = data.index(b"\0", start, start + 2000)
        name = data[start:end].decode("utf-8", "replace").replace("\t", " ").replace("\n", " ")
        following = struct.unpack_from("<I", data, p + table + (i + 1) * 8)[0]
        functions.append((text + entry, text + following, name))
    return functions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=ROOT / "pengutunnel.offline.elf")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--label")
    args = parser.parse_args()
    if args.label is None:
        args.label = json.loads((ROOT / "offline-package-manifest.json").read_text(encoding="utf-8"))["package_version"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", args.label):
        raise SystemExit("Invalid label")
    data = args.binary.read_bytes()
    if len(data) > 60000000:
        raise SystemExit("Binary size limit")
    digest = hashlib.sha256(data).hexdigest()
    functions = inventory(data)
    starts = [row[0] for row in functions]
    args.output.mkdir(parents=True, exist_ok=True)
    catalog = args.output / f"engine-functions-{args.label}.tsv"
    catalog.write_text("address\tend\tname\n" + "".join(f"{a:#x}\t{b:#x}\t{n}\n" for a, b, n in functions), encoding="utf-8", newline="\n")
    assembly = args.output / f"engine-assembly-{args.label}.asm.gz"
    command = ["objdump", "-d", "-M", "intel", "--no-show-raw-insn", "-j", ".text", str(args.binary)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    instructions = total = 0
    current = None
    try:
        with assembly.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=1, mtime=0) as output:
            output.write(f"; SHA256 {digest}\n; Complete .text disassembly; not recovered source or a proof of all behavior.\n".encode())
            for raw_line in process.stdout:
                total += len(raw_line)
                if total > 400000000:
                    raise ValueError("Disassembly output limit")
                line = raw_line.decode("utf-8", "replace")
                if str(args.binary) in line:
                    line = line.replace(str(args.binary), "pengutunnel.offline.elf")
                match = re.match(r"\s*([0-9a-f]+):\s+(.+)", line)
                if match:
                    address = int(match.group(1), 16)
                    index = bisect.bisect_right(starts, address) - 1
                    if index >= 0 and address < functions[index][1] and current != index:
                        current = index
                        a, b, name = functions[index]
                        output.write(f"\n; FUNCTION {a:#x} end={b:#x} {name or '[name removed]'}\n".encode())
                    instructions += 1
                output.write(line.encode())
        stderr = process.stderr.read()
        if process.wait(timeout=5) != 0:
            raise RuntimeError(stderr.decode("utf-8", "replace")[:1000])
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    metadata = args.output / f"engine-analysis-{args.label}.json"
    metadata.write_text(json.dumps(dict(binary_sha256=digest, binary_bytes=len(data),
        functions=len(functions), named_functions=sum(bool(row[2]) for row in functions),
        instructions=instructions, complete_text=True,
        scope="All machine-code instructions and pclntab boundaries; not original source, complete decompilation or complete semantic understanding"), indent=2) + "\n", encoding="utf-8")
    sums = args.output / "SHA256SUMS"
    with sums.open("a", encoding="utf-8", newline="\n") as stream:
        for file in (catalog, assembly, metadata):
            stream.write(f"{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.name}\n")
    print(f"Exported {len(functions)} functions and {instructions} instructions: {digest}")


if __name__ == "__main__":
    main()
