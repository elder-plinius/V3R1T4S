#!/usr/bin/env python3
"""One-command repro: ssp radius.txt vs ssp.html vs coordinate files (stdlib + mpmath).
usage: python3 repro_ssp_radiustxt.py            # fetches the 3 live sources from packomania.com
       python3 repro_ssp_radiustxt.py --local DIR # uses DIR/radius.txt DIR/ssp.html DIR/ssp_coords.tar.gz
Feasible radius r* = min(min_ij |ci-cj|/2, 1 - max_i |ci|) (container radius 1), mpmath mp.dps=50 on
candidate pairs/centers selected by a float cell-list prefilter (window 1e-9). Margin 1e-10 (12-decimal files).
Prints: N radius_txt ssp_html coord_r* gap(coord-radius_txt) binding html-coord, html==coord within 1e-10 verdict"""
import sys,re,io,tarfile,hashlib,urllib.request,datetime,math
import mpmath as mp
mp.mp.dps=50
NS=[1055,1061,1157,1205,1253,1289,1409,1433,1481,1505,1553,1601,1721,1745,1865,1961,1985,2000,2093,2123,2171,2243,2315,2347,2491,2587,2659,2731,2779,2899,3000,3043,3055,3103,3151,3319,3367,3463,3511,3559,3589,3781,3805,3925,3997,4000,4093,4189,4213,4321,4417,4537,4585,4729,4753,4897,4921,5000,5017,5089,5233,5281,5425,5473,5481,5721,5775,5895,5979,6000,6051,6099,6339,6363,6459,6531,6603,7000,8000,9000,9909,10000,10005,20000,20113,30000,30093,40000,40143,50000]
BASE='https://packomania.com/ssp/'
def get(name,url):
    if '--local' in sys.argv:
        b=open(sys.argv[sys.argv.index('--local')+1]+'/'+name,'rb').read(); src='local'
    else:
        r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'V3R1T4S-repro'}),timeout=600); b=r.read(); src=f'HTTP {r.status}'
    print(f'# {name} {src} {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")} sha256 {hashlib.sha256(b).hexdigest()} bytes {len(b)}')
    return b
rad=get('radius.txt',BASE+'txt/radius.txt').decode(); html=get('ssp.html',BASE+'ssp.html').decode('latin-1')
tgz=get('ssp_coords.tar.gz',BASE+'txt/ssp_coords.tar.gz')
RT={int(l.split()[0]):l.split()[1] for l in rad.splitlines() if l.strip() and not l.startswith('#')}
HT={}
for m in re.finditer(r'name="ssp(\d+)">.*?</a></td>\s*<td>(?:&nbsp;)*\s*([0-9.]+)',html): HT[int(m.group(1))]=m.group(2)
want={f'ssp{n}.txt':n for n in NS}; CO={}
with tarfile.open(fileobj=io.BytesIO(tgz)) as tf:
    for m in tf:
        b=m.name.split('/')[-1]
        if b in want: CO[want[b]]=tf.extractfile(m).read().decode()
def rstar(txt):
    S=[]
    for l in txt.splitlines():
        t=l.split()
        if l.startswith('#') or len(t)<4: continue
        S.append(t[1:4])
    F=[tuple(map(float,s)) for s in S]; n=len(F)
    # wall
    nf=[math.sqrt(x*x+y*y+z*z) for x,y,z in F]; mx=max(nf)
    wall=min(1-mp.sqrt(sum(mp.mpf(v)**2 for v in S[i])) for i in range(n) if nf[i]>mx-1e-9)
    # float nearest distance via cell list
    h=2.2*(1/ n**(1/3)); cells={}
    for i,(x,y,z) in enumerate(F): cells.setdefault((int((x+2)//h),int((y+2)//h),int((z+2)//h)),[]).append(i)
    def near(lim):
        out=[]
        for (a,b,c),L in cells.items():
            for da in (-1,0,1):
                for db in (-1,0,1):
                    for dc in (-1,0,1):
                        M=cells.get((a+da,b+db,c+dc))
                        if not M: continue
                        for i in L:
                            for j in M:
                                if j>i:
                                    d=math.dist(F[i],F[j])
                                    if d<lim: out.append((d,i,j))
        return out
    P=near(h); dmin=min(p[0] for p in P)
    pair=min(mp.sqrt(sum((mp.mpf(S[i][k])-mp.mpf(S[j][k]))**2 for k in range(3))) for d,i,j in P if d<dmin+1e-9)/2
    return n,min(pair,wall),('pair' if pair<wall else 'wall')
print('N\tradius_txt\tssp_html\tcoord_rstar\tgap_coord_minus_radiustxt\tbinding\thtml_minus_coord\thtml_eq_coord_within_1e-10\tverdict')
bad=0
for n in NS:
    cnt,r,bind=rstar(CO[n]); t=mp.mpf(RT[n]); h=HT.get(n,'MISSING'); gap=r-t
    heq= h!='MISSING' and abs(mp.mpf(h)-r)<=mp.mpf('1e-10')
    v='RADIUSTXT_ERRATUM' if (gap< -mp.mpf('1e-10') and heq and cnt==n) else 'NOT_CONFIRMED'
    bad+= v!='RADIUSTXT_ERRATUM'
    print(f'{n}\t{RT[n]}\t{h}\t{mp.nstr(r,25)}\t{mp.nstr(gap,6)}\t{bind}\t{mp.nstr(mp.mpf(h)-r,4) if h!='MISSING' else ''}\t{heq}\t{v}')
print(f'# rows {len(NS)} confirmed {len(NS)-bad} not_confirmed {bad}'); print('PASS' if bad==0 else 'FAIL')
