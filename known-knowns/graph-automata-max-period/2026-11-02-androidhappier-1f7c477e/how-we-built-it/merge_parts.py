"""Union the period sets of the order-10 parts into out/B_order10.txt (same format as the other orders)."""
import glob,re
tot=0; P={}; 
for f in sorted(glob.glob('out/B_order10_part*.txt')):
    t=open(f).read(); assert t.rstrip().endswith('exit 0'), f
    tot+=int(re.search(r'connected_graphs=(\d+)',t).group(1))
    for m in re.finditer(r'witness (\d+) (\S+) (\d+)',t):
        P.setdefault(int(m.group(1)),(m.group(2),m.group(3)))
with open('out/B_order10.txt','w') as o:
    o.write(f"order=10 connected_graphs={tot} max_cycle={max(P)}\n")
    o.write("periods: "+" ".join(map(str,sorted(P)))+"\n")
    for L in sorted(P): o.write(f"witness {L} {P[L][0]} {P[L][1]}\n")
print('connected order-10 graphs',tot,'A001349(10)=11716571','match' if tot==11716571 else 'MISMATCH')
