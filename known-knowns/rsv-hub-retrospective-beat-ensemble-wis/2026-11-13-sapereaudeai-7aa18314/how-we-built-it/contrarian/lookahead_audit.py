"""Look-ahead audit (bank verification method): rerun the frozen pipeline for an origin O against a TRUNCATED archive that
holds only vintages dated <= O, each cut to rows with date <= O - 8 days, in a fresh parse cache, and compare the output
file byte for byte with the frozen run's file. usage: python lookahead_audit.py <origin> [<origin> ...]
Writes one line per origin to attempts/contrarian/out/lookahead_audit.txt."""
import os, sys, glob, shutil, subprocess, datetime as dt, hashlib
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ARCH = os.path.join(RUN, "data", "hopkins", "hub", "target-data", "archive")
FC = os.path.join(RUN, "attempts", "forecaster")
WORK = os.path.join(RUN, "attempts", "contrarian", "work", "audit")
OUT = os.path.join(RUN, "attempts", "contrarian", "out", "lookahead_audit.txt")
PY = sys.executable


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def audit(O):
    lim = (dt.date.fromisoformat(O) - dt.timedelta(days=8)).isoformat()
    base = os.path.join(WORK, O)
    shutil.rmtree(base, ignore_errors=True)
    arch = os.path.join(base, "archive"); cache = os.path.join(base, "cache"); out = os.path.join(base, "fc")
    os.makedirs(arch); os.makedirs(cache)
    kept = cut = 0
    for f in sorted(glob.glob(os.path.join(ARCH, "*_rsvnet_hospitalization.csv"))):
        lab = os.path.basename(f)[:10]
        if lab > O:
            continue
        t = pd.read_csv(f, dtype=str, keep_default_na=False)
        if (t.date > lim).any():
            t[t.date <= lim].to_csv(os.path.join(arch, os.path.basename(f)), index=False)
            cut += 1
        else:
            shutil.copyfile(f, os.path.join(arch, os.path.basename(f)))
        kept += 1
    env = dict(os.environ, RSV_ARCH=arch, RSV_CACHE=cache)
    p = subprocess.run([PY, "-W", "ignore", os.path.join(FC, "code", "run_season.py"), os.path.join(FC, "FROZEN_PARAMS.json"),
                        out, "2024-25", O], env=env, capture_output=True, text=True, cwd=RUN)
    mine = os.path.join(out, "%s-V3R1T4S-asofKA.csv" % O)
    ref = os.path.join(FC, "result", "forecasts", "%s-V3R1T4S-asofKA.csv" % O)
    same = os.path.exists(mine) and sha(mine) == sha(ref)
    line = "%s vintages_kept %d truncated %d identical %s %s" % (O, kept, cut, same, (p.stdout.strip().splitlines() or [""])[-1])
    if p.returncode:
        line += " ERROR " + p.stderr[-300:].replace("\n", " | ")
    with open(OUT, "a") as fh:
        fh.write(line + "\n")
    shutil.rmtree(base, ignore_errors=True)
    print(line, flush=True)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    for O in sys.argv[1:]:
        audit(O)
