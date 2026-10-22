# Honesty gate (feigenbaum-constants-and-accumulation-point-digits)

status: CONFIRMED_PARTIAL
confirmed_scope: The coefficient file defines a quartic (z=4) Feigenbaum fixed point and its dominant eigenfunction satisfying the defining equations to about 1e-1092 and 1e-1100 at 31 points, with alpha_4 = -1.6903029714... and delta_4 = 7.2846862170... agreeing between 1070 and 1100 coefficients to 1085 and 1084 decimals (not proven correct to that many digits), exceeding the 49 digits of A195102 and the 331 and 325 proven digits of Thurlby.

## Gate notes
- Objects: 7 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The digit count is agreement between two resolutions of the same method plus residuals of the defining equations at high precision; it is not a rigorous error bound.
