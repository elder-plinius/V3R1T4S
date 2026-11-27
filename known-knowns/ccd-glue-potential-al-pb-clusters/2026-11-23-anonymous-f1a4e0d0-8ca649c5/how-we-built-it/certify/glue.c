/* Ercolessi-Adams glue potential (Al), exact netlib seval semantics. E = sum_{i<j} phi + sum_i U(rho_i). */
#include <math.h>
#include <stdlib.h>
typedef struct { int n; const double *x,*y,*b,*c,*d; } spl;
static void sev(const spl *s, double u, double *f, double *df) {
  int i=0, j=s->n, k; /* 0-based binary search: largest i with x[i] <= u, clamped to [0,n-1] */
  if (u < s->x[0]) i=0; else { i=0; j=s->n; while (j>i+1) { k=(i+j)/2; if (u < s->x[k]) j=k; else i=k; } }
  double dx=u-s->x[i];
  *f = s->y[i]+dx*(s->b[i]+dx*(s->c[i]+dx*s->d[i]));
  *df = s->b[i]+dx*(2*s->c[i]+3*dx*s->d[i]);
}
/* tab layout: for each of v2, rh, uu: n, then x[n],y[n],b[n],c[n],d[n]; then argmax_v2, argmax_rh, argmin_uu */
static spl S[3]; static double AMV, AMR, AMU; static int init=0;
void glue_init(const double *t) {
  int o=0; for (int s=0;s<3;s++){ int n=(int)t[o++]; S[s].n=n; S[s].x=t+o; o+=n; S[s].y=t+o; o+=n; S[s].b=t+o; o+=n; S[s].c=t+o; o+=n; S[s].d=t+o; o+=n; }
  AMV=t[o]; AMR=t[o+1]; AMU=t[o+2]; init=1;
}
static void v2(double r,double*f,double*df){ if(r>=AMV){*f=0;*df=0;} else sev(&S[0],r,f,df);} 
static void rh(double r,double*f,double*df){ if(r>=AMR){*f=0;*df=0;} else sev(&S[1],r,f,df);} 
static void uu(double z,double*f,double*df){ if(z<=AMU){*f=0;*df=0;} else sev(&S[2],z,f,df);} 
double glue_eg(int n, const double *x, double *g) {
  double *rho=calloc(n,sizeof(double)), *up=calloc(n,sizeof(double)); double E=0;
  for (int i=0;i<3*n;i++) g[i]=0;
  for (int i=0;i<n;i++) for (int j=i+1;j<n;j++) {
    double dx=x[3*i]-x[3*j], dy=x[3*i+1]-x[3*j+1], dz=x[3*i+2]-x[3*j+2], r=sqrt(dx*dx+dy*dy+dz*dz), f, df;
    if (r>=AMV) continue;
    v2(r,&f,&df); E+=f; rh(r,&f,&df); rho[i]+=f; rho[j]+=f;
  }
  for (int i=0;i<n;i++){ double f,df; uu(rho[i],&f,&df); E+=f; up[i]=df; }
  for (int i=0;i<n;i++) for (int j=i+1;j<n;j++) {
    double dx=x[3*i]-x[3*j], dy=x[3*i+1]-x[3*j+1], dz=x[3*i+2]-x[3*j+2], r=sqrt(dx*dx+dy*dy+dz*dz), f, dv, dr;
    if (r>=AMV) continue;
    v2(r,&f,&dv); rh(r,&f,&dr); double W=dv+(up[i]+up[j])*dr;
    if (W!=0){ double s=W/r; g[3*i]+=s*dx; g[3*i+1]+=s*dy; g[3*i+2]+=s*dz; g[3*j]-=s*dx; g[3*j+1]-=s*dy; g[3*j+2]-=s*dz; }
  }
  free(rho); free(up); return E;
}
