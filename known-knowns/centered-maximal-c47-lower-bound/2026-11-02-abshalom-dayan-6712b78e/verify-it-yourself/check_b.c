// Checker B, separate code. Exact in 128-bit integers. Same certificate, read from a plain text form: bits Lx Ly n, then x y m.
// Enumerates boxes by a direct mass sum over atoms (no prefix table), sweeps along y (checker A sweeps along x), brute interval union per strip.
// Prints area numerator over 2^80 and mass numerator over 2^bits. Usage: check_b FILE REACH_NUM(over 2^bits)
#include <stdio.h>
#include <stdlib.h>
typedef __int128 I;typedef long long L;
static L Lx,Ly;static int n,b;static L *ax,*ay,*am;
static L *X,*Y,*M;static long np;
typedef struct{L x0,x1,y0,y1;}R;static R*rs;static long nr,capr=4000000;
static I isq(I v){if(v<=0)return 0;I lo=0,hi=(I)1<<62;while(hi-lo>1){I m=(lo+hi)/2;if(m*m<=v)lo=m;else hi=m;}return lo;}
static int cl(const void*p,const void*q){L a=*(L*)p,c=*(L*)q;return a<c?-1:a>c;}
static void put(L a,L c,L d,L e,L LX,L LY){L ia[2][2],ja[2][2];int ni,nj;
 if(c-a>=LX){ia[0][0]=0;ia[0][1]=LX;ni=1;}else{L s=((a%LX)+LX)%LX,t=s+c-a;if(t<=LX){ia[0][0]=s;ia[0][1]=t;ni=1;}else{ia[0][0]=s;ia[0][1]=LX;ia[1][0]=0;ia[1][1]=t-LX;ni=2;}}
 if(e-d>=LY){ja[0][0]=0;ja[0][1]=LY;nj=1;}else{L s=((d%LY)+LY)%LY,t=s+e-d;if(t<=LY){ja[0][0]=s;ja[0][1]=t;nj=1;}else{ja[0][0]=s;ja[0][1]=LY;ja[1][0]=0;ja[1][1]=t-LY;nj=2;}}
 for(int i=0;i<ni;i++)for(int j=0;j<nj;j++){if(nr>=capr){puts("too many");exit(2);}rs[nr++]=(R){ia[i][0],ia[i][1],ja[j][0],ja[j][1]};}}
static int crs(const void*p,const void*q){return __builtin_memcmp(p,q,sizeof(R));}
typedef struct{L y;int t;L a,c;}E;static int ce(const void*p,const void*q){L u=((E*)p)->y,v=((E*)q)->y;return u<v?-1:u>v;}
int main(int ac,char**av){FILE*f=fopen(av[1],"r");fscanf(f,"%d %lld %lld %d",&b,&Lx,&Ly,&n);ax=malloc(8*n);ay=malloc(8*n);am=malloc(8*n);I tot=0;for(int i=0;i<n;i++){fscanf(f,"%lld %lld %lld",&ax[i],&ay[i],&am[i]);tot+=am[i];}
 L reach=atoll(av[2]);int u=(int)(reach/Lx)+2,v=(int)(reach/Ly)+2;np=(long)n*(u+1)*(v+1);X=malloc(8*np);Y=malloc(8*np);M=malloc(8*np);long k=0;for(int i=0;i<n;i++)for(int p=0;p<=u;p++)for(int q=0;q<=v;q++){X[k]=ax[i]+p*Lx;Y[k]=ay[i]+q*Ly;M[k]=am[i];k++;}
 L*xs=malloc(8*np),*ys=malloc(8*np);for(long i=0;i<np;i++){xs[i]=X[i];ys[i]=Y[i];}qsort(xs,np,8,cl);qsort(ys,np,8,cl);long nx=0,ny=0;for(long i=0;i<np;i++){if(!nx||xs[i]!=xs[nx-1])xs[nx++]=xs[i];if(!ny||ys[i]!=ys[ny-1])ys[ny++]=ys[i];}
 rs=malloc(sizeof(R)*capr);int Rb=40;L sc=1LL<<(Rb-b);
 L*lx=malloc(8*n),*ly=malloc(8*n);for(int i=0;i<n;i++){lx[i]=ax[i];ly[i]=ay[i];}qsort(lx,n,8,cl);qsort(ly,n,8,cl);
 for(int i=0;i<n;i++){if(i&&lx[i]==lx[i-1])continue;L x1=lx[i];
  for(int j=0;j<n;j++){if(j&&ly[j]==ly[j-1])continue;L y1=ly[j];
   for(long i2=0;i2<nx;i2++){L x2=xs[i2];if(x2<x1||x2-x1>reach)continue;
    // atoms with x in [x1,x2]: filter once for this column
    static L *ty,*tm;static long cap;if(!ty){cap=np;ty=malloc(8*cap);tm=malloc(8*cap);}long nt=0;for(long q=0;q<np;q++)if(X[q]>=x1&&X[q]<=x2&&Y[q]>=y1&&Y[q]-y1<=reach){ty[nt]=Y[q];tm[nt]=M[q];nt++;}
    for(long j2=0;j2<ny;j2++){L y2=ys[j2];if(y2<y1||y2-y1>reach)continue;I m=0;for(long q=0;q<nt;q++)if(ty[q]<=y2)m+=tm[q];if(m<=0)continue;
     L dx=x2-x1,dy=y2-y1,e=dx>dy?dx:dy;if((I)e*e>(m<<b))continue;I rad=m<<(2*Rb-b-2);L rho=(L)isq(rad);
     L a=x2*sc-rho,c=x1*sc+rho,d=y2*sc-rho,g=y1*sc+rho;if(c>a&&g>d)put(a,c,d,g,Lx*sc,Ly*sc);
 }}}}
 qsort(rs,nr,sizeof(R),crs);long w=0;for(long i=0;i<nr;i++)if(!w||crs(&rs[i],&rs[w-1]))rs[w++]=rs[i];nr=w;
 E*ev=malloc(sizeof(E)*2*nr);for(long i=0;i<nr;i++){ev[2*i]=(E){rs[i].y0,1,rs[i].x0,rs[i].x1};ev[2*i+1]=(E){rs[i].y1,-1,rs[i].x0,rs[i].x1};}qsort(ev,2*nr,sizeof(E),ce);
 // strip sweep: y strips, active list, interval union by sorting active intervals
 typedef struct{L a,c;}Iv;Iv*act=malloc(sizeof(Iv)*(nr+1));long na=0;I area=0;L prev=0;int have=0;
 static int (*cmpiv)(const void*,const void*);
 for(long i=0;i<2*nr;){L y=ev[i].y;if(have&&y>prev){qsort(act,na,sizeof(Iv),cl);I cov=0;L e=-(1LL<<62);for(long q=0;q<na;q++){if(act[q].a>e){cov+=act[q].c-act[q].a;e=act[q].c;}else if(act[q].c>e){cov+=act[q].c-e;e=act[q].c;}}area+=cov*(y-prev);}
  while(i<2*nr&&ev[i].y==y){if(ev[i].t>0){act[na].a=ev[i].a;act[na].c=ev[i].c;na++;}else{for(long q=0;q<na;q++)if(act[q].a==ev[i].a&&act[q].c==ev[i].c){act[q]=act[--na];break;}}i++;}
  prev=y;have=1;}
 char s[64];int l=0;I t=area;if(!t)s[l++]='0';while(t){s[l++]='0'+(int)(t%10);t/=10;}printf("pieces=%ld area_num=",nr);while(l)putchar(s[--l]);printf(" (over 2^80) mass_num=%lld (over 2^%d)\n",(L)tot,b);
 printf("value=%.12Lf\n",(long double)area/((long double)1208925819614629174706176.0L)/((long double)tot/(long double)(1LL<<b)));return 0;}
