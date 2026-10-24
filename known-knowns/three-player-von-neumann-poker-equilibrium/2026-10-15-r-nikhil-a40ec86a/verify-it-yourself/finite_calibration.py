"""Definition-first exact finite-deck evaluator. Distinct cards, net pot payoffs."""
from fractions import Fraction as F
from itertools import permutations, product
import json

def terminal(hands, actions, bet):
    n=len(hands)
    if not actions[0]:
        contributions=[F(1)]*n; active=list(range(n))
    else:
        active=[0]+[i for i in range(1,n) if actions[i]]
        contributions=[F(1)+bet if i in active else F(1) for i in range(n)]
    winner=max(active,key=lambda i:hands[i]); pot=sum(contributions)
    result=[-c for c in contributions]; result[winner]+=pot
    assert sum(result)==0
    return result

def evaluate(profile,bet):
    n=len(profile[0]); players=len(profile)
    assert all(len(row)==n and all(0<=p<=1 for p in row) for row in profile)
    denominator=1
    for j in range(players): denominator*=n-j
    av=[[[F(0),F(0)] for _ in range(n)] for __ in profile]
    for hands in permutations(range(n),players):
        for player in range(players):
            others=[j for j in range(players) if j!=player]
            for aa in product([0,1],repeat=players-1):
                prob=F(1)
                actions=[0]*players
                for j,a in zip(others,aa):
                    p=profile[j][hands[j]]; prob*=p if a else 1-p; actions[j]=a
                if not prob: continue
                for own in [0,1]:
                    actions[player]=own
                    av[player][hands[player]][own]+=prob*terminal(hands,actions,bet)[player]/denominator
    vals=[]; brs=[]
    for player in range(players):
        vals.append(sum((1-p)*v[0]+p*v[1] for p,v in zip(profile[player],av[player])))
        brs.append(sum(max(v) for v in av[player]))
    assert sum(vals)==0
    return {'values':vals,'best_responses':brs,'regrets':[b-v for b,v in zip(brs,vals)],'action_values':av}

def calibration():
    p=[[F(2,3),0,0,1],[0,0,F(1,4),1],[0,0,F(1,4),1]]
    a=evaluate(p,F(1)); assert a['values']==[F(1,24),F(-1,48),F(-1,48)]; assert a['regrets']==[0]*3
    bad=evaluate([[F(0)]*4 for _ in range(3)],F(1)); assert bad['regrets'][0]>0
    p10=[[F(16,19)]+[0]*8+[1],[0]*6+[F(3,25)]+[1]*3,[0]*6+[F(3,25)]+[1]*3]
    b=evaluate(p10,F(2)); assert b['values']==[F(106,1125),F(-53,1125),F(-53,1125)]; assert b['regrets']==[0]*3
    # The n=9 two-player pure profile from the source reproduces 1/9.
    p9=[[1]+[0]*6+[1]*2,[0]*5+[1]*4]
    c=evaluate(p9,F(2)); assert c['values']==[F(1,9),F(-1,9)]; assert c['regrets']==[0]*2
    print(json.dumps({'n4_b1':a,'known_negative':bad,'n10_b2':b,'n9_two_player_b2':c},default=str,indent=2))
    print('PASS: exact finite calibrations and deliberately exploitable profile')
if __name__=='__main__': calibration()
