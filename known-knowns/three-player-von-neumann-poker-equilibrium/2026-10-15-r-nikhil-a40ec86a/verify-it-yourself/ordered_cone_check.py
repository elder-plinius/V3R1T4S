"""Exact sign certificates from independently integrated raw payoff pieces.

Subtract the appropriate defining equation, orient toward the prescribed
action, and substitute nonnegative adjacent gaps. Every coefficient must be
nonnegative. This certifies whole intervals without an SMT timeout or a grid.
Uses the portable rational polynomial ring; no SymPy or numerical roots.
"""
from pathlib import Path
import sys,json,hashlib
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root.parent/'certifier'/'code'))
from universal_check import Poly,parse,NAMES,ZERO,E

def substitute(p,mapping):
    out=Poly.const(0)
    for powers,c in p.d.items():
        term=Poly.const(c)
        for name,power in zip(NAMES,powers):
            term=term*(mapping.get(name,parse(name))**power)
        out=out+term
    return out

def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else root/'output'/'rectangles.json.txt'
    data=json.loads(source.read_text().split('\nPASS:')[0])
    # Independent nonnegative variables: s=A or x, y=next gap,
    # c=next gap and c0=last gap. Strict original order is a subset.
    maps=[
      {'x':'s','A':'s+y','C':'s+y+c','B':'s+y+c+c0'},
      {'A':'s','x':'s+y','C':'s+y+c','B':'s+y+c+c0'},
      {'A':'s','C':'s+y','x':'s+y+c','B':'s+y+c+c0'},
      {'A':'s','C':'s+y','B':'s+y+c','x':'s+y+c+c0'}]
    results=[]
    for player in range(3):
        for gap in range(4):
            raw=parse(data[str(player)][gap]['difference'])
            equation=parse(E[0] if gap<2 else E[1]) if player==0 else parse(E[2])
            # raw + E1 = low I difference; raw - b*E2 = high;
            # raw - E3 = every caller difference.
            residual=raw+equation if player==0 and gap<2 else raw-(parse('b')*equation if player==0 else equation)
            prescribed=([1,0,0,1] if player==0 else [0,0,1,1])[gap]
            if not prescribed:residual=-residual
            transformed=substitute(residual,{n:parse(v) for n,v in maps[gap].items()})
            assert all(c>=0 for c in transformed.d.values()),(player,gap)
            results.append({'player':player+1,'region':gap,'monomials':len(transformed.d),'minimum_coefficient':str(min(transformed.d.values())) if transformed.d else '0 (zero polynomial)'})
    # Bridge the complete conditional payoffs and integrated values too.
    A,B,C,b,x=[parse(n) for n in ['A','B','C','b','x']]
    count=0
    for player in range(3):
        for gap in range(4):
            if player==0:
                base=parse('3*x**2-1')
                active=parse('(b+3)*C**2-(b+1)' if gap<2 else '3*(b+1)*x**2-2*b*C*x-(b+1)')
            else:
                h=['0','x-A','x-A','B-A'][gap]
                base=parse('-1+3*x*('+h+')')
                w=['x','A','A','A+x-B'][gap]
                win=['0','0','x-C','x-C'][gap]
                active=base+parse('('+w+')*((2*b+3)*C+3*(b+1)*('+win+'))-b*(A+1-B)')
            assert parse(data[str(player)][gap]['action0'])==base
            assert parse(data[str(player)][gap]['action1'])==active
            count+=2
    value=parse('-A**3+(b+3)*A*C**2-b*A-b*B**3+b*B**2*C+b*B-b*C')
    assert parse(data['profile_values'][0])==value
    assert parse(data['profile_values'][1])*Poly.const(2)==-value
    assert parse(data['profile_values'][2])*Poly.const(2)==-value
    output={'raw_input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'regions_certified':len(results),'full_action_payoffs_matched':count,'integrated_values_matched':3,'sign_certificates':results,'scope':'conditional on b>0, 0<A<C<B<1 and Eq A-C; existence is in the separate analytic proof'}
    print(json.dumps(output,indent=2))
    print('PASS: exact nonnegative-gap polynomial certificates for all 12 raw payoff regions')

if __name__=='__main__':main()
