// search.c: finds cover in (A,rho,u), u=phi/(pi/2). Plain doubles (search is untrusted; check.c decides).
// usage: search scan outdir ... | search cover libdir out_prefix T eta [opts]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>
#include <unistd.h>
#define LT 18
#define NT (1<<LT)
#define MAXJ 200
static double *tab; static int nj; static double E[MAXJ],P[MAXJ],Q[MAXJ],aP[MAXJ],aQ[MAXJ];
static int ns; static double Ss[64],Rs[64];
static double C_UP,ETA_FILE,SQ34;
static inline double co(int64_t i){return tab[i&(NT-1)];}
static inline double si(int64_t i){return tab[(i-(NT/4))&(NT-1)];}
static void loadlib(const char*d){
  char fn[1024],line[512]; FILE*f;
  snprintf(fn,1024,"%s/minorants.txt",d); f=fopen(fn,"r"); if(!f){perror(fn);exit(2);}
  nj=0; while(fgets(line,512,f)){char a[64],b[64],c[64],n[64]; if(sscanf(line,"%63s %63s %63s %63s",a,b,c,n)<3)continue; E[nj]=strtod(a,0);P[nj]=strtod(b,0);Q[nj]=strtod(c,0);aP[nj]=fabs(P[nj]);aQ[nj]=fabs(Q[nj]);nj++;} fclose(f);
  snprintf(fn,1024,"%s/excl.txt",d); f=fopen(fn,"r"); ns=0; while(fgets(line,512,f)){char a[64],b[64]; if(sscanf(line,"%63s %63s",a,b)==2){Ss[ns]=strtod(a,0);Rs[ns]=strtod(b,0);ns++;}} fclose(f);
  snprintf(fn,1024,"%s/meta.txt",d); f=fopen(fn,"r"); while(fgets(line,512,f)){char a[64],b[128]; if(sscanf(line,"%63s %127s",a,b)==2){ if(!strcmp(a,"C_up"))C_UP=strtod(b,0); if(!strcmp(a,"eta"))ETA_FILE=strtod(b,0); if(!strcmp(a,"SQRT3_4_UP"))SQ34=strtod(b,0);} } fclose(f);
  snprintf(fn,1024,"%s/trig.bin",d); f=fopen(fn,"rb"); tab=malloc(sizeof(double)*NT); if(fread(tab,8,NT,f)!=NT){exit(3);} fclose(f);
}
// ---- primal solve at a point ----
typedef struct {double A,rho; int64_t pi;} Pt;
static inline double Hval(const Pt*x,int64_t k,int*jb){
  double c2=co(2*k), c3=co(3*k+x->pi); double b2=-x->A*c2,b3=x->rho*c3; double best=-1e9;int bj=0;
  for(int j=0;j<nj;j++){double v=E[j]+P[j]*b2+Q[j]*b3; if(v>best){best=v;bj=j;}}
  if(jb)*jb=bj; return best;
}
static int64_t last_oracle_ops=0;
// min of H(theta)-c.u(theta) by Lipschitz branch and bound on the table grid
static double oracle(const Pt*x,double cx,double cy,int64_t*argk){
  double Lc=0; for(int j=0;j<nj;j++){double l=2*aP[j]*x->A+3*aQ[j]*x->rho; if(l>Lc)Lc=l;} Lc+=sqrt(cx*cx+cy*cy);
  static int64_t cur[8192],nxt[8192]; static double val[8192];
  int d=7,n=1<<d; int64_t step=1<<(LT-d);
  double best=1e9;int64_t ba=0;
  for(int i=0;i<n;i++){int64_t k=i*step; double v=Hval(x,k,0)-cx*co(k)-cy*si(k); cur[i]=k;val[i]=v; if(v<best){best=v;ba=k;}}
  while(step>1){
    double dth=2*M_PI/(1<<d)/1.0; // spacing
    int m=0;
    for(int i=0;i<n;i++) if(val[i]-Lc*dth/2<best){ if(m<8190){nxt[m++]=cur[i]-step/2; nxt[m++]=cur[i]+step/2;} }
    step/=2;d++;
    n=m;
    for(int i=0;i<n;i++){int64_t k=nxt[i]; double v=Hval(x,k,0)-cx*co(k)-cy*si(k); cur[i]=k;val[i]=v; if(v<best){best=v;ba=k;}}
    // parents retained implicitly: their value already considered in best; children cover +- half spacing
    last_oracle_ops+=n;
  }
  *argk=ba; return best;
}
typedef struct {double cx,cy,t,m; int64_t ref[3];} Sol;
static int solve3(const Pt*x,const int64_t*r,double*cx,double*cy,double*t,double*w){
  // weights: w_i proportional to sin(theta_{i+2}-theta_{i+1})
  double H[3]; for(int i=0;i<3;i++)H[i]=Hval(x,r[i],0);
  double c[3],s[3]; for(int i=0;i<3;i++){c[i]=co(r[i]);s[i]=si(r[i]);}
  double w0=c[1]*s[2]-s[1]*c[2], w1=c[2]*s[0]-s[2]*c[0], w2=c[0]*s[1]-s[0]*c[1];
  double W=w0+w1+w2; if(fabs(W)<1e-14)return 0;
  w[0]=w0/W;w[1]=w1/W;w[2]=w2/W;
  *t=w[0]*H[0]+w[1]*H[1]+w[2]*H[2];
  // solve H_i-t = cx c_i + cy s_i from two equations
  double a=H[0]-*t,b=H[1]-*t; double det=c[0]*s[1]-s[0]*c[1];
  if(fabs(det)<1e-9){ a=H[1]-*t;b=H[2]-*t; det=c[1]*s[2]-s[1]*c[2]; if(fabs(det)<1e-9){a=H[2]-*t;b=H[0]-*t;det=c[2]*s[0]-s[2]*c[0]; *cx=(a*s[0]-b*s[2])/det;*cy=(c[2]*b-c[0]*a)/det;return 1;}
    *cx=(a*s[2]-b*s[1])/det;*cy=(c[1]*b-c[2]*a)/det;return 1;}
  *cx=(a*s[1]-b*s[0])/det;*cy=(c[0]*b-c[1]*a)/det; return 1;
}
static long nsolves=0,noracles=0;
static void primal(double A,double rho,int64_t pi,Sol*S,int warm){
  Pt x={A,rho,pi}; int64_t r[3];
  if(warm){memcpy(r,S->ref,sizeof r);double w[3],a,b,t; if(!solve3(&x,r,&a,&b,&t,w)||w[0]<-1e-12||w[1]<-1e-12||w[2]<-1e-12)warm=0;}
  if(!warm){r[0]=0;r[1]=NT/3;r[2]=2*(int64_t)NT/3;}
  double bestm=-1e9,bcx=0,bcy=0,cx=0,cy=0,t=0,w[3];
  nsolves++;
  for(int it=0;it<60;it++){
    solve3(&x,r,&cx,&cy,&t,w);
    int64_t ka; double m=oracle(&x,cx,cy,&ka); noracles++;
    if(m>bestm){bestm=m;bcx=cx;bcy=cy;}
    if(t-m<2e-7)break;
    // exchange
    int done=0; double bt=1e9;int bi=-1;
    for(int i=0;i<3;i++){int64_t rr[3];memcpy(rr,r,sizeof r);rr[i]=ka;double a,b,tt,ww[3]; if(!solve3(&x,rr,&a,&b,&tt,ww))continue; if(ww[0]>=-1e-13&&ww[1]>=-1e-13&&ww[2]>=-1e-13){ if(tt<bt){bt=tt;bi=i;} }}
    if(bi<0)break; r[bi]=ka; (void)done;
  }
  S->cx=bcx;S->cy=bcy;S->t=t;S->m=bestm;memcpy(S->ref,r,sizeof r);
}
// feasibility violation at a point: max over tau,s of b2+s b3-RHS(s); positive means excluded.
static double exclscore(double A,double hA,double rho,double hr,int64_t pi,double hphi,int ntau,int64_t*bt,int*bs){
  double best=-1e9; int64_t st=NT/ntau; double rmax=rho+hr;
  for(int64_t t=0;t<ntau;t++){ int64_t k=t*st; double c2=co(2*k),c3=co(3*k+pi),s3=si(3*k+pi);
    double a=-A*c2-hA*fabs(c2); double b=rho*c3-hr*fabs(c3)-rmax*(fabs(s3)*hphi+0.5*hphi*hphi);
    for(int i=0;i<ns;i++){double v=a+Ss[i]*b-Rs[i]; if(v>best){best=v;*bt=k;*bs=i;}}
  }
  return best;
}
static double exclone(double A,double hA,double rho,double hr,int64_t pi,double hphi,int64_t k,int i){
  double rmax=rho+hr,c2=co(2*k),c3=co(3*k+pi),s3=si(3*k+pi);
  double a=-A*c2-hA*fabs(c2); double b=rho*c3-hr*fabs(c3)-rmax*(fabs(s3)*hphi+0.5*hphi*hphi);
  return a+Ss[i]*b-Rs[i];
}
// ---- box evaluation ----
typedef struct {double x0A,x0R,x0U,c0x,c0y,Jx[3],Jy[3]; int64_t idx; Sol sol;} Wit;
typedef struct {int la,lr,lu; int64_t ia,ir,iu;} Box;
static double Tp; // target sqrt3/4+T+slack
static int D0=5,DMAX=17;
typedef struct {double Am,hA,Rm,hR,hphi,hu,Amax,Rmax;int64_t pi;double cx,cy,J[6],cnorm,JA,JR,JU;double a[MAXJ],b[MAXJ],d[MAXJ];int fail_axis; long nev; double minm;} EB;
static int chk(EB*B,int64_t k,int d,int*hint){
  int64_t ti=(2*k+1)<<(LT-d-1); double del=M_PI/(double)(1<<d);
  double c1=co(ti),s1=si(ti),c2=co(2*ti),s2=si(2*ti),c3=co(3*ti+B->pi),s3=si(3*ti+B->pi);
  double cu=B->cx*c1+B->cy*s1, dtc=B->cx*s1-B->cy*c1;
  double dAc=B->J[0]*c1+B->J[3]*s1, dRc=B->J[1]*c1+B->J[4]*s1, dUc=B->J[2]*c1+B->J[5]*s1;
  double Am=B->Am,Rm=B->Rm,hA=B->hA,hR=B->hR,hphi=B->hphi,hu=B->hu;
  // hint first
  int j=*hint; B->nev++;
  double G=E[j]-P[j]*Am*c2+Q[j]*Rm*c3-cu;
  double DA=-P[j]*c2-dAc,DR=Q[j]*c3-dRc,DU=-Q[j]*Rm*s3*hphi-dUc*hu,DT=2*P[j]*Am*s2-3*Q[j]*Rm*s3+dtc;
  double lb=G-fabs(DA)*hA-fabs(DR)*hR-fabs(DU)-fabs(DT)*del-(B->a[j]+B->b[j]*del+B->d[j]*del*del);
  if(lb>Tp){ if(lb-Tp<B->minm)B->minm=lb-Tp; return 1;}
  double best=-1e9;int bj=-1; double bparam=-1e9;
  double p2=-Am*c2,p3=Rm*c3,dt2=2*Am*s2,dt3=-3*Rm*s3;
  for(j=0;j<nj;j++){
    double G=E[j]+P[j]*p2+Q[j]*p3-cu;
    double DA=-P[j]*c2-dAc,DR=Q[j]*c3-dRc,DU=-Q[j]*Rm*s3*hphi-dUc*hu,DT=P[j]*dt2+Q[j]*dt3+dtc;
    double pl=G-fabs(DA)*hA-fabs(DR)*hR-fabs(DU)-B->a[j];
    double lb=pl-fabs(DT)*del-(B->b[j]*del+B->d[j]*del*del);
    if(lb>best){best=lb;bj=j;}
    if(pl>bparam)bparam=pl;
  }
  B->nev+=nj;
  if(best>Tp){*hint=bj; if(best-Tp<B->minm)B->minm=best-Tp; return 1;}
  if(bparam<=Tp||d>=DMAX){ // cannot be rescued by theta splits
    j=bj; double la=fabs(-P[j]*c2-dAc)*hA, lr=fabs(Q[j]*c3-dRc)*hR, lu=fabs(-Q[j]*Rm*s3*hphi-dUc*hu);
    B->fail_axis = (la>=lr&&la>=lu)?0:((lr>=lu)?1:2);
    return 0;
  }
  *hint=bj;
  if(!chk(B,2*k,d+1,hint))return 0;
  if(!chk(B,2*k+1,d+1,hint))return 0;
  return 1;
}
static double RHO0=0.5;
static inline double mid(int64_t i,int l){return (2*i+1)/ldexp(1.0,l+1);}
static void boxmid(const Box*b,double*Am,double*hA,double*Rm,double*hR,double*Um,double*hU){
  *Am=mid(b->ia,b->la);*hA=ldexp(1.0,-b->la-1);
  *Rm=RHO0+4*mid(b->ir,b->lr);*hR=ldexp(4.0,-b->lr-1);
  *Um=mid(b->iu,b->lu);*hU=ldexp(1.0,-b->lu-1);
}
static long nevals=0,nboxes=0;
static int evalbox(const Box*bx,const Wit*w,int*axis,double*minm){
  EB B; double Um,hU; boxmid(bx,&B.Am,&B.hA,&B.Rm,&B.hR,&Um,&hU); B.hu=hU; B.hphi=hU*M_PI_2;
  B.Amax=B.Am+B.hA;B.Rmax=B.Rm+B.hR;
  B.pi=(2*bx->iu+1)*(1LL<<(LT-2-bx->lu-1));
  B.cx=w->c0x+w->Jx[0]*(B.Am-w->x0A)+w->Jx[1]*(B.Rm-w->x0R)+w->Jx[2]*(Um-w->x0U);
  B.cy=w->c0y+w->Jy[0]*(B.Am-w->x0A)+w->Jy[1]*(B.Rm-w->x0R)+w->Jy[2]*(Um-w->x0U);
  for(int i=0;i<3;i++){B.J[i]=w->Jx[i];B.J[3+i]=w->Jy[i];}
  double JA=hypot(B.J[0],B.J[3]),JR=hypot(B.J[1],B.J[4]),JU=hypot(B.J[2],B.J[5]);
  double cn=hypot(B.cx,B.cy)+JA*B.hA+JR*B.hR+JU*hU;
  if(cn>=0.2199){*axis=0;return 0;}
  for(int j=0;j<nj;j++){
    B.a[j]=0.5*aQ[j]*B.Rmax*B.hphi*B.hphi+aQ[j]*B.hR*B.hphi;
    B.b[j]=(3*aQ[j]+JR)*B.hR+(3*aQ[j]*B.Rmax*B.hphi+JU*hU)+(2*aP[j]+JA)*B.hA;
    B.d[j]=0.5*(4*aP[j]*B.Amax+9*aQ[j]*B.Rmax+cn);
  }
  B.nev=0;B.fail_axis=0;B.minm=1e9;
  int hint=0; int n=1<<D0; int ok=1;
  for(int64_t k=0;k<n&&ok;k++){ if(!chk(&B,k,D0,&hint))ok=0; }
  nevals+=B.nev;nboxes++;
  *axis=B.fail_axis; if(minm)*minm=B.minm;
  return ok;
}
static FILE*fC,*fW; static int64_t nleaf=0,nwit=0,ncert=0,nexcl=0,nout=0,nstuck=0; static double ETA;
static double glob_min=1e9, stuck_min_val=1e9; static int STOREOUT=1;
typedef struct __attribute__((packed)){uint8_t la,lr,lu,kind; uint32_t ia,ir,iu,w;} Rec;
static void emit(const Box*b,int kind,uint32_t w){Rec r={b->la,b->lr,b->lu,kind,(uint32_t)b->ia,(uint32_t)b->ir,(uint32_t)b->iu,w}; if(fC)fwrite(&r,sizeof r,1,fC); nleaf++;}
static uint32_t witidx(Wit*w){ if(w->idx<0){w->idx=nwit++; double d[11]={w->x0A,w->x0R,w->x0U,w->c0x,w->c0y,w->Jx[0],w->Jx[1],w->Jx[2],w->Jy[0],w->Jy[1],w->Jy[2]}; if(fW)fwrite(d,8,11,fW);} return (uint32_t)w->idx;}
static int SOLVE_EVERY=1,AFFINE=1;
static void mkwit(const Box*b,Wit*w,const Wit*par){
  double Am,hA,Rm,hR,Um,hU; boxmid(b,&Am,&hA,&Rm,&hR,&Um,&hU);
  int64_t pi=(2*b->iu+1)*(1LL<<(LT-2-b->lu-1));
  Sol S; int warm=0; if(par){S=par->sol;warm=1;}
  primal(Am,Rm,pi,&S,warm);
  w->x0A=Am;w->x0R=Rm;w->x0U=Um;w->c0x=S.cx;w->c0y=S.cy;w->sol=S;w->idx=-1;
  for(int i=0;i<3;i++){w->Jx[i]=0;w->Jy[i]=0;}
  if(AFFINE){
    Sol a=S,c=S;
    primal(Am+hA,Rm,pi,&a,1);primal(Am-hA,Rm,pi,&c,1); w->Jx[0]=(a.cx-c.cx)/(2*hA);w->Jy[0]=(a.cy-c.cy)/(2*hA);
    a=S;c=S; primal(Am,Rm+hR,pi,&a,1);primal(Am,Rm-hR,pi,&c,1); w->Jx[1]=(a.cx-c.cx)/(2*hR);w->Jy[1]=(a.cy-c.cy)/(2*hR);
    a=S;c=S; int64_t dp=(int64_t)1<<(LT-2-b->lu-1); primal(Am,Rm,pi+dp,&a,1);primal(Am,Rm,pi-dp,&c,1); w->Jx[2]=(a.cx-c.cx)/(2*hU);w->Jy[2]=(a.cy-c.cy)/(2*hU);
  }
  // recentre c0 so that c at the box centre matches: already x0=centre
}
static long hist[64]; static double t0; static double TLIM=1e18; static int abortflag=0;
static int MINLVL=26; static int QUICKFAIL=1;
static void process(Box b,Wit*inh,int64_t ext,int exs,int depth,int since){
  double Am,hA,Rm,hR,Um,hU; boxmid(&b,&Am,&hA,&Rm,&hR,&Um,&hU);
  double rlo=Rm-hR,rhi=Rm+hR;
  if(rlo>C_UP){emit(&b,2,0);nout++;return;}
  int64_t pi=(2*b.iu+1)*(1LL<<(LT-2-b.lu-1)); double hphi=hU*M_PI_2;
  // exclusion
  double sc=-1; if(exs>=0) sc=exclone(Am,hA,Rm,hR,pi,hphi,ext,exs);
  if(sc<=1e-13){ int64_t t2=0;int s2=0; sc=exclscore(Am,hA,Rm,hR,pi,hphi,128,&t2,&s2); if(sc>-0.3){ // refine tau near best
      for(int64_t dt=-16;dt<=16;dt++){int64_t k=t2+dt*(NT/2048); for(int i=0;i<ns;i++){double v=exclone(Am,hA,Rm,hR,pi,hphi,k,i); if(v>sc){sc=v;ext=k;exs=i;}}}
      if(exs<0||sc==-1){ext=t2;exs=s2;} }
    else {ext=t2;exs=s2;}
    double sc2=exclone(Am,hA,Rm,hR,pi,hphi,ext,exs); if(sc2<sc)sc=sc2;
  }
  if(sc>1e-13){ emit(&b,1,(uint32_t)(((uint32_t)((ext%NT+NT)%NT))<<6|exs)); nexcl++; return; }
  int axis=0; double mm;
  if(inh&&evalbox(&b,inh,&axis,&mm)){ emit(&b,0,witidx(inh)); ncert++; if(mm<glob_min)glob_min=mm; hist[depth<64?depth:63]++; return; }
  Wit w; Wit*cur=inh; int since2=since+1;
  if(since2>=SOLVE_EVERY){ mkwit(&b,&w,inh); since2=0; cur=&w;
    if(w.sol.m<Tp-1e-6){ int64_t bt;int bs; double sc3=exclscore(Am,0,Rm,0,pi,0,2048,&bt,&bs); if(sc3<-1e-9 && QUICKFAIL){ printf("GENUINE-FAIL T=%.6f primal=%.7f at A=%.7f rho=%.7f u=%.7f (20)-slack=%.3e\n",Tp-SQ34,w.sol.m-SQ34,Am,Rm,Um,sc3); fflush(stdout); exit(1);} }
    if(evalbox(&b,&w,&axis,&mm)){ emit(&b,0,witidx(&w)); ncert++; if(mm<glob_min)glob_min=mm; hist[depth<64?depth:63]++; return; }
  }
  if(b.la+b.lr+b.lu>=MINLVL||(b.la>=24&&b.lr>=24&&b.lu>=15)){ emit(&b,255,0); nstuck++; if(nstuck<40){Sol S; memset(&S,0,sizeof S); primal(Am,Rm,pi,&S,0); fprintf(stderr,"STUCK A=%.8f rho=%.8f u=%.8f hA=%.2e hR=%.2e hU=%.2e primal=%.8f sc=%.3e\n",Am,Rm,Um,hA,hR,hU,S.m-SQ34,sc);} return; }
  if(rlo<=C_UP&&rhi>C_UP&&hR>0.02)axis=1;
  if(axis==2&&b.lu>=15)axis=(hA>hR)?0:1;
  if(b.la>=28&&axis==0)axis=(hU>hR)?2:1;
  // balance: never let one axis become absurdly finer than loss suggests
  Box c1=b,c2=b;
  if(axis==0){c1.la++;c2.la++;c1.ia=2*b.ia;c2.ia=2*b.ia+1;}
  else if(axis==1){c1.lr++;c2.lr++;c1.ir=2*b.ir;c2.ir=2*b.ir+1;}
  else {c1.lu++;c2.lu++;c1.iu=2*b.iu;c2.iu=2*b.iu+1;}
  process(c1,cur,ext,exs,depth+1,since2);
  process(c2,cur,ext,exs,depth+1,since2);
}
static const char*FORCED="AAARRRUU"; // 256 top cells
static int cell=0,cellA=0,cellB=1<<30;
static FILE*fP;
static void top(Box b,int lev){
  if(abortflag)return;
  if(lev==(int)strlen(FORCED)){
    if(cell>=cellA&&cell<cellB){
      process(b,NULL,0,-1,lev,1000);
      if(fC)fflush(fC); if(fW)fflush(fW);
      if(fP){fprintf(fP,"%d %lld %lld %.1f\n",cell,(long long)nleaf,(long long)nwit,(double)clock()/CLOCKS_PER_SEC);fflush(fP);}
      if((double)clock()/CLOCKS_PER_SEC>TLIM){abortflag=1;}
      if(cell%16==0)fprintf(stderr,"cell %d leaves %lld cert %lld excl %lld out %lld stuck %lld wits %lld solves %ld oracles %ld boxes %ld evals %ld cpu %.1f\n",cell,(long long)nleaf,(long long)ncert,(long long)nexcl,(long long)nout,(long long)nstuck,(long long)nwit,nsolves,noracles,nboxes,nevals,(double)clock()/CLOCKS_PER_SEC);
    }
    cell++; return;
  }
  Box c1=b,c2=b; char ax=FORCED[lev];
  if(ax=='A'){c1.la++;c2.la++;c1.ia=2*b.ia;c2.ia=2*b.ia+1;}
  else if(ax=='R'){c1.lr++;c2.lr++;c1.ir=2*b.ir;c2.ir=2*b.ir+1;}
  else {c1.lu++;c2.lu++;c1.iu=2*b.iu;c2.iu=2*b.iu+1;}
  top(c1,lev+1);top(c2,lev+1);
}
int main(int argc,char**argv){
  const char*mode=argv[1]; loadlib(argv[2]);
  fprintf(stderr,"nj=%d ns=%d C=%g eta=%g SQ34=%.17g\n",nj,ns,C_UP,ETA_FILE,SQ34);
  if(!strcmp(mode,"scan")){
    // scan libdir nA nR nU Alo Ahi Rlo Rhi Ulo Uhi
    int nA=atoi(argv[3]),nR=atoi(argv[4]),nU=atoi(argv[5]); double Al=atof(argv[6]),Ah=atof(argv[7]),Rl=atof(argv[8]),Rh=atof(argv[9]),Ul=atof(argv[10]),Uh=atof(argv[11]);
    double mn=1e9,mA=0,mR=0,mU=0; long feas=0,tot=0;
    for(int ia=0;ia<nA;ia++){double A=Al+(Ah-Al)*ia/(nA>1?nA-1:1);
      for(int ir=0;ir<nR;ir++){double R=Rl+(Rh-Rl)*ir/(nR>1?nR-1:1);
        for(int iu=0;iu<nU;iu++){double U=Ul+(Uh-Ul)*iu/(nU>1?nU-1:1); int64_t pi=(int64_t)llround(U*NT/4); tot++;
          int64_t bt;int bs; double sc=exclscore(A,0,R,0,pi,0,2048,&bt,&bs);
          if(sc>0)continue; feas++;
          Sol S; primal(A,R,pi,&S,0); double g=S.m-SQ34;
          if(argc>12)printf("%.6f %.6f %.6f %.8f %.6f %.6f\n",A,R,U,g,S.cx,S.cy);
          if(g<mn){mn=g;mA=A;mR=R;mU=U;}
        }}}
    printf("scan: points %ld feasible %ld min gain %.9f at A=%.6f rho=%.6f u=%.6f (phi=%.6f) solves %ld oracles %ld\n",tot,feas,mn,mA,mR,mU,mU*M_PI_2,nsolves,noracles);
    return 0;
  }
  if(!strcmp(mode,"boundary")){
    // boundary libdir nR nU Rlo Rhi Ulo Uhi : for each (rho,u) take the largest (20)-feasible A, report primal; also sweeps A below it
    int nR=atoi(argv[3]),nU=atoi(argv[4]); double Rl=atof(argv[5]),Rh=atof(argv[6]),Ul=atof(argv[7]),Uh=atof(argv[8]);
    double mn=1e9,mA=0,mR=0,mU=0;
    for(int ir=0;ir<nR;ir++){double R=Rl+(Rh-Rl)*ir/(nR>1?nR-1:1); double rowmin=1e9,rowA=0,rowU=0;
      for(int iu=0;iu<nU;iu++){double U=Ul+(Uh-Ul)*iu/(nU>1?nU-1:1); int64_t pi=(int64_t)llround(U*NT/4);
        double lo=0,hi=1; int64_t bt;int bs; if(exclscore(1.0,0,R,0,pi,0,4096,&bt,&bs)<=0){lo=1;}
        else for(int it=0;it<30;it++){double m=0.5*(lo+hi); if(exclscore(m,0,R,0,pi,0,4096,&bt,&bs)>0)hi=m; else lo=m;}
        for(int k=0;k<6;k++){ double A=lo-k*k*0.0005; if(A<0)break; Sol S; primal(A,R,pi,&S,0); double g=S.m-SQ34;
          if(g<rowmin){rowmin=g;rowA=A;rowU=U;} if(g<mn){mn=g;mA=A;mR=R;mU=U;} }
      }
      printf("rho=%.4f rowmin=%.7f A=%.6f u=%.4f\n",R,rowmin,rowA,rowU); fflush(stdout);
    }
    printf("boundary min gain %.7f at A=%.6f rho=%.6f u=%.5f\n",mn,mA,mR,mU); return 0;
  }
  // cover libdir prefix T eta cellA cellB tlim_cpu [opts: solve_every affine minlvl]
  const char*pre=argv[3]; double T=atof(argv[4]); ETA=(!strcmp(argv[5],"file"))?ETA_FILE:atof(argv[5]); cellA=atoi(argv[6]);cellB=atoi(argv[7]);TLIM=atof(argv[8]);
  if(getenv("NOQUICK"))QUICKFAIL=0; if(argc>9)SOLVE_EVERY=atoi(argv[9]); if(argc>10)AFFINE=atoi(argv[10]); if(argc>11)MINLVL=atoi(argv[11]);
  Tp=SQ34+T+2e-10;
  RHO0=floor(ETA*1048576.0)/1048576.0;
  char fn[1024];
  if(strcmp(pre,"none")){
    const char*md=(cellA==0)?"wb":"ab";
    snprintf(fn,1024,"%s.leaves",pre);fC=fopen(fn,md);snprintf(fn,1024,"%s.wits",pre);fW=fopen(fn,md);snprintf(fn,1024,"%s.progress",pre);fP=fopen(fn,md);
  }
  if(argc>12){nleaf=atoll(argv[12]);nwit=atoll(argv[13]);}
  Box root={0,0,0,0,0,0};
  top(root,0);
  fprintf(stderr,"END");
  printf("cover T=%.6f eta=%.5f cells[%d,%d) leaves %lld cert %lld excl %lld out %lld stuck %lld wits %lld solves %ld oracles %ld boxes %ld evals %ld minmargin %.3e cpu %.2f abort=%d\n",T,ETA,cellA,cellB,(long long)nleaf,(long long)ncert,(long long)nexcl,(long long)nout,(long long)nstuck,(long long)nwit,nsolves,noracles,nboxes,nevals,glob_min,(double)clock()/CLOCKS_PER_SEC,abortflag);
  return nstuck?1:0;
}
