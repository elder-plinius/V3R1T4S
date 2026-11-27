// ev3.h: evaluator for periodic point masses, level 1, floats, search only. Enumerates boxes by y-level pairs: rows share y.
// Raised limits against ev2.h: atoms MAXK, rects MAXR. A box must touch its bottom and top level inside the x range, else it is dominated by a smaller box.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef MAXK
#define MAXK 20000
#endif
#ifndef MAXR
#define MAXR 6000000
#endif
typedef struct { double Lx, Ly; int k; double x[MAXK], y[MAXK], m[MAXK]; } Cfg;
typedef struct { double a,b,c,d; } Rect;
static Rect *RR; static int NR;
static double wrap(double v,double L){v=fmod(v,L);if(v<0)v+=L;if(v>=L)v=0;return v;}
static int dcmp(const void*a,const void*b){double x=*(double*)a,y=*(double*)b;return x<y?-1:x>y;}
static double CL0=-1e300,CL1=1e300;
static inline void addr(double a,double b,double c,double d){if(c<CL0)c=CL0;if(d>CL1)d=CL1;if(NR<MAXR&&b>a&&d>c){RR[NR].a=a;RR[NR].b=b;RR[NR].c=c;RR[NR].d=d;NR++;}}
static void add_wrapped(const Cfg*g,double a,double b,double c,double d){
  double ax[2][2],cy[2][2];int nx,ny;
  if(b-a>=g->Lx){ax[0][0]=0;ax[0][1]=g->Lx;nx=1;}else{double s=wrap(a,g->Lx),e=s+(b-a);if(e<=g->Lx){ax[0][0]=s;ax[0][1]=e;nx=1;}else{ax[0][0]=s;ax[0][1]=g->Lx;ax[1][0]=0;ax[1][1]=e-g->Lx;nx=2;}}
  if(d-c>=g->Ly){cy[0][0]=0;cy[0][1]=g->Ly;ny=1;}else{double s=wrap(c,g->Ly),e=s+(d-c);if(e<=g->Ly){cy[0][0]=s;cy[0][1]=e;ny=1;}else{cy[0][0]=s;cy[0][1]=g->Ly;cy[1][0]=0;cy[1][1]=e-g->Ly;ny=2;}}
  for(int i=0;i<nx;i++)for(int j=0;j<ny;j++)addr(ax[i][0],ax[i][1],cy[j][0],cy[j][1]);
}
typedef struct {double x;int t,r;} Ev;
static int evcmp(const void*p,const void*q){double a=((Ev*)p)->x,b=((Ev*)q)->x;return a<b?-1:a>b;}
static double *Ys;static int *cnt;static double *len;
static void upd(int o,int l,int r,int a,int b,int v){if(a>=r||b<=l)return;if(a<=l&&r<=b){cnt[o]+=v;}else{int m=(l+r)/2;upd(2*o,l,m,a,b,v);upd(2*o+1,m,r,a,b,v);}
  if(cnt[o]>0)len[o]=Ys[r]-Ys[l];else if(r-l==1)len[o]=0;else len[o]=len[2*o]+len[2*o+1];}
static int lb(double*A,int n,double v){int a=0,b=n;while(a<b){int c=(a+b)/2;if(A[c]<v)a=c+1;else b=c;}return a;}
static double union_area(void){
  if(!NR)return 0;static Ev*E;static double*ys;if(!E){E=malloc(sizeof(Ev)*2*MAXR);ys=malloc(8*2*MAXR);cnt=malloc(4*8*(size_t)MAXR);len=malloc(8*8*(size_t)MAXR);}
  int n=0,m=0;for(int i=0;i<NR;i++){E[n].x=RR[i].a;E[n].t=1;E[n].r=i;n++;E[n].x=RR[i].b;E[n].t=-1;E[n].r=i;n++;ys[m++]=RR[i].c;ys[m++]=RR[i].d;}
  qsort(E,n,sizeof(Ev),evcmp);qsort(ys,m,8,dcmp);int u=0;for(int i=0;i<m;i++)if(!u||ys[i]>ys[u-1])ys[u++]=ys[i];Ys=ys;
  memset(cnt,0,4*4*(size_t)(u+2));memset(len,0,8*4*(size_t)(u+2));double A=0;
  for(int i=0;i<n;i++){if(i)A+=(E[i].x-E[i-1].x)*len[1];Rect*R=&RR[E[i].r];upd(1,0,u-1,lb(ys,u,R->c),lb(ys,u,R->d),E[i].t);}
  return A;
}
static double total_mass(const Cfg*c){double s=0;for(int i=0;i<c->k;i++)s+=c->m[i];return s;}
typedef struct {double x,y,m;} Pt;
static int ptcmp(const void*a,const void*b){const Pt*p=a,*q=b;if(p->x<q->x)return -1;if(p->x>q->x)return 1;return 0;}
// optional per-box callback, for analysis
static void (*BOXCB)(double a,double b,double c,double d,double x1,double x2,double y1,double y2,double M);
static long NBOX;
static double evalcfg(const Cfg*g,double E){
  if(!RR)RR=malloc(sizeof(Rect)*MAXR);
  static Pt *P;static double *lev;static int *lo,*hi; static Pt*B; static double *pre;static int *tb;
  if(!P){int z=2000000;P=malloc(sizeof(Pt)*z);lev=malloc(8*z);lo=malloc(4*z);hi=malloc(4*z);B=malloc(sizeof(Pt)*z);pre=malloc(8*z);tb=malloc(4*z);}
  int np=0;int ax=(int)ceil(E/g->Lx)+1,ay=(int)ceil(E/g->Ly)+1;
  for(int i=0;i<g->k;i++){double x0=wrap(g->x[i],g->Lx),y0=wrap(g->y[i],g->Ly);
    for(int u=0;u<=ax;u++)for(int v=0;v<=ay;v++){P[np].x=x0+u*g->Lx;P[np].y=y0+v*g->Ly;P[np].m=g->m[i];np++;}}
  // sort all by x once; levels by y
  qsort(P,np,sizeof(Pt),ptcmp);
  for(int i=0;i<np;i++)lev[i]=P[i].y;qsort(lev,np,8,dcmp);int nl=0;for(int i=0;i<np;i++)if(!nl||lev[i]>lev[nl-1]+1e-13)lev[nl++]=lev[i];
  int nb=0;while(nb<nl&&lev[nb]<g->Ly-1e-13)nb++;
  NR=0;NBOX=0;
  for(int j1=0;j1<nb;j1++){
    for(int j2=j1;j2<nl&&lev[j2]-lev[j1]<=E;j2++){
      double y1=lev[j1],y2=lev[j2],dy=y2-y1;
      // gather atoms in the strip, in x order
      int n=0;for(int i=0;i<np;i++){double y=P[i].y;if(y<y1-1e-13||y>y2+1e-13)continue;B[n]=P[i];tb[n]=(fabs(y-y1)<=1e-13?1:0)|(fabs(y-y2)<=1e-13?2:0);n++;}
      if(!n)continue;
      double s=0;pre[0]=0;for(int i=0;i<n;i++){s+=B[i].m;pre[i+1]=s;}
      for(int i=0;i<n;i++){double x1=B[i].x;if(x1>=g->Lx)break;if(i&&B[i-1].x==x1)continue;
        int mask=0;
        for(int q=i;q<n;q++){double dx=B[q].x-x1;if(dx>E)break;mask|=tb[q];
          if(q+1<n&&B[q+1].x==B[q].x)continue;
          if(mask!=3)continue;
          double M=pre[q+1]-pre[i];double e=dx>dy?dx:dy;if(e*e>M)continue;double rho=sqrt(M)/2;
          double a=B[q].x-rho,b=x1+rho,c=y2-rho,d=y1+rho;NBOX++;
          add_wrapped(g,a,b,c,d);if(BOXCB)BOXCB(a,b,c,d,x1,B[q].x,y1,y2,M);
        }}
    }}
  return union_area()/total_mass(g);
}
