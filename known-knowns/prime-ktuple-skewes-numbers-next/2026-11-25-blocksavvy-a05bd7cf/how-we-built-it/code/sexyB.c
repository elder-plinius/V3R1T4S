/* sexyB: independent recount. Odd-only bitset (bit i <-> n=2i+1, 1 = composite), plain segmented
   Eratosthenes with every odd prime 3..sqrt, no wheel/presieve. Pair (n,n+6) <-> bits i, i+3 both clear.
   Mode count:  sexyB count NEND nthreads outfile   -> uint32 count of pair starts n in [s*65536,(s+1)*65536) for every sub-block s < NEND/65536
   Mode dump:   sexyB dump A Bnd                    -> prints every pair start n in [A,Bnd)  (A, Bnd multiples of 2) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
typedef uint64_t u64; typedef uint32_t u32; typedef uint8_t u8;
#define SUB 65536ull            /* n-length of a sub-block */
#define SEGN (SUB*128ull)       /* n-length of a segment = 8388608 */
#define SEGB (SEGN/2)           /* odd bits per segment */
static u32 *pr; static long npr; static u64 nend, nsub; static u32 *res; static u64 nextseg=0; static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
static void primes_upto(u64 lim){ u8*s=calloc(lim+1,1); pr=malloc(sizeof(u32)*(lim/2+16)); npr=0;
  for(u64 i=3;i<=lim;i+=2){ if(!s[i]){ pr[npr++]=(u32)i; for(u64 j=i*i;j<=lim;j+=2*i) s[j]=1; } } free(s); }
/* sieve odd numbers in [lo, lo+2*nb) (lo odd) into bitmap bm (nb bits, +pad) */
static void sieve_seg(u64 lo, u64 nb, u64 *bm){
  memset(bm,0,((nb+127)/64)*8);
  u64 hi=lo+2*nb;
  for(long t=0;t<npr;t++){ u64 p=pr[t]; if(p*p>=hi) break;
    u64 m=p*p; if(m<lo){ m=((lo+p-1)/p)*p; if(!(m&1)) m+=p; }
    for(u64 i=(m-lo)/2;i<nb;i+=p) bm[i>>6]|=1ull<<(i&63);
  }
  if(lo==1) bm[0]|=1ull; /* n=1 */
}
static void *worker(void*arg){
  u64 nb=SEGB+64; u64 *bm=malloc(((nb+127)/64)*8);
  for(;;){ pthread_mutex_lock(&mu); u64 sg=nextseg++; pthread_mutex_unlock(&mu);
    u64 n0=sg*SEGN; if(n0>=nend) break;
    sieve_seg(n0+1,nb,bm);  /* bit i <-> n0+1+2i */
    for(u64 q=0;q<SEGN/SUB;q++){ u64 sb=n0/SUB+q; if(sb>=nsub) break; u32 c=0;
      for(u64 i=q*(SUB/2); i<(q+1)*(SUB/2); i++){
        if(!((bm[i>>6]>>(i&63))&1) && !((bm[(i+3)>>6]>>((i+3)&63))&1)){ u64 n=n0+1+2*i; if(n>=5) c++; }
      }
      res[sb]=c; }
  }
  free(bm); return 0; }
int main(int argc,char**argv){
  if(!strcmp(argv[1],"count")){
    nend=strtoull(argv[2],0,10); int nt=atoi(argv[3]); nsub=nend/SUB;
    u64 lim=(u64)sqrtl((long double)(nend+SEGN+16))+2; primes_upto(lim);
    res=calloc(nsub,4); pthread_t th[64]; for(int i=0;i<nt;i++) pthread_create(&th[i],0,worker,0); for(int i=0;i<nt;i++) pthread_join(th[i],0);
    FILE*f=fopen(argv[4],"wb"); fwrite(res,4,nsub,f); fclose(f); u64 tot=0; for(u64 i=0;i<nsub;i++) tot+=res[i];
    printf("nend=%llu subblocks=%llu total_pairs=%llu nprimes=%ld\n",(unsigned long long)nend,(unsigned long long)nsub,(unsigned long long)tot,npr); return 0; }
  if(!strcmp(argv[1],"dump")){
    u64 A=strtoull(argv[2],0,10), Bn=strtoull(argv[3],0,10); u64 lim=(u64)sqrtl((long double)(Bn+16))+2; primes_upto(lim);
    u64 lo=A+1, nb=(Bn-A)/2+8; u64*bm=malloc(((nb+127)/64)*8); sieve_seg(lo,nb,bm);
    for(u64 i=0;i<(Bn-A)/2;i++) if(!((bm[i>>6]>>(i&63))&1)&&!((bm[(i+3)>>6]>>((i+3)&63))&1)){u64 n=lo+2*i; if(n>=5) printf("%llu\n",(unsigned long long)n);} return 0; }
  return 1; }
