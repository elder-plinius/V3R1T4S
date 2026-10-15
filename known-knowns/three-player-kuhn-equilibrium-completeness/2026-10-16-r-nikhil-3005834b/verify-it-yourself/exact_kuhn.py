"""Definition-first, standard-library exact checker for AAMAS 2013 Kuhn poker.

No solver imports. Card-specific pure plans enumerate all 2^4 choices, so
best responses allow coordinated deviations at initial and later decisions.
The 24 equally likely deals are enumerated without replacement.
"""
from fractions import Fraction as F
from itertools import permutations, product
import json

SITUATIONS = [('', 'KKB', 'KBF', 'KBC'),
              ('K', 'B', 'KKBF', 'KKBC'),
              ('KK', 'KB', 'BF', 'BC')]
ACTOR = {h:(p,k) for p,hs in enumerate(SITUATIONS) for k,h in enumerate(hs)}
DEALS = list(permutations(range(4),3))

def parse_profile(obj):
    if isinstance(obj,dict): obj=obj['profile']
    assert len(obj)==3 and all(len(x)==4 and all(len(y)==4 for y in x) for x in obj)
    a=[[[F(str(z)) for z in y] for y in x] for x in obj]
    assert all(0<=z<=1 for x in a for y in x for z in y)
    return a

def payoff(deal,history):
    chips=[1,1,1];active={0,1,2};h=''
    for action in history:
        p,_=ACTOR[h]
        if action in 'BC':chips[p]+=1
        if action=='F':active.remove(p)
        h+=action
    winner=max(active,key=lambda p:deal[p]);u=[-x for x in chips]
    u[winner]+=sum(chips)
    assert sum(u)==0
    return u

def walk(profile,deal,h='',deviator=None,plan=None,reach=None,mass=F(1)):
    if h not in ACTOR:return [F(x) for x in payoff(deal,h)]
    p,k=ACTOR[h];j=deal[p]
    if reach is not None:reach[p][j][k]+=mass/F(24)
    q=F(plan[k]) if p==deviator else profile[p][j][k]
    letters='KB' if 'B' not in h else 'FC'
    out=[F(0)]*3
    for a,prob in zip(letters,[1-q,q]):
        if prob:
            child=walk(profile,deal,h+a,deviator,plan,reach,mass*prob)
            for i in range(3):out[i]+=prob*child[i]
    return out

def evaluate(profile):
    profile=parse_profile(profile);u=[F(0)]*3
    reach=[[[F(0)]*4 for _ in range(4)] for _ in range(3)]
    for deal in DEALS:
        v=walk(profile,deal,reach=reach)
        for p in range(3):u[p]+=v[p]/24
    br=[];policies=[]
    for p in range(3):
        total=F(0);chosen=[]
        for j in range(4):
            vals=[]
            for plan in product([0,1],repeat=4):
                val=sum((walk(profile,d,deviator=p,plan=plan)[p] for d in DEALS if d[p]==j),F(0))/24
                vals.append((val,plan))
            v,plan=max(vals);total+=v;chosen.append(plan)
        br.append(total);policies.append(chosen)
    assert all(b>=v for b,v in zip(br,u)) and sum(u)==0
    return {'payoffs':u,'best_responses':br,'gaps':[b-v for b,v in zip(br,u)],
            'is_nash':br==u,'reach':reach,'best_response_plans':policies}

def witnesses(profile,result):
    p=parse_profile(profile);u=result['payoffs'];beta=(-48*u[0]-1)/2
    return {'W1':u[1]!=-F(1,48),'W2':not(0<=beta<=F(1,4) and u[1]==-F(1,48) and u[2]==(1+beta)/24),
            'W3':any(p[0][j][0]>0 for j in range(4)),'beta_from_u1':beta}

def dump(obj,path=None):
    s=json.dumps(obj,default=str,indent=2)
    if path:open(path,'w').write(s+'\n')
    else:print(s)

if __name__=='__main__':
    import sys
    p=json.load(open(sys.argv[1]));r=evaluate(p);r['witnesses']=witnesses(p,r);dump(r)
