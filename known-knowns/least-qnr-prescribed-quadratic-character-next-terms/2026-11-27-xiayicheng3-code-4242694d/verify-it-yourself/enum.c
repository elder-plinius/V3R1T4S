/* Lens sieve-first: enumerate every q = 1 (mod 8), 1 <= q <= X, such that q mod p is a nonzero quadratic residue
   for every odd prime p <= 113. For each survivor print q and k = number of consecutive odd primes from 3 for which
   q mod p is a nonzero QR (tested up to 251). Wheel: M = 8*3*5*...*31. Filters (survivors must also pass a base-2 Fermat test): byte tables for 37,41,43,47
   (branchless), then q % p for 53..113, then k up to 251.
   Usage: wheel X outfile   (OpenMP) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
/* OpenMP pragmas only; compiles without OpenMP too (single thread). */
typedef unsigned __int128 u128;
/* Fermat base-2 test: every odd prime q satisfies 2^(q-1) = 1 mod q, so this filter never drops a prime. */
static int fermat2(uint64_t q){ uint64_t e=q-1, r=1, b=2%q; while(e){ if(e&1) r=(uint64_t)((u128)r*b%q); b=(uint64_t)((u128)b*b%q); e>>=1; } return r==1; }
static const int WP[] = {3,5,7,11,13,17,19,23,29,31};
#define NW 10
static const int FP[] = {37,41,43,47};
static int isqr[300][300]; /* isqr[p][a] = 1 iff a != 0 is a QR mod p */
static int oddp[64], nodd = 0;
static int64_t inv_mod(int64_t a, int64_t m){ int64_t g=m,x=0,x1=1,a1=a%m; if(a1<0)a1+=m; int64_t b=a1;
  /* extended Euclid */ int64_t old_r=b, r=m, old_s=1, s=0; while(r){ int64_t q=old_r/r, t=old_r-q*r; old_r=r; r=t; t=old_s-q*s; old_s=s; s=t; }
  (void)g;(void)x;(void)x1; int64_t v=old_s%m; if(v<0)v+=m; return v; }
int main(int argc, char **argv){
  if(argc<3){fprintf(stderr,"usage: wheel X outfile\n");return 1;}
  uint64_t X = strtoull(argv[1],0,10);
  for(int p=3;p<=251;p++){ int pr=1; for(int d=2;d*d<=p;d++) if(p%d==0){pr=0;break;} if(!pr) continue;
    oddp[nodd++]=p; for(int a=1;a<p;a++) isqr[p][(int)((int64_t)a*a%p)]=1; }
  /* build residues mod M by CRT */
  uint64_t M=8; uint64_t *R=malloc(sizeof(uint64_t)*1); size_t nR=1; R[0]=1;
  for(int w=0;w<NW;w++){ int p=WP[w]; size_t nq=0; for(int b=1;b<p;b++) if(isqr[p][b]) nq++;
    uint64_t *S=malloc(sizeof(uint64_t)*nR*nq); size_t n=0; int64_t im=inv_mod((int64_t)(M%p),p);
    for(size_t i=0;i<nR;i++) for(int b=1;b<p;b++) if(isqr[p][b]){
      int64_t a=(int64_t)(R[i]%p); int64_t t=((b-a)%p+p)%p; t=t*im%p; S[n++]=R[i]+M*(uint64_t)t; }
    free(R); R=S; nR=n; M*=p; }
  fprintf(stderr,"M=%llu residues=%zu\n",(unsigned long long)M,nR);
  /* sanity: every residue satisfies the conditions */
  for(size_t i=0;i<nR;i+=9973){ if(R[i]%8!=1){fprintf(stderr,"bad mod8\n");return 2;} for(int w=0;w<NW;w++) if(!isqr[WP[w]][R[i]%WP[w]]){fprintf(stderr,"bad res\n");return 2;} }
  uint8_t *rm[4]; for(int f=0;f<4;f++){ rm[f]=malloc(nR); for(size_t i=0;i<nR;i++) rm[f][i]=(uint8_t)(R[i]%FP[f]); }
  uint8_t T[4][2*48]; for(int f=0;f<4;f++){ int p=FP[f]; for(int a=0;a<2*p;a++) T[f][a]=(uint8_t)isqr[p][a%p]; }
  uint64_t K = X/M + 1; /* periods k = 0..K-1 cover [0, K*M) >= X */
  fprintf(stderr,"periods=%llu candidates~%.3e\n",(unsigned long long)K,(double)K*nR);
  FILE *out=fopen(argv[2],"w"); if(!out){perror("out");return 1;}
  const size_t CH=16384; size_t nch=(nR+CH-1)/CH; uint64_t total=0; int done=0;
  #pragma omp parallel for schedule(dynamic,1) reduction(+:total)
  for(size_t c=0;c<nch;c++){
    size_t lo=c*CH, hi=lo+CH; if(hi>nR) hi=nR;
    uint64_t found_local=0; char buf[1<<16]; size_t bl=0;
    for(uint64_t k=0;k<K;k++){
      uint64_t base=k*M; uint8_t b0=base%37,b1=base%41,b2=base%43,b3=base%47;
      const uint8_t *t0=T[0]+b0,*t1=T[1]+b1,*t2=T[2]+b2,*t3=T[3]+b3;
      for(size_t i=lo;i<hi;i++){
        if(!(t0[rm[0][i]] & t1[rm[1][i]] & t2[rm[2][i]] & t3[rm[3][i]])) continue;
        uint64_t q=base+R[i]; if(q>X) continue;
        int j, ok=1; for(j=0;oddp[j]<=113;j++){ if(oddp[j]<53) continue; if(!isqr[oddp[j]][q%oddp[j]]){ok=0;break;} }
        if(!ok) continue;
        if(!fermat2(q)) continue;
        int kk=0; while(kk<nodd && isqr[oddp[kk]][q%oddp[kk]]) kk++;
        bl+=snprintf(buf+bl,sizeof(buf)-bl,"%llu %d\n",(unsigned long long)q,kk); found_local++;
        if(bl>sizeof(buf)-64){
          #pragma omp critical
          { fwrite(buf,1,bl,out); } bl=0; }
      }
    }
    if(bl){
      #pragma omp critical
      { fwrite(buf,1,bl,out); } }
    total+=found_local;
    #pragma omp critical
    { done++; if(done%200==0){ fprintf(stderr,"progress %d/%zu chunks\n",done,nch); fflush(out);} }
  }
  fclose(out);
  fprintf(stderr,"DONE survivors=%llu X=%llu\n",(unsigned long long)total,(unsigned long long)X);
  return 0;
}
