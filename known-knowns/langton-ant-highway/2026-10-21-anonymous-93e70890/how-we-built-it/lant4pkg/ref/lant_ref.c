// lant2.c - faster version of diagnose/code/lant.c (same rule, same certificate C(s), same output format).
// Changes: position kept as a flat grid index; trajectory stored as uint32 index + uint8 dir;
// branchless turn; bounding box computed lazily from the trajectory only when C(s) is tested;
// out-of-bounds test replaced by a "safe until" step counter (exact same OOB semantics: margin 16).
// Adds rectangles: lant2 enumr W H START END CAP (bit b -> cell (b%W - (W-1)/2, b/W - (H-1)/2)).
//   lant2 enum K START END CAP == enumr K K ...
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define LN 13
#define N (1<<LN)
#define O (N/2)
static uint8_t g[(size_t)N*N];
static uint8_t par[(size_t)N*N];
static uint32_t *PA; static uint8_t *PD;
static const int DX[4]={0,1,0,-1}, DY[4]={1,0,-1,0};
static long DA[4];
static int bx0,bx1,by0,by1; static long scanned;
static inline size_t IDX(int x,int y){return (size_t)(y+O)*N+(size_t)(x+O);}
static inline int XOF(uint32_t a){return (int)(a&(N-1))-O;}
static inline int YOF(uint32_t a){return (int)(a>>LN)-O;}
static void setup(int W,int H,uint64_t mask){
  int ox=(W-1)/2, oy=(H-1)/2; bx0=-ox; by0=-oy; bx1=W-1-ox; by1=H-1-oy;
  for(int b=0;b<W*H;b++) if((mask>>b)&1ULL){int xi=b%W, yi=b/W; g[IDX(xi-ox,yi-oy)]=1;}
  if(bx0>0)bx0=0; if(by0>0)by0=0; if(bx1<0)bx1=0; if(by1<0)by1=0;
  scanned=0;
}
static inline void bbox_upto(long t){ // include positions PA[0..t]
  for(long i=scanned;i<=t;i++){int x=XOF(PA[i]),y=YOF(PA[i]); if(x<bx0)bx0=x; if(x>bx1)bx1=x; if(y<by0)by0=y; if(y>by1)by1=y;}
  if(t+1>scanned) scanned=t+1;
}
static void clear_grid(void){
  for(int y=by0-2;y<=by1+2;y++) memset(&g[IDX(bx0-2,y)],0,(size_t)(bx1-bx0+5));
}
static int checkC(long s){
  int vx=XOF(PA[s+104])-XOF(PA[s]), vy=YOF(PA[s+104])-YOF(PA[s]);
  if(abs(vx)!=2||abs(vy)!=2||PD[s+104]!=PD[s]) return 0;
  for(long i=s;i<s+104;i++) par[PA[i]]^=1;
  int ok=1;
  for(int k=0;ok;k++){
    int allx=1, ally=1;
    for(long i=s;i<s+104;i++){
      int cx=XOF(PA[i])+k*vx, cy=YOF(PA[i])+k*vy;
      if(!(vx>0? cx>bx1 : cx<bx0)) allx=0;
      if(!(vy>0? cy>by1 : cy<by0)) ally=0;
    }
    if(allx||ally) break;
    if(k>N/8){ok=-1;break;}
    for(long i=s;i<s+104;i++){
      int cx=XOF(PA[i])+k*vx, cy=YOF(PA[i])+k*vy;
      if(cx+vx<-O+2||cx+vx>O-3||cy+vy<-O+2||cy+vy>O-3){ok=-1;break;}
      size_t a=IDX(cx,cy), b=IDX(cx+vx,cy+vy);
      if(g[a]!=(g[b]^par[b])){ok=0;break;}
    }
  }
  for(long i=s;i<s+104;i++) par[PA[i]]=0;
  return ok;
}
static long safe_steps(uint32_t a){ // steps the ant can take with no chance of tripping the OOB test
  int x=XOF(a),y=YOF(a); long m=x-(-O+16); long q=(O-16)-x; if(q<m)m=q; q=y-(-O+16); if(q<m)m=q; q=(O-16)-y; if(q<m)m=q;
  return m-1;
}
static int run(int W,int H,uint64_t mask,long cap,long *tcap,int *vx,int *vy,int *dc,long *steps){
  setup(W,H,mask);
  uint32_t a=(uint32_t)IDX(0,0); int d=0; long run=0; long rv=0; long next_s=-1; int status=1;
  long safe_until=safe_steps(a);
  const long D1=2*N+2,D2=2*N-2,D3=-2*N+2,D4=-2*N-2;
  long t;
  for(t=0;t<=cap+104;t++){
    PA[t]=a;PD[t]=(uint8_t)d;
    if(t>=104){
      long ad=(long)a-(long)PA[t-104];
      // branchless run detector (same logic as lant.c): okd = same dir and displacement (+-2,+-2)
      int okd = (PD[t-104]==d) & ((ad==D1)|(ad==D2)|(ad==D3)|(ad==D4));
      int cont = okd & ((run==0)|(ad==rv));
      rv = run==0 ? ad : rv;
      run = cont ? run+1 : 0;
      if(__builtin_expect(run>=312,0) && (run%312)==0){
        bbox_upto(t);
        long rs=t-run+1; long s0=rs-104; if(next_s>s0) s0=next_s;
        for(long i=t-1;i>=s0;i--) g[PA[i]]^=1;
        long s; int found=0;
        for(s=s0;s<=t-104;s++){
          int r=checkC(s);
          if(r<0){status=2;break;}
          if(r==1){found=1;break;}
          g[PA[s]]^=1;
        }
        if(status==2){*steps=t;goto done;}
        if(found){*tcap=s;*vx=XOF(PA[s+104])-XOF(PA[s]);*vy=YOF(PA[s+104])-YOF(PA[s]);*dc=PD[s];*steps=t;status=0;
          for(long i=s;i<t;i++) g[PA[i]]^=1; goto done;}
        next_s=t-104+1;
        for(long i=t-103;i<t;i++) g[PA[i]]^=1;
      }
    }
    if(t>=cap+104) break;
    d=(d+1+((int)g[a]<<1))&3;
    g[a]^=1; { long m=(d&1)?1L:(long)N; a=(uint32_t)((long)a+((d&2)?-m:m)); }
    if(t>=safe_until){ int x=XOF(a),y=YOF(a);
      if(x<-O+16||x>O-16||y<-O+16||y>O-16){status=2;*steps=t;goto done;}
      safe_until=t+safe_steps(a); }
  }
  *steps=cap+104;
done:
  bbox_upto(t<=cap+104?t:cap+104);
  { int x=XOF(a),y=YOF(a); if(x<bx0)bx0=x; if(x>bx1)bx1=x; if(y<by0)by0=y; if(y>by1)by1=y; }
  clear_grid();
  return status;
}
int main(int argc,char**argv){
  for(int i=0;i<4;i++) DA[i]=(long)DY[i]*N+DX[i];
  if(argc<6){fprintf(stderr,"usage: lant2 enum K S E CAP | enumr W H S E CAP\n");return 1;}
  int W,H; uint64_t st,en; long cap=atol(argv[argc-1]);
  if(strcmp(argv[1],"enum")==0){W=H=atoi(argv[2]);st=strtoull(argv[3],0,10);en=strtoull(argv[4],0,10);}
  else if(strcmp(argv[1],"enumr")==0&&argc>=7){W=atoi(argv[2]);H=atoi(argv[3]);st=strtoull(argv[4],0,10);en=strtoull(argv[5],0,10);}
  else {fprintf(stderr,"usage\n");return 1;}
  PA=malloc(sizeof(uint32_t)*(cap+1000));PD=malloc(cap+1000);
  for(uint64_t m=st;m<en;m++){
    long tc=-1,steps=0;int vx=0,vy=0,dc=0;
    int r=run(W,H,m,cap,&tc,&vx,&vy,&dc,&steps);
    printf("%llu %ld %d %d %d %ld %s\n",(unsigned long long)m,tc,vx,vy,dc,steps,r==0?"CAP":(r==1?"UNCAPTURED_WITHIN_CAP":"OUT_OF_BOUNDS"));
  }
  return 0;
}
