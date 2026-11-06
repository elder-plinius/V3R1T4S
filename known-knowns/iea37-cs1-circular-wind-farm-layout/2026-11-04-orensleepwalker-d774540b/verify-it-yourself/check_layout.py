"""Portable standard-library verifier for one frozen IEA37 CS1 64-turbine full-criterion object.

Physics: Baker, Stanley, Thomas, Ning and Dykes, AIAA 2019-0540.
Comparator files are fetched from pinned public commits and hash-checked, never
executed. This script verifies numeric eligibility, not literature novelty.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile
import urllib.request

OBJECT_SHA256 = 'd774540b96ab9d9db5a2b164e8c97e3222dc78ca62c1fbbdcc04ce4993645dc5'
EXPECTED_AEP = 1543800.4664981714
N, RADIUS = 64, 3000.
P1_THRESHOLD = 1526474.8025 + 0.01  # posted record + 0.01 (full criterion)
FREQUENCIES = [.025,.024,.029,.036,.063,.065,.100,.122,.063,.038,.039,.083,.213,.046,.032,.022]
REFERENCES = {
    'participant12': {
        'url':'https://raw.githubusercontent.com/IEAWindSystems/iea37-wflo-casestudies/267f6e5d2906400b2ee0a8ff533da7ebcc4bb47a/cs1-2/iea37-cs1-results/iea37-par12-opt64.yaml',
        'sha256':'7e643ef74c61cc2a2af8a93afd2bfb6b9737091ad8a52c8984c2bafa343b9fae',
        'filename':'iea37-par12-opt64.yaml'},
    'PR938': {
        'url':'https://raw.githubusercontent.com/Jimbootgit/V3R1T4S/9f1145de2f2c98d686f9ca7b74ffca6cab6c467d/known-knowns/iea37-cs1-circular-wind-farm-layout/2026-10-18-anonymous-f1a4e0d0-d63ed6df/object/iea37-v3r1t4s-opt64.yaml',
        'sha256':'d63ed6df76fcbf03297cdb171acda406f597bfc959b1610711dc0d68dd93c851',
        'filename':'pr938-opt64.yaml'}
}


def finite_points(obj):
    p = obj['coordinates_m'] if 'coordinates_m' in obj else list(zip(obj['x'],obj['y']))
    if len(p)!=N or any(len(x)!=2 or any(not math.isfinite(z) for z in x) for x in p):
        raise ValueError('expected exactly %d finite coordinate pairs' % N)
    return p


def reference(entry, directory=None):
    cache = Path(tempfile.gettempdir())/'iea37-public-reference-cache'
    path = directory/entry['filename'] if directory else cache/entry['sha256']
    if path.exists():
        data = path.read_bytes()
    elif directory:
        raise ValueError('missing local reference '+entry['filename'])
    else:
        # One honest request. No retries or bypasses on denial or challenge.
        request = urllib.request.Request(entry['url'],headers={'User-Agent':'V3R1T4S-layout-verifier'})
        with urllib.request.urlopen(request,timeout=30) as response:
            if response.status!=200:raise ValueError('reference HTTP '+str(response.status))
            data = response.read(1_000_001)
        if len(data)>1_000_000:raise ValueError('oversized reference')
        if hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise ValueError('downloaded reference hash mismatch')
        cache.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    if hashlib.sha256(data).hexdigest()!=entry['sha256']:
        raise ValueError('reference hash mismatch: '+entry['filename'])
    text=data.decode('utf-8')
    if entry['filename'].endswith('.json'):return finite_points(json.loads(text))
    def array(key):
        values=re.findall(r'(?m)^\s*'+key+r':\s*\[([^]]*)\]',text)
        if len(values)!=1:raise ValueError('ambiguous coordinate block')
        return [float(x) for x in values[0].replace('\n','').split(',') if x.strip()]
    x,y=array('xc'),array('yc')
    if len(x)!=len(y):raise ValueError('coordinate array length mismatch')
    return finite_points({'x':x,'y':y})


def geometry(points):
    radius=max(math.sqrt(x*x+y*y) for x,y in points)
    spacing=min(math.sqrt((x-u)**2+(y-v)**2)
                for i,(x,y) in enumerate(points) for u,v in points[:i])
    return {'maximum_radius_m':radius,'minimum_spacing_m':spacing,
            'strictly_feasible':radius<=RADIUS and spacing>=260.}


def aep(points, offset=0.):
    bins=[]
    for k,freq in enumerate(FREQUENCIES):
        a=math.radians(k*22.5+offset-270);co,si=math.cos(a),math.sin(a)
        q=[(co*x-si*y,si*x+co*y) for x,y in points]
        powers=[]
        for x,y in q:
            losses=[]
            for u,v in q:
                dx=x-u
                if dx>0:
                    sigma=.0324555*dx+130/math.sqrt(8)
                    d=(1-math.sqrt(1-(8/9)*130**2/(8*sigma**2)))*math.exp(-.5*((y-v)/sigma)**2)
                    losses.append(d*d)
            velocity=9.8*(1-math.sqrt(sum(losses)))
            power=3.35*((velocity-4)/5.8)**3 if 4<=velocity<9.8 else (3.35 if 9.8<=velocity<25 else 0.)
            powers.append(power)
        bins.append(8760*freq*sum(powers))
    return sum(bins),bins


def matching(points,other):
    n=len(points)
    cost=[[math.dist(a,b) for b in other] for a in points]
    # Standard primal-dual Hungarian algorithm; return its certificate too.
    u,v=[0.]*(n+1),[0.]*(n+1)
    p,way=[0]*(n+1),[0]*(n+1)
    for i in range(1,n+1):
        p[0]=i;j0=0;minimum=[math.inf]*(n+1);used=[False]*(n+1)
        while True:
            used[j0]=True;i0=p[j0];delta=math.inf;j1=0
            for j in range(1,n+1):
                if not used[j]:
                    value=cost[i0-1][j-1]-u[i0]-v[j]
                    if value<minimum[j]:minimum[j]=value;way[j]=j0
                    if minimum[j]<delta:delta=minimum[j];j1=j
            for j in range(n+1):
                if used[j]:u[p[j]]+=delta;v[j]-=delta
                else:minimum[j]-=delta
            j0=j1
            if p[j0]==0:break
        while j0:
            j1=way[j0];p[j0]=p[j1];j0=j1
    columns=[0]*n
    for j in range(1,n+1):columns[p[j]-1]=j-1
    distances=[cost[i][columns[i]] for i in range(n)]
    primal=sum(distances);dual=sum(u[1:])+sum(v[1:])
    violation=max(u[i+1]+v[j+1]-cost[i][j] for i in range(n) for j in range(n))
    if abs(primal-dual)>1e-8 or violation>1e-8:raise ValueError('assignment certificate invalid')
    return {'columns':columns,'distances_m':distances,'farther_than_50m':sum(d>50. for d in distances),
            'total_distance_m':primal,'dual_value_m':dual,'dual_violation_m':violation}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--object',type=Path,default=Path(__file__).resolve().parents[1]/'object/layout.json')
    parser.add_argument('--reference-dir',type=Path)
    args=parser.parse_args()
    data=args.object.read_bytes()
    if hashlib.sha256(data).hexdigest()!=OBJECT_SHA256:raise ValueError('frozen object hash mismatch')
    points=finite_points(json.loads(data))
    g=geometry(points)
    if not g['strictly_feasible']:raise ValueError('strict geometry failed')
    total,bins=aep(points)
    if abs(total-EXPECTED_AEP)>1e-4 or total<P1_THRESHOLD:raise ValueError('AEP criterion failed')
    refs={name:reference(entry,args.reference_dir) for name,entry in REFERENCES.items()}
    matches={name:matching(points,p) for name,p in refs.items()}
    others={name:aep(p)[0] for name,p in refs.items()}
    if total<=max(others.values()):raise ValueError('object does not exceed every comparator')
    print(json.dumps({'AEP_MWh':total,'directional_AEP_MWh':bins,'geometry':g,'matchings':{k:{kk:v[kk] for kk in ('farther_than_50m','total_distance_m')} for k,v in matches.items()},
                      'comparator_AEP_MWh':others,'margin_over_posted_record_MWh':total-1526474.8025,'scope':'Full criterion (64 turbines): strict feasibility, AEP above posted record + 0.01, and above hash-pinned participant 12 and PR #938 layouts (recomputed); see panel for novelty.'},indent=2))
    print('PASS')


if __name__=='__main__':
    try:main()
    except Exception as error:
        print('FAIL:',error)
        raise SystemExit(1)
