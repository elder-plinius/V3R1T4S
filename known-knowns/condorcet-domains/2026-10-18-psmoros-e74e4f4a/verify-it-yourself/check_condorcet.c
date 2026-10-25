/* check_condorcet.c: standalone checker for an explicit Condorcet domain (V3R1T4S package).
   Definition (Karpov, Markstrom, Riis and Zhou, arXiv:2601.07336v1, Section 2, quoting Sen): a domain D of linear
   orders is a Condorcet domain if the restriction of D to any triple of alternatives (a,b,c) satisfies a never
   condition: some alternative of the triple is never ranked first, never second or never last within the triple.
   Size = number of (distinct) orders.
   Input on stdin: one linear order per line, the alternatives 1..N separated by single spaces, most preferred first.
   Checks: strict line format; every line a permutation of 1..N; all orders distinct (128-bit keys, sorted);
   every one of the C(N,3) triples satisfies a never condition. Optional ASSIGNMENT file (lines "a b c iNj", a<b<c,
   the i-th smallest of the triple never at position j, 1 top 2 middle 3 bottom): every triple must have exactly
   one line and every order must obey every line.
   Usage: ./check_condorcet N MIN_SIZE [ASSIGNMENT] < list.txt     Last output line: PASS or FAIL. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static int cmp(const void *x, const void *y){ u128 a=*(const u128*)x, b=*(const u128*)y; return a<b?-1:(a>b?1:0); }
static int tidx[26][26][26];
int main(int argc, char **argv){
  if(argc<3){ printf("usage: check_condorcet N MIN_SIZE [ASSIGNMENT] < list\nFAIL\n"); return 2; }
  int n=atoi(argv[1]); long long minsize=atoll(argv[2]);
  if(n<3||n>25){ printf("N must be 3..25\nFAIL\n"); return 2; }
  int T=0, ta[2300], tb[2300], tc[2300];
  for(int a=1;a<=n;a++) for(int b=a+1;b<=n;b++) for(int c=b+1;c<=n;c++){ tidx[a][b][c]=T; ta[T]=a; tb[T]=b; tc[T]=c; T++; }
  /* optional assignment: forbidden (member index 0..2, position 0..2) per triple */
  int have_asg = argc>3; int asg_x[2300], asg_p[2300]; long long asg_bad=0, asg_lines=0; int covered[2300];
  memset(covered,0,sizeof covered);
  if(have_asg){
    FILE *f=fopen(argv[3],"r"); if(!f){ printf("cannot open assignment\nFAIL\n"); return 2; }
    char ln[256];
    while(fgets(ln,sizeof ln,f)){
      int a,b,c,i,j; char N_; char extra[8];
      if(ln[0]=='\n') { asg_bad++; continue; }
      int k=sscanf(ln,"%d %d %d %d%c%d%7s",&a,&b,&c,&i,&N_,&j,extra);
      if(k!=6||N_!='N'||a<1||c>n||!(a<b&&b<c)||i<1||i>3||j<1||j>3){ asg_bad++; continue; }
      int t=tidx[a][b][c]; asg_lines++;
      if(covered[t]) { asg_bad++; continue; }
      covered[t]=1; asg_x[t]=i-1; asg_p[t]=j-1;
    }
    fclose(f);
    for(int t=0;t<T;t++) if(!covered[t]) asg_bad++;
  }
  unsigned char *mask=calloc(T,1);
  size_t cap=1<<20, cnt=0; u128 *keys=malloc(cap*sizeof(u128));
  char line[512]; long long bad=0, lines=0, disobey=0;
  while(fgets(line,sizeof line,stdin)){
    lines++;
    int ord[32], k=0, seen[32]; memset(seen,0,sizeof seen); int ok=1; char *p=line;
    for(;;){
      if(*p<'1'||*p>'9'){ ok=0; break; }                    /* no leading zero, no empty token */
      int v=0; while(*p>='0'&&*p<='9'){ v=v*10+(*p-'0'); p++; }
      if(k>=n||v<1||v>n||seen[v]){ ok=0; break; }
      seen[v]=1; ord[k++]=v;
      if(*p==' ') { p++; continue; }
      if(*p=='\n' && p[1]==0) break;
      ok=0; break;
    }
    if(!ok||k!=n){ bad++; continue; }
    int pos[32]; u128 key=0;
    for(int r=0;r<n;r++){ pos[ord[r]]=r; key=(key<<5)|(u128)ord[r]; }
    if(cnt==cap){ cap*=2; keys=realloc(keys,cap*sizeof(u128)); if(!keys){ printf("out of memory\nFAIL\n"); return 3; } }
    keys[cnt++]=key;
    int dis=0;
    for(int t=0;t<T;t++){
      int pa=pos[ta[t]], pb=pos[tb[t]], pc=pos[tc[t]];
      int ra=(pb<pa)+(pc<pa), rb=(pa<pb)+(pc<pb), rc=(pa<pc)+(pb<pc);   /* rank within the triple: 0 top .. 2 bottom */
      mask[t] |= (unsigned char)(1u << (ra*3+rb));            /* (ra,rb) determines the restricted order */
      if(have_asg){ int r = asg_x[t]==0?ra: asg_x[t]==1?rb: rc; if(r==asg_p[t]) dis=1; }
    }
    if(dis) disobey++;
  }
  qsort(keys,cnt,sizeof(u128),cmp);
  long long dup=0; for(size_t i=1;i<cnt;i++) if(keys[i]==keys[i-1]) dup++;
  long long viol=0;
  for(int t=0;t<T;t++){
    int s[3][3]; memset(s,0,sizeof s);
    for(int ra=0;ra<3;ra++) for(int rb=0;rb<3;rb++) if(mask[t] & (1u<<(ra*3+rb))){
      int rc=3-ra-rb; s[0][ra]=1; s[1][rb]=1; s[2][rc]=1;
    }
    int never=0; for(int x=0;x<3;x++) for(int j=0;j<3;j++) if(!s[x][j]) never=1;
    if(!never){ viol++; if(viol<=5) printf("  triple (%d,%d,%d) satisfies no never condition\n",ta[t],tb[t],tc[t]); }
  }
  long long distinct=(long long)cnt-dup;
  printf("n %d lines %lld malformed %lld distinct %lld duplicates %lld triples %d violations %lld\n",n,lines,bad,distinct,dup,T,viol);
  if(have_asg) printf("assignment lines %lld bad_or_missing %lld orders_disobeying %lld\n",asg_lines,asg_bad,disobey);
  printf("size %lld, required more than %lld\n", distinct, minsize-1);
  int pass = lines>0 && bad==0 && dup==0 && viol==0 && distinct>=minsize && (!have_asg || (asg_bad==0 && disobey==0));
  printf("%s\n", pass?"PASS":"FAIL");
  return pass?0:1;
}
