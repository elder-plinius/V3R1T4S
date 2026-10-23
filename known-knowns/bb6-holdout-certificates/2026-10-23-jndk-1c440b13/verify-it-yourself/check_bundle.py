#!/usr/bin/env python3
"""Check package hashes and safely reconstruct its compressed proof packet."""
import hashlib
import io
import pathlib
import sys
import tarfile

ROOT = pathlib.Path.cwd()

def fail(message):
    print("FAIL:", message)
    raise SystemExit(1)

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

sums_path = ROOT / "SHA256SUMS"
if not sums_path.is_file():
    fail("missing SHA256SUMS")
expected = {}
for line in sums_path.read_text().splitlines():
    fields = line.strip().split(None, 1)
    if len(fields) != 2 or len(fields[0]) != 64:
        fail("malformed SHA256SUMS line")
    rel = fields[1].lstrip("*").removeprefix("./")
    p = pathlib.PurePosixPath(rel)
    if p.is_absolute() or ".." in p.parts or rel == "SHA256SUMS":
        fail("unsafe SHA256SUMS path")
    expected[rel] = fields[0]
actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p != sums_path}
if actual != set(expected):
    fail("SHA256SUMS file set mismatch")
for rel, want in expected.items():
    if sha(ROOT / rel) != want:
        fail("SHA256SUMS mismatch: " + rel)

parts = sorted((ROOT / "object").glob("proof_bundle.part-*"))
if not parts:
    fail("missing proof bundle parts")
blob = b"".join(p.read_bytes() for p in parts)
want = (ROOT / "object/proof_bundle.sha256").read_text().strip()
if hashlib.sha256(blob).hexdigest() != want:
    fail("proof bundle digest mismatch")
try:
    archive = tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz")
except (tarfile.TarError, OSError) as exc:
    fail("invalid proof bundle: " + str(exc))
with archive:
    members = archive.getmembers()
    for member in members:
        path = pathlib.PurePosixPath(member.name)
        if path.is_absolute() or ".." in path.parts or not member.isfile():
            fail("unsafe proof bundle member: " + member.name)
        if not member.name.startswith("claim/") or member.name.startswith("claim/data/") or member.name.endswith(".html"):
            fail("unexpected table data in proof bundle: " + member.name)
    destination = pathlib.Path(sys.argv[1]).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for member in members:
        output = destination.joinpath(*pathlib.PurePosixPath(member.name).parts)
        output.parent.mkdir(parents=True, exist_ok=True)
        source = archive.extractfile(member)
        if source is None:
            fail("cannot read bundle member: " + member.name)
        with source, output.open("wb") as target:
            target.write(source.read())
print("BUNDLE_INTEGRITY_PASS")
