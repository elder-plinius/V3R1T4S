#!/usr/bin/env python3
"""Build the claim for one length L: per-claim run folder runs/<RUN>-L<L>/ (kit layout) and the isolated panel copy
panel-claim-L<L>/. Usage: make_claim.py WORKDIR RUN L"""
import sys, os, re, csv, shutil, hashlib, subprocess, html
from pathlib import Path
import numpy as np

W, RUN, L = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
sys.path.insert(0, str(W / "tools"))
from labs_energy import energy, to_pm

main = W / "runs" / RUN
rows = list(csv.DictReader(open(W / "baseline/rows.tsv"), delimiter="\t"))
def ok_parent(r):
    """Verified rows, plus printed sequences whose decode is plausible but whose printed F is inconsistent
    (kind hex-full?, energy within 0.5% of the energy implied by the printed F: a typo in F, not a bad decode)."""
    if not r["seq"]: return False
    if "?" not in r["kind"]: return True
    return r["kind"] == "hex-full?" and bool(r["implied"]) and abs(int(r["E"]) - int(r["implied"])) <= 0.005 * int(r["implied"])

fetch = [l.split() for l in open(main / "data/fetchlog.txt") if l.strip()]
def fetched(url_part):
    hits = [f for f in fetch if url_part in f[-1]]
    return (hits[-1][0], hits[-1][1], hits[-1][-1]) if hits else ("", "", "")
SRC_URL = {"knauer2004": "results-2016/2004-Knauer-original.html"}
def src_key(s): return s.split("-prev")[0].split("-old")[0].split("-repaired")[0]
def src_fetch(s):
    k = src_key(s)
    return fetched(SRC_URL.get(k, "arxiv.org/src/" + k))

E_np = lambda s: int(sum(int(c) ** 2 for c in np.correlate(np.array(s, dtype=np.int64), np.array(s, dtype=np.int64), "full")[len(s):]))

# baseline for L (same rule as PREREG)
base_rows = [r for r in rows if int(r["L"]) == L]
vals = [int(r["implied"]) for r in base_rows if r["implied"]] + [int(r["E"]) for r in base_rows if r["E"]]
assert vals, "no published value for L"
baseE = min(vals)

# candidate objects: refined outputs and one-element edits of published L-1 / L+1 sequences
KT, KA = 8, 3   # end operators: trim up to KT elements in total, or append up to KA elements in total
def edits(s):
    """(object, description, operation_code) for k-element end operators; 0 means +1, 1 means -1."""
    import itertools
    out = []
    n = len(s)
    if 1 <= L - n <= KA:
        k = L - n
        for bits in itertools.product("01", repeat=k):
            b = "".join(bits)
            for i in range(k + 1):
                a, z = b[:i], b[i:]
                out.append((a + s + z, f"prepend '{a}' and append '{z}' (0 = +1, 1 = -1)", f"prefix={a or '-'} suffix={z or '-'} trim_start=0 trim_end=0"))
    if 1 <= n - L <= KT:
        k = n - L
        for i in range(k + 1):
            out.append((s[i:n - (k - i)], f"remove {i} element(s) at the start and {k - i} at the end", f"prefix=- suffix=- trim_start={i} trim_end={k - i}"))
    return out
cands = []
for r in rows:
    if int(r["L"]) != L and L - KA <= int(r["L"]) <= L + KT and ok_parent(r):
        for e, how, code in edits(r["seq"]):
            kind = {1: "one", 2: "two"}.get(abs(int(r["L"]) - L), str(abs(int(r["L"]) - L)))
            cands.append((energy(to_pm(e)), e, f"{kind}-element edit ({how}) of the published L={r['L']} sequence from {r['src']}", dict(r, opcode=code)))
refined = []
for p in sorted(set(W.glob(f"jobs/*/out/L{L}.best")) | set(W.glob(f"jobs/*/out/L{L}.*.best"))):
    E, s = open(p).read().split()
    refined.append((int(E), s, f"refined by seeded memetic tabu search ({p.parent.parent.name})", None))
allc = sorted(cands + refined, key=lambda c: (c[0], c[3] is None))
best = allc[0]
E1, seq, how, parent = best
if parent is None:   # refined: name the seed it started from
    how += "; seeds were the one-element edits listed in parent.txt"
pm = to_pm(seq); E2 = E_np(pm)
assert len(seq) == L and E1 == energy(pm) == E2, "energy mismatch"
assert E1 < baseE, f"no claim: E={E1} baseline={baseE}"
print(f"L={L} E={E1} (numpy {E2}) baseline={baseE} gap={baseE - E1} via: {how}")

# per-claim run folder
cr = W / "runs" / f"{RUN}-L{L}"
for d in ("data", "attempts/object-as-data/code", "attempts/object-as-data/result",
          "attempts/evaluator-first-local-search/code", "claim", "panel"):
    (cr / d).mkdir(parents=True, exist_ok=True)
for f in ("target.md", "scout.md", "BRIEF.md", "PREREG.md"):
    shutil.copy2(main / f, cr / f)
shutil.copy2(main / "data/status_2607.09688_abs.html", cr / "data/status_2607.09688_abs.html")
shutil.copy2(main / "data/fetchlog.txt", cr / "data/fetchlog.txt")
with open(cr / "target.md", "a") as f:
    f.write(f"\nThis run folder holds the claim for the single length L={L} (one table cell per claim); the search that\n"
            f"produced it is in runs/{RUN}/.\n")

# source excerpts (exact lines from each source mentioning L)
src_files = {"2206.12070": "2206.12070/bare_jrnl.tex", "2011.00068": "2011.00068/tb_best201-303--PSL.tex",
             "2210.15962": "2210.15962/paper.tex", "2409.07222": "2409.07222/table.tex",
             "2607.09688": "2607.09688/TAB_RECORDS.tex", "2504.00987": "2504.00987/main.tex",
             "1406.5301": "1406.5301/Tables/tb_new_records.tex", "1512.02475": "1512.02475/labs-15.tex"}
ex = []
for M in range(L - KA, L + KT + 1):
    for k, rp in src_files.items():
        t = (W / "big/src" / rp).read_text(errors="replace").splitlines()
        for i, line in enumerate(t):
            if re.match(rf"^\s*\$?{M}\$?\s*&", line):
                ex.append(f"[{k} {rp} line {i + 1}] " + line.strip())
                if i + 1 < len(t) and not re.match(r"^\s*\$?\d", t[i + 1]): ex.append("    " + t[i + 1].strip())
    dt = (W / "big/src/2106.03377/bare_jrnl.tex").read_text(errors="replace").splitlines()
    for i, line in enumerate(dt):
        if re.match(rf"^{M} &\s*$", line):
            ex.append(f"[2106.03377 2106.03377/bare_jrnl.tex lines {i + 1}-{i + 5}] " + " ".join(x.strip() for x in dt[i:i + 5]))
    kt = html.unescape(re.sub(r"<[^>]*>", " ", (main / "data/git_labs/2004-Knauer-original.html").read_text(errors="replace")))
    m = re.search(rf"^\s*{M}\*?\s+\d+\s+\d+\.\d+[^\n]*", kt, re.M)
    if m: ex.append(f"[knauer2004 git_labs results-2016/2004-Knauer-original.html] " + " ".join(m.group(0).split())[:400])

claim = cr / "claim"
(claim / "sequence.txt").write_text(seq + "\n")
shutil.copy(W / "tools/labs_energy.py", claim / "check_energy.py")
with open(claim / "baseline.tsv", "w") as f:
    f.write("source\tL\tprinted_E\tprinted_F\tsmallest_E_consistent_with_printed_value\tE_of_printed_sequence\tdecoding\tsource_url\tfetched_utc\thttp\n")
    for r in base_rows:
        t, code, url = src_fetch(r["src"])
        f.write(f"{r['src']}\t{L}\t{r['pE']}\t{r['pF']}\t{r['implied']}\t{r['E']}\t{r['kind'] or 'no sequence printed'}\t{url}\t{t}\t{code}\n")
(claim / "source_excerpts.txt").write_text(
    "Exact lines for lengths L-3..L+8 from the fetched sources (arXiv TeX sources from https://arxiv.org/src/<id>;\n"
    "Knauer's table from the git_labs copy). Data only.\n\n" + "\n".join(ex) + "\n")
par = ""
if parent is not None:
    t, code, url = src_fetch(parent["src"])
    par = (f"parent_source: {parent['src']} (L={parent['L']}, printed E {parent['pE'] or '-'}, printed F {parent['pF'] or '-'}, "
           f"recomputed E {parent['E']})\n" + f"operation_code: {parent['opcode']}\n" + (f"note: the printed merit factor of this row ({parent['pF']}) is inconsistent with its printed sequence (E={parent['E']}, F={int(parent['L']) ** 2 / (2 * int(parent['E'])):.4f}); the sequence as printed is used as the parent\n" if "?" in parent["kind"] else "") + ("repair: the printed hex for this row does not reproduce the printed F; the parent_sequence is the unique one-hex-digit insertion/deletion of the printed hex whose exact energy reproduces the printed F (tools/repair_dimitrov.py)\n" if parent["kind"] == "hex-repaired" else "") + f"parent_url: {url} (fetched {t}, HTTP {code})\nparent_sequence: {parent['seq']}\n"
           f"operation: {how}\n")
else:
    seeds = [c for c in cands][:3]
    par = "refined object; the seeds were one-element edits such as:\n" + "".join(
        f"- E={c[0]} {c[2]}\n  {c[1]}\n" for c in sorted(cands)[:3])
(claim / "parent.txt").write_text(par)
cover = {}
for r in rows: cover.setdefault(src_key(r["src"]), set()).add(int(r["L"]))
lines = ["# Sources checked for L = %d\n" % L, "| source | url | fetched (UTC) | HTTP | lengths it tabulates | row for L? |", "|---|---|---|---|---|---|"]
for k in sorted(cover):
    tt, code, url = src_fetch(k); Ls = sorted(cover[k])
    lines.append(f"| {k} | {url} | {tt} | {code} | {len(Ls)} lengths in {Ls[0]}..{Ls[-1]} | {'yes' if L in cover[k] else 'no'} |")
lines += ["", "Not readable in this run (PENDING SOURCE CHECK): the git_labs tree listing (github.com 403 from the session proxy),",
          "git_labs results-2016/Merit_Factor_Records-2013-even.html and -odd.html (404 at the paths linked from the Knauer page),",
          "Mertens' open.dat (DNS failure), labraj.feri.um.si (proxy 403), the arXiv API listing (export.arxiv.org 429),",
          "journal-only versions (IEEE Access 2018, MENDEL 2022, Digital Signal Processing 2025, J. Comput. Sci. 2024; hosts unreachable).",
          "arxiv.org itself answered 429 to a search page at about 17:11:35Z; under the human's host rule arxiv.org was not used",
          "again in this run (the TeX sources above were fetched before that). github.com answered 403 at preflight and was not used again.",
          "",
          "Statements in the read sources about what was published before them (quoted from the TeX sources fetched above):",
          "- arXiv:2607.09688 (June 2026): \"Local search methods in [boskovic17, dimitrov22] have produced sequences with a merit",
          "  factor exceeding 8.0 for 172 <= L <= 268, and exceeding 7.0 for 172 <= L <= 527.\" Its own table covers 450..527 and 573.",
          "- arXiv:2206.12070 (Dimitrov et al.): \"we were able to improve all the results, for all skew-symmetric lengths in the",
          "  range 225-451, announced in literature and reached by using a supercomputer grid.\"",
          "- arXiv:2210.15962: its solver \"found all the known and seven new best-known skew-symmetric sequences for odd instances",
          "  from L=121 to L=223\" and was run up to L=247 (comparing against Knauer04, Boskovic17, Brest22)."] + (["", "Known unread table for this length: arXiv:2011.00068 v1 (November 2020) reportedly tabulated odd lengths 301..401",
           "with F > 7 (reported by a web search summary during this run); only the current version (201..303) was read.",
           "Dimitrov's 2022 statement above (all skew-symmetric lengths 225-451 improved over the literature) postdates v1."] if (L % 2 == 1 and 301 <= L <= 401) else [])
(claim_dir := cr / "claim").mkdir(parents=True, exist_ok=True)
(claim_dir / "sources_checked.md").write_text("\n".join(lines) + "\n")
st = "https://arxiv.org/abs/2607.09688"
(claim / "CLAIM.md").write_text(f"""# Claim: labs-merit-factor-records, L = {L}

claim: The +-1 sequence of length {L} in sequence.txt has aperiodic energy E = {E1}, strictly below {baseE}, the lowest
energy published for length {L} in the sources listed in baseline.tsv.

target_id: labs-merit-factor-records
status_source: {st}

criterion (verbatim from the bank): {open(main / 'target.md').read().split('## Success criterion (verbatim from bank/targets.json)')[1].split('## Partial wins')[0].strip()}

Definitions: s_i in {{+1,-1}}, C_k = sum_{{i=0}}^{{L-1-k}} s_i s_{{i+k}}, E = sum_{{k=1}}^{{L-1}} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1 (E is invariant under global negation).

Object: sequence.txt (one line, {L} characters). Claimed E = {E1} (F = {L * L}/{2 * E1}).
How it was made: {how}. Details of the parent object in parent.txt.
Baseline: baseline.tsv lists every published row for L = {L} found in the sources read; baseline_E = {baseE}
(minimum over printed energies, the smallest integer energy consistent with each printed merit factor, and the
recomputed energy of each printed sequence). sources_checked.md lists every source read (with or without a row
for L) and the sources that could not be read. source_excerpts.txt quotes the exact source lines for L-3..L+8.
""")
(claim / "REPRODUCE.md").write_text(f"""# Reproduce (from inside this folder, Python 3 standard library only)

    python3 check_energy.py "$(cat sequence.txt)"

Expected output: `{L} {E1}` (length, exact energy). Then compare {E1} with the baseline column values in baseline.tsv
(minimum {baseE}). To check the parent: `python3 check_energy.py <parent_sequence from parent.txt>` and apply the
operation stated in parent.txt.
""")
shutil.copytree(claim, W / f"panel-claim-L{L}", dirs_exist_ok=True)

# attempts for this claim
a = cr / "attempts/object-as-data"
shutil.copy2(W / "tools/labs_energy.py", a / "code/labs_energy.py")
shutil.copy2(W / "tools/make_claim.py", a / "code/make_claim.py")
(a / "result/sequence.txt").write_text(seq + "\n")
(a / "output.txt").write_text("".join(f"E={c[0]} {c[2]}\n" for c in sorted(cands)[:40]) +
                              f"\nnumpy second implementation: E={E2}\nbaseline_E={baseE}\n")
(a / "NOTES.md").write_text((main / "attempts/object-as-data/NOTES.md").read_text() if (main / "attempts/object-as-data/NOTES.md").exists() else "see main run\n")
(a / "REPRODUCE.md").write_text(f"    python3 code/labs_energy.py \"$(cat result/sequence.txt)\"   # expect: {L} {E1}\n")
(a / "report.md").write_text(f"""claim level: solution_claim

L={L}: {how}. E = {E1} by the exact checker and by numpy (E={E2}); baseline_E = {baseE} from the sources in
claim/baseline.tsv. Labels: energy PROVED-HERE (exact integer computation); baseline completeness NUMERICAL/KNOWN
(minimum over the sources read; unread sources listed in scout.md).
""")
b = cr / "attempts/evaluator-first-local-search"
shutil.copy2(W / "tools/labs_ma.c", b / "code/labs_ma.c")
logs = []
for p in sorted(W.glob(f"jobs/*/out/L{L}.*")):
    if p.suffix in (".ckpt", ".best"): logs.append(f"{p.parent.parent.name}/{p.name}: {p.read_text().strip()[:120]}")
(b / "output.txt").write_text("\n".join(logs) + "\n")
(b / "NOTES.md").write_text((main / "attempts/evaluator-first-local-search/NOTES.md").read_text() if (main / "attempts/evaluator-first-local-search/NOTES.md").exists() else "see main run\n")
if parent is None:
    (b / "result").mkdir(exist_ok=True); (b / "result/sequence.txt").write_text(seq + "\n")
    (b / "REPRODUCE.md").write_text(f"    python3 ../object-as-data/code/labs_energy.py \"$(cat result/sequence.txt)\"   # expect: {L} {E1}\n")
    (b / "report.md").write_text(f"claim level: solution_claim\n\nL={L}: the seeded search improved the best one-element edit "
                                 f"(E={sorted(cands)[0][0]}) to E={E1}; logs in output.txt.\n")
else:
    (b / "report.md").write_text(f"""claim level: negative

L={L}: seeded memetic tabu search and iterated tabu search started from the one-element edits did not go below the
best edit (E={E1}); the claim object therefore comes from the object-as-data lens. Logs: output.txt.

dead lines:
- Seeded memetic tabu search (labs_ma, population of seeds plus mutated copies and random sequences) from the best edits: no energy below E={E1} in the runs logged in output.txt; the edit sits in a deep local minimum.
- Iterated tabu search around the best edit (kicks of 1-16 flips, walks of 2-4x the usual length): no improvement in the runs logged; same basin.
- Cold-start memetic tabu search (calibration at L=176/230/274, 540 s each): far above the published values (e.g. L=274 reached 6889 versus 5225 published), so cold search is not competitive at these lengths within this budget.
""")
print("built", cr, "and", W / f"panel-claim-L{L}")
