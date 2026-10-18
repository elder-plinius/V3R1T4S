# The record we beat (proportion 0.30, mean BLEU over the 10 surprise families)

| record | value (mean BLEU) | source | fetched (UTC) |
|---|---|---|---|
| our own earlier object (confirmed on mean NED at 0.30; package 2026-10-18-psmoros-634f2c35), the highest mean BLEU known at 0.30 | 0.6839233380559118 | earlier_object_predictions-0.30.tsv (this folder; byte-identical to that package's object) | n/a (our own file) |
| FeVeT (Wientzek 2025), published per-item predictions rescored with the official scorer | 0.6356571184958077 | https://github.com/TGH-2020/FeVeT at 31898c53bfffeef87265efa8a780b7be740162d1, results/predictions/reflex/FAMILY/s2s_reflex_0.30_predictions.tsv | repository HEAD checked unchanged 2026-10-18T12:59:33Z (NOVELTY skeptic) |
| Mockingbird-I1, best official system | 0.6058548112827981 | https://raw.githubusercontent.com/sigtyp/ST2022/03094435cba4293ce0eea383036cab78499ad50d/results/results-surprise-0.30.json | 2026-10-18T12:56:07Z (NOVELTY skeptic; identical to the pinned copy) |

Status source: https://github.com/sigtyp/ST2022, one plain GET at 2026-10-18T12:55:22Z (NOVELTY skeptic), HTTP 200, HEAD
03094435cba4293ce0eea383036cab78499ad50d (2022-05-27); the official results stand. Neither FeVeT nor Cognate Transformer
prints BLEU (panel/novelty.md). The page itself is not copied here.
