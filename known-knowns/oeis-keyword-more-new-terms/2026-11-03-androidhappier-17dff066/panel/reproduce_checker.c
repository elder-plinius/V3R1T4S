/* Own checker from definition (A331783): locally disjoint rooted semi-identity trees.
   Tree = k leaf children + SET of distinct non-leaf children, non-leaf children pairwise
   having disjoint child-type sets ("support"; leaf type id 0 counts as an element). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
int N,n,curK; int *sz; ll *S; int *D; ll nT, nD; int sizeEnd[64];
ll *oS; int *oD; ll noS,noD; char *used; int chosen[64]; int nch; ll c;
#define CAP_T 20000000LL
#define CAP_D 200000000LL
void go(int last,int rem){
  if(rem==0){ if(curK+nch>=1){ c++; if(n<N){ oS[noS++]=noD; if(curK>0) oD[noD++]=0; for(int i=0;i<nch;i++) oD[noD++]=chosen[i]; } } return; }
  int hi=sizeEnd[rem];
  for(int id=last+1; id<hi; id++){
    int s=sz[id]; if(s>rem) continue;
    ll a=S[id], b=S[id+1]; int ok=1;
    for(ll j=a;j<b;j++) if(used[D[j]]){ok=0;break;}
    if(!ok) continue;
    for(ll j=a;j<b;j++) used[D[j]]=1;
    chosen[nch++]=id; go(id,rem-s); nch--;
    for(ll j=a;j<b;j++) used[D[j]]=0;
  }
}
int main(int argc,char**argv){
  N=atoi(argv[1]);
  sz=malloc(CAP_T*sizeof(int)); S=malloc((CAP_T+1)*sizeof(ll)); D=malloc(CAP_D*sizeof(int));
  oS=malloc(CAP_T*sizeof(ll)); oD=malloc(CAP_D/2*sizeof(int)); used=calloc(CAP_T,1);
  sz[0]=1; S[0]=0; S[1]=0; nT=1; nD=0; sizeEnd[1]=1;
  printf("1 1\n"); fflush(stdout);
  for(n=2;n<=N;n++){
    c=0; noS=0; noD=0;
    for(curK=n-1; curK>=0; curK--){ nch=0; go(0,n-1-curK); }
    if(n<N){
      for(ll i=0;i<noS;i++){ S[nT+i]=nD+oS[i]; sz[nT+i]=n; }
      memcpy(D+nD,oD,noD*sizeof(int)); nD+=noD; nT+=noS; S[nT]=nD;
    }
    sizeEnd[n]=nT;
    printf("%d %lld\n",n,c); fflush(stdout);
  }
  return 0;
}
