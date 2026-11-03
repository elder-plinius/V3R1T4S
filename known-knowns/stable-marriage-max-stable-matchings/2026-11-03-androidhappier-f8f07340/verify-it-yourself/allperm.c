/* Independent counter (written from the definition): enumerate every perfect matching (all n! permutations, DFS with
   pruning only by blocking pairs among already-assigned men) and count those with no blocking pair. */
#include <stdio.h>
#include <stdlib.h>
int n, mp[16][16], wp[16][16], mr[16][16], wr[16][16], M[16], used[16]; long long cnt;
/* partial check: when man m gets w, test blocking pairs (m, w') and (m', w) for all assigned m' < m and their women */
static int ok(int m){
  for(int a=0;a<=m;a++) for(int b=0;b<=m;b++) if(a!=b){
    int w=M[b]; /* does man a and woman w (matched to b) block? */
    if(mr[a][w]<mr[a][M[a]] && wr[w][a]<wr[w][b]) return 0; }
  return 1; }
static void rec(int m){ if(m==n){cnt++;return;}
  for(int w=0;w<n;w++) if(!used[w]){ used[w]=1; M[m]=w; if(ok(m)) rec(m+1); used[w]=0; } }
int main(int c,char**v){ FILE*f=fopen(v[1],"r"); char line[4096]; int rows=0; int g[32][16];
  while(fgets(line,sizeof line,f)){ if(line[0]=='#'||line[0]=='\n') continue; int k=0; char*s=line; int x,off;
    while(sscanf(s,"%d%n",&x,&off)==1){ g[rows][k++]=x-1; s+=off; } if(k){ n=k; rows++; } }
  if(rows!=2*n){fprintf(stderr,"bad rows %d n %d\n",rows,n);return 2;}
  for(int i=0;i<n;i++){ int seenm[16]={0},seenw[16]={0};
    for(int p=0;p<n;p++){ mp[i][p]=g[i][p]; wp[i][p]=g[n+i][p]; if(seenm[mp[i][p]]++||seenw[wp[i][p]]++){fprintf(stderr,"not perm\n");return 3;} } }
  for(int i=0;i<n;i++) for(int p=0;p<n;p++){ mr[i][mp[i][p]]=p; wr[i][wp[i][p]]=p; }
  rec(0); printf("n=%d stable_matchings=%lld\n",n,cnt); return 0; }
