/* Program A: max Life cycle period over graphs read as graph6 lines on stdin.
   Life on a graph: live vertex stays live iff 2 or 3 live neighbours; dead vertex born iff exactly 3. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 12
static int n; static uint32_t adj[MAXN];
static int decode(const char *s){
  int k=0; n = s[k++]-63; if(n<1||n>MAXN) return 0;
  memset(adj,0,sizeof adj);
  int bit=0, byte=0, bi=6;
  for(int j=1;j<n;j++) for(int i=0;i<j;i++){
    if(bi==6){ byte = s[k++]-63; bi=0; }
    int b = (byte>>(5-bi))&1; bi++;
    if(b){ adj[i]|=1u<<j; adj[j]|=1u<<i; }
  }
  (void)bit; return 1;
}
int main(int argc,char**argv){
  char line[256]; static uint32_t nxt[1<<MAXN]; static uint32_t stamp[1<<MAXN]; static uint32_t pos[1<<MAXN];
  long long cnt=0; int best=0; char bestg[256]=""; uint32_t bests=0; long long hist[4096]={0};
  int nn=-1;
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(line[0]=='>'||!line[0]) continue;
    if(!decode(line)) { fprintf(stderr,"bad line\n"); return 1; }
    nn=n; cnt++;
    uint32_t N=1u<<n;
    for(uint32_t s=0;s<N;s++){
      uint32_t t=0;
      for(int v=0;v<n;v++){ int c=__builtin_popcount(s&adj[v]); int alive=(s>>v)&1;
        if(c==3 || (alive && c==2)) t|=1u<<v; }
      nxt[s]=t; stamp[s]=0;
    }
    int gbest=0; uint32_t gs=0;
    for(uint32_t s=0;s<N;s++){ if(stamp[s]) continue;
      uint32_t x=s, p=0;
      while(!stamp[x]){ stamp[x]=s+1; pos[x]=p++; x=nxt[x]; }
      if(stamp[x]==s+1){ int L=p-pos[x]; if(L>gbest){gbest=L; gs=x;} }
    }
    hist[gbest]++;
    if(gbest>best){ best=gbest; strcpy(bestg,line); bests=gs; }
  }
  printf("n=%d graphs=%lld maxperiod=%d witness_graph6=%s witness_state=%u\n",nn,cnt,best,bestg,bests);
  for(int i=0;i<4096;i++) if(hist[i]) printf("hist %d %lld\n",i,hist[i]);
  return 0;
}
