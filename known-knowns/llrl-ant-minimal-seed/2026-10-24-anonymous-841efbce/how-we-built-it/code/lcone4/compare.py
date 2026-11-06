import re,sys
def cells(line): return tuple(sorted(tuple(map(int,m)) for m in re.findall(r'\((-?\d+),(-?\d+),(\d+)\)',line.split('cells:')[1])))
a,b,best=sys.argv[1],sys.argv[2],int(sys.argv[3])
A={cells(l) for l in open(a) if l.startswith('SOL') and int(re.search(r'onset=(\d+)',l).group(1))==best}
B={cells(l) for l in open(b) if l.startswith('MIN')}
print(len(A),len(B),'IDENTICAL' if A==B else 'DIFFER')
for s in sorted(A): print(';'.join(f'{x},{y},{c}' for x,y,c in s))
