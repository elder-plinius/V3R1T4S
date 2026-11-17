// Depth-major greedy construction of a digital (t,m,s)-net over F_2 (derived from gvgreedy4.c).
// F_4 = F_2[w]/(w^2+w+1). Vector in F_4^m packed as lo | hi<<m (element a0 + a1*w -> bits lo=a0, hi=a1).
// Addition = XOR. Row j (1-based) of matrix i must avoid span(own rows <j) + {sums with NRT weight <= k-j over other matrices' placed rows}.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
static int m,s,k; static u32 MASK;
static u32 rows[64][32]; static int placed[64];
static uint8_t *bm; static u32 *own; static int nown;
static u32 *P[64][32]; static int nP[64][32];
static u32 mulw(u32 v){u32 lo=v&MASK, hi=(v>>m)&MASK; return hi | ((lo^hi)<<m);}
static u32 mulc(u32 v,int c){ return c? v:0; }
static uint64_t rng=88172645463325252ULL;
static uint64_t xr(void){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}
static int cur_i;
static void mark_all(u32 acc){ for(int l=0;l<nown;l++){u32 x=acc^own[l]; bm[x>>3]|=1<<(x&7);} }
static void dfs(int o,int w,u32 acc){
  if(w==0||o==s){ mark_all(acc); return; }
  dfs(o+1,w,acc);
  if(o==cur_i) return;
  int R=placed[o]; if(R>w) R=w;
  for(int r=1;r<=R;r++) for(int a=0;a<nP[o][r];a++) dfs(o+1,w-r,acc^P[o][r][a]);
}
// span of first n rows of matrix o (all F4 combos)
static int span(int o,int n,u32 *out){ int sz=1; out[0]=0; for(int r=0;r<n;r++){ int old=sz; {u32 v=rows[o][r]; for(int x=0;x<old;x++) out[sz++]=out[x]^v;} } return sz; }
static void buildP(int o){ int r=placed[o]; // vectors with top exactly at row r
  u32 *tmp=malloc(sizeof(u32)<<(r-1)); int n=span(o,r-1,tmp);
  P[o][r]=malloc(sizeof(u32)*n); int c2=0;
  {u32 v=rows[o][r-1]; for(int x=0;x<n;x++) P[o][r][c2++]=tmp[x]^v;}
  nP[o][r]=c2; free(tmp);}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage: m s t seed\n");return 1;}
  m=atoi(argv[1]); s=atoi(argv[2]); int t=atoi(argv[3]); rng ^= (uint64_t)atoll(argv[4])*0x9E3779B97F4A7C15ULL; for(int z=0;z<10;z++)xr();
  k=m-t; MASK=(1u<<m)-1; u32 N=1u<<m;
  bm=malloc(N/8); own=malloc(sizeof(u32)<<k);
  for(int j=1;j<=k;j++) for(int i=0;i<s;i++){
    memset(bm,0,N/8); cur_i=i; nown=span(i,j-1,own);
    dfs(0,k-j,0);
    u32 nfree=0; for(u32 x=0;x<N;x++) if(!(bm[x>>3]>>(x&7)&1)) nfree++;
    if(nfree==0){ printf("FAIL at j=%d i=%d\n",j,i); return 2; }
    u32 pick=xr()%nfree, x=0; for(;;x++){ if(!(bm[x>>3]>>(x&7)&1)){ if(pick==0)break; pick--; } }
    rows[i][j-1]=x; placed[i]=j; buildP(i);
    fprintf(stderr,"j=%d i=%d free=%u (%.4f)\n",j,i,nfree,(double)nfree/N);
  }
  // output: s matrices, each k rows (only first k rows matter for t); entries 0..3 with 2 = w, 3 = w^2 = w+1
  printf("# digital (%d,%d,%d)-net over F2; first k=%d rows of each C_i, columns 1..m\n",t,m,s,k);
  for(int i=0;i<s;i++){ for(int r=0;r<k;r++){ u32 v=rows[i][r]; for(int c=0;c<m;c++){printf("%d",(int)((v>>c)&1));} printf("\n"); } printf("\n"); }
  return 0;
}
