/* Pair-merge local move for a (v,k,t) covering (0-based, v<=128).
   For block B let U(B) = union of points of t-subsets of B with stored count 1 (only B covers them).
   If |U(B1) u U(B2)| <= k (computed exactly w.r.t. sets covered only by B1 and/or B2), replace B1,B2 by one block
   W = U(B1)uU(B2) padded with points of B1 (then B2, then others) -> b decreases by 1. Counts uint8 saturating (stored<=true).
   Usage: merge V K T IN OUT MAXSEC CANDMAX
   Prints histogram of |U| and merges done. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef unsigned long long u64; typedef struct { u64 w[2]; } bm;
static u64 C[130][16]; static int v,k,t; static uint8_t *cnt;
#define FORSUB(blk, BODY) { int idx[16]; for(int i=0;i<t;i++) idx[i]=i; for(;;){ u64 r=0; for(int i=0;i<t;i++) r+=C[blk[idx[i]]][i+1]; BODY; int i=t-1; while(i>=0 && idx[i]==k-t+i) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<t;j++) idx[j]=idx[j-1]+1; } }
static inline int pc(bm a){ return __builtin_popcountll(a.w[0])+__builtin_popcountll(a.w[1]); }
static inline void setb(bm*a,int x){ a->w[x>>6]|=1ULL<<(x&63); }
static inline int hasb(const bm*a,int x){ return (a->w[x>>6]>>(x&63))&1; }
static size_t nb; static uint8_t *B;
static bm uniq(size_t i){ bm u={{0,0}}; uint8_t*b=B+i*k; FORSUB(b, if(cnt[r]<=1){ for(int q=0;q<t;q++) setb(&u,b[idx[q]]); }); return u; }
/* sets covered by i (and possibly j) with no other cover: count - [in i] - [in j] == 0 */
static bm need(size_t i, size_t j, bm bj){ bm u={{0,0}}; uint8_t*b=B+i*k; FORSUB(b, { int inj=1; for(int q=0;q<t;q++) if(!hasb(&bj,b[idx[q]])){inj=0;break;} int c=cnt[r]-1-inj; if(c<=0){ for(int q=0;q<t;q++) setb(&u,b[idx[q]]);} }); return u; }
static int cmpu8(const void*a,const void*b){ return *(const uint8_t*)a-*(const uint8_t*)b; }
int main(int argc,char**argv){
  if(argc!=8){fprintf(stderr,"usage\n");return 2;}
  v=atoi(argv[1]);k=atoi(argv[2]);t=atoi(argv[3]); double maxsec=atof(argv[6]); long candmax=atol(argv[7]);
  for(int n=0;n<130;n++){C[n][0]=1;for(int r=1;r<16;r++)C[n][r]=(n==0)?0:C[n-1][r-1]+C[n-1][r];}
  FILE*f=fopen(argv[4],"r"); size_t cap=1<<18; nb=0; B=malloc(cap*k); char line[4096];
  while(fgets(line,sizeof line,f)){ char*p=line,*e; int c=0; if(nb==cap){cap*=2;B=realloc(B,cap*k);}
    for(;;){ long x=strtol(p,&e,10); if(e==p)break; B[nb*k+c++]=(uint8_t)x; p=e; } if(c==0) continue;
    qsort(B+nb*k,k,1,cmpu8); nb++; }
  fclose(f);
  u64 N=C[v][t]; cnt=calloc(N,1); if(!cnt){fprintf(stderr,"oom\n");return 1;}
  clock_t t0=clock();
  for(size_t i=0;i<nb;i++){ uint8_t*b=B+i*k; FORSUB(b, if(cnt[r]<255) cnt[r]++); }
  bm *U=malloc(nb*sizeof(bm)); int *us=malloc(nb*sizeof(int)); long hist[130]={0};
  for(size_t i=0;i<nb;i++){ U[i]=uniq(i); us[i]=pc(U[i]); hist[us[i]]++; }
  printf("nb=%zu |U| histogram:",nb); for(int x=0;x<=v;x++) if(hist[x]) printf(" %d:%ld",x,hist[x]); printf("\n");
  /* candidates: |U| <= k, sorted ascending */
  size_t *cand=malloc(nb*sizeof(size_t)); long nc=0;
  for(int s=0;s<=k;s++) for(size_t i=0;i<nb;i++) if(us[i]==s && nc<candmax) cand[nc++]=i;
  uint8_t *dead=calloc(nb,1); long merges=0; uint8_t *extra=malloc((size_t)nb*k); size_t nex=0;
  printf("candidates=%ld\n",nc); fflush(stdout);
  for(long a=0;a<nc;a++){ size_t i=cand[a]; if(dead[i]) continue;
    if((double)(clock()-t0)/CLOCKS_PER_SEC>maxsec){ printf("time cap at a=%ld\n",a); break; }
    for(long c2=a+1;c2<nc;c2++){ size_t j=cand[c2]; if(dead[j]) continue;
      bm q={{U[i].w[0]|U[j].w[0],U[i].w[1]|U[j].w[1]}}; if(pc(q)>k) continue;   /* fast filter (necessary cond.) */
      bm bi={{0,0}},bj={{0,0}}; for(int x=0;x<k;x++){ setb(&bi,B[i*k+x]); setb(&bj,B[j*k+x]); }
      bm ni=need(i,j,bj), nj=need(j,i,bi); bm w={{ni.w[0]|nj.w[0],ni.w[1]|nj.w[1]}}; if(pc(w)>k) continue;
      /* pad W with points of B_i then B_j then 0.. */
      for(int x=0;x<k && pc(w)<k;x++) setb(&w,B[i*k+x]);
      for(int x=0;x<k && pc(w)<k;x++) setb(&w,B[j*k+x]);
      for(int x=0;x<v && pc(w)<k;x++) setb(&w,x);
      uint8_t nbk[64]; int m=0; for(int x=0;x<v;x++) if(hasb(&w,x)) nbk[m++]=(uint8_t)x;
      /* apply: decrement i,j; increment new */
      { uint8_t*b=B+i*k; FORSUB(b, cnt[r]--); } { uint8_t*b=B+j*k; FORSUB(b, cnt[r]--); }
      { uint8_t*b=nbk; FORSUB(b, if(cnt[r]<255) cnt[r]++); }
      dead[i]=dead[j]=1; memcpy(extra+nex*k,nbk,k); nex++; merges++;
      /* affected U values are stale for others; recompute lazily: blocks' U only shrink-or-change; we re-verify exactly via need() anyway */
      break; }
  }
  FILE*o=fopen(argv[5],"w"); size_t kept=0;
  for(size_t i=0;i<nb;i++) if(!dead[i]){ for(int x=0;x<k;x++) fprintf(o,x?" %d":"%d",B[i*k+x]); fputc('\n',o); kept++; }
  for(size_t e2=0;e2<nex;e2++){ for(int x=0;x<k;x++) fprintf(o,x?" %d":"%d",extra[e2*k+x]); fputc('\n',o); kept++; }
  fclose(o);
  printf("merge in=%zu merges=%ld out=%zu secs=%.1f\n",nb,merges,kept,(double)(clock()-t0)/CLOCKS_PER_SEC);
  return 0;
}
