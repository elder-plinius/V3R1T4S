import numpy as np

def cover(B,n,picks,candidates,seed):
 rng=np.random.default_rng(seed);cand=np.array(candidates).copy();rng.shuffle(cand)
 cov=np.zeros(B.shape[1],np.uint64);chosen=[]
 for k in range(picks):
  if not len(cand):break
  gains=np.unpackbits((B[cand]&~cov).view(np.uint8),axis=-1).sum(1)
  i=0 if k==0 and seed else int(np.argmax(gains))
  if gains[i]==0:break
  chosen.append(int(cand[i]));cov|=B[cand[i]];cand=np.delete(cand,i)
  if int(np.unpackbits(cov.view(np.uint8)).sum())==n:break
 return n-int(np.unpackbits(cov.view(np.uint8)).sum()),chosen
