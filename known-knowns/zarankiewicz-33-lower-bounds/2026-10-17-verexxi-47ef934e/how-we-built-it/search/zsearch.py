"""Long-running rip-up-and-repair local search for z(m,n;3,3) (no all-ones 3x3 submatrix).
usage: python zsearch.py M N TARGET MINUTES SEED OUTDIR [SEED_MATRIX_FILE]
Saves every matrix with at least TARGET ones (and each new best) to OUTDIR as z_MxN_ONES_seedS.txt and prints one line
per new best. Restarts from a fresh greedy fill (or the seed matrix) after a long stall."""
import os, random, sys, time

m, n, target, minutes, seed, outdir = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
seedfile = sys.argv[7] if len(sys.argv) > 7 else None
os.makedirs(outdir, exist_ok=True)
rng = random.Random(seed)


def can_set(rows, r, c):
    mask_r = rows[r]
    others = [rows[i] for i in range(m) if i != r and (rows[i] >> c) & 1]
    for x in range(len(others)):
        a = others[x] & mask_r
        if (a & ~(1 << c)).bit_count() < 2:
            continue
        for y in range(x + 1, len(others)):
            if ((a & others[y]) & ~(1 << c)).bit_count() >= 2:
                return False
    return True


def fill(rows):
    zeros = [(r, c) for r in range(m) for c in range(n) if not (rows[r] >> c) & 1]
    rng.shuffle(zeros)
    for r, c in zeros:
        if can_set(rows, r, c):
            rows[r] |= 1 << c


def load(path):
    rows = []
    for line in open(path):
        s = line.strip()
        if s and set(s) <= {"0", "1"}:
            rows.append(int(s[::-1], 2))
    return rows if len(rows) == m and all(r < (1 << n) for r in rows) else None


def start():
    if seedfile and rng.random() < 0.5:
        s = load(seedfile)
        if s:
            fill(s)
            return s
    rows = [0] * m
    fill(rows)
    return rows


def save(rows, ones):
    p = os.path.join(outdir, "z_%dx%d_%d_seed%d.txt" % (m, n, ones, seed))
    with open(p, "w", newline="\n") as f:
        f.write("\n".join("".join(str((rows[r] >> c) & 1) for c in range(n)) for r in range(m)) + "\n")


deadline = time.time() + minutes * 60
best_ones = -1
cur = start(); cur_ones = sum(x.bit_count() for x in cur); stall = 0
while time.time() < deadline:
    new = cur[:]
    ones = [(r, c) for r in range(m) for c in range(n) if (new[r] >> c) & 1]
    k = rng.choice((1, 1, 2, 2, 3, 4, 5, 6))
    for r, c in rng.sample(ones, min(len(ones), k)):
        new[r] &= ~(1 << c)
    fill(new)
    new_ones = sum(x.bit_count() for x in new)
    if new_ones >= cur_ones:
        if new_ones > cur_ones:
            stall = 0
        cur, cur_ones = new, new_ones
        if cur_ones > best_ones:
            best_ones = cur_ones
            print("%s best %d" % (time.strftime("%H:%M:%S"), best_ones), flush=True)
            if best_ones >= target:
                save(cur, best_ones)
    else:
        stall += 1
    if stall > 400000:
        cur = start(); cur_ones = sum(x.bit_count() for x in cur); stall = 0
print("done best %d" % best_ones, flush=True)
