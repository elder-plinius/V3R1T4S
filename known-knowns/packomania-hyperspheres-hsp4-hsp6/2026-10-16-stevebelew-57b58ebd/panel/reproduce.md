# REPRODUCE skeptic verdict for claim N88 (hsp4)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Scope: only the claim folder was read (CLAIM.md, hsp4-88-candidate.txt, hsp4-88-posted.txt, hsp4_radius_as_fetched.txt, and REPRODUCE.md last). No web access, nothing else on the machine. The author's code was not executed; my own checker was written from the definition first and the author's REPRODUCE.md was read only afterwards.

## Definition used (quoted from the success criterion in CLAIM.md)

"the FEASIBLE radius r* := min( min_{i,j : i strictly before j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 (the table carries 12 decimals; 1e-10 is 200x its rounding), AND the configuration is not isometric to the posted hsp[d]-[N].txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"

Transliteration note for this file: inside the quote above, the strict-order subscript on the inner minimum and the two placeholders in the posted filename have been spelled out in words / square brackets so that this document carries no angle-bracket characters; nothing else in the quote was changed. The formula I implemented is: r* = min( (smallest distance over all unordered pairs of distinct centres) / 2 , 1 - (largest Euclidean norm of any centre) ), with mp.dps = 50 and exact mpmath comparisons (no epsilon anywhere).

## Checker (my own; run with the venv python, flag -I, claim folder passed as argv[1])

```python
# Independent checker for claim N88 (hsp4), written from the definition in CLAIM.md:
#   r* := min( half of the smallest pairwise centre distance , 1 - max_i |c_i| )
#   unit container ball centred at the origin; mpmath at 50 digits; no tolerance.
# Comparisons go through lt() (mpmath sign) so this file carries no angle-bracket characters.
import sys, hashlib
from mpmath import mp, mpf, sqrt, nstr, sign
mp.dps = 50

CLAIMDIR = sys.argv[1]
N_EXPECTED = 88
D = 4

def lt(a, b):          # exact: True iff a is strictly less than b
    return sign(b - a) == 1

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def dist(p, q):
    return sqrt(sum((p[k] - q[k]) ** 2 for k in range(D)))

def parse_candidate(path):
    pts = []
    for line in open(path):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        tok = s.split()
        if len(tok) != D:
            raise ValueError(f"{path}: bad token count {len(tok)} on line {s!r}")
        pts.append([mpf(t) for t in tok])
    return pts

def rstar(pts):
    dmin = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = dist(pts[i], pts[j])
            if dmin is None or lt(d, dmin):
                dmin = d
    nmax = max(sqrt(sum(c ** 2 for c in p)) for p in pts)
    return min(dmin / 2, 1 - nmax), dmin, nmax

def pairdists(pts):
    return sorted(dist(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts)))

cand_path = f"{CLAIMDIR}/hsp4-88-candidate.txt"
post_path = f"{CLAIMDIR}/hsp4-88-posted.txt"
tab_path  = f"{CLAIMDIR}/hsp4_radius_as_fetched.txt"
for p in (cand_path, post_path, tab_path):
    print("sha256", p.split('/')[-1], sha(p))

# candidate: one comment line, then 88 lines of 4 coordinates
cand = parse_candidate(cand_path)
print("candidate point count:", len(cand), "(expected", N_EXPECTED, ")", "OK" if len(cand) == N_EXPECTED else "FAIL")
print("candidate all finite:", "OK" if all(mp.isfinite(c) for p in cand for c in p) else "FAIL")

# posted: first line is the radius, then "index x1 x2 x3 x4"
lines = [l for l in open(post_path).read().splitlines() if l.strip()]
posted_hdr = mpf(lines[0].strip())
post = []
for l in lines[1:]:
    tok = l.split()
    if len(tok) != D + 1:
        raise ValueError("posted: bad line " + repr(l))
    post.append([mpf(t) for t in tok[1:]])
print("posted point count:", len(post), "OK" if len(post) == N_EXPECTED else "FAIL")
print("posted header radius:", nstr(posted_hdr, 20))

# table: rows "N radius"
table = {}
for l in open(tab_path):
    tok = l.split()
    if len(tok) == 2:
        table[int(tok[0])] = mpf(tok[1])
tab88 = table[N_EXPECTED]
print("table rows:", len(table), "row 88 value:", nstr(tab88, 20))
print("posted header == table row 88:", "OK" if posted_hdr == tab88 else "FAIL")

r_cand, dmin_c, nmax_c = rstar(cand)
r_post, dmin_p, nmax_p = rstar(post)
print("candidate: dmin/2 =", nstr(dmin_c / 2, 30), " 1-maxnorm =", nstr(1 - nmax_c, 30))
print("candidate r* =", nstr(r_cand, 40))
print("posted:    dmin/2 =", nstr(dmin_p / 2, 30), " 1-maxnorm =", nstr(1 - nmax_p, 30))
print("posted r* =", nstr(r_post, 40))

diff_post_tab = abs(r_post - tab88)
print("|posted r* - table| =", nstr(diff_post_tab, 10), "(at most 1e-11)", "OK" if not lt(mpf('1e-11'), diff_post_tab) else "FAIL")

gain = r_cand - tab88
print("candidate r* - table =", nstr(gain, 15), "(at least 1e-10)", "OK" if not lt(gain, mpf('1e-10')) else "FAIL")
print("candidate r* strictly above table:", "OK" if lt(tab88, r_cand) else "FAIL")

pc = pairdists(cand); pp = pairdists(post)
assert len(pc) == len(pp) == N_EXPECTED * (N_EXPECTED - 1) // 2
maxdev = max(abs(a - b) for a, b in zip(pc, pp))
print("pair count:", len(pc), "max |sorted-dist diff| =", nstr(maxdev, 10), "(more than 1e-8)", "OK" if lt(mpf('1e-8'), maxdev) else "FAIL")

print("RSTAR_CAND_FULL", mp.nstr(r_cand, 50))
```

## Real output (run A; run B was byte-identical, see determinism below)

```text
sha256 hsp4-88-candidate.txt 57b58ebd166e6338aa97219429ba49100cd64b376a21e7d3b3c483e7d5a96e68
sha256 hsp4-88-posted.txt 25619cce9602d44bc867863108963cba501c13bee96e837a294144a8049de2f9
sha256 hsp4_radius_as_fetched.txt f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f
candidate point count: 88 (expected 88 ) OK
candidate all finite: OK
posted point count: 88 OK
posted header radius: 0.248505598356
table rows: 299 row 88 value: 0.248505598356
posted header == table row 88: OK
candidate: dmin/2 = 0.248514071390619123124834421303  1-maxnorm = 0.248514071390400259345584842155
candidate r* = 0.2485140713904002593455848421553032863821
posted:    dmin/2 = 0.248505598355296302441464593227  1-maxnorm = 0.248505598355162058455939161984
posted r* = 0.2485055983551620584559391619837109221698
|posted r* - table| = 8.379415441e-13 (at most 1e-11) OK
candidate r* - table = 8.47303440025935e-6 (at least 1e-10) OK
candidate r* strictly above table: OK
pair count: 3828 max |sorted-dist diff| = 0.01570545603 (more than 1e-8) OK
RSTAR_CAND_FULL 0.24851407139040025934558484215530328638211795818054
```

sha256 of the two output files:
b00c3d99f1cbfe3ca9c6787953dfd5173dbb3befc49ea19ee3ca95e8fd78fcb9  n88_runA.txt
b00c3d99f1cbfe3ca9c6787953dfd5173dbb3befc49ea19ee3ca95e8fd78fcb9  n88_runB.txt

## Property-by-property verdict

| Property | Evidence | Verdict |
|---|---|---|
| Exactly 88 points in hsp4-88-candidate.txt | parser (comment line skipped, 4 tokens per line enforced) counted 88 | PASS |
| All coordinates finite | mp.isfinite true for all 352 values | PASS |
| Posted file has 88 points and its header equals table row 88 | 88 points; header 0.248505598356 == table 0.248505598356 | PASS |
| Parser sanity: r*(posted) reproduces table value within 1e-11 | r*(posted) = 0.24850559835516205845...; abs diff 8.379e-13 | PASS |
| r*(candidate) at 50 digits | 0.24851407139040025934558484215530328638211795818054; binding term is the container (1 - max norm), dmin/2 is 2.19e-13 larger | computed |
| r*(candidate) strictly greater than table 0.248505598356 | yes, exact mpmath comparison | PASS |
| Margin at least 1e-10 | gain = 8.47303440025935e-6 (about 84,730 times the required margin) | PASS |
| Not isometric to posted (sorted pairwise-distance multisets differ by more than 1e-8 somewhere) | 3828 pairs each; max abs difference of sorted lists = 0.01570545603 | PASS |
| Determinism of r*(candidate) across two runs | two separate -I invocations; output files byte-identical (same sha256, cmp clean); 50-digit r* string identical | PASS |
| Claimed value in CLAIM.md "0.248514071390400..." | matches my 0.2485140713904002593... | PASS |
| Claimed gain "about 8.47e-06" | matches my 8.473e-6 | PASS |

## Comparison with the author's REPRODUCE.md (read only after my runs)

The author's script implements the same definition: mp.dps = 50, r* = min(dmin/2, 1 - max norm), table row 88 parsed from hsp4_radius_as_fetched.txt, non-isometry via sorted pairwise-distance lists with the 1e-8 threshold. Its loader takes the last four tokens per line and skips lines with fewer than four tokens, which handles both file formats (the posted file's one-token radius header is skipped). No definitional mismatch with my checker. The three curl commands at the end of REPRODUCE.md (live re-fetch of radius.txt, the hsp4.html last-update string, and the pending-requests page) are outside my scope (no web access) and were not run; the liveness, history-of-updates and queue-rule conditions of the criterion are therefore NOT verified here and remain for whichever panel member owns the live check. The CLAIM.md caveat about the category-unspecified "Moki and Julio" pending bundle stands.

## Mismatches found

None in the mathematical claim. One cosmetic observation: the comment line in hsp4-88-candidate.txt reports r_float=0.24851407139040016, whereas the 50-digit value is 0.24851407139040025934...; the difference is about 1e-16, i.e. a double-precision rounding artifact in the comment, not a discrepancy in the claimed value (which CLAIM.md states as 0.248514071390400...). It does not affect any criterion.

## Process note

My first attempt wrote outputs under generic names in a scratch directory shared with sibling panel agents, and one output file was overwritten by another agent's N=81 run between two of my commands. I discarded that attempt and redid both runs in a private subdirectory with unique names; the output and hashes pasted above come from that clean rerun.

pass: true
