# Novelty Skeptic Report (`voynich-generator-heldout-fingerprints` — Partial Win `p2`)

context: subagent

## 1. Independent Live Fetch of `status_source` and Primary Benchmark Reference

Both the target's `status_source` and the primary `p2` benchmark paper (`arXiv:2604.19762`) were fetched once honestly using `curl -sS -D -` with no user-agent spoofing and no retries:

1. **Target `status_source` (`claim/CLAIM.md`)**:
   - **URL**: `https://www.voynich.nu/transcr.html`
   - **UTC Fetch Time**: `2026-10-24T15:15:37Z`
   - **HTTP Status**: `HTTP/2 200` (`200 OK`)
   - **Last-Modified Header**: `Sat, 31 May 2025 00:16:05 GMT`
   - **Content-Length**: `60410` bytes
   - **SHA-256**: `57f8aaf6b1cdd6a292361b3a94e723f8fb14f0960b2cb349acee142fbadb19a5`
   - **Verification**: Exact byte-for-byte match with `claim/data/transcr.html`. Links to the current canonical transliteration files `data/ZL3b-n.txt` ("v. 3b"), `data/IT2a-n.txt` ("v. 2a"), and `data/RF1b-e.txt` ("full"), matching `claim/data/ZL3b-n.txt`, `claim/data/IT2a-n.txt`, and `claim/data/RF1b-e.txt`.

2. **Primary Benchmark Reference for Partial Win `p2`**:
   - **URL**: `https://arxiv.org/abs/2604.19762`
   - **UTC Fetch Time**: `2026-10-24T15:15:38Z`
   - **HTTP Status**: `HTTP/2 200` (`200 OK`)
   - **Last-Modified Header**: `Mon, 24 Aug 2026 19:41:09 GMT`
   - **Content-Length**: `41942` bytes
   - **SHA-256**: `f43d3885b01f235d338191f4fa2053ef6b6e044ba9e246f23a7a571570a66ad3`
   - **Verification**: Exact byte-for-byte match with `claim/data/arxiv_2604.19762.html`. The latest version is `v2` (submitted 26 Mar 2026, last revised 16 Jun 2026) by Christophe Parisel, titled *"Evidence of Layered Positional and Directional Constraints in the Voynich Manuscript: Implications for Cipher-Like Structure"*. The published abstract confirms that the problem of jointly passing the four signatures remains open across the tested generator families:
     > *"We further evaluate two classes of structured generator against a four-signature joint criterion: a parametric slot-based generator and a Cardan grille implementing Rugg's (2004) gibberish hypothesis. Across their full tested parameter spaces, neither class reproduces all four signatures simultaneously."*

---

## 2. Repository Trophy Case, Open Pull Requests, and 24-Month Literature Search

1. **Repository Trophy Case (`TROPHY_CASE.md`)**:
   - Inspected all 53 rows across the six result families (`degree-diameter graphs`, `constant-weight codes`, `Lehmer's totient problem`, `matrix multiplication`, `VNN-COMP 2026 counterexamples`, `RobustBench CIFAR-100 attack`) and two `cipher-challenge commitments` (`Bouchaudy Hebern 5-rotor Problem 8` and `Bouchaudy Kryha v2 Problem 5`).
   - **Result**: Zero prior entries exist for `voynich-generator-heldout-fingerprints`, Voynich generators, `arXiv:2604.19762`, or Currier signatures.

2. **GitHub Pull Request Search**:
   - **URL**: `https://api.github.com/search/issues?q=voynich-generator-heldout-fingerprints+type:pr`
   - **UTC Fetch Time**: `2026-10-24T15:15:38Z`
   - **HTTP Status**: `HTTP/2 200` (`200 OK`)
   - **Response**: `"total_count": 0`, `"incomplete_results": false`, `"items": []`. No open or closed pull requests target `voynich-generator-heldout-fingerprints`.

3. **24-Month Literature Search (including post-`2026-10-03` cutoff check)**:
   - Searched the scientific literature and web records for `"2604.19762"`, `"currier-signatures"`, `"Positional and Sequential Structure in the Voynich Manuscript"`, `"2608.17096"`, and `"Naibbe"` generators through October 2026, including an explicit filter for works published after `2026-10-03`.
   - **Result**: Aside from Parisel's benchmark paper `arXiv:2604.19762` (June 2026, whose slot-based and Cardan-grille generators fail the joint four-signature criterion), Greshko's Naibbe cipher (2025, which fails the `E->S >= 60%` and strict-Zipf criteria), and Rozanova & Temerev's `arXiv:2608.17096` (August 2026, which analyzes Naibbe's edge-glyph coupling and singleton-rate limitations without constructing a generator passing the four signatures of `arXiv:2604.19762`), no generator published after `2026-10-03` (or prior to it) achieves joint passage of all four Currier signatures of `arXiv:2604.19762` across Currier A and Currier B on `ZL3b-n.txt` and `IT2a-n.txt` within the hand-executable limits ($\le 200$ table entries, $\le 1$ per-folio state bit).

---

## 3. Quantitative Comparison Against Published Baselines

The claimed generator `VBCLC-152` (`claim/vbclc.py`, `claim/HAND_PROCEDURE.md`, `claim/vbclc_200streams_evaluation.json`) uses **152 table entries** ($\le 200$ limit) and **1 per-folio state bit** $\sigma_f \in \{0, 1\}$ ($\le 1$ limit), and is evaluated over **200 streams per cell** (20 period Latin and Italian plaintexts $\times$ 10 seeds) against the published baselines in `arXiv:2604.19762` (`claim/data/signatures_v27.py`, `claim/data/grille.py`) and `claim/data/author/naibbe.py` (recorded in `claim/CLAIM.md` and `claim/reference_calibration.json`):

| Generator / Model | Hand-Executable Budget | `A/ZL3b` Joint Pass Rate | `B/ZL3b` Joint Pass Rate | `A/IT2a` Joint Pass Rate | `B/IT2a` Joint Pass Rate | Key Statistics (`E->S`, Cross-Boundary `MI`, `Shape`) |
|---|---|---|---|---|---|---|
| **Slot-Based Generator** (`claim/data/signatures_v27.py`, `arXiv:2604.19762`) | Parametric slot tables | `10.0%` (`2/20` adaptive; `10.0%` fixed) | `0.0%` (`0/20` adaptive; `0.0%` fixed) | `10.0%` (`2/20` adaptive) | `0.0%` (`0/20` adaptive) | Fails `MI` and `Shape`: `MI = 0.1771 < 0.2910` on A; `MI = 0.1396 < 0.2508` on B (`0.1312` at 37k words); `50%` Intermediate shape |
| **Cardan-Grille Generator** (`claim/data/grille.py`, `arXiv:2604.19762`, `G0/G1/G2/G6`) | 36-cell table + grilles | `0.0%` (`0/20` across all modes) | `0.0%` (`0/20` across all modes) | `0.0%` (`0/20` across all modes) | `0.0%` (`0/20` across all modes) | Fails `E->S` directionality: `E->S = 0.30% - 17.76%` (requires `>= 60.0%` fixed / `>= 55.2%` adaptive) |
| **Unmodified Naibbe Cipher** (`claim/data/author/naibbe.py`, Greshko 2025) | 6 tables (156 entries), 0 state bits | `10.0%` adaptive (`0.0%` fixed / strict-Zipf, `0/40`) | `100.0%` adaptive (`0.0%` fixed / strict-Zipf, `0/40`) | `10.0%` adaptive (`0.0%` fixed / strict-Zipf) | `100.0%` adaptive (`0.0%` fixed / strict-Zipf) | Fails `E->S` on A & fixed (`E->S = 53.17%` on A, `52.87%` on B vs `60.0%` fixed / `55.99%` A adaptive) and fails strict Zipf (`Shape = Intermediate` on `40/40` streams) |
| **Claimed `VBCLC-152`** (`claim/vbclc.py`, `claim/vbclc_200streams_evaluation.json`) | **152 table entries** ($\le 200$), **1 per-folio state bit** ($\le 1$) | **`100.0%` (`200/200` all criteria)** | **`100.0%` (`200/200` all criteria)** | **`100.0%` (`200/200` all criteria)** | **`100.0%` (`200/200` all criteria)** | Passes all 4 signatures jointly on every stream: `E->S = 68.04%` (`A/ZL3b`), `67.30%` (`B/ZL3b`), `68.09%` (`A/IT2a`), `67.27%` (`B/IT2a`); `MI = 0.4631` (`A/ZL3b`), `0.4312` (`B/ZL3b`), `0.4635` (`A/IT2a`), `0.4307` (`B/IT2a`); `Bilat = 100%`; `Shape = Zipfian` (`200/200` per cell) |

In addition, `VBCLC-152` achieves `200/200 = 100.0%` joint pass rate on the third reference transliteration (`A/RF1b-e` and `B/RF1b-e`) and `100/100 = 100.0%` separately on both period Latin and period Italian plaintexts (`claim/vbclc_200streams_evaluation.json`).

## Conclusion

The claimed result (`VBCLC-152` achieving partial win `p2` on `voynich-generator-heldout-fingerprints`) strictly beats all published baselines in `arXiv:2604.19762` (`0%` on Currier B and `10%` on Currier A for the slot generator; `0%` across all modes for the Cardan grille; `0%` fixed/strict-Zipf and `10%` Currier A adaptive for unmodified Naibbe) by achieving `200/200 (100.0%)` joint passage across Currier A and Currier B on both `ZL3b-n.txt` and `IT2a-n.txt` (as well as `RF1b-e.txt`) within the hand-executable limits (152 table entries $\le 200$, 1 per-folio state bit $\le 1$). No prior solution exists in `TROPHY_CASE.md`, open pull requests, or the literature published after `2026-10-03`.

pass: true
