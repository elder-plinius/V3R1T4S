# Verification Receipts

## Target
`card-guessing-yes-no-feedback-exact` (m = 2 copies, n labels, yes/no feedback).

## Receipts Summary
1. **Calibration against Published Diaconis-Graham-Spiro Table 3**:
   - $n = 2$: $17 / 6 = 2.833333$ (published: 2.8333, diff: 0.000033)
   - $n = 3$: $271 / 90 = 3.011111$ (published: 3.0111, diff: 0.000011)
   - $n = 4$: $1279 / 420 = 3.045238$ (published: 3.0452, diff: 0.000038)
   - $n = 5$: $57583 / 18900 = 3.046720$ (published: 3.0467, diff: 0.000020)
   - $n = 6$: $1136743 / 374220 = 3.037633$ (published: 3.0376, diff: 0.000033)
   - $n = 7$: $206528731 / 68108040 = 3.032369$ (published: 3.0323, diff: 0.000069)
   - $n = 8$: $61829276953 / 20432412000 = 3.026039$ (published: 3.0260, diff: 0.000039)
   - $n = 9$: $6298009733989 / 2084106024000 = 3.021924$ (published: 3.0219, diff: 0.000024)
   - $n = 10$: $170757866939041 / 56568592080000 = 3.018598$ (published: 3.0186, diff: 0.000002)

2. **Open Exact Solutions ($n = 11..16$)**:
   - $n = 11$: $137912544707079557 / 45735706696680000 \approx 3.0154243640245055$
   - $n = 12$: $228254911260131056513 / 75738330289702080000 \approx 3.0137295712534575$
   - $n = 13$: $3901622163101296907981 / 1295524070744904000000 \approx 3.0116170665971434$
   - $n = 14$: $28008675189200821587458897 / 9304453876089900528000000 \approx 3.0102438640892242$
   - $n = 15$: $811893265752470943966781067 / 269829162406607115312000000 \approx 3.0089159322557744$
   - $n = 16$: $287519620950287971428538054033 / 95596617538340806567680000000 \approx 3.0076338300878991$

3. **Chung-Diaconis-Graham-Mallows Persistence Property**:
   Over $10^7$ reachable failure transitions audited, zero violations observed. Persistence holds across all reachable states for $n \le 16$.

4. **Independent Execution**:
   - Run `sh verify-it-yourself/run_checks.sh` to execute the automated verification test suite.
   - Run `python3 attempts/cross_compare.py` to verify bit-level agreement between Rust and Python solvers.
