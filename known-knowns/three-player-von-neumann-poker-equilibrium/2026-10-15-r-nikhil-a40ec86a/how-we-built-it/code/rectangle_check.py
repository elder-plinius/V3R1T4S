"""Independent continuous payoff integration from terminal pot accounting.
No use of the certifier's payoff formulas. Own-hand interval is fixed, and
opponent rectangles are cut at the own hand and all profile thresholds.
"""
import sympy as s
from itertools import product
from pathlib import Path
import json
x,A,C,B,b=s.symbols('x A C B b')
base=[s.S(0),A,C,B,s.S(1)]
numbers={A:s.Rational(1,10),C:s.Rational(3,5),B:s.Rational(4,5)}

def payoff(player,act,hands,actions):
    actions=list(actions); actions[player]=act
    if not actions[0]: active=[0,1,2]; contrib=[1,1,1]
    else:
        active=[0]+[j for j in [1,2] if actions[j]]
        contrib=[1+b if j in active else s.S(1) for j in range(3)]
    winner=max(active,key=lambda j:hands[j])
    return (sum(contrib) if winner==player else 0)-contrib[player]

def integrate(player,gap,act):
    sample_x=(base[gap]+base[gap+1]).subs(numbers)/2
    cuts=base[:gap+1]+[x]+base[gap+1:]
    boxes=[(l,h,(l+h).subs({**numbers,x:sample_x})/2) for l,h in zip(cuts,cuts[1:])]
    other=[j for j in range(3) if j!=player]
    out=0
    for q,r in product(boxes,repeat=2):
        hands=[sample_x]*3; weight=1
        for j,(lo,hi,mid) in zip(other,[q,r]): hands[j]=mid; weight*=hi-lo
        actions=[hands[0]<numbers[A] or hands[0]>numbers[B],hands[1]>numbers[C],hands[2]>numbers[C]]
        out+=weight*payoff(player,act,hands,actions)
    return s.expand(out)

def main():
    results={}; checks=0
    for player in range(3):
        results[player]=[]
        for gap in range(4):
            u0=integrate(player,gap,0);u1=integrate(player,gap,1);d=s.expand(u1-u0)
            results[player].append(dict(interval=[str(base[gap]),str(base[gap+1])],action0=str(u0),action1=str(u1),difference=str(d)))
            if player==0:
                expected=(b+3)*C*C-b-3*x*x if gap<2 else b*(3*x*x-2*C*x-1)
            else:
                winmass=[x,A,A,A+x-B][gap]
                winother=0 if gap<2 else x-C
                expected=winmass*((2*b+3)*C+(3*b+3)*winother)-b*(A+1-B)
            assert s.expand(d-expected)==0
            checks+=1
    # Independently integrate player I's prescribed payoff, with b=2.
    values=[]
    for player in range(3):
        value=0
        for gap in range(4):
            action=([1,0,0,1] if player==0 else [0,0,1,1])[gap]
            value+=s.integrate(integrate(player,gap,action),(x,base[gap],base[gap+1]))
        values.append(s.factor(value))
    assert s.expand(sum(values))==0
    results['profile_values']=[str(v) for v in values]
    results['symbolic_action_differences_verified']=checks
    print(json.dumps(results,indent=2))
    print('PASS: all 12 action-difference polynomials match, value sum is zero')
if __name__=='__main__':main()
