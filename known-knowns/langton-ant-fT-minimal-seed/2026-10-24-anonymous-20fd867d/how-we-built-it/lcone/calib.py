# blank-grid calibration: turn sequence, periodicity start
N=30000
g=set();x=y=0;h=0;dx=[0,1,0,-1];dy=[-1,0,1,0];R=[]
for u in range(N):
    b=(x,y) in g; R.append(1 if b else 0)
    h=(h+(3 if b else 1))%4
    if b: g.remove((x,y))
    else: g.add((x,y))
    x+=dx[h];y+=dy[h]
s=N-105
while s>0 and R[s-1]==R[s-1+104]: s-=1
print("periodic from update index",s)
