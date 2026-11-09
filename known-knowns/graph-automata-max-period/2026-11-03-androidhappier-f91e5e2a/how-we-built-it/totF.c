/* totF: max cycle length of totalistic CA on connected graphs (graph6 on stdin), all rules.
   Usage: totF [self] [thresh]. default counts neighbours only (A357953); "self" adds the node's own state (A357952).
   next(v)=ON iff count(v) in R. count(v) <= deg(v) (+1 with self) <= D (+1), so rule bits above Kmax=D(+1)
   never influence the dynamics: enumerating R subset {0..Kmax} is complete (R restricted to {0..Kmax} gives the
   same successor map as any R' agreeing on {0..Kmax}).
   Rules walked in Gray-code order: toggling count k XORs mask M_k[s] (vertices whose count is k in state s).
   Output: summary, histogram of per-graph maxima, graphs with max >= thresh, FNV-1a hash of the per-graph max
   sequence in input order. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 11
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
static uint16_t M[MAXN+2][1<<MAXN] __attribute__((aligned(64)));
static uint16_t nxt[1<<MAXN] __attribute__((aligned(64)));
static uint32_t stamp[1<<MAXN], pos[1<<MAXN];
int main(int argc,char**argv){
  int self=0, thresh=1000000;
  for(int i=1;i<argc;i++){ if(!strcmp(argv[i],"self")) self=1; else thresh=atoi(argv[i]); }
  char line[256]; long long graphs=0; static long long hist[4096]; int best=0, nn=0;
  char bg[256]=""; uint32_t brule=0, bstate=0; uint64_t h=1469598103934665603ULL; uint32_t epoch=0;
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(!line[0]||line[0]=='>') continue;
    if(!decode(line)){fprintf(stderr,"bad\n");return 1;}
    nn=n; graphs++; uint32_t N=1u<<n; int D=0;
    for(int v=0;v<n;v++){ int d=__builtin_popcount(adj[v]); if(d>D) D=d; }
    int Kmax = D + self;
    for(int k=0;k<=Kmax;k++) memset(M[k],0,N*sizeof(uint16_t));
    for(uint32_t s=0;s<N;s++) for(int v=0;v<n;v++){
      int c=__builtin_popcount(s&adj[v]) + (self? (int)((s>>v)&1) : 0); M[c][s]|=(uint16_t)(1u<<v); }
    memset(nxt,0,N*sizeof(uint16_t));
    uint32_t R=0; int gbest=1; uint32_t nR = 1u<<(Kmax+1);
    for(uint32_t i=1;i<nR;i++){
      int k=__builtin_ctz(i); R^=1u<<k; uint16_t *mk=M[k];
      for(uint32_t s=0;s<N;s++) nxt[s]^=mk[s];
      if(epoch > 0xFFFFFFFFu - 2*N){ memset(stamp,0,sizeof stamp); epoch=0; }
      uint32_t base=epoch;
      for(uint32_t s=0;s<N;s++){
        if(stamp[s]>base) continue;
        uint32_t id=++epoch, x=s, p=0;
        while(stamp[x]<=base){ stamp[x]=id; pos[x]=p++; x=nxt[x]; }
        if(stamp[x]==id){ int L=p-pos[x]; if(L>gbest){ gbest=L; }
          if(L>best){ best=L; strcpy(bg,line); brule=R; bstate=x; } }
      }
    }
    hist[gbest]++;
    if(gbest>=thresh) printf("high %d %s\n",gbest,line);
    h ^= (uint64_t)gbest; h *= 1099511628211ULL;
  }
  printf("n=%d mode=%s graphs=%lld maxperiod=%d witness_graph6=%s witness_rule_mask=%u witness_state=%u rule={",
         nn,self?"self":"neighbours",graphs,best,bg,brule,bstate);
  int first=1; for(int k=0;k<32;k++) if((brule>>k)&1){ printf(first?"%d":",%d",k); first=0; } printf("}\n");
  for(int i=0;i<4096;i++) if(hist[i]) printf("hist %d %lld\n",i,hist[i]);
  printf("fnv %016llx\n",(unsigned long long)h);
  return 0;
}
