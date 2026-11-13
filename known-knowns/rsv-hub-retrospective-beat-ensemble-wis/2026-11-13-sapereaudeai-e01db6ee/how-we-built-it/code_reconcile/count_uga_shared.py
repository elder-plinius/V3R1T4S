"""Units shared by RSVHub-ensemble and UGA_flucast-INFLAenza (hosp, horizons 0-3), and how many are Puerto Rico.
usage: python -I count_uga_shared.py HUB OUT"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubload import load_models
w = load_models(sys.argv[1], models=["RSVHub-ensemble", "UGA_flucast-INFLAenza"])
w = w[(w["target"] == "wk inc rsv hosp") & w["horizon"].between(0, 3)]
k = ["reference_date", "location", "horizon", "target_end_date"]
c = w[w["model"] == "RSVHub-ensemble"][k].merge(w[w["model"] == "UGA_flucast-INFLAenza"][k], on=k)
line = "hosp units shared by RSVHub-ensemble and UGA_flucast-INFLAenza at horizons 0-3: %d, of which location 72 (Puerto Rico): %d, outside Puerto Rico: %d" % (len(c), int((c["location"] == "72").sum()), int((c["location"] != "72").sum()))
open(sys.argv[2], "w", newline="\n").write(line + "\n"); print(line)
