#!/usr/bin/env python3
"""Standalone checker for A084235(18) = 330055906058 (least k >= 1 with |M(k)| = 2^18), written from the definition.

Definitions (OEIS A008683, A002321, A084235):
  mu(n) = 0 if p^2 | n for some prime p, else (-1)^(number of prime factors of n);  M(x) = sum_{n<=x} mu(n);
  A084235(n) = least k with |M(k)| = 2^n.

Run from the package folder:  python3 verify-it-yourself/check.py          (quick tier, about a minute)
                               FULL=1 python3 verify-it-yourself/check.py   (full tier: every block from k = 1)
Needs Python 3 (standard library only) and a C compiler (cc, gcc or clang; OpenMP used if available).

Quick tier:
  A. Python brute force from the definition (trial division) agrees with the C sieve on mu(1..20000) and on the
     200 integers ending at the claimed k; a pure-Python sieve reproduces the published a(0..9).
  B. The certificate (run-1 block table: per 1e8 block the sum and the max/min prefix) is complete for blocks
     0..3399; chaining it reproduces M(10^8), M(10^9), M(10^10), M(10^11) and locates the first block reaching
     2^n for n = 14..18.
  C. The C sieve recomputes, from the definition, the anchor blocks, the first-hit blocks for n = 14..18, the
     block before the claimed hit and 12 random blocks, and must match the certificate exactly; exact scans from
     the certificate's M(lo-1) reproduce the published a(14..17) and the object's k and M(k).
  The quick tier trusts the certificate for blocks it does not recompute (a spot check, not a proof of "least").
Full tier (FULL=1): recomputes every block 0..3300 (k = 1 .. 330100000000) and compares all of them; with C this
  is complete and does not trust the certificate.
Last output line: PASS or FAIL.
"""
import os, random, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
B = 100_000_000
# Published values (OEIS A084235 b-file, a(0..17); OEIS A084237 b-file, M(10^8..10^11)); see the-record-we-beat/.
KNOWN_A = [1, 5, 31, 199, 1637, 8507, 24110, 95961, 355541, 1786062, 6473791, 30649362, 109851909, 456774199,
           2589994747, 7613644886, 37725066313, 108500046711]
KNOWN_M = {10**8: 1928, 10**9: -222, 10**10: -33722, 10**11: -87856}
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def mu_brute(n):
    if n == 1:
        return 1
    s, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            s = -s
        p += 1 if p == 2 else 2
    return -s if n > 1 else s


def compile_c(tmp):
    cc = next((c for c in ("cc", "gcc", "clang") if shutil.which(c)), None)
    if not cc:
        print("no C compiler (cc, gcc or clang) found")
        return None
    exe = os.path.join(tmp, "mu_check")
    src = os.path.join(HERE, "mu_check.c")
    for flags in (["-O2", "-fopenmp"], ["-O2"]):
        r = subprocess.run([cc] + flags + ["-o", exe, src], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if r.returncode == 0:
            print("compiled mu_check.c with %s %s" % (cc, " ".join(flags)))
            return exe
    print(r.stdout.decode(errors="replace"))
    return None


def run(exe, *args):
    r = subprocess.run([exe] + [str(a) for a in args], stdout=subprocess.PIPE, check=True)
    return r.stdout.decode()


def blocks(exe, idx):
    out = {}
    idx = sorted(set(idx))
    # contiguous runs, so OpenMP can parallelise inside one call
    runs, start, prev = [], None, None
    for b in idx:
        if start is None:
            start = prev = b
        elif b == prev + 1:
            prev = b
        else:
            runs.append((start, prev)); start = prev = b
    if start is not None:
        runs.append((start, prev))
    for a, z in runs:
        for line in run(exe, "blocks", B, a, z + 1).strip().splitlines():
            b, s, mx, mn = map(int, line.split())
            out[b] = (s, mx, mn)
    return out


def main():
    full = os.environ.get("FULL", "") == "1"
    # object
    lines = [l.split() for l in open(os.path.join(PKG, "object", "a18.txt")).read().splitlines() if l.strip()]
    try:
        n_obj, k_obj, m_obj = (int(x) for x in lines[1])
    except (IndexError, ValueError):
        check(False, "object/a18.txt parses as 'n k M(k)'"); return
    check(n_obj == 18 and abs(m_obj) == 2 ** 18, "object names n = 18 and |M(k)| = 2^18 (n=%d, M=%d)" % (n_obj, m_obj))

    tmp = tempfile.mkdtemp(prefix="a084235_")
    try:
        exe = compile_c(tmp)
        check(exe is not None, "C checker compiled")
        if exe is None:
            return
        # A. brute force vs C, and pure-Python small terms
        cmu = [int(x) for x in run(exe, "range", 1, 20000).split()]
        check(cmu == [mu_brute(i) for i in range(1, 20001)], "C mu(1..20000) equals trial-division mu")
        lo = k_obj - 199
        cmu = [int(x) for x in run(exe, "range", lo, k_obj).split()]
        check(cmu == [mu_brute(i) for i in range(lo, k_obj + 1)], "C mu(k-199..k) equals trial-division mu near the claimed k")
        N = 2_000_000
        mu = [1] * (N + 1)
        isp = bytearray([1]) * (N + 1)
        for p in range(2, N + 1):
            if isp[p]:
                isp[p * p::p] = bytearray(len(range(p * p, N + 1, p)))
                for j in range(p, N + 1, p):
                    mu[j] = -mu[j]
                for j in range(p * p, N + 1, p * p):
                    mu[j] = 0
        firsts, M = {}, 0
        for x in range(1, N + 1):
            M += mu[x]
            a = abs(M)
            if a and a & (a - 1) == 0:
                e = a.bit_length() - 1
                firsts.setdefault(e, x)
        check([firsts.get(e) for e in range(10)] == KNOWN_A[:10], "pure-Python sieve reproduces a(0..9)")

        # B. certificate
        cert = {}
        for line in open(os.path.join(HERE, "certificate_blocks.txt")):
            b, s, mx, mn = map(int, line.split())
            cert[b] = (s, mx, mn)
        check(sorted(cert) == list(range(3400)), "certificate has every block 0..3399 exactly once")
        Mb = [0]
        for b in range(3400):
            Mb.append(Mb[-1] + cert[b][0])          # Mb[b] = M(b*B)
        for x, v in KNOWN_M.items():
            check(Mb[x // B] == v, "certificate chain gives M(%d) = %d (published %d)" % (x, Mb[x // B], v))
        first_block = {}
        for e in range(14, 19):
            T = 2 ** e
            first_block[e] = next((b for b in range(3400) if Mb[b] + cert[b][1] >= T or Mb[b] + cert[b][2] <= -T), None)
        check(first_block[18] is not None and first_block[18] == (k_obj - 1) // B, "first certificate block reaching 2^18 is the block holding k (%s)" % first_block[18])

        # C. recompute blocks from the definition
        if full:
            idx = list(range(0, 3301))
            print("FULL tier: recomputing all %d blocks from k = 1 (about 2 CPU-hours single-threaded)" % len(idx))
        else:
            rng = random.SystemRandom()
            extra = rng.sample(range(0, 3300), 12)
            idx = [0, 9, 99, 999] + [first_block[e] for e in range(14, 19)] + [3299] + extra
            print("quick tier: recomputing blocks %s" % sorted(set(idx)))
        got = blocks(exe, idx)
        bad = []
        for b in sorted(set(idx)):
            s, mx, mn = got[b]
            cs, cmx, cmn = cert[b]
            # the certificate's max/min may include the empty prefix 0; normalise both sides the same way
            if s != cs or max(mx, 0) != max(cmx, 0) or min(mn, 0) != min(cmn, 0):
                bad.append(b)
        check(not bad, "recomputed blocks match the certificate (%d blocks; mismatches: %s)" % (len(set(idx)), bad[:5]))
        if full:
            # rebuild the chain from the recomputed blocks only (no trust in the certificate)
            Mr = [0]
            for b in range(3301):
                Mr.append(Mr[-1] + got[b][0])
            for x, v in KNOWN_M.items():
                check(Mr[x // B] == v, "recomputed chain gives M(%d) = %d (published %d)" % (x, Mr[x // B], v))
            T = 2 ** 18
            fb = next((b for b in range(3301) if Mr[b] + got[b][1] >= T or Mr[b] + got[b][2] <= -T), None)
            check(fb == (k_obj - 1) // B, "recomputed: no block before %s reaches |M| = 2^18 (k = 1 .. %d covered)" % (fb, (fb or 0) * B))
            check(Mr[fb] == Mb[fb] if fb is not None else False, "recomputed M(%d) equals the certificate's" % ((fb or 0) * B))
        # exact scans
        for e in range(14, 19):
            b = first_block[e]
            out = run(exe, "scan", b * B + 1, (b + 1) * B, Mb[b], 2 ** e).strip()
            m = re.match(r"first k=(\d+) M=(-?\d+)", out)
            if e < 18:
                check(bool(m) and int(m.group(1)) == KNOWN_A[e], "scan reproduces published a(%d) = %d (%s)" % (e, KNOWN_A[e], out))
            else:
                check(bool(m) and int(m.group(1)) == k_obj and int(m.group(2)) == m_obj,
                      "scan of block %d gives the object's k = %d, M = %d (%s)" % (b, k_obj, m_obj, out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:  # any crash is a failure
        fails.append(repr(ex))
        print("error: %r" % ex)
    print("FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)
