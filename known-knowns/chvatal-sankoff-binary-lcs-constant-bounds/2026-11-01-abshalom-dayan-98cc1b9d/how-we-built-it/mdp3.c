// Full value iteration on canonical states of window M; dumps int16 V*2048. usage: mdp3 M maxit tol outfile cap_s
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef uint64_t u64;
static int N;static u64 MN;
static inline u64 canon(u64 h,u64 b){if((b>>(N-1))&1)b=(~b)&MN;return h|(b<<N);}
static inline u64 rowst(u64 s,int a){u64 h=s&MN,b=s>>N;u64 M_=a?b:(~b&MN);u64 U=(~h)&MN;u64 Un=((U+(U&M_))|(U&~M_))&MN;return ((~Un)&MN)|(b<<N);}
static inline u64 shf(u64 s,int c,int*r){u64 h=s&MN,b=s>>N;*r=h&1;h>>=1;b=(b>>1)|((u64)c<<(N-1));return canon(h,b);}
static double now(){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+1e-9*t.tv_nsec;}
int main(int ac,char**av){N=atoi(av[1]);int its=atoi(av[2]);double tol=atof(av[3]);double cap=atof(av[5]);MN=(1ULL<<N)-1;u64 n=1ULL<<(2*N-1);float*V=calloc(n,4),*W=malloc(n*4);double t0=now();double lo=0,hi=0;
 for(int it=0;it<its;it++){lo=1e9;hi=-1e9;for(u64 s=0;s<n;s++){float A=0.5f*(V[rowst(s,0)]+V[rowst(s,1)]);int r;u64 x0=shf(s,0,&r),x1=shf(s,1,&r);float B=0.5f*(V[x0]+V[x1])+r;float T=A>B?A:B;double d=T-V[s];if(d<lo)lo=d;if(d>hi)hi=d;W[s]=V[s]+0.5f*(T-V[s]);}
  float base=W[0];for(u64 s=0;s<n;s++)V[s]=W[s]-base;
  if(it%10==0){printf("it %d rho [%.6f,%.6f] t=%.1f\n",it,lo,hi,now()-t0);fflush(stdout);}
  if(hi-lo<tol||now()-t0>cap)break;}
 printf("M=%d rho in [%.7f,%.7f] gamma>=[%.7f,%.7f] t=%.1f\n",N,lo,hi,2*lo,2*hi,now()-t0);
 float mn=1e30,mx=-1e30;for(u64 s=0;s<n;s++){if(V[s]<mn)mn=V[s];if(V[s]>mx)mx=V[s];}printf("V range %.4f %.4f\n",mn,mx);
 int16_t*Q=malloc(n*2);for(u64 s=0;s<n;s++){Q[s]=(int16_t)(V[s]*2048.0f);}FILE*f=fopen(av[4],"wb");fwrite(Q,2,n,f);fclose(f);return 0;}
