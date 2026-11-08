/* nullgreedy.c: random maximal constant-GC codes (random-order greedy) as null controls.
   Repeatedly picks a uniformly random word among all words at distance >= D from every chosen word (reservoir
   sampling over the full space of C(N,W)*2^N words) until none is left. Prints the size of each maximal code.
   Usage: nullgreedy N D SEED_FIRST SEED_LAST   -> one line "seed S size K" per control. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int N,D,W,MASK,NG; static int gcm[20000]; static uint64_t rs;
static inline uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int argc,char**argv){
  N=atoi(argv[1]); D=atoi(argv[2]); int s0=atoi(argv[3]), s1=atoi(argv[4]);
  W=N/2; MASK=(1<<N)-1; NG=0; for(int g=0;g<(1<<N);g++) if(__builtin_popcount(g)==W) gcm[NG++]=g;
  long NW=(long)NG<<N; uint8_t *bad=malloc(NW); if(!bad) return 2;
  for(int s=s0;s<=s1;s++){
    rs=(uint64_t)s*2654435761ULL+88172645463325252ULL; for(int k=0;k<10;k++) rnd();
    memset(bad,0,NW); int K=0;
    for(;;){ long pick=-1; uint64_t cnt=0;
      for(long w=0;w<NW;w++) if(!bad[w]){ cnt++; if(rnd()%cnt==0) pick=w; }
      if(pick<0) break; K++;
      int gx=gcm[pick>>N], bx=(int)(pick&MASK);
      for(int gi=0;gi<NG;gi++){ int gd=gcm[gi]^gx; uint8_t*row=bad+((long)gi<<N);
        for(int b=0;b<=MASK;b++) if(__builtin_popcount(gd|(b^bx))<D) row[b]=1; } }
    printf("seed %d size %d\n",s,K); fflush(stdout);
  }
  return 0;
}
