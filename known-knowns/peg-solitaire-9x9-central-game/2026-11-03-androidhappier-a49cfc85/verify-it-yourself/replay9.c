/* Independent replay checker (self-break), written from the definition without looking at check9.py.
   13x13 array with a 2-cell wall border; cell value: -1 wall, 0 hole, 1 peg. Hole name: column a..i, row 1..9.
   Reads all hole names from the file in order; '-' joins holes of one move line; newline/comma/space separate lines.
   Start: all 81 filled except e5. Each consecutive pair within a line is a jump; must be orthogonal distance 2,
   over a peg, into an empty hole, from a peg. Moves = number of maximal same-peg runs (a jump whose origin is the
   previous jump's landing hole continues the move). PASS iff legal, 1 peg left at e5; prints jumps and moves. */
#include <stdio.h>
#include <string.h>
#include <ctype.h>
int g[13][13];
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); if(!f){puts("no file");return 2;}
  for(int i=0;i<13;i++)for(int j=0;j<13;j++) g[i][j]=(i>=2&&i<11&&j>=2&&j<11)?1:-1;
  g[6][6]=0; /* e5 = col 4 (0-based) +2, row 4 +2 */
  char line[4096]; int jumps=0,moves=0,lr=-1,lc=-1;
  while(fgets(line,sizeof line,f)){
    if(line[0]=='#') continue;
    int hr[512],hc[512],nh=0; char*p=line;
    for(;;){ while(*p && !isalnum((unsigned char)*p)){ if(*p=='\n'||*p==','||*p==' '){ /* line break inside? handled below */ } p++; }
      if(!*p) break; if(*p<'a'||*p>'i'){printf("FAIL bad token at %s",p);return 1;}
      int c=*p-'a'; p++; int r=0; while(isdigit((unsigned char)*p)){r=r*10+(*p-'0');p++;}
      if(r<1||r>9){printf("FAIL bad row\n");return 1;}
      hc[nh]=c+2; hr[nh]=r-1+2; nh++;
      if(*p!='-'){ /* end of this move's hole list */
        for(int k=0;k+1<nh;k++){ int r0=hr[k],c0=hc[k],r1=hr[k+1],c1=hc[k+1];
          int dr=r1-r0,dc=c1-c0;
          if(!((dr==0&&(dc==2||dc==-2))||(dc==0&&(dr==2||dr==-2)))){printf("FAIL jump %d not orthogonal-2\n",jumps+1);return 1;}
          int mr=r0+dr/2,mc=c0+dc/2;
          if(g[r0][c0]!=1||g[mr][mc]!=1||g[r1][c1]!=0){printf("FAIL jump %d illegal (from=%d over=%d to=%d)\n",jumps+1,g[r0][c0],g[mr][mc],g[r1][c1]);return 1;}
          g[r0][c0]=0; g[mr][mc]=0; g[r1][c1]=1; jumps++;
          if(!(r0==lr&&c0==lc)) moves++;
          lr=r1; lc=c1; }
        if(nh==1){printf("FAIL lone hole\n");return 1;}
        nh=0; }
      else p++;
    }
  }
  int left=0,cen=g[6][6];
  for(int i=2;i<11;i++)for(int j=2;j<11;j++) left+=g[i][j]==1;
  printf("jumps=%d moves=%d left=%d centre=%d\n",jumps,moves,left,cen);
  if(left==1&&cen==1){printf("PASS\n");return 0;} printf("FAIL final\n"); return 1;
}
