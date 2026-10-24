# Honesty Gate Verdict (`voynich-generator-heldout-fingerprints` — Partial Win `p2`)

status: CONFIRMED_PARTIAL
confirmed_scope: Partial win p2 is achieved by the 152-entry hand-executable cipher VBCLC-152 (`claim/vbclc.py`, `claim/HAND_PROCEDURE.md`) using 1 per-folio state bit, which passes all four signatures of arXiv:2604.19762 jointly on 200/200 streams (20 period Latin and Italian plaintexts x 10 seeds) per cell across Currier A and Currier B separately on both ZL3b-n and IT2a-n (as well as RF1b-e), where the published slot and Cardan-grille generators fail.

## Honesty Gate 8-Item Checklist
1. **All three panelists returned `pass: true` without hedging**: `YES` (`panel/reproduce.md`, `panel/novelty.md`, `panel/criterion.md` all end with `pass: true` from independent `subagent` contexts).
2. **`REPRODUCE` got the exact same numbers from scratch**: `YES` (independent checker written before reading `claim/verify_p2_claim.py`, executed on `veritas` in `job 2903`, reproducing all 6 manuscript cells to `< 1e-6`, verifying all 1,200 saved streams and 400-control nulls, and verifying 176 fresh streams across all 20 period plaintexts and unseen seeds).
3. **`NOVELTY` confirmed the live status source and benchmark at a timestamp `< 6h` old and the result is strictly better**: `YES` (`https://www.voynich.nu/transcr.html` and `https://arxiv.org/abs/2604.19762` fetched at `2026-10-24T15:15:37Z` and `2026-10-24T15:15:38Z`, HTTP 200; `VBCLC-152` achieves `200/200 = 100.0%` joint pass per cell across `A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, `B/RF1b-e`, strictly beating the published slot generator [`0%` on B, `10%` on A], Cardan-grille generator [`0%`], and unmodified Naibbe [`0%` fixed/strict-Zipf]).
4. **`CRITERION` found no stretched definition or hidden quantifier**: `YES` (152 table entries `<= 200`, 1 per-folio state bit `<= 1`, written hand procedure in `claim/HAND_PROCEDURE.md`, 20 period Latin and Italian plaintexts x 10 seeds = 200 streams per cell, joint pass on all 4 signatures across Currier A and B on both `ZL3b-n` and `IT2a-n`).
5. **No sampling presented as exhaustive, no capped search as an exclusion, no probable prime as a proof**: `YES`.
6. **No table access used browser User-Agents, cookies, bypasses, or retries after 403/429**: `YES`.
7. **Only one object/claim is bundled**: `YES` (`VBCLC-152` for partial win `p2`).
8. **For cipher/script targets, the real output beat all 400 null controls**: `YES` (`400/400` controls beaten across `A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a` on `delta_mi_10chunk`, `es_x_delta_mi`, and `excess_edge_mi`).
