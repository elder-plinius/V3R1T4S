"""Assemble outbox/<submission-id>/ from attempts/contrarian/package_draft and the run's files (kit/SUBMIT.md section 1).
Only for a CONFIRMED_* gate. usage: python build_package.py <workdir>"""
import os, sys, shutil, glob, hashlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DRAFT = os.path.join(RUN, "attempts", "contrarian", "package_draft")
WORK = sys.argv[1]
settings = open(os.path.join(WORK, "settings.md"), encoding="utf-8").read()
credit = re.search(r"(?m)^credit:\s*(\S+)", settings).group(1).lower()
gate = open(os.path.join(RUN, "panel", "gate.md"), encoding="utf-8").read()
assert re.search(r"(?m)^status:\s*CONFIRMED_", gate), "gate is not CONFIRMED_*"
scope = re.search(r"(?m)^confirmed_scope:\s*(.+)$", gate).group(1).strip()
main_obj = os.path.join(DRAFT, "object", "forecasts_sha256.txt")
h8 = hashlib.sha256(open(main_obj, "rb").read()).hexdigest()[:8]
date = re.search(r"(?m)^date:\s*(\S+)", gate).group(1)
sid = "%s-%s-%s" % (date, credit, h8)
P = os.path.join(WORK, "outbox", sid)
if os.path.exists(P):
    shutil.rmtree(P)
shutil.copytree(DRAFT, P)


def cp(src, dst):
    os.makedirs(os.path.dirname(os.path.join(P, dst)), exist_ok=True)
    shutil.copyfile(src, os.path.join(P, dst))


F = os.path.join(RUN, "attempts", "forecaster"); E = os.path.join(RUN, "attempts", "evaluator")
C = os.path.join(RUN, "attempts", "contrarian")
for f in ["model_rsv.py", "asof_rsv.py", "run_season.py", "make_submission.py", "dev_eval.py", "run_batch.py"]:
    cp(os.path.join(F, "code", f), "how-we-built-it/forecaster/" + f)
for f in ["FROZEN_PARAMS.json", "METHOD_FREEZE.md", "freeze_hashes.txt", "freeze_hashes_v3.txt", "freeze_hashes_v4.txt",
          "forecasts_sha256.txt", "submission_sha256.txt"]:
    cp(os.path.join(F, f), "how-we-built-it/forecaster/" + f)
cp(os.path.join(F, "work", "dev", "dev_results.jsonl"), "how-we-built-it/forecaster/dev_results_2023-24.jsonl")
cp(os.path.join(F, "result", "forecasts", "read_log.csv"), "how-we-built-it/forecaster/read_log_2024-25.csv")
for f in ["wis.py", "score.py", "score_test.py", "parse_mo.py", "baseline_dev.py", "task_sets.py", "fetch_list.sh"]:
    cp(os.path.join(E, "code", f), "how-we-built-it/evaluator/" + f)
for f in ["score_test_2024-25.log", "score_2023-24_descriptive.log"]:
    cp(os.path.join(E, "test", f), "how-we-built-it/evaluator/" + f)
for f in ["lookahead_audit.py", "validate_format.py", "sensitivity.py", "refetch_check.py", "build_claim.py", "build_package.py"]:
    cp(os.path.join(C, "code", f), "how-we-built-it/contrarian/" + f)
for f in ["lookahead_audit.txt", "validate_format.txt", "sensitivity.txt"]:
    cp(os.path.join(C, "out", f), "how-we-built-it/contrarian/" + f)
for f in ["PREREG.md", "PREREG.v2.md", "PREREG.v3.md", "PREREG.v4.md"]:
    cp(os.path.join(RUN, f), "how-we-built-it/" + f)
for p in glob.glob(os.path.join(RUN, "baseline", "*")):
    cp(p, "how-we-built-it/baseline/" + os.path.basename(p))
cp(os.path.join(RUN, "data", "hopkins", "fetch_list_vintages.tsv"), "how-we-built-it/inputs_vintages_pinned.tsv")
cp(os.path.join(RUN, "data", "hopkins", "fetch_list_modeloutput.tsv"), "how-we-built-it/inputs_modeloutput_pinned.tsv")
for r in ["reproduce", "novelty", "criterion", "gate"]:
    cp(os.path.join(RUN, "panel", r + ".md"), "panel/%s.md" % r)
# README "What" gets the confirmed scope verbatim
rd = open(os.path.join(P, "README.md"), encoding="utf-8").read().replace("<<CONFIRMED_SCOPE>>", scope)
open(os.path.join(P, "README.md"), "w", encoding="utf-8").write(rd)
for p in glob.glob(os.path.join(P, "**", "__pycache__"), recursive=True):
    shutil.rmtree(p, ignore_errors=True)
for p in glob.glob(os.path.join(P, "**", "*.pyc"), recursive=True):
    os.remove(p)
lines = []
for root, _, fs in os.walk(P):
    for f in sorted(fs):
        rp = os.path.relpath(os.path.join(root, f), P).replace(os.sep, "/")
        if rp == "SHA256SUMS":
            continue
        lines.append("%s  %s" % (hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest(), rp))
open(os.path.join(P, "SHA256SUMS"), "w").write("\n".join(sorted(lines, key=lambda l: l.split("  ")[1])) + "\n")
print(sid)
