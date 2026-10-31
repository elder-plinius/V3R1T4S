# Null Model Control Test (`indus-temporal-heldout-structure`)

controls: 400
best_control: 0.096221
real: 0.200482
command: sh verify-it-yourself/run_checks.sh
real_beats_all_controls: yes

## Summary of 400 SIGIL Matched-Null Controls

- **Number of independent synthetic controls**: `400` (`seed = 1..400`)
- **Generator**: `generate_matched_null_corpus` (`adversarial_null_model.py`), matching `M77` length, initial-sign, final-sign, and unigram distributions
- **Held-out evaluation tokens**: `3731` tokens across `999` deduplicated post-1977 inscriptions
- **Control accuracy median (IQR)**: `0.088984` (`IQR = 0.002948`)
- **Control accuracy mean (SD)**: `0.089058` (`SD = 0.002328`)
- **Best control accuracy across all 400 runs**: `0.096221`
- **Real frozen `M77-CLSS` accuracy**: `0.200482` (`748 / 3731`)
- **Tuned `KN3-Left` baseline accuracy**: `0.147146` (`549 / 3731`, paired-bootstrap $p = 0.0001$ pooled, `0.0001` Mohenjo-daro, `0.0001` Harappa)
- **Tuned `KN3-Bidir` baseline accuracy**: `0.188957` (`705 / 3731`, paired-bootstrap $p = 0.0001$ pooled, `0.0019` Mohenjo-daro, `0.0147` Harappa)
- **Tuned `KN3-BlanketF` baseline accuracy**: `0.194586` (`726 / 3731`, paired-bootstrap $p = 0.0048$ pooled, `0.2988` Mohenjo-daro, `0.0188` Harappa)
- **Partial Win `p3` (10,000 frequency-matched random permutations, `seed = 0`)**: `30` shared parallel frames on the 25 frozen `M77` telescoping pairs vs null mean `7.6427` (`SD = 3.1291`, `max = 23`, `0 / 10,000` controls $\ge 30$, $p = 0.0001 < 0.001$)
