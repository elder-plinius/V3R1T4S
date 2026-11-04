# PREREG.v2 (frozen 2026-10-19T19:41Z; still before any model was scored on any test split)
Reason: measured MACE-from-scratch cost on this CPU (4 threads, Mo: about 18 s/epoch for the small model; the 107-atom Cu/Ni cells are about 2.7x slower), so the 8 h budget cannot cover all six elements in the original order.
Changes (process only; PREREG.md otherwise stands, including the metric, the val rule, the success rule and no test peeking):
1. Element order becomes Mo, Li, Si, Ge, then Ni, Cu (cheap cells first, 107-atom cells last).
2. Selection phase: two configurations per element run in parallel at 2 threads each: A = 32 channels, r_max 5.0; B = 16 channels, r_max 4.5; both L=1 (hidden NxOe+Nx1o), max_ell 2, correlation 3, 2 interactions, float32 training, 120 epochs, Adam lr 0.01 with plateau decay, EMA 0.99, forces weight 100, energy weight 1. The config with the lower val force MAE (best EMA checkpoint on val) wins.
3. Final phase uses the winner with a fixed epoch count (the winning run's epoch count), seeds 1, 2, 3 on all train ids; ensemble = mean of the 3 seeds' forces; inference in float64 from the saved models.

## PREREG.v3 addendum (20:08Z, val-only information used: B reached val MAE 0.1x and train≈val RMSE, i.e. underfit at only ~2000 optimizer steps)
Configs A (killed unfinished at epoch ~50) and B (finished) at batch 10 / lr 0.01 are superseded. Selection now compares C = 16 channels, r_max 4.5 and D = 32 channels, r_max 4.5, both batch size 3, lr 0.005, 150 epochs, otherwise identical. Still val-only; test untouched.

## PREREG.v3 addendum 2 (22:50Z; before any Li/Si/Ge/Ni/Cu test scoring; Mo test scored once at 22:50Z)
Compute is the limit. For elements after Mo and Li the config pair C/D may be reduced to C alone if the remaining wall clock cannot pay for D; the choice is made from val only and is stated in each package.
