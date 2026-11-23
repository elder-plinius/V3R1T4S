# Baseline record (p3)

No published baseline exists for this exact setup (all 8,719 rows, CodaType tokens, rewritten-Date + Unit streams,
the bank's date folds). Sinha and Chavan's Dominica numbers use a different public coda set (1,483 to 1,501 codas)
and other references; the bank calls them context. The partial win defines the reference: "a smoothed bigram over
the same tokens". It is computed here from the definition (code/dompipe.py: bigram_P, ref_fit): counts over all
consecutive pairs of the training-fold streams, additive alpha from the R1 grid by inner leave-one-training-fold-out
CV (alpha 0.3 in every fold), same data, folds, scored set and metric as the model. Held-out bits per fold 1.5077,
1.7059, 1.8709, 1.8484, 1.5941; pooled 1.7179 over 8,501 codas (result/p3_summary.json).
