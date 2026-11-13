"""Structural facts only (no values, no truth): task sets of hub-ensemble and of every model per season.
Season windows: 2023-24 = origin dates 2023-10-01 .. 2024-07-31; 2024-25 = 2024-10-01 .. 2025-07-31."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_mo import load_all  # noqa: E402

SEASONS = {"2023-24": ("2023-10-01", "2024-07-31"), "2024-25": ("2024-10-01", "2025-07-31")}

if __name__ == "__main__":
    d = load_all()
    d = d[d.output_type == "quantile"]
    for s, (a, b) in SEASONS.items():
        g = d[(d.origin_date >= a) & (d.origin_date <= b)]
        print("=== season", s)
        for m, h in g.groupby("model_id"):
            for retro, hh in h.groupby("retro"):
                tasks = hh.drop_duplicates(["origin_date", "horizon", "location", "age_group"])
                print("%-24s retro=%-5s files %2d origins %2d tasks %5d ages %s hz %s locs %d" % (
                    m, retro, hh.file.nunique(), hh.origin_date.nunique(), len(tasks), sorted(hh.age_group.unique()),
                    sorted(int(x) for x in hh.horizon.unique()), hh.location.nunique()))
        e = g[g.model_id == "hub-ensemble"]
        print("hub-ensemble origins:", sorted(e.origin_date.unique()))
        for (o, r), h in e.groupby(["origin_date", "retro"]):
            print("  ", o, "retro" if r else "rt   ", "ages", sorted(h.age_group.unique()), "locs", h.location.nunique(),
                  "hz", sorted(int(x) for x in h.horizon.unique()), "tasks", len(h.drop_duplicates(["horizon", "location", "age_group"])))
