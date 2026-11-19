#!/usr/bin/env python3
"""Harvest: compose + verify downstream still lifes from injected Dijkstra (fixed settle timing).
Fix vs compose_inject.py: settle time was sampled only at t in {256..4096} and each later stage assumed to settle
within a fixed --step=512. Seeds whose (far-rewound) synthesis RLE settles after 4096 gens, and stages that need >512 gens,
failed. Now: settle time searched adaptively (step 64, bound from pattern diameter) for the seed and after every stage."""
import sys, os, heapq, argparse, json, time, re, urllib.request, urllib.error
# Paths are supplied by the operator (no machine-absolute defaults).
# GLIDER_RUN: the earlier glider-harvest folder (needs data/Shinjuku, code/, attempts/verified/INDEX.tsv).
# HARVEST_RUN: this harvest folder (INDEX.tsv is written here).
G3=os.environ['GLIDER_RUN']; H=os.environ['HARVEST_RUN']
sys.path.insert(0, G3+'/data/Shinjuku'); sys.path.insert(0, G3+'/code')
os.chdir(G3+'/data/Shinjuku')
from shinjuku import lt
from shinjuku.search import read_components, decode_comp
from shinjuku.transcode import realise_comp
from shinjuku.gliderset import gset
from shinjuku.checks import rewind_check
import verify_synthesis as VS
TFS=["identity","rot90","rot180","rot270","flip_x","flip_y","swap_xy","swap_xy_flip"]
ap=argparse.ArgumentParser(); ap.add_argument('--targets',required=True); ap.add_argument('--deadline',type=float,required=True)
ap.add_argument('--predict-out'); ap.add_argument('--sleep',type=float,default=2.0); a=ap.parse_args()
IDX=H+'/INDEX.tsv'
COLS=['apgcode','our_cost','live_cost','live_kind','saving','status','rle_path','depends_on','timestamp','note']
done={}
if os.path.exists(IDX):
    for l in list(open(IDX))[1:]:
        s=l.rstrip('\n').split('\t'); done[s[0]]=dict(zip(COLS,s))
else: open(IDX,'w').write('\t'.join(COLS)+'\n')
def addrow(r):
    with open(IDX,'a') as f: f.write('\t'.join(str(r.get(c,'')) for c in COLS)+'\n')
    done[r['apgcode']]=r
# seeds: glider INDEX verified + composed/ + our own VERIFIED harvest rows
seeds={}
for l in list(open(G3+'/attempts/verified/INDEX.tsv'))[1:]:
    s=l.rstrip('\n').split('\t'); seeds[s[1]]=(int(s[3]),G3+'/attempts/verified/'+s[5],'glider-INDEX:'+s[1])
for k,r in done.items():
    if r['status']=='VERIFIED' and (k not in seeds or int(r['our_cost'])<seeds[k][0]):
        seeds[k]=(int(r['our_cost']),r['rle_path'],'harvest:'+k+'<-'+r['depends_on'])
print('seeds',len(seeds),flush=True)
db={}
for line in read_components():
    i,n,o=decode_comp(line); db.setdefault(i,[]).append((n,o,line))
res={"":[0,None,None]}; pq=[(0,"")]
for k,(v,_,_) in seeds.items(): res[k]=[v,'INJ',None]; pq.append((v,k))
heapq.heapify(pq)
while pq:
    d,c=heapq.heappop(pq)
    if d>res[c][0]: continue
    for n,o,line in db.get(c,()):
        nd=d+n
        if o not in res or nd<res[o][0] or (nd==res[o][0] and line<(res[o][2] or '~')):
            res[o]=[nd,c,line]; heapq.heappush(pq,(nd,o))
print('dijkstra done',len(res),flush=True)
if a.predict_out:
    with open(a.predict_out,'w') as f:
        for k,(d,p,_) in res.items():
            if k.startswith('xs'): f.write(f'{k}\t{d}\n')
def settle(P,t0,want,limit):
    t=t0
    while t<=t0+limit:
        X=P[t]
        if X[1]==X and X.population>0:
            try:
                if X.apgcode==want: return t
            except Exception: pass
        t+=64
    return None
def diam(P):
    r=P.getrect() or (0,0,1,1); return max(r[2],r[3])
def compose(tgt):
    lines=[]; cur=tgt
    while res[cur][1] not in ('INJ',None): lines.append(res[cur][2]); cur=res[cur][1]
    if res[cur][1]!='INJ': raise Exception('path does not use a seed')
    seed=cur; lines=lines[::-1]
    P=lt.pattern(open(seeds[seed][1]).read())
    T=settle(P,0,seed,8*diam(P)+8192); assert T is not None,'seed did not settle'
    for i,line in enumerate(lines):
        base,gs=realise_comp(line,separate=True); X=P[T]; ok=False
        outp=decode_comp(line)[2]
        G=None
        for tf in TFS:
            Bt=base(tf); rb=Bt.getrect(); ry=X.getrect()
            dx,dy=ry[0]-rb[0],ry[1]-rb[1]
            if Bt(dx,dy)==X:
                G=gs(tf)(dx,dy); ok=True; break
        assert ok,('stage',i,'no match',X.apgcode)
        T2=None
        # stage gliders must arrive after the previous stage settled; try increasing arrival delays so the
        # (far-out) stage gliders do not cross still-inbound/outbound gliders of earlier stages
        for off in (0,64,128,256,512,768,1024,1536,2048,3072,4096,6144,8192):
            r=T+off; P2=P+G[-r].s
            if P2.population!=P.population+G.s.population: continue  # overlap at gen 0
            T2=settle(P2,r,outp,8*diam(P2)+8192)
            if T2 is not None: P=P2; break
        assert T2 is not None,('stage',i,'did not settle to',outp)
        T=T2
    return P,seed,len(lines)
def rewind4(P):
    """explicit: all components are gliders, gliders rewound by 4*diameter gens re-evolve to P (no interaction) and
    every glider is moving toward the pattern centre (inbound)."""
    gs=gset.extract(P); D=diam(P); R=4*D
    if (P-gs.s).population: return False,'residual'
    Q=gs[-R].s
    if Q[R]!=P: return False,'interaction during 4*diam rewind'
    if len(list(Q.components()))!=len(list(P.components())): return False,'gliders not separated after rewind'
    # inbound: centre distance grows when rewinding further
    r=P.getrect(); cx,cy=r[0]+r[2]/2,r[1]+r[3]/2
    def dist(p):
        rr=p.getrect(); return abs(rr[0]+rr[2]/2-cx)+abs(rr[1]+rr[3]/2-cy)
    cp=list(P.components()); cq=list(gs[-R-64].s.components())
    tot0=sum(dist(c) for c in cp); tot1=sum(dist(c) for c in cq)
    if not tot1>tot0: return False,'not inbound'
    return True,f'R={R}'
def fetch(apg):
    url=f"https://catagolue.hatsya.com/object/{apg}/b3s23"
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'v3r1t4s-research (low rate)'})
            html=urllib.request.urlopen(req,timeout=30).read().decode('utf-8','replace')
            m=re.search(rf"#CSYNTH\s+{re.escape(apg)}\s+costs\s+(\d+)\s+gliders(\s*\(pseudo\))?",html)
            if m: return int(m.group(1)),('pseudo' if m.group(2) else 'true'),None
            return None,None,'no CSYNTH on page'
        except urllib.error.HTTPError as e:
            if e.code in (401,403,429) or e.code>=500: return None,None,f'HTTP {e.code}'
            err=f'HTTP {e.code}'
        except Exception as e: err=str(e)[:80]
        time.sleep(3*(i+1))
    return None,None,err
for tgt in [l.split()[0] for l in open(a.targets) if l.strip()]:
    if time.time()>a.deadline: print('deadline reached',flush=True); break
    if tgt in done and (done[tgt]['status']=='VERIFIED' or 'not cheaper' in done[tgt].get('note','')): continue
    if tgt not in res: print(tgt,'unreachable',flush=True); continue
    ts=time.strftime('%Y-%m-%dT%H:%M:%S%z'); t0=time.time()
    row={'apgcode':tgt,'our_cost':res[tgt][0],'timestamp':ts}
    try:
        P,seed,ns=compose(tgt)
        row['depends_on']=seeds[seed][2]
        out=H+'/rle/'+tgt+'.rle'; open(out,'w').write(P.rle_string()); row['rle_path']=out
        okr,why=rewind4(P)
        v=VS.verify_pattern(lt,gset,rewind_check,P,tgt) if okr else None
        if not okr: raise Exception('rewind4: '+why)
        if not v['structurally_valid']: raise Exception('verify: '+';'.join(v['errors'])[:150])
        row['our_cost']=v['n_gliders']
        time.sleep(a.sleep)
        live,kind,err=fetch(tgt)
        if live is None:
            row.update(status='PENDING TABLE CHECK',note=err)
        else:
            row.update(live_cost=live,live_kind=kind,saving=live-v['n_gliders'])
            row['status']='VERIFIED' if v['n_gliders']<live else 'FAILED'
            if v['n_gliders']>=live: row['note']='not cheaper than live'
        row['note']=(row.get('note','')+f' stages={ns} {why}').strip()
        json.dump({**v,'rewind4':why,'live':live,'live_kind':kind,'fetched':ts},open(H+'/verify/'+tgt+'.json','w'),default=str)
    except Exception as e:
        row.update(status='FAILED',note=str(e)[:160].replace('\t',' '))
    addrow(row); print(tgt,row['status'],row.get('our_cost'),row.get('live_cost'),row.get('note',''),f'{time.time()-t0:.1f}s',flush=True)
