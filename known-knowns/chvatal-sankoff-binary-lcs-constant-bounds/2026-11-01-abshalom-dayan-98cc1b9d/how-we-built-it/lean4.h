// lean4.h: shared code of prod4.c. Sparse two-level state set: index of 2^(2N-1-9) slots, 64-byte chunks, one dirty byte per chunk.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <sys/resource.h>
#include <sys/mman.h>
typedef uint64_t u64; typedef uint32_t u32; typedef int32_t i32; typedef int64_t i64;
static int N; static u64 MN;
static const i64 K=1LL<<24;
static inline u64 canon(u64 h,u64 b){ if((b>>(N-1))&1) b=(~b)&MN; return h|(b<<N);}
static inline u64 rowst(u64 s,int a){u64 h=s&MN,b=s>>N;u64 M_=a?b:(~b&MN);u64 U=(~h)&MN;u64 Un=((U+(U&M_))|(U&~M_))&MN;return ((~Un)&MN)|(b<<N);}
static inline u64 shf(u64 s,int c,int*r){u64 h=s&MN,b=s>>N;*r=h&1;h>>=1;b=(b>>1)|((u64)c<<(N-1));return canon(h,b);}
static double now(){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+1e-9*t.tv_nsec;}
// big arrays come straight from mmap: zero-filled, untouched pages not resident, memory returned at once on free (malloc's cache of freed large blocks stays resident on macOS)
static void*xalloc(u64 bytes){u64 t=bytes+16384;char*p=mmap(NULL,t,PROT_READ|PROT_WRITE,MAP_ANON|MAP_PRIVATE,-1,0);if(p==MAP_FAILED){printf("mmap fail\n");exit(8);}*(u64*)p=t;return p+16384;}
static void xfree(void*q){if(!q)return;char*p=(char*)q-16384;munmap(p,*(u64*)p);}
#define CW 8
#define CBITS 9
typedef struct{u32*idx;u64*pool;unsigned char*dirty;u32*pre;u64 slots,nch,cnt;}Set;
static u64 memcap=0;
static double maxrss_mb(void){struct rusage u;getrusage(RUSAGE_SELF,&u);return u.ru_maxrss/1e6;}
static void memcheck(const char*w){if(!memcap)return;struct rusage u;getrusage(RUSAGE_SELF,&u);if((u64)u.ru_maxrss>memcap){printf("MEMCAP exceeded at %s: maxrss=%llu cap=%llu\n",w,(unsigned long long)u.ru_maxrss,(unsigned long long)memcap);fflush(stdout);exit(9);}}
static void set_init(Set*S,u64 bits){S->slots=bits>>CBITS;S->idx=xalloc(S->slots*4);S->pool=xalloc(S->slots*CW*8);S->dirty=xalloc(S->slots);S->pre=NULL;S->nch=0;S->cnt=0;if(!S->idx||!S->pool||!S->dirty){printf("alloc fail\n");exit(8);}}
static inline int set_has(const Set*S,u64 x){u32 id=S->idx[x>>CBITS];if(!id)return 0;return (S->pool[(u64)(id-1)*CW+((x>>6)&(CW-1))]>>(x&63))&1;}
static inline void set_add(Set*S,u64 x){u32 id=S->idx[x>>CBITS];if(!id){id=(u32)++S->nch;S->idx[x>>CBITS]=id;if((S->nch&0xfffff)==0)memcheck("set_add");}u64 w=(u64)(id-1)*CW+((x>>6)&(CW-1));u64 m=1ULL<<(x&63);if(!(S->pool[w]&m)){S->pool[w]|=m;S->dirty[id-1]=1;}}
static void set_build(Set*S){if(S->dirty){xfree(S->dirty);S->dirty=NULL;}S->pre=xalloc(S->nch*4+4);u64 c=0;for(u64 sl=0;sl<S->slots;sl++){u32 id=S->idx[sl];if(!id)continue;S->pre[id-1]=(u32)c;const u64*p=S->pool+(u64)(id-1)*CW;for(int w=0;w<CW;w++)c+=__builtin_popcountll(p[w]);}S->cnt=c;}
static inline u64 set_rank(const Set*S,u64 x){u32 id=S->idx[x>>CBITS];const u64*p=S->pool+(u64)(id-1)*CW;int w=(x>>6)&(CW-1);u64 c=S->pre[id-1];for(int i=0;i<w;i++)c+=__builtin_popcountll(p[i]);return c+__builtin_popcountll(p[w]&((1ULL<<(x&63))-1));}
static void set_free(Set*S){xfree(S->idx);xfree(S->pool);xfree(S->dirty);xfree(S->pre);S->idx=NULL;S->pool=NULL;S->dirty=NULL;S->pre=NULL;}
#define SET_FOR(S,s,...) do{for(u64 _sl=0;_sl<(S)->slots;_sl++){u32 _id=(S)->idx[_sl];if(!_id)continue;const u64*_p=(S)->pool+(u64)(_id-1)*CW;for(int _w=0;_w<CW;_w++){u64 _x=_p[_w];while(_x){int _t=__builtin_ctzll(_x);_x&=_x-1;u64 s=(_sl<<CBITS)|((u64)_w<<6)|_t;__VA_ARGS__}}}}while(0)
#define PBIT(p,i) (((p)[(i)>>3]>>((i)&7))&1)
// spill: exact i32 array on disk in pieces of 2^27 items (537 MB each), random access through one 64k-item buffer
#define SP_ITEMS (1ULL<<27)
static FILE*spf[32];static int spn=0;static char sppre[1024];static i32 spbuf[1<<16];static u64 sp0=1,sp1=0;
static void sp_write(const char*pre,const i32*A,u64 n){strcpy(sppre,pre);spn=0;for(u64 o=0;o<n||o==0;o+=SP_ITEMS){char fn[1100];snprintf(fn,sizeof fn,"%s.sp%d",pre,spn);FILE*f=fopen(fn,"wb");u64 c=n-o<SP_ITEMS?n-o:SP_ITEMS;if(fwrite(A+o,4,c,f)!=c){printf("spill write fail\n");exit(6);}fclose(f);spn++;if(n==0)break;}for(int i=0;i<spn;i++){char fn[1100];snprintf(fn,sizeof fn,"%s.sp%d",pre,i);spf[i]=fopen(fn,"rb");}sp0=1;sp1=0;}
static inline i32 sp_get(u64 id){if(id<sp0||id>=sp1){int p=(int)(id/SP_ITEMS);u64 lo=id%SP_ITEMS;fseeko(spf[p],(off_t)lo*4,SEEK_SET);size_t g=fread(spbuf,4,1<<16,spf[p]);sp0=id;sp1=id+g;}return spbuf[id-sp0];}
static void sp_close(void){for(int i=0;i<spn;i++){char fn[1100];snprintf(fn,sizeof fn,"%s.sp%d",sppre,i);fclose(spf[i]);remove(fn);}spn=0;}
static void write_cert(const char*pre,const Set*S,const unsigned char*pol,const i32*V,u64 n,int newfmt){char fn[1024];
 if(!newfmt){snprintf(fn,sizeof fn,"%s.states",pre);FILE*a=fopen(fn,"wb");setvbuf(a,NULL,_IOFBF,1<<20);u64 i=0;SET_FOR(S,s,u32 e=(u32)s;if(PBIT(pol,i))e|=0x80000000u;fwrite(&e,4,1,a);i++;);fclose(a);}
 else{u64 nb=1ULL<<(N-1);u32*cn=calloc(nb,4);snprintf(fn,sizeof fn,"%s.states",pre);FILE*a=fopen(fn,"wb");setvbuf(a,NULL,_IOFBF,1<<20);u64 i=0;SET_FOR(S,s,u32 h=(u32)(s&MN);u64 b=s>>N;if(b>=nb){printf("noncanonical\n");exit(7);}cn[b]++;u32 e=h|((PBIT(pol,i)?1u:0u)<<23);unsigned char t0=(unsigned char)e,t1=(unsigned char)(e>>8),t2=(unsigned char)(e>>16);putc(t0,a);putc(t1,a);putc(t2,a);i++;);fclose(a);snprintf(fn,sizeof fn,"%s.counts",pre);a=fopen(fn,"wb");fwrite(cn,4,nb,a);fclose(a);free(cn);}
 snprintf(fn,sizeof fn,"%s.V",pre);FILE*c=fopen(fn,"wb");fwrite(V,4,n,c);fclose(c);}
