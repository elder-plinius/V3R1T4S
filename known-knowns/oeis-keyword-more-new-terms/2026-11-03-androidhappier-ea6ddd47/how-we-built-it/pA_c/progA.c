/* Program A (A214570): direct reading of the definition.  Enumerate ALL ordered (plane) trees on n
   vertices as Dyck words of length 2(n-1) (Catalan(n-1) of them), map each to its rooted-tree
   isomorphism class by bottom-up interning (class id of a node = id of the SORTED multiset of its
   children's class ids, kept in a hash table), count ordered trees per class, print the largest count.
   No embedding/automorphism formula is used.  usage: ./progA NMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HB 23
#define HS (1u<<HB)
static int *pool; static long poolN, poolCap;     /* key storage: len, ids... */
static long *hkey; static int *hid; static int nid;
static unsigned long long *cnt;                     /* per class id: number of ordered trees (root ids) */
static unsigned hsh(const int*a,int k){unsigned long long h=1469598103934665603ULL^k;for(int i=0;i<k;i++){h^=(unsigned)a[i]+0x9e3779b9u;h*=1099511628211ULL;}return (unsigned)(h^(h>>29));}
static int cmpi(const void*a,const void*b){int x=*(const int*)a,y=*(const int*)b;return (x>y)-(x<y);}
static int idOf(int*a,int k){ if(k>1)qsort(a,k,sizeof(int),cmpi);
  unsigned p=hsh(a,k)&(HS-1);
  while(hkey[p]>=0){long o=hkey[p];if(pool[o]==k&&memcmp(pool+o+1,a,k*sizeof(int))==0)return hid[p];p=(p+1)&(HS-1);}
  if(poolN+k+1>poolCap){poolCap*=2;pool=realloc(pool,poolCap*sizeof(int));}
  hkey[p]=poolN;pool[poolN++]=k;memcpy(pool+poolN,a,k*sizeof(int));poolN+=k;hid[p]=nid;
  if(nid>=(int)(HS*3/4)){fprintf(stderr,"table full\n");exit(1);} return nid++; }
static int n; static char w[64]; static unsigned long long total;
static int ch[64][64], nch[64];
static void classify(void){ int d=0; nch[0]=0;
  for(int i=0;i<2*(n-1);i++){ if(w[i]=='('){ d++; nch[d]=0; }
    else { int id=idOf(ch[d],nch[d]); d--; ch[d][nch[d]++]=id; } }
  int r=idOf(ch[0],nch[0]); cnt[r]++; total++; }
static void gen(int pos,int open,int close){ if(pos==2*(n-1)){ classify(); return; }
  if(open<n-1){ w[pos]='('; gen(pos+1,open+1,close); }
  if(close<open){ w[pos]=')'; gen(pos+1,open,close+1); } }
int main(int argc,char**argv){ int NMAX=atoi(argv[1]);
  poolCap=1<<22; pool=malloc(poolCap*sizeof(int)); hkey=malloc(HS*sizeof(long)); hid=malloc(HS*sizeof(int));
  cnt=calloc(HS,sizeof(unsigned long long)); memset(hkey,-1,HS*sizeof(long));
  for(n=1;n<=NMAX;n++){ total=0; int before=nid; (void)before;
    memset(cnt,0,HS*sizeof(unsigned long long)); gen(0,0,0);
    unsigned long long mx=0,nmx=0,ncls=0; for(int i=0;i<nid;i++) if(cnt[i]){ncls++; if(cnt[i]>mx){mx=cnt[i];nmx=1;} else if(cnt[i]==mx) nmx++;}
    printf("%d %llu ordered=%llu classes=%llu argmax=%llu\n",n,mx,total,ncls,nmx); fflush(stdout); }
  return 0; }
