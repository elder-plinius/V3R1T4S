# Attack Results: `spherical-codes-cohn-table` (Cohn's Table of Spherical Codes)

## Executive Summary

We executed a multi-pronged attack on [Henry Cohn's Table of Spherical Codes](https://spherical-codes.org/) (`spherical-codes-cohn-table`, Tractability 3.5, category `packings-physics`) using a custom Riemannian L-BFGS log-sum-exp homotopy and tangential basin-hopping solver (`sc_opt.c`) coupled with an independent 50-digit `mpmath` verifier and normalizer (`verify_sc.py`).

All candidate codes are normalized onto $(S^{d-1})^N$ to 30 significant digits (`max_norm_err < 1.2e-30`) and verified in 50-digit arbitrary-precision arithmetic (`mpmath.mp.dps = 50`) against both the 12-decimal `plain.txt` table and the 50-digit recomputed value of the posted coordinate files from `spherical-codes.org`.

- **Goal A (`FULL_WIN` — Primary Full Win)**: **6 new record-breaking spherical codes** beating **unstarred, unlabeled** rows in `plain.txt` (rows that do **not** carry the `"needs more optimization"` label and are **not** marked optimal `&ast;`), by up to **$2.4345 \times 10^{-6}$** ($24,345\times$ the $10^{-10}$ full-win threshold).
- **Goal B (`PARTIAL_WIN_P2` — Single-Dimension Batch)**: **24 certified record improvements in a single dimension ($d = 7$)** on rows labeled `"needs more optimization"`, exceeding the $\ge 20$ threshold, with improvements up to **$1.3771 \times 10^{-4}$** ($1,377,124\times$ the $10^{-10}$ threshold).
- **Goal C (`p3` Investigation — Rigid Contact Graph & 500-Digit Polish)**: Established exact infinitesimal rigidity (`rank(J) == d*N - d*(d-1)/2`) and 120-to-500-digit Newton-Raphson contact-graph solutions for unstarred, unlabeled rows `(4, 17)`, `(6, 19)`, `(6, 21)`, `(7, 21)`, `(4, 22)`, and `(8, 18)` (`max_contact_err = 4.3e-483` on `(8, 18)`).

---

## Goal A (`FULL_WIN`): 6 Record Improvements on Unstarred, Unlabeled Rows

All 6 rows below are **unstarred** (`&ast;` absent in `data/index.html`), **unlabeled** (`"needs more optimization"` absent in `data/index.html`), outside the excluded `9 <= d <= 23` kissing-number regime, and strictly improve upon both `plain.txt` and the posted coordinate file by $2.60 \times 10^{-8}$ to $2.43 \times 10^{-6}$.

| $(d, N)$ | `plain.txt` $\cos\theta$ (12d) | New Record $c^*$ (12d) | New Record $c^*$ (30d `mpmath`) | Improvement $\Delta c = c_{\text{table}} - c^*$ | New Minimal Angle $\theta^*$ (deg) | Contacts ($10^{-9}$) | Current Table Attribution | Coordinate File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`(30, 64)`** | `0.038215865917` | **`0.038213431432`** | `0.038213431431870275994193954328` | **`+2.434485e-06`** | `87.809996846648024831` | 1502 | Uploaded by anonymous internet user, 2026 | `results/goal_a/30x64.txt` |
| **`(28, 59)`** | `0.039154654978` | **`0.039154189773`** | `0.039154189772679138676566957165` | **`+4.652053e-07`** | `87.756059008949956782` | 1323 | Pavlos Moros, 2026 | `results/goal_a/28x59.txt` |
| **`(29, 60)`** | `0.032282791684` | **`0.032282689322`** | `0.032282689322403249986273377213` | **`+1.023616e-07`** | `88.150016797797149449` | 1345 | Ilmari Vahteristo, annealing solver | `results/goal_a/29x60.txt` |
| **`(30, 62)`** | `0.031273236170` | **`0.031273183364`** | `0.031273183363813242615324799071` | **`+5.280619e-08`** | `88.207884691079092710` | 1437 | Ilmari Vahteristo, annealing solver | `results/goal_a/30x62.txt` |
| **`(31, 65)`** | `0.037040536638` | **`0.037040509595`** | `0.037040509594848894967753715904` | **`+2.704315e-08`** | `87.877231072692140065` | 1554 | Pavlos Moros, 2026 | `results/goal_a/31x65.txt` |
| **`(27, 56)`** | `0.034509985004` | **`0.034509959006`** | `0.034509959006364448778750463218` | **`+2.599764e-08`** | `88.022325413283082972` | 1185 | Ilmari Vahteristo, annealing solver | `results/goal_a/27x56.txt` |

- Batch summary JSON: `results/goal_a/summary_goal_a.json`
- Individual 50-digit verification receipts: `results/goal_a/{d}x{N}.json`

---

## Goal B (`PARTIAL_WIN_P2`): 24 Certified Improvements in Dimension $d = 7$

We targeted rows labeled `"needs more optimization"` in a single dimension ($d = 7$) and achieved **24 certified improvements** (exceeding the $\ge 20$ threshold for `p2`), each verified in 50-digit `mpmath` with 30-digit normalized coordinate files:

| Rank | $(d, N)$ | `plain.txt` $\cos\theta$ (12d) | New Record $c^*$ (12d) | Improvement $\Delta c = c_{\text{table}} - c^*$ | New Minimal Angle $\theta^*$ (deg) | Contacts ($10^{-9}$) | Coordinate File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **`(7, 308)`** | `0.660836744901` | **`0.660699032482`** | **`+1.377124e-04`** | `48.646793207550857813` | 1433 | `results/p2_d7/7x308.txt` |
| 2 | **`(7, 315)`** | `0.662675365192` | **`0.662539672249`** | **`+1.356929e-04`** | `48.506148541123475835` | 1561 | `results/p2_d7/7x315.txt` |
| 3 | **`(7, 309)`** | `0.660912967551` | **`0.660863660177`** | **`+4.930737e-05`** | `48.634226270510072964` | 1659 | `results/p2_d7/7x309.txt` |
| 4 | **`(7, 313)`** | `0.661974195320` | **`0.661945822982`** | **`+2.837234e-05`** | `48.551558314062885909` | 1690 | `results/p2_d7/7x313.txt` |
| 5 | **`(7, 365)`** | `0.670487284551` | **`0.670467035142`** | **`+2.024941e-05`** | `47.897049265288227739` | 1919 | `results/p2_d7/7x365.txt` |
| 6 | **`(7, 310)`** | `0.660953811794` | **`0.660935439266`** | **`+1.837253e-05`** | `48.628746672318077807` | 1666 | `results/p2_d7/7x310.txt` |
| 7 | **`(7, 323)`** | `0.665046095133` | **`0.665027820692`** | **`+1.827444e-05`** | `48.315460891431995679` | 1647 | `results/p2_d7/7x323.txt` |
| 8 | **`(7, 366)`** | `0.670943830170` | **`0.670926060412`** | **`+1.776976e-05`** | `47.861614315596682479` | 1906 | `results/p2_d7/7x366.txt` |
| 9 | **`(7, 312)`** | `0.661595420972` | **`0.661581951870`** | **`+1.346910e-05`** | `48.579367954672295911` | 1673 | `results/p2_d7/7x312.txt` |
| 10 | **`(7, 314)`** | `0.662290658947` | **`0.662280558847`** | **`+1.010010e-05`** | `48.525967638906964883` | 1639 | `results/p2_d7/7x314.txt` |
| 11 | **`(7, 316)`** | `0.663332152344` | **`0.663322953428`** | **`+9.198916e-06`** | `48.446188249386058240` | 1581 | `results/p2_d7/7x316.txt` |
| 12 | **`(7, 212)`** | `0.611962614152` | **`0.611955584704`** | **`+7.029448e-06`** | `52.268829642041145714` | 1094 | `results/p2_d7/7x212.txt` |
| 13 | **`(7, 325)`** | `0.665504583307` | **`0.665499516135`** | **`+5.067172e-06`** | `48.279263449266213577` | 1618 | `results/p2_d7/7x325.txt` |
| 14 | **`(7, 317)`** | `0.663597580717` | **`0.663592917690`** | **`+4.663027e-06`** | `48.425505962413669412` | 1599 | `results/p2_d7/7x317.txt` |
| 15 | **`(7, 364)`** | `0.670170636995` | **`0.670168019241`** | **`+2.617754e-06`** | `47.920125614877942187` | 1903 | `results/p2_d7/7x364.txt` |
| 16 | **`(7, 318)`** | `0.663816385482` | **`0.663813842524`** | **`+2.542958e-06`** | `48.408576902263834315` | 1581 | `results/p2_d7/7x318.txt` |
| 17 | **`(7, 322)`** | `0.665029616003` | **`0.665027566539`** | **`+2.049464e-06`** | `48.315480395111035562` | 1666 | `results/p2_d7/7x322.txt` |
| 18 | **`(7, 367)`** | `0.671529770134` | **`0.671527896172`** | **`+1.873962e-06`** | `47.815129276109026486` | 1898 | `results/p2_d7/7x367.txt` |
| 19 | **`(7, 368)`** | `0.671589583556` | **`0.671588063958`** | **`+1.519598e-06`** | `47.810480858285519507` | 1903 | `results/p2_d7/7x368.txt` |
| 20 | **`(7, 215)`** | `0.614265846451` | **`0.614265014927`** | **`+8.315243e-07`** | `52.101420971708758672` | 1110 | `results/p2_d7/7x215.txt` |
| 21 | **`(7, 204)`** | `0.601295919469` | **`0.601295776909`** | **`+1.425596e-07`** | `53.037273230392347692` | 1054 | `results/p2_d7/7x204.txt` |
| 22 | **`(7, 177)`** | `0.570051592256` | **`0.570051466490`** | **`+1.257656e-07`** | `55.246233640262432257` | 886 | `results/p2_d7/7x177.txt` |
| 23 | **`(7, 178)`** | `0.570228301539` | **`0.570228270372`** | **`+3.116653e-08`** | `55.233952328534987354` | 871 | `results/p2_d7/7x178.txt` |
| 24 | **`(7, 362)`** | `0.668965357603` | **`0.668965354413`** | **`+3.189908e-09`** | `48.012945759557960516` | 1848 | `results/p2_d7/7x362.txt` |

- Batch summary JSON: `results/p2_d7/summary_p2_d7.json`

---

## Verification & Reproducibility

To independently re-verify any coordinate file in 50-digit `mpmath`:
```bash
python3 verify_sc.py \
  results/goal_a/30x64.txt 30 64 \
  --posted-file data/coords/30/64.txt
```
