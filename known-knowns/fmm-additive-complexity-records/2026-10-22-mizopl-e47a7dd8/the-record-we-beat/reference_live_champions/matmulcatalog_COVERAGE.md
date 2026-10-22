# Matrix-Multiplication Algorithm Coverage

Auto-generated from `src/main/resources/schemes/` + `KnownAlgorithmCatalog`.
Re-run via `java … CoverageMatrixGenerator`.

Cell legend:

- **✓ r=N** — verified scheme on disk at `src/main/resources/schemes/`. N is the multiplication count.
- **📄 r=N** — known from the literature, no scheme file yet.
- **—** — not tracked at all.

`+N adds` is the addition count (`nz(U)+nz(V)+nz(W) − 2r − n·p`), shown for verified schemes only.

Formats are grouped by `max(n,m,p)` (the **section number**), then sorted with
components in ascending order. Permutations of `⟨n,m,p⟩` are merged (the rank is
invariant under axis permutation).

## Section 2 — max-dimension = 2

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,2⟩` | **✓ 7** Alphatensor-F2 | **✓ 7** Alphatensor-Z | **📄 7** Strassen | **📄 7** Strassen | **7** in F₂, R/Q/Z, C, commutative | +24 | • 1969 Strassen r=7 (R/Q/Z)<br>• 1969 Strassen r=7 (F₂)<br>• 1969 Strassen r=7 (C)<br>• 1969 Strassen r=7 (commutative) |

## Section 3 — max-dimension = 3

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,3⟩` | **✓ 11** Alphatensor-F2 | **✓ 11** Alphatensor-Z | — | — | **11** in F₂, R/Q/Z | +31 | • 1971 Hopcroft–Kerr r=11 (R/Q/Z) |
| `⟨2,3,3⟩` | **✓ 15** Alphatensor-F2 | **✓ 15** Alphatensor-Z | — | — | **15** in F₂, R/Q/Z | +71 | • 1973 Hopcroft–Kerr / Pan r=15 (R/Q/Z) |
| `⟨3,3,3⟩` | **✓ 23** Alphaevolve [Z→F₂] | **✓ 23** Alphaevolve | — | — | **23** in F₂, R/Q/Z | +95 | • 1976 Laderman r=23 (R/Q/Z)<br>• 1976 Laderman r=23 (F₂) |

## Section 4 — max-dimension = 4

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,4⟩` | **✓ 14** Alphatensor-F2 | **✓ 14** Alphatensor-Z | — | — | **14** in F₂, R/Q/Z | +69 | — |
| `⟨2,3,4⟩` | **✓ 20** Alphatensor-F2 | **✓ 20** Alphatensor-Z | — | — | **20** in F₂, R/Q/Z | +90 | — |
| `⟨2,4,4⟩` | **✓ 26** Alphatensor-F2 | **✓ 26** Alphatensor-Z | — | — | **26** in F₂, R/Q/Z | +149 | — |
| `⟨3,3,4⟩` | **✓ 29** Alphatensor-F2 | **✓ 29** Alphatensor-Z | — | — | **29** in F₂, R/Q/Z | +141 | — |
| `⟨3,4,4⟩` | **✓ 38** Alphatensor-F2 | **✓ 38** Alphatensor-Z | — | — | **38** in F₂, R/Q/Z | +216 | — |
| `⟨4,4,4⟩` | **✓ 47** Alphatensor-F2 | **✓ 49** Alphatensor-Z | **✓ 48** Alphaevolve | — | **47** in F₂ | +340 | • 1969 Strassen² (recursive) r=49 (R/Q/Z)<br>• 2022 AlphaTensor r=47 (F₂)<br>• 2025 AlphaEvolve r=48 (C) |

## Section 5 — max-dimension = 5

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,5⟩` | **✓ 18** Alphatensor-F2 | **✓ 18** Alphatensor-Z | — | — | **18** in F₂, R/Q/Z | +71 | — |
| `⟨2,3,5⟩` | **✓ 25** Alphatensor-F2 | **✓ 25** Alphatensor-Z | — | — | **25** in F₂, R/Q/Z | +118 | — |
| `⟨2,4,5⟩` | **✓ 33** Alphatensor-F2 | **✓ 32** Alphaevolve | — | — | **32** in R/Q/Z | +190 | — |
| `⟨2,5,5⟩` | **✓ 40** Alphatensor-F2 | **✓ 40** Alphatensor-Z | — | — | **40** in F₂, R/Q/Z | +256 | — |
| `⟨3,3,5⟩` | **✓ 36** Alphatensor-F2 | **✓ 36** Alphatensor-Z | — | — | **36** in F₂, R/Q/Z | +230 | — |
| `⟨3,4,5⟩` | **✓ 47** Alphatensor-F2 | **✓ 47** Alphatensor-Z | — | — | **47** in F₂, R/Q/Z | +287 | — |
| `⟨3,5,5⟩` | **✓ 58** Alphatensor-F2 | **✓ 58** Alphatensor-Z | — | — | **58** in F₂, R/Q/Z | +413 | — |
| `⟨4,4,5⟩` | **✓ 61** Alphaevolve [Z→F₂] | **✓ 61** Alphaevolve | — | — | **61** in F₂, R/Q/Z | +455 | — |
| `⟨4,5,5⟩` | **✓ 76** Alphatensor-F2 | **✓ 76** Alphatensor-Z | — | — | **76** in F₂, R/Q/Z | +549 | • 2022 AlphaTensor r=76 (F₂) |
| `⟨5,5,5⟩` | **✓ 93** Alphaevolve [Z→F₂] | **✓ 93** Alphaevolve | — | — | **93** in F₂, R/Q/Z | +846 | • 2022 AlphaTensor r=96 (F₂) |

## Section 6 — max-dimension = 6

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,6⟩` | **✓ 21** Alphatensor-Z [Z→F₂] | **✓ 21** Alphatensor-Z | — | — | **21** in F₂, R/Q/Z | +54 | — |
| `⟨2,3,6⟩` | — | **✓ 30** Dronperminov-cr81_cn116_ZT_reduced | — | — | **30** in R/Q/Z | — | — |
| `⟨2,4,6⟩` | **✓ 39** Dronperminov-ZT [Z→F₂] | **✓ 39** Dronperminov-ZT | — | — | **39** in F₂, R/Q/Z | +215 | — |
| `⟨2,5,6⟩` | **✓ 47** Alphaevolve [Z→F₂] | **✓ 47** Alphaevolve | — | — | **47** in F₂, R/Q/Z | +332 | — |
| `⟨2,6,6⟩` | **✓ 56** Dronperminov-ZT [Z→F₂] | **✓ 56** Dronperminov-ZT | — | — | **56** in F₂, R/Q/Z | +535 | — |
| `⟨3,3,6⟩` | **✓ 42** Dronperminov-ZT [Z→F₂] | **✓ 42** Dronperminov-ZT | — | — | **42** in F₂, R/Q/Z | +367 | — |
| `⟨3,4,6⟩` | **✓ 54** Dronperminov-ZT [Z→F₂] | **✓ 54** Alphaevolve | — | — | **54** in F₂, R/Q/Z | +700 | — |
| `⟨3,5,6⟩` | **✓ 68** Alphaevolve [Z→F₂] | **✓ 68** Alphaevolve | — | — | **68** in F₂, R/Q/Z | +482 | — |
| `⟨3,6,6⟩` | **✓ 83** Dronperminov-ZT [Z→F₂] | **✓ 83** Dronperminov-ZT | — | — | **83** in F₂, R/Q/Z | +912 | — |
| `⟨4,4,6⟩` | **✓ 73** Dronperminov-ZT [Z→F₂] | **✓ 73** Dronperminov-ZT | — | — | **73** in F₂, R/Q/Z | +565 | — |
| `⟨4,5,6⟩` | **✓ 90** Alphaevolve [Z→F₂] | **✓ 90** Alphaevolve | — | — | **90** in F₂, R/Q/Z | +775 | — |
| `⟨4,6,6⟩` | **✓ 105** Dronperminov-ZT [Z→F₂] | **✓ 105** Dronperminov-ZT | — | — | **105** in F₂, R/Q/Z | +965 | — |
| `⟨5,5,6⟩` | **✓ 110** Dronperminov-ZT [Z→F₂] | **✓ 110** Dronperminov-ZT | — | — | **110** in F₂, R/Q/Z | +1215 | — |
| `⟨5,6,6⟩` | **✓ 130** Dronperminov-ZT [Z→F₂] | **✓ 130** Dronperminov-ZT | — | — | **130** in F₂, R/Q/Z | +1716 | — |
| `⟨6,6,6⟩` | **✓ 153** Dronperminov-c2171_ZT [Z→F₂] | **✓ 153** Dronperminov-c2171_ZT | — | — | **153** in F₂, R/Q/Z | +2171 | — |

## Section 7 — max-dimension = 7

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,7⟩` | **✓ 25** Alphatensor-Z [Z→F₂] | **✓ 25** Alphatensor-Z | — | — | **25** in F₂, R/Q/Z | +75 | — |
| `⟨2,3,7⟩` | **✓ 35** Dronperminov-ZT [Z→F₂] | **✓ 35** Dronperminov-ZT | — | — | **35** in F₂, R/Q/Z | +179 | — |
| `⟨2,4,7⟩` | **✓ 45** Alphaevolve [Z→F₂] | **✓ 45** Alphaevolve | — | — | **45** in F₂, R/Q/Z | +308 | — |
| `⟨2,5,7⟩` | **✓ 55** Dronperminov-ZT [Z→F₂] | **✓ 55** Dronperminov-ZT | — | — | **55** in F₂, R/Q/Z | +536 | — |
| `⟨2,6,7⟩` | **✓ 66** Dronperminov-ZT [Z→F₂] | **✓ 66** Dronperminov-ZT | — | — | **66** in F₂, R/Q/Z | +797 | — |
| `⟨2,7,7⟩` | **✓ 76** Dronperminov-ZT [Z→F₂] | **✓ 76** Dronperminov-ZT | — | — | **76** in F₂, R/Q/Z | +1267 | — |
| `⟨3,3,7⟩` | **✓ 49** Dronperminov-ZT [Z→F₂] | **✓ 49** Dronperminov-ZT | — | — | **49** in F₂, R/Q/Z | +404 | — |
| `⟨3,4,7⟩` | **✓ 64** Dronperminov-ZT [Z→F₂] | **✓ 64** Dronperminov-ZT | **✓ 63** Alphaevolve | — | **63** in C | +454 | — |
| `⟨3,5,7⟩` | **✓ 79** Dronperminov-ZT [Z→F₂] | **✓ 79** Dronperminov-ZT | — | — | **79** in F₂, R/Q/Z | +520 | — |
| `⟨3,6,7⟩` | **✓ 96** Dronperminov-ZT [Z→F₂] | **✓ 96** Dronperminov-ZT | — | — | **96** in F₂, R/Q/Z | +1082 | — |
| `⟨3,7,7⟩` | **✓ 111** Dronperminov-ZT [Z→F₂] | **✓ 111** Dronperminov-ZT | — | — | **111** in F₂, R/Q/Z | +993 | — |
| `⟨4,4,7⟩` | **✓ 85** Alphaevolve [Z→F₂] | **✓ 85** Alphaevolve | — | — | **85** in F₂, R/Q/Z | +631 | — |
| `⟨4,5,7⟩` | **✓ 104** Dronperminov-ZT [Z→F₂] | **✓ 104** Dronperminov-ZT | — | — | **104** in F₂, R/Q/Z | +927 | — |
| `⟨4,6,7⟩` | **✓ 123** Dronperminov-ZT [Z→F₂] | **✓ 123** Dronperminov-ZT | — | — | **123** in F₂, R/Q/Z | +1586 | — |
| `⟨4,7,7⟩` | **✓ 144** Dronperminov-ZT [Z→F₂] | **✓ 144** Dronperminov-ZT | — | — | **144** in F₂, R/Q/Z | +1983 | — |
| `⟨5,5,7⟩` | **✓ 127** Dronperminov-ZT [Z→F₂] | **✓ 127** Dronperminov-ZT | — | — | **127** in F₂, R/Q/Z | +1606 | — |
| `⟨5,6,7⟩` | **✓ 150** Dronperminov-ZT [Z→F₂] | **✓ 150** Dronperminov-ZT | — | — | **150** in F₂, R/Q/Z | +2039 | — |
| `⟨5,7,7⟩` | **✓ 176** Dronperminov-ZT [Z→F₂] | **✓ 176** Dronperminov-ZT | — | — | **176** in F₂, R/Q/Z | +2745 | — |
| `⟨6,6,7⟩` | **✓ 183** Dronperminov-ZT [Z→F₂] | **✓ 183** Dronperminov-ZT | — | — | **183** in F₂, R/Q/Z | +2493 | — |
| `⟨6,7,7⟩` | **✓ 212** Dronperminov-ZT [Z→F₂] | **✓ 212** Dronperminov-ZT | — | — | **212** in F₂, R/Q/Z | +2320 | — |
| `⟨7,7,7⟩` | **✓ 250** Dronperminov-ZT [Z→F₂] | **✓ 250** Dronperminov-ZT | — | — | **250** in F₂, R/Q/Z | +2417 | — |

## Section 8 — max-dimension = 8

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,8⟩` | **✓ 28** Alphatensor-Z [Z→F₂] | **✓ 28** Alphatensor-Z | — | — | **28** in F₂, R/Q/Z | +103 | — |
| `⟨2,3,8⟩` | **✓ 40** Dronperminov-ZT [Z→F₂] | **✓ 40** Dronperminov-ZT | — | — | **40** in F₂, R/Q/Z | +190 | — |
| `⟨2,4,8⟩` | **✓ 51** Alphaevolve [Z→F₂] | **✓ 51** Alphaevolve | — | — | **51** in F₂, R/Q/Z | +354 | — |
| `⟨2,5,8⟩` | **✓ 63** Dronperminov-ZT [Z→F₂] | **✓ 63** Dronperminov-ZT | — | — | **63** in F₂, R/Q/Z | +570 | — |
| `⟨2,6,8⟩` | **✓ 75** Dronperminov-ZT [Z→F₂] | **✓ 75** Dronperminov-ZT | — | — | **75** in F₂, R/Q/Z | +926 | — |
| `⟨2,7,8⟩` | **✓ 88** Dronperminov-ZT [Z→F₂] | **✓ 88** Dronperminov-ZT | — | — | **88** in F₂, R/Q/Z | +745 | — |
| `⟨2,8,8⟩` | — | **✓ 100** Dronperminov-cr424_cn608_ZT_reduced | — | — | **100** in R/Q/Z | — | — |
| `⟨3,3,8⟩` | **✓ 56** Dronperminov-ZT [Z→F₂] | **✓ 56** Dronperminov-ZT | — | — | **56** in F₂, R/Q/Z | +509 | — |
| `⟨3,4,8⟩` | **✓ 73** Dronperminov-ZT [Z→F₂] | **✓ 73** Dronperminov-ZT | — | — | **73** in F₂, R/Q/Z | +976 | — |
| `⟨3,5,8⟩` | **✓ 90** Dronperminov-ZT [Z→F₂] | **✓ 90** Dronperminov-ZT | — | — | **90** in F₂, R/Q/Z | +712 | — |
| `⟨3,6,8⟩` | **✓ 108** Dronperminov-ZT [Z→F₂] | **✓ 108** Dronperminov-ZT | — | — | **108** in F₂, R/Q/Z | +1412 | — |
| `⟨3,7,8⟩` | **✓ 128** Dronperminov-ZT [Z→F₂] | **✓ 128** Dronperminov-ZT | — | — | **128** in F₂, R/Q/Z | +930 | — |
| `⟨3,8,8⟩` | **✓ 146** Dronperminov-ZT [Z→F₂] | **✓ 146** Dronperminov-ZT | — | — | **146** in F₂, R/Q/Z | +1976 | — |
| `⟨4,4,8⟩` | **✓ 96** Dronperminov-ZT [Z→F₂] | **✓ 96** Dronperminov-ZT | — | — | **96** in F₂, R/Q/Z | +1027 | — |
| `⟨4,5,8⟩` | **✓ 118** Dronperminov-ZT [Z→F₂] | **✓ 118** Dronperminov-ZT | — | — | **118** in F₂, R/Q/Z | +1521 | — |
| `⟨4,6,8⟩` | — | **✓ 140** Dronperminov-cr551_cn1248_ZT_reduced | — | — | **140** in R/Q/Z | — | — |
| `⟨4,7,8⟩` | **✓ 161** Dronperminov-ZT [Z→F₂] | **✓ 161** Dronperminov-ZT | — | — | **161** in F₂, R/Q/Z | +2270 | — |
| `⟨4,8,8⟩` | **✓ 180** Dronperminov-ZT [Z→F₂] | **✓ 180** Dronperminov-ZT | — | — | **180** in F₂, R/Q/Z | +2888 | — |
| `⟨5,5,8⟩` | **✓ 144** Dronperminov-ZT [Z→F₂] | **✓ 144** Dronperminov-ZT | — | — | **144** in F₂, R/Q/Z | +1908 | — |
| `⟨5,6,8⟩` | **✓ 170** Dronperminov-ZT [Z→F₂] | **✓ 170** Dronperminov-ZT | — | — | **170** in F₂, R/Q/Z | +2410 | — |
| `⟨5,7,8⟩` | **✓ 204** Dronperminov-ZT [Z→F₂] | **✓ 204** Dronperminov-ZT | — | — | **204** in F₂, R/Q/Z | +2606 | — |
| `⟨5,8,8⟩` | **✓ 230** Dronperminov-c2638_ZT [Z→F₂] | **✓ 230** Dronperminov-c2638_ZT | — | — | **230** in F₂, R/Q/Z | +2638 | — |
| `⟨6,6,8⟩` | — | **✓ 203** Dronperminov-cr836_fv454_cn1994_ZT_reduced | — | — | **203** in R/Q/Z | — | — |
| `⟨6,7,8⟩` | **✓ 238** Dronperminov-ZT [Z→F₂] | **✓ 238** Dronperminov-ZT | — | — | **238** in F₂, R/Q/Z | +2644 | — |
| `⟨6,8,8⟩` | — | **✓ 266** Dronperminov-cr1161_fv654_cn2780_ZT_reduced | — | — | **266** in R/Q/Z | — | — |
| `⟨7,7,8⟩` | **✓ 278** Dronperminov-ZT [Z→F₂] | **✓ 278** Dronperminov-ZT | — | — | **278** in F₂, R/Q/Z | +3229 | — |
| `⟨7,8,8⟩` | **✓ 310** Dronperminov-ZT [Z→F₂] | **✓ 310** Dronperminov-ZT | — | — | **310** in F₂, R/Q/Z | +3604 | — |
| `⟨8,8,8⟩` | **✓ 329** Composed-ATf2-strassen | **✓ 343** Composed-strassen3 | — | — | **329** in F₂ | +4678 | — |

## Section 9 — max-dimension = 9

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,9⟩` | — | **✓ 32** Dronperminov-cr59_cn74_ZT_reduced | — | — | **32** in R/Q/Z | — | — |
| `⟨2,3,9⟩` | — | **✓ 45** Dronperminov-cr116_cn174_ZT_reduced | — | — | **45** in R/Q/Z | — | — |
| `⟨2,4,9⟩` | **✓ 58** Dronperminov-ZT [Z→F₂] | **✓ 58** Dronperminov-Q | — | — | **58** in F₂, R/Q/Z | +439 | — |
| `⟨2,5,9⟩` | **✓ 72** Dronperminov-ZT [Z→F₂] | **✓ 72** Dronperminov-ZT | — | — | **72** in F₂, R/Q/Z | +465 | — |
| `⟨2,6,9⟩` | **✓ 86** Dronperminov-ZT [Z→F₂] | **✓ 86** Dronperminov-ZT | — | — | **86** in F₂, R/Q/Z | +553 | — |
| `⟨2,7,9⟩` | **✓ 99** Dronperminov-ZT [Z→F₂] | **✓ 99** Dronperminov-ZT | — | — | **99** in F₂, R/Q/Z | +804 | — |
| `⟨2,8,9⟩` | **✓ 113** Dronperminov-ZT [Z→F₂] | **✓ 113** Dronperminov-ZT | — | — | **113** in F₂, R/Q/Z | +1162 | — |
| `⟨3,3,9⟩` | **✓ 63** Dronperminov-ZT [Z→F₂] | **✓ 63** Dronperminov-ZT | — | — | **63** in F₂, R/Q/Z | +522 | — |
| `⟨3,4,9⟩` | **✓ 83** Dronperminov-ZT [Z→F₂] | **✓ 83** Dronperminov-ZT | — | — | **83** in F₂, R/Q/Z | +837 | — |
| `⟨3,5,9⟩` | **✓ 102** Dronperminov-ZT [Z→F₂] | **✓ 102** Dronperminov-ZT | — | — | **102** in F₂, R/Q/Z | +818 | — |
| `⟨3,6,9⟩` | **✓ 122** Dronperminov-ZT [Z→F₂] | **✓ 122** Dronperminov-ZT | — | — | **122** in F₂, R/Q/Z | +1203 | — |
| `⟨3,7,9⟩` | **✓ 141** Dronperminov-ZT [Z→F₂] | **✓ 141** Dronperminov-ZT | — | — | **141** in F₂, R/Q/Z | +1048 | — |
| `⟨3,8,9⟩` | **✓ 163** Dronperminov-ZT [Z→F₂] | **✓ 163** Dronperminov-ZT | — | — | **163** in F₂, R/Q/Z | +1709 | — |
| `⟨3,9,9⟩` | **✓ 185** Dronperminov-ZT [Z→F₂] | **✓ 185** Dronperminov-ZT | — | — | **185** in F₂, R/Q/Z | +1641 | — |
| `⟨4,4,9⟩` | **✓ 107** Dronperminov-ZT [Z→F₂] | **✓ 107** Dronperminov-ZT | — | — | **107** in F₂, R/Q/Z | +1112 | — |
| `⟨4,5,9⟩` | **✓ 132** Dronperminov-ZT [Z→F₂] | **✓ 132** Dronperminov-ZT | — | — | **132** in F₂, R/Q/Z | +1761 | — |
| `⟨4,6,9⟩` | **✓ 159** Dronperminov-ZT [Z→F₂] | **✓ 159** Dronperminov-ZT | — | — | **159** in F₂, R/Q/Z | +1600 | — |
| `⟨4,7,9⟩` | **✓ 187** Dronperminov-ZT [Z→F₂] | **✓ 187** Dronperminov-ZT | — | — | **187** in F₂, R/Q/Z | +2053 | — |
| `⟨4,8,9⟩` | **✓ 209** Dronperminov-ZT [Z→F₂] | **✓ 209** Dronperminov-ZT | — | — | **209** in F₂, R/Q/Z | +2777 | — |
| `⟨5,5,9⟩` | **✓ 161** Dronperminov-ZT [Z→F₂] | **✓ 161** Dronperminov-ZT | — | — | **161** in F₂, R/Q/Z | +2218 | — |
| `⟨5,6,9⟩` | **✓ 193** Dronperminov-ZT [Z→F₂] | **✓ 193** Dronperminov-ZT | — | — | **193** in F₂, R/Q/Z | +2812 | — |
| `⟨5,7,9⟩` | **✓ 229** Dronperminov-ZT [Z→F₂] | **✓ 229** Dronperminov-ZT | — | — | **229** in F₂, R/Q/Z | +2525 | — |
| `⟨5,8,9⟩` | **✓ 260** Dronperminov-ZT [Z→F₂] | **✓ 260** Dronperminov-ZT | — | — | **260** in F₂, R/Q/Z | +3043 | — |
| `⟨5,9,9⟩` | **✓ 293** Dronperminov-ZT [Z→F₂] | **✓ 293** Dronperminov-ZT | — | — | **293** in F₂, R/Q/Z | +4015 | — |
| `⟨6,6,9⟩` | — | **✓ 225** Dronperminov-cr923_fv503_cn2440_ZT_reduced | — | — | **225** in R/Q/Z | — | — |
| `⟨6,7,9⟩` | **✓ 264** Dronperminov-ZT [Z→F₂] | **✓ 264** Dronperminov-ZT | — | — | **264** in F₂, R/Q/Z | +4210 | — |
| `⟨6,9,9⟩` | **✓ 341** Dronperminov-ZT [Z→F₂] | **✓ 332** Dronperminov-Q | — | — | **332** in R/Q/Z | +3865 | — |
| `⟨7,7,9⟩` | **✓ 316** Dronperminov-ZT [Z→F₂] | **✓ 316** Dronperminov-ZT | — | — | **316** in F₂, R/Q/Z | +3452 | — |
| `⟨7,8,9⟩` | **✓ 347** Dronperminov-ZT [Z→F₂] | **✓ 347** Dronperminov-ZT | — | — | **347** in F₂, R/Q/Z | +5823 | — |
| `⟨7,9,9⟩` | **✓ 396** Dronperminov-ZT [Z→F₂] | **✓ 396** Dronperminov-ZT | — | — | **396** in F₂, R/Q/Z | +4916 | — |
| `⟨8,8,9⟩` | **✓ 391** Dronperminov-ZT [Z→F₂] | **✓ 391** Dronperminov-ZT | — | — | **391** in F₂, R/Q/Z | +5304 | — |
| `⟨8,9,9⟩` | **✓ 432** Dronperminov-ZT [Z→F₂] | **✓ 432** Dronperminov-ZT | — | — | **432** in F₂, R/Q/Z | +5667 | — |
| `⟨9,9,9⟩` | **✓ 486** Dronperminov-ZT [Z→F₂] | **✓ 486** Dronperminov-ZT | — | — | **486** in F₂, R/Q/Z | +7100 | — |

## Section 10 — max-dimension = 10

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,10⟩` | — | **✓ 35** Dronperminov-cr70_cn90_ZT_reduced | — | — | **35** in R/Q/Z | — | — |
| `⟨2,3,10⟩` | **✓ 50** Dronperminov-ZT [Z→F₂] | **✓ 50** Dronperminov-ZT | — | — | **50** in F₂, R/Q/Z | +198 | — |
| `⟨2,4,10⟩` | **✓ 64** Dronperminov-ZT [Z→F₂] | **✓ 64** Dronperminov-ZT | — | — | **64** in F₂, R/Q/Z | +450 | — |
| `⟨2,5,10⟩` | **✓ 79** Dronperminov-ZT [Z→F₂] | **✓ 79** Dronperminov-ZT | — | — | **79** in F₂, R/Q/Z | +957 | — |
| `⟨2,6,10⟩` | — | **✓ 94** Dronperminov-cr325_fv153_cn668_ZT_reduced | — | — | **94** in R/Q/Z | — | — |
| `⟨2,7,10⟩` | **✓ 110** Dronperminov-ZT [Z→F₂] | **✓ 110** Dronperminov-ZT | — | — | **110** in F₂, R/Q/Z | +1080 | — |
| `⟨2,8,10⟩` | **✓ 125** Dronperminov-ZT [Z→F₂] | **✓ 125** Dronperminov-ZT | — | — | **125** in F₂, R/Q/Z | +1374 | — |
| `⟨2,9,10⟩` | **✓ 143** Dronperminov-ZT [Z→F₂] | **✓ 143** Dronperminov-ZT | — | — | **143** in F₂, R/Q/Z | +1427 | — |
| `⟨3,3,10⟩` | **✓ 69** Dronperminov-ZT [Z→F₂] | **✓ 69** Dronperminov-ZT | — | — | **69** in F₂, R/Q/Z | +620 | — |
| `⟨3,4,10⟩` | **✓ 92** Dronperminov-ZT [Z→F₂] | **✓ 92** Dronperminov-ZT | — | — | **92** in F₂, R/Q/Z | +892 | — |
| `⟨3,5,10⟩` | **✓ 114** Dronperminov-ZT [Z→F₂] | **✓ 114** Dronperminov-ZT | — | — | **114** in F₂, R/Q/Z | +1028 | — |
| `⟨3,6,10⟩` | **✓ 136** Dronperminov-ZT [Z→F₂] | **✓ 136** Dronperminov-ZT | — | — | **136** in F₂, R/Q/Z | +994 | — |
| `⟨3,7,10⟩` | **✓ 158** Dronperminov-ZT [Z→F₂] | **✓ 158** Dronperminov-ZT | — | — | **158** in F₂, R/Q/Z | +1052 | — |
| `⟨3,8,10⟩` | **✓ 180** Dronperminov-ZT [Z→F₂] | **✓ 180** Dronperminov-ZT | — | — | **180** in F₂, R/Q/Z | +1442 | — |
| `⟨3,9,10⟩` | **✓ 204** Dronperminov-ZT [Z→F₂] | **✓ 204** Dronperminov-ZT | — | — | **204** in F₂, R/Q/Z | +1660 | — |
| `⟨3,10,10⟩` | **✓ 227** Dronperminov-ZT [Z→F₂] | **✓ 227** Dronperminov-ZT | — | — | **227** in F₂, R/Q/Z | +1702 | — |
| `⟨4,4,10⟩` | **✓ 115** Dronperminov-ZT [Z→F₂] | **✓ 115** Dronperminov-ZT | — | — | **115** in F₂, R/Q/Z | +1358 | — |
| `⟨4,5,10⟩` | **✓ 146** Dronperminov-ZT [Z→F₂] | **✓ 146** Dronperminov-ZT | — | — | **146** in F₂, R/Q/Z | +2012 | — |
| `⟨4,6,10⟩` | **✓ 175** Dronperminov-ZT [Z→F₂] | **✓ 175** Dronperminov-ZT | — | — | **175** in F₂, R/Q/Z | +1878 | — |
| `⟨4,7,10⟩` | **✓ 206** Dronperminov-ZT [Z→F₂] | **✓ 206** Dronperminov-ZT | — | — | **206** in F₂, R/Q/Z | +3349 | — |
| `⟨4,8,10⟩` | **✓ 230** Dronperminov-ZT [Z→F₂] | **✓ 230** Dronperminov-ZT | — | — | **230** in F₂, R/Q/Z | +2756 | — |
| `⟨4,9,10⟩` | **✓ 250** Dronperminov-ZT [Z→F₂] | **✓ 250** Dronperminov-ZT | — | — | **250** in F₂, R/Q/Z | +4853 | — |
| `⟨5,5,10⟩` | **✓ 178** Dronperminov-ZT [Z→F₂] | **✓ 178** Dronperminov-ZT | — | — | **178** in F₂, R/Q/Z | +2648 | — |
| `⟨5,6,10⟩` | **✓ 216** Dronperminov-ZT [Z→F₂] | **✓ 216** Dronperminov-ZT | — | — | **216** in F₂, R/Q/Z | +2374 | — |
| `⟨5,7,10⟩` | **✓ 254** Dronperminov-ZT [Z→F₂] | **✓ 254** Dronperminov-ZT | — | — | **254** in F₂, R/Q/Z | +2931 | — |
| `⟨5,8,10⟩` | **✓ 286** Dronperminov-ZT [Z→F₂] | **✓ 286** Dronperminov-ZT | — | — | **286** in F₂, R/Q/Z | +2762 | — |
| `⟨5,9,10⟩` | **✓ 322** Dronperminov-ZT [Z→F₂] | **✓ 322** Dronperminov-ZT | — | — | **322** in F₂, R/Q/Z | +4476 | — |
| `⟨6,6,10⟩` | **✓ 252** Dronperminov-ZT [Z→F₂] | **✓ 252** Dronperminov-ZT | — | — | **252** in F₂, R/Q/Z | +3536 | — |
| `⟨6,7,10⟩` | **✓ 296** Alphatensor-Z [Z→F₂] | **✓ 293** Dronperminov-Q | — | — | **293** in R/Q/Z | +3825 | — |
| `⟨6,8,10⟩` | **✓ 327** Dronperminov-ZT [Z→F₂] | **✓ 327** Dronperminov-ZT | — | — | **327** in F₂, R/Q/Z | +7489 | — |
| `⟨6,9,10⟩` | **✓ 371** Dronperminov-ZT [Z→F₂] | **✓ 367** Dronperminov-Q | — | — | **367** in R/Q/Z | +4604 | — |
| `⟨7,7,10⟩` | **✓ 346** Dronperminov-ZT [Z→F₂] | **✓ 345** Dronperminov-Q | — | — | **345** in R/Q/Z | +4082 | — |
| `⟨7,8,10⟩` | **✓ 385** Dronperminov-ZT [Z→F₂] | **✓ 385** Dronperminov-ZT | — | — | **385** in F₂, R/Q/Z | +5040 | — |
| `⟨7,9,10⟩` | **✓ 433** Dronperminov-ZT [Z→F₂] | **✓ 433** Dronperminov-ZT | — | — | **433** in F₂, R/Q/Z | +13048 | — |
| `⟨7,10,10⟩` | **✓ 478** Alphatensor-Z [Z→F₂] | **✓ 478** Alphatensor-Z | — | — | **478** in F₂, R/Q/Z | +7008 | — |
| `⟨8,8,10⟩` | **✓ 441** Alphatensor-Z [Z→F₂] | **✓ 441** Alphatensor-Z | — | — | **441** in F₂, R/Q/Z | +7704 | — |
| `⟨8,9,10⟩` | **✓ 482** Dronperminov-ZT [Z→F₂] | **✓ 482** Dronperminov-ZT | — | — | **482** in F₂, R/Q/Z | +6639 | — |
| `⟨8,10,10⟩` | **✓ 528** Dronperminov-ZT [Z→F₂] | **✓ 528** Dronperminov-ZT | — | — | **528** in F₂, R/Q/Z | +11199 | — |
| `⟨9,9,10⟩` | **✓ 534** Alphatensor-Z [Z→F₂] | **✓ 534** Alphatensor-Z | — | — | **534** in F₂, R/Q/Z | +12730 | — |
| `⟨9,10,10⟩` | **✓ 597** Dronperminov-ZT [Z→F₂] | **✓ 597** Dronperminov-ZT | — | — | **597** in F₂, R/Q/Z | +10705 | — |
| `⟨10,10,10⟩` | **✓ 651** Dronperminov-ZT [Z→F₂] | **✓ 651** Dronperminov-ZT | — | — | **651** in F₂, R/Q/Z | +11246 | — |

## Section 11 — max-dimension = 11

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,11⟩` | — | **✓ 39** Dronperminov-cr72_cn92_ZT_reduced | — | — | **39** in R/Q/Z | — | — |
| `⟨2,3,11⟩` | **✓ 55** Dronperminov-ZT [Z→F₂] | **✓ 55** Dronperminov-ZT | — | — | **55** in F₂, R/Q/Z | +263 | — |
| `⟨2,4,11⟩` | **✓ 70** Dronperminov-ZT [Z→F₂] | **✓ 70** Dronperminov-ZT | — | — | **70** in F₂, R/Q/Z | +599 | — |
| `⟨2,5,11⟩` | — | **✓ 87** Dronperminov-cr323_fv89_cn540_ZT_reduced | — | — | **87** in R/Q/Z | — | — |
| `⟨2,6,11⟩` | **✓ 103** Dronperminov-ZT [Z→F₂] | **✓ 103** Dronperminov-ZT | — | — | **103** in F₂, R/Q/Z | +869 | — |
| `⟨2,7,11⟩` | **✓ 121** Dronperminov-ZT [Z→F₂] | **✓ 121** Dronperminov-ZT | — | — | **121** in F₂, R/Q/Z | +1339 | — |
| `⟨2,8,11⟩` | **✓ 138** Dronperminov-ZT [Z→F₂] | **✓ 138** Dronperminov-ZT | — | — | **138** in F₂, R/Q/Z | +1506 | — |
| `⟨2,9,11⟩` | **✓ 157** Dronperminov-ZT [Z→F₂] | **✓ 157** Dronperminov-ZT | — | — | **157** in F₂, R/Q/Z | +1161 | — |
| `⟨2,10,11⟩` | **✓ 173** Dronperminov-ZT [Z→F₂] | **✓ 173** Dronperminov-ZT | — | — | **173** in F₂, R/Q/Z | +1643 | — |
| `⟨3,3,11⟩` | **✓ 76** Dronperminov-ZT [Z→F₂] | **✓ 76** Dronperminov-ZT | — | — | **76** in F₂, R/Q/Z | +646 | — |
| `⟨3,4,11⟩` | **✓ 101** Dronperminov-ZT [Z→F₂] | **✓ 101** Dronperminov-ZT | — | — | **101** in F₂, R/Q/Z | +977 | — |
| `⟨3,5,11⟩` | **✓ 126** Dronperminov-ZT [Z→F₂] | **✓ 126** Dronperminov-ZT | — | — | **126** in F₂, R/Q/Z | +800 | — |
| `⟨3,6,11⟩` | **✓ 150** Dronperminov-ZT [Z→F₂] | **✓ 150** Dronperminov-ZT | — | — | **150** in F₂, R/Q/Z | +1788 | — |
| `⟨3,7,11⟩` | **✓ 175** Dronperminov-ZT [Z→F₂] | **✓ 175** Dronperminov-ZT | — | — | **175** in F₂, R/Q/Z | +1448 | — |
| `⟨3,8,11⟩` | **✓ 198** Dronperminov-ZT [Z→F₂] | **✓ 198** Dronperminov-ZT | — | — | **198** in F₂, R/Q/Z | +2139 | — |
| `⟨3,9,11⟩` | **✓ 224** Dronperminov-ZT [Z→F₂] | **✓ 222** Dronperminov-Q | — | — | **222** in R/Q/Z | +2042 | — |
| `⟨3,10,11⟩` | **✓ 249** Dronperminov-ZT [Z→F₂] | **✓ 248** Dronperminov-Q | — | — | **248** in R/Q/Z | +2089 | — |
| `⟨3,11,11⟩` | **✓ 274** Dronperminov-ZT [Z→F₂] | **✓ 274** Dronperminov-ZT | — | — | **274** in F₂, R/Q/Z | +2818 | — |
| `⟨4,4,11⟩` | **✓ 129** Dronperminov-ZT [Z→F₂] | **✓ 129** Dronperminov-ZT | — | — | **129** in F₂, R/Q/Z | +1117 | — |
| `⟨4,5,11⟩` | **✓ 160** Dronperminov-ZT [Z→F₂] | **✓ 160** Dronperminov-ZT | — | — | **160** in F₂, R/Q/Z | +2192 | — |
| `⟨4,6,11⟩` | **✓ 194** Dronperminov-ZT [Z→F₂] | **✓ 194** Dronperminov-ZT | — | — | **194** in F₂, R/Q/Z | +1954 | — |
| `⟨4,7,11⟩` | **✓ 225** Dronperminov-ZT [Z→F₂] | **✓ 224** Dronperminov-Q | — | — | **224** in R/Q/Z | +2725 | — |
| `⟨4,8,11⟩` | **✓ 253** Dronperminov-ZT [Z→F₂] | **✓ 253** Dronperminov-ZT | — | — | **253** in F₂, R/Q/Z | +3876 | — |
| `⟨4,9,11⟩` | **✓ 275** Dronperminov-ZT [Z→F₂] | **✓ 275** Dronperminov-ZT | — | — | **275** in F₂, R/Q/Z | +6146 | — |
| `⟨4,11,11⟩` | **✓ 340** Dronperminov-ZT [Z→F₂] | **✓ 340** Dronperminov-ZT | — | — | **340** in F₂, R/Q/Z | +4836 | — |
| `⟨5,5,11⟩` | **✓ 195** Dronperminov-ZT [Z→F₂] | **✓ 195** Dronperminov-ZT | — | — | **195** in F₂, R/Q/Z | +2981 | — |
| `⟨5,6,11⟩` | **✓ 238** Dronperminov-ZT [Z→F₂] | **✓ 238** Dronperminov-ZT | — | — | **238** in F₂, R/Q/Z | +2809 | — |
| `⟨5,7,11⟩` | **✓ 277** Dronperminov-ZT [Z→F₂] | **✓ 277** Dronperminov-ZT | — | — | **277** in F₂, R/Q/Z | +3615 | — |
| `⟨5,8,11⟩` | **✓ 313** Dronperminov-ZT [Z→F₂] | **✓ 313** Dronperminov-ZT | — | — | **313** in F₂, R/Q/Z | +4667 | — |
| `⟨5,9,11⟩` | **✓ 353** Dronperminov-ZT [Z→F₂] | **✓ 353** Dronperminov-ZT | — | — | **353** in F₂, R/Q/Z | +4561 | — |
| `⟨5,10,11⟩` | **✓ 386** Dronperminov-ZT [Z→F₂] | **✓ 386** Dronperminov-ZT | — | — | **386** in F₂, R/Q/Z | +4715 | — |
| `⟨5,11,11⟩` | **✓ 427** Dronperminov-ZT [Z→F₂] | **✓ 427** Dronperminov-ZT | — | — | **427** in F₂, R/Q/Z | +6172 | — |
| `⟨6,6,11⟩` | **✓ 276** Dronperminov-ZT [Z→F₂] | **✓ 276** Dronperminov-ZT | — | — | **276** in F₂, R/Q/Z | +3846 | — |
| `⟨6,7,11⟩` | **✓ 322** Alphatensor-Z [Z→F₂] | **✓ 322** Alphatensor-Z | — | — | **322** in F₂, R/Q/Z | +5286 | — |
| `⟨6,8,11⟩` | **✓ 357** Dronperminov-ZT [Z→F₂] | **✓ 357** Dronperminov-ZT | — | — | **357** in F₂, R/Q/Z | +6778 | — |
| `⟨6,9,11⟩` | **✓ 407** Dronperminov-ZT [Z→F₂] | **✓ 404** Dronperminov-Q | — | — | **404** in R/Q/Z | +6261 | — |
| `⟨6,10,11⟩` | **✓ 446** Dronperminov-ZT [Z→F₂] | **✓ 446** Dronperminov-ZT | — | — | **446** in F₂, R/Q/Z | +5836 | — |
| `⟨6,11,11⟩` | **✓ 496** Dronperminov-ZT [Z→F₂] | **✓ 496** Dronperminov-ZT | — | — | **496** in F₂, R/Q/Z | +7575 | — |
| `⟨7,7,11⟩` | **✓ 378** Dronperminov-ZT [Z→F₂] | **✓ 378** Dronperminov-ZT | — | — | **378** in F₂, R/Q/Z | +5766 | — |
| `⟨7,8,11⟩` | **✓ 423** Dronperminov-ZT [Z→F₂] | **✓ 423** Dronperminov-ZT | — | — | **423** in F₂, R/Q/Z | +6666 | — |
| `⟨7,9,11⟩` | **✓ 478** Dronperminov-ZT [Z→F₂] | **✓ 478** Dronperminov-ZT | — | — | **478** in F₂, R/Q/Z | +6646 | — |
| `⟨7,10,11⟩` | **✓ 526** Dronperminov-ZT [Z→F₂] | **✓ 526** Dronperminov-ZT | — | — | **526** in F₂, R/Q/Z | +7980 | — |
| `⟨7,11,11⟩` | **✓ 580** Dronperminov-ZT [Z→F₂] | **✓ 580** Dronperminov-ZT | — | — | **580** in F₂, R/Q/Z | +9281 | — |
| `⟨8,8,11⟩` | **✓ 475** Dronperminov-ZT [Z→F₂] | **✓ 475** Dronperminov-ZT | — | — | **475** in F₂, R/Q/Z | +6694 | — |
| `⟨8,9,11⟩` | **✓ 521** Dronperminov-ZT [Z→F₂] | **✓ 521** Dronperminov-ZT | — | — | **521** in F₂, R/Q/Z | +12741 | — |
| `⟨8,10,11⟩` | **✓ 588** Dronperminov-ZT [Z→F₂] | **✓ 588** Dronperminov-ZT | — | — | **588** in F₂, R/Q/Z | +10338 | — |
| `⟨8,11,11⟩` | **✓ 646** Dronperminov-ZT [Z→F₂] | **✓ 646** Dronperminov-ZT | — | — | **646** in F₂, R/Q/Z | +11498 | — |
| `⟨9,9,11⟩` | **✓ 576** Alphatensor-Z [Z→F₂] | **✓ 576** Alphatensor-Z | — | — | **576** in F₂, R/Q/Z | +13899 | — |
| `⟨9,10,11⟩` | **✓ 657** Alphatensor-Z [Z→F₂] | **✓ 657** Alphatensor-Z | — | — | **657** in F₂, R/Q/Z | +12593 | — |
| `⟨9,11,11⟩` | **✓ 721** Dronperminov-ZT [Z→F₂] | **✓ 715** Dronperminov-Q | — | — | **715** in R/Q/Z | +15731 | — |
| `⟨10,10,11⟩` | **✓ 719** Dronperminov-ZT [Z→F₂] | **✓ 719** Dronperminov-ZT | — | — | **719** in F₂, R/Q/Z | +13524 | — |
| `⟨10,11,11⟩` | **✓ 793** Dronperminov-ZT [Z→F₂] | **✓ 793** Dronperminov-ZT | — | — | **793** in F₂, R/Q/Z | +16182 | — |
| `⟨11,11,11⟩` | **✓ 873** Dronperminov-ZT [Z→F₂] | **✓ 873** Dronperminov-ZT | — | — | **873** in F₂, R/Q/Z | +18863 | — |

## Section 12 — max-dimension = 12

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,12⟩` | — | **✓ 42** Dronperminov-cr83_cn108_ZT_reduced | — | — | **42** in R/Q/Z | — | — |
| `⟨2,3,12⟩` | — | **✓ 60** Dronperminov-cr151_cn232_ZT_reduced | — | — | **60** in R/Q/Z | — | — |
| `⟨2,4,12⟩` | **✓ 77** Dronperminov-ZT [Z→F₂] | **✓ 77** Dronperminov-ZT | — | — | **77** in F₂, R/Q/Z | +527 | — |
| `⟨2,5,12⟩` | — | **✓ 94** Dronperminov-cr322_fv137_cn664_ZT_reduced | — | — | **94** in R/Q/Z | — | — |
| `⟨2,6,12⟩` | **✓ 112** Dronperminov-ZT [Z→F₂] | **✓ 112** Dronperminov-ZT | — | — | **112** in F₂, R/Q/Z | +1070 | — |
| `⟨2,7,12⟩` | **✓ 131** Dronperminov-ZT [Z→F₂] | **✓ 131** Dronperminov-ZT | — | — | **131** in F₂, R/Q/Z | +1807 | — |
| `⟨2,8,12⟩` | **✓ 150** Dronperminov-ZT [Z→F₂] | **✓ 150** Dronperminov-ZT | — | — | **150** in F₂, R/Q/Z | +1860 | — |
| `⟨2,9,12⟩` | **✓ 171** Dronperminov-ZT [Z→F₂] | **✓ 171** Dronperminov-ZT | — | — | **171** in F₂, R/Q/Z | +1172 | — |
| `⟨2,10,12⟩` | **✓ 188** Dronperminov-ZT [Z→F₂] | **✓ 188** Dronperminov-ZT | — | — | **188** in F₂, R/Q/Z | +1352 | — |
| `⟨2,11,12⟩` | **✓ 204** Dronperminov-Z [Z→F₂] | **✓ 204** Dronperminov-Z | — | — | **204** in F₂, R/Q/Z | +2120 | — |
| `⟨3,3,12⟩` | **✓ 84** Dronperminov-ZT [Z→F₂] | **✓ 84** Dronperminov-ZT | — | — | **84** in F₂, R/Q/Z | +734 | — |
| `⟨3,4,12⟩` | **✓ 108** Dronperminov-ZT [Z→F₂] | **✓ 108** Dronperminov-ZT | — | — | **108** in F₂, R/Q/Z | +1400 | — |
| `⟨3,5,12⟩` | **✓ 136** Dronperminov-ZT [Z→F₂] | **✓ 136** Dronperminov-ZT | — | — | **136** in F₂, R/Q/Z | +988 | — |
| `⟨3,6,12⟩` | **✓ 162** Dronperminov-ZT [Z→F₂] | **✓ 162** Dronperminov-ZT | — | — | **162** in F₂, R/Q/Z | +2118 | — |
| `⟨3,7,12⟩` | **✓ 190** Dronperminov-ZT [Z→F₂] | **✓ 190** Dronperminov-ZT | — | — | **190** in F₂, R/Q/Z | +1519 | — |
| `⟨3,8,12⟩` | **✓ 216** Dronperminov-ZT [Z→F₂] | **✓ 216** Dronperminov-ZT | — | — | **216** in F₂, R/Q/Z | +2836 | — |
| `⟨3,9,12⟩` | **✓ 243** Dronperminov-ZT [Z→F₂] | **✓ 243** Dronperminov-ZT | — | — | **243** in F₂, R/Q/Z | +1884 | — |
| `⟨3,10,12⟩` | **✓ 270** Dronperminov-ZT [Z→F₂] | **✓ 270** Dronperminov-ZT | — | — | **270** in F₂, R/Q/Z | +3554 | — |
| `⟨3,11,12⟩` | **✓ 298** Dronperminov-ZT [Z→F₂] | **✓ 298** Dronperminov-ZT | — | — | **298** in F₂, R/Q/Z | +2955 | — |
| `⟨3,12,12⟩` | **✓ 324** Dronperminov-ZT [Z→F₂] | **✓ 324** Dronperminov-ZT | — | — | **324** in F₂, R/Q/Z | +4272 | — |
| `⟨4,4,12⟩` | **✓ 141** Dronperminov-ZT [Z→F₂] | **✓ 141** Dronperminov-ZT | — | — | **141** in F₂, R/Q/Z | +1480 | — |
| `⟨4,5,12⟩` | **✓ 174** Dronperminov-ZT [Z→F₂] | **✓ 174** Dronperminov-ZT | — | — | **174** in F₂, R/Q/Z | +2454 | — |
| `⟨4,7,12⟩` | **✓ 242** Dronperminov-ZT [Z→F₂] | **✓ 242** Dronperminov-ZT | — | — | **242** in F₂, R/Q/Z | +3576 | — |
| `⟨4,11,12⟩` | **✓ 362** Dronperminov-ZT [Z→F₂] | **✓ 362** Dronperminov-Q | — | — | **362** in F₂, R/Q/Z | +7837 | — |
| `⟨4,12,12⟩` | **✓ 389** Dronperminov-ZT [Z→F₂] | **✓ 389** Dronperminov-ZT | — | — | **389** in F₂, R/Q/Z | +5958 | — |
| `⟨5,5,12⟩` | **✓ 204** Dronperminov-ZT [Z→F₂] | **✓ 204** Dronperminov-ZT | — | — | **204** in F₂, R/Q/Z | +2326 | — |
| `⟨5,6,12⟩` | **✓ 258** Dronperminov-ZT [Z→F₂] | **✓ 258** Dronperminov-ZT | — | — | **258** in F₂, R/Q/Z | +3453 | — |
| `⟨5,7,12⟩` | **✓ 298** Dronperminov-ZT [Z→F₂] | **✓ 298** Dronperminov-ZT | — | — | **298** in F₂, R/Q/Z | +3014 | — |
| `⟨5,8,12⟩` | **✓ 333** Dronperminov-ZT [Z→F₂] | **✓ 333** Dronperminov-ZT | — | — | **333** in F₂, R/Q/Z | +6192 | — |
| `⟨5,9,12⟩` | **✓ 377** Dronperminov-ZT [Z→F₂] | **✓ 377** Dronperminov-ZT | — | — | **377** in F₂, R/Q/Z | +5802 | — |
| `⟨5,10,12⟩` | **✓ 408** Dronperminov-ZT [Z→F₂] | **✓ 408** Dronperminov-ZT | — | — | **408** in F₂, R/Q/Z | +4712 | — |
| `⟨5,11,12⟩` | **✓ 461** Dronperminov-ZT [Z→F₂] | **✓ 454** Dronperminov-Q | — | — | **454** in R/Q/Z | +7587 | — |
| `⟨5,12,12⟩` | **✓ 498** Dronperminov-ZT [Z→F₂] | **✓ 498** Dronperminov-ZT | — | — | **498** in F₂, R/Q/Z | +6092 | — |
| `⟨6,6,12⟩` | **✓ 294** Dronperminov-ZT [Z→F₂] | **✓ 294** Dronperminov-ZT | — | — | **294** in F₂, R/Q/Z | +4968 | — |
| `⟨6,7,12⟩` | **✓ 342** Dronperminov-ZT [Z→F₂] | **✓ 342** Dronperminov-ZT | — | — | **342** in F₂, R/Q/Z | +7117 | — |
| `⟨6,8,12⟩` | **✓ 378** Dronperminov-ZT [Z→F₂] | **✓ 378** Dronperminov-ZT | — | — | **378** in F₂, R/Q/Z | +9084 | — |
| `⟨6,9,12⟩` | **✓ 433** Dronperminov-ZT [Z→F₂] | **✓ 429** Dronperminov-Q | — | — | **429** in R/Q/Z | +5494 | — |
| `⟨6,10,12⟩` | **✓ 476** Dronperminov-ZT [Z→F₂] | **✓ 476** Dronperminov-ZT | — | — | **476** in F₂, R/Q/Z | +6752 | — |
| `⟨6,11,12⟩` | **✓ 521** Dronperminov-ZT [Z→F₂] | **✓ 521** Dronperminov-ZT | — | — | **521** in F₂, R/Q/Z | +12354 | — |
| `⟨6,12,12⟩` | **✓ 564** Dronperminov-ZT [Z→F₂] | **✓ 564** Dronperminov-ZT | — | — | **564** in F₂, R/Q/Z | +10402 | — |
| `⟨7,7,12⟩` | **✓ 404** Dronperminov-ZT [Z→F₂] | **✓ 404** Dronperminov-ZT | — | — | **404** in F₂, R/Q/Z | +7509 | — |
| `⟨7,8,12⟩` | **✓ 452** Dronperminov-ZT [Z→F₂] | **✓ 452** Dronperminov-ZT | — | — | **452** in F₂, R/Q/Z | +6610 | — |
| `⟨7,9,12⟩` | **✓ 510** Alphatensor-Z [Z→F₂] | **✓ 508** Dronperminov-Q | — | — | **508** in R/Q/Z | +9492 | — |
| `⟨7,10,12⟩` | **✓ 564** Dronperminov-ZT [Z→F₂] | **✓ 557** Dronperminov-Q | — | — | **557** in R/Q/Z | +10064 | — |
| `⟨7,11,12⟩` | **✓ 624** Dronperminov-ZT [Z→F₂] | **✓ 624** Dronperminov-ZT | — | — | **624** in F₂, R/Q/Z | +10863 | — |
| `⟨7,12,12⟩` | **✓ 669** Dronperminov-ZT [Z→F₂] | **✓ 669** Dronperminov-ZT | — | — | **669** in F₂, R/Q/Z | +11570 | — |
| `⟨8,8,12⟩` | **✓ 508** Dronperminov-ZT [Z→F₂] | **✓ 508** Dronperminov-ZT | — | — | **508** in F₂, R/Q/Z | +7228 | — |
| `⟨8,9,12⟩` | **✓ 560** Alphatensor-Z [Z→F₂] | **✓ 560** Alphatensor-Z | — | — | **560** in F₂, R/Q/Z | +13984 | — |
| `⟨8,10,12⟩` | **✓ 630** Dronperminov-ZT [Z→F₂] | **✓ 624** Dronperminov-Q | — | — | **624** in R/Q/Z | +13068 | — |
| `⟨8,11,12⟩` | **✓ 690** Dronperminov-ZT [Z→F₂] | **✓ 676** Dronperminov-Q | — | — | **676** in R/Q/Z | +12178 | — |
| `⟨8,12,12⟩` | **✓ 735** Dronperminov-ZT [Z→F₂] | **✓ 735** Dronperminov-ZT | — | — | **735** in F₂, R/Q/Z | +11970 | — |
| `⟨9,9,12⟩` | **✓ 626** Dronperminov-ZT [Z→F₂] | **✓ 626** Dronperminov-ZT | — | — | **626** in F₂, R/Q/Z | +13529 | — |
| `⟨9,10,12⟩` | **✓ 696** Alphatensor-Z [Z→F₂] | **✓ 668** Dronperminov-Q | — | — | **668** in R/Q/Z | +16838 | — |
| `⟨9,11,12⟩` | **✓ 760** Alphatensor-Z [Z→F₂] | **✓ 738** Dronperminov-Q | — | — | **738** in R/Q/Z | +20428 | — |
| `⟨9,12,12⟩` | **✓ 810** Dronperminov-ZT [Z→F₂] | **✓ 810** Dronperminov-ZT | — | — | **810** in F₂, R/Q/Z | +24272 | — |
| `⟨10,10,12⟩` | **✓ 766** Dronperminov-ZT [Z→F₂] | **✓ 766** Dronperminov-ZT | — | — | **766** in F₂, R/Q/Z | +22274 | — |
| `⟨10,11,12⟩` | **✓ 850** Dronperminov-ZT [Z→F₂] | **✓ 849** Dronperminov-Q | — | — | **849** in R/Q/Z | +18911 | — |
| `⟨10,12,12⟩` | **✓ 902** Dronperminov-ZT [Z→F₂] | **✓ 902** Dronperminov-ZT | — | — | **902** in F₂, R/Q/Z | +27437 | — |
| `⟨11,11,12⟩` | **✓ 936** Dronperminov-ZT [Z→F₂] | **✓ 922** Dronperminov-Q | — | — | **922** in R/Q/Z | +21895 | — |
| `⟨11,12,12⟩` | **✓ 990** Alphatensor-Z [Z→F₂] | **✓ 968** Dronperminov-Q | — | — | **968** in R/Q/Z | +29840 | — |
| `⟨12,12,12⟩` | **✓ 1068** Dronperminov-ZT [Z→F₂] | **✓ 1068** Dronperminov-ZT | — | — | **1068** in F₂, R/Q/Z | +29468 | — |

## Section 13 — max-dimension = 13

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,13⟩` | — | **✓ 46** Dronperminov-cr85_cn110_ZT_reduced | — | — | **46** in R/Q/Z | — | — |
| `⟨2,3,13⟩` | **✓ 65** Dronperminov-ZT [Z→F₂] | **✓ 65** Dronperminov-ZT | — | — | **65** in F₂, R/Q/Z | +382 | — |
| `⟨2,4,13⟩` | **✓ 83** Dronperminov-ZT [Z→F₂] | **✓ 83** Dronperminov-ZT | — | — | **83** in F₂, R/Q/Z | +599 | — |
| `⟨2,5,13⟩` | **✓ 102** Dronperminov-ZT [Z→F₂] | **✓ 102** Dronperminov-ZT | — | — | **102** in F₂, R/Q/Z | +868 | — |
| `⟨2,6,13⟩` | **✓ 122** Dronperminov-ZT [Z→F₂] | **✓ 122** Dronperminov-ZT | — | — | **122** in F₂, R/Q/Z | +1332 | — |
| `⟨2,7,13⟩` | **✓ 142** Dronperminov-ZT [Z→F₂] | **✓ 142** Dronperminov-ZT | — | — | **142** in F₂, R/Q/Z | +2066 | — |
| `⟨2,8,13⟩` | **✓ 163** Dronperminov-ZT [Z→F₂] | **✓ 163** Dronperminov-ZT | — | — | **163** in F₂, R/Q/Z | +1184 | — |
| `⟨2,9,13⟩` | **✓ 184** Dronperminov-ZT [Z→F₂] | **✓ 184** Dronperminov-ZT | — | — | **184** in F₂, R/Q/Z | +1253 | — |
| `⟨2,10,13⟩` | **✓ 204** Dronperminov-ZT [Z→F₂] | **✓ 204** Dronperminov-ZT | — | — | **204** in F₂, R/Q/Z | +1762 | — |
| `⟨2,11,13⟩` | **✓ 221** Dronperminov-Z [Z→F₂] | **✓ 221** Dronperminov-Z | — | — | **221** in F₂, R/Q/Z | +2911 | — |
| `⟨2,12,13⟩` | **✓ 243** Dronperminov-ZT [Z→F₂] | **✓ 243** Dronperminov-ZT | — | — | **243** in F₂, R/Q/Z | +2899 | — |
| `⟨3,3,13⟩` | **✓ 91** Dronperminov-ZT [Z→F₂] | **✓ 91** Dronperminov-ZT | — | — | **91** in F₂, R/Q/Z | +771 | — |
| `⟨3,4,13⟩` | **✓ 118** Dronperminov-ZT [Z→F₂] | **✓ 118** Dronperminov-ZT | — | — | **118** in F₂, R/Q/Z | +1146 | — |
| `⟨3,5,13⟩` | **✓ 147** Dronperminov-ZT [Z→F₂] | **✓ 147** Dronperminov-ZT | — | — | **147** in F₂, R/Q/Z | +1014 | — |
| `⟨3,6,13⟩` | **✓ 176** Dronperminov-ZT [Z→F₂] | **✓ 176** Dronperminov-ZT | — | — | **176** in F₂, R/Q/Z | +1909 | — |
| `⟨3,7,13⟩` | **✓ 204** Dronperminov-ZT [Z→F₂] | **✓ 204** Dronperminov-Q | — | — | **204** in F₂, R/Q/Z | +1537 | — |
| `⟨3,8,13⟩` | **✓ 236** Dronperminov-ZT [Z→F₂] | **✓ 236** Dronperminov-ZT | — | — | **236** in F₂, R/Q/Z | +2331 | — |
| `⟨3,9,13⟩` | **✓ 263** Dronperminov-ZT [Z→F₂] | **✓ 261** Dronperminov-Q | — | — | **261** in R/Q/Z | +2266 | — |
| `⟨3,10,13⟩` | **✓ 294** Dronperminov-ZT [Z→F₂] | **✓ 294** Dronperminov-ZT | — | — | **294** in F₂, R/Q/Z | +3094 | — |
| `⟨3,11,13⟩` | **✓ 322** Dronperminov-ZT [Z→F₂] | **✓ 322** Dronperminov-ZT | — | — | **322** in F₂, R/Q/Z | +2722 | — |
| `⟨3,12,13⟩` | **✓ 351** Dronperminov-ZT [Z→F₂] | **✓ 351** Dronperminov-ZT | — | — | **351** in F₂, R/Q/Z | +3317 | — |
| `⟨3,13,13⟩` | **✓ 380** Dronperminov-ZT [Z→F₂] | **✓ 378** Dronperminov-Q | — | — | **378** in R/Q/Z | +3485 | — |
| `⟨4,4,13⟩` | **✓ 153** Dronperminov-ZT [Z→F₂] | **✓ 153** Dronperminov-ZT | — | — | **153** in F₂, R/Q/Z | +1550 | — |
| `⟨4,5,13⟩` | **✓ 191** Dronperminov-ZT [Z→F₂] | **✓ 191** Dronperminov-ZT | — | — | **191** in F₂, R/Q/Z | +2812 | — |
| `⟨4,6,13⟩` | **✓ 227** Dronperminov-ZT [Z→F₂] | **✓ 227** Dronperminov-ZT | — | — | **227** in F₂, R/Q/Z | +2772 | — |
| `⟨4,7,13⟩` | **✓ 265** Dronperminov-ZT [Z→F₂] | **✓ 265** Dronperminov-ZT | — | — | **265** in F₂, R/Q/Z | +3202 | — |
| `⟨4,8,13⟩` | **✓ 297** Dronperminov-ZT [Z→F₂] | **✓ 297** Dronperminov-ZT | — | — | **297** in F₂, R/Q/Z | +3620 | — |
| `⟨4,9,13⟩` | **✓ 325** Dronperminov-ZT [Z→F₂] | **✓ 325** Dronperminov-ZT | — | — | **325** in F₂, R/Q/Z | +7871 | — |
| `⟨4,10,13⟩` | **✓ 361** Dronperminov-ZT [Z→F₂] | **✓ 361** Dronperminov-ZT | — | — | **361** in F₂, R/Q/Z | +5906 | — |
| `⟨4,11,13⟩` | **✓ 401** Dronperminov-ZT [Z→F₂] | **✓ 401** Dronperminov-ZT | — | — | **401** in F₂, R/Q/Z | +7291 | — |
| `⟨4,12,13⟩` | **✓ 430** Dronperminov-ZT [Z→F₂] | **✓ 422** Dronperminov-Q | — | — | **422** in R/Q/Z | +5324 | — |
| `⟨4,13,13⟩` | **✓ 472** Dronperminov-ZT [Z→F₂] | **✓ 472** Dronperminov-ZT | — | — | **472** in F₂, R/Q/Z | +5872 | — |
| `⟨5,5,13⟩` | **✓ 227** Dronperminov-ZT [Z→F₂] | **✓ 227** Dronperminov-ZT | — | — | **227** in F₂, R/Q/Z | +2795 | — |
| `⟨5,6,13⟩` | **✓ 280** Dronperminov-ZT [Z→F₂] | **✓ 280** Dronperminov-ZT | — | — | **280** in F₂, R/Q/Z | +3509 | — |
| `⟨5,7,13⟩` | **✓ 325** Dronperminov-ZT [Z→F₂] | **✓ 325** Dronperminov-ZT | — | — | **325** in F₂, R/Q/Z | +5962 | — |
| `⟨5,8,13⟩` | **✓ 365** Dronperminov-ZT [Z→F₂] | **✓ 365** Dronperminov-ZT | — | — | **365** in F₂, R/Q/Z | +5628 | — |
| `⟨5,9,13⟩` | **✓ 412** Dronperminov-ZT [Z→F₂] | **✓ 412** Dronperminov-ZT | — | — | **412** in F₂, R/Q/Z | +5873 | — |
| `⟨5,10,13⟩` | **✓ 451** Dronperminov-ZT [Z→F₂] | **✓ 451** Dronperminov-ZT | — | — | **451** in F₂, R/Q/Z | +6306 | — |
| `⟨5,11,13⟩` | **✓ 503** Dronperminov-ZT [Z→F₂] | **✓ 503** Dronperminov-ZT | — | — | **503** in F₂, R/Q/Z | +8557 | — |
| `⟨5,12,13⟩` | **✓ 537** Dronperminov-ZT [Z→F₂] | **✓ 537** Dronperminov-ZT | — | — | **537** in F₂, R/Q/Z | +8573 | — |
| `⟨5,13,13⟩` | **✓ 592** Dronperminov-ZT [Z→F₂] | **✓ 587** Dronperminov-Q | — | — | **587** in R/Q/Z | +8488 | — |
| `⟨6,6,13⟩` | **✓ 322** Dronperminov-ZT [Z→F₂] | **✓ 315** Dronperminov-Q | — | — | **315** in R/Q/Z | +5156 | — |
| `⟨6,7,13⟩` | **✓ 376** Dronperminov-ZT [Z→F₂] | **✓ 376** Dronperminov-ZT | — | — | **376** in F₂, R/Q/Z | +6268 | — |
| `⟨6,8,13⟩` | **✓ 418** Dronperminov-ZT [Z→F₂] | **✓ 418** Dronperminov-ZT | — | — | **418** in F₂, R/Q/Z | +7267 | — |
| `⟨6,9,13⟩` | **✓ 472** Dronperminov-Z [Z→F₂] | **✓ 468** Dronperminov-Q | — | — | **468** in R/Q/Z | +10079 | — |
| `⟨6,10,13⟩` | **✓ 520** Dronperminov-ZT [Z→F₂] | **✓ 520** Dronperminov-ZT | — | — | **520** in F₂, R/Q/Z | +6883 | — |
| `⟨6,11,13⟩` | **✓ 584** Dronperminov-ZT [Z→F₂] | **✓ 584** Dronperminov-ZT | — | — | **584** in F₂, R/Q/Z | +7564 | — |
| `⟨6,12,13⟩` | **✓ 615** Dronperminov-ZT [Z→F₂] | **✓ 615** Dronperminov-ZT | — | — | **615** in F₂, R/Q/Z | +10153 | — |
| `⟨6,13,13⟩` | **✓ 682** Dronperminov-ZT [Z→F₂] | **✓ 678** Dronperminov-Q | — | — | **678** in R/Q/Z | +9478 | — |
| `⟨7,7,13⟩` | **✓ 443** Dronperminov-ZT [Z→F₂] | **✓ 443** Dronperminov-ZT | — | — | **443** in F₂, R/Q/Z | +6816 | — |
| `⟨7,8,13⟩` | **✓ 498** Dronperminov-ZT [Z→F₂] | **✓ 498** Dronperminov-ZT | — | — | **498** in F₂, R/Q/Z | +7273 | — |
| `⟨7,9,13⟩` | **✓ 563** Dronperminov-ZT [Z→F₂] | **✓ 563** Dronperminov-ZT | — | — | **563** in F₂, R/Q/Z | +8062 | — |
| `⟨7,10,13⟩` | **✓ 614** Dronperminov-ZT [Z→F₂] | **✓ 614** Dronperminov-ZT | — | — | **614** in F₂, R/Q/Z | +9671 | — |
| `⟨7,11,13⟩` | **✓ 680** Dronperminov-ZT [Z→F₂] | **✓ 680** Dronperminov-ZT | — | — | **680** in F₂, R/Q/Z | +12073 | — |
| `⟨7,12,13⟩` | **✓ 731** Dronperminov-ZT [Z→F₂] | **✓ 731** Dronperminov-ZT | — | — | **731** in F₂, R/Q/Z | +14335 | — |
| `⟨7,13,13⟩` | **✓ 798** Dronperminov-ZT [Z→F₂] | **✓ 794** Dronperminov-Q | — | — | **794** in R/Q/Z | +15982 | — |
| `⟨8,8,13⟩` | **✓ 559** Dronperminov-ZT [Z→F₂] | **✓ 559** Dronperminov-ZT | — | — | **559** in F₂, R/Q/Z | +7915 | — |
| `⟨8,9,13⟩` | **✓ 615** Dronperminov-ZT [Z→F₂] | **✓ 615** Dronperminov-ZT | — | — | **615** in F₂, R/Q/Z | +10081 | — |
| `⟨8,10,13⟩` | **✓ 686** Dronperminov-ZT [Z→F₂] | **✓ 686** Dronperminov-ZT | — | — | **686** in F₂, R/Q/Z | +12390 | — |
| `⟨8,11,13⟩` | **✓ 754** Dronperminov-ZT [Z→F₂] | **✓ 754** Dronperminov-ZT | — | — | **754** in F₂, R/Q/Z | +14039 | — |
| `⟨8,12,13⟩` | **✓ 807** Dronperminov-ZT [Z→F₂] | **✓ 784** Dronperminov-Q | — | — | **784** in R/Q/Z | +16520 | — |
| `⟨8,13,13⟩` | **✓ 885** Dronperminov-ZT [Z→F₂] | **✓ 885** Dronperminov-ZT | — | — | **885** in F₂, R/Q/Z | +20034 | — |
| `⟨9,9,13⟩` | **✓ 683** Dronperminov-ZT [Z→F₂] | **✓ 683** Dronperminov-ZT | — | — | **683** in F₂, R/Q/Z | +14220 | — |
| `⟨9,10,13⟩` | **✓ 763** Dronperminov-Z [Z→F₂] | **✓ 758** Dronperminov-Q | — | — | **758** in R/Q/Z | +18940 | — |
| `⟨9,11,13⟩` | **✓ 843** Dronperminov-ZT [Z→F₂] | **✓ 835** Dronperminov-Q | — | — | **835** in R/Q/Z | +17535 | — |
| `⟨9,12,13⟩` | **✓ 894** Dronperminov-ZT [Z→F₂] | **✓ 878** Dronperminov-Q | — | — | **878** in R/Q/Z | +21009 | — |
| `⟨9,13,13⟩` | **✓ 986** Dronperminov-ZT [Z→F₂] | **✓ 981** Dronperminov-Q | — | — | **981** in R/Q/Z | +18526 | — |
| `⟨10,10,13⟩` | **✓ 838** Dronperminov-ZT [Z→F₂] | **✓ 838** Dronperminov-ZT | — | — | **838** in F₂, R/Q/Z | +18357 | — |
| `⟨10,11,13⟩` | **✓ 924** Dronperminov-ZT [Z→F₂] | **✓ 924** Dronperminov-ZT | — | — | **924** in F₂, R/Q/Z | +21141 | — |
| `⟨10,12,13⟩` | **✓ 990** Dronperminov-ZT [Z→F₂] | **✓ 990** Dronperminov-ZT | — | — | **990** in F₂, R/Q/Z | +23668 | — |
| `⟨10,13,13⟩` | **✓ 1082** Dronperminov-ZT [Z→F₂] | **✓ 1082** Dronperminov-ZT | — | — | **1082** in F₂, R/Q/Z | +26067 | — |
| `⟨11,11,13⟩` | **✓ 1023** Dronperminov-ZT [Z→F₂] | **✓ 1023** Dronperminov-ZT | — | — | **1023** in F₂, R/Q/Z | +24094 | — |
| `⟨11,12,13⟩` | **✓ 1102** Dronperminov-ZT [Z→F₂] | **✓ 1082** Dronperminov-Q | — | — | **1082** in R/Q/Z | +26850 | — |
| `⟨11,13,13⟩` | **✓ 1205** Dronperminov-ZT [Z→F₂] | **✓ 1205** Dronperminov-ZT | — | — | **1205** in F₂, R/Q/Z | +30870 | — |
| `⟨12,12,13⟩` | **✓ 1168** Dronperminov-ZT [Z→F₂] | **✓ 1144** Dronperminov-Q | — | — | **1144** in R/Q/Z | +28335 | — |
| `⟨12,13,13⟩` | **✓ 1298** Dronperminov-ZT [Z→F₂] | **✓ 1298** Dronperminov-ZT | — | — | **1298** in F₂, R/Q/Z | +34919 | — |
| `⟨13,13,13⟩` | **✓ 1426** Dronperminov-ZT [Z→F₂] | **✓ 1421** Dronperminov-Q | — | — | **1421** in R/Q/Z | +30135 | — |

## Section 14 — max-dimension = 14

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,14⟩` | — | **✓ 49** Dronperminov-cr96_cn126_ZT_reduced | — | — | **49** in R/Q/Z | — | — |
| `⟨2,3,14⟩` | — | **✓ 70** Dronperminov-cr180_cn280_ZT_reduced | — | — | **70** in R/Q/Z | — | — |
| `⟨2,4,14⟩` | — | **✓ 90** Dronperminov-cr313_fv121_cn616_ZT_reduced | — | — | **90** in R/Q/Z | — | — |
| `⟨2,5,14⟩` | **✓ 110** Dronperminov-ZT [Z→F₂] | **✓ 110** Dronperminov-ZT | — | — | **110** in F₂, R/Q/Z | +1072 | — |
| `⟨2,6,14⟩` | **✓ 131** Dronperminov-ZT [Z→F₂] | **✓ 131** Dronperminov-ZT | — | — | **131** in F₂, R/Q/Z | +1600 | — |
| `⟨2,7,14⟩` | **✓ 152** Dronperminov-ZT [Z→F₂] | **✓ 152** Dronperminov-ZT | — | — | **152** in F₂, R/Q/Z | +2534 | — |
| `⟨2,8,14⟩` | **✓ 175** Dronperminov-ZT [Z→F₂] | **✓ 175** Dronperminov-ZT | — | — | **175** in F₂, R/Q/Z | +1538 | — |
| `⟨2,9,14⟩` | **✓ 198** Dronperminov-ZT [Z→F₂] | **✓ 198** Dronperminov-ZT | — | — | **198** in F₂, R/Q/Z | +1277 | — |
| `⟨2,10,14⟩` | **✓ 219** Dronperminov-ZT [Z→F₂] | **✓ 219** Dronperminov-ZT | — | — | **219** in F₂, R/Q/Z | +1478 | — |
| `⟨2,11,14⟩` | **✓ 238** Dronperminov-Z [Z→F₂] | **✓ 238** Dronperminov-Z | — | — | **238** in F₂, R/Q/Z | +2483 | — |
| `⟨2,12,14⟩` | **✓ 262** Dronperminov-ZT [Z→F₂] | **✓ 262** Dronperminov-ZT | — | — | **262** in F₂, R/Q/Z | +3228 | — |
| `⟨2,13,14⟩` | **✓ 283** Dronperminov-ZT [Z→F₂] | **✓ 283** Dronperminov-ZT | — | — | **283** in F₂, R/Q/Z | +4162 | — |
| `⟨3,3,14⟩` | **✓ 98** Dronperminov-ZT [Z→F₂] | **✓ 98** Dronperminov-ZT | — | — | **98** in F₂, R/Q/Z | +808 | — |
| `⟨3,4,14⟩` | **✓ 127** Dronperminov-ZT [Z→F₂] | **✓ 127** Dronperminov-ZT | — | — | **127** in F₂, R/Q/Z | +1676 | — |
| `⟨3,5,14⟩` | **✓ 158** Dronperminov-ZT [Z→F₂] | **✓ 158** Dronperminov-ZT | — | — | **158** in F₂, R/Q/Z | +1040 | — |
| `⟨3,6,14⟩` | **✓ 190** Dronperminov-ZT [Z→F₂] | **✓ 190** Dronperminov-ZT | — | — | **190** in F₂, R/Q/Z | +1700 | — |
| `⟨3,7,14⟩` | **✓ 219** Dronperminov-ZT [Z→F₂] | **✓ 219** Dronperminov-ZT | — | — | **219** in F₂, R/Q/Z | +2054 | — |
| `⟨3,8,14⟩` | **✓ 253** Dronperminov-ZT [Z→F₂] | **✓ 253** Dronperminov-ZT | — | — | **253** in F₂, R/Q/Z | +2430 | — |
| `⟨3,9,14⟩` | **✓ 281** Dronperminov-ZT [Z→F₂] | **✓ 281** Dronperminov-ZT | — | — | **281** in F₂, R/Q/Z | +2634 | — |
| `⟨3,10,14⟩` | **✓ 312** Dronperminov-ZT [Z→F₂] | **✓ 312** Dronperminov-ZT | — | — | **312** in F₂, R/Q/Z | +2210 | — |
| `⟨3,11,14⟩` | **✓ 346** Dronperminov-ZT [Z→F₂] | **✓ 345** Dronperminov-Q | — | — | **345** in R/Q/Z | +3772 | — |
| `⟨3,12,14⟩` | **✓ 377** Dronperminov-ZT [Z→F₂] | **✓ 377** Dronperminov-ZT | — | — | **377** in F₂, R/Q/Z | +3136 | — |
| `⟨3,13,14⟩` | **✓ 408** Dronperminov-ZT [Z→F₂] | **✓ 407** Dronperminov-Q | — | — | **407** in R/Q/Z | +4352 | — |
| `⟨3,14,14⟩` | **✓ 438** Dronperminov-ZT [Z→F₂] | **✓ 438** Dronperminov-Q | — | — | **438** in F₂, R/Q/Z | +4150 | — |
| `⟨4,4,14⟩` | **✓ 164** Dronperminov-ZT [Z→F₂] | **✓ 163** Dronperminov-Q | — | — | **163** in R/Q/Z | +1826 | — |
| `⟨4,5,14⟩` | **✓ 207** Dronperminov-ZT [Z→F₂] | **✓ 206** Dronperminov-Q | — | — | **206** in R/Q/Z | +2472 | — |
| `⟨4,7,14⟩` | **✓ 284** Dronperminov-ZT [Z→F₂] | **✓ 284** Dronperminov-ZT | — | — | **284** in F₂, R/Q/Z | +3836 | — |
| `⟨4,9,14⟩` | **✓ 350** Dronperminov-ZT [Z→F₂] | **✓ 350** Dronperminov-ZT | — | — | **350** in F₂, R/Q/Z | +12149 | — |
| `⟨4,10,14⟩` | **✓ 385** Dronperminov-ZT [Z→F₂] | **✓ 385** Dronperminov-ZT | — | — | **385** in F₂, R/Q/Z | +7094 | — |
| `⟨4,11,14⟩` | **✓ 429** Dronperminov-ZT [Z→F₂] | **✓ 429** Dronperminov-ZT | — | — | **429** in F₂, R/Q/Z | +8737 | — |
| `⟨4,12,14⟩` | **✓ 455** Dronperminov-ZT [Z→F₂] | **✓ 452** Dronperminov-Q | — | — | **452** in R/Q/Z | +10959 | — |
| `⟨4,13,14⟩` | **✓ 502** Dronperminov-ZT [Z→F₂] | **✓ 502** Dronperminov-ZT | — | — | **502** in F₂, R/Q/Z | +13380 | — |
| `⟨4,14,14⟩` | **✓ 532** Dronperminov-ZT [Z→F₂] | **✓ 532** Dronperminov-ZT | — | — | **532** in F₂, R/Q/Z | +16076 | — |
| `⟨5,5,14⟩` | **✓ 244** Dronperminov-ZT [Z→F₂] | **✓ 244** Dronperminov-ZT | — | — | **244** in F₂, R/Q/Z | +2534 | — |
| `⟨5,6,14⟩` | **✓ 300** Dronperminov-ZT [Z→F₂] | **✓ 300** Dronperminov-ZT | — | — | **300** in F₂, R/Q/Z | +4009 | — |
| `⟨5,7,14⟩` | **✓ 351** Dronperminov-ZT [Z→F₂] | **✓ 351** Dronperminov-ZT | — | — | **351** in F₂, R/Q/Z | +4456 | — |
| `⟨5,8,14⟩` | **✓ 391** Dronperminov-ZT [Z→F₂] | **✓ 391** Dronperminov-ZT | — | — | **391** in F₂, R/Q/Z | +5133 | — |
| `⟨5,9,14⟩` | **✓ 441** Dronperminov-ZT [Z→F₂] | **✓ 441** Dronperminov-ZT | — | — | **441** in F₂, R/Q/Z | +5962 | — |
| `⟨5,10,14⟩` | **✓ 481** Dronperminov-ZT [Z→F₂] | **✓ 481** Dronperminov-ZT | — | — | **481** in F₂, R/Q/Z | +6853 | — |
| `⟨5,11,14⟩` | **✓ 537** Dronperminov-ZT [Z→F₂] | **✓ 537** Dronperminov-ZT | — | — | **537** in F₂, R/Q/Z | +9462 | — |
| `⟨5,12,14⟩` | **✓ 581** Dronperminov-ZT [Z→F₂] | **✓ 581** Dronperminov-ZT | — | — | **581** in F₂, R/Q/Z | +8178 | — |
| `⟨5,13,14⟩` | **✓ 632** Dronperminov-ZT [Z→F₂] | **✓ 628** Dronperminov-Q | — | — | **628** in R/Q/Z | +13162 | — |
| `⟨5,14,14⟩` | **✓ 672** Dronperminov-ZT [Z→F₂] | **✓ 672** Dronperminov-ZT | — | — | **672** in F₂, R/Q/Z | +13847 | — |
| `⟨6,6,14⟩` | **✓ 343** Dronperminov-ZT [Z→F₂] | **✓ 343** Dronperminov-ZT | — | — | **343** in F₂, R/Q/Z | +5506 | — |
| `⟨6,7,14⟩` | **✓ 403** Dronperminov-ZT [Z→F₂] | **✓ 403** Dronperminov-ZT | — | — | **403** in F₂, R/Q/Z | +5636 | — |
| `⟨6,8,14⟩` | **✓ 448** Dronperminov-ZT [Z→F₂] | **✓ 448** Dronperminov-ZT | — | — | **448** in F₂, R/Q/Z | +6160 | — |
| `⟨6,9,14⟩` | **✓ 507** Dronperminov-ZT [Z→F₂] | **✓ 494** Dronperminov-Q | — | — | **494** in R/Q/Z | +6484 | — |
| `⟨6,10,14⟩` | **✓ 553** Dronperminov-ZT [Z→F₂] | **✓ 553** Dronperminov-ZT | — | — | **553** in F₂, R/Q/Z | +7198 | — |
| `⟨6,11,14⟩` | **✓ 621** Dronperminov-ZT [Z→F₂] | **✓ 621** Dronperminov-ZT | — | — | **621** in F₂, R/Q/Z | +10936 | — |
| `⟨6,12,14⟩` | **✓ 654** Dronperminov-Z [Z→F₂] | **✓ 645** Dronperminov-Q | — | — | **645** in R/Q/Z | +12788 | — |
| `⟨6,13,14⟩` | **✓ 730** Dronperminov-ZT [Z→F₂] | **✓ 726** Dronperminov-Q | — | — | **726** in R/Q/Z | +13529 | — |
| `⟨6,14,14⟩` | **✓ 777** Dronperminov-ZT [Z→F₂] | **✓ 776** Dronperminov-Q | — | — | **776** in R/Q/Z | +13194 | — |
| `⟨7,7,14⟩` | **✓ 475** Dronperminov-ZT [Z→F₂] | **✓ 475** Dronperminov-ZT | — | — | **475** in F₂, R/Q/Z | +6351 | — |
| `⟨7,8,14⟩` | **✓ 532** Dronperminov-ZT [Z→F₂] | **✓ 532** Dronperminov-ZT | — | — | **532** in F₂, R/Q/Z | +7384 | — |
| `⟨7,9,14⟩` | **✓ 600** Dronperminov-ZT [Z→F₂] | **✓ 600** Dronperminov-ZT | — | — | **600** in F₂, R/Q/Z | +8433 | — |
| `⟨7,10,14⟩` | **✓ 653** Dronperminov-ZT [Z→F₂] | **✓ 653** Dronperminov-ZT | — | — | **653** in F₂, R/Q/Z | +9857 | — |
| `⟨7,11,14⟩` | **✓ 725** Dronperminov-ZT [Z→F₂] | **✓ 725** Dronperminov-ZT | — | — | **725** in F₂, R/Q/Z | +13782 | — |
| `⟨7,12,14⟩` | **✓ 780** Dronperminov-ZT [Z→F₂] | **✓ 780** Dronperminov-ZT | — | — | **780** in F₂, R/Q/Z | +17093 | — |
| `⟨7,13,14⟩` | **✓ 852** Dronperminov-ZT [Z→F₂] | **✓ 850** Dronperminov-Q | — | — | **850** in R/Q/Z | +17859 | — |
| `⟨7,14,14⟩` | **✓ 909** Dronperminov-ZT [Z→F₂] | **✓ 909** Dronperminov-ZT | — | — | **909** in F₂, R/Q/Z | +19703 | — |
| `⟨8,9,14⟩` | **✓ 654** Dronperminov-ZT [Z→F₂] | **✓ 654** Dronperminov-ZT | — | — | **654** in F₂, R/Q/Z | +10686 | — |
| `⟨8,10,14⟩` | **✓ 726** Dronperminov-ZT [Z→F₂] | **✓ 726** Dronperminov-ZT | — | — | **726** in F₂, R/Q/Z | +14733 | — |
| `⟨8,11,14⟩` | **✓ 804** Dronperminov-ZT [Z→F₂] | **✓ 804** Dronperminov-ZT | — | — | **804** in F₂, R/Q/Z | +16638 | — |
| `⟨8,12,14⟩` | **✓ 861** Dronperminov-ZT [Z→F₂] | **✓ 843** Dronperminov-Q | — | — | **843** in R/Q/Z | +20198 | — |
| `⟨8,13,14⟩` | **✓ 945** Dronperminov-ZT [Z→F₂] | **✓ 945** Dronperminov-ZT | — | — | **945** in F₂, R/Q/Z | +22857 | — |
| `⟨8,14,14⟩` | **✓ 1008** Dronperminov-ZT [Z→F₂] | **✓ 1004** Dronperminov-Q | — | — | **1004** in R/Q/Z | +25460 | — |
| `⟨9,9,14⟩` | **✓ 725** Dronperminov-ZT [Z→F₂] | **✓ 720** Dronperminov-Q | — | — | **720** in R/Q/Z | +15455 | — |
| `⟨9,10,14⟩` | **✓ 820** Dronperminov-ZT [Z→F₂] | **✓ 808** Dronperminov-Q | — | — | **808** in R/Q/Z | +16767 | — |
| `⟨9,11,14⟩` | **✓ 900** Dronperminov-ZT [Z→F₂] | **✓ 882** Dronperminov-Q | — | — | **882** in R/Q/Z | +15580 | — |
| `⟨9,12,14⟩` | **✓ 960** Dronperminov-ZT [Z→F₂] | **✓ 940** Dronperminov-Q | — | — | **940** in R/Q/Z | +16610 | — |
| `⟨9,13,14⟩` | **✓ 1050** Dronperminov-ZT [Z→F₂] | **✓ 1026** Dronperminov-Q | — | — | **1026** in R/Q/Z | +17090 | — |
| `⟨9,14,14⟩` | **✓ 1125** Dronperminov-ZT [Z→F₂] | **✓ 1101** Dronperminov-Q | — | — | **1101** in R/Q/Z | +18189 | — |
| `⟨10,10,14⟩` | **✓ 889** Dronperminov-ZT [Z→F₂] | **✓ 889** Dronperminov-ZT | — | — | **889** in F₂, R/Q/Z | +20822 | — |
| `⟨10,11,14⟩` | **✓ 981** Dronperminov-ZT [Z→F₂] | **✓ 981** Dronperminov-ZT | — | — | **981** in F₂, R/Q/Z | +23202 | — |
| `⟨10,12,14⟩` | **✓ 1050** Dronperminov-ZT [Z→F₂] | **✓ 1050** Dronperminov-ZT | — | — | **1050** in F₂, R/Q/Z | +25708 | — |
| `⟨10,13,14⟩` | **✓ 1154** Dronperminov-ZT [Z→F₂] | **✓ 1154** Dronperminov-ZT | — | — | **1154** in F₂, R/Q/Z | +29099 | — |
| `⟨10,14,14⟩` | **✓ 1232** Dronperminov-ZT [Z→F₂] | **✓ 1232** Dronperminov-ZT | — | — | **1232** in F₂, R/Q/Z | +32460 | — |
| `⟨11,11,14⟩` | **✓ 1093** Dronperminov-ZT [Z→F₂] | **✓ 1093** Dronperminov-ZT | — | — | **1093** in F₂, R/Q/Z | +26028 | — |
| `⟨11,12,14⟩` | **✓ 1182** Dronperminov-ZT [Z→F₂] | **✓ 1153** Dronperminov-Q | — | — | **1153** in R/Q/Z | +25786 | — |
| `⟨11,13,14⟩` | **✓ 1292** Dronperminov-ZT [Z→F₂] | **✓ 1292** Dronperminov-ZT | — | — | **1292** in F₂, R/Q/Z | +29509 | — |
| `⟨11,14,14⟩` | **✓ 1376** Dronperminov-ZT [Z→F₂] | **✓ 1376** Dronperminov-ZT | — | — | **1376** in F₂, R/Q/Z | +30584 | — |
| `⟨12,12,14⟩` | **✓ 1260** Dronperminov-ZT [Z→F₂] | **✓ 1234** Dronperminov-Q | — | — | **1234** in R/Q/Z | +27948 | — |
| `⟨12,13,14⟩` | **✓ 1389** Dronperminov-ZT [Z→F₂] | **✓ 1370** Dronperminov-Q | — | — | **1370** in R/Q/Z | +26698 | — |
| `⟨12,14,14⟩` | **✓ 1484** Dronperminov-ZT [Z→F₂] | **✓ 1449** Dronperminov-Q | — | — | **1449** in R/Q/Z | +30296 | — |
| `⟨13,13,14⟩` | **✓ 1511** Dronperminov-ZT [Z→F₂] | **✓ 1511** Dronperminov-ZT | — | — | **1511** in F₂, R/Q/Z | +31675 | — |
| `⟨13,14,14⟩` | **✓ 1614** Dronperminov-ZT [Z→F₂] | **✓ 1614** Dronperminov-ZT | — | — | **1614** in F₂, R/Q/Z | +36606 | — |
| `⟨14,14,14⟩` | **✓ 1725** Dronperminov-ZT [Z→F₂] | **✓ 1725** Dronperminov-ZT | — | — | **1725** in F₂, R/Q/Z | +42285 | — |

## Section 15 — max-dimension = 15

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,15⟩` | — | **✓ 53** Dronperminov-cr98_cn128_ZT_reduced | — | — | **53** in R/Q/Z | — | — |
| `⟨2,3,15⟩` | **✓ 75** Dronperminov-ZT [Z→F₂] | **✓ 75** Dronperminov-ZT | — | — | **75** in F₂, R/Q/Z | +451 | — |
| `⟨2,4,15⟩` | **✓ 96** Dronperminov-ZT [Z→F₂] | **✓ 96** Dronperminov-ZT | — | — | **96** in F₂, R/Q/Z | +704 | — |
| `⟨2,5,15⟩` | **✓ 118** Dronperminov-ZT [Z→F₂] | **✓ 118** Dronperminov-ZT | — | — | **118** in F₂, R/Q/Z | +1106 | — |
| `⟨2,7,15⟩` | **✓ 164** Dronperminov-ZT [Z→F₂] | **✓ 164** Dronperminov-ZT | — | — | **164** in F₂, R/Q/Z | +2012 | — |
| `⟨2,8,15⟩` | **✓ 188** Dronperminov-ZT [Z→F₂] | **✓ 188** Dronperminov-ZT | — | — | **188** in F₂, R/Q/Z | +1355 | — |
| `⟨2,9,15⟩` | **✓ 212** Dronperminov-ZT [Z→F₂] | **✓ 212** Dronperminov-ZT | — | — | **212** in F₂, R/Q/Z | +1358 | — |
| `⟨2,10,15⟩` | **✓ 234** Dronperminov-ZT [Z→F₂] | **✓ 234** Dronperminov-ZT | — | — | **234** in F₂, R/Q/Z | +1983 | — |
| `⟨2,11,15⟩` | **✓ 257** Dronperminov-ZT [Z→F₂] | **✓ 257** Dronperminov-ZT | — | — | **257** in F₂, R/Q/Z | +1831 | — |
| `⟨2,12,15⟩` | **✓ 281** Dronperminov-ZT [Z→F₂] | **✓ 281** Dronperminov-ZT | — | — | **281** in F₂, R/Q/Z | +3685 | — |
| `⟨2,13,15⟩` | **✓ 300** Dronperminov-Z [Z→F₂] | **✓ 300** Dronperminov-Z | — | — | **300** in F₂, R/Q/Z | +3655 | — |
| `⟨2,14,15⟩` | **✓ 327** Dronperminov-ZT [Z→F₂] | **✓ 327** Dronperminov-ZT | — | — | **327** in F₂, R/Q/Z | +4098 | — |
| `⟨3,3,15⟩` | **✓ 105** Dronperminov-ZT [Z→F₂] | **✓ 105** Dronperminov-ZT | — | — | **105** in F₂, R/Q/Z | +889 | — |
| `⟨3,4,15⟩` | **✓ 137** Dronperminov-ZT [Z→F₂] | **✓ 137** Dronperminov-ZT | — | — | **137** in F₂, R/Q/Z | +1537 | — |
| `⟨3,5,15⟩` | **✓ 169** Dronperminov-ZT [Z→F₂] | **✓ 169** Dronperminov-ZT | — | — | **169** in F₂, R/Q/Z | +1232 | — |
| `⟨3,6,15⟩` | **✓ 204** Dronperminov-ZT [Z→F₂] | **✓ 204** Dronperminov-ZT | — | — | **204** in F₂, R/Q/Z | +2494 | — |
| `⟨3,7,15⟩` | **✓ 236** Dronperminov-ZT [Z→F₂] | **✓ 235** Dronperminov-Q | — | — | **235** in R/Q/Z | +2592 | — |
| `⟨3,8,15⟩` | **✓ 270** Dronperminov-ZT [Z→F₂] | **✓ 270** Dronperminov-ZT | — | — | **270** in F₂, R/Q/Z | +2163 | — |
| `⟨3,9,15⟩` | **✓ 304** Dronperminov-ZT [Z→F₂] | **✓ 304** Dronperminov-ZT | — | — | **304** in F₂, R/Q/Z | +2766 | — |
| `⟨3,10,15⟩` | **✓ 335** Dronperminov-ZT [Z→F₂] | **✓ 335** Dronperminov-ZT | — | — | **335** in F₂, R/Q/Z | +3592 | — |
| `⟨3,11,15⟩` | **✓ 373** Dronperminov-ZT [Z→F₂] | **✓ 373** Dronperminov-ZT | — | — | **373** in F₂, R/Q/Z | +3771 | — |
| `⟨3,12,15⟩` | **✓ 405** Dronperminov-ZT [Z→F₂] | **✓ 405** Dronperminov-ZT | — | — | **405** in F₂, R/Q/Z | +4029 | — |
| `⟨3,13,15⟩` | **✓ 439** Dronperminov-ZT [Z→F₂] | **✓ 435** Dronperminov-Q | — | — | **435** in R/Q/Z | +3440 | — |
| `⟨3,14,15⟩` | **✓ 470** Dronperminov-ZT [Z→F₂] | **✓ 469** Dronperminov-Q | — | — | **469** in R/Q/Z | +3289 | — |
| `⟨3,15,15⟩` | **✓ 504** Dronperminov-ZT [Z→F₂] | **✓ 504** Dronperminov-ZT | — | — | **504** in F₂, R/Q/Z | +4869 | — |
| `⟨4,4,15⟩` | **✓ 176** Dronperminov-ZT [Z→F₂] | **✓ 176** Dronperminov-ZT | — | — | **176** in F₂, R/Q/Z | +1813 | — |
| `⟨4,5,15⟩` | **✓ 221** Dronperminov-ZT [Z→F₂] | **✓ 221** Dronperminov-ZT | — | — | **221** in F₂, R/Q/Z | +2648 | — |
| `⟨4,6,15⟩` | **✓ 263** Dronperminov-ZT [Z→F₂] | **✓ 263** Dronperminov-ZT | — | — | **263** in F₂, R/Q/Z | +2810 | — |
| `⟨4,7,15⟩` | **✓ 305** Dronperminov-ZT [Z→F₂] | **✓ 305** Dronperminov-Q | — | — | **305** in F₂, R/Q/Z | +4253 | — |
| `⟨4,9,15⟩` | **✓ 375** Dronperminov-ZT [Z→F₂] | **✓ 375** Dronperminov-ZT | — | — | **375** in F₂, R/Q/Z | +4378 | — |
| `⟨4,10,15⟩` | **✓ 417** Dronperminov-ZT [Z→F₂] | **✓ 413** Dronperminov-Q | — | — | **413** in R/Q/Z | +7262 | — |
| `⟨4,11,15⟩` | **✓ 458** Dronperminov-ZT [Z→F₂] | **✓ 449** Dronperminov-Q | — | — | **449** in R/Q/Z | +6302 | — |
| `⟨4,12,15⟩` | **✓ 488** Dronperminov-ZT [Z→F₂] | **✓ 488** Dronperminov-ZT | — | — | **488** in F₂, R/Q/Z | +6900 | — |
| `⟨4,13,15⟩` | **✓ 536** Dronperminov-ZT [Z→F₂] | **✓ 521** Dronperminov-Q | — | — | **521** in R/Q/Z | +8344 | — |
| `⟨4,14,15⟩` | **✓ 572** Dronperminov-ZT [Z→F₂] | **✓ 557** Dronperminov-Q | — | — | **557** in R/Q/Z | +7622 | — |
| `⟨4,15,15⟩` | **✓ 599** Dronperminov-ZT [Z→F₂] | **✓ 596** Dronperminov-Q | — | — | **596** in R/Q/Z | +10951 | — |
| `⟨5,5,15⟩` | **✓ 262** Dronperminov-ZT [Z→F₂] | **✓ 262** Dronperminov-ZT | — | — | **262** in F₂, R/Q/Z | +2677 | — |
| `⟨5,6,15⟩` | **✓ 320** Dronperminov-ZT [Z→F₂] | **✓ 320** Dronperminov-ZT | — | — | **320** in F₂, R/Q/Z | +4306 | — |
| `⟨5,7,15⟩` | **✓ 377** Dronperminov-ZT [Z→F₂] | **✓ 377** Dronperminov-ZT | — | — | **377** in F₂, R/Q/Z | +3540 | — |
| `⟨5,8,15⟩` | **✓ 421** Dronperminov-ZT [Z→F₂] | **✓ 421** Dronperminov-ZT | — | — | **421** in F₂, R/Q/Z | +6804 | — |
| `⟨5,9,15⟩` | **✓ 468** Dronperminov-ZT [Z→F₂] | **✓ 468** Dronperminov-ZT | — | — | **468** in F₂, R/Q/Z | +6173 | — |
| `⟨5,10,15⟩` | **✓ 519** Dronperminov-ZT [Z→F₂] | **✓ 519** Dronperminov-ZT | — | — | **519** in F₂, R/Q/Z | +7512 | — |
| `⟨5,11,15⟩` | **✓ 577** Dronperminov-ZT [Z→F₂] | **✓ 577** Dronperminov-ZT | — | — | **577** in F₂, R/Q/Z | +10487 | — |
| `⟨5,12,15⟩` | **✓ 612** Dronperminov-ZT [Z→F₂] | **✓ 612** Dronperminov-ZT | — | — | **612** in F₂, R/Q/Z | +7083 | — |
| `⟨5,13,15⟩` | **✓ 675** Dronperminov-ZT [Z→F₂] | **✓ 675** Dronperminov-ZT | — | — | **675** in F₂, R/Q/Z | +9219 | — |
| `⟨5,14,15⟩` | **✓ 722** Dronperminov-ZT [Z→F₂] | **✓ 722** Dronperminov-ZT | — | — | **722** in F₂, R/Q/Z | +9769 | — |
| `⟨5,15,15⟩` | **✓ 761** Dronperminov-ZT [Z→F₂] | **✓ 761** Dronperminov-ZT | — | — | **761** in F₂, R/Q/Z | +11276 | — |
| `⟨6,6,15⟩` | **✓ 371** Dronperminov-ZT [Z→F₂] | **✓ 371** Dronperminov-ZT | — | — | **371** in F₂, R/Q/Z | +6152 | — |
| `⟨6,7,15⟩` | **✓ 435** Dronperminov-ZT [Z→F₂] | **✓ 435** Dronperminov-ZT | — | — | **435** in F₂, R/Q/Z | +7781 | — |
| `⟨6,8,15⟩` | **✓ 484** Dronperminov-ZT [Z→F₂] | **✓ 484** Dronperminov-ZT | — | — | **484** in F₂, R/Q/Z | +9641 | — |
| `⟨6,9,15⟩` | **✓ 538** Dronperminov-ZT [Z→F₂] | **✓ 529** Dronperminov-Q | — | — | **529** in R/Q/Z | +7160 | — |
| `⟨6,10,15⟩` | **✓ 594** Dronperminov-ZT [Z→F₂] | **✓ 594** Dronperminov-ZT | — | — | **594** in F₂, R/Q/Z | +10762 | — |
| `⟨6,11,15⟩` | **✓ 653** Dronperminov-ZT [Z→F₂] | **✓ 653** Dronperminov-ZT | — | — | **653** in F₂, R/Q/Z | +13674 | — |
| `⟨6,12,15⟩` | **✓ 703** Dronperminov-Z [Z→F₂] | **✓ 686** Dronperminov-Q | — | — | **686** in R/Q/Z | +10616 | — |
| `⟨6,13,15⟩` | **✓ 763** Dronperminov-ZT [Z→F₂] | **✓ 763** Dronperminov-ZT | — | — | **763** in F₂, R/Q/Z | +12587 | — |
| `⟨6,14,15⟩` | **✓ 814** Dronperminov-ZT [Z→F₂] | **✓ 814** Dronperminov-ZT | — | — | **814** in F₂, R/Q/Z | +13060 | — |
| `⟨6,15,15⟩` | **✓ 868** Dronperminov-ZT [Z→F₂] | **✓ 859** Dronperminov-Q | — | — | **859** in R/Q/Z | +13344 | — |
| `⟨7,7,15⟩` | **✓ 511** Dronperminov-ZT [Z→F₂] | **✓ 511** Dronperminov-ZT | — | — | **511** in F₂, R/Q/Z | +8741 | — |
| `⟨7,8,15⟩` | **✓ 572** Dronperminov-ZT [Z→F₂] | **✓ 557** Dronperminov-Q | — | — | **557** in R/Q/Z | +10262 | — |
| `⟨7,9,15⟩` | **✓ 639** Dronperminov-ZT [Z→F₂] | **✓ 634** Dronperminov-Q | — | — | **634** in R/Q/Z | +8775 | — |
| `⟨7,10,15⟩` | **✓ 694** Dronperminov-ZT [Z→F₂] | **✓ 694** Dronperminov-ZT | — | — | **694** in F₂, R/Q/Z | +18581 | — |
| `⟨7,11,15⟩` | **✓ 778** Dronperminov-ZT [Z→F₂] | **✓ 777** Dronperminov-Q | — | — | **777** in R/Q/Z | +11857 | — |
| `⟨7,12,15⟩` | **✓ 815** Dronperminov-ZT [Z→F₂] | **✓ 815** Dronperminov-ZT | — | — | **815** in F₂, R/Q/Z | +15402 | — |
| `⟨7,13,15⟩` | **✓ 909** Dronperminov-ZT [Z→F₂] | **✓ 909** Dronperminov-ZT | — | — | **909** in F₂, R/Q/Z | +14480 | — |
| `⟨7,14,15⟩` | **✓ 952** Dronperminov-ZT [Z→F₂] | **✓ 952** Dronperminov-ZT | — | — | **952** in F₂, R/Q/Z | +21365 | — |
| `⟨7,15,15⟩` | **✓ 1032** Dronperminov-ZT [Z→F₂] | **✓ 1032** Dronperminov-ZT | — | — | **1032** in F₂, R/Q/Z | +16325 | — |
| `⟨8,8,15⟩` | **✓ 639** Dronperminov-ZT [Z→F₂] | **✓ 628** Dronperminov-Q | — | — | **628** in R/Q/Z | +10889 | — |
| `⟨8,9,15⟩` | **✓ 699** Dronperminov-ZT [Z→F₂] | **✓ 699** Dronperminov-ZT | — | — | **699** in F₂, R/Q/Z | +11849 | — |
| `⟨8,10,15⟩` | **✓ 784** Dronperminov-ZT [Z→F₂] | **✓ 778** Dronperminov-Q | — | — | **778** in R/Q/Z | +15881 | — |
| `⟨8,11,15⟩` | **✓ 859** Dronperminov-ZT [Z→F₂] | **✓ 848** Dronperminov-Q | — | — | **848** in R/Q/Z | +14594 | — |
| `⟨8,12,15⟩` | **✓ 914** Dronperminov-ZT [Z→F₂] | **✓ 904** Dronperminov-Q | — | — | **904** in R/Q/Z | +16687 | — |
| `⟨8,13,15⟩` | **✓ 992** Dronperminov-ZT [Z→F₂] | **✓ 992** Dronperminov-Q | — | — | **992** in F₂, R/Q/Z | +19714 | — |
| `⟨8,14,15⟩` | **✓ 1063** Dronperminov-ZT [Z→F₂] | **✓ 1063** Dronperminov-Q | — | — | **1063** in F₂, R/Q/Z | +21931 | — |
| `⟨8,15,15⟩` | **✓ 1137** Dronperminov-ZT [Z→F₂] | **✓ 1130** Dronperminov-Q | — | — | **1130** in R/Q/Z | +22114 | — |
| `⟨9,9,15⟩` | **✓ 794** Dronperminov-ZT [Z→F₂] | **✓ 760** Dronperminov-Q | — | — | **760** in R/Q/Z | +17091 | — |
| `⟨9,10,15⟩` | **✓ 865** Dronperminov-ZT [Z→F₂] | **✓ 865** Dronperminov-ZT | — | — | **865** in F₂, R/Q/Z | +13754 | — |
| `⟨9,11,15⟩` | **✓ 958** Dronperminov-ZT [Z→F₂] | **✓ 958** Dronperminov-ZT | — | — | **958** in F₂, R/Q/Z | +17798 | — |
| `⟨9,12,15⟩` | **✓ 1012** Dronperminov-ZT [Z→F₂] | **✓ 996** Dronperminov-Q | — | — | **996** in R/Q/Z | +18439 | — |
| `⟨9,13,15⟩` | **✓ 1119** Dronperminov-ZT [Z→F₂] | **✓ 1119** Dronperminov-ZT | — | — | **1119** in F₂, R/Q/Z | +18463 | — |
| `⟨9,14,15⟩` | **✓ 1179** Dronperminov-ZT [Z→F₂] | **✓ 1175** Dronperminov-Q | — | — | **1175** in R/Q/Z | +19893 | — |
| `⟨9,15,15⟩` | **✓ 1276** Dronperminov-ZT [Z→F₂] | **✓ 1236** Dronperminov-Q | — | — | **1236** in R/Q/Z | +22142 | — |
| `⟨10,10,15⟩` | **✓ 957** Dronperminov-ZT [Z→F₂] | **✓ 957** Dronperminov-ZT | — | — | **957** in F₂, R/Q/Z | +22501 | — |
| `⟨10,11,15⟩` | **✓ 1050** Dronperminov-ZT [Z→F₂] | **✓ 1050** Dronperminov-ZT | — | — | **1050** in F₂, R/Q/Z | +21792 | — |
| `⟨10,12,15⟩` | **✓ 1122** Dronperminov-ZT [Z→F₂] | **✓ 1122** Dronperminov-ZT | — | — | **1122** in F₂, R/Q/Z | +21397 | — |
| `⟨10,13,15⟩` | **✓ 1230** Dronperminov-ZT [Z→F₂] | **✓ 1230** Dronperminov-ZT | — | — | **1230** in F₂, R/Q/Z | +24859 | — |
| `⟨10,14,15⟩` | **✓ 1314** Dronperminov-ZT [Z→F₂] | **✓ 1314** Dronperminov-ZT | — | — | **1314** in F₂, R/Q/Z | +28027 | — |
| `⟨10,15,15⟩` | **✓ 1389** Dronperminov-Z [Z→F₂] | **✓ 1385** Dronperminov-Q | — | — | **1385** in R/Q/Z | +30320 | — |
| `⟨11,11,15⟩` | **✓ 1169** Dronperminov-ZT [Z→F₂] | **✓ 1169** Dronperminov-ZT | — | — | **1169** in F₂, R/Q/Z | +28849 | — |
| `⟨11,12,15⟩` | **✓ 1234** Dronperminov-ZT [Z→F₂] | **✓ 1234** Dronperminov-ZT | — | — | **1234** in F₂, R/Q/Z | +23686 | — |
| `⟨11,13,15⟩` | **✓ 1377** Dronperminov-ZT [Z→F₂] | **✓ 1371** Dronperminov-Q | — | — | **1371** in R/Q/Z | +30722 | — |
| `⟨11,14,15⟩` | **✓ 1432** Dronperminov-ZT [Z→F₂] | **✓ 1432** Dronperminov-ZT | — | — | **1432** in F₂, R/Q/Z | +32651 | — |
| `⟨11,15,15⟩` | **✓ 1548** Dronperminov-ZT [Z→F₂] | **✓ 1548** Dronperminov-ZT | — | — | **1548** in F₂, R/Q/Z | +36233 | — |
| `⟨12,12,15⟩` | **✓ 1332** Dronperminov-ZT [Z→F₂] | **✓ 1332** Dronperminov-ZT | — | — | **1332** in F₂, R/Q/Z | +47283 | — |
| `⟨12,13,15⟩` | **✓ 1470** Dronperminov-ZT [Z→F₂] | **✓ 1442** Dronperminov-Q | — | — | **1442** in R/Q/Z | +36790 | — |
| `⟨12,14,15⟩` | **✓ 1546** Dronperminov-ZT [Z→F₂] | **✓ 1538** Dronperminov-Q | — | — | **1538** in R/Q/Z | +34545 | — |
| `⟨12,15,15⟩` | **✓ 1650** Dronperminov-ZT [Z→F₂] | **✓ 1650** Dronperminov-ZT | — | — | **1650** in F₂, R/Q/Z | +41692 | — |
| `⟨13,13,15⟩` | **✓ 1605** Dronperminov-ZT [Z→F₂] | **✓ 1605** Dronperminov-ZT | — | — | **1605** in F₂, R/Q/Z | +38065 | — |
| `⟨13,14,15⟩` | **✓ 1681** Dronperminov-ZT [Z→F₂] | **✓ 1681** Dronperminov-ZT | — | — | **1681** in F₂, R/Q/Z | +42817 | — |
| `⟨13,15,15⟩` | **✓ 1797** Dronperminov-ZT [Z→F₂] | **✓ 1797** Dronperminov-ZT | — | — | **1797** in F₂, R/Q/Z | +38494 | — |
| `⟨14,14,15⟩` | **✓ 1798** Dronperminov-ZT [Z→F₂] | **✓ 1798** Dronperminov-ZT | — | — | **1798** in F₂, R/Q/Z | +42512 | — |
| `⟨14,15,15⟩` | **✓ 1895** Dronperminov-Z [Z→F₂] | **✓ 1890** Dronperminov-Q | — | — | **1890** in R/Q/Z | +55893 | — |
| `⟨15,15,15⟩` | **✓ 2058** Dronperminov-ZT [Z→F₂] | **✓ 2058** Dronperminov-ZT | — | — | **2058** in F₂, R/Q/Z | +60024 | — |

## Section 16 — max-dimension = 16

| format | F₂ | R/Q/Z | C | commutative | best (any field) | adds | history |
|---|---|---|---|---|---|---|---|
| `⟨2,2,16⟩` | — | **✓ 56** Dronperminov-cr109_cn144_ZT_reduced | — | — | **56** in R/Q/Z | — | — |
| `⟨2,3,16⟩` | — | **✓ 80** Dronperminov-cr196_cn328_ZT_reduced | — | — | **80** in R/Q/Z | — | — |
| `⟨2,4,16⟩` | — | **✓ 102** Dronperminov-cr338_fv130_cn708_ZT_reduced | — | — | **102** in R/Q/Z | — | — |
| `⟨2,5,16⟩` | **✓ 126** Dronperminov-ZT [Z→F₂] | **✓ 126** Dronperminov-ZT | — | — | **126** in F₂, R/Q/Z | +1140 | — |
| `⟨2,6,16⟩` | **✓ 150** Dronperminov-ZT [Z→F₂] | **✓ 150** Dronperminov-ZT | — | — | **150** in F₂, R/Q/Z | +1203 | — |
| `⟨2,7,16⟩` | **✓ 175** Dronperminov-ZT [Z→F₂] | **✓ 175** Dronperminov-ZT | — | — | **175** in F₂, R/Q/Z | +2071 | — |
| `⟨2,9,16⟩` | **✓ 225** Dronperminov-ZT [Z→F₂] | **✓ 225** Dronperminov-ZT | — | — | **225** in F₂, R/Q/Z | +1612 | — |
| `⟨2,11,16⟩` | **✓ 274** Dronperminov-ZT [Z→F₂] | **✓ 274** Dronperminov-ZT | — | — | **274** in F₂, R/Q/Z | +1770 | — |
| `⟨2,12,16⟩` | **✓ 298** Dronperminov-Z [Z→F₂] | **✓ 298** Dronperminov-Z | — | — | **298** in F₂, R/Q/Z | +4344 | — |
| `⟨2,13,16⟩` | **✓ 320** Dronperminov-Z [Z→F₂] | **✓ 320** Dronperminov-Z | — | — | **320** in F₂, R/Q/Z | +4168 | — |
| `⟨2,14,16⟩` | **✓ 350** Dronperminov-ZT [Z→F₂] | **✓ 350** Dronperminov-ZT | — | — | **350** in F₂, R/Q/Z | +2188 | — |
| `⟨2,15,16⟩` | **✓ 368** Dronperminov-Z [Z→F₂] | **✓ 368** Dronperminov-Z | — | — | **368** in F₂, R/Q/Z | +4105 | — |
| `⟨3,3,16⟩` | **✓ 111** Dronperminov-ZT [Z→F₂] | **✓ 111** Dronperminov-ZT | — | — | **111** in F₂, R/Q/Z | +987 | — |
| `⟨3,4,16⟩` | **✓ 146** Dronperminov-ZT [Z→F₂] | **✓ 146** Dronperminov-ZT | — | — | **146** in F₂, R/Q/Z | +1592 | — |
| `⟨3,5,16⟩` | **✓ 180** Dronperminov-ZT [Z→F₂] | **✓ 180** Dronperminov-ZT | — | — | **180** in F₂, R/Q/Z | +1424 | — |
| `⟨3,6,16⟩` | **✓ 216** Dronperminov-ZT [Z→F₂] | **✓ 216** Dronperminov-ZT | — | — | **216** in F₂, R/Q/Z | +2824 | — |
| `⟨3,7,16⟩` | **✓ 252** Dronperminov-ZT [Z→F₂] | **✓ 252** Dronperminov-ZT | — | — | **252** in F₂, R/Q/Z | +2041 | — |
| `⟨3,8,16⟩` | **✓ 288** Dronperminov-ZT [Z→F₂] | **✓ 288** Dronperminov-ZT | — | — | **288** in F₂, R/Q/Z | +2860 | — |
| `⟨3,9,16⟩` | **✓ 326** Dronperminov-ZT [Z→F₂] | **✓ 326** Dronperminov-ZT | — | — | **326** in F₂, R/Q/Z | +3064 | — |
| `⟨3,10,16⟩` | **✓ 355** Dronperminov-ZT [Z→F₂] | **✓ 355** Dronperminov-ZT | — | — | **355** in F₂, R/Q/Z | +4464 | — |
| `⟨3,11,16⟩` | **✓ 396** Dronperminov-ZT [Z→F₂] | **✓ 396** Dronperminov-ZT | — | — | **396** in F₂, R/Q/Z | +4296 | — |
| `⟨3,12,16⟩` | **✓ 432** Dronperminov-ZT [Z→F₂] | **✓ 432** Dronperminov-ZT | — | — | **432** in F₂, R/Q/Z | +5696 | — |
| `⟨3,13,16⟩` | **✓ 466** Dronperminov-ZT [Z→F₂] | **✓ 464** Dronperminov-Q | — | — | **464** in R/Q/Z | +5499 | — |
| `⟨3,14,16⟩` | **✓ 500** Dronperminov-ZT [Z→F₂] | **✓ 500** Dronperminov-Q | — | — | **500** in F₂, R/Q/Z | +4724 | — |
| `⟨3,15,16⟩` | **✓ 534** Dronperminov-ZT [Z→F₂] | **✓ 534** Dronperminov-ZT | — | — | **534** in F₂, R/Q/Z | +12209 | — |
| `⟨3,16,16⟩` | **✓ 571** Dronperminov-ZT [Z→F₂] | **✓ 569** Dronperminov-Q | — | — | **569** in R/Q/Z | +7336 | — |
| `⟨4,4,16⟩` | **✓ 188** Dronperminov-ZT [Z→F₂] | **✓ 188** Dronperminov-ZT | — | — | **188** in F₂, R/Q/Z | +1898 | — |
| `⟨4,5,16⟩` | **✓ 235** Dronperminov-ZT [Z→F₂] | **✓ 235** Dronperminov-ZT | — | — | **235** in F₂, R/Q/Z | +2910 | — |
| `⟨4,6,16⟩` | **✓ 276** Dronperminov-ZT [Z→F₂] | **✓ 276** Dronperminov-ZT | — | — | **276** in F₂, R/Q/Z | +2945 | — |
| `⟨4,7,16⟩` | **✓ 322** Dronperminov-ZT [Z→F₂] | **✓ 322** Dronperminov-ZT | — | — | **322** in F₂, R/Q/Z | +4955 | — |
| `⟨4,9,16⟩` | **✓ 398** Dronperminov-ZT [Z→F₂] | **✓ 398** Dronperminov-ZT | — | — | **398** in F₂, R/Q/Z | +5574 | — |
| `⟨4,10,16⟩` | **✓ 441** Dronperminov-ZT [Z→F₂] | **✓ 441** Dronperminov-ZT | — | — | **441** in F₂, R/Q/Z | +7598 | — |
| `⟨4,11,16⟩` | **✓ 480** Dronperminov-ZT [Z→F₂] | **✓ 480** Dronperminov-ZT | — | — | **480** in F₂, R/Q/Z | +7075 | — |
| `⟨4,12,16⟩` | **✓ 513** Dronperminov-ZT [Z→F₂] | **✓ 513** Dronperminov-ZT | — | — | **513** in F₂, R/Q/Z | +12494 | — |
| `⟨4,13,16⟩` | **✓ 560** Dronperminov-ZT [Z→F₂] | **✓ 560** Dronperminov-ZT | — | — | **560** in F₂, R/Q/Z | +15833 | — |
| `⟨4,14,16⟩` | **✓ 598** Dronperminov-ZT [Z→F₂] | **✓ 598** Dronperminov-ZT | — | — | **598** in F₂, R/Q/Z | +17688 | — |
| `⟨4,15,16⟩` | **✓ 640** Dronperminov-ZT [Z→F₂] | **✓ 632** Dronperminov-Q | — | — | **632** in R/Q/Z | +10347 | — |
| `⟨4,16,16⟩` | **✓ 666** Dronperminov-ZT [Z→F₂] | **✓ 666** Dronperminov-ZT | — | — | **666** in F₂, R/Q/Z | +17711 | — |
| `⟨5,5,16⟩` | **✓ 280** Dronperminov-ZT [Z→F₂] | **✓ 280** Dronperminov-ZT | — | — | **280** in F₂, R/Q/Z | +2854 | — |
| `⟨5,6,16⟩` | **✓ 340** Dronperminov-ZT [Z→F₂] | **✓ 340** Dronperminov-ZT | — | — | **340** in F₂, R/Q/Z | +4624 | — |
| `⟨5,7,16⟩` | **✓ 400** Dronperminov-ZT [Z→F₂] | **✓ 400** Dronperminov-ZT | — | — | **400** in F₂, R/Q/Z | +6705 | — |
| `⟨5,8,16⟩` | **✓ 445** Dronperminov-ZT [Z→F₂] | **✓ 445** Dronperminov-ZT | — | — | **445** in F₂, R/Q/Z | +8972 | — |
| `⟨5,9,16⟩` | **✓ 503** Dronperminov-ZT [Z→F₂] | **✓ 503** Dronperminov-ZT | — | — | **503** in F₂, R/Q/Z | +8543 | — |
| `⟨5,10,16⟩` | **✓ 549** Dronperminov-ZT [Z→F₂] | **✓ 549** Dronperminov-ZT | — | — | **549** in F₂, R/Q/Z | +8404 | — |
| `⟨5,11,16⟩` | **✓ 609** Dronperminov-ZT [Z→F₂] | **✓ 609** Dronperminov-ZT | — | — | **609** in F₂, R/Q/Z | +11719 | — |
| `⟨5,12,16⟩` | **✓ 657** Dronperminov-ZT [Z→F₂] | **✓ 655** Dronperminov-Q | — | — | **655** in R/Q/Z | +14890 | — |
| `⟨5,13,16⟩` | **✓ 718** Dronperminov-ZT [Z→F₂] | **✓ 718** Dronperminov-ZT | — | — | **718** in F₂, R/Q/Z | +11397 | — |
| `⟨5,14,16⟩` | **✓ 769** Dronperminov-ZT [Z→F₂] | **✓ 769** Dronperminov-ZT | — | — | **769** in F₂, R/Q/Z | +11546 | — |
| `⟨5,15,16⟩` | **✓ 813** Dronperminov-ZT [Z→F₂] | **✓ 813** Dronperminov-ZT | — | — | **813** in F₂, R/Q/Z | +11988 | — |
| `⟨5,16,16⟩` | **✓ 868** Dronperminov-ZT [Z→F₂] | **✓ 868** Dronperminov-ZT | — | — | **868** in F₂, R/Q/Z | +12156 | — |
| `⟨6,6,16⟩` | **✓ 392** Dronperminov-ZT [Z→F₂] | **✓ 392** Dronperminov-ZT | — | — | **392** in F₂, R/Q/Z | +6860 | — |
| `⟨6,7,16⟩` | **✓ 460** Dronperminov-ZT [Z→F₂] | **✓ 460** Dronperminov-ZT | — | — | **460** in F₂, R/Q/Z | +9887 | — |
| `⟨6,8,16⟩` | **✓ 510** Dronperminov-ZT [Z→F₂] | **✓ 510** Dronperminov-ZT | — | — | **510** in F₂, R/Q/Z | +14139 | — |
| `⟨6,9,16⟩` | **✓ 572** Dronperminov-ZT [Z→F₂] | **✓ 552** Dronperminov-Q | — | — | **552** in R/Q/Z | +9230 | — |
| `⟨6,10,16⟩` | **✓ 630** Dronperminov-ZT [Z→F₂] | **✓ 630** Dronperminov-ZT | — | — | **630** in F₂, R/Q/Z | +9636 | — |
| `⟨6,11,16⟩` | **✓ 684** Dronperminov-ZT [Z→F₂] | **✓ 684** Dronperminov-Q | — | — | **684** in F₂, R/Q/Z | +14164 | — |
| `⟨6,12,16⟩` | **✓ 736** Dronperminov-ZT [Z→F₂] | **✓ 736** Dronperminov-ZT | — | — | **736** in F₂, R/Q/Z | +13880 | — |
| `⟨6,13,16⟩` | **✓ 816** Dronperminov-ZT [Z→F₂] | **✓ 798** Dronperminov-Q | — | — | **798** in R/Q/Z | +18741 | — |
| `⟨6,14,16⟩` | **✓ 864** Dronperminov-ZT [Z→F₂] | **✓ 864** Dronperminov-ZT | — | — | **864** in F₂, R/Q/Z | +15888 | — |
| `⟨6,15,16⟩` | **✓ 920** Dronperminov-ZT [Z→F₂] | **✓ 920** Dronperminov-ZT | — | — | **920** in F₂, R/Q/Z | +16970 | — |
| `⟨6,16,16⟩` | **✓ 972** Dronperminov-ZT [Z→F₂] | **✓ 972** Dronperminov-ZT | — | — | **972** in F₂, R/Q/Z | +28265 | — |
| `⟨7,7,16⟩` | **✓ 540** Dronperminov-ZT [Z→F₂] | **✓ 540** Dronperminov-ZT | — | — | **540** in F₂, R/Q/Z | +10972 | — |
| `⟨7,8,16⟩` | **✓ 598** Dronperminov-ZT [Z→F₂] | **✓ 598** Dronperminov-ZT | — | — | **598** in F₂, R/Q/Z | +10956 | — |
| `⟨7,9,16⟩` | **✓ 677** Dronperminov-ZT [Z→F₂] | **✓ 677** Dronperminov-ZT | — | — | **677** in F₂, R/Q/Z | +14870 | — |
| `⟨7,10,16⟩` | **✓ 742** Dronperminov-ZT [Z→F₂] | **✓ 736** Dronperminov-Q | — | — | **736** in R/Q/Z | +14565 | — |
| `⟨7,11,16⟩` | **✓ 822** Dronperminov-ZT [Z→F₂] | **✓ 822** Dronperminov-ZT | — | — | **822** in F₂, R/Q/Z | +15894 | — |
| `⟨7,12,16⟩` | **✓ 878** Dronperminov-Z [Z→F₂] | **✓ 878** Dronperminov-Z | — | — | **878** in F₂, R/Q/Z | +22798 | — |
| `⟨7,13,16⟩` | **✓ 966** Dronperminov-ZT [Z→F₂] | **✓ 962** Dronperminov-Q | — | — | **962** in R/Q/Z | +18378 | — |
| `⟨7,14,16⟩` | **✓ 1036** Dronperminov-ZT [Z→F₂] | **✓ 1022** Dronperminov-Q | — | — | **1022** in R/Q/Z | +23138 | — |
| `⟨7,15,16⟩` | **✓ 1089** Dronperminov-ZT [Z→F₂] | **✓ 1083** Dronperminov-Q | — | — | **1083** in R/Q/Z | +25173 | — |
| `⟨7,16,16⟩` | **✓ 1164** Dronperminov-ZT [Z→F₂] | **✓ 1164** Dronperminov-ZT | — | — | **1164** in F₂, R/Q/Z | +19425 | — |
| `⟨8,8,16⟩` | **✓ 666** Dronperminov-ZT [Z→F₂] | **✓ 666** Dronperminov-ZT | — | — | **666** in F₂, R/Q/Z | +16556 | — |
| `⟨8,9,16⟩` | **✓ 735** Dronperminov-ZT [Z→F₂] | **✓ 735** Dronperminov-ZT | — | — | **735** in F₂, R/Q/Z | +26904 | — |
| `⟨8,10,16⟩` | **✓ 826** Dronperminov-ZT [Z→F₂] | **✓ 822** Dronperminov-Q | — | — | **822** in R/Q/Z | +18992 | — |
| `⟨8,11,16⟩` | **✓ 914** Dronperminov-ZT [Z→F₂] | **✓ 904** Dronperminov-Q | — | — | **904** in R/Q/Z | +17235 | — |
| `⟨8,12,16⟩` | **✓ 960** Dronperminov-ZT [Z→F₂] | **✓ 960** Dronperminov-ZT | — | — | **960** in F₂, R/Q/Z | +17770 | — |
| `⟨8,13,16⟩` | **✓ 1072** Dronperminov-ZT [Z→F₂] | **✓ 1054** Dronperminov-Q | — | — | **1054** in R/Q/Z | +25024 | — |
| `⟨8,14,16⟩` | **✓ 1127** Dronperminov-ZT [Z→F₂] | **✓ 1104** Dronperminov-Q | — | — | **1104** in R/Q/Z | +29106 | — |
| `⟨8,15,16⟩` | **✓ 1204** Dronperminov-ZT [Z→F₂] | **✓ 1185** Dronperminov-Q | — | — | **1185** in R/Q/Z | +26858 | — |
| `⟨8,16,16⟩` | **✓ 1260** Dronperminov-ZT [Z→F₂] | **✓ 1230** Dronperminov-Q | — | — | **1230** in R/Q/Z | +36712 | — |
| `⟨9,9,16⟩` | **✓ 824** Dronperminov-ZT [Z→F₂] | **✓ 823** Dronperminov-Q | — | — | **823** in R/Q/Z | +17947 | — |
| `⟨9,10,16⟩` | **✓ 920** Dronperminov-Z [Z→F₂] | **✓ 916** Dronperminov-Q | — | — | **916** in R/Q/Z | +17390 | — |
| `⟨9,11,16⟩` | **✓ 996** Dronperminov-ZT [Z→F₂] | **✓ 996** Dronperminov-ZT | — | — | **996** in F₂, R/Q/Z | +17821 | — |
| `⟨9,12,16⟩` | **✓ 1074** Dronperminov-ZT [Z→F₂] | **✓ 1035** Dronperminov-Q | — | — | **1035** in R/Q/Z | +33084 | — |
| `⟨9,13,16⟩` | **✓ 1188** Dronperminov-ZT [Z→F₂] | **✓ 1179** Dronperminov-Q | — | — | **1179** in R/Q/Z | +35159 | — |
| `⟨9,14,16⟩` | **✓ 1270** Dronperminov-ZT [Z→F₂] | **✓ 1254** Dronperminov-Q | — | — | **1254** in R/Q/Z | +27552 | — |
| `⟨9,15,16⟩` | **✓ 1320** Dronperminov-ZT [Z→F₂] | **✓ 1320** Dronperminov-ZT | — | — | **1320** in F₂, R/Q/Z | +25501 | — |
| `⟨9,16,16⟩` | **✓ 1380** Dronperminov-ZT [Z→F₂] | **✓ 1380** Dronperminov-ZT | — | — | **1380** in F₂, R/Q/Z | +28224 | — |
| `⟨10,10,16⟩` | **✓ 1008** Dronperminov-ZT [Z→F₂] | **✓ 1008** Dronperminov-ZT | — | — | **1008** in F₂, R/Q/Z | +24224 | — |
| `⟨10,11,16⟩` | **✓ 1112** Dronperminov-ZT [Z→F₂] | **✓ 1112** Dronperminov-ZT | — | — | **1112** in F₂, R/Q/Z | +26958 | — |
| `⟨10,12,16⟩` | **✓ 1190** Dronperminov-ZT [Z→F₂] | **✓ 1176** Dronperminov-Q | — | — | **1176** in R/Q/Z | +29764 | — |
| `⟨10,13,16⟩` | **✓ 1326** Dronperminov-ZT [Z→F₂] | **✓ 1318** Dronperminov-Q | — | — | **1318** in R/Q/Z | +31420 | — |
| `⟨10,14,16⟩` | **✓ 1418** Dronperminov-ZT [Z→F₂] | **✓ 1398** Dronperminov-Q | — | — | **1398** in R/Q/Z | +31093 | — |
| `⟨10,15,16⟩` | **✓ 1484** Dronperminov-Z [Z→F₂] | **✓ 1482** Dronperminov-Q | — | — | **1482** in R/Q/Z | +28118 | — |
| `⟨10,16,16⟩` | **✓ 1578** Dronperminov-Z [Z→F₂] | **✓ 1560** Dronperminov-Q | — | — | **1560** in R/Q/Z | +40999 | — |
| `⟨11,11,16⟩` | **✓ 1230** Dronperminov-ZT [Z→F₂] | **✓ 1230** Dronperminov-ZT | — | — | **1230** in F₂, R/Q/Z | +26919 | — |
| `⟨11,12,16⟩` | **✓ 1306** Dronperminov-ZT [Z→F₂] | **✓ 1278** Dronperminov-Q | — | — | **1278** in R/Q/Z | +30342 | — |
| `⟨11,13,16⟩` | **✓ 1458** Dronperminov-ZT [Z→F₂] | **✓ 1446** Dronperminov-Q | — | — | **1446** in R/Q/Z | +36677 | — |
| `⟨11,14,16⟩` | **✓ 1550** Dronperminov-ZT [Z→F₂] | **✓ 1520** Dronperminov-Q | — | — | **1520** in R/Q/Z | +34075 | — |
| `⟨11,15,16⟩` | **✓ 1629** Dronperminov-Z [Z→F₂] | **✓ 1605** Dronperminov-Q | — | — | **1605** in R/Q/Z | +47860 | — |
| `⟨11,16,16⟩` | **✓ 1752** Dronperminov-ZT [Z→F₂] | **✓ 1752** Dronperminov-ZT | — | — | **1752** in F₂, R/Q/Z | +32390 | — |
| `⟨12,12,16⟩` | **✓ 1380** Dronperminov-ZT [Z→F₂] | **✓ 1380** Dronperminov-ZT | — | — | **1380** in F₂, R/Q/Z | +27787 | — |
| `⟨12,13,16⟩` | **✓ 1544** Dronperminov-Z [Z→F₂] | **✓ 1509** Dronperminov-Q | — | — | **1509** in R/Q/Z | +62718 | — |
| `⟨12,14,16⟩` | **✓ 1663** Dronperminov-ZT [Z→F₂] | **✓ 1617** Dronperminov-Q | — | — | **1617** in R/Q/Z | +39844 | — |
| `⟨12,15,16⟩` | **✓ 1725** Dronperminov-ZT [Z→F₂] | **✓ 1725** Dronperminov-ZT | — | — | **1725** in F₂, R/Q/Z | +35818 | — |
| `⟨12,16,16⟩` | **✓ 1862** Dronperminov-ZT [Z→F₂] | **✓ 1815** Dronperminov-Q | — | — | **1815** in R/Q/Z | +36404 | — |
| `⟨13,13,16⟩` | **✓ 1711** Dronperminov-ZT [Z→F₂] | **✓ 1704** Dronperminov-Q | — | — | **1704** in R/Q/Z | +34331 | — |
| `⟨13,14,16⟩` | **✓ 1820** Dronperminov-ZT [Z→F₂] | **✓ 1800** Dronperminov-Q | — | — | **1800** in R/Q/Z | +47185 | — |
| `⟨13,15,16⟩` | **✓ 1908** Dronperminov-ZT [Z→F₂] | **✓ 1908** Dronperminov-Q | — | — | **1908** in F₂, R/Q/Z | +68914 | — |
| `⟨13,16,16⟩` | **✓ 2038** Dronperminov-ZT [Z→F₂] | **✓ 2038** Dronperminov-ZT | — | — | **2038** in F₂, R/Q/Z | +41676 | — |
| `⟨14,14,16⟩` | **✓ 1943** Dronperminov-ZT [Z→F₂] | **✓ 1931** Dronperminov-Q | — | — | **1931** in R/Q/Z | +53324 | — |
| `⟨14,15,16⟩` | **✓ 2043** Dronperminov-ZT [Z→F₂] | **✓ 2043** Dronperminov-ZT | — | — | **2043** in F₂, R/Q/Z | +59266 | — |
| `⟨14,16,16⟩` | **✓ 2170** Dronperminov-ZT [Z→F₂] | **✓ 2128** Dronperminov-Q | — | — | **2128** in R/Q/Z | +46796 | — |
| `⟨15,15,16⟩` | **✓ 2132** Dronperminov-ZT [Z→F₂] | **✓ 2132** Dronperminov-ZT | — | — | **2132** in F₂, R/Q/Z | +46964 | — |
| `⟨15,16,16⟩` | **✓ 2302** Dronperminov-ZT [Z→F₂] | **✓ 2302** Dronperminov-ZT | — | — | **2302** in F₂, R/Q/Z | +51980 | — |
| `⟨16,16,16⟩` | **✓ 2209** Composed-ATf2-squared | **✓ 2401** Dronperminov-ZT | **✓ 2304** Composed-AE2 | — | **2209** in F₂ | +62850 | — |

---

## How to fill gaps

- A `📄` cell becomes `✓` once a scheme file is committed to
  `src/main/resources/schemes/` and round-trips through `SchemeIO` + `Verifier`.
- A `—` cell becomes `📄` once an entry is added to
  `io.cormoran.strassen.v3.catalog.KnownAlgorithmCatalog`.
- Important format-field cells we know exist but don't have schemes for:
  AlphaTensor's full F₂ result set (~50 schemes), Smirnov's `{-1,0,+1}` catalog
  for `⟨6,6,6⟩` / `⟨7,7,7⟩` / etc.
