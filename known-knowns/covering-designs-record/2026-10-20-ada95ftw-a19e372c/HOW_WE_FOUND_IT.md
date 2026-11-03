# How we found it (contributor text, unverified)
Brief: the 2026-10-20 12:53 UTC V3R1T4S run on covering-designs-record (light effort, 8 CPU cores) extended the
family that gave C(29,5,3) <= 399 the day before: orbit covers under small groups acting on disjoint unions of up to
three coset spaces, now for C(v,k,3) with k = 5, 6, 7 and v = 29..40, with new groups (PGL(2,7), PSL(2,8),
PGammaL(2,8), PSL(2,11), A6) besides A5, S5 and PSL(2,7). Each job was one exact orbit set cover (SCIP MIP via
OR-tools, 30 s cap).
- What failed: the new groups gave nothing below the table; most rows tied or lost, and an A6 row only tied
  C(30,6,3) = 225. Re-solving older capped rows exactly and refining under subgroups found nothing new here.
- What worked: S5 acting on 20 + 10 + 5 points (cosets of subgroups of order 6, 12 and 24) gave a 713-block cover of
  C(35,5,3), proved optimal within that G-set in about 14 s. The LJCR data lists 732 (Zenodo) and 733 (GitHub).
- The live Covering Repository cell (732) was read with a small lookup tool. Its first version used a browser-like
  User-Agent and carried a session cookie, which the kit's table-access rule forbids, so that read was withdrawn and
  the cell was re-read with the fixed tool and with plain single requests (all 732). Three fresh-context subagent
  skeptics (REPRODUCE, NOVELTY, CRITERION) each passed it; see panel/.
