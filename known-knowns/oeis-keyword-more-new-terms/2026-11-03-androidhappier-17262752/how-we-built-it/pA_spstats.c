/* Set-partition statistics (Gus Wiseman family), Program A (C).
   For each set partition of {1..n} (restricted growth strings):
     cro(A,B): exists x<z<y<t, x,y in A, z,t in B (either order)
     cap(A,B): exists x<z<t<y, x,y in A, z,t in B (either order)
     nes(A,B): exists consecutive x,y in A and consecutive z,t in B with x<z<t<y (either order)
   Prints n and counts:
     A326245 crossing & not capturing; A326246 crossing & capturing; A326249 capturing & not nesting;
     A326335 nesting graph connected; A326336 capturing graph connected. (empty partition: connected) */
#include <stdio.h>
#include <stdlib.h>
static int n, rgs[32], k;
static int el[32][32], sz[32];
static long long c245,c246,c249,c335,c336;
static int has_cro(int a,int b){for(int i=0;i<sz[a];i++)for(int j=i+1;j<sz[a];j++)for(int p=0;p<sz[b];p++)for(int q=p+1;q<sz[b];q++){int x=el[a][i],y=el[a][j],z=el[b][p],t=el[b][q]; if(x<z&&z<y&&y<t) return 1;} return 0;}
static int has_cap(int a,int b){for(int i=0;i<sz[a];i++)for(int j=i+1;j<sz[a];j++)for(int p=0;p<sz[b];p++)for(int q=p+1;q<sz[b];q++){int x=el[a][i],y=el[a][j],z=el[b][p],t=el[b][q]; if(x<z&&t<y) return 1;} return 0;}
static int has_nes(int a,int b){for(int i=0;i+1<sz[a];i++)for(int p=0;p+1<sz[b];p++){int x=el[a][i],y=el[a][i+1],z=el[b][p],t=el[b][p+1]; if(x<z&&t<y) return 1;} return 0;}
static int par[32]; static int fnd(int x){while(par[x]!=x)x=par[x]=par[par[x]];return x;}
static void check(void){
  for(int b=0;b<k;b++) sz[b]=0;
  for(int i=0;i<n;i++){int b=rgs[i]; el[b][sz[b]++]=i+1;}
  int cro=0,cap=0,nes=0; int pn[32],pc[32];
  for(int b=0;b<k;b++){pn[b]=b;pc[b]=b;}
  int compN=k, compC=k;
  for(int a=0;a<k;a++)for(int b=a+1;b<k;b++){
    int r= has_cro(a,b)||has_cro(b,a);
    int c= has_cap(a,b)||has_cap(b,a);
    int s= has_nes(a,b)||has_nes(b,a);
    cro|=r; cap|=c; nes|=s;
    if(s){ for(int i=0;i<k;i++) par[i]=pn[i]; int ra=fnd(a),rb=fnd(b); if(ra!=rb){par[ra]=rb;compN--;} for(int i=0;i<k;i++) pn[i]=par[i]; }
    if(c){ for(int i=0;i<k;i++) par[i]=pc[i]; int ra=fnd(a),rb=fnd(b); if(ra!=rb){par[ra]=rb;compC--;} for(int i=0;i<k;i++) pc[i]=par[i]; }
  }
  if(cro&&!cap) c245++;
  if(cro&&cap) c246++;
  if(cap&&!nes) c249++;
  if(compN<=1) c335++;
  if(compC<=1) c336++;
}
static void rec(int i,int kk){ if(i==n){k=kk;check();return;} for(int b=0;b<=kk;b++){rgs[i]=b;rec(i+1,b==kk?kk+1:kk);} }
int main(int argc,char**argv){
  int lo=atoi(argv[1]),hi=atoi(argv[2]);
  printf("n A326245 A326246 A326249 A326335 A326336\n");
  for(n=lo;n<=hi;n++){c245=c246=c249=c335=c336=0;
    if(n==0){c335=c336=1;} else {rgs[0]=0;rec(1,1);}
    printf("%d %lld %lld %lld %lld %lld\n",n,c245,c246,c249,c335,c336); fflush(stdout);}
}
