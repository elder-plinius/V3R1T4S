// fam5: fam4 family with an active-set evaluator. Full pass enumerates every box (via ev3 logic, atom ids kept), drops rectangles contained in one of the TOPK largest, later evaluations use only the kept boxes (missing boxes only lower the value). Floats: search only.
// Usage: fam5 IN.par OUTPREFIX SECONDS E SEED S0 [TOPK] [FULLEVERY]
#include "ev3.h"
#include <time.h>
#define MF 8
#define ML 8
typedef struct {int anch,n,L;double c,off,hl,M,dy[ML],w[ML],phi[ML];} Seg;
typedef struct {double Px,Py,m1;int K;Seg s[MF];} Par;
static Cfg G;
static double urand(void){return (double)rand()/RAND_MAX;}
static double nrand(void){double u=urand()+1e-12,v=urand();return sqrt(-2*log(u))*cos(6.283185307179586*v);}
static int build(const Par*p){G.Lx=p->Px;G.Ly=p->Py;G.k=0;G.x[0]=0;G.y[0]=0;G.m[0]=1;G.x[1]=p->Px/2;G.y[1]=0;G.m[1]=p->m1;G.k=2;
 for(int j=0;j<p->K;j++){const Seg*f=&p->s[j];double c=f->anch==0?f->c:0,ws=0;for(int l=0;l<f->L;l++){if(f->w[l]<=0)return 0;ws+=f->w[l];}
  for(int i=0;i<f->n;i++)for(int l=0;l<f->L;l++){double sp=2*f->hl/f->n;double tt=c+f->hl*(2.0*i+1-f->n)/f->n;double t=tt+f->phi[l]*sp,y=f->off+f->dy[l],w=f->M*f->w[l]/ws/f->n;
   if(f->anch==1)t=tt>=0?tt+f->phi[l]*sp:tt-f->phi[l]*sp;
   double a[4],b[4];int ni=0;a[ni]=t;b[ni]=y;ni++;a[ni]=t;b[ni]=-y;ni++;
   if(!f->anch){a[ni]=-t;b[ni]=y;ni++;a[ni]=-t;b[ni]=-y;ni++;}
   for(int q=0;q<ni;q++){if(G.k>=MAXK)return 0;G.x[G.k]=a[q];G.y[G.k]=b[q];G.m[G.k]=w;G.k++;}}}
 return 1;}
// id-based tables
typedef struct {int x1,x2,y1,y2;} Key;
static Key*KF,*KA;static int NKA;static int ncop;static int *IDS;
typedef struct {double a,b,c,d,ar;int key;} UR;
static UR*U;
static int urc(const void*p,const void*q){double u=((UR*)p)->ar,v=((UR*)q)->ar;return u>v?-1:u<v;}
static double *XS,*YS,*TX,*TY,*TM,*PTAB;static int *RXX,*RYY;static int nxs,nys,ntp;
static void table(const Cfg*g,double E){if(!XS){int z=2000000;XS=malloc(8*z);YS=malloc(8*z);TX=malloc(8*z);TY=malloc(8*z);TM=malloc(8*z);RXX=malloc(4*z);RYY=malloc(4*z);PTAB=0;}
 ntp=0;int ax=(int)ceil(E/g->Lx)+1,ay=(int)ceil(E/g->Ly)+1;for(int i=0;i<g->k;i++){double x0=wrap(g->x[i],g->Lx),y0=wrap(g->y[i],g->Ly);for(int u=0;u<=ax;u++)for(int v=0;v<=ay;v++){TX[ntp]=x0+u*g->Lx;TY[ntp]=y0+v*g->Ly;TM[ntp]=g->m[i];ntp++;}}
 memcpy(XS,TX,ntp*8);memcpy(YS,TY,ntp*8);qsort(XS,ntp,8,dcmp);qsort(YS,ntp,8,dcmp);nxs=nys=0;for(int i=0;i<ntp;i++){if(!nxs||XS[i]>XS[nxs-1])XS[nxs++]=XS[i];if(!nys||YS[i]>YS[nys-1])YS[nys++]=YS[i];}
 static size_t cap=0;size_t need=(size_t)(nxs+1)*(nys+1);if(need>cap){free(PTAB);PTAB=malloc(8*need);cap=need;}
 memset(PTAB,0,8*need);for(int q=0;q<ntp;q++){RXX[q]=lb(XS,nxs,TX[q]);RYY[q]=lb(YS,nys,TY[q]);PTAB[(size_t)(RXX[q]+1)*(nys+1)+RYY[q]+1]+=TM[q];}
 for(int i=1;i<=nxs;i++){double*r=PTAB+(size_t)i*(nys+1),*w=r-(nys+1);double s=0;for(int j=1;j<=nys;j++){s+=r[j];r[j]=w[j]+s;}}}
#define PT(i,j) PTAB[(size_t)(i)*(nys+1)+(j)]
// full pass: boxes bounded by id atoms; a box must touch all four sides
static long NB;
typedef struct{int rx,ry,id;}PR;static int prc(const void*a,const void*b){const PR*p=a,*q=b;return p->rx-q->rx;}
static double full(const Cfg*g,double E,int topk){if(!RR)RR=malloc(sizeof(Rect)*MAXR);if(!U){U=malloc(sizeof(UR)*MAXR);KF=malloc(sizeof(Key)*MAXR);KA=malloc(sizeof(Key)*MAXR);}
 table(g,E);static PR*S;static int*ids;static int*tb;if(!S){S=malloc(sizeof(PR)*2000000);ids=malloc(4*2000000);tb=malloc(4*2000000);}
 for(int q=0;q<ntp;q++){S[q].rx=RXX[q];S[q].ry=RYY[q];S[q].id=q;}qsort(S,ntp,sizeof(PR),prc);
 int nb=lb(YS,nys,g->Ly-1e-13);NR=0;int nu=0;NB=0;static int*yid;if(!yid)yid=malloc(4*2000000);for(int q=0;q<ntp;q++)yid[RYY[q]]=q;
 for(int j1=0;j1<nb;j1++)for(int j2=j1;j2<nys&&YS[j2]-YS[j1]<=E;j2++){double dy=YS[j2]-YS[j1];int n=0;for(int q=0;q<ntp;q++){int r=S[q].ry;if(r<j1||r>j2)continue;ids[n]=q;tb[n]=(r==j1?1:0)|(r==j2?2:0);n++;}
   if(!n)continue;
   for(int a=0;a<n;a++){int i1=S[ids[a]].rx;double x1=XS[i1];if(x1>=g->Lx)break;if(a&&S[ids[a-1]].rx==i1)continue;int mask=0;
    for(int b=a;b<n;b++){int i2=S[ids[b]].rx;double dx=XS[i2]-x1;if(dx>E)break;mask|=tb[b];if(b+1<n&&S[ids[b+1]].rx==i2)continue;if(mask!=3)continue;
     double M=PT(i2+1,j2+1)-PT(i1,j2+1)-PT(i2+1,j1)+PT(i1,j1);double e=dx>dy?dx:dy;if(e*e>M)continue;double rho=sqrt(M)/2;double A=XS[i2]-rho,B=x1+rho,C=YS[j2]-rho,D=YS[j1]+rho;if(B<=A||D<=C||nu>=MAXR)continue;
     add_wrapped(g,A,B,C,D);double aw=wrap(A,g->Lx),cw=wrap(C,g->Ly);U[nu].a=aw;U[nu].b=aw+B-A;U[nu].c=cw;U[nu].d=cw+D-C;U[nu].ar=(B-A)*(D-C);U[nu].key=nu;KF[nu].x1=S[ids[a]].id;KF[nu].x2=S[ids[b]].id;KF[nu].y1=yid[j1];KF[nu].y2=yid[j2];nu++;}}}
 NB=nu;double Ar=union_area();qsort(U,nu,sizeof(UR),urc);NKA=0;int lim=topk<nu?topk:nu;double Lx=g->Lx,Ly=g->Ly;
 for(int i=0;i<nu;i++){int cov=0;for(int t=0;t<lim&&t<i&&!cov;t++){for(int sx=-1;sx<=1&&!cov;sx++)for(int sy=-1;sy<=1&&!cov;sy++){double s=sx*Lx,w=sy*Ly;if(U[t].a+s<=U[i].a&&U[i].b<=U[t].b+s&&U[t].c+w<=U[i].c&&U[i].d<=U[t].d+w)cov=1;}}if(!cov)KA[NKA++]=KF[U[i].key];}
 return Ar/total_mass(g);}
static double active(const Cfg*g,double E){table(g,E);NR=0;for(int q=0;q<NKA;q++){Key*k=&KA[q];int i1=RXX[k->x1],i2=RXX[k->x2],j1=RYY[k->y1],j2=RYY[k->y2];if(i2<i1||j2<j1)continue;double dx=XS[i2]-XS[i1],dy=YS[j2]-YS[j1];double M=PT(i2+1,j2+1)-PT(i1,j2+1)-PT(i2+1,j1)+PT(i1,j1);if(M<=1e-12)continue;double e=dx>dy?dx:dy;if(e*e>M)continue;double r=sqrt(M)/2;add_wrapped(g,XS[i2]-r,XS[i1]+r,YS[j2]-r,YS[j1]+r);}return union_area()/total_mass(g);}
static long EV;
static int vp(const Par*p){if(p->Px<.5||p->Py<.5||p->m1<=0)return 0;for(int j=0;j<p->K;j++)if(p->s[j].M<=0||p->s[j].hl<=0)return 0;return build(p);}
static double savefull(const char*o,const Par*p,double E,double t,int topk){char b[512];vp(p);double v=full(&G,E,topk);snprintf(b,512,"%s.cfg",o);FILE*f=fopen(b,"w");fprintf(f,"%.15g %.15g\n",G.Lx,G.Ly);for(int i=0;i<G.k;i++)fprintf(f,"%.15g %.15g %.15g\n",G.x[i],G.y[i],G.m[i]);fclose(f);
 snprintf(b,512,"%s.par",o);f=fopen(b,"w");fprintf(f,"%.15g %.15g %.15g %d\n",p->Px,p->Py,p->m1,p->K);for(int j=0;j<p->K;j++){const Seg*q=&p->s[j];fprintf(f,"%d %.15g %.15g %.15g %.15g %d %d\n",q->anch,q->c,q->off,q->hl,q->M,q->n,q->L);for(int l=0;l<q->L;l++)fprintf(f,"%.15g %.15g %.15g\n",q->dy[l],q->w[l],q->phi[l]);}fprintf(f,"# value %.10f evals %ld secs %.0f k %d boxes %ld active %d\n",v,EV,t,G.k,NB,NKA);fclose(f);return v;}
static void perturb(Par*p,double s){if(urand()<.3)p->Px*=exp(s*.3*nrand());if(urand()<.3)p->Py*=exp(s*.3*nrand());if(urand()<.3)p->m1*=exp(s*nrand());
 int any=rand()%(p->K+1);for(int j=0;j<p->K;j++){if(urand()>.3&&j!=any)continue;Seg*f=&p->s[j];if(urand()<.5&&!f->anch)f->c+=s*nrand();if(urand()<.5)f->off+=s*nrand();if(urand()<.5)f->hl*=exp(s*nrand());if(urand()<.5)f->M*=exp(s*nrand());
  for(int l=0;l<f->L;l++){if(urand()<.3)f->dy[l]+=s*nrand();if(urand()<.2)f->w[l]*=exp(s*nrand());if(urand()<.1)f->phi[l]+=3*s*nrand();}}}
int main(int c,char**v){const char*in=v[1],*o=v[2];double tl=atof(v[3]),E=atof(v[4]);srand(atoi(v[5]));double s0=c>6?atof(v[6]):.005;int topk=c>7?atoi(v[7]):1500;int fe=c>8?atoi(v[8]):400;
 Par p;memset(&p,0,sizeof p);FILE*f=fopen(in,"r");if(!f)return 1;fscanf(f,"%lf %lf %lf %d",&p.Px,&p.Py,&p.m1,&p.K);for(int j=0;j<p.K;j++){Seg*q=&p.s[j];fscanf(f,"%d %lf %lf %lf %lf %d %d",&q->anch,&q->c,&q->off,&q->hl,&q->M,&q->n,&q->L);for(int l=0;l<q->L;l++)fscanf(f,"%lf %lf %lf",&q->dy[l],&q->w[l],&q->phi[l]);}fclose(f);
 time_t t0=time(0),tl2=t0;vp(&p);double st=full(&G,E,topk),cur=st;long nb0=NB;int na0=NKA;double s=s0;long it=0;
 double ttot=0;
 while(difftime(time(0),t0)<tl){Par h=p;perturb(&h,s);if(!vp(&h)){s*=.99;continue;}double e=active(&G,E);EV++;it++;if(e>cur){p=h;cur=e;s*=1.25;}else s*=0.99;if(s<3e-7)s=s0*.3;
  if(it%fe==0){vp(&p);double fv=full(&G,E,topk);if(fv>cur)cur=fv;}
  if(difftime(time(0),tl2)>120){savefull(o,&p,E,difftime(time(0),t0),topk);tl2=time(0);}}
 double v2=savefull(o,&p,E,difftime(time(0),t0),topk);printf("%s start %.8f best %.8f evals %ld k %d boxes %ld/%ld active %d/%d secs %.0f\n",o,st,v2,EV,G.k,nb0,NB,na0,NKA,difftime(time(0),t0));return 0;}
