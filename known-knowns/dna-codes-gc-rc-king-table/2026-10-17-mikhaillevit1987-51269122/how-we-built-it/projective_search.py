from engine import *
# Projective evaluation codes independently generated from GF(4) column vectors.
# Search only new cells; exclude (20,16), already found by the parent lens.
base=[]
for v in itertools.product(range(4),repeat=3):
 if v==(0,0,0):continue
 first=next(x for x in v if x)
 if first==1:base.append(v)
base=np.array(base,dtype=np.uint8)
messages=np.array(list(itertools.product(range(4),repeat=3)),dtype=np.uint8)
def code(cols):
 return np.bitwise_xor.reduce(mul[messages[:,:,None],cols.T[None,:,:]],axis=1)
def normalize(v):
 x=next(x for x in v if x);inv=[0,1,3,2][x];return tuple(mul[inv,v])
# Transvection (x,y,z)->(x+y,y,z), fixed projective line y=0.
L=base.copy();L[:,0]^=L[:,1]
lookup={tuple(v):i for i,v in enumerate(base)}
perm=[lookup[normalize(v)] for v in L]
fixed=[i for i,j in enumerate(perm) if i==j]
print('GEOMETRY',{'points':len(base),'fixed':fixed},flush=True)
end=time.time()+1080;loops=0
while time.time()<end:
 removed=random.choice(fixed)
 cols=base.copy();pairs=[];used={removed}
 for i,j in enumerate(perm):
  if i in used or i==j:continue
  pairs.append((i,j));used|={i,j};cols[j]=L[i]
 fs=[i for i in fixed if i!=removed];random.shuffle(fs);pairs.extend(zip(fs[::2],fs[1::2]))
 # Test fully algebraic matching first, then a few pair exchanges.
 for mutation in range(6):
  if mutation:
   a,b=random.sample(range(len(pairs)),2);x,y=pairs[a];z,w=pairs[b];pairs[a]=(x,w);pairs[b]=(z,y)
  order=[a for a,b in pairs]+[b for a,b in pairs][::-1]
  raw=code(cols[order]);n=20
  for offmode in range(16):
   # XOR2 controls GC coset; XOR1 on paired positions controls RC offset.
   off=np.array([random.randrange(4) if offmode>7 else random.randrange(2) for _ in range(n)],dtype=np.uint8) if offmode else np.zeros(n,dtype=np.uint8)
   W=raw^off;W=W[np.count_nonzero(W>=2,axis=1)==10]
   evaluate(W,15,'projective_transvection_coset',.05)
   evaluate(W,14,'projective_transvection_coset',.02)
  # Puncture one arbitrary coordinate, independent balanced slice from all code words.
  if mutation<2:
   for cut in random.sample(range(20),3):
    X=np.delete(raw,cut,axis=1)
    for j in range(3):
     off=np.random.default_rng(trials).integers(0,4,19,dtype=np.uint8);W=X^off;W=W[np.count_nonzero(W>=2,axis=1)==9]
     evaluate(W,15,'punctured_projective19',.05);evaluate(W,14,'punctured_projective19',.02)
 loops+=1
 if loops%10==0:
  (P/'checkpoint_projective.json').write_text(json.dumps({'pid':os.getpid(),'loops':loops,'trials':trials,'seconds':time.time()-T,'best':{str(k):v for k,v in best.items()},'counts':counts}))
print('DONE',json.dumps({'loops':loops,'trials':trials,'best':{str(k):v for k,v in best.items()},'counts':counts}),flush=True)
