// check.c: independent rigorous checker. Reads only lib/ and cover files.
// usage: check libdir prefix T eta
// All arithmetic in rounding-upward mode with midpoint-radius balls (Rump). A ball (m,r) encloses [m-r,m+r].
// Proves for each leaf: kind 0: forall (A,rho,phi) in leaf, forall theta: max_j [...] - Re(c e^{-i theta}) > sqrt3/4+T, |c|<0.22
//                       kind 1: inequality (20) is violated on the whole leaf at (tau,s)
//                       kind 2: rho_lo > C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <fenv.h>
#include <stdint.h>
#include <time.h>
#pragma STDC FENV_ACCESS ON
#define LT 18
#define NT (1<<LT)
#define MJ 200
#define U (0x1p-52)
#define ETA_MIN (1e-300)
typedef struct {double m,r;} B;
static inline B bc(double x){B z={x,0.0};return z;}
static inline double up_abs(B x){return fabs(x.m)+x.r;}
static inline B badd(B x,B y){B z; z.m=x.m+y.m; z.r=U*fabs(z.m)+x.r+y.r; return z;}
static inline B bneg(B x){B z={-x.m,x.r};return z;}
static inline B bsub(B x,B y){return badd(x,bneg(y));}
static inline B bmul(B x,B y){B z; z.m=x.m*y.m; z.r=U*fabs(z.m)+ETA_MIN+fabs(x.m)*y.r+fabs(y.m)*x.r+x.r*y.r; return z;}
static inline B bmuld(B x,double y){B z; z.m=x.m*y; z.r=U*fabs(z.m)+ETA_MIN+fabs(y)*x.r; return z;}
static double *TAB; static double TEPS; static int J; static double Es[MJ],Ps[MJ],Qs[MJ],aPs[MJ],aQs[MJ];
static int NS; static double SV[64],RV[64];
static double CUP,SQ34,PI2UP,PI2DN;
static void die(const char*m){printf("FAIL: %s\n",m);exit(1);}
static void readlib(const char*d){
  char fn[1200],ln[600]; FILE*f;
  snprintf(fn,1200,"%s/minorants.txt",d); f=fopen(fn,"r"); if(!f)die("minorants");
  while(fgets(ln,600,f)){char a[80],b[80],c[80]; if(sscanf(ln,"%79s %79s %79s",a,b,c)!=3)continue; Es[J]=strtod(a,0);Ps[J]=strtod(b,0);Qs[J]=strtod(c,0);aPs[J]=fabs(Ps[J]);aQs[J]=fabs(Qs[J]);J++; if(J>=MJ)die("many");} fclose(f);
  snprintf(fn,1200,"%s/excl.txt",d); f=fopen(fn,"r"); if(!f)die("excl");
  while(fgets(ln,600,f)){char a[80],b[80]; if(sscanf(ln,"%79s %79s",a,b)!=2)continue; SV[NS]=strtod(a,0);RV[NS]=strtod(b,0);NS++; if(NS>=64)die("many s");} fclose(f);
  snprintf(fn,1200,"%s/meta.txt",d); f=fopen(fn,"r"); if(!f)die("meta");
  while(fgets(ln,600,f)){char a[80],b[200]; if(sscanf(ln,"%79s %199s",a,b)!=2)continue;
    if(!strcmp(a,"C_up"))CUP=strtod(b,0); else if(!strcmp(a,"SQRT3_4_UP"))SQ34=strtod(b,0); else if(!strcmp(a,"PI2_UP"))PI2UP=strtod(b,0); else if(!strcmp(a,"PI2_DN"))PI2DN=strtod(b,0); else if(!strcmp(a,"TRIG_EPS"))TEPS=strtod(b,0);} fclose(f);
  snprintf(fn,1200,"%s/trig.bin",d); f=fopen(fn,"rb"); if(!f)die("trig"); TAB=malloc(8*NT); if(fread(TAB,8,NT,f)!=NT)die("trig size"); fclose(f);
  if(!(TEPS>=0x1p-53))die("TEPS"); if(!(SQ34>0.433&&SQ34<0.4331))die("sq34"); if(!(PI2UP>1.5707&&PI2UP<1.5708))die("pi");
}
// volatile-based proof that rounding mode is live, including via the same inline routines
static void roundtest(void){
  volatile double one=1.0,tiny=1e-30,three=3.0,two=2.0;
  double a=one+tiny; if(!(a>1.0))die("FE_UPWARD add");
  double b=-one+tiny; if(!(b==-1.0+0.0||b>-1.0))die("FE_UPWARD add2"); if(b!=-1.0&&b<=-1.0)die("add2");
  double c=one/three; double e=c*three; if(!(e>=1.0))die("FE_UPWARD mul");
  double s=sqrt(two); if(!(s*s>=2.0))die("FE_UPWARD sqrt");
  B x=badd(bc(one),bc(tiny)); if(!(x.m>1.0))die("badd"); B y=bmul(bc(one/three),bc(three)); if(!(y.m+y.r>=1.0))die("bmul");
  printf("rounding test ok: FE_UPWARD active; 1+1e-30 = %a; fegetround=%d (FE_UPWARD=%d)\n",a,fegetround(),FE_UPWARD);
}
typedef struct __attribute__((packed)){uint8_t la,lr,lu,kind; uint32_t ia,ir,iu,w;} R;
static double RHO0,TPUP;
static inline B tc(int64_t i){B z={TAB[i&(NT-1)],TEPS};return z;}
static inline B ts(int64_t i){B z={TAB[(i-NT/4)&(NT-1)],TEPS};return z;}
typedef struct {double Am,hA,Rm,hR,Um,hU,hphi; int64_t pi; B cx,cy; double JxA,JxR,JxU,JyA,JyR,JyU; double a[MJ],b[MJ],d[MJ]; B PI2; long n; double minm;} L;
static double PIUP;
// returns 1 if certified on theta interval k at level d
static int iv(L*l,int64_t k,int d,int*hint){
  int64_t ti=(2*k+1)<<(LT-d-1);
  double del=PIUP/(double)(1<<d); // exact power-of-two scaling; rounding up
  B c1=tc(ti),s1=ts(ti),c2=tc(2*ti),s2=ts(2*ti),c3=tc(3*ti+l->pi),s3=ts(3*ti+l->pi);
  B cu=badd(bmul(l->cx,c1),bmul(l->cy,s1));
  B dtc=bsub(bmul(l->cx,s1),bmul(l->cy,c1));
  B dAc=badd(bmuld(c1,l->JxA),bmuld(s1,l->JyA));
  B dRc=badd(bmuld(c1,l->JxR),bmuld(s1,l->JyR));
  B dUc=badd(bmuld(c1,l->JxU),bmuld(s1,l->JyU));
  B X2=bmuld(c2,l->Am),X3=bmuld(c3,l->Rm),Y2=bmuld(s2,l->Am),Y3=bmuld(s3,l->Rm);
  B Y3P=bmul(Y3,l->PI2);
  int j=*hint;
  for(int attempt=0;attempt<2;attempt++){
    double p=Ps[j],q=Qs[j];
    B G=bsub(badd(bc(Es[j]),bmuld(X3,q)),badd(bmuld(X2,p),cu));
    B DA=bneg(badd(bmuld(c2,p),dAc));
    B DR=bsub(bmuld(c3,q),dRc);
    B DU=bneg(badd(bmuld(Y3P,q),dUc));
    B DT=badd(bsub(bmuld(Y2,2.0*p),bmuld(Y3,3.0*q)),dtc);
    // upper bound of (T' - lower(G over the leaf))
    double loss=G.r+up_abs(DA)*l->hA+up_abs(DR)*l->hR+up_abs(DU)*l->hU+up_abs(DT)*del+l->a[j]+l->b[j]*del+l->d[j]*del*del;
    double ub=TPUP+(-G.m)+loss;
    l->n++;
    if(ub<0.0){ if(-ub<l->minm)l->minm=-ub; *hint=j; return 1; }
    if(attempt==1)break;
    // non-rigorous selection of a better j: value is only used as a hint
    double best=-1e300;int bj=j;
    for(int t=0;t<J;t++){
      double pp=Ps[t],qq=Qs[t];
      double g=Es[t]-pp*X2.m+qq*X3.m-cu.m;
      double da=-pp*c2.m-dAc.m,dr=qq*c3.m-dRc.m,du=-(qq*Y3P.m+dUc.m),dt=2*pp*Y2.m-3*qq*Y3.m+dtc.m;
      double lb=g-fabs(da)*l->hA-fabs(dr)*l->hR-fabs(du)*l->hU-fabs(dt)*del-l->a[t]-l->b[t]*del-l->d[t]*del*del;
      if(lb>best){best=lb;bj=t;}
    }
    if(bj==j)break;
    j=bj;
  }
  *hint=j;
  if(d>=17)return 0;
  if(!iv(l,2*k,d+1,hint))return 0;
  return iv(l,2*k+1,d+1,hint);
}
int main(int argc,char**argv){
  if(argc<5){puts("usage: check libdir prefix T eta");return 2;}
  fesetround(FE_UPWARD);
  roundtest();
  readlib(argv[1]);
  double T=strtod(argv[3],0); T=nextafter(T,INFINITY);
  double ETA=strtod(argv[4],0);
  RHO0=floor(ETA*1048576.0)/1048576.0; if(RHO0>ETA)die("rho0"); // floor is exact in any mode
  PIUP=2*PI2UP;
  TPUP=SQ34+T; double TPDN=-((-SQ34)+(-T))-1e-15;
  if(!(0.22<TPDN/2-1e-3))die("|c|<0.22 does not imply |c|<T'/2");
  char fn[1200]; snprintf(fn,1200,"%s.leaves",argv[2]); FILE*fl=fopen(fn,"rb"); if(!fl)die("leaves");
  snprintf(fn,1200,"%s.wits",argv[2]); FILE*fw=fopen(fn,"rb"); if(!fw)die("wits");
  fseek(fw,0,SEEK_END); long nw=ftell(fw)/88; fseek(fw,0,SEEK_SET); double*W=malloc(88*(nw+1)); if((long)fread(W,88,nw,fw)!=nw)die("wits read"); fclose(fw);
  R r; long nl=0,n0=0,n1=0,n2=0,evals=0; double minm=1e300,minex=1e300,maxc=0; unsigned __int128 vol=0; const int SC=110;
  B PI2={PI2UP,PI2UP-PI2DN};
  while(fread(&r,sizeof r,1,fl)==1){
    nl++;
    if(r.la>45||r.lr>40||r.lu>15)die("levels out of range");
    if(((uint64_t)r.ia>>r.la)!=0||((uint64_t)r.ir>>r.lr)!=0||((uint64_t)r.iu>>r.lu)!=0)die("index out of range");
    if(r.la+r.lr+r.lu>SC)die("vol scale");
    vol+=((unsigned __int128)1)<<(SC-r.la-r.lr-r.lu);
    double ip=ldexp(1.0,-(int)r.la-1),irp=ldexp(1.0,-(int)r.lr+1),iup=ldexp(1.0,-(int)r.lu-1);
    L l; l.hA=ip; l.Am=(2.0*r.ia+1.0)*ip; l.hR=irp; l.Rm=RHO0+(2.0*r.ir+1.0)*irp; l.hU=iup; l.Um=(2.0*r.iu+1.0)*iup;
    if(r.kind==2){ double lo=l.Rm-l.hR; // exact dyadic
      if(!(lo>CUP)){printf("FAIL: out leaf %ld rho_lo=%.17g not > C\n",nl,lo);return 1;} n2++; continue; }
    if(r.kind==255){printf("FAIL: stuck leaf in cover at %ld\n",nl);return 1;}
    l.hphi=l.hU*PI2UP;
    l.pi=(2*(int64_t)r.iu+1)*(1LL<<(LT-2-r.lu-1));
    double Amax=l.Am+l.hA,Rmax=l.Rm+l.hR;
    if(r.kind==1){
      int s=r.w&63; int64_t tk=r.w>>6; if(s>=NS)die("s idx"); if(tk>=NT)die("tau idx");
      B c2=tc(2*tk),c3=tc(3*tk+l.pi),s3=ts(3*tk+l.pi);
      // lower bound of b2+s*b3 on the leaf
      double hC=up_abs(s3)*l.hphi+0.5*l.hphi*l.hphi;
      B a=bneg(bmuld(c2,l.Am)); double al=up_abs(c2)*l.hA;
      B b=bmuld(c3,l.Rm); double bl=up_abs(c3)*l.hR+Rmax*hC;
      B v=badd(a,bmuld(b,SV[s]));
      double ub=RV[s]+(-v.m)+v.r+al+SV[s]*bl;
      if(!(ub<0.0)){printf("FAIL: exclusion leaf %ld (A=%.10g rho=%.10g u=%.10g) ub=%g\n",nl,l.Am,l.Rm,l.Um,ub);return 1;}
      if(-ub<minex)minex=-ub; n1++; continue;
    }
    if(r.kind!=0)die("bad kind");
    if((long)r.w>=nw)die("witness index");
    double*w=W+11*(long)r.w;
    for(int i=0;i<11;i++) if(!isfinite(w[i]))die("non-finite witness");
    double dA=l.Am-w[0],dR=l.Rm-w[1],dU=l.Um-w[2];
    B DAb={dA,U*fabs(dA)},DRb={dR,U*fabs(dR)},DUb={dU,U*fabs(dU)};
    l.cx=badd(bc(w[3]),badd(bmuld(DAb,w[5]),badd(bmuld(DRb,w[6]),bmuld(DUb,w[7]))));
    l.cy=badd(bc(w[4]),badd(bmuld(DAb,w[8]),badd(bmuld(DRb,w[9]),bmuld(DUb,w[10]))));
    l.JxA=w[5];l.JxR=w[6];l.JxU=w[7];l.JyA=w[8];l.JyR=w[9];l.JyU=w[10];
    double JA=sqrt(w[5]*w[5]+w[8]*w[8]),JR=sqrt(w[6]*w[6]+w[9]*w[9]),JUu=sqrt(w[7]*w[7]+w[10]*w[10]);
    double ux=up_abs(l.cx),uy=up_abs(l.cy);
    double cn=sqrt(ux*ux+uy*uy)+JA*l.hA+JR*l.hR+JUu*l.hU;
    if(!(cn<0.22)){printf("FAIL: |c| bound %.6f at leaf %ld\n",cn,nl);return 1;}
    if(cn>maxc)maxc=cn;
    for(int j=0;j<J;j++){
      l.a[j]=0.5*aQs[j]*Rmax*l.hphi*l.hphi+aQs[j]*l.hR*l.hphi;
      l.b[j]=(3.0*aQs[j]+JR)*l.hR+(3.0*aQs[j]*Rmax*l.hphi+JUu*l.hU)+(2.0*aPs[j]+JA)*l.hA;
      l.d[j]=0.5*(4.0*aPs[j]*Amax+9.0*aQs[j]*Rmax+cn);
    }
    l.PI2=PI2; l.n=0; l.minm=1e300;
    int hint=0;
    for(int64_t k=0;k<32;k++){
      if(!iv(&l,k,5,&hint)){ printf("FAIL: leaf %ld kind 0 A=[%.12g,%.12g] rho=[%.12g,%.12g] u=[%.12g,%.12g] at theta interval level5 k=%lld T=%s\n",nl,l.Am-l.hA,l.Am+l.hA,l.Rm-l.hR,l.Rm+l.hR,l.Um-l.hU,l.Um+l.hU,(long long)k,argv[3]); return 1; }
    }
    evals+=l.n; if(l.minm<minm)minm=l.minm; n0++;
  }
  fclose(fl);
  if(vol!=(((unsigned __int128)1)<<SC)){printf("FAIL: leaf volume sum is not the full root (missing or extra leaves): %.12g of 1\n",(double)vol/ldexp(1.0,SC));return 1;}
  fesetround(FE_TONEAREST);
  printf("PASS T=%s eta=%s rho0=%.17g leaves=%ld (cert=%ld excl=%ld out=%ld) witnesses=%ld minorants=%d evals=%ld min_margin=%.4e min_excl_margin=%.4e max|c|<=%.5f cpu=%.2fs\n",argv[3],argv[4],RHO0,nl,n0,n1,n2,nw,J,evals,minm,minex,maxc,(double)clock()/CLOCKS_PER_SEC);
  return 0;
}
