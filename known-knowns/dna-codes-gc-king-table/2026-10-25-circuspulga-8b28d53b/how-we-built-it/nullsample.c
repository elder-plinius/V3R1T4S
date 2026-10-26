/* nullsample.c: random-order greedy null for large n (n >= 17), where nullgreedy's full-space table does not fit.
   Draws uniformly random constant-GC words (w = n/2) and accepts one iff its Hamming distance to every accepted word
   is >= D; stops after STOP consecutive rejections (a near-maximal random greedy code). Prints "seed S size K".
   Usage: nullsample N D SEED_FIRST SEED_LAST STOP */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static uint64_t rs; static inline uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int argc,char**argv){
  int N=atoi(argv[1]),D=atoi(argv[2]),s0=atoi(argv[3]),s1=atoi(argv[4]); long STOP=atol(argv[5]); int W=N/2;
  static uint32_t G[100000],B[100000];
  for(int s=s0;s<=s1;s++){ rs=(uint64_t)s*2654435761ULL+88172645463325252ULL; for(int k=0;k<10;k++) rnd();
    int K=0; long rej=0;
    while(rej<STOP && K<100000){ uint32_t g=0; int c=0; /* random W-subset of positions */
      while(c<W){ int p=(int)(rnd()%N); if(!((g>>p)&1)){ g|=1u<<p; c++; } }
      uint32_t b=(uint32_t)(rnd()&((1u<<N)-1)); int ok=1;
      for(int i=0;i<K;i++) if(__builtin_popcount((G[i]^g)|(B[i]^b))<D){ ok=0; break; }
      if(ok){ G[K]=g; B[K]=b; K++; rej=0; } else rej++; }
    printf("seed %d size %d\n",s,K); fflush(stdout); }
  return 0; }
