# Prospective Pre-Registration & 7-Hypothesis Ledger (`PREREG.md`)

- `target_id`: `nist-aes-circuit-records`
- `milestones_targeted`: `p3 ([Inv]MixColumns strict depth-bounded XOR improvement), p4 (Route 1: [Inv]S-box zero-NOT minimum gate depth GD <= 10), CSRC Wish-List (c) (G <= 110 at GD <= 14), p1, p2, and p4 Route 2`
- `stage0_recon_frozen_utc`: `2026-11-17T17:25:00Z`
- `gate_model`: `strict 2-input {XOR} for [Inv]MixColumns (x0:x31 -> y0:y31) and strict 2-input {AND, XOR, XNOR} for [Inv]S-box (U0:U7 -> S0:S7 / x0:x7 -> y0:y7) with zero NOT gates, zero constants, zero self-inputs, and zero dead gates`
- `ex_ante_hypotheses_resolved`: `15 / 15 (Open: 0; 4 pre-registered hypothesis wins [L-NACR-001 -> p4 GD=10 InvS-box, L-NACR-005 -> p3 92@10 InvMixColumns, L-NACR-011 -> T8-GL4 & T9 exact obstructions, L-NACR-015 -> T10 & T11 exact obstructions] + 11 falsified search hypotheses [L-NACR-002..004, L-NACR-006..010, L-NACR-012..014]; Brier calibration = 0.147)`
- `null_test`: `not needed because deterministic algebraic evaluation checks 100% of the 256-input S-box domain and all 32 GF(2) InvMixColumns basis vectors with zero statistical variance; adversarial 1-gate corruption (verify.py --corrupt) is enforced with exit code 1`
