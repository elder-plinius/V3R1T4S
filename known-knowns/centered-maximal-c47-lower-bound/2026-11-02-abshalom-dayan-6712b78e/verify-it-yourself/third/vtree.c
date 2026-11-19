// Adaptive dyadic quadtree from the definition: rigorous covered / uncovered tests, exact integers only.
#include "common.h"
typedef struct { i64 x,y,m,d; } It;
#define MAXD 40
static It *L[MAXD+2]; static size_t Lcap;
static int shift,maxdepth,K; static u128 cov[MAXD+2],unc[MAXD+2],total; static unsigned long long nodes,unk_nodes,listwork;
static inline u128 clip(i64 x0,i64 y0,i64 s){ i64 x1=x0+s,y1=y0+s; if(x1>LX)x1=LX; if(y1>LY)y1=LY; if(x0>=x1||y0>=y1) return 0; return (u128)(uint64_t)(x1-x0)*(u128)(uint64_t)(y1-y0); }
/* Node D=[x0,x0+s]x[y0,y0+s], centre c. pn items of parent's list. S0: for ALL x in D and ALL S>=S0: mu(Q(x,S/2))<S^2. */
static void rec(int dep,i64 x0,i64 y0,i64 s,size_t pn,i64 S0){
  u128 a=clip(x0,y0,s); if(!a) return; nodes++;
  i64 cx=x0+s/2,cy=y0+s/2; It*p=L[dep],*q=L[dep+1]; size_t m=0; i64 lim=(S0+s)/2+1;
  for(size_t i=0;i<pn;i++){ i64 dx=iabs64(p[i].x-cx),dy=iabs64(p[i].y-cy),d=dx>dy?dx:dy; if(d>lim) continue;
    size_t j=m++; while(j>0&&q[j-1].d>d){q[j]=q[j-1];j--;} q[j]=p[i]; q[j].d=d; }
  listwork+=m;
  i64 W=0; size_t lastfail=(size_t)-1; int any=0;
  for(size_t k=0;k<m;k++){ W+=q[k].m; i64 d=q[k].d; u128 v=((u128)(uint64_t)W)<<shift;
    i64 Sc=2*d+s; // COVERED: all atoms with d_i<=d lie in every Q(x,Sc/2), x in D. fixed r=Sc/2.
    if(Sc<S0 && v>=(u128)Sc*(u128)Sc){ cov[dep]+=a; return; }
    i64 Su=2*d-s; // UNCOVERED sup on piece S in [Su, next): mu(Q(x,S/2)) <= W_k, worst S=Su.
    if(Su<S0){ if(Su<=0||v>=(u128)Su*(u128)Su){lastfail=k;any=1;} }
  }
  if(!any){ unc[dep]+=a; return; }
  if(dep>=maxdepth){ unk_nodes++; return; }
  i64 S1=S0; // after last failing index the test passes for every later piece, so children may stop at its S
  if(lastfail+1<m){ i64 Sn=2*q[lastfail+1].d-s; if(Sn<S1) S1=Sn; }
  i64 h=s/2;
  rec(dep+1,x0,y0,h,m,S1); rec(dep+1,x0+h,y0,h,m,S1); rec(dep+1,x0,y0+h,h,m,S1); rec(dep+1,x0+h,y0+h,h,m,S1);
}
int main(int ac,char**av){
  if(ac<3) die("usage: vtree file maxdepth");
  parse(av[1]); maxdepth=atoi(av[2]); if(maxdepth>MAXD) die("depth");
  shift=bits+2*KBITS; i64 Sraw=tail_side_raw(),SU=Sraw<<KBITS;
  K=0; while((1LL<<K)<LX||(1LL<<K)<LY) K++; i64 R=1LL<<K;
  if(K-maxdepth<2) die("resolution finer than unit");
  // image list: everything with distance <= (S*+R)/2+1 from root centre (R/2,R/2)
  i64 lim=(SU+R)/2+2; size_t c=0;
  for(int pass=0;pass<2;pass++){ c=0;
    for(int i=0;i<n;i++){ i64 ax=A[i].x<<KBITS,ay=A[i].y<<KBITS;
      i64 p0=-(lim+R)/LX-1,p1=(lim+R)/LX+1,q0=-(lim+R)/LY-1,q1=(lim+R)/LY+1;
      for(i64 p=p0;p<=p1;p++) for(i64 q=q0;q<=q1;q++){ i64 x=ax+p*LX,y=ay+q*LY;
        if(iabs64(x-R/2)<=lim&&iabs64(y-R/2)<=lim){ if(pass){L[0][c]=(It){x,y,A[i].m,0};} c++; } } }
    if(!pass){ Lcap=c+8; for(int d=0;d<MAXD+2;d++){L[d]=malloc(sizeof(It)*Lcap); if(!L[d])die("oom");} }
  }
  total=(u128)LX*(u128)LY;
  rec(0,0,0,R,c,SU);
  printf("bits %d kbits %d Lx %lld Ly %lld M %lld n %d K %d maxdepth %d images %zu tail_S_raw %lld nodes %llu unknown_leaves %llu listwork %llu\n",
     bits,KBITS,(long long)Lx,(long long)Ly,(long long)Mtot,n,K,maxdepth,c,(long long)Sraw,nodes,unk_nodes,listwork);
  u128 C=0,N=0;
  for(int d=0;d<=maxdepth;d++){ C+=cov[d];N+=unc[d]; printf("depth %d side_log2_U %d cumcov_U2 ",d,K-d);pr128(stdout,C);printf(" cumunc_U2 ");pr128(stdout,N);printf("\n"); }
  printf("total_U2 ");pr128(stdout,total);printf("\n");
  return 0;
}
