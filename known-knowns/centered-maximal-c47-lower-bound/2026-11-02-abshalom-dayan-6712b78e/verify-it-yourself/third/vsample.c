// Monte Carlo test: M mu(x)>=1 decided exactly per point. Test only, not evidence.
#include "common.h"
#include <math.h>
typedef struct { i64 d,m; } DM;
static int cmpd(const void*a,const void*b){i64 x=((DM*)a)->d,y=((DM*)b)->d;return x<y?-1:x>y;}
static uint64_t st; static uint64_t next(void){uint64_t z=(st+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
static i64 unif(i64 L){ uint64_t mask=1; while(mask<(uint64_t)L) mask<<=1; mask-=1; for(;;){uint64_t v=next()&mask; if(v<(uint64_t)L) return (i64)v;} }
int main(int ac,char**av){
  if(ac<4) die("usage: vsample file N seed");
  parse(av[1]); long N=atol(av[2]); st=strtoull(av[3],0,10);
  int shift=bits+2*KBITS; i64 Sraw=tail_side_raw(),SU=Sraw<<KBITS; i64 hw=SU/2+1;
  size_t c=0,cap=(size_t)n*8192; Atom*im=malloc(sizeof(Atom)*cap); DM*w=malloc(sizeof(DM)*cap);
  for(int i=0;i<n;i++){ for(i64 p=-40;p<=40;p++){ i64 x=(A[i].x<<KBITS)+p*LX; if(x<-hw||x>LX+hw) continue;
    for(i64 q=-40;q<=40;q++){ i64 y=(A[i].y<<KBITS)+q*LY; if(y<-hw||y>LY+hw) continue; if(c>=cap)die("cap"); im[c++]=(Atom){x,y,A[i].m}; } } }
  long hit=0; size_t maxused=0;
  for(long t=0;t<N;t++){ i64 x=unif(LX),y=unif(LY); size_t m=0;
    for(size_t i=0;i<c;i++){ i64 dx=iabs64(im[i].x-x),dy=iabs64(im[i].y-y),d=dx>dy?dx:dy; if(d<=hw){w[m].d=d;w[m].m=im[i].m;m++;} }
    if(m>maxused) maxused=m;
    qsort(w,m,sizeof(DM),cmpd);
    i64 W=0; int cv=0;
    for(size_t k=0;k<m;k++){ W+=w[k].m; if(((u128)(uint64_t)W<<shift)>=(u128)(uint64_t)(2*w[k].d)*(u128)(uint64_t)(2*w[k].d)){cv=1;break;} }
    hit+=cv;
  }
  // display only: floats are used only in this statistical test
  double p=(double)hit/N; double ar=((double)Lx/ldexp(1,bits))*((double)Ly/ldexp(1,bits)), mu=(double)Mtot/ldexp(1,bits);
  printf("N %ld seed %s hits %ld images_listed %zu max_images_used %zu tail_S_raw %lld fraction %.8f V_est %.8f SE %.8f\n",N,av[3],hit,c,maxused,(long long)Sraw,p,p*ar/mu,sqrt(p*(1-p)/N)*ar/mu);
  return 0;
}
