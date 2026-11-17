/* Program A: max cycle length of totalistic CA on graphs (graph6 on stdin), over all rules R subset {0..K-1}.
   Usage: totA [self]   default: count only neighbours (A357953); "self": count neighbours + node (A357952).
   next(v) = ON iff count(v) in R. K = n (neighbours only) or n+1 (with self). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 10
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
int main(int argc,char**argv){
  int self = argc>1 && !strcmp(argv[1],"self");
  char line[256]; static uint8_t cnt[MAXN][1<<MAXN]; static uint32_t nxt[1<<MAXN], stamp[1<<MAXN], pos[1<<MAXN];
  long long graphs=0; int best=0, nn=0; char bg[256]=""; uint32_t brule=0, bstate=0; static long long hist[1<<MAXN];
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(!line[0]||line[0]=='>') continue;
    if(!decode(line)){fprintf(stderr,"bad\n");return 1;}
    nn=n; graphs++; uint32_t N=1u<<n; int K = self? n+1 : n;
    for(int v=0;v<n;v++) for(uint32_t s=0;s<N;s++) cnt[v][s]=__builtin_popcount(s&adj[v]) + (self? (s>>v)&1 : 0);
    int gbest=0;
    for(uint32_t R=0;R<(1u<<K);R++){
      for(uint32_t s=0;s<N;s++){ uint32_t t=0; for(int v=0;v<n;v++) t|=((R>>cnt[v][s])&1u)<<v; nxt[s]=t; stamp[s]=0; }
      for(uint32_t s=0;s<N;s++){ if(stamp[s]) continue; uint32_t x=s,p=0;
        while(!stamp[x]){ stamp[x]=s+1; pos[x]=p++; x=nxt[x]; }
        if(stamp[x]==s+1){ int L=p-pos[x]; if(L>gbest) gbest=L; if(L>best){ best=L; strcpy(bg,line); brule=R; bstate=x; } }
      }
    }
    hist[gbest]++;
  }
  printf("n=%d mode=%s graphs=%lld maxperiod=%d witness_graph6=%s witness_rule_mask=%u witness_state=%u rule={",nn,self?"self":"neighbours",graphs,best,bg,brule,bstate);
  int first=1; for(int k=0;k<32;k++) if((brule>>k)&1){ printf(first?"%d":",%d",k); first=0; } printf("}\n");
  for(int i=0;i<(1<<MAXN);i++) if(hist[i]) printf("hist %d %lld\n",i,hist[i]);
  return 0;
}
