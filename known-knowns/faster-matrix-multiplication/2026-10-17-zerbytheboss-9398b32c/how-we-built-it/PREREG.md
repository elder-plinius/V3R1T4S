# Pre-Registration — `fmm-additive-complexity-records` (`4x5x5`)

date_utc: 2026-10-17T15:00:00Z
target_id: fmm-additive-complexity-records
null_test: not needed because exact symbolic polynomial identity verification over Z and straight-line program DAG addition counting are deterministic with zero statistical error
statistic: reduced addition count cr = len(u_fresh) + sum(len(x)-1 for x in u) + len(v_fresh) + sum(len(x)-1 for x in v) + len(w_fresh) + sum(len(x)-1 for x in w)
threshold: cr < 281 (strictly beating both Perminov's live 299 and merged PR #222 at 281 at exact SOTA rank 76)
