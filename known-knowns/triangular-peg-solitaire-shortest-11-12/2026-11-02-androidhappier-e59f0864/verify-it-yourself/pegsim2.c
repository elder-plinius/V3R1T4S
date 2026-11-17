/* Second, independent simulator (C, cube coordinates). Triangle(n) holes: cube coords (x,y,z) with x+y+z = n-1,
   x,y,z >= 0; Bell hole letter L (a=0) row R (1-based) maps to x = L, y = R-1-L, z = n-R.
   A jump: from p over p+d to p+2d, d one of the 6 cube unit vectors (permutations of (1,-1,0)).
   Reads moves "h-h-...-h" separated by ',' (also accepts '[', ']', '(k)' noise). The peg must sit at the move's
   first hole; each later hole must be a legal jump from the previous. Moves = maximal runs where a jump starts
   at the previous jump's landing hole. Prints VALID iff exactly one peg remains. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
static int n; static char peg[32][32][32];
static int inb(int x,int y,int z){return x>=0&&y>=0&&z>=0&&x+y+z==n-1;}
int main(int argc,char**argv){ n=atoi(argv[1]); FILE*f=fopen(argv[2],"r"); static char buf[1<<16]; size_t L=fread(buf,1,sizeof buf-1,f); buf[L]=0;
  for(char*p=buf;*p;p++){ if(*p=='('){ while(*p&&*p!=')')*p++=' '; if(*p)*p=' ';} if(*p=='['||*p==']'||*p=='\n'||*p==';')*p=','; }
  for(int x=0;x<n;x++)for(int y=0;y<n;y++){int z=n-1-x-y; if(z>=0) peg[x][y][z]=1;}
  int jumps=0,moves=0,first=1,px=-1,py=-1,pz=-1, sx=0,sy=0,sz=0;
  char *tok=strtok(buf,",");
  /* collect all jumps first to know start vacancy */
  int H[4096][3]; int nh=0; int brk[4096]; int nb=0;
  while(tok){ char*s=tok; int any=0;
    while(*s){ while(*s&&!isalpha((unsigned char)*s))s++; if(!*s)break; int Lt=*s-'a'; s++; int R=strtol(s,&s,10);
      H[nh][0]=Lt; H[nh][1]=R-1-Lt; H[nh][2]=n-R; if(!inb(H[nh][0],H[nh][1],H[nh][2])){printf("ILLEGAL off-board\n");return 1;} brk[nh]=(any==0); nh++; any=1; }
    tok=strtok(NULL,","); }
  /* start vacancy = landing hole of first jump (H[1]) */
  sx=H[1][0];sy=H[1][1];sz=H[1][2]; peg[sx][sy][sz]=0;
  for(int i=1;i<nh;i++){ if(brk[i]) continue; int *a=H[i-1],*b=H[i]; int dx=b[0]-a[0],dy=b[1]-a[1],dz=b[2]-a[2];
    if(dx%2||dy%2||dz%2){printf("ILLEGAL not a jump\n");return 1;} dx/=2;dy/=2;dz/=2;
    int ok=(abs(dx)+abs(dy)+abs(dz)==2)&&(dx+dy+dz==0); if(!ok){printf("ILLEGAL direction\n");return 1;}
    int mx=a[0]+dx,my=a[1]+dy,mz=a[2]+dz;
    if(!peg[a[0]][a[1]][a[2]]||!peg[mx][my][mz]||peg[b[0]][b[1]][b[2]]){printf("ILLEGAL jump %d\n",jumps+1);return 1;}
    peg[a[0]][a[1]][a[2]]=0;peg[mx][my][mz]=0;peg[b[0]][b[1]][b[2]]=1; jumps++;
    if(first||a[0]!=px||a[1]!=py||a[2]!=pz) moves++; first=0; px=b[0];py=b[1];pz=b[2]; }
  int left=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++){int z=n-1-x-y; if(z>=0&&peg[x][y][z]) left++;}
  printf("n=%d jumps=%d moves=%d pegs_left=%d %s\n",n,jumps,moves,left,left==1?"VALID":"NOT_SOLVED"); return left==1?0:1; }
