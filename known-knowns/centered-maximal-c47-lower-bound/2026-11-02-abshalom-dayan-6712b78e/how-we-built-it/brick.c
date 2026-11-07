// brick: L equally spaced levels filling the strip |y|<=1/2, level j atoms with phase j*PH of the period p, equal mass m. Two parameter scan by coordinate refinement. Score cover - MU*density. Floats, search only.
// Usage: brick Lmax MU
#define MAXK 64
#define MAXR 800000
#include "ev3.h"
static Cfg G;static double cov,den;
static double sc(int L,double m,double p,double ph,double MU){if(m<=0||p<=0.02)return -9;G.Lx=p;G.Ly=40;G.k=L;double d=L>1?(1-sqrt(m))/(L-1):0;if(d<0)return -9;for(int j=0;j<L;j++){G.x[j]=fmod(j*ph,1.0)*p;G.y[j]=20+(j-(L-1)/2.0)*d;G.m[j]=m;}CL0=19.5;CL1=20.5;double S=L*m;double v=evalcfg(&G,3.0)*S;cov=v/p;den=S/p;return cov-MU*den;}
int main(int c,char**v){int Lm=atoi(v[1]);double MU=atof(v[2]);for(int L=1;L<=Lm;L++){for(int w=0;w<2;w++){double ph=w?(L>2?1.0/3:0.5):0.5;double best=-9,bm=0,bp=0;
   double m0=0.7/(L*L),p0=(1.2/L);for(double fm=.4;fm<=2.2;fm*=1.04)for(double fp=.4;fp<=2.2;fp*=1.04){double e=sc(L,m0*fm,p0*fp,ph,MU);if(e>best){best=e;bm=m0*fm;bp=p0*fp;}}
   double s=.02;while(s>1e-6){int im=0;double cand[4][2]={{bm*(1+s),bp},{bm*(1-s),bp},{bm,bp*(1+s)},{bm,bp*(1-s)}};for(int i=0;i<4;i++){double e=sc(L,cand[i][0],cand[i][1],ph,MU);if(e>best+1e-12){best=e;bm=cand[i][0];bp=cand[i][1];im=1;}}if(!im)s/=2;}
   sc(L,bm,bp,ph,MU);printf("L=%d phase %.3f score %.6f cover %.6f density %.6f ratio %.5f m %.6f sqrtm %.5f p %.5f d %.5f\n",L,ph,best,cov,den,cov/den,bm,sqrt(bm),bp,L>1?(1-sqrt(bm))/(L-1):0);fflush(stdout);}}return 0;}
