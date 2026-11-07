// Shared parsing and exact integer helpers. No floating point here.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef __int128 i128; typedef unsigned __int128 u128; typedef int64_t i64;
#define KBITS 16  /* working unit U = 2^-(bits+KBITS) */
typedef struct { i64 x,y,m; } Atom;
static int bits; static i64 Lx,Ly; static int n; static Atom *A; static i64 Mtot;
static i64 LX,LY; /* cell in units U */
static void die(const char*s){fprintf(stderr,"FATAL %s\n",s);exit(2);}
static void parse(const char*fn){
  FILE*f=fopen(fn,"r"); if(!f) die("open");
  long long a,b,c; int bb,nn;
  if(fscanf(f,"%d %lld %lld %d",&bb,&a,&b,&nn)!=4) die("header");
  bits=bb;Lx=a;Ly=b;n=nn;A=malloc(sizeof(Atom)*n);Mtot=0;
  for(int i=0;i<n;i++){ if(fscanf(f,"%lld %lld %lld",&a,&b,&c)!=3) die("row");
    if(a<0||a>=Lx||b<0||b>=Ly||c<=0) die("atom outside cell or nonpositive mass");
    A[i].x=a;A[i].y=b;A[i].m=c;Mtot+=c; }
  fclose(f);
  if(bits+KBITS>=62||Lx>=(1LL<<46)||Ly>=(1LL<<46)) die("range");
  LX=Lx<<KBITS; LY=Ly<<KBITS;
}
static void pr128(FILE*f,u128 v){ char b[64];int i=63;b[i]=0; if(!v)b[--i]='0'; while(v){b[--i]='0'+(int)(v%10);v/=10;} fputs(b+i,f); }
// 128x128 -> 256 bit compare, a*b < c*d
static void mul256(u128 a,u128 b,u128*hi,u128*lo){
  uint64_t a0=(uint64_t)a,a1=(uint64_t)(a>>64),b0=(uint64_t)b,b1=(uint64_t)(b>>64);
  u128 p00=(u128)a0*b0,p01=(u128)a0*b1,p10=(u128)a1*b0,p11=(u128)a1*b1;
  u128 mid=(p00>>64)+(uint64_t)p01+(uint64_t)p10;
  *lo=(mid<<64)|(uint64_t)p00;
  *hi=p11+(p01>>64)+(p10>>64)+(mid>>64);
}
static int mul_lt(u128 a,u128 b,u128 c,u128 d){u128 h1,l1,h2,l2;mul256(a,b,&h1,&l1);mul256(c,d,&h2,&l2);return h1<h2||(h1==h2&&l1<l2);}
/* TAIL BOUND. For a closed interval of length S, an atom's images (period L) inside number <= floor(S/L)+1.
   So mu(Q) <= Mtot (S/Lx+1)(S/Ly+1) for ANY centre, and mu(Q)<S^2 whenever
   f(S)=Mtot (1/Lx+1/S)(1/Ly+1/S) < 1; f is strictly decreasing in S, so this holds for ALL S>=S*.
   Raw units 2^-bits: Mtot 2^bits (S+Lx)(S+Ly) < S^2 Lx Ly. Returns smallest such integer S* (raw). */
static i64 tail_side_raw(void){
  u128 M2=((u128)(uint64_t)Mtot)<<bits; u128 LL=(u128)Lx*(u128)Ly;
  if(!mul_lt(M2,(u128)1,LL,(u128)1)) die("density >= 1: tail bound unavailable");
  i64 lo=0,hi=1; // invariant: fail at lo, success at hi
  for(;;){ u128 s=hi; if(mul_lt(M2,(s+Lx)*(s+Ly),s*s,LL)) break; hi*=2; if(hi>(1LL<<52)) die("tail too large"); }
  while(hi-lo>1){ i64 mid=lo+(hi-lo)/2; u128 s=mid; if(mul_lt(M2,(s+Lx)*(s+Ly),s*s,LL)) hi=mid; else lo=mid; }
  return hi;
}
static u128 isqrt128(u128 v){ // exact floor sqrt, bit by bit
  u128 r=0, bit=((u128)1)<<126; while(bit>v) bit>>=2;
  while(bit){ if(v>=r+bit){v-=r+bit;r=(r>>1)+bit;} else r>>=1; bit>>=2; } return r;
}
static inline i64 iabs64(i64 v){return v<0?-v:v;}
