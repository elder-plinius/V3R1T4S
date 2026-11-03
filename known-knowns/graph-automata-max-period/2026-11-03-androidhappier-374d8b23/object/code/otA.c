/* Program A: max cycle length of outer-totalistic CA on graphs (graph6 on stdin), over ALL rules (B,S),
   B,S subsets of {0..n-1} (2^(2n) rules, no pruning).  Rule mask R: bit c = (c in B), bit n+c = (c in S).
   next(v) = ON iff  (v OFF and c(v) in B) or (v ON and c(v) in S), c(v) = # ON neighbours.
   Rules walked in Gray-code order: flipping rule bit k XORs delta_k into the successor table.
   Output: one line per graph "g6 maxperiod", then summary. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 8
static int n; static uint32_t adj[MAXN];
static int decode(const char *s){
  int k=0; n=s[k++]-63; if(n<1||n>MAXN) return 0; memset(adj,0,sizeof adj);
  int byte=0, bi=6;
  for(int j=1;j<n;j++) for(int i=0;i<j;i++){
    if(bi==6){ byte=s[k++]-63; bi=0; }
    if((byte>>(5-bi))&1){ adj[i]|=1u<<j; adj[j]|=1u<<i; } bi++;
  }
  return 1;
}
static uint32_t gray(uint32_t g){ return g^(g>>1); }
int main(int argc,char**argv){
  int pergraph = argc>1 && !strcmp(argv[1],"pg");
  char line[256]; static uint8_t delta[2*MAXN][1<<MAXN]; static uint8_t nxt[1<<MAXN];
  static uint32_t mark[1<<MAXN], pos[1<<MAXN];
  long long graphs=0; int best=0, nn=0; char bg[256]=""; uint32_t brule=0, bstate=0; static long long hist[1<<MAXN];
  uint32_t E=0;
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(!line[0]||line[0]=='>') continue;
    if(!decode(line)){fprintf(stderr,"bad\n");return 1;}
    nn=n; graphs++; uint32_t N=1u<<n; int K=2*n;
    memset(delta,0,sizeof delta);
    for(uint32_t s=0;s<N;s++) for(int v=0;v<n;v++){ int c=__builtin_popcount(s&adj[v]); int k=c+n*((s>>v)&1); delta[k][s]|=1u<<v; }
    memset(nxt,0,sizeof nxt); memset(mark,0,sizeof mark); E=0;
    int gbest=0;
    for(uint32_t g=0; g<(1u<<K); g++){
      if(g){ int k=__builtin_ctz(g); for(uint32_t s=0;s<N;s++) nxt[s]^=delta[k][s]; }
      uint32_t R=gray(g);
      uint32_t base=E;
      if(E > 0xF0000000u){ memset(mark,0,sizeof mark); E=0; base=0; }
      for(uint32_t s=0;s<N;s++){ if(mark[s]>base) continue; E++; uint32_t x=s,p=0;
        while(mark[x]<=base){ mark[x]=E; pos[x]=p++; x=nxt[x]; }
        if(mark[x]==E){ int L=p-pos[x]; if(L>gbest) gbest=L; if(L>best){ best=L; strcpy(bg,line); brule=R; bstate=x; } }
      }
    }
    hist[gbest]++;
    if(pergraph) printf("%s %d\n",line,gbest);
  }
  printf("n=%d graphs=%lld maxperiod=%d witness_graph6=%s witness_rule_mask=%u witness_state=%u B={",nn,graphs,best,bg,brule,bstate);
  int first=1; for(int k=0;k<nn;k++) if((brule>>k)&1){ printf(first?"%d":",%d",k); first=0; } printf("} S={");
  first=1; for(int k=0;k<nn;k++) if((brule>>(nn+k))&1){ printf(first?"%d":",%d",k); first=0; } printf("}\n");
  for(int i=0;i<(1<<MAXN);i++) if(hist[i]) printf("hist %d %lld\n",i,hist[i]);
  return 0;
}
