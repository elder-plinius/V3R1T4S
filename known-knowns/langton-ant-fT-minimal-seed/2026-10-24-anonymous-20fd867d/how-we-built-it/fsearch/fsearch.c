/* fsearch.c — exact minimal-seed search for Langton's ant (run 2026-10-23-1306).
 * Rule: white -> turn right, black -> turn left, flip, move. Ant starts at (0,0) heading N (wlog: rotation+translation).
 * dirs 0:N(0,-1) 1:E(1,0) 2:S(0,1) 3:W(-1,0)  (y down), right turn = +1.
 * Forward branching over first reads: when the ant first reads a cell, branch white / black (black costs 1).
 * At every time t (0..Tmax) the completion test: for each of the 104 highway phases p of the blank orbit
 * (steps 9977..10080, rotated to heading N), walk the phase's future first-read list R_p (80 periods):
 * read cell -> its current colour must equal the phase's colour; unread cell -> if phase needs black, cost+1.
 * Feasible iff u + cost <= K. Then the configuration (placed cells + unread forced cells) is on the highway at t
 * (Jillhewar Thm 3.1 / LEMMA.md Lemma 1). Reports least such t (= g(K)) and every minimiser at that t.
 * usage: fsearch K TMAX   (searches t <= TMAX; prints best t and minimisers, or NONE <= TMAX) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define LG 11
#define SZ (1<<LG)
#define C0 (SZ/2)
#define NPER 80
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static uint8_t G[SZ*SZ];         /* bit0 colour, bit1 read */
typedef struct {int dx,dy; uint8_t col;} rc_t;
static rc_t *RP[104]; static int RL[104]; static int Dmin=1<<30;
static int K; static long TMAX;
static long best; static long nsol=0, nodes=0, flagged=0;
static int maxR=0;
/* undo log */
typedef struct {int idx; uint8_t old;} lg_t;
static lg_t *LOG; static long lp=0, lcap=1<<26;
static int px[4096], py[4096], np_=0; /* placed blacks (absolute, rel origin) */
static FILE *solf;
static inline void setc(int idx, uint8_t v){ LOG[lp].idx=idx; LOG[lp].old=G[idx]; lp++; G[idx]=v; }
static void rot(int dx,int dy,int h,int*ox,int*oy){ /* frame where heading h becomes N: rotate by -h */
  for(int i=0;i<h;i++){ int t=dx; dx=dy; dy=-t; } *ox=dx;*oy=dy; }
static void unrot(int dx,int dy,int h,int*ox,int*oy){ for(int i=0;i<h;i++){int t=dx; dx=-dy; dy=t;} *ox=dx;*oy=dy; }
static void build_phases(void){
  memset(G,0,sizeof G); int x=C0,y=C0,h=0;
  for(long t=0;t<9977;t++){ int i=y*SZ+x; int g=G[i]&1; h=(h+(g?3:1))&3; G[i]^=1; x+=DX[h]; y+=DY[h]; }
  static uint8_t H[SZ*SZ]; static int seen[SZ*SZ];
  for(int p=0;p<104;p++){
    memcpy(H,G,sizeof G); memset(seen,0,sizeof seen);
    int X=x,Y=y,hh=h; RP[p]=malloc(sizeof(rc_t)*104*NPER); RL[p]=0;
    for(long s=0;s<104L*(NPER+6);s++){ int i=Y*SZ+X; int g=H[i]&1;
      if(!seen[i]){ seen[i]=1; int ox,oy; rot(X-x,Y-y,h,&ox,&oy);
        if(s<104L*NPER){ RP[p][RL[p]].dx=ox; RP[p][RL[p]].dy=oy; RP[p][RL[p]].col=g; RL[p]++; }
        else { int d=abs(ox)>abs(oy)?abs(ox):abs(oy); if(d<Dmin) Dmin=d; } }
      hh=(hh+(g?3:1))&3; H[i]^=1; X+=DX[hh]; Y+=DY[hh]; }
    int i=y*SZ+x; int g=G[i]&1; h=(h+(g?3:1))&3; G[i]^=1; x+=DX[h]; y+=DY[h];
  }
  int mn=99,mx=0; for(int p=0;p<104;p++){int c=0; for(int j=0;j<RL[p];j++) c+=RP[p][j].col; if(c<mn)mn=c; if(c>mx)mx=c;}
  fprintf(stderr,"phases built: forced-set size min %d max %d, Dmin(after %d periods)=%d\n",mn,mx,NPER,Dmin);
  memset(G,0,sizeof G);
}
/* completion cost at current state; returns min cost over phases and best phase */
static int completion(int x,int y,int h,int budget,int*bp){
  int bestc=budget+1;
  for(int p=0;p<104;p++){ int c=0, ok=1; rc_t*r=RP[p];
    for(int j=0;j<RL[p];j++){ int ax,ay; unrot(r[j].dx,r[j].dy,h,&ax,&ay); int i=(y+ay)*SZ+(x+ax); uint8_t v=G[i];
      if(v&2){ if((v&1)!=r[j].col){ok=0;break;} } else if(r[j].col){ if(++c>=bestc){ok=0;break;} } }
    if(ok && c<bestc){bestc=c;*bp=p;} }
  return bestc;
}
static int phase_cost(int x,int y,int h,int p){ int c=0; rc_t*r=RP[p];
  for(int j=0;j<RL[p];j++){ int ax,ay; unrot(r[j].dx,r[j].dy,h,&ax,&ay); uint8_t v=G[(y+ay)*SZ+(x+ax)];
    if(v&2){ if((v&1)!=r[j].col) return 1<<20; } else if(r[j].col) c++; } return c; }
static void report(long t,int x,int y,int h,int u){
  if(t<best){ best=t; nsol=0; fprintf(solf,"# new best t=%ld\n",t); }
  for(int p=0;p<104;p++){ int c=phase_cost(x,y,h,p); if(u+c>K) continue;
  nsol++;
  fprintf(solf,"t=%ld cells=%d placed=%d forced_unread=%d phase=%d cells:",t,u+c,u,c,p);
  for(int k=0;k<np_;k++) fprintf(solf," (%d,%d)",px[k],py[k]);
  rc_t*r=RP[p]; for(int j=0;j<RL[p];j++){ int ax,ay; unrot(r[j].dx,r[j].dy,h,&ax,&ay); int i=(y+ay)*SZ+(x+ax);
    if(!(G[i]&2) && r[j].col) fprintf(solf," (%d,%d)*",x+ax-C0,y+ay-C0); }
  fprintf(solf,"\n"); }
  fflush(solf);
}
static void dfs(long t,int x,int y,int h,int u){
  nodes++;
  for(;;){
    if(t>best || t>TMAX) return;
    int bp=-1; int c=completion(x,y,h,K-u,&bp);
    if(c<=K-u){ { int r=abs(x-C0)>abs(y-C0)?abs(x-C0):abs(y-C0); (void)r; }
      if(2*maxR+4>=Dmin) flagged++;
      report(t,x,y,h,u); return; } /* later times cannot beat t on this branch */
    if(t==best) return;
    int i=y*SZ+x; uint8_t v=G[i];
    if(!(v&2)){
      int r=abs(x-C0)>abs(y-C0)?abs(x-C0):abs(y-C0); int oldmax=maxR; if(r>maxR) maxR=r;
      if(u<K){ long save=lp; int sx=x,sy=y,sh=h; px[np_]=x-C0; py[np_]=y-C0; np_++;
        setc(i,3); /* read, black */
        { int g=1; int hh=(h+(g?3:1))&3; setc(i,G[i]^1); dfs(t+1,x+DX[hh],y+DY[hh],hh,u+1); }
        np_--; while(lp>save){ lp--; G[LOG[lp].idx]=LOG[lp].old; } x=sx;y=sy;h=sh; }
      setc(i,2); v=2; (void)oldmax;
    }
    int g=v&1; h=(h+(g?3:1))&3; setc(i,G[i]^1); x+=DX[h]; y+=DY[h]; t++;
    if(lp>lcap-100000){ fprintf(stderr,"log overflow\n"); exit(2);} 
    if(x<8||y<8||x>SZ-8||y>SZ-8){ fprintf(stderr,"oob\n"); exit(3);} 
  }
}
int main(int argc,char**argv){
  K=atoi(argv[1]); TMAX=atol(argv[2]); LOG=malloc(sizeof(lg_t)*lcap); solf=stdout;
  build_phases(); best=TMAX+1;
  long save=lp; dfs(0,C0,C0,0,0);
  while(lp>save){lp--;G[LOG[lp].idx]=LOG[lp].old;}
  if(best>TMAX) printf("RESULT K=%d NONE t<=%ld nodes=%ld maxR=%d Dmin=%d\n",K,TMAX,nodes,maxR,Dmin);
  else printf("RESULT K=%d best_t=%ld minimisers=%ld nodes=%ld maxR=%d Dmin=%d flagged=%ld\n",K,best,nsol,nodes,maxR,Dmin,flagged);
  return 0;
}
