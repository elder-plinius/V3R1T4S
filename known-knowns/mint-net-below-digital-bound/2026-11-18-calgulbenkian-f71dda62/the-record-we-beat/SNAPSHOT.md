# Baseline Snapshot (`mint-net-below-digital-bound`, Partial Win `p1`)

- **Live MinT cell query**: http://mint.sbg.ac.at/query.php?b=3&s=19&m=11&p=smt
- **Fetched UTC**: `2026-11-17T15:18:00Z` (`HTTP 200`, `mint_b3_m11_s19.html` SHA-256 `9c138a9b22271f54ab1818ba33ecff9ed21603cce456cb91414caa924a1da399`)
- **Live MinT cell values**: `Best known t: 5`, `Lower bound on t (digital): 4`, `Lower bound on t: 3` (open non-digital gap `t = 3 < 4`)
- **MinT OOA LP documentation**: http://mint.sbg.ac.at/desc_OBoundLP.html (`HTTP 200`, SHA-256 `a878ed653883ad890fd2648a1a63655b23dbb7e8b48c38efdd2d035ea07b4404`) and http://mint.sbg.ac.at/history.php (`HTTP 200`, SHA-256 `cdcc1d082ff53527da9c6fd0c031e069febfedbfbe0a24fa46f3765b5e071cd6`)
- **New verified result (`p1`)**: Exact rational `OOA(M, 19, S_3, 4, 8)` LP dual certificate proving `M >= 2403828588527406331 / 13544324988667 > 177,147 = 3^11`, ruling out a `(3, 11, 19)`-net in base `3` and raising MinT's general lower bound on `t` from `3` to `4`.
