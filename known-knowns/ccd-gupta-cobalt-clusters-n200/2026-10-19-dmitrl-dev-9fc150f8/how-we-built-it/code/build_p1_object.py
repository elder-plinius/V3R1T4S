#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Build object/ccd_cobalt_audit.csv (partial win p1) from the three CCD files in DATA_DIR. Needs numpy and scipy.
    python3 build_p1_object.py DATA_DIR OUT_CSV
Same potential and polish as audit_ccd_cobalt.py; one row per N = 2..200."""
import csv, sys
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util, os
spec = importlib.util.spec_from_file_location("au", os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_ccd_cobalt.py"))
au = importlib.util.module_from_spec(spec); spec.loader.exec_module(au)
import html, re, tarfile, zipfile
ddir, out = sys.argv[1], sys.argv[2]
page = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", open(ddir + "/cobalt.html", "rb").read().decode("latin-1"))).split())
tab_txt = page[page.find("N PG Energy / eV"):]
posted = {}
for n, pg, en in re.findall(r"(?<![\d.])(\d{1,3}) ((?:[A-Z][a-z]* ?(?:\d+[vhd]?|infh|[vhds])?|C s|C 1|C i|O h|T d|I h|D infh)) (-\d+\.\d+)", tab_txt):
    if 2 <= int(n) <= 200 and int(n) not in posted:
        posted[int(n)] = (pg.strip(), en)
tf = tarfile.open(ddir + "/points.tgz", "r:gz")
tab = {int(m.name.split("/")[-1]): au.load(tf.extractfile(m).read().decode()) for m in tf.getmembers() if m.isfile()}
zf = zipfile.ZipFile(ddir + "/Co.zip")
zx = {int(re.search(r"Co(\d+)\.txt", i.filename).group(1)): au.load(zf.read(i).decode()) for i in zf.infolist() if re.search(r"Co\d+\.txt", i.filename)}
zE = {int(a): b for a, b in re.findall(r"Co(\d+)\s*:\s*(-\d+\.\d+)", zf.read("Co/Energy.txt").decode())}
cols = ["N", "point_group", "E_table_posted", "E_table_as_is", "as_is_off_by_more_than_1e-5", "E_table_polished",
        "polished_within_1e-5", "polishes_lower_by_more_than_1e-4", "E_coZip_posted", "E_coZip_as_is", "E_best", "best_source"]
with open(out, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(cols)
    for n in range(2, 201):
        e0 = au.e_g(tab[n])[0]; _, ep, _ = au.polish(tab[n]); pe = float(posted[n][1])
        eb, src, ezp_s, ez0_s = ep, "table", "", ""
        if n in zx:
            ez0 = au.e_g(zx[n])[0]; _, ezp, _ = au.polish(zx[n]); ez0_s = "%.9f" % ez0
            if ezp < ep: eb, src = ezp, "Co.zip"
        w.writerow([n, posted[n][0], posted[n][1], "%.9f" % e0, "yes" if abs(e0 - pe) > 1e-5 else "no", "%.7f" % ep,
                    "yes" if abs(ep - pe) <= 1e-5 else "no", "yes" if ep < pe - 1e-4 else "no", zE.get(n, ""), ez0_s, "%.7f" % eb, src])
print("wrote", out)
