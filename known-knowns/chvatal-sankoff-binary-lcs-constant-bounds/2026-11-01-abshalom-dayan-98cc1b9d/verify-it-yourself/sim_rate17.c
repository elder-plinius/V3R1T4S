/* sim_rate17.c: Monte Carlo of the certificate policy, frontier cell by cell, to cross-check the certified rate (NUMERICAL, not evidence for the bound).
   usage: sim_rate17 N counts states steps seed */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static unsigned char*st;static uint64_t*off;
static inline uint32_t ent(uint64_t i){unsigned char*p=st+3*i;return p[0]|(p[1]<<8)|((uint32_t)p[2]<<16);}
static int look(uint32_t b,uint32_t h){uint64_t lo=off[b],hi=off[b+1];while(lo<hi){uint64_t m=lo+(hi-lo)/2;if((ent(m)&0x7fffff)<h)lo=m+1;else hi=m;}if(lo>=off[b+1]||(ent(lo)&0x7fffff)!=h){printf("state missing\n");exit(1);}return ent(lo)>>23;}
static uint64_t z;static inline uint64_t rn(){z^=z<<13;z^=z>>7;z^=z<<17;return z;}
int main(int c,char**v){int N=atoi(v[1]);uint64_t nb=1ULL<<(N-1);off=malloc((nb+1)*8);uint32_t*cn=malloc(nb*4);FILE*f=fopen(v[2],"rb");if(fread(cn,4,nb,f)!=nb)return 1;fclose(f);off[0]=0;for(uint64_t i=0;i<nb;i++)off[i+1]=off[i]+cn[i];st=malloc(off[nb]*3);f=fopen(v[3],"rb");if(fread(st,3,off[nb],f)!=off[nb])return 1;fclose(f);long long T=atoll(v[4]);z=88172645463325252ULL^(uint64_t)atoll(v[5]);uint32_t mask=(1u<<N)-1,h=0,b=(uint32_t)(rn()>>20)&mask;long long R=0,rows=0;
 for(long long t=0;t<T;t++){uint32_t bb=b;if(bb>>(N-1))bb=~bb&mask;int act=look(bb,h);if(act){int a=(rn()>>31)&1;uint32_t o=0;int vv=0;for(int p=0;p<N;p++){int hp=(h>>p)&1,m=((b>>p)&1)==a,x=hp|vv|m;o|=(uint32_t)(x-vv)<<p;vv=x-hp;}h=o;rows++;}else{R+=h&1;h>>=1;b=(b>>1)|((uint32_t)((rn()>>31)&1)<<(N-1));}}
 printf("N=%d T=%lld reward=%lld rows=%lld 2R/T=%.6f rowfrac=%.5f\n",N,T,R,rows,2.0*R/T,(double)rows/T);return 0;}
