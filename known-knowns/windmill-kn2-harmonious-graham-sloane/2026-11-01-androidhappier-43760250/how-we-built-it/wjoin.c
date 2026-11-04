/* wjoin.c n [d1 d2 ...] - for K_n^(2), q = n(n-1) <= 126: enumerate every n-subset S of Z_q with 0 in S and all
   C(n,2) pair sums distinct; store (sum mask, element mask). Then
   (i) exact join: count ordered pairs (S1,S2) with summask2 == ~summask1 (within q bits) and elemmask1 & elemmask2 == {0};
   (ii) for each d | q given, the mod-d class-count projection obstruction (number of sets with a compatible vector).
   Translation f -> f - f(c) is the only reduction. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static int n,q; static int A[16];
typedef struct { u128 sm, em; } rec_t;
static rec_t *R; static long long nR=0, cap=1<<20;
static u128 one=1;
static void rec(int k,int lo,u128 used,u128 em){
  if(k==n){ if(nR==cap){cap*=2; R=realloc(R,cap*sizeof(rec_t)); if(!R){fprintf(stderr,"oom\n");exit(1);} } R[nR].sm=used; R[nR].em=em; nR++; return; }
  for(int x=lo;x<q;x++){
    u128 add=0; int ok=1;
    for(int i=0;i<k;i++){ int s=(x+A[i])%q; if(((used|add)>>s)&1){ok=0;break;} add|=one<<s; }
    if(!ok) continue; A[k]=x; rec(k+1,x+1,used|add,em|(one<<x));
  }
}
static int cmpsm(const void*a,const void*b){u128 x=((rec_t*)a)->sm,y=((rec_t*)b)->sm;return x<y?-1:x>y;}
typedef unsigned long long u64;
static int cmp64(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){
  n=atoi(argv[1]); q=n*(n-1); if(q>126) return 1;
  R=malloc(cap*sizeof(rec_t)); A[0]=0; rec(1,1,0,one);
  printf("n=%d q=%d sum_distinct_sets_containing_0=%lld\n",n,q,nR); fflush(stdout);
  for(int ai=2;ai<argc;ai++){
    int d=atoi(argv[ai]); int base=q/d+1;
    u64 *v=malloc(nR*8), *s=malloc(nR*8);
    for(long long i=0;i<nR;i++){ int cnt[128]={0}; for(int t=0;t<q;t++) if((R[i].sm>>t)&1) cnt[t%d]++; u64 k=0; for(int r=0;r<d;r++) k=k*base+cnt[r]; v[i]=k; s[i]=k; }
    qsort(s,nR,8,cmp64); long long nd=0; for(long long i=0;i<nR;i++) if(i==0||s[i]!=s[i-1]) s[nd++]=s[i];
    long long alive=0;
    for(long long i=0;i<nR;i++){ int cnt[128]; u64 k=v[i]; for(int r=d-1;r>=0;r--){cnt[r]=k%base;k/=base;} u64 c=0; for(int r=0;r<d;r++) c=c*base+(q/d-cnt[r]); if(bsearch(&c,s,nd,8,cmp64)) alive++; }
    printf("d=%d distinct_vectors=%lld sets_with_compatible_partner_vector=%lld\n",d,nd,alive); fflush(stdout);
    free(v); free(s);
  }
  qsort(R,nR,sizeof(rec_t),cmpsm);
  u128 full=(one<<q)-1; long long sol=0;
  for(long long i=0;i<nR;i++){
    u128 c=full^R[i].sm; long long lo=0,hi=nR-1,f=-1;
    while(lo<=hi){ long long m=(lo+hi)/2; if(R[m].sm<c) lo=m+1; else { if(R[m].sm==c) f=m; hi=m-1; } }
    if(f<0) continue;
    for(long long j=f;j<nR&&R[j].sm==c;j++) if((R[i].em&R[j].em)==one){ sol++;
      if(sol<=10){ printf("SOLUTION A={"); for(int t=0;t<q;t++) if((R[i].em>>t)&1) printf("%d ",t); printf("} B={"); for(int t=0;t<q;t++) if((R[j].em>>t)&1) printf("%d ",t); printf("}\n"); } }
  }
  printf("n=%d solutions_ordered_pairs=%lld\nVERDICT n=%d: %s\n",n,sol,n,sol?"HARMONIOUS":"NOT HARMONIOUS");
  return 0;
}
