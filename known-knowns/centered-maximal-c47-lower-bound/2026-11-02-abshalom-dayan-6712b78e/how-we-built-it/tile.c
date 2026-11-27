// tile: minimal line density to cover the strip |y|<=1/2 by a periodic tile of J atoms, free x,y,m (or y=0 if LINE). Score = covered fraction - MU*density. Floats, search only.
// Usage: tile J SECONDS SEED MU LINE(1/0)
#define MAXK 64
#define MAXR 400000
#include "ev3.h"
#include <time.h>
static Cfg G;static double urand(void){return (double)rand()/RAND_MAX;}
static double nrand(void){double u=urand()+1e-12,v=urand();return sqrt(-2*log(u))*cos(6.283185307179586*v);}
typedef struct{double p;double x[32],y[32],m[32];}T;static int J,LINE;static double MU;static double cov,den;
static double score(const T*t){if(t->p<.05||t->p>8)return -9;G.Lx=t->p;G.Ly=40;G.k=J;double S=0;for(int i=0;i<J;i++){if(t->m[i]<=1e-5||fabs(t->y[i])>1)return -9;G.x[i]=t->x[i];G.y[i]=20+(LINE?0:t->y[i]);G.m[i]=t->m[i];S+=t->m[i];}
 CL0=19.5;CL1=20.5;double v=evalcfg(&G,3.0)*S;cov=v/t->p;den=S/t->p;return cov-MU*den;}
int main(int c,char**v){J=atoi(v[1]);double tl=atof(v[2]);srand(atoi(v[3]));MU=atof(v[4]);LINE=atoi(v[5]);time_t t0=time(0);double gb=-9;T gbt;int rs=0;
 while(difftime(time(0),t0)<tl){rs++;T t;t.p=J*(.6+urand());for(int i=0;i<J;i++){t.x[i]=urand()*t.p;t.y[i]=LINE?0:.4*(urand()-.5);t.m[i]=.3+urand();}
  double cur=score(&t),s=.1;while(s>1e-6&&difftime(time(0),t0)<tl){T h=t;if(urand()<.5)h.p*=exp(s*nrand());int n=1+rand()%3;for(int q=0;q<n;q++){int i=rand()%J;double w=urand();if(w<.4)h.x[i]+=s*nrand();else if(w<.6&&!LINE)h.y[i]+=s*nrand();else h.m[i]*=exp(s*nrand());}double e=score(&h);if(e>cur){t=h;cur=e;s*=1.3;}else s*=.995;}
  if(cur>gb){gb=cur;gbt=t;}}
 score(&gbt);printf("J=%d LINE=%d MU=%.3f restarts %d score %.6f cover %.6f density %.6f p %.5f\n",J,LINE,MU,rs,gb,cov,den,gbt.p);for(int i=0;i<J;i++)printf("  x %.5f y %.5f m %.5f\n",fmod(gbt.x[i]+100*gbt.p,gbt.p),LINE?0:gbt.y[i],gbt.m[i]);return 0;}
