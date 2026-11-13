"""Produce hub-format forecast files of the frozen pipeline for every origin date of a hub round.
usage: python run_season.py <params.json> <out_dir> <season: 2024-25|2023-24> [origin ...]
Writes <out_dir>/<origin>-V3R1T4S-asofKA.csv (hub columns; output_type_id as 0.### levels) and <out_dir>/read_log.csv
(origin, vintage used, last data date read) for the look-ahead audit."""
import os, sys, json
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_rsv as M  # noqa: E402
import asof_rsv as A  # noqa: E402

RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CFG = {"2024-25": os.path.join(RUN, "data", "hopkins", "hub-config_tasks.json"),
       "2023-24": os.path.join(RUN, "data", "hopkins", "hub-config_tasks.json_2023-24")}

if __name__ == "__main__":
    params = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    season = sys.argv[3]
    os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 4:
        origins = sys.argv[4:]
    else:
        j = json.load(open(CFG[season]))
        od = j["rounds"][0]["model_tasks"][0]["task_ids"]["origin_date"]
        origins = sorted(set((od["required"] or []) + (od["optional"] or [])))
        origins = [o for o in origins if pd.Timestamp(o).dayofweek == 6]   # Sundays only
    for O in origins:
        df, info = M.forecast(O, params)
        df = df.drop(columns=["target_end_date"])
        df["output_type_id"] = df.output_type_id.map(lambda x: "%.3f" % x)
        df.to_csv(os.path.join(out, "%s-V3R1T4S-asofKA.csv" % O), index=False, float_format="%.6f")
        print(O, info["vintage"], info["T"], len(df), flush=True)
    pd.DataFrame(A.READ_LOG, columns=["origin_date", "vintage", "last_date_read"]).to_csv(os.path.join(out, "read_log.csv"), index=False)
