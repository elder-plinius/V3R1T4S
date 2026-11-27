"""Pack the Monte Carlo files into .tar.xz archives (added 2026-10-26, so that the package fits in one pull request).

Deterministic: members sorted, stored as mc/<dataset>/<file>, ustar format, mtime 0, mode 0644, uid/gid 0, xz preset
9e. No file is changed: the archives hold the original bytes, and unpack_mc.py (verify-it-yourself/) restores the
original layout.
  object/mc/<dataset>/*            -> object/mc/<dataset>_<L1>x<L2>.tar.xz, one archive per dataset and torus size
  how-we-built-it/timeline-aligner/mc/<dataset>/*  -> how-we-built-it/timeline-aligner/mc/<dataset>.tar.xz
Each folder gets ARCHIVES.sha256 (the archives) and FILES.sha256 (every packed file); the per-file sha256 of the
object's histograms are also in object/threshold_23_site.json.

usage: python how-we-built-it/pack_mc.py      (from the package folder, before the unpacked folders are removed)
"""
import hashlib
import io
import lzma
import os
import re
import sys
import tarfile


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_archive(path, members):
    """members: list of (name, bytes)."""
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.USTAR_FORMAT) as t:
        for name, data in sorted(members):
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime, ti.mode, ti.uid, ti.gid, ti.uname, ti.gname = len(data), 0, 0o644, 0, 0, "", ""
            t.addfile(ti, io.BytesIO(data))
    blob = lzma.compress(raw.getvalue(), format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=9 | lzma.PRESET_EXTREME)
    with open(path, "wb") as f:
        f.write(blob)
    return blob


def pack(mc, group_by_size):
    arch, files = [], []
    for ds in sorted(d for d in os.listdir(mc) if os.path.isdir(os.path.join(mc, d))):
        groups = {}
        for n in sorted(os.listdir(os.path.join(mc, ds))):
            data = open(os.path.join(mc, ds, n), "rb").read()
            key = ds
            if group_by_size:
                key = "%s_%s" % (ds, re.search(r"_(L\d+x\d+)_", n).group(1))
            groups.setdefault(key, []).append(("mc/%s/%s" % (ds, n), data))
            files.append((sha(data), "%s/%s" % (ds, n)))
        for key, members in sorted(groups.items()):
            blob = write_archive(os.path.join(mc, key + ".tar.xz"), members)
            arch.append((sha(blob), key + ".tar.xz"))
            print("%-48s %4d files %8d bytes" % (os.path.join(mc, key + ".tar.xz"), len(members), len(blob)))
            if len(blob) > 1000000:
                sys.exit("archive over 1 MB: " + key)
    for fname, rows in (("ARCHIVES.sha256", arch), ("FILES.sha256", files)):
        with open(os.path.join(mc, fname), "w", newline="\n") as f:
            f.writelines("%s  %s\n" % r for r in sorted(rows, key=lambda r: r[1]))


if __name__ == "__main__":
    pack(os.path.join("object", "mc"), True)
    pack(os.path.join("how-we-built-it", "timeline-aligner", "mc"), False)
