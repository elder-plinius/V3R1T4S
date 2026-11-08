import os, sys, glob, json
import numpy as np
import mpmath as mp

mp.mp.dps = 60

# target energies
rows = {}
for line in open('/inputs/cohn_harmonic.tsv'):
    if line.startswith('#') or line.startswith('N\t') or not line.strip():
        continue
    N, n, te, e2, d, u = line.rstrip('\n').split('\t')
    rows[f"{N}-{n}"] = dict(N=int(N), n=int(n),
                            tgt=min(float(te), float(e2)))


def energy_mp_file(Y, p):
    N, n = Y.shape
    Ym = [[mp.mpf(repr(float(v))) for v in row] for row in Y]
    for i in range(N):
        s = mp.sqrt(sum(v * v for v in Ym[i]))
        Ym[i] = [v / s for v in Ym[i]]
    E = mp.mpf(0)
    for i in range(N):
        for j in range(i + 1, N):
            r2 = sum((Ym[i][k] - Ym[j][k]) ** 2 for k in range(n))
            E += r2 ** (-mp.mpf(p) / 2)
    return E, Ym


def main():
    pub = set(open('/inputs/already_published.txt').read().split())
    outdir = sys.argv[1] if len(sys.argv) > 1 else '/work/cells'
    bestdir = sys.argv[2] if len(sys.argv) > 2 else '/work/best'
    os.makedirs(outdir, exist_ok=True)
    # gather all result npz from all run dirs
    best = {}  # key -> (E, path)
    for f in glob.glob('/work/run*/w*/*.npz') + glob.glob(bestdir + '/*.npz'):
        key = os.path.basename(f)[:-4]
        try:
            z = np.load(f)
            E = float(z['E'])
        except Exception:
            continue
        if key not in best or E < best[key][0]:
            best[key] = (E, f)
    improved = []
    for key, (E, f) in sorted(best.items()):
        if key not in rows or key in pub:
            continue
        r = rows[key]
        thr = max(1e-9, 1e-12 * r['tgt'])
        if r['tgt'] - E > thr:
            improved.append((key, E, f, r['tgt']))
    print(f"{len(improved)} improved rows")
    for key, E, f, tgt in improved:
        z = np.load(f)
        Y = z['Y']
        p = rows[key]['n'] - 2
        Emp, Ym = energy_mp_file(Y, p)
        thr = max(mp.mpf('1e-9'), mp.mpf('1e-12') * mp.mpf(repr(tgt)))
        gain = mp.mpf(repr(tgt)) - Emp
        status = "KEEP" if gain > thr else "DROP"
        print(f"{key}: E={mp.nstr(Emp,20)} tgt={tgt:.10f} gain={mp.nstr(gain,4)} {status}")
        if gain > thr:
            path = os.path.join(outdir, f"{key}.txt")
            # keep only best file per row
            if os.path.exists(path):
                old = open(path).readline()
                # parse old energy
                try:
                    oE = mp.mpf(old.split('energy')[1].strip())
                    if oE <= Emp:
                        print(f"  existing file better ({mp.nstr(oE,20)}), skip")
                        continue
                except Exception:
                    pass
            with open(path, 'w') as fo:
                fo.write(f"# cell {key} energy {mp.nstr(Emp, 45)}\n")
                for row in Ym:
                    fo.write(",".join(mp.nstr(v, 30) for v in row) + "\n")


if __name__ == '__main__':
    main()
