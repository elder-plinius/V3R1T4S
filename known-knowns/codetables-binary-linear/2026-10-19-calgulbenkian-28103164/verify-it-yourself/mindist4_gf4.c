/* Own checker: exact min distance of a GF(4) linear code by full enumeration of 4^k messages.
   Input text: n k then k rows of n ints in 0..3 (v = a + 2b means a + b*w, w^2=w+1).
   Also counts min-weight words and checks no nonzero message gives weight 0 (rank k). */
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "stdint.h"
#define W 4
typedef struct { uint64_t lo[W], hi[W]; } vec;
static int n,k,nw;
static vec mult[16][4]; /* row i, scalar c */
static int best, cnt, zero_nonzero; static long long total;
static void mulw(vec *v){ /* multiply by w: (a+bw)w = b + (a+b)w  => a'=b, b'=a^b */
  for(int i=0;i<W;i++){ uint64_t a=(*v).lo[i], b=(*v).hi[i]; (*v).lo[i]=b; (*v).hi[i]=a^b; } }
static int wt(const vec*v){ int s=0; for(int i=0;i<nw;i++) s+=__builtin_popcountll((*v).lo[i]|(*v).hi[i]); return s; }
static void dfs(int lvl, vec acc, int nonzero){
  if(lvl==k){ if(!nonzero) return; int w=wt(&acc); total++; if(w==0) zero_nonzero++; else if(w<best){best=w;cnt=1;} else if(w==best) cnt++; return; }
  for(int c=0;c<4;c++){ vec a=acc; if(c) for(int i=0;i<nw;i++){ a.lo[i]^=mult[lvl][c].lo[i]; a.hi[i]^=mult[lvl][c].hi[i]; }
    dfs(lvl+1,a,nonzero||c); }
}
int main(int argc,char**argv){ FILE*f=fopen(argv[1],"r"); if(!f||fscanf(f,"%d %d",&n,&k)!=2) return 2; nw=(n+63)/64; if(nw>W) return 3;
  for(int r=0;r<k;r++){ memset(&mult[r][1],0,sizeof(vec)); for(int j=0;j<n;j++){ int v; if(fscanf(f,"%d",&v)!=1) return 4; if(v&1) mult[r][1].lo[j/64]|=1ULL<<(j%64); if(v&2) mult[r][1].hi[j/64]|=1ULL<<(j%64);} 
    mult[r][2]=mult[r][1]; mulw(&mult[r][2]); mult[r][3]=mult[r][2]; mulw(&mult[r][3]);
    /* check w^3 = 1: mult by w again returns the original */
    vec t=mult[r][3]; mulw(&t); if(memcmp(&t,&mult[r][1],sizeof(vec))) { puts("field arithmetic self-check failed"); return 5; } }
  best=1<<30; cnt=0; zero_nonzero=0; total=0; vec z; memset(&z,0,sizeof z); dfs(0,z,0);
  printf("n=%d k=%d messages=%lld rank_deficient=%s min_distance=%d A_d=%d\n",n,k,total,zero_nonzero?"YES":"no",best,cnt); return 0; }
