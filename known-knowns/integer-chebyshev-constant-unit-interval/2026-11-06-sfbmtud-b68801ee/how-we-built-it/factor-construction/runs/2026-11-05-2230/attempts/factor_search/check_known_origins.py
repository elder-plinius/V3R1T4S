"""Check supplied-library origins against the exact final integer factors."""
import argparse,hashlib,json,time
from pathlib import Path
from flint import fmpz_poly
B=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--candidate',default='claim/candidate.json');ap.add_argument('--output',default='known_origins_result.json');args=ap.parse_args()
start=time.perf_counter();candidate_path=Path(args.candidate);candidate=json.loads(candidate_path.read_text());P=json.loads((B/'provenance_final.json').read_text());U=json.loads((B.parent.parent/'data/upper_certificate.json').read_text());assert hashlib.sha256(candidate_path.read_bytes()).hexdigest()==P['candidate_sha256']
X=fmpz_poly([0,1]);W=X-X*X;rows=[]
for f in P['factors']:
    index=f['candidate_factor_index'];coeffs=f['coeffs_desc_w'];assert candidate['factors'][index]['coeffs_desc_w']==coeffs
    if f['source_class']=='shipped_upper':
        assert U['factors'][f['source_upper_index']]['coeffs_desc_w']==coeffs
        rows.append({'candidate_factor_index':index,'method':'exact_original_coefficient_equality','pass':True})
    elif f['source_class']=='shipped_lower_symmetry_transport':
        q=fmpz_poly(f['origin']['coeffs_desc_x'][::-1]);r=fmpz_poly(coeffs[::-1]);product=q*q(1-X);composed=r(W);quotient,remainder=divmod(product,composed);assert not remainder and composed*quotient==product
        rows.append({'candidate_factor_index':index,'method':'exact_divisibility_in_Qx_times_Q1minusx','pass':True})
R={'candidate_sha256':P['candidate_sha256'],'all_known_origins_valid':True,'checked_factors':len(rows),'factors':rows,'elapsed_seconds':time.perf_counter()-start,'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};Path(args.output).write_text(json.dumps(R,indent=2));print({k:v for k,v in R.items() if k!='factors'})
