/* Program B: TSASM count A005164(n), column-major sweep of the upper triangle of the reduced quadrant Q
   (symmetric n x n over {-1,0,1}, every row has prefix sums in {0,1}, row i sums to i mod 2; see NOTES.md).
   Different sweep order and state encoding from Program A:
   processing column j top to bottom, the state is (R_0..R_{j-1}, c): R_i = prefix sum of row i over columns
   0..j-1 (row i's entries left of the diagonal are Q[k][i], k<i, i.e. column i above the diagonal), c = running
   sum of column j over rows 0..i-1. Bit layout: bit i = R_i (i<j), bit j = c. Growing state (2^(j+1)).
   Cell (i,j), i<j: x with R_i+x and c+x in {0,1}.  Cell (j,j): c -> c+x in {0,1}; c then *becomes* R_j (bit j),
   and the next column's c starts at 0 in bit j+1.  At the end, the answer is the entry with R_i = i mod 2.
   Arithmetic: unsigned __int128 wraparound, i.e. exact modulo 2^128 (only additions, so the final entry is a(n) mod 2^128;
   equal to a(n) whenever a(n) < 2^128) (mode "exact"), or modulo a prime p (mode p; -DSTORE64 stores 64-bit cells).
   Overwrite-free formulation: explicit new/old arrays (no in-place pairing), to differ from Program A.
   usage: tsasm_colmajor exact|<p> nmin nmax */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
#ifdef STORE64
typedef uint64_t cell;
#else
typedef unsigned __int128 cell;
#endif
static int exact; static u128 P; static volatile int overflow=0;
static inline u128 add(u128 a,u128 b){ u128 s=a+b; if(exact){ if(s<a) overflow=1; return s;} return s>=P? s-P: s; }
static void pr(u128 v,char*buf){ char t[64]; int k=0; if(!v){strcpy(buf,"0");return;} while(v){t[k++]='0'+(int)(v%10); v/=10;} for(int i=0;i<k;i++) buf[i]=t[k-1-i]; buf[k]=0; }
int main(int argc,char**argv){
  if(argc<4) return 1;
  exact=!strcmp(argv[1],"exact"); if(!exact) P=(u128)strtoull(argv[1],0,10);
  int nmin=atoi(argv[2]), nmax=atoi(argv[3]);
  for(int n=nmin;n<=nmax;n++){
    if(n==0){ if(exact) printf("n=0 mode=wrap2^128 value_mod_2^128=1\n"); else printf("n=0 p=%s a_mod_p=1\n",argv[1]); continue; }
    size_t sz=(size_t)1<<n;
    overflow=0;
    if(exact && sizeof(cell)!=16){fprintf(stderr,"exact mode needs 128-bit storage\n");return 3;}
    cell *O=calloc(sz,sizeof(cell)), *N=calloc(sz,sizeof(cell));
    if(!O||!N){fprintf(stderr,"oom\n");return 2;}
    O[0]=1; /* column 0, before any cell: no rows, c=0 */
    for(int j=0;j<n;j++){
      size_t S=(size_t)1<<(j+1); size_t cb=(size_t)1<<j;   /* c lives in bit j */
      for(int i=0;i<j;i++){
        size_t rb=(size_t)1<<i;
        /* pull formulation: each target t gathers from its sources (no write races) */
        #pragma omp parallel for schedule(static)
        for(size_t t=0;t<S;t++){
          int r2=(t&rb)!=0, c2=(t&cb)!=0; u128 acc=0;
          for(int x=-1;x<=1;x++){
            int r=r2-x,c=c2-x; if(r<0||r>1||c<0||c>1) continue;
            size_t s=(t&~(rb|cb)) | (r?rb:0) | (c?cb:0);
            acc=add(acc,O[s]);
          }
          N[t]=acc;
        }
        cell*T=O;O=N;N=T;
      }
      /* diagonal cell (j,j): c -> c+x in {0,1}; result stays in bit j as R_j */
      memset(N,0,S*sizeof(cell));
      for(size_t s=0;s<S;s++){
        cell v=O[s]; if(!v) continue;
        int c=(s&cb)!=0;
        for(int x=-1;x<=1;x++){ int c2=c+x; if(c2<0||c2>1) continue;
          size_t t=(s&~cb)|(c2?cb:0); N[t]=add(N[t],v); }
      }
      cell*T=O;O=N;N=T;
      /* bit j+1 (next column's c) is 0: array indices >= S are already 0 in O? clear them */
      if(j+1<n) memset(O+S,0,S*sizeof(cell));
    }
    size_t target=0; for(int i=0;i<n;i++) if(i&1) target|=(size_t)1<<i;
    char buf[64]; pr(O[target],buf);
    if(exact) printf("n=%d mode=wrap2^128 value_mod_2^128=%s%s\n",n,buf,overflow?" (intermediate wraparound occurred; result is exact mod 2^128)":"");
    else printf("n=%d p=%s a_mod_p=%s\n",n,argv[1],buf); fflush(stdout);
    free(O);free(N);
  }
  return 0;
}
