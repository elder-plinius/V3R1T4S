# run: python3 -I code/export_arrays.py <wikstrom_src> <out.json>  (system python, numpy; allow_pickle=False; untrusted data)
import sys, json
import numpy as np
src, out = sys.argv[1], sys.argv[2]
def nz(lam, gam):
    idx = np.nonzero(lam)[0]
    return idx.tolist(), [float(lam[i]).hex() for i in idx], [float(gam[i]).hex() for i in idx]
D = {"cuts": [], "extra": []}
m = np.load(src+"/multicut_certificate.npz", allow_pickle=False)
v = np.load(src+"/variable_radius_certificate.npz", allow_pickle=False)
c = np.load(src+"/certificates.npz", allow_pickle=False)
cc = np.load(src+"/certificates_coarse.npz", allow_pickle=False)
def rows(z, idx):
    return [float(z["rho"][i]).hex() for i in idx], [float(z["psi"][i]).hex() for i in idx]
def add(lst, z, name, lam, gam, K):
    idx, l, g = nz(lam, gam)
    r, p = rows(z, idx)
    lst.append(dict(name=name, K=int(K), lam=l, gam=g, rho=r, psi=p, minlam=float(lam.min()), maxrho=float(z["rho"][idx].max()) if idx else 0.0))
for i in range(m["lams"].shape[0]):
    add(D["cuts"], m, "multicut%d"%i, m["lams"][i], m["gams"][i], m["K"])
for i in range(v["away_lams"].shape[0]):
    add(D["cuts"], v, "away%d"%i, v["away_lams"][i], v["away_gams"][i], v["K"])
n = c["gam_glob"].shape[0]
lg = c["lam_glob"].reshape(n, -1)
for i in range(n):
    add(D["extra"], c, "glob%d"%i, lg[i], c["gam_glob"][i], c["K"])
n = cc["gam_glob"].shape[0]
lg = cc["lam_glob"].reshape(n, -1)
for i in range(n):
    add(D["extra"], cc, "cglob%d"%i, lg[i], cc["gam_glob"][i], cc["K"])
add(D["extra"], c, "phi", c["lam_phi"], c["gam_phi"], c["K"])
idx, l, g = nz(c["lam_a3"], c["gam_a3"])
r, p = rows(c, idx)
D["a3"] = dict(K=int(c["K"]), lam=l, gam=g, rho=r, psi=p, minlam=float(c["lam_a3"].min()))
D["eta"] = float(v["eta"]).hex(); D["C"] = float(v["C"]).hex()
D["anchors_multi"] = m["anchors"].tolist(); D["anchors_away"] = v["away_anchors"].tolist()
json.dump(D, open(out, "w"))
print("cuts", len(D["cuts"]), "extra", len(D["extra"]), "nnz first", len(D["cuts"][0]["lam"]), "a3 nnz", len(D["a3"]["lam"]), "minlam", min(x["minlam"] for x in D["cuts"]), D["a3"]["minlam"], "maxrho", max(x["maxrho"] for x in D["cuts"]))
