/* mod14.c - C re-derivation of the mod-d projection obstruction for K_8^(2) (q = 56), independent of mitm.py.
   Enumerate every 8-subset S of Z_56 with 0 in S and all 28 pair sums distinct (recursive, increasing elements);
   for each, count its sums in each residue class mod d (d | 56). A harmonious labeling needs two such sets whose
   class counts add to 56/d in every class.  Prints the number of sets, number of distinct vectors, and the number of
   sets whose complementary vector occurs.  Vectors encoded base (56/d+1). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int q=56, n=8, d;
static int A[8]; static long long nS=0;
static unsigned long long *keys; static long long nk=0, cap=1<<22;
static unsigned long long enc(unsigned long long mask){
  int cnt[64]={0}; for(int s=0;s<q;s++) if(mask>>s&1) cnt[s%d]++;
  unsigned long long k=0; for(int r=0;r<d;r++) k=k*(q/d+1)+cnt[r]; return k;
}
static unsigned long long comp(unsigned long long k){
  int cnt[64]; for(int r=d-1;r>=0;r--){cnt[r]=k%(q/d+1); k/=(q/d+1);}
  unsigned long long c=0; for(int r=0;r<d;r++) c=c*(q/d+1)+(q/d-cnt[r]); return c;
}
static void rec(int k,int lo,unsigned long long used){
  if(k==n){ nS++; if(nk==cap){cap*=2; keys=realloc(keys,cap*8);} keys[nk++]=enc(used); return; }
  for(int x=lo;x<q;x++){
    unsigned long long add=0; int ok=1;
    for(int i=0;i<k;i++){ int s=(x+A[i])%q; if((used|add)>>s&1){ok=0;break;} add|=1ULL<<s; }
    if(!ok) continue; A[k]=x; rec(k+1,x+1,used|add);
  }
}
static int cmp(const void*a,const void*b){unsigned long long x=*(unsigned long long*)a,y=*(unsigned long long*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){
  d=atoi(argv[1]); keys=malloc(cap*8);
  A[0]=0; rec(1,1,0);
  unsigned long long *all=malloc(nk*8); memcpy(all,keys,nk*8);
  qsort(keys,nk,8,cmp); long long nd=0; for(long long i=0;i<nk;i++) if(i==0||keys[i]!=keys[i-1]) keys[nd++]=keys[i];
  long long alive=0;
  for(long long i=0;i<nk;i++){ unsigned long long c=comp(all[i]); if(bsearch(&c,keys,nd,8,cmp)) alive++; }
  printf("d=%d sets=%lld distinct_vectors=%lld sets_with_compatible_partner_vector=%lld\n",d,nS,nd,alive);
  return 0;
}
