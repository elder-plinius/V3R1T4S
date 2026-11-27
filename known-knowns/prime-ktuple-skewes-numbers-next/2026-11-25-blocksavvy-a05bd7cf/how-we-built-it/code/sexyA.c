/* sexyA: segmented sieve on 6k+1 / 6k+5 bitsets. Sexy pair (n,n+6) <-> bits k,k+1 of the same class.
   Block j covers n in [j*B, (j+1)*B), B = 6*S.  For each block, outputs:
     cnt  = number of pair starts n in block,
     M    = max over pairs (in increasing n, rank i=1..cnt) of (i - slope*(n - a)),  slope=(L[j+1]-L[j])/B
     ckc  = for a checkpoint c inside the block (from list), number of pair starts <= c (else -1)
   L[] = lower bounds of C*Li2 at block boundaries (binary doubles), read from file.
   usage: sexyA nblocks Lfile outfile nthreads [checkpoints...] */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
#define S (1u<<21)
#define W (S/64)
typedef uint64_t u64; typedef uint32_t u32;
static u64 nblocks; static double *L; static u32 *P; static u32 *R1,*R5; static int np;
static u64 *pat1,*pat5; static u64 PW; /* presieve 5..17 */
static int nck; static u64 ck[64]; static int64_t ckres[64]; static u64 ckblk[64];
typedef struct { u32 cnt; double M; int64_t ckc; } rec;
static rec *out; static u64 nextchunk=0; static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
#define CHUNK 32
static u64 modinv(u64 a,u64 m){ int64_t t=0,nt=1,r=m,nr=a%m; while(nr){int64_t q=r/nr,x;x=t-q*nt;t=nt;nt=x;x=r-q*nr;r=nr;nr=x;} if(t<0)t+=m; return t;}
static void build_pattern(void){
  u64 per=5*7*11*13*17; PW=per; /* words: pattern of per*64 bits = per words */
  pat1=malloc(PW*8); pat5=malloc(PW*8); memset(pat1,0xff,PW*8); memset(pat5,0xff,PW*8);
  int sp[5]={5,7,11,13,17};
  for(int a=0;a<5;a++){u64 p=sp[a]; u64 inv=modinv(6%p,p);
    u64 r1=(p - (1*inv)%p)%p, r5=(p-(5*inv)%p)%p; /* k == -r*inv6 */
    for(u64 k=r1;k<PW*64;k+=p) pat1[k>>6]&=~(1ull<<(k&63));
    for(u64 k=r5;k<PW*64;k+=p) pat5[k>>6]&=~(1ull<<(k&63)); }
}
static void *worker(void *arg){
  u64 *b1=malloc((W+1)*8),*b5=malloc((W+1)*8);
  u32 *o1=malloc(np*4),*o5=malloc(np*4);
  for(;;){
    pthread_mutex_lock(&mu); u64 c0=nextchunk; nextchunk+=CHUNK; pthread_mutex_unlock(&mu);
    if(c0>=nblocks) break;
    u64 c1=c0+CHUNK; if(c1>nblocks)c1=nblocks;
    u64 K0=c0*(u64)S;
    for(int i=0;i<np;i++){ u64 p=P[i];
      /* first k>=K0 with residue, and n>=p*p */
      u64 kmin1=(p*p-1)/6; /* p^2 = 1 mod 6 */
      u64 base= K0>kmin1?K0:kmin1; u64 k=base+((R1[i]+p-(base%p))%p); o1[i]=(u32)(k-K0); /* may exceed S*CHUNK; fits u32 since K0 offset small? handled below */
      if(k-K0>0xffffffffull) o1[i]=0xffffffffu;
      u64 kmin5=(p*p+4*p-5)/6; /* smallest multiple of p in class 5 that is >= p^2 is at most p(p+4)?  use n>=p*p: kmin5=ceil((p*p-5)/6)*/
      kmin5=(p*p>=5)?((p*p-5)+5)/6:0;
      base= K0>kmin5?K0:kmin5; k=base+((R5[i]+p-(base%p))%p);
      o5[i]=(k-K0>0xffffffffull)?0xffffffffu:(u32)(k-K0);
    }
    for(u64 j=c0;j<c1;j++){
      u64 Kb=j*(u64)S;
      /* presieve copy: word index of bit Kb is Kb/64 (S multiple of 64) */
      u64 w0=(Kb/64)%PW;
      for(u64 w=0;w<=W;w++){ u64 q=(w0+w)%PW; b1[w]=pat1[q]; b5[w]=pat5[q]; }
      if(Kb==0){ /* n=1 not prime; restore 5,7,11,13,17 */
        b1[0]&=~1ull; b5[0]|=1ull<<0; /*5*/ b1[0]|=1ull<<1; /*7*/ b5[0]|=1ull<<1; /*11*/ b1[0]|=1ull<<2; /*13*/ b5[0]|=1ull<<2; /*17*/ }
      u64 lim=S+64; /* sieve bits 0..S+63 of this segment (extra word for k+1) */
      for(int i=0;i<np;i++){ u32 p=P[i];
        u64 o=o1[i]; if(o!=0xffffffffu){ for(;o<lim;o+=p) b1[o>>6]&=~(1ull<<(o&63)); }
        u64 q=o5[i]; if(q!=0xffffffffu){ for(;q<lim;q+=p) b5[q>>6]&=~(1ull<<(q&63)); }
        /* advance to next segment: offsets relative to Kb+S */
        if(o1[i]!=0xffffffffu){ u64 x=o1[i]; if(x<S){ x = x + ((S - x + p -1)/p)*p; } o1[i]=(u32)(x-S);} 
        if(o5[i]!=0xffffffffu){ u64 x=o5[i]; if(x<S){ x = x + ((S - x + p -1)/p)*p; } o5[i]=(u32)(x-S);} 
      }
      /* pairs */
      double a=(double)(j*6ull*S); double slope=(L[j+1]-L[j])/(6.0*S);
      u32 cnt=0; double M=-1e300; int64_t ckc=-1; u64 lo=j*6ull*S, hi=(j+1)*6ull*S; int hasck=0; int ckin[64]; int nin=0; u32 cb[64];
      for(int t=0;t<nck;t++) if(ck[t]>=lo && ck[t]<hi){ckin[nin]=t;cb[nin]=0;nin++;hasck=1;}
      for(u64 w=0;w<W;w++){
        u64 m1=b1[w]&((b1[w]>>1)|(b1[w+1]<<63));
        u64 m5=b5[w]&((b5[w]>>1)|(b5[w+1]<<63));
        u64 m=m1|m5;
        while(m){ int bt=__builtin_ctzll(m); m&=m-1; u64 k=Kb+w*64+bt;
          if((m1>>bt)&1){ u64 n=6*k+1; cnt++; double v=cnt-slope*((double)n-a); if(v>M)M=v; if(hasck){for(int z=0;z<nin;z++) if(n<=ck[ckin[z]]) cb[z]=cnt;} }
          if((m5>>bt)&1){ u64 n=6*k+5; cnt++; double v=cnt-slope*((double)n-a); if(v>M)M=v; if(hasck){for(int z=0;z<nin;z++) if(n<=ck[ckin[z]]) cb[z]=cnt;} }
        }
      }
      if(hasck){ ckc=nin; for(int z=0;z<nin;z++){ckres[ckin[z]]=cb[z]; ckblk[ckin[z]]=j;} }
      out[j].cnt=cnt; out[j].M=M; out[j].ckc=ckc;
    }
  }
  free(b1);free(b5);free(o1);free(o5); return NULL;
}
int main(int argc,char**argv){
  nblocks=strtoull(argv[1],0,10); const char*Lf=argv[2]; const char*of=argv[3]; int nt=atoi(argv[4]);
  nck=argc-5; for(int i=0;i<nck;i++) ck[i]=strtoull(argv[5+i],0,10);
  L=malloc((nblocks+1)*8); FILE*f=fopen(Lf,"rb"); if(fread(L,8,nblocks+1,f)!=nblocks+1){fprintf(stderr,"Lfile short\n");return 1;} fclose(f);
  u64 nmax=nblocks*6ull*S+6*64+12; u64 sq=(u64)sqrtl((long double)nmax)+2;
  char*s=calloc(sq+1,1); np=0; P=malloc(sizeof(u32)*(sq/2+10)); R1=malloc(sizeof(u32)*(sq/2+10)); R5=malloc(sizeof(u32)*(sq/2+10));
  for(u64 i=2;i<=sq;i++) if(!s[i]){ for(u64 j=i*i;j<=sq;j+=i) s[j]=1; if(i>=19){ P[np]=i; u64 inv=modinv(6%i,i); R1[np]=(i-(1*inv)%i)%i; R5[np]=(i-(5*inv)%i)%i; np++; } }
  build_pattern();
  out=calloc(nblocks,sizeof(rec));
  pthread_t th[64]; for(int i=0;i<nt;i++) pthread_create(&th[i],0,worker,0); for(int i=0;i<nt;i++) pthread_join(th[i],0);
  FILE*g=fopen(of,"wb"); for(u64 j=0;j<nblocks;j++){ fwrite(&out[j].cnt,4,1,g); fwrite(&out[j].M,8,1,g); fwrite(&out[j].ckc,8,1,g);} fclose(g);
  for(int t=0;t<nck;t++) printf("ck %llu block %llu inblock %lld\n",(unsigned long long)ck[t],(unsigned long long)ckblk[t],(long long)ckres[t]);
  u64 tot=0; for(u64 j=0;j<nblocks;j++) tot+=out[j].cnt; printf("blocks=%llu B=%llu total_pairs=%llu np=%d\n",(unsigned long long)nblocks,(unsigned long long)(6ull*S),(unsigned long long)tot,np);
  return 0;
}
