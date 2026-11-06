/* lcone.c - second, independent completeness checker for Langton highway seeds.
   Written from scratch; shares no code with fsearch.c or attempts/brute.
   Method: forward light-cone DFS over the colours of cells the ant reads for the first time
   (white free, black costs 1, budget K), to depth T. At depth T, exact "turn-word" highway test:
   for each phase p of the blank highway's 104-periodic turn word w, force the ant's future turns to be
   w[p], w[p+1], ...; every read of an already-known cell must have the required colour, every read of a
   never-visited cell assigns the required colour (black costs 1). Success once (a) the blank highway from
   phase p can no longer read any cell of its own pre-history and (b) the ant can no longer reach any cell
   visited in [0,T) -- both via an exact back-reach bound c_back of the periodic path.
   Convention: time t = number of updates done; onset = least t such that the turn sequence from update t on
   is the highway word (blank grid: 9977).
   Usage: lcone K T W wid   -> tests at depth T-1 (violations) and T (minimisers). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define G 2048
#define C0 1024
#define NB 40000
static unsigned char col[G*G], known[G*G];
static int dxs[4]={0,1,0,-1}, dys[4]={-1,0,1,0}; /* N E S W, y down */
static unsigned char w[104]; static int S0;
static int bh[104], Hp[104]; static long Dbx,Dby; static long cback;
static int K,T,W,wid; static long leaves=0, splitctr=0, viol=0, mins=0;
static int px[12000],py[12000]; /* ant positions at times 0..t */
typedef struct{int c; unsigned char col,kn;} U; static U *ul; static long un=0;
static int blk[64]; static int nblk=0; /* DFS black cells (idx) */
static void setc(int c,int cv){ul[un].c=c;ul[un].col=col[c];ul[un].kn=known[c];un++;col[c]=cv;known[c]=1;}
static void undo(long m){while(un>m){un--;col[ul[un].c]=ul[un].col;known[ul[un].c]=ul[un].kn;}}
static void blank_pre(void){
  /* simulate blank grid, record turn word and back-reach bounds */
  static unsigned char g[G*G]; int x=C0,y=C0,h=0; int n=S0+104+30000;
  int *X=malloc(sizeof(int)*(n+1)),*Y=malloc(sizeof(int)*(n+1)),*Hh=malloc(sizeof(int)*(n+1)); unsigned char *Rd=malloc(n);
  for(int u=0;u<n;u++){X[u]=x;Y[u]=y;Hh[u]=h;int c=y*G+x;int b=g[c];Rd[u]=b;h=(h+(b?3:1))&3;g[c]^=1;x+=dxs[h];y+=dys[h];}
  X[n]=x;Y[n]=y;Hh[n]=h;
  for(int u=S0;u<n-104;u++) if(Rd[u]!=Rd[u+104]){fprintf(stderr,"blank not periodic at %d\n",u);exit(2);}
  for(int p=0;p<104;p++){w[p]=Rd[S0+p];bh[p]=Hh[S0+p];}
  Dbx=X[S0+104]-X[S0];Dby=Y[S0+104]-Y[S0];
  if(Hh[S0+104]!=Hh[S0]){fprintf(stderr,"period rotates\n");exit(2);}
  for(int u=S0;u<S0+104;u++){ if(X[u+104]-X[u]!=Dbx||Y[u+104]-Y[u]!=Dby){fprintf(stderr,"bad D\n");exit(2);} }
  /* c_back = max_{u0 in period} pi(u0) - min_{u in [u0,u0+104]} pi(u) (exact: pi grows by |D|^2 per period) */
  cback=0;
  for(int u0=S0;u0<S0+104;u0++){long a=X[u0]*Dbx+Y[u0]*Dby,mn=a;for(int u=u0;u<=u0+104;u++){long q=X[u]*Dbx+Y[u]*Dby;if(q<mn)mn=q;} if(a-mn>cback)cback=a-mn;}
  /* positions are read cells: cell read at update u is (X[u],Y[u]) */
  long mh=-(1L<<60); int p=0;
  for(int u=0;u<S0+104;u++){ if(u>=S0){ p=u-S0; /* history = cells read at updates < S0+p */
      long need=mh; int v=u; while(1){ long q=X[v]*Dbx+Y[v]*Dby; if(q-cback>need) break; v++; if(v>=n){fprintf(stderr,"Hp overflow\n");exit(2);} }
      Hp[p]=v-u; }
    long q=X[u]*Dbx+Y[u]*Dby; if(q>mh)mh=q; }
  fprintf(stderr,"S0=%d D=(%ld,%ld) cback=%ld Hp[0]=%d Hp[103]=%d\n",S0,Dbx,Dby,cback,Hp[0],Hp[103]);
}
static int asg[NB]; 
static void test(int t,int x,int y,int h,int used){
  leaves++;
  for(int p=0;p<104;p++){
    int r=(h-bh[p])&3; /* rotate blank frame by r quarter-turns clockwise */
    long Dx=Dbx,Dy=Dby; for(int i=0;i<r;i++){long tx=-Dy,ty=Dx;Dx=tx;Dy=ty;} /* (x,y)->(-y,x) is clockwise with y down */
    long mk=-(1L<<60); for(int i=0;i<t;i++){long q=(long)(px[i]-C0)*Dx+(long)(py[i]-C0)*Dy; if(q>mk)mk=q;}
    long m=un; int cost=used, na=0, st=0; int ax=x,ay=y,ah=h; /* st: 0 running, 1 success, 2 fail */
    for(int u=0;u<NB && st==0;u++){
      if(u>=Hp[p]){ long q=(long)(ax-C0)*Dx+(long)(ay-C0)*Dy; if(q-cback>mk){st=1;break;} }
      int c=ay*G+ax; int rq=w[(p+u)%104];
      if(known[c]){ if(col[c]!=rq){st=2;break;} }
      else { if(rq){ if(++cost>K){st=2;break;} asg[na++]=c; } }
      setc(c,rq^1); /* read rq, flip */
      ah=(ah+(rq?3:1))&3; ax+=dxs[ah]; ay+=dys[ah];
      if(ax<2||ay<2||ax>G-3||ay>G-3){fprintf(stderr,"FLAG grid edge\n");exit(3);}
    }
    if(st==0){fprintf(stderr,"FLAG forced sim did not resolve in %d steps\n",NB);exit(3);}
    int ok=(st==1);
    if(ok){
      if(t==T-1) viol++; else mins++;
      printf("%s t=%d p=%d k=%d cells:", t==T-1?"VIOLATION":"MIN", t,p,cost);
      for(int i=0;i<nblk;i++) printf(" (%d,%d)",blk[i]%G-C0,blk[i]/G-C0);
      for(int i=0;i<na;i++) printf(" (%d,%d)*",asg[i]%G-C0,asg[i]/G-C0);
      printf("\n");
    }
    undo(m);
  }
}
static void dfs(int t,int x,int y,int h,int used){
  px[t]=x;py[t]=y;
  if(t==8){ if((splitctr++)%W!=wid) return; }
  if(t==T-1||t==T) test(t,x,y,h,used);
  if(t==T) return;
  int c=y*G+x; int fresh=!known[c];
  for(int b=0;b<(fresh?2:1);b++){
    if(b==1 && used>=K) break;
    long m=un;
    int cv = fresh ? b : col[c];          /* colour read now */
    int nh=(h+(cv?3:1))&3;
    setc(c,cv^1);                          /* flip after reading */
    if(fresh && b) blk[nblk++]=c;
    dfs(t+1,x+dxs[nh],y+dys[nh],nh,used+(fresh&&b));
    if(fresh && b) nblk--;
    undo(m);
  }
}
int main(int argc,char**argv){
  K=atoi(argv[1]);T=atoi(argv[2]); if(T>11000||K>60){fprintf(stderr,"bounds\n");return 2;}W=atoi(argv[3]);wid=atoi(argv[4]); S0=9977;
  ul=malloc(sizeof(U)*4000000);
  blank_pre();
  memset(col,0,sizeof col);memset(known,0,sizeof known);
  if(T==0){ px[0]=C0;py[0]=C0; if(wid==0) test(0,C0,C0,0,0); }
  else dfs(0,C0,C0,0,0);
  fprintf(stderr,"DONE K=%d T=%d wid=%d leaves=%ld viol=%ld mins=%ld\n",K,T,wid,leaves,viol,mins);
  printf("DONE K=%d T=%d wid=%d leaves=%ld viol=%ld mins=%ld\n",K,T,wid,leaves,viol,mins);
  return 0;
}
