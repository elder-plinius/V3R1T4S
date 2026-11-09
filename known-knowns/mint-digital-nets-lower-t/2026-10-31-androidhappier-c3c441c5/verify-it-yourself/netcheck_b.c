/* Checker B (independent of netcheck.py): digital (t,m,s)-net check over F_q, q prime or q=4.
   F_4 elements a+b*w (w^2=w+1) coded as a+2b. Reads the same text format (lines '#' ignored, s blocks of rows
   of m digits separated by blank lines). Enumerates every composition (d_1..d_s) of k=m-t into s parts in
   lexicographic order with an odometer and performs incremental Gaussian elimination: rows of block i are
   pushed onto an echelon basis kept per recursion level, so each composition costs at most k row reductions.
   Usage: netcheck_b FILE q m s t */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int q,m,s,t,k; static int ADD[16][16],MUL[16][16],INV[16],NEG[16];
static unsigned char C[64][32][32]; static int nrows[64];
static long long ncomp=0, nbad=0;
static void setup(void){
  for(int a=0;a<q;a++)for(int b=0;b<q;b++){
    if(q==4){ int a0=a&1,a1=a>>1,b0=b&1,b1=b>>1; ADD[a][b]=a^b;
      int c0=(a0&b0)^(a1&b1), c1=(a0&b1)^(a1&b0)^(a1&b1); MUL[a][b]=c0|(c1<<1);}
    else { ADD[a][b]=(a+b)%q; MUL[a][b]=(a*b)%q; } }
  for(int a=0;a<q;a++){ for(int b=0;b<q;b++){ if(MUL[a][b]==1) INV[a]=b; if(ADD[a][b]==0) NEG[a]=b; } }
}
/* basis[level] : echelon rows with pivot positions; reduce v against basis, return 1 if independent and add */
typedef struct { unsigned char r[32][32]; int piv[32]; int n; } Basis;
static Basis stack[40];
static int push(Basis *B, const unsigned char *v){
  unsigned char w[32]; memcpy(w,v,m);
  for(int i=0;i<B->n;i++){ int p=B->piv[i]; if(w[p]){ int f=NEG[w[p]]; for(int c=0;c<m;c++) w[c]=ADD[w[c]][MUL[f][B->r[i][c]]]; } }
  int p=-1; for(int c=0;c<m;c++) if(w[c]){p=c;break;}
  if(p<0) return 0;
  int iv=INV[w[p]]; for(int c=0;c<m;c++) w[c]=MUL[iv][w[c]];
  memcpy(B->r[B->n],w,m); B->piv[B->n]=p; B->n++; return 1;
}
/* rec over blocks: level = rows used so far */
static int dfs(int blk,int remaining,int lvl){
  if(blk==s-1){ /* last block takes all remaining */
    if(remaining>nrows[blk]) { nbad++; return 0; }
    Basis B=stack[lvl];
    for(int r=0;r<remaining;r++) if(!push(&B,C[blk][r])){ ncomp++; nbad++; return 0; }
    ncomp++; return 1; }
  int ok=1;
  /* d_blk = 0..remaining */
  stack[lvl+1]=stack[lvl]; int depth=0; int indep=1;
  for(int d=0; d<=remaining; d++){
    if(d>0){ if(d>nrows[blk]){ nbad++; return 0; }
      Basis *B=&stack[lvl+1]; if(indep && !push(B,C[blk][d-1])) indep=0; }
    if(!indep){ /* every composition with this prefix fails; count them as bad */ nbad++; return 0; }
    if(!dfs(blk+1,remaining-d,lvl+1)) ok=0;
    if(!ok) return 0;
    depth=d;
  }
  (void)depth; return ok;
}
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage\n");return 2;}
  FILE*f=fopen(argv[1],"r"); q=atoi(argv[2]); m=atoi(argv[3]); s=atoi(argv[4]); t=atoi(argv[5]); k=m-t;
  if(!(q==2||q==3||q==5||q==7||q==4)){fprintf(stderr,"q unsupported\n");return 2;}
  setup();
  char line[256]; int blk=0,inblk=0;
  while(fgets(line,sizeof line,f)){
    if(line[0]=='#') continue;
    int L=strlen(line); while(L&&(line[L-1]=='\n'||line[L-1]=='\r'||line[L-1]==' ')) line[--L]=0;
    if(L==0){ if(inblk){blk++; inblk=0;} continue; }
    if(L!=m){fprintf(stderr,"bad row length\n");return 2;}
    for(int c=0;c<m;c++){ int v=line[c]-'0'; if(v<0||v>=q){fprintf(stderr,"bad symbol\n");return 2;} C[blk][nrows[blk]][c]=v; }
    nrows[blk]++; inblk=1;
  }
  if(inblk) blk++;
  if(blk!=s){fprintf(stderr,"found %d blocks, expected %d\n",blk,s);return 2;}
  stack[0].n=0;
  int ok=dfs(0,k,0);
  printf("%s q=%d m=%d s=%d t=%d k=%d compositions_reached=%lld\n", ok?"PASS":"FAIL",q,m,s,t,k,ncomp);
  return ok?0:1;
}
