/* lant_core.h - shared single-ant core for the CPU solver (lant4) and the CUDA kernel (lant_cuda.cu).
 * Same rule, same highway detector, same capture certificate C(s), same T_cap as ref/lant_ref.c (= lant2.c),
 * but: (a) the trajectory is a 1024-entry ring buffer instead of a full array, (b) the grid is a WIN x WIN bit-plane
 * window (default 1024x1024 = 128 KB) instead of an 8192x8192 byte grid, (c) the bounding box is a running min/max.
 * If the ant (or a certificate translate) would touch the window margin the run stops with status 3 (WINDOW_OVERFLOW);
 * the caller must re-run that mask with the reference program (scripts do this automatically).
 * Compiles as plain C99 and as CUDA (LF = __host__ __device__). */
#ifndef LANT_CORE_H
#define LANT_CORE_H
#include <stdint.h>
#ifdef __CUDACC__
#define LF __host__ __device__
#else
#define LF
#endif
#ifndef WINLG
#define WINLG 10
#endif
#define WIN (1<<WINLG)
#define H2 (WIN/2)
#define RING 1024
#define RM (RING-1)
#ifdef BYTEGRID   /* one byte per cell: faster on CPU (1 MB per plane at WIN=1024); default is the 1-bit plane (128 KB, used on GPU) */
#define PLANE_BYTES ((size_t)WIN*WIN)
#else
#define PLANE_BYTES ((size_t)WIN*WIN/8)
#endif
/* status: 0 captured ("CAP"), 1 not captured within cap, 3 window overflow (use reference) */
LF static inline unsigned cidx(int x,int y){return (unsigned)((y+H2)*WIN+(x+H2));}
#ifdef BYTEGRID
LF static inline int gget(const uint8_t*G,int x,int y){return G[cidx(x,y)];}
LF static inline void gflip(uint8_t*G,int x,int y){G[cidx(x,y)]^=1;}
#else
LF static inline int gget(const uint8_t*G,int x,int y){unsigned i=cidx(x,y);return (G[i>>3]>>(i&7))&1;}
LF static inline void gflip(uint8_t*G,int x,int y){unsigned i=cidx(x,y);G[i>>3]^=(uint8_t)(1u<<(i&7));}
#endif
#ifdef BYTEGRID
LF static inline int gget_a(const uint8_t*G,unsigned a){return G[a];}
LF static inline void gflip_a(uint8_t*G,unsigned a){G[a]^=1;}
#else
LF static inline int gget_a(const uint8_t*G,unsigned a){return (G[a>>3]>>(a&7))&1;}
LF static inline void gflip_a(uint8_t*G,unsigned a){G[a>>3]^=(uint8_t)(1u<<(a&7));}
#endif
LF static inline int iabs_(int v){return v<0?-v:v;}

typedef struct { uint32_t ra[RING]; uint8_t rd[RING]; } Ring;   /* flat cell index (y+H2)*WIN+(x+H2), direction */
#define RXo(R,i) ((int)((R)->ra[(i)&RM]&(WIN-1))-H2)
#define RYo(R,i) ((int)((R)->ra[(i)&RM]>>WINLG)-H2)

LF static int checkC(long s,const Ring*R,uint8_t*G,uint8_t*P,int bx0,int bx1,int by0,int by1){
  int vx=RXo(R,s+104)-RXo(R,s), vy=RYo(R,s+104)-RYo(R,s);
  if(iabs_(vx)!=2||iabs_(vy)!=2||R->rd[(s+104)&RM]!=R->rd[s&RM]) return 0;
  for(long i=s;i<s+104;i++) gflip(P,RXo(R,i),RYo(R,i));
  int ok=1;
  for(int k=0;ok==1;k++){
    int allx=1,ally=1;
    for(long i=s;i<s+104;i++){
      int cx=RXo(R,i)+k*vx, cy=RYo(R,i)+k*vy;
      if(!(vx>0? cx>bx1 : cx<bx0)) allx=0;
      if(!(vy>0? cy>by1 : cy<by0)) ally=0;
    }
    if(allx||ally) break;
    if(k>1024){ok=-1;break;}
    for(long i=s;i<s+104;i++){
      int cx=RXo(R,i)+k*vx, cy=RYo(R,i)+k*vy;
      if(cx+vx<-H2+2||cx+vx>H2-3||cy+vy<-H2+2||cy+vy>H2-3||cx<-H2+2||cx>H2-3||cy<-H2+2||cy>H2-3){ok=-1;break;}
      int ga=gget(G,cx,cy), gb=gget(G,cx+vx,cy+vy), pb=gget(P,cx+vx,cy+vy);
      if(ga!=(gb^pb)){ok=0;break;}
    }
    if(ok==-1) break;
  }
  for(long i=s;i<s+104;i++) gflip(P,RXo(R,i),RYo(R,i));   /* parity plane back to all-zero */
  return ok;
}
/* G,P: zeroed bit planes of PLANE_BYTES each; they are returned zeroed. */
LF static int lant_run(int W,int H,uint64_t mask,long cap,uint8_t*G,uint8_t*P,Ring*R,
                       long*tcap,int*vxo,int*vyo,int*dco,long*steps){
  const int DXs[4]={0,1,0,-1}, DYs[4]={1,0,-1,0};
  int ox=(W-1)/2, oy=(H-1)/2, bx0=-ox,by0=-oy,bx1=W-1-ox,by1=H-1-oy;
  if(bx0>0)bx0=0; if(by0>0)by0=0; if(bx1<0)bx1=0; if(by1<0)by1=0;
  for(int b=0;b<W*H;b++) if((mask>>b)&1ULL) gflip(G,b%W-ox,b/W-oy);
  int x=0,y=0,d=0,status=1; long run=0,rv=0,next_s=-1,t; uint32_t a=cidx(0,0); long safe_until=H2-16-1;
  const long D1=2L*WIN+2,D2=2L*WIN-2,D3=-2L*WIN+2,D4=-2L*WIN-2;
  int mnx=bx0,mxx=bx1,mny=by0,mxy=by1; long scanned=0;   /* bbox of init box + positions 0..scanned-1, refreshed lazily from the ring (<=256 new entries) */
#define BBOX_UPTO(T_) do{ for(long i_=scanned;i_<=(T_);i_++){int xx_=RXo(R,i_),yy_=RYo(R,i_); if(xx_<mnx)mnx=xx_; if(xx_>mxx)mxx=xx_; if(yy_<mny)mny=yy_; if(yy_>mxy)mxy=yy_;} if((T_)+1>scanned) scanned=(T_)+1; }while(0)
  for(t=0;t<=cap+104;t++){
    R->ra[t&RM]=a; R->rd[t&RM]=(uint8_t)d;
    if((t&255)==255) BBOX_UPTO(t);
    if(t>=104){
      long ad=(long)a-(long)R->ra[(t-104)&RM];
      int okd=(R->rd[(t-104)&RM]==d)&((ad==D1)|(ad==D2)|(ad==D3)|(ad==D4));
      int cont=okd&((run==0)|(ad==rv));
      if(run==0) rv=ad;
      run=cont?run+1:0;
      if(run>=312 && (run%312)==0){
        BBOX_UPTO(t);
        long rs=t-run+1, s0=rs-104; if(next_s>s0) s0=next_s;
        for(long i=t-1;i>=s0;i--) gflip(G,RXo(R,i),RYo(R,i));
        long s; int found=0, st2=0;
        for(s=s0;s<=t-104;s++){
          int r=checkC(s,R,G,P,mnx,mxx,mny,mxy);
          if(r<0){st2=1;break;}
          if(r==1){found=1;break;}
          gflip(G,RXo(R,s),RYo(R,s));
        }
        if(st2){status=3;*steps=t;goto done;}
        if(found){*tcap=s;*vxo=RXo(R,s+104)-RXo(R,s);*vyo=RYo(R,s+104)-RYo(R,s);*dco=R->rd[s&RM];*steps=t;status=0;
          for(long i=s;i<t;i++) gflip(G,RXo(R,i),RYo(R,i)); goto done;}
        next_s=t-104+1;
        for(long i=t-103;i<t;i++) gflip(G,RXo(R,i),RYo(R,i));
      }
    }
    if(t>=cap+104) break;
    d=(d+1+(gget_a(G,a)<<1))&3;
    gflip_a(G,a); { long m=(d&1)?1L:(long)WIN; a=(uint32_t)((long)a+((d&2)?-m:m)); }
    if(t>=safe_until){ x=(int)(a&(WIN-1))-H2; y=(int)(a>>WINLG)-H2; if(x<-H2+16||x>H2-16||y<-H2+16||y>H2-16){status=3;*steps=t;goto done;}
      { int m=x+H2-16; int q=H2-16-x; if(q<m)m=q; q=y+H2-16; if(q<m)m=q; q=H2-16-y; if(q<m)m=q; safe_until=t+m-1; } }
  }
  *steps=cap+104;
done:
  BBOX_UPTO(t<=cap+104?t:cap+104);
  x=(int)(a&(WIN-1))-H2; y=(int)(a>>WINLG)-H2;
  if(x<mnx)mnx=x; if(x>mxx)mxx=x; if(y<mny)mny=y; if(y>mxy)mxy=y;
  for(int yy=mny-2;yy<=mxy+2;yy++){
    unsigned i0=cidx(mnx-2,yy), i1=cidx(mxx+2,yy);
#ifdef BYTEGRID
    for(unsigned i=i0;i<=i1;i++){G[i]=0;P[i]=0;}
#else
    for(unsigned i=i0>>3;i<=(i1>>3);i++){G[i]=0;P[i]=0;}
#endif
  }
  return status;
}

/* ---------- interleaved multi-ant engine (CPU only): K independent ants advanced in lockstep for instruction-level parallelism.
 * Same logic as lant_run, split into a resumable state machine. */
#ifndef __CUDACC__
#define KK 4
typedef struct { uint8_t*G,*P; Ring*R; int W,H; uint64_t mask; long cap; uint32_t a; int d; long t,run,rv,next_s,safe_until,scanned;
  int mnx,mxx,mny,mxy; int status; long tcap,steps; int vx,vy,dc; long idx; } Ant;   /* status -1 = running */
static void ant_start(Ant*A,int W,int H,uint64_t mask,long cap,long idx){
  int ox=(W-1)/2, oy=(H-1)/2, bx0=-ox,by0=-oy,bx1=W-1-ox,by1=H-1-oy;
  if(bx0>0)bx0=0; if(by0>0)by0=0; if(bx1<0)bx1=0; if(by1<0)by1=0;
  for(int b=0;b<W*H;b++) if((mask>>b)&1ULL) gflip(A->G,b%W-ox,b/W-oy);
  A->W=W;A->H=H;A->mask=mask;A->cap=cap;A->a=cidx(0,0);A->d=0;A->t=0;A->run=0;A->rv=0;A->next_s=-1;A->safe_until=H2-16-1;A->scanned=0;
  A->mnx=bx0;A->mxx=bx1;A->mny=by0;A->mxy=by1;A->status=-1;A->tcap=-1;A->vx=A->vy=A->dc=0;A->steps=0;A->idx=idx;
}
static void ant_bbox(Ant*A,long T){ Ring*R=A->R;
  long i=A->scanned;
  while(i<=T){ long j=i|RM; if(j>T) j=T; /* segment [i,j] without ring wrap */
    const uint32_t*p=R->ra+(i&RM); long n=j-i+1;
    uint32_t xl=WIN,xh=0,yl=WIN,yh=0;
    for(long q=0;q<n;q++){ uint32_t v=p[q]; uint32_t xx=v&(WIN-1), yy=v>>WINLG; xl=xx<xl?xx:xl; xh=xx>xh?xx:xh; yl=yy<yl?yy:yl; yh=yy>yh?yy:yh; }
    if((int)xl-H2<A->mnx)A->mnx=(int)xl-H2; if((int)xh-H2>A->mxx)A->mxx=(int)xh-H2;
    if((int)yl-H2<A->mny)A->mny=(int)yl-H2; if((int)yh-H2>A->mxy)A->mxy=(int)yh-H2;
    i=j+1; }
  if(T+1>A->scanned)A->scanned=T+1; }
static void ant_finish(Ant*A,int status,long steps,long t){
  Ring*R=A->R; A->status=status; A->steps=steps; ant_bbox(A,t<=A->cap+104?t:A->cap+104);
  int x=(int)(A->a&(WIN-1))-H2, y=(int)(A->a>>WINLG)-H2; if(x<A->mnx)A->mnx=x; if(x>A->mxx)A->mxx=x; if(y<A->mny)A->mny=y; if(y>A->mxy)A->mxy=y;
  for(int yy=A->mny-2;yy<=A->mxy+2;yy++){ unsigned i0=cidx(A->mnx-2,yy), i1=cidx(A->mxx+2,yy);
#ifdef BYTEGRID
    for(unsigned i=i0;i<=i1;i++){A->G[i]=0;A->P[i]=0;}
#else
    for(unsigned i=i0>>3;i<=(i1>>3);i++){A->G[i]=0;A->P[i]=0;}
#endif
  } (void)R;
}
static void ant_event(Ant*A){            /* called at step t=A->t with A->run multiple of 312; may finish the ant */
  Ring*R=A->R; uint8_t*G=A->G,*P=A->P; long t=A->t, run=A->run;
  ant_bbox(A,t);
  long rs=t-run+1, s0=rs-104; if(A->next_s>s0) s0=A->next_s;
  for(long i=t-1;i>=s0;i--) gflip(G,RXo(R,i),RYo(R,i));
  long s; int found=0, st2=0;
  for(s=s0;s<=t-104;s++){
    int r=checkC(s,R,G,P,A->mnx,A->mxx,A->mny,A->mxy);
    if(r<0){st2=1;break;}
    if(r==1){found=1;break;}
    gflip(G,RXo(R,s),RYo(R,s));
  }
  if(st2){ ant_finish(A,3,t,t); return; }
  if(found){A->tcap=s;A->vx=RXo(R,s+104)-RXo(R,s);A->vy=RYo(R,s+104)-RYo(R,s);A->dc=R->rd[s&RM];
    for(long i=s;i<t;i++) gflip(G,RXo(R,i),RYo(R,i)); ant_finish(A,0,t,t); return; }
  A->next_s=t-104+1;
  for(long i=t-103;i<t;i++) gflip(G,RXo(R,i),RYo(R,i));
}
/* advance all running ants of A[0..KK-1] by up to n steps; returns early as soon as any ant finishes */
static void ant_burst(Ant**A,long n){
  uint32_t a[KK]; int d[KK]; long t[KK],run[KK],rv[KK],su[KK],lim[KK]; uint8_t*G[KK]; uint32_t*ra[KK]; uint8_t*rd[KK];
  const long D1=2L*WIN+2,D2=2L*WIN-2,D3=-2L*WIN+2,D4=-2L*WIN-2;
  for(int k=0;k<KK;k++){ a[k]=A[k]->a;d[k]=A[k]->d;t[k]=A[k]->t;run[k]=A[k]->run;rv[k]=A[k]->rv;su[k]=A[k]->safe_until;lim[k]=A[k]->cap+104;
    G[k]=A[k]->G;ra[k]=A[k]->R->ra;rd[k]=A[k]->R->rd; }
  int fin=0;
  for(long s=0;s<n && !fin;s++){
    for(int k=0;k<KK;k++){
      if(A[k]->status!=-1) continue;
      long tk=t[k]; ra[k][tk&RM]=a[k]; rd[k][tk&RM]=(uint8_t)d[k];
      if((tk&255)==255) ant_bbox(A[k],tk);
      if(tk>=104){
        long ad=(long)a[k]-(long)ra[k][(tk-104)&RM];
        int okd=(rd[k][(tk-104)&RM]==d[k])&((ad==D1)|(ad==D2)|(ad==D3)|(ad==D4));
        int cont=okd&((run[k]==0)|(ad==rv[k]));
        if(run[k]==0) rv[k]=ad;
        run[k]=cont?run[k]+1:0;
        if(run[k]>=312 && (run[k]%312)==0){
          A[k]->t=tk;A[k]->run=run[k];A[k]->a=a[k]; ant_event(A[k]);
          if(A[k]->status!=-1){fin=1;continue;}
        }
      }
      if(tk>=lim[k]){ A[k]->a=a[k]; ant_finish(A[k],1,lim[k],tk); fin=1; continue; }
      d[k]=(d[k]+1+(gget_a(G[k],a[k])<<1))&3;
      gflip_a(G[k],a[k]); { long m=(d[k]&1)?1L:(long)WIN; a[k]=(uint32_t)((long)a[k]+((d[k]&2)?-m:m)); }
      if(tk>=su[k]){ int x=(int)(a[k]&(WIN-1))-H2, y=(int)(a[k]>>WINLG)-H2;
        if(x<-H2+16||x>H2-16||y<-H2+16||y>H2-16){ A[k]->a=a[k]; ant_finish(A[k],3,tk,tk); fin=1; continue; }
        { int m=x+H2-16; int q=H2-16-x; if(q<m)m=q; q=y+H2-16; if(q<m)m=q; q=H2-16-y; if(q<m)m=q; su[k]=tk+m-1; } }
      t[k]=tk+1;
    }
  }
  for(int k=0;k<KK;k++) if(A[k]->status==-1){ A[k]->a=a[k];A[k]->d=d[k];A[k]->t=t[k];A[k]->run=run[k];A[k]->rv=rv[k];A[k]->safe_until=su[k]; }
}
#endif
static const char* lant_status_name(int r){return r==0?"CAP":(r==1?"UNCAPTURED_WITHIN_CAP":(r==2?"OUT_OF_BOUNDS":"WINDOW_OVERFLOW"));}
#endif
