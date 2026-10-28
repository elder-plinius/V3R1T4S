# Reproduce Skeptic Report — `card-guessing-yes-no-feedback-exact`

context: subagent (fresh invocation)
target_id: card-guessing-yes-no-feedback-exact
review_utc: 2026-10-28T18:45:00Z

## Reproduction Audit

1. **Independent Verification of Calibration Against Published Table 3**:
   - Diaconis, Graham, and Spiro ("Guessing about guessing", *American Mathematical Monthly* 129(7) (2022) 607–622, arXiv:2012.04019), Table 3 lists numerical values for two-copy decks ($m = 2$) for $n = 2..10$.
   - Re-evaluated in two independent clean-room implementations (compiled Rust engine and pure Python standard library solver):
     - $n = 2$: $17 / 6 \approx 2.833333$ vs Table 3: $2.8333$ (diff: $0.000033$)
     - $n = 3$: $271 / 90 \approx 3.011111$ vs Table 3: $3.0111$ (diff: $0.000011$)
     - $n = 4$: $1279 / 420 \approx 3.045238$ vs Table 3: $3.0452$ (diff: $0.000038$)
     - $n = 5$: $57583 / 18900 \approx 3.046720$ vs Table 3: $3.0467$ (diff: $0.000020$)
     - $n = 6$: $1136743 / 374220 \approx 3.037633$ vs Table 3: $3.0376$ (diff: $0.000033$)
     - $n = 7$: $206528731 / 68108040 \approx 3.032369$ vs Table 3: $3.0323$ (diff: $0.000069$)
     - $n = 8$: $61829276953 / 20432412000 \approx 3.026039$ vs Table 3: $3.0260$ (diff: $0.000039$)
     - $n = 9$: $6298009733989 / 2084106024000 \approx 3.021924$ vs Table 3: $3.0219$ (diff: $0.000024$)
     - $n = 10$: $170757866939041 / 56568592080000 \approx 3.018598$ vs Table 3: $3.0186$ (diff: $0.000002$)
   - Every single value matches Table 3 well within the required $0.0001$ calibration threshold.

2. **Reproduction of Target Values ($n = 11..16$)**:
   - Both Lens 1 and Lens 2 independently evaluate the inclusion-exclusion polynomial convolution and integer Bellman recursion, agreeing bit-for-bit across all computed terms:
     - $n = 11$: $137912544707079557 / 45735706696680000 \approx 3.0154239360882285$
     - $n = 12$: $228254911260131056513 / 75738330289702080000 \approx 3.0137304372442206$
     - $n = 13$: $3901622163101296907981 / 1295524070744904000000 \approx 3.0116168824697573$
     - $n = 14$: $28008675189200821587458897 / 9304453876089900528000000 \approx 3.0102438640892242$
     - $n = 15$: $811893265752470943966781067 / 269829162406607115312000000 \approx 3.0089159322557744$
     - $n = 16$: $287519620950287971428538054033 / 95596617538340806567680000000 \approx 3.0076338300878991$
   - All fractions are strictly irreducible ($\gcd(\text{numerator}, \text{denominator}) = 1$).
   - Values satisfy Luo's rigorous analytical bounds ($2.91 \le P^+_{2,n} \le 2(e-1) \approx 3.4366$) and decrease strictly monotonically for $n \ge 5$ toward 3.

3. **Certificate Integrity & Persistence Audit**:
   - Executed `verify-it-yourself/run_checks.sh`, which confirms all values in `object/values.txt`.
   - Verified that all $27,118,527$ reachable failure transitions across $n \le 16$ satisfy persistence (label with incremented counter remains in the optimal set).

pass: true
