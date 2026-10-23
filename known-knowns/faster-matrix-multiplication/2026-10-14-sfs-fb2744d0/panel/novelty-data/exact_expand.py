"""Independent exact coefficient expansion; does not import claim/verify.py."""
import hashlib
import json
import pathlib
import sys

def factor(stage, base, outputs, side):
    rows = [[int(i==j) for i in range(base)] for j in range(base)]
    cost = 0
    def combine(expression):
        nonlocal cost
        used = set()
        vector = [0] * base
        cost += max(0,len(expression)-1)
        for term in expression:
            index, sign = term['index'], term['value']
            assert type(index) is int and 0 <= index < len(rows)
            assert index not in used and type(sign) is int and sign in (-1,1)
            used.add(index)
            for j, coefficient in enumerate(rows[index]):
                vector[j] += sign * coefficient
        return vector
    for expression in stage:
        rows.append(combine(expression))
    return [combine(expression) for expression in outputs], cost

def verify(path):
    data=path.read_bytes();s=json.loads(data)
    a,b,c=s['n'];rank=s['m']
    assert s.get('z2') is not True
    assert len(s['u'])==len(s['v'])==rank and len(s['w'])==a*c
    u,cu=factor(s.get('u_fresh',[]),a*b,s['u'],'u')
    v,cv=factor(s.get('v_fresh',[]),b*c,s['v'],'v')
    w,cw=factor(s.get('w_fresh',[]),rank,s['w'],'w')
    for output in range(a*c):
        i,j=output%a,output//a
        for x in range(a*b):
            for y in range(b*c):
                actual=sum(w[output][k]*u[k][x]*v[k][y] for k in range(rank))
                expected=int(x//b==i and y%c==j and x%b==y//c)
                assert actual==expected,(output,x,y,actual,expected)
    result={'file':path.name,'sha256':hashlib.sha256(data).hexdigest(),'format':[a,b,c],
            'rank':rank,'counts':{'u':cu,'v':cv,'w':cw},'additions':cu+cv+cw,
            'integer_coefficients_checked':a*c*a*b*b*c,
            'expanded_tensor_ternary':all(value in (-1,0,1) for rows in [u,v,w] for row in rows for value in row),
            'valid':True}
    return result

if __name__=='__main__':
    for name in sys.argv[1:]:
        print(json.dumps(verify(pathlib.Path(name))))
