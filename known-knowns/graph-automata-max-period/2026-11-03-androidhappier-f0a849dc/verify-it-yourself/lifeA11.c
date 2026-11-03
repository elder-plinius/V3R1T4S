/* Program A for A384209: max Life cycle period over graphs (graph6 lines on stdin), any n <= 12.
   Life: live vertex stays live iff 2 or 3 live neighbours; dead vertex born iff exactly 3 live neighbours.
   Successor table: states visited in Gray-code order; the 4-bit live-neighbour counts of all vertices are packed
   in one 64-bit word and updated by +/- a precomputed neighbour pattern when one vertex flips; "count==3" and
   "count==2" are found per nibble with SWAR zero tests and compressed to a state with pext.
   Cycles: walk from every unvisited start, epoch stamps.
   Output: summary, witness (graph with the largest period seen first, and a state on that cycle),
   "hist_all <max> <graphs>", "hist_conn <max> <connected graphs>", and "high <g6> <max> <connected>" for max >= HIGH. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>
#define MAXN 12
#define HIGH 40
static int n; static uint32_t adj[MAXN];
static int decode(const char *s){ int k=0; n=s[k++]-63; if(n<1||n>MAXN) return 0; memset(adj,0,sizeof adj);
  int byte=0,bi=6; for(int j=1;j<n;j++) for(int i=0;i<j;i++){ if(bi==6){byte=s[k++]-63;bi=0;} if((byte>>(5-bi))&1){adj[i]|=1u<<j;adj[j]|=1u<<i;} bi++; } return 1; }
static int connected(void){ uint32_t seen=1, fr=1, all=(1u<<n)-1;
  while(fr){ uint32_t nf=0; for(int v=0;v<n;v++) if(fr>>v&1) nf|=adj[v]; nf&=~seen; seen|=nf; fr=nf; } return seen==all; }
int main(void){
  char line[256]; static uint16_t nxt[1<<MAXN]; static uint32_t mark[1<<MAXN]; static uint16_t pos[1<<MAXN];
  long long cnt=0, ccnt=0; int best=0, nn=0; char bg[256]=""; uint32_t bstate=0, E=0;
  static long long hall[(1<<MAXN)+1], hconn[(1<<MAXN)+1];
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0; if(!line[0]||line[0]=='>') continue; if(!decode(line)){fprintf(stderr,"bad\n");return 1;}
    nn=n; cnt++;
    uint32_t N=1u<<n; uint64_t inc[MAXN]; uint64_t H=0,L7=0,K3=0,K2=0;
    for(int v=0;v<n;v++){ H|=8ull<<(4*v); L7|=7ull<<(4*v); K3|=3ull<<(4*v); K2|=2ull<<(4*v); }
    for(int u=0;u<n;u++){ inc[u]=0; for(int v=0;v<n;v++) if(adj[u]>>v&1) inc[u]+=1ull<<(4*v); }
    uint64_t c=0; nxt[0]=0;
    for(uint32_t i=1;i<N;i++){ int u=__builtin_ctz(i); uint32_t s=i^(i>>1);
      if(s>>u&1) c+=inc[u]; else c-=inc[u];
      uint64_t y3=c^K3, y2=c^K2;
      uint64_t z3=~(((y3&L7)+L7)|y3)&H, z2=~(((y2&L7)+L7)|y2)&H;
      nxt[s]=(uint16_t)_pext_u64(z3|(z2&_pdep_u64(s,H)),H);
    }
    if(E>0xF0000000u){ memset(mark,0,sizeof mark); E=0; }
    uint32_t base=E; int gbest=0; uint32_t gs=0;
    for(uint32_t s=0;s<N;s++){ if(mark[s]>base) continue; E++; uint32_t x=s; uint16_t p=0;
      while(mark[x]<=base){ mark[x]=E; pos[x]=p++; x=nxt[x]; }
      if(mark[x]==E){ int Lc=p-pos[x]; if(Lc>gbest){ gbest=Lc; gs=x; } } }
    int con=connected(); hall[gbest]++; if(con){ ccnt++; hconn[gbest]++; }
    if(gbest>=HIGH) printf("high %s %d %d\n",line,gbest,con);
    if(gbest>best){ best=gbest; strcpy(bg,line); bstate=gs; }
  }
  printf("n=%d graphs=%lld connected=%lld maxperiod=%d witness_graph6=%s witness_state=%u\n",nn,cnt,ccnt,best,bg,bstate);
  for(int i=0;i<=(1<<MAXN);i++) if(hall[i]) printf("hist_all %d %lld\n",i,hall[i]);
  for(int i=0;i<=(1<<MAXN);i++) if(hconn[i]) printf("hist_conn %d %lld\n",i,hconn[i]);
  return 0; }
