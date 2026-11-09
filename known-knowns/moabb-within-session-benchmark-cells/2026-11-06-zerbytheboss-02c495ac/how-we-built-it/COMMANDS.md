# Exact Commands Executed

```bash
# 1. Run official MOABB WithinSessionEvaluation on FB_HTR_SSVEP across Kalunga2016, Nakanishi2015, and MAMEM3
PYTHONPATH=how-we-built-it python3 -c '
from moabb.datasets import Kalunga2016, Nakanishi2015, MAMEM3
from moabb.paradigms import SSVEP
from moabb.evaluations import WithinSessionEvaluation
from fb_htr_ssvep import make_fb_htr_ssvep_pipeline

ev = WithinSessionEvaluation(
    paradigm=SSVEP(),
    datasets=[Kalunga2016(), Nakanishi2015(), MAMEM3()],
    overwrite=True,
    random_state=42,
)
res = ev.process({"FB_HTR_SSVEP": make_fb_htr_ssvep_pipeline()})
for ds in ["Kalunga2016", "Nakanishi2015", "MAMEM3"]:
    g = res[res["dataset"] == ds]
    print(ds, f"{g[\x27score\x27].mean()*100:.2f} +/- {g[\x27score\x27].std(ddof=0)*100:.2f}")
'

# 2. Rebuild object/moabb_ssvep_within_session_cells.csv and verify-it-yourself/data/moabb_ssvep_fold_witness.json.gz
PYTHONPATH=how-we-built-it python3 how-we-built-it/export_moabb_witness.py

# 3. Run the standalone pure-stdlib package verifier
sh verify-it-yourself/run_checks.sh
```
