# Status source and table record
- status_source (bank): https://en.wikipedia.org/wiki/Mertens_conjecture , fetched 2026-11-25T00:47:07Z, HTTP 200,
  sha256 63a125428c82569e4b4eba8474699960f28cad0c679981e27add1ea24ac2ac5a ; cites Kim-Nguyen exp(1.96e19) as the bound; does not mention the 3.485e18 claims.
- Certificate checked: https://raw.githubusercontent.com/bzyzz/mertens_bound/a0b267c2/certification/k2_certificate.json ,
  fetched 2026-11-25T00:47Z, HTTP 200, sha256 811145be4741c4cb42f9fe1e5eefca2ffc9ee01bbfae32925ca2db0a85df48ff (copy in inputs/). Repo head a0b267c2 (2026-10-22T14:26:15Z), README
  "Status: not peer-reviewed". The certificate gives K2_main (n <= 600,000) as a ball and the rest only as a bound
  K2_tail_ball = [+- 9.43e-12].
- Open V3R1T4S PRs on this target id (2026-11-25 ~00:49Z): only #1234 (p1, Kim-Nguyen tables; no bound claimed).
- Independence caveat: the zeros in this claim come from FLINT/Arb's acb_dirichlet_zeta_zeros, the same routine the
  certificate uses (python-flint 0.9.0 / FLINT 3.6.0 per its versions field); the code is separately written.
