# The published evaluation reproduced (p3)

p3 is a reproduction of published numbers, not a new record. The cells reproduced, read from the published evaluation:

| item | value |
|---|---|
| status source | https://github.com/KITmetricslab/hospitalization-nowcast-hub (fetched 2026-11-13T04:20:41Z, HTTP 200, page sha256 be376bf395e29d75a812ceac97bd5ce1364ef9ea7844cd6fb9a341a375127806; re-fetched by the NOVELTY skeptic 2026-11-13T04:53:55Z, HTTP 200) |
| published tables | https://raw.githubusercontent.com/dwolffram/hospitalization-nowcast-hub-evaluation/main/data/scores/wis_national.csv, wis_states.csv, wis_age.csv (fetched 2026-11-13 between 04:23:3x and 04:23:56Z, HTTP 200; re-fetched by the REPRODUCE skeptic 05:02:10-05:02:16Z, HTTP 200, byte-identical) |
| sha256 of the tables (not included) | national 78aeb28ad32c120a3f873eb5e47fff092296b98661cdcb6e7d3ba8eed0c52f37; states 2cde62e4394a6f20edfdd51dc8133fe310a3f1a4a76d2edb9621e5caa2f56dd9; age 88936f4c3c7e895f7ec89645bf2328231d7354ec66e5412414a115e1c21fe022 |
| paper | Wolffram et al. 2023, PLoS Comput Biol 19:e1011394, Fig 7; https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10446237/fullTextXML (fetched 2026-11-13T04:21:51Z, HTTP 200) |

Extracted cells (mean WIS, count scale, truth version 2022-08-08, period 2021-11-22..2022-04-29):

| level | Epiforecasts | ILM | KIT | FrozenBaseline | LMU | MeanEnsemble | MedianEnsemble | RIVM | RKI | SU | SZ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| national | 423.0878 | 142.6290 | 256.1102 | 1572.7173 | 465.8457 | 259.5945 | 319.9148 | 289.0506 | 382.9351 | 382.4496 | 521.6907 |
| states | 26.4361 | - | 21.9668 | 98.4124 | 29.4011 | 22.1865 | 23.7621 | 24.3368 | 30.7078 | 25.4388 | 36.5054 |
| age | 64.8460 | 29.2992 | 44.0025 | 262.3707 | 76.7803 | 41.4840 | 50.3725 | 46.2835 | - | 59.5096 | 87.4256 |

(Full precision in verify-it-yourself/check_p3.py, PUB.)
