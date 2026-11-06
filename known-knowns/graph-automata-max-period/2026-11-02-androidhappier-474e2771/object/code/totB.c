/* Program B (written separately from A): totalistic CA, neighbours only (A357953), connected graphs on stdin.
   For each node v and count k, EQ[v][k] = bitmask over all 2^n states of "v has exactly k ON neighbours",
   built with a bit-sliced adder over the neighbours' state-bit masks. For a rule R the next-state mask of v is
   OR_{k in R} EQ[v][k]; masks are transposed into a successor table; transient states are removed by in-degree
   peeling, then each remaining cycle is walked once. Reports max cycle length, a witness and the per-length set. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 10
#define MAXS (1<<MAXN)
#define WMAX (MAXS/64)
static int n, A[MAXN][MAXN];
static int g6(const char*s){
  n=(unsigned char)s[0]-63; if(n<1||n>MAXN) return 0; memset(A,0,sizeof A);
  int idx=0, i=0, j=1; const char*p=s+1;
  int total=n*(n-1)/2;
  while(idx<total){ int x=(unsigned char)*p++-63;
    for(int b=5;b>=0 && idx<total;b--,idx++){ if((x>>b)&1) A[i][j]=A[j][i]=1; if(++i==j){ i=0; j++; } } }
  return 1;
}
int main(void){
  static char line[256]; static uint64_t X[MAXN][WMAX], EQ[MAXN][MAXN+1][WMAX], M[MAXN][WMAX];
  static uint16_t succ[MAXS]; static int indeg[MAXS]; static uint8_t live[MAXS]; static uint16_t st[MAXS];
  static long long lenseen[MAXS+1];
  long long graphs=0; int best=0, nn=0; char bg[64]=""; int brule=0, bstate=0;
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(!line[0]||line[0]=='>') continue;
    if(!g6(line)){ fprintf(stderr,"parse\n"); return 1; }
    nn=n; graphs++; int S=1<<n, W=(S+63)/64;
    for(int v=0;v<n;v++) for(int w=0;w<W;w++){ uint64_t m=0; for(int b=0;b<64;b++){ int s=w*64+b; if(s<S && (s>>v&1)) m|=1ULL<<b; } X[v][w]=m; }
    for(int v=0;v<n;v++) for(int w=0;w<W;w++){
      uint64_t c[4]={0,0,0,0};
      for(int u=0;u<n;u++) if(A[v][u]){ uint64_t a=X[u][w]; for(int q=0;q<4;q++){ uint64_t t=c[q]&a; c[q]^=a; a=t; } }
      for(int k=0;k<=n;k++){ uint64_t e=~0ULL; for(int q=0;q<4;q++) e &= ((k>>q)&1)? c[q] : ~c[q]; EQ[v][k][w]=e; }
    }
    for(int R=0;R<(1<<n);R++){
      for(int v=0;v<n;v++) for(int w=0;w<W;w++){ uint64_t m=0; for(int k=0;k<n;k++) if(R>>k&1) m|=EQ[v][k][w]; M[v][w]=m; }
      for(int s=0;s<S;s++){ int t=0; for(int v=0;v<n;v++) t|=(int)((M[v][s>>6]>>(s&63))&1)<<v; succ[s]=t; indeg[s]=0; live[s]=1; }
      for(int s=0;s<S;s++) indeg[succ[s]]++;
      int sp=0; for(int s=0;s<S;s++) if(!indeg[s]) st[sp++]=s;
      while(sp){ int s=st[--sp]; live[s]=0; if(--indeg[succ[s]]==0) st[sp++]=succ[s]; }
      for(int s=0;s<S;s++) if(live[s]){ int L=0,x=s; do{ live[x]=0; x=succ[x]; L++; }while(x!=s);
        lenseen[L]++; if(L>best){ best=L; strncpy(bg,line,63); brule=R; bstate=s; } }
    }
  }
  printf("order=%d connected_graphs=%lld max_cycle=%d witness %s rule_mask %d state %d\n",nn,graphs,best,bg,brule,bstate);
  printf("lengths:"); for(int L=1;L<=MAXS;L++) if(lenseen[L]) printf(" %d",L); printf("\n");
  return 0;
}
