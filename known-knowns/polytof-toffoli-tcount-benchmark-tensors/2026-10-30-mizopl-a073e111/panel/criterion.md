context: isolated Antigravity subagent 6a66af46-2f89-4de9-ad9a-7d97b80aa3a4 (V3R1T4S Skeptic CRITERION)
target_id: polytof-toffoli-tcount-benchmark-tensors
run_id: 2026-10-30-a073e111

# Adversarial Skeptic Report: `CRITERION`

- **Package:** `2026-10-30-mizopl-a073e111`
- **Problem Criterion (`p2`):**
  > *"p2: A certified optimality proof for a table row whose optimality is not already published: an exhaustive or SAT/DRAT certificate that no decomposition with (table value - 1) terms exists for that tensor variant, re-checkable in under an hour."*
- **Maintainer Review Criteria (`2026-10-29T23:11:07Z`):**
  - **Separate single-row PR**: Scoped exclusively to row `0725` ($\mathrm{GF}(2^2)$ mult, $n=6$, $5$ cubic monomials, `CP = 3`, `Waring = 17`), leaving out `Mod 5_4` and `CP = 1`.
  - **Executable solver/obstruction check**: `verify-it-yourself/verify.py` recomputes the entire Grassmannian $\operatorname{Gr}(3, \mathbb{F}_2^6)$ exhaustion ($1,395$ singletons + $972,315$ pairs = $0$ solutions at $R \le 2$; $120$ triples at $R = 3$), bilinear exhaustion ($9$ singletons + $36$ pairs = $0$ solutions at $R \le 2$; $3$ triples at $R = 3$), and punctured Reed-Muller coset enumeration ($2^{22} = 4,194,304$ valid Waring decompositions = $0$ solutions at $r \le 16$; $1,008$ optimal weight-17 solutions at $r = 17$) from scratch in `0.21s`.

pass: true
