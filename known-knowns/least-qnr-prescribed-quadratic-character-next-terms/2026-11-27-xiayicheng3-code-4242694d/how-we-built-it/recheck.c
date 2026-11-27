/* Lens independent-recheck. Different construction from the sieve-first lens:
   - modulus M2 = 8*3*5*7*11*13*17*19*23*37 (no 29, no 31; includes 37);
   - admissible residues found by a direct scan of r = 1, 9, 17, ... < M2 (no CRT);
   - per-residue loop over periods with incremental residues mod 29, 31, 41, 43;
   - then q % p for the odd primes 47..113; then a deterministic Miller-Rabin primality test (first 12 prime bases,
     valid for q < 3.18e23) and Euler's criterion p^((q-1)/2) mod q for the primes 2, 3, ... directly (no reciprocity).
   Prints "q n" for every prime q <= X, q = 1 mod 8, whose first n >= 30 primes are QRs (n counted up to 60 primes).
   Usage: recheck X outfile */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <omp.h>
typedef unsigned __int128 u128;
static uint64_t mulm(uint64_t a,uint64_t b,uint64_t m){return (uint64_t)((u128)a*b%m);}
static uint64_t powm(uint64_t b,uint64_t e,uint64_t m){uint64_t r=1;b%=m;while(e){if(e&1)r=mulm(r,b,m);b=mulm(b,b,m);e>>=1;}return r;}
static int pr[64]; static int npr=0;
static int mr(uint64_t n){ if(n<2) return 0; for(int i=0;i<12;i++){ if(n%pr[i]==0) return n==(uint64_t)pr[i]; }
  uint64_t d=n-1; int s=0; while(!(d&1)){d>>=1;s++;}
  for(int i=0;i<12;i++){ uint64_t x=powm(pr[i],d,n); if(x==1||x==n-1) continue; int c=0; for(int j=1;j<s;j++){ x=mulm(x,x,n); if(x==n-1){c=1;break;} } if(!c) return 0; }
  return 1; }
static unsigned char qr[200][200];
int main(int argc,char**argv){
  uint64_t X=strtoull(argv[1],0,10);
  for(int c=2;npr<60;c++){int ok=1;for(int d=2;d*d<=c;d++)if(c%d==0){ok=0;break;} if(ok) pr[npr++]=c;}
  for(int i=1;i<npr && pr[i]<200;i++){int p=pr[i]; for(int a=1;a<p;a++) qr[p][a*a%p]=1;}
  const int W[9]={3,5,7,11,13,17,19,23,37}; uint64_t M=8; for(int i=0;i<9;i++) M*=W[i];
  /* direct scan for admissible residues */
  size_t cap=3000000, nR=0; uint64_t *R=malloc(cap*8);
  #pragma omp parallel
  { size_t lcap=1<<16, ln=0; uint64_t *L=malloc(lcap*8);
    #pragma omp for schedule(static)
    for(uint64_t r=1;r<M;r+=8){ int ok=1; for(int i=0;i<9;i++) if(!qr[W[i]][r%W[i]]){ok=0;break;}
      if(ok){ if(ln==lcap){ lcap*=2; L=realloc(L,lcap*8);} L[ln++]=r; } }
    #pragma omp critical
    { for(size_t i=0;i<ln;i++) R[nR++]=L[i]; }
    free(L); }
  fprintf(stderr,"M2=%llu residues=%zu (expected 2566080)\n",(unsigned long long)M,nR);
  if(nR!=2566080) return 3;
  const int F[4]={29,31,41,43}; unsigned char T[4][43]; for(int f=0;f<4;f++) for(int a=0;a<F[f];a++) T[f][a]=qr[F[f]][a];
  uint64_t K=X/M+1; int dM[4]; for(int f=0;f<4;f++) dM[f]=(int)(M%F[f]);
  FILE*out=fopen(argv[2],"w"); long long hits=0;
  #pragma omp parallel for schedule(dynamic,256) reduction(+:hits)
  for(size_t i=0;i<nR;i++){
    uint64_t r=R[i]; int c0=r%29,c1=r%31,c2=r%41,c3=r%43;
    for(uint64_t k=0;k<K;k++){
      if(T[0][c0]&T[1][c1]&T[2][c2]&T[3][c3]){
        uint64_t q=r+k*M;
        if(q<=X){ int ok=1; for(int j=14;pr[j]<=113;j++){ if(!qr[pr[j]][q%pr[j]]){ok=0;break;} }  /* pr[14]=47 */
          if(ok && mr(q)){ int n=0; while(n<npr && powm(pr[n],(q-1)/2,q)==1) n++;
            if(n>=30){
              #pragma omp critical
              { fprintf(out,"%llu %d\n",(unsigned long long)q,n); }
              hits++; } } } }
      c0+=dM[0]; if(c0>=29)c0-=29; c1+=dM[1]; if(c1>=31)c1-=31; c2+=dM[2]; if(c2>=41)c2-=41; c3+=dM[3]; if(c3>=43)c3-=43;
    }
  }
  fclose(out); fprintf(stderr,"DONE primes_with_first30QR=%lld X=%llu periods=%llu\n",hits,(unsigned long long)X,(unsigned long long)K);
  return 0; }
