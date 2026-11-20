# Live Record Table Snapshot: `cohn-sphere-packing-density-table` (Dimension `n = 19`)

## Primary Live Status Source (`https://cohn.mit.edu/sphere-packing/`)
- **Author / Maintainer**: Henry Cohn (*Sphere packing*)
- **URL**: https://cohn.mit.edu/sphere-packing/
- **UTC Fetch Time**: `2026-11-19T06:31:25Z`
- **HTTP Status**: `200`
- **Payload Size**: `88271` bytes
- **SHA-256 of Fetched HTML Page**: `82146ed92040267f45ec2862c58534d28fe2aad5e531a7525e3e80955a4bb26d`
- **Selected Response Headers**:
  - `HTTP/2 200`
  - `server: openresty`
  - `date: Thu, 19 Nov 2026 06:31:25 GMT`
  - `content-type: text/html; charset=UTF-8`
  - `last-modified: Thu, 19 Nov 2026 04:06:39 GMT`
  - `strict-transport-security: max-age=31536000`
  - `x-content-type-options: nosniff`

## Extracted Table Cells for Dimension `n = 19`
- **Unrestricted Periodic / General Sphere Packings Table (Table `1`, row `n = 19`)**:
  - `n`: `19`
  - `Center density`: `3^(-9) * 5^(-21/2) * 13^(19/2)` (exact squared center density `13^19 / (3^18 * 5^21) = 1461920290375446110677 / 184736485004425048828125`)
  - `#` (spheres per unit cell of underlying Bravais lattice): `6`
  - `Density`: `0.0041473691458627...`
  - `Upper bound`: `0.0092288097047995`
  - `Ratio`: `2.226`
  - `References`: `[8, 25]` where `[8]` is Ruitao Chen, Jiachen Hu, Binghui Li, Liwei Wang, and Tianyi Wu, *New Sphere Packings from the Antipode Construction*, preprint, `2025`, `https://arxiv.org/abs/2505.02394`, and `[25]` is Alexey Kravatskiy, *Sphere-packing density bounds and constructions*, `2026`, `https://github.com/alexlegeartis/SpherePackings` (upper bound; repository `CITATION.cff` title: *Sphere-packing density: new upper bounds in dimensions 4 through 48, with verification packages*).
- **Lattice Packings Only Table (Table `3`, row `n = 19`)**:
  - `n`: `19`
  - `Center density`: `2^(-7/2)`
  - `Density`: `0.0041208062797686...`

## Primary Literature Snapshots Verified for Novelty & Rigidity Scope
| Source | URL | UTC Fetch Time | HTTP | Bytes | SHA-256 | Verified Scope |
| --- | --- | --- | --- | --- | --- | --- |
| Henry Cohn live table (`v2` pre-claim fetch) | https://cohn.mit.edu/sphere-packing/ | 2026-11-19T06:31:25Z | 200 | 88271 | `82146ed92040267f45ec2862c58534d28fe2aad5e531a7525e3e80955a4bb26d` | Confirms `n = 19` record center density remains `3^(-9) * 5^(-21/2) * 13^(19/2)` (`# = 6`, sole lower-bound ref `[8]`) |
| Ruitao Chen, Jiachen Hu, Binghui Li, Liwei Wang, and Tianyi Wu (2025) TeX source | https://arxiv.org/e-print/2505.02394 | 2026-11-19T01:21:40Z | 200 | 14256 | `e114460c10a5770100eaafd647426bc5c7eb8e915aed9d2b3179cb36789a821e` | Gives sole published `n = 19` packing at this density (`Orbit I`, `norm4(L_I) = 6942`, kissing `4110` per sphere); no `Orbit II` embedding reported |
| Ivan Dorofeev, Xiaoming Sun, and Chengu Wang (2026) TeX source | https://arxiv.org/e-print/2607.20359 | 2026-11-19T01:23:02Z | 200 | 27364 | `a242514d574e67bf4f9fabb2b2a24fb5b5a5ec3ab9487410bbc1dfb47621dd8a` | Studies `P_48` cross-sections in dimensions `38..47` only; does not treat `n = 19` |
| Alexey Kravatskiy (2026) `RESULTS.md` and `CITATION.cff` | https://raw.githubusercontent.com/alexlegeartis/SpherePackings/main/RESULTS.md | 2026-11-19T01:24:03Z | 200 | 17081 | `630ad07ac3cdd830af83cb1946c4b9737bc09a431eadda0b06280b62df87ac23` | Upper bounds plus lower constructions in `dim36` and `dim59` only (`CITATION.cff` SHA-256 `676b44b261460aebb06dd9fbdf2c72bde0227fc8d700a1bf932dcc2f6a6299f7`) |
| arXiv API search (`"antipode construction" OR "2505.02394"`) | https://export.arxiv.org/api/query?search_query=all:%22antipode+construction%22+OR+all:%222505.02394%22&max_results=25 | 2026-11-19T01:24:50Z | 200 | 5757 | `0a7381b150df7acec8cb117705f67a59155e4f534830c748669b776894eb8737` | Confirms zero subsequent papers constructing companion `n = 19` packings |
| Salvatore Torquato & Frank H. Stillinger (2001) Crossref | https://api.crossref.org/works/10.1021/jp011960q | 2026-11-19T06:31:27Z | 200 | 6525 | `70460a29f6c0306d3a24d0eee69c7b149ce16a8990e721e17e1c918278164036` | *J. Phys. Chem. B* `105(47)`, `11849`–`11853` (`2001`), unilateral hard-particle jamming taxonomy |
| Aleksandar Donev, Salvatore Torquato, Frank H. Stillinger & Robert Connelly (2004) Crossref | https://api.crossref.org/works/10.1016/j.jcp.2003.11.022 | 2026-11-19T06:31:29Z | 200 | 9365 | `9b927b6f9b63d7afc3462e307eb12724c8c608717f4ecfefcc92f48b4f38048a` | *J. Comput. Phys.* `197(1)`, `139`–`166` (`2004`; companion *J. Appl. Phys.* `95(3)`, `989`–`999`, SHA-256 `d23359e28f6120f757f4c65833aba2ea83e01aebeda5edaa170d1855e7567347`), Farkas positive-stress criterion |
