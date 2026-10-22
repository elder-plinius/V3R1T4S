# Receipts (real output of `sh verify-it-yourself/run_checks.sh`, run by the main session with V3R1T4S_Q15_DATA set to a local folder of the pinned inputs, each checked against inputs.sha256)

```
inputs: 41 files, 0 with a wrong sha256
1. Mockingbird-I1 mean BCFS recomputed 0.6050308536957327, official 0.6050308536957327: EXACT
2. FeVeT published predictions mean BCFS 0.6423935720824072
3. object mean BCFS 0.7114179305724276 over 18101 items (claimed 0.7114179305724276): EQUAL
   margin vs Mockingbird-I1 0.106387076877 (higher is better)
   margin vs FeVeT 0.069024358490 (higher is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```
exit status 0
