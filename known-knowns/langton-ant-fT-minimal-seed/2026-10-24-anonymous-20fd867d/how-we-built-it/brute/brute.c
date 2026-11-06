/* Independent completeness check (segment 2). Enumerate every set C' of k<=2 black cells in the box |x|,|y|<=R.
   Simulate NS steps (ant (0,0) north, y down, white->right). Filter-onset s = least s with H[u]==H[u-104] for all u in [s+104,NS).
   Flag ESCAPE if the ant leaves the box within NS steps (then the box argument fails for that C').
   Prints min filter-s over all C' of exactly k cells, and every C' attaining it (and all with s < THR). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define R 35
#define NS 1000
#define G 256
static unsigned char g[G][G]; static int H[NS];
static int vx[NS+4],vy[NS+4];
static int sim(int n,int*cx,int*cy,int*esc){
  for(int i=0;i<n;i++) g[cy[i]+128][cx[i]+128]=1;
  int x=0,y=0,d=0,nv=0; static const int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
  *esc=0;
  for(int t=0;t<NS;t++){ unsigned char*c=&g[y+128][x+128];
    if(*c){d=(d+3)&3;*c=0;} else {d=(d+1)&3;*c=1;}
    vx[nv]=x;vy[nv]=y;nv++;
    x+=DX[d];y+=DY[d];H[t]=d; if(abs(x)>R||abs(y)>R)*esc=1; }
  for(int i=0;i<nv;i++) g[vy[i]+128][vx[i]+128]=0;
  for(int i=0;i<n;i++) g[cy[i]+128][cx[i]+128]=0;
  int bad=-1; for(int u=104;u<NS;u++) if(H[u]!=H[u-104]) bad=u;
  return bad<0?0:bad-103; }
int main(int a,char**v){ int k=atoi(v[1]),thr=atoi(v[2]),W=atoi(v[3]),w=atoi(v[4]);
  int N=(2*R+1)*(2*R+1),best=1<<30; long cnt=0,esc=0; int cx[2],cy[2],e;
  for(int i=0;i<N;i++){ if(i%W!=w) continue;
    for(int j=(k==1?i:i+1);j<(k==1?i+1:N);j++){
      cx[0]=i%(2*R+1)-R;cy[0]=i/(2*R+1)-R;cx[1]=j%(2*R+1)-R;cy[1]=j/(2*R+1)-R;
      int s=sim(k,cx,cy,&e); cnt++; if(e)esc++;
      if(s<best)best=s;
      if(s<=thr){printf("HIT s=%d esc=%d cells:",s,e);for(int q=0;q<k;q++)printf(" (%d,%d)",cx[q],cy[q]);printf("\n");}
    }}
  printf("DONE k=%d worker=%d configs=%ld escapes=%ld min_filter_s=%d\n",k,w,cnt,esc,best); return 0;}
