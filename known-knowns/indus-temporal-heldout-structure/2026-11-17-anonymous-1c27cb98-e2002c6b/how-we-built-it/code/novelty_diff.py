"""Novelty diff: the structure claim's prediction signature vs paragorth P1-P9 / Q1-Q14
(+ R1-R13, P4-credential, P5.x) and the published positional findings. Records a line of
reasoning per item. This is the artifact the NOVELTY panelist re-runs from scratch.

Output: output_novelty_diff.json (machine-readable) + a console table.
"""
import json, os, datetime

CLAIM = {
    "property": "object-class predictability (4-class Seal/Tablet/Pottery/Other; secondary 2-class "
                "Seal-vs-Tablet) of the sign sequence, measured as per-object accuracy",
    "protocol": "temporal held-out: model fitted ONLY on M77 (1977) corpus, scored on deduplicated "
                "post-1977 objects (CISI-numbered not-M77-attested + Dholavira + Lothal), seal-"
                "identity dedup, no held-out sequence/identity in training",
    "baselines": "tuned per-class Kneser-Ney 3-gram (same M77 data) AND a SIGIL-style class-"
                 "conditional position-unigram control (matched on unigram+length)",
    "test": "paired bootstrap p<0.001 (10,000, seed 20261117) at pooled AND Mohenjo-daro AND "
            "Harappa separately (n>=20 each)",
    "label": "structural finding (object-type predictability across the 1977 time split), "
             "never decipherment",
}

# Each comparator: what it actually claims/measures, and why the structure claim is NOT equivalent.
COMPARATORS = [
    {"id": "P1", "type": "re-derivation", "claims": "modal ending sign takes 28-45% of endings (in-sample, 1977-era corpus)",
     "not_equivalent": "a re-derivation of an in-sample ending-frequency statistic; not a held-out predictive property, not object-type, not a time split"},
    {"id": "P2", "type": "re-derivation", "claims": "terminal-class joint ending share 50-75% (in-sample)",
     "not_equivalent": "in-sample terminal-class frequency; no held-out, no object-type, no baselines-vs-control test"},
    {"id": "P3", "type": "falsifier", "claims": "zero-violation terminal-zone (R1) compliance 65-82%, >=25pts above within-text shuffle (in-sample)",
     "not_equivalent": "in-sample compliance of a rule; the null is a within-text shuffle, not a held-out + KN + SIGIL-control design; property is rule-compliance, not object-type prediction"},
    {"id": "P4", "type": "exploratory", "claims": "pre-enumerated stroke taxonomy contains >=1 family (>=3 members, monotone freq, final-rate<5%) (in-sample)",
     "not_equivalent": "stroke-family existence in-sample; not a temporal held-out prediction"},
    {"id": "P5", "type": "transfer", "claims": "double-terminal endings (distinct signs) 4-18% of eligible texts (in-sample)",
     "not_equivalent": "in-sample ending-pattern frequency; not object-type, not held-out"},
    {"id": "P6", "type": "re-derivation", "claims": "[initial-class]->[high-freq strictly-medial] bigram in corpus top10 (in-sample)",
     "not_equivalent": "in-sample bigram ranking; the structure claim is a multi-position object-type likelihood, not a single bigram"},
    {"id": "P7", "type": "re-derivation", "claims": "final-position entropy (Miller-Madow) lower than initial by >=0.3 bits (in-sample)",
     "not_equivalent": "in-sample positional-entropy gap (the published positional finding); the structure claim's property is object-type accuracy on held-out, and it is NOT the edge-entropy statistic that SIGIL shows is non-specific"},
    {"id": "P8", "type": "transfer", "claims": "foreign texts: elevated mean per-text surprisal under a home model (in-sample + foreign sub-corpus)",
     "not_equivalent": "surprisal on foreign (non-home) texts; a different property (language-likelihood) and a different population (foreign vs post-1977 home material)"},
    {"id": "P9", "type": "equivalence", "claims": "emblem-animal vs terminal-distribution weighted JSD <0.10 bits (in-sample; the emblem is independent)",
     "not_equivalent": "an emblem/text INDEPENDENCE statement (JSD small); the structure claim is object-type predictability, an orthogonal property (and the field-symbol lens p2 is the emblem angle, judged negative)"},
    {"id": "Q1", "type": "falsifier", "claims": "plain jar text-final >=60% / marked jar <=15% (in-sample, both transcriptions)",
     "not_equivalent": "in-sample jar-final rate; not object-type, not held-out"},
    {"id": "Q3", "type": "falsifier", "claims": "count paradigm starts at three (values 3-8 : 1-2 >= 8:1) (in-sample)",
     "not_equivalent": "in-sample numeral-value distribution before the tree; not object-type prediction"},
    {"id": "Q10", "type": "falsifier", "claims": "emblem independence: no sign-by-field-symbol pair survives BH-FDR 5% after dedup (in-sample, >=500 seals)",
     "not_equivalent": "the FALSIFIED emblem linkage (in-sample). The field-symbol lens (p2) is the closest relative and is judged NEGATIVE; the object-type claim does not involve the emblem at all"},
    {"id": "Q11", "type": "falsifier", "claims": "seals and sealings do not co-locate (>=80% different site) (in-sample)",
     "not_equivalent": "a co-location rate; not object-type, not a time split"},
    {"id": "Q12", "type": "falsifier", "claims": ">=20% of distinct seal texts have a one-substitution twin, differing before the ending (in-sample)",
     "not_equivalent": "in-sample twin rate (the ligature lens p3 is the closest relative, judged negative on the held-out); not object-type"},
    {"id": "Q13", "type": "falsifier", "claims": "stability over time: jar-final and opener rates differ <=10pts between earliest/latest dated periods (in-sample, dated sub-corpora)",
     "not_equivalent": "the closest comparator — a TIME effect — but it measures in-sample rate STABILITY (a difference bound) across dated periods of the 1977-era corpus, not a predictive held-out accuracy beating two baselines. Different statistic (|rate_early - rate_late| <= bound) and different direction (we predict, they bound). NOT equivalent."},
    {"id": "Q14", "type": "falsifier", "claims": "blind validator for any proposed dictionary (any sign-to-sound key must beat scrambled + value-shuffled nulls)",
     "not_equivalent": "a DICTIONARY (sound-key) validator; the structure claim is explicitly NOT a decipherment/dictionary (object-type, not sign-to-sound)"},
    {"id": "R1-R13", "type": "transfer (new-data)", "claims": "repetition avoidance, foreign person-sign openers, no home opener abroad, marker exclusivity, closed title slot, voucher values (all frozen for NEW data, in-sample-derived)",
     "not_equivalent": "frozen new-data predictions about specific sign/position properties (repetition, openers, co-occurrence); none is object-type prediction with a time split + dual baselines + site replication"},
    {"id": "Mahadevan_1977", "type": "published positional", "claims": "the 1977 concordance/tables: sign positions, frequency, site/object tabulation (in-sample, 1977)",
     "not_equivalent": "descriptive 1977-era tables; no predictive held-out model, no 2026 post-1977 test, no KN/SIGIL baselines"},
    {"id": "Rao_2009_Yadav_2010", "type": "published positional", "claims": "structural statistics on the EBUDS subset (reciprocity, connectivity, beginner/ender asymmetry, non-randomness) (in-sample)",
     "not_equivalent": "in-sample corpus-level statistics (the kind SIGIL shows is non-specific); not a temporal predictive object-type property"},
    {"id": "Kriger_Hunt_2026", "type": "published positional", "claims": "179 MD unicorn seals: 98.3% uniqueness, edge-peaked positional entropy, stroke numerals 15.4% penultimate, digit-2 = 66.9% of numerals, 8 one-substitution pairs; 'registration codes / credit instruments'",
     "not_equivalent": "in-sample on a 179-seal CISI-vol-3 sub-corpus; the properties are uniqueness / edge-entropy / numeral-position (all in the non-specific class per 2608.02999) — none is a temporal M77->post-1977 predictive object-type accuracy beating a tuned KN + SIGIL control. The 'credit instrument' reading is an interpretation, not the predictive structural claim."},
    {"id": "arXiv_2608.02999_SIGIL", "type": "published non-specificity", "claims": "the standard Indus statistics (uniqueness, directional asymmetry, positional/lexical/entropy/predictive/network measures) are reproduced by a non-linguistic generative emblem system (SIGIL); they cannot on their own establish encoded speech",
     "not_equivalent": "this is the DESIGN RATIONALE, not a competitor: it tells us the claim must be a genuinely predictive temporal property that beats a non-linguistic control. The structure claim is exactly that (a predictive held-out object-type property, dual-baseline, multi-site). It is the class SIGIL does NOT establish (SIGIL is the control's model, not a temporal object-type prediction)."},
]

def main():
    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "claim": CLAIM,
        "verdict_per_comparator": [
            {"id": c["id"], "type": c["type"], "claims": c["claims"], "equivalent": False,
             "reason": c["not_equivalent"]} for c in COMPARATORS
        ],
        "summary": "The structure claim (temporal M77->post-1977 object-type predictability, dual-baseline, "
                   "multi-site, paired-bootstrap) is not equivalent to any P1-P9, Q1-Q14, R1-R13, "
                   "Mahadevan 1977, Rao/Yadav 2009-10, or Kriger-Hunt 2026 property, and is the class "
                   "the SIGIL paper (2608.02999) establishes as NOT covered by the standard statistics.",
        "closest_comparator": "Q13 (stability over time) — a time effect, but an in-sample rate-bound, "
                              "not a predictive dual-baseline held-out accuracy; and P7/K-H edge-entropy "
                              "(the non-specific positional class, which the claim deliberately avoids).",
    }
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output_novelty_diff.json"), "w"), indent=2)
    for c in COMPARATORS:
        print(f"- {c['id']} ({c['type']}): NOT equivalent — {c['not_equivalent'][:100]}")
    print("\nSummary:", out["summary"])

if __name__ == "__main__":
    main()
