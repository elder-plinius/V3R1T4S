"""Build the outbox package for the confirmed p3 claim (lead agent, after the gate). Usage, from the workspace root:
python3 -I runs/2026-11-18-1925/code/build_package.py <stage-parent-dir>
Prints the submission id. Everything comes from claim/ (frozen), panel/ (as written), lead-agent-checks/ and the
whale package's generic prompt/ files."""
import sys, os, json, csv, hashlib, shutil
from pathlib import Path
RUN = Path(__file__).resolve().parents[1]; WS = RUN.parents[1]; C = RUN / 'claim'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
S = json.loads((C / 'output/summary.json').read_text())
sid = '2026-11-18-orensleepwalker-' + sha(C / 'output/summary.json')[:8]
out = Path(sys.argv[1]) / sid; assert not out.exists(); out.mkdir(parents=True)
cp = lambda a, b: (Path(b).parent.mkdir(parents=True, exist_ok=True), shutil.copy(a, b))

# object/
cp(C / 'output/summary.json', out / 'object/summary.json')
for p in sorted((C / 'output/real').glob('draw_*.json')): cp(p, out / 'object/real-draws' / p.name)
with open(out / 'object/null-rf-controls.jsonl', 'w') as f:
    for p in sorted((C / 'output/null_rf').glob('rerun_*.json')): f.write(p.read_text().strip() + '\n')
SRC = C / 'data/20231225_dfall_obs_data_and_spectral_features_revision1_n469.csv'
rows = [r for r in csv.DictReader(open(SRC, encoding='utf-8-sig')) if r['Cert_ID_Bin'] == '1']
with open(out / 'object/calls.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['soundID', 'CallerID', 'Elicitor1_ID'])
    for r in rows: w.writerow([r['soundID'], r['CallerID'], r['Elicitor1_ID']])
# how-we-built-it/
for n in ('core.py', 'run_real.py', 'null_rf.py', 'null_pa.py', 'context_check.py', 'summarize.py', 'replay.py'):
    cp(C / 'code' / n, out / 'how-we-built-it/code' / n)
cp(RUN / 'code/build_package.py', out / 'how-we-built-it/code/build_package.py')
for n in ('PREREG.md', 'PREREG.sha256', 'null_test.md'): cp(C / n, out / 'how-we-built-it' / n)
cp(C / 'baseline/README.md', out / 'how-we-built-it/baseline/README.md')
for p in sorted((RUN / 'lead-agent-checks').iterdir()): cp(p, out / 'how-we-built-it/lead-agent-checks' / p.name)
for k in ('null_pa', 'context'):
    with open(out / f'how-we-built-it/full-win-attempt-{k}.jsonl', 'w') as f:
        for p in sorted((C / 'output' / k).glob('*.json')): f.write(p.read_text().strip() + '\n')
(out / 'how-we-built-it/requirements.txt').write_text('numpy==2.5.4\npandas==3.1.1\nscikit-learn==1.9.1\n')
# panel/ and prompt/
for n in ('reproduce.md', 'novelty.md', 'criterion.md', 'gate.md'): cp(RUN / 'panel' / n, out / 'panel' / n)
for n in ('RUN_PROMPT.txt', 'charter.md', 'repo-version.md'): cp(WS / 'outbox/2026-11-18-orensleepwalker-ccdbee70/prompt' / n, out / 'prompt' / n)
# verify-it-yourself/
cp(RUN / 'code/package_verify.py', out / 'verify-it-yourself/verify.py')
(out / 'verify-it-yourself/run_checks.sh').write_text(
    "#!/bin/sh\nset -eu\nfailure() { printf '%s\\n' FAIL; exit 1; }\nsha256sum --check --quiet SHA256SUMS || failure\n"
    "PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py . || failure\nprintf '%s\\n' PASS\n")
# the-record-we-beat/
for dd in ('the-record-we-beat', 'verify-it-yourself'): (out / dd).mkdir(parents=True, exist_ok=True)
cit = C / 'data/europepmc-citations.json'
(out / 'the-record-we-beat/snapshot.md').write_text(
    "# What this result is compared against\n\n"
    "Published value: Pardo et al., Nature Ecology and Evolution 8:1353-1364 (2024), https://doi.org/10.1038/s41559-024-02420-w : random forest receiver accuracy 27.5% (spectral features, caller x receiver stratified 7-fold CV), as quoted by the bank entry.\n\n"
    "Status source (the bank's status_source, Europe PMC citations of the paper): https://www.ebi.ac.uk/europepmc/webservices/rest/MED/38858512/citations?format=json&pageSize=100\n"
    f"Fetched 2026-11-18T19:25:40Z, HTTP 200, content type application/json, response sha256 {sha(cit)}; hitCount {json.loads(cit.read_text())['hitCount']}; no citing paper is a reanalysis by title. "
    "Fetched again by the NOVELTY reviewer at 2026-11-18T22:55:56Z: HTTP 200, hitCount 32, the same titles (panel/novelty.md).\n\n"
    "Data: Dryad doi 10.5061/dryad.hmgqnk9nj, version 16 (2025-09-27), CC0; file 20231225_dfall_obs_data_and_spectral_features_revision1_n469.csv, "
    f"sha256 {sha(SRC)} (equal to the digest Dryad publishes for it).\n")
# INDEX.csv
with open(out / 'INDEX.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(('target_id', 'cell', 'value', 'table_value', 'table_fetched_utc', 'file', 'sha256'))
    w.writerow(('elephant-rumble-receiver-identity-beyond-caller', 'p3', repr(S['mean']['rf']), '0.275', '2026-11-18T22:55:56Z', 'object/summary.json', sha(out / 'object/summary.json')))
scope = [l for l in (RUN / 'panel/gate.md').read_text().splitlines() if l.startswith('confirmed_scope: ')][0][len('confirmed_scope: '):]
(out / 'README.md').write_text(f"""# Elephant rumbles: the 27.5% receiver accuracy against caller habits and a within-caller shuffle

## What

{scope}

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only, under a minute). It checks the hashes, then recomputes from the saved per-call predictions and the call list every accuracy of the 100 fold draws, the fold stratification, the caller-habit rule, the 1,000 shuffle controls' statistics and every statement of partial win p3. Expected last line: PASS. Rebuilding the predictions themselves takes about 2.5 hours on 4 cores; see RUN_IT_YOURSELF.md.

## Compared to

| what | value | source |
|---|---|---|
| Pardo et al. (2024) random forest | 27.5% | the paper, as quoted by the bank entry |
| our re-implementation, mean of 100 fold draws | {S['mean']['rf']:.4f} | object/summary.json |
| caller-habit baseline, same draws | {S['mean']['habit']:.4f} | object/summary.json |
| forest on within-caller shuffled labels, 1,000 controls: 99.9th percentile / maximum | {S['null_rf']['p99_9']:.4f} / {S['null_rf']['max']:.4f} | object/null-rf-controls.jsonl |

Status source (Europe PMC citations of the paper) fetched 2026-11-18T22:55:56Z by the NOVELTY reviewer: 32 citing papers, none a reanalysis. See the-record-we-beat/snapshot.md.

## Not claimed

The full win: a preregistered caller-habit-plus-acoustic pipeline scored {S['mean']['pa']:.4f} against the habit baseline's {S['mean']['habit']:.4f}, inside its own within-caller shuffle null (99.9th percentile {S['null_pa']['p99_9']:.4f}); its outputs are in how-we-built-it/ and it is not claimed. Not claimed either: that elephants do or do not use names, partial wins p1 and p2, or an exact replication of ranger and caret (the trees are scikit-learn CART and the folds come from our own stratified generator; a with-replacement forest scores lower, 0.258, still above its own shuffle null; panel/gate.md lists every disclosure). The shuffle null's tail is noisy: a reviewer's own 10 shuffles reached 0.2471, still below 0.275 and 0.2695. object/calls.csv lists only the sound IDs, callers and receivers of the 437 calls (three columns of the CC0 Dryad deposit, no acoustic features), because Dryad refuses scripted downloads; how-we-built-it/code/build_package.py shows how it is cut from the Dryad file, whose sha256 is in the-record-we-beat/snapshot.md.

## Credits

Data and the original analysis: Pardo, Fristrup, Lolchuragi, Poole, Granli, Moss, Douglas-Hamilton and Wittemyer, [Nature Ecology and Evolution 8:1353-1364 (2024)](https://doi.org/10.1038/s41559-024-02420-w); data on [Dryad](https://doi.org/10.5061/dryad.hmgqnk9nj) (CC0); code on [Zenodo 10576772](https://zenodo.org/records/10576772). Citation index: [Europe PMC](https://europepmc.org/). Tools: NumPy, pandas, scikit-learn. Run by the V3R1T4S kit (Claude Code as lead agent, with three fresh reviewer subagents).
""")
(out / 'RUN_IT_YOURSELF.md').write_text("""# Run it yourself

1. Check the package: `sh verify-it-yourself/run_checks.sh` (expect PASS). Standard library only.
2. Rebuild the predictions: download the Dryad deposit doi 10.5061/dryad.hmgqnk9nj (version 16) in a browser (Dryad refuses scripted downloads) and check the spectral and cepstral n469 files against Dryad's sha-256 digests. Make a folder with `code/` (copy how-we-built-it/code/*.py) and `data/` (the two n469 CSV files). Install how-we-built-it/requirements.txt (Python 3.12). Then, with OMP_NUM_THREADS=1:
   `WORKERS=4 python3 code/run_real.py && python3 code/context_check.py && python3 code/null_pa.py && python3 code/null_rf.py && python3 code/summarize.py`
   (about 2.5 hours on 4 cores). output/summary.json must equal object/summary.json, and output/real/draw_SSS.json must equal object/real-draws/draw_SSS.json byte for byte. A single file can be replayed in seconds with `python3 code/replay.py real <s>` or `python3 code/replay.py null_rf <j>` once output/ holds the saved files.
3. The call list: object/calls.csv equals the rows with Cert_ID_Bin == 1 of the spectral n469 file, columns soundID, CallerID, Elicitor1_ID, in file order.
""")
(out / 'HOW_WE_FOUND_IT.md').write_text("""# How we found it (contributor text, unverified)

The scout computed the bank's caller-habit baseline (about 0.49) before any model ran on the acoustic features, which showed that the paper's 27.5% sits far below simply guessing each caller's usual receiver. We then froze one plan (PREREG.md) for two lenses. The paper's forest, re-implemented, landed at 0.2695 and beat all 1,000 within-caller shuffles of its labels (maximum 0.2449), so it does carry some receiver-specific structure beyond each caller's receiver frequencies, while staying about 22 points below the caller-habit rule. The full-win attempt (caller-habit prior plus a within-caller acoustic distance, its weight chosen by nested cross-validation) did not beat the habit baseline (0.4902 vs 0.4922) and sat inside its own shuffle null, so with these summary features and a median of two calls per receiver we found no usable receiver signal beyond the caller's habits.
""")
files = sorted(p for p in out.rglob('*') if p.is_file() and p.name != 'SHA256SUMS')
(out / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(out)}\n' for p in files))
print(sid)
