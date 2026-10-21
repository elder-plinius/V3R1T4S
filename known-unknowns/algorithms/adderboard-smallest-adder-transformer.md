# AdderBoard: smallest transformer (fewest unique parameters) adding two 10-digit numbers

⚡ **Algorithms** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

AdderBoard (github.com/anadim/AdderBoard) is a public leaderboard for the smallest autoregressive transformer that adds two integers in [0, 9,999,999,999] with >= 99% accuracy on verify.py's fixed test (10 edge cases + 10,000 random pairs, seed 2025). Two boards: 'Trained weights' (learned by a generic algorithm) and 'Hand-coded weights' (constructive proofs). README at the last commit (07061de, 2026-03-26): trained leader 36 params, 100% (tbukic, 1-layer Qwen3-style, d=3, 1 head, head dim 4, ff 2, circular-arc embedding, K=rotation(Q), V=Q, tied O=Q^T); then 39 (99.91%), 41, 44, 45. Hand-coded leader 6* params (zcbtrak; the README footnote says strict counting gives 10 unique weight values, see issue #75), then 8, 10, 12, 20. IMPORTANT, checked live 2026-10-08: open issue #83 (lokimorty, 2026-03-11) claims a 28-parameter TRAINED model at 100% (d=3, 1h, hd=4, ff=2, signed-pair Q, tied K=V); on 2026-03-25 the maintainer wrote that code review confirms '28 parameters verified, no hidden buffers' and asked for the training pipeline before accepting it on the trained board; lokimorty posted training code the same day and the issue has had no further activity. Issue #76 (zcbtrak 6p 'trained' by coordinate descent) was rejected for the trained board. Other open claims: #89 warlockee 6p hand-coded, #85 Kiguli 7p hand-coded, #91/#90/#88 warlockee 49/58/62 trained, #74 lokimorty 47 trained. The repository has had no commits since 2026-03-26 (34 commits; README trained leader still 36). A new wave of unaccepted issue claims arrived 2026-10-14..19 (checked 2026-10-20): trained #98 Skyway1111 6p (d=2, 100% on verify.py), #103 cyz14 4 learned scalars (100% locally, architecture/counting review requested), #99 abgri 4 learned scalars in Skyway1111's d=2 family (99.71%, review request), #100 neilbauman21-hub 28p and 34p; hand-coded #97 Skyway1111 5p, #101 harishsg993010 5p, #102 cyz14 4 scalars, #100 4p (constructive) and 6p (strict). None is accepted. The effective (unaccepted) trained frontier is now 4-6 parameters, not 28, and the README still says 36.

## What counts as a win

Success means a submission file (build_model + add) that (1) passes the repository's verify.py (sha256 1135b7cd1e335a3b50121cc9ebe68fdacafa235ba82e1d4d65554408db009ec9, commit 07061de) with seed 2025 at >= 99% on all 10,010 cases, run on this Mac from the saved file; (2) is a trained model: weights produced by a generic learning algorithm (gradient-based or otherwise generic optimiser that would train any architecture on any dataset) from freshly sampled addition data, with the training script, seed and checkpoint saved and re-runnable; (3) satisfies the README rules re-read at verification time (at least one self-attention layer, generic autoregressive decode, no addition-specific control flow in forward or the generation loop); and (4) has a unique-parameter count, counted conservatively (every tunable or hand-set non-universal scalar counts, including hard-coded projection values and norm weights; fixed sinusoidal/RoPE tables with a conventional base are free), that is STRICTLY LESS (direction: min) than the smallest entry in the 'Trained Weights' table of https://raw.githubusercontent.com/anadim/AdderBoard/main/README.md re-fetched live immediately before claiming, AND strictly less than the conservatively re-counted parameter count of every trained claim in the live issue/PR list https://github.com/anadim/AdderBoard/issues (open or closed, including #83's 28) whose code the skeptic can download and which passes verify.py on this Mac. On 2026-10-20 the open trained claims go as low as 4 (#103, #99) and 6 (#98), so the bar is below those unless they fail the skeptic's re-run or conservative re-count. Submitting to the repository is NOT part of the target (would require the human's permission).

## Partial wins

- **p1:** A hand-coded (constructive) model passing verify.py at >= 99% whose unique-parameter count under conservative counting (every tunable or hand-set non-universal scalar counts, fixed RoPE/sinusoidal tables free) is strictly below the smallest entry of the live 'Hand-Coded Weights' table (counted the same conservative way, i.e. 10 for the current 6* leader) and below every hand-coded claim in the live issues (#89: 6, #85: 7, #97: 5, #101: 5, #102: 4, #100: 4 and 6) that passes verify.py, each re-counted conservatively.
- **p2:** A trained model (conditions 1-3 of the success criterion) whose conservatively counted unique-parameter count is strictly below the live README 'Trained Weights' leader (36 today) but not below the lowest verify.py-passing trained claim in the live issues (as low as 4 in #103 and #99 and 6 in #98, all unaccepted, on 2026-10-20): beats the published board, not the pending frontier.
- **p3:** A trained model with d_model = 2 (every width hyperparameter strictly smaller than the live trained leader's d=3/hd=4) that passes verify.py at >= 99%, with the training run reproducible from a saved seed on this Mac within 4 hours, even if its conservatively counted parameter count only ties the live leader.

## How a win is checked

Clone the repo at commit 07061de and confirm sha256 of verify.py matches the pin; run `python verify.py submissions/<file>.py` (CPU, PyTorch) and require QUALIFIED. Independently count parameters: enumerate every tensor and Python scalar used in forward, deduplicate tied tensors by identity, exclude only fixed sinusoidal/RoPE tables, count hard-coded non-universal values, and report the count. Read forward and add to confirm no carry logic or digit pairing in Python, that at least one attention layer with softmax over keys exists, and that decoding is generic token-by-token argmax. For the trained claim, re-run the saved training script with the saved seed and confirm it reaches a passing checkpoint, or load the saved checkpoint and confirm count and accuracy; also re-test on a different seed as a leakage sanity check. Re-fetch README and the issues list; download and run the code of every lower trained claim (today #83) and re-count it the same way. Under an hour on a 10-core Mac excluding any from-scratch retraining.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/anadim/AdderBoard>

## Sources

- <https://github.com/anadim/AdderBoard>
- <https://raw.githubusercontent.com/anadim/AdderBoard/main/README.md>
- <https://raw.githubusercontent.com/anadim/AdderBoard/main/verify.py>
- <https://raw.githubusercontent.com/anadim/AdderBoard/main/submission_template.py>
- <https://github.com/anadim/AdderBoard/issues>
- <https://github.com/anadim/AdderBoard/issues/75>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Reproduce the 36-parameter architecture (d=3, 1 head, hd=4, ff=2, circular-arc digit embedding, K = rotation(Q), V = Q, O = Q^T) and ablate: tie or drop the remaining norm scales and the FF bias, share the embedding and unembedding, replace learned scalars by fixed constants that the rules treat as architecture (RoPE period), each time retraining to 100%.
- Search architectures with d=2 and hd=2 (the hand-coded 6-12 param designs prove d=2 suffices for the computation) and train them with curriculum (reversed-digit format, carry-chain-heavy sampling) and many seeds in parallel on 10 cores; grokking-style long training with weight decay.
- Distillation from the hand-coded 6-10 parameter solutions: initialise a d=2 model near a hand-coded solution's basin and train with noise so the result is legitimately 'trained' (keep the training log; declare the init).
- Parameter-sharing tricks already accepted on the board (phase-tied Q, gate tying, norm folding) applied to the trained d=3 model, then re-train from scratch with the sharing structure fixed so the weights are learned rather than set.
- Automated search: evolutionary search over tying patterns and fixed-vs-learned scalar choices with a 10-minute training budget per candidate, selecting on verify.py accuracy.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A model that passes because add does digit pairing, carry handling or any problem-specific control flow in Python is disqualified by the rules even if verify.py says QUALIFIED; verify.py checks accuracy only.
- Undercounting: hard-coded non-universal scalars (e.g. a chosen RoPE period, a fixed Q projection matrix) are contested (issue #75); the skeptic counts conservatively, so a 'win' that depends on the lenient count is not a win here.
- Test-set leakage: training on the seed-2025 test pairs is trivial cheating; the training script must sample fresh random pairs and the skeptic re-tests on a different seed as a sanity check (not for the record, which is seed 2025).
- Nondeterministic training: a single lucky seed that cannot be reproduced is weak; save the checkpoint and seed so the result is checkable from the saved object.
- Stale README: last commit 2026-03-26, last issue 2026-04-15; issue #83 (28 params trained, maintainer-verified count, acceptance pending) is the real bar unless the skeptic cannot run it or it fails verify.py; a 'win' at 29-35 params is partial win p2 only.
- Generic-training rule: the maintainer rejected coordinate-descent 'training' of a hand-designed architecture (#76) and questioned #83 on the same ground; keep the training loop generic and document the init.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/algorithms/adderboard-smallest-adder-transformer.md
```

Already set up? Say `run V3R1T4S on adderboard-smallest-adder-transformer`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `adderboard-smallest-adder-transformer`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
