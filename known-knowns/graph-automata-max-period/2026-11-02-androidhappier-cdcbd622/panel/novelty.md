# NOVELTY panel: A357952(9) = 200
context: subagent (novelty skeptic, isolated claim copy)

Claim: A357952(9) = 200; witness graph6 `H?o|]|~`, rule {1,3,5} (counting self), start state 1 (node 0 ON).
Inputs read: claim copy in the panel tmp directory (claim.md, REPRODUCE.md, table_record.md) plus public web/GitHub only.

## 1. Primary table (one fetch, no retries)
- URL: https://oeis.org/search?q=id:A357952&fmt=text
- UTC: 2026-11-02T21:50:44Z, HTTP 200, sha256 760308c0b91d85ea8aa5ba802ed5fd374f0d1fef38c7d56b023ff5892d94bb9b
  (identical to the claim's table_record fetches at 21:05:02Z and 21:35:11Z).
- %S A357952 2,2,4,6,8,18,42,112 — DATA still ends a(8)=112. Keywords nonn,more,hard.
- The string "200" appears nowhere in the entry (grep count 0). a(9) is open in the live entry.

## 2. GitHub elder-plinius/V3R1T4S (PRs open+closed, code)
- PR search "A357952": 1 hit, #904 (open, 2026-11-02T18:47:50Z UTC), "[claim] graph-automata-max-period: A384209(10) = 46";
  its body says A357951, A357952 and A357953 are "not claimed". Different cell; does not fill A357952(9).
- PR search "graph-automata-max-period OR totalistic OR A357953 OR A384209": #904, #859, #699 (subtraction-game bank),
  #534 (SAW bound). None claims A357952(9) or 200 at n=9. A357953(9)=180 and A384209(10)=46 are different cells.
- Repo grep (local clone at origin/HEAD 9a0d19a, 2026-11-02T05:14:05-08:00) for the witness string `H?o|]|~`: no hits.
  A357952 only shows up in known-unknowns/graphs-games-automata/ (bank entry: "n <= 8, a(8) = 112", open) and bank/targets.json.
- GitHub-wide code search "A357952": only loda-lang/loda-programs oeis/357/A357952.asm (a fitted recurrence reproducing the
  8 listed terms; not an enumeration, no a(9) claim) plus the V3R1T4S known-unknowns files; the rest is unrelated noise.

## 3. TROPHY_CASE.md / known-knowns/
- git grep on origin/HEAD and the working tree for A357952, A357953, A384209 and `H?o|]|~` in TROPHY_CASE.md and known-knowns/: no hits.
  This cell has no trophy or known-known.

## 4. Literature (last 24 months)
- Web searches ("A357952 ... a(9)", "maximum period totalistic cellular automata graphs 9 nodes 2025 2026"): only the OEIS entries
  A357951/2/3, the von Brömssen OEIS wiki page, LifeWiki, and arXiv 2607.10453 ("Pulse Graphs", July 2026), which uses a different
  model (prime in-neighbour counts on directed graphs, exact only up to n<=5). Nothing gives A357952(9) or any value at n=9.

## Verdict
No public source has A357952(9). The live OEIS DATA stops at a(8)=112, and the cell is listed as open in the bank. A new exact term
for an open cell beats everything known, so this is not a tie. (This panel checks novelty only. Whether 200 is correct is up to the
reproduction panels.)

pass: true
