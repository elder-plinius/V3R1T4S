# Lead agent's additional checks (Andy, 2026-11-18): author evidence, NOT reviewed by the panel

Run from the run folder with Python 3 and NumPy (OPENBLAS_NUM_THREADS=1). Outputs are saved next to each script.

1. **Independent re-derivation from the bank's criterion alone** (written without reading the authors' code):
   - `models_vs_r1.py claim/data/sperm-whale-dialogues.csv`: same 3,418 scored positions. Dirichlet-backoff n-grams with inner-CV smoothing: order 2 gains 0.242 and order 3 gains 0.266 bits per coda over my own R1 (2.787); a repetition-aware first-order model gains only 0.054, so runs of one repeated token do not explain the gain.
   - `criterion_and_bootstrap.py ...`: both criterion conditions with my own models: gain over R1 0.266 (95% paired interval over 188 recordings 0.223 to 0.319); gain over a well-tuned order-1 twin (2.772 bits, better than R1) 0.251 (0.208 to 0.311).
   - `folds_and_recordings.py ...`: my model's gain over R1 is 0.229 to 0.321 in every fold.
2. **On the frozen claim object** (`frozen_object_folds_and_recordings.py claim/output`): reproduces the claimed pooled scores to nine digits; gain over R1 0.174 to 0.325 and over the twin 0.182 to 0.415 in every one of the five folds; 137 of 188 recordings gain over R1 and 146 over the twin; the five most-helped recordings supply about a third of the summed gain, and without them the gain is still 0.221 bits over R1 and 0.265 over the twin.

What these do not show: anything beyond the bank's fixed benchmark (dataset, tokens, folds, R1, twin). The panel's verdicts are in panel/; these checks only add evidence a reader may want.
