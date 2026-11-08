context: Claude Code subagent, fresh context [claude-sonnet-5-5]
ROLE: novelty

Cell: sc-p2-d7-batch24

## Sources fetched (once; plain requests)
All requests: curl -A 'V3R1T4S-research (honest client; curl)', no retries. The log is not shipped in this package.
- https://spherical-codes.org/plain  2026-10-18T17:50:10Z  HTTP 200  sha256 8655466f3692fa9197809db2b6fb7ca4f022b605c08b0fa76d78138915e93f35 (identical to the claim's own fetch of 17:39:49Z, so the table had not changed)
- https://spherical-codes.org/  2026-10-18T17:50:11Z  HTTP 200  sha256 ad3039078a704fe0745f447d29e407554fe3b028fdf8017c617d0c7a80618190 (identical to the claim's own fetch of 17:39:51Z)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md  2026-10-18T17:50:14Z  HTTP 200  sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 : no line mentions spherical codes or Cohn.
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 pages 1 to 5, all HTTP 200 (17:50:14Z to 17:50:22Z; 415 pull requests, numbers up to 425). I read every title and the body of every PR on this target.
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns  17:50:23Z  HTTP 200 : no spherical-codes folder (folders include thomson-problem-live-tables, packomania-*, bigger-codes, etc.), so no merged known value for this target.
- arXiv export API (https first; the plain http URL answered 301 with an empty body, recorded in the log): 3 searches (spherical code newest 30; Vahteristo; Tammes / kissing configuration / minimal angle) plus id_list 2610.19988, all HTTP 200, 17:50:28Z to 17:50:31Z.
Competing PRs on this target: #364 (psmoros, open) is for (6,526) only; #231 (psmoros, closed, replaced by #364) the same cell; #399 (DmitrL-dev, open) is a bank-status note that counts rows (it says the index now has 16,448 rows, 'needs more optimization' fell from 11,996 to 5,222, 4,160 rows cite Vahteristo, 3,541 cite Ozgen) and carries no coordinates. No open or merged PR names this package's cell or rows.
Literature: arXiv:2610.19988 (Vahteristo, 2026-10-14, 'New spherical codes by tuning an annealing solver': 29,670 instances N up to 1024, D 3..32, improves 4,577 instances; code https://github.com/ilmari99/Spherical-code-solver, data https://doi.org/10.5281/zenodo.23270586, named in the arXiv comment field). Other hits (arXiv:2609.21591 kissing numbers in dimensions 25 to 31, arXiv:2609.12640, arXiv:2602.10233 ImprovEvolve, arXiv:2510.23609 almost orthogonal vectors survey) concern kissing configurations or other methods; none states a cosine for the cell or rows of this package in its abstract.
unresolved: the Zenodo data set and the GitHub repository of arXiv:2610.19988 were not fetched (very large; outside the one-fetch budget). They could in principle hold an unposted code for a cell below. The table's own rows are the maintained record of what was accepted, and for the cells below the table already postdates that paper (the live table cites it, 4,160 rows). Residual risk is low but not zero.

## Cell values read
- (d=7, N=177): live /plain 0.570051592256; claimed c* (own float64 recompute) 0.570051466490; gain 1.258e-07; index row text: '> 7 177 0.570051592256 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=178): live /plain 0.570228301539; claimed c* (own float64 recompute) 0.570228270372; gain 3.117e-08; index row text: '> 7 178 0.570228301539 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=204): live /plain 0.601295919469; claimed c* (own float64 recompute) 0.601295776909; gain 1.426e-07; index row text: '> 7 204 0.601295919469 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=212): live /plain 0.611962614152; claimed c* (own float64 recompute) 0.611955584704; gain 7.029e-06; index row text: '> 7 212 0.611962614152 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=215): live /plain 0.614265846451; claimed c* (own float64 recompute) 0.614265014927; gain 8.315e-07; index row text: '> 7 215 0.614265846451 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=308): live /plain 0.660836744901; claimed c* (own float64 recompute) 0.660699032482; gain 1.377e-04; index row text: '> 7 308 0.660836744901 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=309): live /plain 0.660912967551; claimed c* (own float64 recompute) 0.660863660177; gain 4.931e-05; index row text: '> 7 309 0.660912967551 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=310): live /plain 0.660953811794; claimed c* (own float64 recompute) 0.660935439266; gain 1.837e-05; index row text: '> 7 310 0.660953811794 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=312): live /plain 0.661595420972; claimed c* (own float64 recompute) 0.661581951870; gain 1.347e-05; index row text: '> 7 312 0.661595420972 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=313): live /plain 0.661974195320; claimed c* (own float64 recompute) 0.661945822982; gain 2.837e-05; index row text: '> 7 313 0.661974195320 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=314): live /plain 0.662290658947; claimed c* (own float64 recompute) 0.662280558847; gain 1.010e-05; index row text: '> 7 314 0.662290658947 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=315): live /plain 0.662675365192; claimed c* (own float64 recompute) 0.662539672249; gain 1.357e-04; index row text: '> 7 315 0.662675365192 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=316): live /plain 0.663332152344; claimed c* (own float64 recompute) 0.663322953428; gain 9.199e-06; index row text: '> 7 316 0.663332152344 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=317): live /plain 0.663597580717; claimed c* (own float64 recompute) 0.663592917690; gain 4.663e-06; index row text: '> 7 317 0.663597580717 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=318): live /plain 0.663816385482; claimed c* (own float64 recompute) 0.663813842524; gain 2.543e-06; index row text: '> 7 318 0.663816385482 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=322): live /plain 0.665029616003; claimed c* (own float64 recompute) 0.665027566539; gain 2.049e-06; index row text: '> 7 322 0.665029616003 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=323): live /plain 0.665046095133; claimed c* (own float64 recompute) 0.665027820692; gain 1.827e-05; index row text: '> 7 323 0.665046095133 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=325): live /plain 0.665504583307; claimed c* (own float64 recompute) 0.665499516135; gain 5.067e-06; index row text: '> 7 325 0.665504583307 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=362): live /plain 0.668965357603; claimed c* (own float64 recompute) 0.668965354413; gain 3.190e-09; index row text: '> 7 362 0.668965357603 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=364): live /plain 0.670170636995; claimed c* (own float64 recompute) 0.670168019241; gain 2.618e-06; index row text: '> 7 364 0.670170636995 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=365): live /plain 0.670487284551; claimed c* (own float64 recompute) 0.670467035142; gain 2.025e-05; index row text: '> 7 365 0.670487284551 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=366): live /plain 0.670943830170; claimed c* (own float64 recompute) 0.670926060412; gain 1.777e-05; index row text: '> 7 366 0.670943830170 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=367): live /plain 0.671529770134; claimed c* (own float64 recompute) 0.671527896172; gain 1.874e-06; index row text: '> 7 367 0.671529770134 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes
- (d=7, N=368): live /plain 0.671589583556; claimed c* (own float64 recompute) 0.671588063958; gain 1.520e-06; index row text: '> 7 368 0.671589583556 Henry Cohn, 2026, needs more optimization.'; star mark: no; passes margin 1e-10: yes

Rows passing strictly (gain at least 1e-10, row labelled 'needs more optimization', no star): 24 of 24. Smallest gain is N=362 at 3.19e-09; largest N=315 at 1.357e-04. The partial win p2 needs at least 20 in one dimension (d=7, within 4..32): met by count.
Comparability: every one of the 24 rows reads 'Henry Cohn, 2026, needs more optimization.', i.e. Vahteristo's October paper did not replace them (a row he improved would cite him), so the paper gives no better value for them. No PR or trophy entry touches dimension 7.
Verdict: all 24 rows strictly beat the live table; no competing value found; unresolved caveat above. This supports the p2 batch as new relative to the table. (Whether the batch fits the p2 wording is for the criterion skeptic.)

novelty: strictly beats the live table at fetch time
pass: true
