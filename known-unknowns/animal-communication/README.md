# 🐋 Animal communication

Whale, dolphin, elephant and other animal signals: structure, context and prediction problems scored on held-out public recordings; never a translation.

**4 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★★☆ | [BEANS-Next in-context call-type matching: beat NatureLM-audio T4 on both the giant otter…](beans-next-few-shot-call-type-matching.md) | standard | laptop-hours (only the 400 Otters and Crows examples are needed, five short clips each; the full Hugging Face test split has 37,718 examples) |
| ★★★☆☆ | [OpenWhistle bottlenose dolphin whistles: beat the best published session-held-out macro-F…](openwhistle-dolphin-signature-whistle-benchmark.md) | harvest | laptop-hours for frozen-encoder probes, laptop-days for end-to-end fine-tuning (a GPU helps); classification set 4.64 GB and detection set about 237 MB of Parquet audio on Hugging Face, optional 114-hour unlabelled pretraining corpus |
| ★★☆☆☆ | [African elephant name-like rumbles: predict who a call is addressed to better than Pardo…](elephant-rumble-receiver-identity-beyond-caller.md) | standard | laptop-minutes to laptop-hours (Dryad deposit of 42.3 MB: acoustic feature tables and contours for 469 calls, no audio) |
| ★★☆☆☆ | [MOONSHOT - Sperm whale codas: frozen next-coda predictions on held-out DTag recordings th…](sperm-whale-next-coda-beyond-first-order.md) | moonshot | laptop-minutes to laptop-hours (two public CSV files of about 0.5 MB and 0.75 MB in one GitHub repository) |

← [All categories](../README.md)
