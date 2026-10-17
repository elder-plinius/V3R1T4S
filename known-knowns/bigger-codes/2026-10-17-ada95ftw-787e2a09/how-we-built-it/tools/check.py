"""Independent checker: python3 check.py n d w codefile  (one word per line as 0/1 string)"""
import sys
def check(n,d,w,words):
    S=set()
    for s in words:
        assert len(s)==n and set(s)<= set('01'), 'bad length/char'
        x=int(s,2); assert bin(x).count('1')==w, 'bad weight'
        assert x not in S, 'duplicate'; S.add(x)
    L=list(S)
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            assert bin(L[i]^L[j]).count('1')>=d, f'distance<{d}'
    return len(L)
if __name__=='__main__':
    n,d,w=map(int,sys.argv[1:4]); ws=[l.strip() for l in open(sys.argv[4]) if l.strip()]
    print('VALID M =',check(n,d,w,ws))
