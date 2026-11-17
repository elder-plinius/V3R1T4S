"""Assemble claim/ for the panel: the same relative layout as the run folder so the code runs unchanged from claim/.
Copies (not links) every input the checks need. usage: python build_claim.py"""
import os, shutil, glob
HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
C = os.path.join(RUN, "claim")

def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)

if os.path.exists(C):
    raise SystemExit("claim/ exists; remove it first")
H = os.path.join(RUN, "data", "hopkins")
for p in glob.glob(os.path.join(H, "hub", "model-output", "*", "*")):
    cp(p, os.path.join(C, os.path.relpath(p, RUN)))
for p in glob.glob(os.path.join(H, "hub", "target-data", "archive", "*.csv")) + \
         [os.path.join(H, "hub", "target-data", "2026-06-05_rsvnet_hospitalization.csv")] + \
         glob.glob(os.path.join(H, "hub", "model-metadata", "*")) + glob.glob(os.path.join(H, "hub", "auxiliary-data", "location_census", "*")):
    cp(p, os.path.join(C, os.path.relpath(p, RUN)))
for f in ["hub-config_tasks.json", "hub-config_tasks.json_2023-24", "hub-config_tasks.json_29Feb2024", "tree_main.json",
          "ls_remote.txt", "scripts_ensemble.R", "scripts_retro_ensemble.R", "predsci_fork_README.md", "README.md",
          "target-data_README.md", "model-output_README.md", "fetch_list_vintages.tsv", "fetch_list_modeloutput.tsv",
          "fetch_log.tsv", "fetch_log_vintages.tsv"]:
    cp(os.path.join(H, f), os.path.join(C, "data", "hopkins", f))
cp(os.path.join(RUN, "data", "status_RSVHub-ensemble_tree.html"), os.path.join(C, "data", "status_RSVHub-ensemble_tree.html"))
F = os.path.join(RUN, "attempts", "forecaster")
for f in ["code/model_rsv.py", "code/asof_rsv.py", "code/run_season.py", "FROZEN_PARAMS.json", "METHOD_FREEZE.md",
          "freeze_hashes.txt", "freeze_hashes_v3.txt", "freeze_hashes_v4.txt", "forecasts_sha256.txt"]:
    cp(os.path.join(F, f), os.path.join(C, "attempts", "forecaster", f))
for p in glob.glob(os.path.join(F, "result", "forecasts", "*")):
    cp(p, os.path.join(C, os.path.relpath(p, RUN)))
E = os.path.join(RUN, "attempts", "evaluator")
for f in ["code/wis.py", "code/score.py", "code/score_test.py", "code/parse_mo.py", "code/fetch_list.sh",
          "test/score_test_2024-25.log", "test/2024-25_summary.txt", "wis_selftest.txt", "task_sets.txt",
          "hub_season_wis_2024-25.txt"]:
    cp(os.path.join(E, f), os.path.join(C, "attempts", "evaluator", f))
for f in ["code/lookahead_audit.py", "code/sensitivity.py", "code/refetch_check.py"]:
    cp(os.path.join(RUN, "attempts", "contrarian", f), os.path.join(C, "attempts", "contrarian", f))
for f in ["PREREG.md", "PREREG.v2.md", "PREREG.v3.md", "PREREG.v4.md", "target.md", "scout.md"]:
    cp(os.path.join(RUN, f), os.path.join(C, f))
for p in glob.glob(os.path.join(RUN, "baseline", "*")):
    cp(p, os.path.join(C, "baseline", os.path.basename(p)))
print("claim built:", sum(len(fs) for _, _, fs in os.walk(C)), "files")
