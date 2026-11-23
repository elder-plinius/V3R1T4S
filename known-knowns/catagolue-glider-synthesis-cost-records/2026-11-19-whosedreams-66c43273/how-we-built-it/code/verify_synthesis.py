#!/usr/bin/env python3
"""Strict glider-synthesis verifier (bank: catagolue-glider-synthesis-cost-records)."""
from __future__ import annotations
import argparse, json, re, sys, time, urllib.request
from pathlib import Path

GLIDER_APG = "xq4_153"

def fetch_csynth(apgcode: str, retries=5) -> tuple[int|None, bool, str]:
    """Returns (cost, is_pseudo, raw_snippet_or_error)."""
    url = f"https://catagolue.hatsya.com/object/{apgcode}/b3s23"
    last = ""
    for i in range(retries):
        try:
            html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "replace")
            m = re.search(
                rf"#CSYNTH\s+{re.escape(apgcode)}\s+costs\s+(\d+)\s+gliders(\s*\(pseudo\))?",
                html,
            )
            if m:
                return int(m.group(1)), bool(m.group(2)), m.group(0)
            return None, False, html[:300]
        except Exception as e:
            last = str(e)
            time.sleep(1.5 * (i + 1))
    return None, False, last

def verify_pattern(lt, gset_mod, rewind_check, pat, target: str) -> dict:
    out = {"ok": False, "target": target, "errors": [], "structurally_valid": False}
    comps = list(pat.components())
    if not comps:
        out["errors"].append("empty")
        return out
    nong = []
    for i, c in enumerate(comps):
        info = c.oscar(verbose=False, return_apgcode=True, maxexp=8) or {}
        if info.get("apgcode") != GLIDER_APG:
            nong.append((i, info.get("apgcode"), c.population))
    if nong:
        out["errors"].append(f"non-glider gen0 components: {nong}")
        return out
    out["n_gliders"] = len(comps)
    gs = gset_mod.extract(pat)
    base = pat - gs.s
    if base.population != 0:
        out["errors"].append(f"residual non-glider cells after gset extract: pop={base.population}")
        return out
    if not rewind_check(base, gs):
        out["errors"].append("rewind_check failed (gliders interact when rewound)")
        return out
    # diameter-based minimum rewind already covered by rewind_check's expo loop;
    # additionally require at least 4*diam conceptually satisfied by infinite rewind.
    out["rewind_ok"] = True
    # Evolve to periodic
    rect = pat.getrect() or (0, 0, 1, 1)
    diam = max(rect[2], rect[3])
    advanced = pat[max(512, diam * 16)]
    info = advanced.oscar(verbose=False, return_apgcode=True, maxexp=18)
    if not info:
        out["errors"].append("not periodic")
        return out
    out["final_apgcode"] = info["apgcode"]
    out["period"] = info.get("period")
    if info["apgcode"] != target:
        out["errors"].append(f"got {info['apgcode']} != {target}")
        return out
    out["structurally_valid"] = True
    live, pseudo, snip = fetch_csynth(target)
    out["live_csynth"] = live
    out["live_pseudo"] = pseudo
    out["csynth_snippet"] = snip
    if live is None:
        out["errors"].append(f"live #CSYNTH fetch failed: {snip[:160]}")
        return out
    if out["n_gliders"] < live:
        out["ok"] = True
        out["improvement"] = live - out["n_gliders"]
    else:
        out["errors"].append(f"cost {out['n_gliders']} not < live {live}")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rle")
    ap.add_argument("--target")
    ap.add_argument("--shinjuku-apgcode", help="build continuous-ish synth via Shinjuku and verify")
    ap.add_argument("--component", help="verify a single Shinjuku component line as a converter (not full synth)")
    ap.add_argument("--out", default="-")
    args = ap.parse_args()

    shinjuku = Path(__file__).resolve().parents[1] / "data" / "Shinjuku"
    sys.path.insert(0, str(shinjuku))
    from shinjuku import lt
    from shinjuku.gliderset import gset
    from shinjuku.checks import rewind_check
    from shinjuku.transcode import realise_comp, decode_comp

    if args.component:
        inp, cost, outp = decode_comp(args.component)
        base, gs = realise_comp(args.component, separate=True)
        ok = rewind_check(base, gs)
        combined = realise_comp(args.component, separate=False)
        info = combined.oscar(verbose=False, return_apgcode=True, maxexp=16) or {}
        result = {
            "kind": "component",
            "input": inp,
            "output": outp,
            "cost": cost,
            "rewind_ok": ok,
            "result_apgcode": info.get("apgcode"),
            "match_output": info.get("apgcode") == outp,
        }
    elif args.shinjuku_apgcode:
        from shinjuku.search import dijkstra, lookup_synth
        paths = dijkstra()
        got = lookup_synth(paths, args.shinjuku_apgcode, orien_lock=True, gnf=True)
        if not got:
            result = {"ok": False, "errors": ["no path"]}
        else:
            cost, pat = got
            # Note: multi-stage stitch is a strip of stages, NOT one continuous collision.
            # Only single-stage (pure glider) patterns are claimed as full syntheses here.
            result = verify_pattern(lt, gset, rewind_check, pat, args.shinjuku_apgcode)
            result["shinjuku_cost"] = int(cost)
            result["rle"] = pat.rle_string()
            result["note"] = (
                "Shinjuku slock/gnf may produce a staged strip; "
                "only patterns that are pure gliders at gen0 pass."
            )
    else:
        rle = Path(args.rle).read_text() if Path(args.rle).exists() else args.rle
        pat = lt.pattern(rle)
        result = verify_pattern(lt, gset, rewind_check, pat, args.target)
        result["rle"] = rle

    text = json.dumps(result, indent=2)
    if args.out != "-":
        Path(args.out).write_text(text)
    print(text)

if __name__ == "__main__":
    main()
