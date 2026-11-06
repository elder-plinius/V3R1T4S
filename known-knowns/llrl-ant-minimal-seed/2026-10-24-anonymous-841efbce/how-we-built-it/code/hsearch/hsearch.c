/* hsearch.c — checker A: exact least-onset search for a generalised ant reaching a given highway H
 * (run 2026-10-24-1428). Conventions as PREREG: y down, 0:N 1:E 2:S 3:W, R=+1, L=-1; on colour c turn rule[c],
 * write c+1 mod n, step; ant at origin facing N.
 * H is given as the canonical run: blank grid (or a seed file) whose highway starts at onset t0 with period P.
 * Phase lists: for each phase p (state at t0+p) the future first-read cells (relative to the ant, rotated so the
 * ant's heading is N) with the colour read, for NPER periods.  Later first reads lie at Chebyshev distance >= Dmin
 * (measured on NPER..NPER+6 periods; Dmin grows by translation) and must all read 0 (checked: zreq).
 * Search: DFS over first reads (branch each colour at a cell's first read; non-zero costs 1, budget K).
 * Every STRIDE steps: completion test (exists phase p: decided cells match, undecided forced non-zero cells
 * cost <= K-u).  On success, every feasible phase's minimal completion is re-simulated from scratch and its exact
 * onset found by backward extension of the word; best = min onset.  A branch is cut once a failed test time >= best.
 * usage: hsearch RULE K TMAX t0 P [canonseed|- [W wid SPLITD]]
 * Split (run 2026-10-24-1605): the subtree under the SCTR-th first-read node at first-read depth SPLITD goes to worker SCTR%W;
 * above SPLITD the best-cut is disabled so every worker visits the same nodes in the same order (consistent SCTR).   prints minimisers with onset == best (<= TMAX). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define LG 11
#define SZ (1<<LG)
#define C0 (SZ/2)
#define NPER 60
#define STRIDE 8
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static char rule[16]; static int n; static int K; static long TMAX,T0; static int P;
static uint8_t G[SZ*SZ];  /* bits0-3 colour, bit4 decided */
typedef struct{short dx,dy; uint8_t col;} rc_t;
static rc_t *RP[4096]; static int RL[4096]; static int Dmin=1<<30, zreqbad=0; static uint8_t W[4096];
static long best; static long nsol=0,nodes=0,flagged=0,tests=0; static int maxR=0;
typedef struct{int idx; uint8_t old;} lg_t; static lg_t *LOG; static long lp=0, lcap=1L<<26;
static int SW=1,SWID=0,SPLITD=0; static long SCTR=0;
static int px[256],py[256],pc[256],np_=0;
static inline int turn(int h,int c){ return (h+(rule[c]=='R'?1:3))&3; }
static void rot(int dx,int dy,int h,int*ox,int*oy){ for(int i=0;i<h;i++){int t=dx;dx=dy;dy=-t;} *ox=dx;*oy=dy; }
static void unrot(int dx,int dy,int h,int*ox,int*oy){ for(int i=0;i<h;i++){int t=dx;dx=-dy;dy=t;} *ox=dx;*oy=dy; }
#define BL 12
#define BS (1<<BL)
#define BC (BS/2)
static void loadseed(uint8_t*g,const char*f,int sz,int c0){ if(!f||!strcmp(f,"-"))return; FILE*F=fopen(f,"r"); int x,y,c; while(fscanf(F,"%d %d %d",&x,&y,&c)==3) g[(size_t)(y+c0)*sz+x+c0]=c; fclose(F); }
static void build(const char*canon){
  uint8_t *B=calloc((size_t)BS*BS,1),*Hh=malloc((size_t)BS*BS); int *seen=malloc(sizeof(int)*(size_t)BS*BS);
  loadseed(B,canon,BS,BC); int x=BC,y=BC,h=0;
  for(long t=0;t<T0;t++){ size_t i=(size_t)y*BS+x; int c=B[i]; h=turn(h,c); B[i]=(c+1)%n; x+=DX[h]; y+=DY[h]; }
  for(int p=0;p<P;p++){
    memcpy(Hh,B,(size_t)BS*BS); memset(seen,0,sizeof(int)*(size_t)BS*BS);
    int X=x,Y=y,hh=h; RP[p]=malloc(sizeof(rc_t)*(size_t)P*NPER); RL[p]=0;
    for(long s=0;s<(long)P*(NPER+6);s++){ size_t i=(size_t)Y*BS+X; int c=Hh[i];
      if(s<P) W[(p+s)%P]=c;
      if(!seen[i]){ seen[i]=1; int ox,oy; rot(X-x,Y-y,h,&ox,&oy);
        if(s<(long)P*NPER){ RP[p][RL[p]].dx=ox; RP[p][RL[p]].dy=oy; RP[p][RL[p]].col=c; RL[p]++; }
        else { int d=abs(ox)>abs(oy)?abs(ox):abs(oy); if(d<Dmin)Dmin=d; if(c) zreqbad++; } }
      hh=turn(hh,c); Hh[i]=(c+1)%n; X+=DX[hh]; Y+=DY[hh]; if(X<4||Y<4||X>BS-5||Y>BS-5){fprintf(stderr,"build edge\n");exit(3);} }
    size_t i=(size_t)y*BS+x; int c=B[i]; h=turn(h,c); B[i]=(c+1)%n; x+=DX[h]; y+=DY[h];
  }
  int mn=1<<30,mx=0,arg=0; for(int p=0;p<P;p++){int c=0; for(int j=0;j<RL[p];j++) c+=RP[p][j].col!=0; if(c<mn){mn=c;arg=p;} if(c>mx)mx=c;}
  fprintf(stderr,"phases built P=%d: forced non-zero first reads min %d (phase %d) max %d; Dmin(after %d periods)=%d; late non-zero first reads=%d\n",P,mn,arg,mx,NPER,Dmin,zreqbad);
  if(zreqbad){fprintf(stderr,"late first reads not all zero\n"); exit(4);}
  free(B);free(Hh);free(seen);
}
static inline void setc(int idx,uint8_t v){ LOG[lp].idx=idx; LOG[lp].old=G[idx]; lp++; G[idx]=v; }
static int phase_cost(int x,int y,int h,int p,int lim){ int c=0; rc_t*r=RP[p];
  for(int j=0;j<RL[p];j++){ int ax,ay; unrot(r[j].dx,r[j].dy,h,&ax,&ay); uint8_t v=G[(y+ay)*SZ+(x+ax)];
    if(v&16){ if((v&15)!=r[j].col) return 1<<20; } else if(r[j].col){ if(++c>lim) return 1<<20; } } return c; }
/* exact onset of a fully specified configuration that is on H at time ts with phase p: re-simulate, extend back */
static uint8_t *SG; static uint8_t *RD;
static long exact_onset(int ncell,int*cx,int*cy,int*cc,long ts,int p){
  memset(SG,0,(size_t)SZ*SZ); for(int i=0;i<ncell;i++) SG[(cy[i]+C0)*SZ+cx[i]+C0]=cc[i];
  int x=C0,y=C0,h=0; long N=ts+2L*P;
  for(long u=0;u<N;u++){ size_t i=(size_t)y*SZ+x; int c=SG[i]; RD[u]=c; h=turn(h,c); SG[i]=(c+1)%n; x+=DX[h]; y+=DY[h]; }
  for(long u=ts;u<N;u++) if(RD[u]!=W[((p+u-ts)%P+P)%P]){ fprintf(stderr,"BUG: forward word mismatch\n"); exit(5);} 
  long t=ts; while(t>0 && RD[t-1]==W[((p+t-1-ts)%P+P)%P]) t--; return t; }
static void on_success(long t,int x,int y,int h,int u){
  for(int p=0;p<P;p++){ int c=phase_cost(x,y,h,p,K-u); if(c>K-u) continue;
    int cx[256],cy[256],cc[256],m=0; for(int i=0;i<np_;i++){cx[m]=px[i];cy[m]=py[i];cc[m]=pc[i];m++;}
    rc_t*r=RP[p]; for(int j=0;j<RL[p];j++){ int ax,ay; unrot(r[j].dx,r[j].dy,h,&ax,&ay); int i=(y+ay)*SZ+(x+ax);
      if(!(G[i]&16) && r[j].col){ cx[m]=x+ax-C0; cy[m]=y+ay-C0; cc[m]=r[j].col; m++; } }
    long on=exact_onset(m,cx,cy,cc,t,p);
    if(on<best){ best=on; nsol=0; printf("# new best %ld\n",on); }
    if(on==best){ nsol++; printf("SOL onset=%ld k=%d found_t=%ld phase=%d cells:",on,m,t,p); for(int i=0;i<m;i++) printf(" (%d,%d,%d)",cx[i],cy[i],cc[i]); printf("\n"); }
  }
  fflush(stdout);
}
static void dfs(long t,int x,int y,int h,int u,int dd){
  nodes++;
  for(;;){
    if(t%STRIDE==0){ tests++;
      int ok=0; for(int p=0;p<P && !ok;p++) if(phase_cost(x,y,h,p,K-u)<=K-u) ok=1;
      if(ok){ if(2*maxR+8>=Dmin) flagged++; on_success(t,x,y,h,u); return; }
      if((dd>=SPLITD && t>=best) || t>TMAX) return; }
    int i=y*SZ+x; uint8_t v=G[i];
    if(!(v&16)){
      if(SW>1 && dd==SPLITD){ if((SCTR++)%SW!=SWID) return; }
      dd++;
      int r=abs(x-C0)>abs(y-C0)?abs(x-C0):abs(y-C0); int om=maxR; if(r>maxR)maxR=r;
      if(u<K){ for(int col=1;col<n;col++){ long save=lp; px[np_]=x-C0;py[np_]=y-C0;pc[np_]=col;np_++;
          setc(i,16|((col+1)%n)); int hh=turn(h,col); dfs(t+1,x+DX[hh],y+DY[hh],hh,u+1,dd);
          np_--; while(lp>save){lp--;G[LOG[lp].idx]=LOG[lp].old;} } }
      (void)om; setc(i,16|0); v=16;
    }
    int c=v&15; h=turn(h,c); setc(i,16|((c+1)%n)); x+=DX[h]; y+=DY[h]; t++;
    if(lp>lcap-100000){fprintf(stderr,"log overflow\n");exit(2);} if(x<8||y<8||x>SZ-8||y>SZ-8){fprintf(stderr,"oob\n");exit(3);} }
}
int main(int argc,char**argv){
  strcpy(rule,argv[1]); n=strlen(rule); K=atoi(argv[2]); TMAX=atol(argv[3]); T0=atol(argv[4]); P=atoi(argv[5]);
  const char*canon=argc>6?argv[6]:"-"; if(argc>9){SW=atoi(argv[7]);SWID=atoi(argv[8]);SPLITD=atoi(argv[9]);}
  LOG=malloc(sizeof(lg_t)*lcap); SG=malloc((size_t)SZ*SZ); RD=malloc(TMAX+4L*P+STRIDE+10);
  build(canon); best=TMAX+1;
  dfs(0,C0,C0,0,0,0);
  if(best>TMAX) printf("RESULT split=%d/%d@%d subtrees=%ld rule=%s K=%d NONE onset<=%ld nodes=%ld tests=%ld maxR=%d Dmin=%d\n",SWID,SW,SPLITD,SCTR,rule,K,TMAX,nodes,tests,maxR,Dmin);
  else printf("RESULT split=%d/%d@%d subtrees=%ld rule=%s K=%d best_onset=%ld minimisers=%ld nodes=%ld tests=%ld maxR=%d Dmin=%d flagged=%ld\n",SWID,SW,SPLITD,SCTR,rule,K,best,nsol,nodes,tests,maxR,Dmin,flagged);
  return 0; }
