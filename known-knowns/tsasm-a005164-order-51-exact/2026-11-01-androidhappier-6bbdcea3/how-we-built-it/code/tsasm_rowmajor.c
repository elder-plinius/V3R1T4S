/* Program A: TSASM count A005164(n) modulo a prime p, row-major transfer matrix on the reduced quadrant.
   Reduction (see NOTES.md): a TSASM of order 2n+1 <-> a symmetric n x n matrix Q over {-1,0,1} whose rows
   have all prefix sums in {0,1} and row i (0-based) sums to i mod 2.
   Sweep the upper triangle row by row. At the start of row i the state holds, for columns j=i..n-1, the bit
   "prefix sum of column j over rows 0..i-1" (bit k <-> column i+k). Bit 0 doubles as the running row sum r.
   Cell (i,i): r -> r+x in {0,1}.  Cell (i,i+k): x must keep r+x and s_k+x in {0,1}: either x=0, or (r==s_k) and
   both flip. End of row: keep r == i%2, shift right.  In-place pairwise updates; OpenMP.
   usage: tsasm_rowmajor p nmin nmax */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
static u64 P;
static inline u64 addm(u64 a,u64 b){u64 s=a+b; return s>=P? s-P: s;}
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: p nmin nmax\n");return 1;}
  P=strtoull(argv[1],0,10); int nmin=atoi(argv[2]), nmax=atoi(argv[3]);
  if(P>=(1ULL<<63)){fprintf(stderr,"p too big\n");return 1;}
  for(int n=nmin;n<=nmax;n++){
    if(n==0){printf("n=0 p=%llu a_mod_p=%llu\n",(unsigned long long)P,1ULL%P);fflush(stdout);continue;}
    size_t sz=(size_t)1<<n;
    u64*A=(u64*)calloc(sz,sizeof(u64)); if(!A){fprintf(stderr,"oom\n");return 2;}
    A[0]=1%P;                      /* before row 0 all column prefix sums are 0 */
    for(int i=0;i<n;i++){
      int m=n-i; size_t S=(size_t)1<<m;
      for(int k=0;k<m;k++){
        size_t mask = (k==0)? 1 : (((size_t)1<<k)|1);
        /* pair a (bit0=0,bitk=0) with b=a|mask (both 1); for k==0 pair bit0 only */
        #pragma omp parallel for schedule(static)
        for(size_t a=0;a<S;a++){
          if(a&mask) continue;
          size_t b=a|mask; u64 v=addm(A[a],A[b]); A[a]=v; A[b]=v;
        }
      }
      int par=i&1; size_t half=S>>1;
      /* keep bit0==par, shift right; new index t = a>>1; writes go to t<=a so forward order is safe sequentially */
      for(size_t t=0;t<half;t++) A[t]=A[(t<<1)|par];
      memset(A+half,0,(S-half)*sizeof(u64));
    }
    printf("n=%d p=%llu a_mod_p=%llu\n",n,(unsigned long long)P,(unsigned long long)A[0]); fflush(stdout);
    free(A);
  }
  return 0;
}
