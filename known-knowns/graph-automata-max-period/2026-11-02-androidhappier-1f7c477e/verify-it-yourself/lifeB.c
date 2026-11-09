/* Program B (independent of A): for CONNECTED graphs (graph6 on stdin), collect the SET of Life cycle lengths.
   Successor map built bit-sliced over all 2^n states at once; cycles found by Kahn-style trimming of transient
   states (in-degree peeling), then walking each remaining cycle once.
   Output: graphs count, union of achievable cycle lengths, the max, and one witness per length (first seen). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 11
#define MAXS (1<<MAXN)
#define W (MAXS/64)
static int n;
static int A[MAXN][MAXN];
static int parse_g6(const char*s){
  const unsigned char*p=(const unsigned char*)s; n=*p++-63; if(n<1||n>MAXN) return 0;
  memset(A,0,sizeof A); int need=n*(n-1)/2, done=0;
  while(done<need){ int x=*p++-63; if(x<0||x>63) return 0;
    for(int b=5;b>=0&&done<need;b--){ /* column-major upper triangle: (0,1),(0,2),(1,2),(0,3)... */
      static int i,j; if(done==0){i=0;j=1;}
      if((x>>b)&1){A[i][j]=A[j][i]=1;}
      done++; i++; if(i==j){j++;i=0;}
    } }
  return 1;
}
int main(void){
  static char line[512]; static uint64_t X[MAXN][W], NEW[MAXN][W];
  static uint16_t succ[MAXS]; static int indeg[MAXS]; static uint8_t alive_[MAXS]; static uint16_t stack[MAXS];
  static char wit_g[MAXS+1][64]; static int wit_s[MAXS+1]; static int have[MAXS+1];
  long long graphs=0; int nn=0;
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(!line[0]||line[0]=='>') continue;
    if(!parse_g6(line)){fprintf(stderr,"parse error\n");return 1;}
    nn=n; graphs++; int S=1<<n, words=(S+63)/64;
    for(int v=0;v<n;v++) for(int w=0;w<words;w++){ uint64_t m=0;
      for(int b=0;b<64;b++){ int s=w*64+b; if(s<S && ((s>>v)&1)) m|=1ULL<<b; } X[v][w]=m; }
    for(int v=0;v<n;v++) for(int w=0;w<words;w++){
      uint64_t c0=0,c1=0,c2=0,c3=0; /* 4-bit bit-sliced counter */
      for(int u=0;u<n;u++) if(A[v][u]){ uint64_t a=X[u][w], t;
        t=c0&a; c0^=a; a=t; t=c1&a; c1^=a; a=t; t=c2&a; c2^=a; a=t; c3^=a; }
      uint64_t eq3=c0&c1&~c2&~c3, eq2=~c0&c1&~c2&~c3;
      NEW[v][w]= eq3 | (X[v][w]&eq2);
    }
    for(int s=0;s<S;s++){ int t=0; for(int v=0;v<n;v++) if((NEW[v][s>>6]>>(s&63))&1) t|=1<<v; succ[s]=t; }
    for(int s=0;s<S;s++){indeg[s]=0; alive_[s]=1;}
    for(int s=0;s<S;s++) indeg[succ[s]]++;
    int sp=0; for(int s=0;s<S;s++) if(!indeg[s]) stack[sp++]=s;
    while(sp){ int s=stack[--sp]; alive_[s]=0; int t=succ[s]; if(--indeg[t]==0) stack[sp++]=t; }
    for(int s=0;s<S;s++) if(alive_[s]){ int L=0,x=s; do{ alive_[x]=0; x=succ[x]; L++; }while(x!=s);
      if(!have[L]){ have[L]=1; strncpy(wit_g[L],line,63); wit_s[L]=s; } }
  }
  int mx=0; for(int L=1;L<=MAXS;L++) if(have[L]) mx=L;
  printf("order=%d connected_graphs=%lld max_cycle=%d\n",nn,graphs,mx);
  printf("periods:"); for(int L=1;L<=MAXS;L++) if(have[L]) printf(" %d",L); printf("\n");
  for(int L=1;L<=MAXS;L++) if(have[L]) printf("witness %d %s %d\n",L,wit_g[L],wit_s[L]);
  return 0;
}
