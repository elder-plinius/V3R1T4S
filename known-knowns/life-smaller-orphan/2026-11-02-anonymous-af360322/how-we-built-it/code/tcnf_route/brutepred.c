/* brutepred h w BM SM modelfile: reads T from a SAT model (var 1+r*w+j), searches for a predecessor by
   backtracking over the (h+2)x(w+2) grid in column-major order, checking each target cell when its 3x3 block is filled.
   Independent of tcnf (no transfer table). Prints HAS_PREDECESSOR or NO_PREDECESSOR. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int h,w,H,W,BM,SM,T[16][16],G[16][16];
int ok(int r,int c){int n=0;for(int dr=-1;dr<=1;dr++)for(int dc=-1;dc<=1;dc++)if(dr||dc)n+=G[r+dr][c+dc];
 int nx=G[r][c]?(SM>>n)&1:(BM>>n)&1; return nx==T[r-1][c-1];}
int rec(int k){ if(k==H*W) return 1; int c=k/H,r=k%H;
 for(int b=0;b<2;b++){G[r][c]=b; int good=1;
  /* cell (r,c) completes target (r-1,c-1) when r>=2... target (tr,tc) with tr+1==r && tc+1==c, needs all of rows tr-1..tr+1, cols tc-1..tc+1 */
  int tr=r-1,tc=c-1; if(tr>=1&&tr<=h&&tc>=1&&tc<=w) good=ok(tr,tc);
  if(good && r==H-1){ /* nothing extra */ }
  if(good&&rec(k+1))return 1;}
 return 0;}
int main(int a,char**v){h=atoi(v[1]);w=atoi(v[2]);BM=atoi(v[3]);SM=atoi(v[4]);H=h+2;W=w+2;
 FILE*f=fopen(v[5],"r");char line[1<<16];static char pos[100000];
 while(fgets(line,sizeof line,f)) if(line[0]=='v'){char*p=line+1;int x;int n;while(sscanf(p,"%d%n",&x,&n)==1){p+=n;if(x>0&&x<100000)pos[x]=1;}}
 for(int r=0;r<h;r++)for(int j=0;j<w;j++)T[r][j]=pos[1+r*w+j];
 for(int r=0;r<h;r++){for(int j=0;j<w;j++)putchar(T[r][j]?'o':'.');putchar('\n');}
 puts(rec(0)?"HAS_PREDECESSOR":"NO_PREDECESSOR"); return 0;}
