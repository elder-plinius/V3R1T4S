/* checkK: per-line certificate check for graceful labelings of connected cubic graphs (written separately from glab).
   Usage: checkK n < cert_n.txt > graphs_n.g6     (writes the graph6 column for the coverage step)
   For each line "<graph6> f0 .. f(n-1)": decode graph6 (own decoder), require exactly n vertices, all degrees 3,
   connected; labels distinct integers in [0,q], q=3n/2; edge differences |f(u)-f(v)| form exactly {1..q}.
   Prints "CHECKK n=<n> lines=<L> bad=<B>" on stderr; exit 0 iff bad==0 and L>0. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
  if(argc<2){fprintf(stderr,"usage\n");return 2;}
  int N=atoi(argv[1]), Q=3*N/2; char *line=malloc(1<<16); long long L=0,B=0;
  while(fgets(line,1<<16,stdin)){
    int len=strlen(line); while(len&&(line[len-1]=='\n'||line[len-1]=='\r')) line[--len]=0; if(!len) continue;
    L++; char *sp=strchr(line,' '); int bad=0;
    if(!sp){ bad=1; goto done; }
    *sp=0; char *g=line; int n=g[0]-63;
    if(n!=N){ bad=2; goto done; }
    int nbits=n*(n-1)/2, nch=(nbits+5)/6; if((int)strlen(g)!=1+nch){ bad=3; goto done; }
    static int A[64][64]; memset(A,0,sizeof A); int deg[64]={0}; int k=0;
    for(int j=1;j<n;j++) for(int i=0;i<j;i++,k++){ int c=g[1+k/6]-63; if(c<0||c>63){bad=4;goto done;} if((c>>(5-k%6))&1){A[i][j]=A[j][i]=1;deg[i]++;deg[j]++;} }
    for(int v=0;v<n;v++) if(deg[v]!=3){bad=5;goto done;}
    /* connected */
    int seen[64]={0},st[64],t=0,cnt=1; seen[0]=1; st[t++]=0;
    while(t){int v=st[--t]; for(int w=0;w<n;w++) if(A[v][w]&&!seen[w]){seen[w]=1;cnt++;st[t++]=w;}}
    if(cnt!=n){bad=6;goto done;}
    /* labels */
    int f[64], used[200]={0}; char *p=sp+1, *e;
    for(int v=0;v<n;v++){ long x=strtol(p,&e,10); if(e==p){bad=7;goto done;} p=e; if(x<0||x>Q){bad=8;goto done;} if(used[x]){bad=9;goto done;} used[x]=1; f[v]=(int)x; }
    while(*p==' ') p++; if(*p){bad=10;goto done;}
    int dseen[200]={0}, m=0;
    for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(A[i][j]){ int d=abs(f[i]-f[j]); m++; if(d<1||d>Q||dseen[d]){bad=11;goto done;} dseen[d]=1; }
    if(m!=Q){bad=12;goto done;}
    for(int d=1;d<=Q;d++) if(!dseen[d]){bad=13;goto done;}
    printf("%s\n",g);
  done:
    if(bad){ B++; if(B<=10) fprintf(stderr,"BAD line %lld code %d\n",L,bad); }
  }
  fprintf(stderr,"CHECKK n=%d lines=%lld bad=%lld\n",N,L,B);
  return (B==0&&L>0)?0:1;
}
