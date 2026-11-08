/* check_a17.c: check_a.c (not shipped) of the N = 16 claim, carried over to the new certificate format (FORMAT.md).
 * usage: check_a17 N K M_CLAIMED counts states V [perturb|drop]
 * Regenerates every transition cell by cell from the definition in PROOF.md, looks successors up by binary search
 * in the window's block of the state list. Standard library only. Exit 0 only if all tests pass.
 * Input checks (2026-11-08): N, K and M_CLAIMED must be whole decimal integers (no trailing text), M_CLAIMED within
 * +-2^60, the optional mode exactly "perturb" or "drop"; counts and V are decoded byte by byte as little-endian, so
 * the result does not depend on the host's byte order; a window count above 2^N is rejected (h < 2^N is strictly
 * ascending within a window, so no valid window holds more). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
static unsigned char *st; static int32_t *val; static uint64_t n, *off; static int N, drop_on=0; static uint64_t drop_i=0;
static inline uint32_t ent(uint64_t i){const unsigned char*p=st+3*i;return p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16);}
static int64_t find(uint32_t b,uint32_t h){uint64_t lo=off[b],hi=off[b+1];while(lo<hi){uint64_t mid=lo+(hi-lo)/2;uint32_t x=ent(mid)&0x7fffff;if(x<h)lo=mid+1;else hi=mid;}if(lo<off[b+1]&&(ent(lo)&0x7fffff)==h&&!(drop_on&&lo==drop_i))return (int64_t)lo;return -1;}
static uint32_t row_update(uint32_t h,uint32_t b,int a){uint32_t out=0;int v=0;for(int p=0;p<N;p++){int hp=(h>>p)&1,bp=(b>>p)&1,m=(bp==a);int x=(hp||v||m)?1:0;int hout=x-v;int vout=x-hp;if(hout<0||hout>1||vout<0||vout>1){printf("REJECT cell range\n");exit(1);}out|=((uint32_t)hout)<<p;v=vout;}return out;}
static long long fsz(FILE*f){fseeko(f,0,SEEK_END);long long s=ftello(f);fseeko(f,0,SEEK_SET);return s;}
static int64_t parse_ll(const char*s,const char*what){char*end;errno=0;long long v=strtoll(s,&end,10);if(errno||*s==0||*end!=0){printf("bad %s: %s\nREJECT\n",what,s);exit(1);}return (int64_t)v;}
static inline uint32_t le32(const unsigned char*q){return (uint32_t)q[0]|((uint32_t)q[1]<<8)|((uint32_t)q[2]<<16)|((uint32_t)q[3]<<24);}
int main(int ac,char**av){if(ac<7||ac>8){printf("usage: check_a17 N K M_CLAIMED counts states V [perturb|drop]\n");return 2;}
 int64_t Narg=parse_ll(av[1],"N");int64_t K=parse_ll(av[2],"K");int64_t claimed=parse_ll(av[3],"m");
 int ctl=0;if(ac==8){if(!strcmp(av[7],"perturb"))ctl=1;else if(!strcmp(av[7],"drop"))ctl=2;else{printf("bad mode\nREJECT\n");return 2;}}
 if(K<=0||K>(1LL<<40)){printf("REJECT K\n");return 1;}
 if(claimed<-(1LL<<60)||claimed>(1LL<<60)){printf("REJECT m range\n");return 1;}
 if(Narg<1||Narg>18){printf("REJECT N range\n");return 1;}N=(int)Narg;
 uint64_t nb=1ULL<<(N-1);unsigned char*cb=malloc(nb*4);off=malloc((nb+1)*8);if(!cb||!off){printf("REJECT out of memory\n");return 1;}
 FILE*f=fopen(av[4],"rb");if(!f||fsz(f)!=(long long)(nb*4)||fread(cb,4,nb,f)!=nb){printf("REJECT counts\n");return 1;}fclose(f);
 off[0]=0;for(uint64_t b=0;b<nb;b++){uint32_t c=le32(cb+4*b);if((uint64_t)c>(1ULL<<N)){printf("REJECT count %u above 2^N at b=%llu\n",c,(unsigned long long)b);return 1;}off[b+1]=off[b]+c;}n=off[nb];free(cb);
 f=fopen(av[5],"rb");if(!f||fsz(f)!=(long long)(n*3)){printf("REJECT states size\n");return 1;}st=malloc(n*3+1);if(!st||fread(st,3,n,f)!=n){printf("REJECT read\n");return 1;}fclose(f);
 f=fopen(av[6],"rb");if(!f||fsz(f)!=(long long)(n*4)){printf("REJECT V size\n");return 1;}val=malloc(n*4+1);if(!val||fread(val,4,n,f)!=n){printf("REJECT read\n");return 1;}fclose(f);
 /* decode V in place as little-endian: entry i is read from its own four bytes before being overwritten */
 for(uint64_t i=0;i<n;i++){uint32_t u=le32((const unsigned char*)val+4*i);val[i]=(int32_t)u;}
 uint32_t mask=(1u<<N)-1;
 if(ctl==2){drop_on=1;drop_i=n/2;printf("control: dropped state index %llu\n",(unsigned long long)drop_i);}
 for(int pass=(ctl==1?0:1);pass<2;pass++){
  int64_t mn=INT64_MAX;uint64_t am=0,rows=0;int64_t vmin=INT64_MAX,vmax=INT64_MIN;
  for(uint32_t b=0;b<nb;b++){uint32_t prev=0;int first=1;for(uint64_t i=off[b];i<off[b+1];i++){if(drop_on&&i==drop_i)continue;uint32_t e=ent(i),h=e&0x7fffff;int act=(e>>23)&1;
    if(h>mask){printf("REJECT h range at %llu\n",(unsigned long long)i);return 1;}
    if(!first&&prev>=h){printf("REJECT not sorted at %llu\n",(unsigned long long)i);return 1;}prev=h;first=0;
    int64_t sum=0,rew=0;
    if(act){rows++;for(int a=0;a<2;a++){uint32_t nh=row_update(h,b,a);int64_t j=find(b,nh);if(j<0){printf("REJECT closure row: b=%u h=%u a=%d next %u missing\n",b,h,a,nh);return 1;}sum+=val[j];}}
    else{rew=h&1;for(int c=0;c<2;c++){uint32_t nh=h>>1;uint32_t nbb=(b>>1)|((uint32_t)c<<(N-1));if(nbb>>(N-1))nbb=(~nbb)&mask;int64_t j=find(nbb,nh);if(j<0){printf("REJECT closure shift: b=%u h=%u c=%d next %u missing\n",b,h,c,nh);return 1;}sum+=val[j];}}
    int64_t E=2*K*rew+sum-2*(int64_t)val[i];if(E<mn){mn=E;am=i;}
    if(val[i]<vmin)vmin=val[i];if(val[i]>vmax)vmax=val[i];}}
  if(pass==0){val[am]+=1;printf("control: V at argmin index %llu raised by 1\n",(unsigned long long)am);continue;}
  for(uint32_t b=0;b<nb;b++){if(find(b,0)<0){printf("REJECT start state b=%u missing\n",b);return 1;}}
  printf("N=%d states=%llu row_action_states=%llu K=%lld min_E=%lld Vmin=%lld Vmax=%lld\n",N,(unsigned long long)n,(unsigned long long)rows,(long long)K,(long long)mn,(long long)vmin,(long long)vmax);
  if(mn<claimed){printf("REJECT min_E %lld < claimed %lld\n",(long long)mn,(long long)claimed);return 1;}
  printf("ACCEPT claimed m=%lld, L=m/K=%lld/%lld=%.12f\n",(long long)claimed,(long long)claimed,(long long)K,(double)claimed/(double)K);return 0;}
 return 1;}
