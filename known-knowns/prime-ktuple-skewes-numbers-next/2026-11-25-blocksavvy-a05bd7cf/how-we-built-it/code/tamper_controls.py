"""400 tampered claims; verify_claim.verify must reject every one, and accept the real claim."""
import sys, os, copy, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_claim as V
rd=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','result')
res,counts,a=V.load(rd); rnd=random.Random(20261125)
real=V.verify(res,counts,a,quiet=True); print('real_claim_pass:',real)
prs=V.block_pairs(res['crossing_block'], res['skewes_number_inclusive']+40000)
idx=prs.index(res['skewes_number_inclusive']); N0=res['pairs_below_crossing_block_start_349012230144']
kinds={'other_pair_start':0,'pi6_shift':0,'table_entry':0,'prefix_shift':0}; rejected=0; total=0
for t in range(400):
    r=copy.deepcopy(res); c=list(counts); k=list(kinds)[t%4]
    if k=='other_pair_start':
        d=rnd.choice([x for x in range(-150,151) if x]); i=idx+d; r['skewes_number_inclusive']=prs[i]; r['pi6_at_p_inclusive']=N0+i+1
    elif k=='pi6_shift':
        r['pi6_at_p_inclusive']+=rnd.choice([x for x in range(-60,61) if x])
    elif k=='table_entry':
        j=rnd.randrange(0,27737); c[j]+=rnd.choice([-3,-2,-1,1,2,3])
    else:
        r['pairs_below_crossing_block_start_349012230144']+=rnd.choice([x for x in range(-100,101) if x])
    ok=V.verify(r,c,a,quiet=True); total+=1; kinds[k]+=1
    if not ok: rejected+=1
print('controls:',total,'by kind:',kinds); print('controls_rejected:',rejected); print('controls_accepted:',total-rejected)
print('RESULT:', 'PASS' if real and rejected==total else 'FAIL')
