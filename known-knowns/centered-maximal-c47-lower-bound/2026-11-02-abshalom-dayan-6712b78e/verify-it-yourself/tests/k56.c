// K5 and K6: pointwise test of the rectangle union against the definition, and finite-block ratio. Exact integers (coordinates over 2^40).
// Usage: k56 CERT.txt RADIUS_int MODE N SAMPLES SEED [RECTS]
// MODE 5: uniform points of the cell, periodic atoms out to |.|_inf <= RADIUS. Reports in_S, M>=1, violations (in S but M<1), missed (M>=1, not in S).
// MODE 6: N x N block of cells, no other atoms. Uniform points of the block widened by 2 cells each side. Reports ratio = hits*region/(N^2 mass).
// RADIUS must be a valid tail radius: no square of half-side above RADIUS can reach average 1 (shown separately for the periodic measure; for a finite block a sub-measure of it has the same bound).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long L; typedef __int128 I;
static uint64_t s; static uint64_t nx(void){uint64_t z=(s+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
static L ur(L n){return (L)(((unsigned __int128)nx()*(unsigned __int128)n)>>64);} 
typedef struct{L d;L m;}P; static int cp(const void*a,const void*b){L x=((P*)a)->d,y=((P*)b)->d;return x<y?-1:x>y;}
int main(int c,char**v){int b,n;L Lx,Ly;FILE*f=fopen(v[1],"r");fscanf(f,"%d %lld %lld %d",&b,&Lx,&Ly,&n);L*X=malloc(8*n),*Y=malloc(8*n),*Mm=malloc(8*n);L sc=1LL<<(40-b),tot=0;for(int i=0;i<n;i++){fscanf(f,"%lld %lld %lld",&X[i],&Y[i],&Mm[i]);X[i]*=sc;Y[i]*=sc;tot+=Mm[i];}Lx*=sc;Ly*=sc;
 L Rad=atoll(v[2])*(1LL<<40);int mode=atoi(v[3]);int N=atoi(v[4]);long S=atol(v[5]);s=atoll(v[6]);
 long nr=0;L*R=0;if(mode==5){FILE*g=fopen(v[7],"r");fscanf(g,"%ld",&nr);R=malloc(32*nr);for(long i=0;i<4*nr;i++)fscanf(g,"%lld",&R[i]);}
 long cap=1<<20;P*pl=malloc(sizeof(P)*cap);
 long hit=0,ins=0,viol=0,miss=0;
 for(long t=0;t<S;t++){L x,y;if(mode==5){x=ur(Lx);y=ur(Ly);}else{x=ur((N+4)*Lx)-2*Lx;y=ur((N+4)*Ly)-2*Ly;}
  long np=0;L fi=(x-Rad)/Lx-2,li=(x+Rad)/Lx+2,fj=(y-Rad)/Ly-2,lj=(y+Rad)/Ly+2;
  for(L i=fi;i<=li;i++){if(mode==6&&(i<0||i>=N))continue;for(L j=fj;j<=lj;j++){if(mode==6&&(j<0||j>=N))continue;L ox=i*Lx-x,oy=j*Ly-y;
    if(ox>Rad+Lx||ox<-Rad-Lx||oy>Rad+Ly||oy<-Rad-Ly)continue;
    for(int a=0;a<n;a++){L dx=X[a]+ox,dy=Y[a]+oy;if(dx<0)dx=-dx;if(dy<0)dy=-dy;L d=dx>dy?dx:dy;if(d>Rad)continue;if(np==cap){cap*=2;pl=realloc(pl,sizeof(P)*cap);}pl[np].d=d;pl[np].m=Mm[a];np++;}}}
  qsort(pl,np,sizeof(P),cp);I W=0;int in=0;for(long k=0;k<np;){L d=pl[k].d;while(k<np&&pl[k].d==d){W+=pl[k].m;k++;}
    // W/2^b >= (2 d/2^40)^2 iff W*2^(80-b) >= 4 d^2
    if((W<<(80-b))>=(I)4*(I)d*(I)d){in=1;break;}}
  hit+=in;
  if(mode==5){int cl=0;for(long r=0;r<nr&&!cl;r++){L a=R[4*r],bb=R[4*r+1],cc=R[4*r+2],dd=R[4*r+3];L wx=(x-a)%Lx;if(wx<0)wx+=Lx;L wy=(y-cc)%Ly;if(wy<0)wy+=Ly;if(wx<=bb-a&&wy<=dd-cc)cl=1;}
   ins+=cl;if(cl&&!in)viol++;if(!cl&&in)miss++;}
 }
 if(mode==5)printf("samples=%ld M_ge_1=%ld in_S=%ld violations=%ld missed=%ld\n",S,hit,ins,viol,miss);
 else{double reg=(double)(N+4)*(N+4)*((double)Lx/(1LL<<40))*((double)Ly/(1LL<<40));double mass=N*N*((double)tot/(1LL<<b));double p=(double)hit/S;printf("N=%d samples=%ld hits=%ld ratio=%.6f se=%.6f\n",N,S,hit,p*reg/mass,reg/mass*__builtin_sqrt(p*(1-p)/S));}
 return 0;}
