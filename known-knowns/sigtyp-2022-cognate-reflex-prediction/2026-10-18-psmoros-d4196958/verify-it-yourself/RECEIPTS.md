# Receipts (real output of `sh verify-it-yourself/run_checks.sh`, run by the main session with V3R1T4S_Q15_DATA set to a local folder of the pinned inputs, each checked against inputs.sha256)

```
inputs: 41 files, 0 with a wrong sha256
1. Mockingbird-I1 mean BLEU recomputed 0.6058548112827981, official 0.6058548112827981: EXACT
2. FeVeT published predictions mean BLEU 0.6356571184958077
2. earlier object the-record-we-beat/earlier_object_predictions-0.30.tsv mean BLEU 0.6839233380559118 (stated 0.6839233380559118): EQUAL
3. object mean BLEU 0.6874377388475998 over 11586 items (claimed 0.6874377388475998): EQUAL
   margin vs Mockingbird-I1 0.081582927565 (higher is better)
   margin vs FeVeT 0.051780620352 (higher is better)
   margin vs the-record-we-beat/earlier_object_predictions-0.30.tsv 0.003514400792 (higher is better)
4. rebuilt official-format files equal to the frozen ones: 10 of 10
PASS
```
