// Three-body exponential-basis engine (GMP multiprecision). See gen.py for the definitions.
// usage: engine basis.txt eig SIGMA NITER [vecfile]   |   engine basis.txt count SIGMA
#include <gmpxx.h>
#include <dispatch/dispatch.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>
struct C { mpf_class re, im; C(){} C(const mpf_class&r):re(r),im(0){} C(const mpf_class&r,const mpf_class&i):re(r),im(i){} };
static inline C operator+(const C&x,const C&y){return C(x.re+y.re,x.im+y.im);}
static inline C operator-(const C&x,const C&y){return C(x.re-y.re,x.im-y.im);}
static inline C operator-(const C&x){return C(-x.re,-x.im);}
static inline C operator*(const C&x,const C&y){return C(x.re*y.re-x.im*y.im,x.re*y.im+x.im*y.re);}
static inline C operator*(long k,const C&x){return C(k*x.re,k*x.im);}
static inline C operator*(const C&x,long k){return C(k*x.re,k*x.im);}
#include "elems_L1.h"
#include "elems_L2.h"
struct Fn { int type; mpf_class ar,ai,br,bi,cr,ci; };
static int L, kappa=0, N, NT=6; static mp_bitcnt_t prec=384;
static mpf_class W1,W2,W3,Q13,Q23,Q12; static std::vector<Fn> F; static bool cplx=false;
static mpf_class parse_ratio(const std::string&s){ if(s=="inf") return mpf_class(0,prec); size_t p=s.find('/'); if(p==std::string::npos) return mpf_class(s,prec,10);
  mpf_class n(s.substr(0,p),prec,10), d(s.substr(p+1),prec,10); return n/d; }
static void exch(const Fn&f, Fn&o, int&sgn){ o=f; std::swap(o.ar,o.br); std::swap(o.ai,o.bi); sgn=1;
  if(L==1){ if(f.type==0) o.type=1; else if(f.type==1) o.type=0; else sgn=-1; }
  else { if(f.type==0) o.type=2; else if(f.type==2) o.type=0; } }
// bilinear element between primitive functions; conjb: conjugate the bra parameters
template<class T> static void elemT(int tb,int tk,const T&a,const T&b,const T&c,const T&d,const T&e,const T&g,T&S,T&H){
  T one(mpf_class(1,prec)); (void)one; T u,wq,v; }
static void inv(const C&z, C&o){ mpf_class n=z.re*z.re+z.im*z.im; o.re=z.re/n; o.im=-z.im/n; }
static void prim(const Fn&x,bool conj,const Fn&y,mpf_class&S,mpf_class&H){
  if(!cplx){ mpf_class A=x.ar+y.ar,B=x.br+y.br,Cc=x.cr+y.cr; mpf_class u=1/(A+B),wq=1/(A+Cc),v=1/(B+Cc);
    if(sgn(A+B)<=0||sgn(A+Cc)<=0||sgn(B+Cc)<=0){fprintf(stderr,"non-integrable pair\n");exit(2);}
    if(L==1) el_L1<mpf_class>(x.type,y.type,x.ar,x.br,x.cr,y.ar,y.br,y.cr,u,wq,v,W1,W2,W3,Q13,Q23,Q12,S,H);
    else el_L2<mpf_class>(x.type,y.type,x.ar,x.br,x.cr,y.ar,y.br,y.cr,u,wq,v,W1,W2,W3,Q13,Q23,Q12,S,H); return; }
  C a(x.ar,conj?mpf_class(-x.ai):x.ai),b(x.br,conj?mpf_class(-x.bi):x.bi),c(x.cr,conj?mpf_class(-x.ci):x.ci);
  C d(y.ar,y.ai),e(y.br,y.bi),g(y.cr,y.ci); C AB=a+d+b+e, AC=a+d+c+g, BC=b+e+c+g, u,wq,v;
  if(sgn(AB.re)<=0||sgn(AC.re)<=0||sgn(BC.re)<=0){fprintf(stderr,"non-integrable pair\n");exit(2);}
  inv(AB,u); inv(AC,wq); inv(BC,v); C Sc,Hc; C w1(W1),w2(W2),w3(W3),q13(Q13),q23(Q23),q12(Q12);
  if(L==1) el_L1<C>(x.type,y.type,a,b,c,d,e,g,u,wq,v,w1,w2,w3,q13,q23,q12,Sc,Hc);
  else el_L2<C>(x.type,y.type,a,b,c,d,e,g,u,wq,v,w1,w2,w3,q13,q23,q12,Sc,Hc);
  S=Sc.re; H=Hc.re; }
static void realel(const Fn&x,const Fn&y,mpf_class&S,mpf_class&H){ // <Re phi_x | Re phi_y>
  if(!cplx){ prim(x,false,y,S,H); return; }
  mpf_class s1,h1,s2,h2; prim(x,false,y,s1,h1); prim(x,true,y,s2,h2); S=(s1+s2)/2; H=(h1+h2)/2; }
static void element(int i,int j,mpf_class&S,mpf_class&H){ realel(F[i],F[j],S,H);
  if(kappa){ Fn o; int sg; exch(F[j],o,sg); mpf_class s2,h2; realel(F[i],o,s2,h2); int k=kappa*sg; S+=k*s2; H+=k*h2; } }
static std::vector<mpf_class> Sm,Hm,Am; static inline size_t ix(int i,int j){ return (size_t)i*(i+1)/2+j; } // j<=i
static void build(){ Sm.resize(ix(N,0)); Hm.resize(ix(N,0));
  dispatch_apply(NT, dispatch_get_global_queue(QOS_CLASS_UTILITY,0), ^(size_t t){
    for(int i=(int)t;i<N;i+=NT) for(int j=0;j<=i;j++){ mpf_class s,h; element(i,j,s,h); Sm[ix(i,j)]=s; Hm[ix(i,j)]=h; } }); }
static int ldl(const mpf_class&sigma){ Am.resize(ix(N,0)); for(size_t k=0;k<Am.size();k++) Am[k]=Hm[k]-sigma*Sm[k];
  int neg=0; std::vector<mpf_class> lc(N);
  for(int k=0;k<N;k++){ const mpf_class d=Am[ix(k,k)]; if(sgn(d)<0) neg++; if(sgn(d)==0){fprintf(stderr,"zero pivot\n");exit(3);}
    int m=N-k-1; if(m<=0) break; int nt=(m>96)?NT:1; mpf_class*lcp=lc.data(); const mpf_class*dp=&d;
    dispatch_apply(nt, dispatch_get_global_queue(QOS_CLASS_UTILITY,0), ^(size_t t){ mpf_t tmp; mpf_init2(tmp,prec);
      for(int i=N-1-(int)t;i>k;i-=nt){ mpf_class li=Am[ix(i,k)]/(*dp); mpf_class*row=&Am[ix(i,0)];
        for(int j=k+1;j<=i;j++){ mpf_mul(tmp,li.get_mpf_t(),Am[ix(j,k)].get_mpf_t()); mpf_sub(row[j].get_mpf_t(),row[j].get_mpf_t(),tmp); }
        lcp[i]=li; }
      mpf_clear(tmp); });
    for(int i=k+1;i<N;i++) Am[ix(i,k)]=lc[i]; }
  return neg; }
static void solve(std::vector<mpf_class>&z){ for(int i=0;i<N;i++){ mpf_class s=z[i]; for(int j=0;j<i;j++) s-=Am[ix(i,j)]*z[j]; z[i]=s; }
  for(int i=0;i<N;i++) z[i]/=Am[ix(i,i)];
  for(int i=N-1;i>=0;i--){ mpf_class s=z[i]; for(int j=i+1;j<N;j++) s-=Am[ix(j,i)]*z[j]; z[i]=s; } }
static void matvec(const std::vector<mpf_class>&M,const std::vector<mpf_class>&x,std::vector<mpf_class>&y){
  for(int i=0;i<N;i++){ mpf_class s(0,prec); for(int j=0;j<N;j++) s+=M[i>=j?ix(i,j):ix(j,i)]*x[j]; y[i]=s; } }
static mpf_class dotp(const std::vector<mpf_class>&x,const std::vector<mpf_class>&y){ mpf_class s(0,prec); for(int i=0;i<N;i++) s+=x[i]*y[i]; return s; }
int main(int argc,char**argv){ if(argc<4){fprintf(stderr,"usage\n");return 1;}
  if(getenv("NT")) NT=atoi(getenv("NT")); std::ifstream in(argv[1]); std::string key; std::string m1,m2,m3; int q1=1,q2=1,q3=-1;
  std::vector<std::vector<std::string>> rows;
  while(in>>key){ if(key=="L") in>>L; else if(key=="prec"){ unsigned long p; in>>p; prec=p; } else if(key=="masses") in>>m1>>m2>>m3;
    else if(key=="charges") in>>q1>>q2>>q3; else if(key=="sym") in>>kappa; else if(key=="N"){ in>>N; break; } }
  mpf_set_default_prec(prec);
  mpf_class M1=parse_ratio(m1),M2=parse_ratio(m2),M3=parse_ratio(m3); mpf_class one(1,prec);
  mpf_class I1(0,prec),I2(0,prec),I3(0,prec); if(m1!="inf") I1=one/M1; if(m2!="inf") I2=one/M2; if(m3!="inf") I3=one/M3;
  W1.set_prec(prec);W2.set_prec(prec);W3.set_prec(prec);Q13.set_prec(prec);Q23.set_prec(prec);Q12.set_prec(prec);
  W1=I1+I3; W2=I2+I3; W3=I3;
  Q13=q1*q3; Q23=q2*q3; Q12=q1*q2; F.resize(N);
  for(int i=0;i<N;i++){ std::string a,ai,b,bi,c,ci; in>>F[i].type>>a>>ai>>b>>bi>>c>>ci;
    F[i].ar=mpf_class(a,prec,10);F[i].ai=mpf_class(ai,prec,10);F[i].br=mpf_class(b,prec,10);F[i].bi=mpf_class(bi,prec,10);F[i].cr=mpf_class(c,prec,10);F[i].ci=mpf_class(ci,prec,10);
    if(sgn(F[i].ai)!=0||sgn(F[i].bi)!=0||sgn(F[i].ci)!=0) cplx=true; }
  build(); std::string mode=argv[2]; mpf_class sigma(argv[3],prec,10); int neg=ldl(sigma);
  gmp_printf("N %d prec %lu cplx %d sigma %.30Ff roots_below_sigma %d\n",N,(unsigned long)prec,(int)cplx,sigma.get_mpf_t(),neg);
  if(mode=="count") return 0;
  int niter=argc>4?atoi(argv[4]):8; std::vector<mpf_class> vv(N),w(N),hv(N); unsigned long seed=12345;
  for(int i=0;i<N;i++){ seed=seed*6364136223846793005UL+1442695040888963407UL; vv[i]=mpf_class((double)((seed>>33)%1000003)/1000003.0-0.5,prec); }
  mpf_class rho;
  for(int it=0;it<niter;it++){ matvec(Sm,vv,w); solve(w); vv=w; matvec(Sm,vv,w); matvec(Hm,vv,hv); mpf_class n=dotp(vv,w); rho=dotp(vv,hv)/n;
    mpf_class sn=sqrt(n); for(int i=0;i<N;i++) vv[i]/=sn; gmp_printf("iter %d E %.45Ff\n",it,rho.get_mpf_t()); }
  if(argc>5){ FILE*f=fopen(argv[5],"w"); for(int i=0;i<N;i++) gmp_fprintf(f,"%.*Fe\n",(int)(prec*0.30103),vv[i].get_mpf_t()); fclose(f); }
  return 0; }
