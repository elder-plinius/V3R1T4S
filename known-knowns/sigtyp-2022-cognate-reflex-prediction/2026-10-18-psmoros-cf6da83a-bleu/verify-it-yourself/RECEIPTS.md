# Receipts (real output of `sh verify-it-yourself/run_checks.sh`, run by the main session with V3R1T4S_Q15_DATA set to a local folder of the pinned inputs, each checked against inputs.sha256)

```
inputs: 41 files, 0 with a wrong sha256
1. Mockingbird-I1 mean BLEU recomputed 0.5337187296541888, official 0.5337187296541888: EXACT
2. FeVeT published predictions mean BLEU 0.5768215755932388
3. object mean BLEU 0.6520222200978466 over 18101 items (claimed 0.6520222200978466): EQUAL
   margin vs Mockingbird-I1 0.118303490444 (higher is better)
   margin vs FeVeT 0.075200644505 (higher is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```
exit status 0
