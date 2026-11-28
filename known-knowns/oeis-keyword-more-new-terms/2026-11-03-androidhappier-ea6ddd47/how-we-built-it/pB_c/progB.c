/* Program B (A214570): enumerate all rooted trees on n vertices (Beyer-Hedetniemi canonical level
   sequences); per tree c(t) = prod_v (#children(v))! / prod over runs of identical child subtrees (mult)!
   = number of distinct plane embeddings.  In a canonical level sequence identical sibling subtrees are
   adjacent.  Prints n, max c(t), sum c(t) (must equal Catalan(n-1)), #trees, #trees attaining max.
   usage: ./progB NMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static u64 F[40];
int main(int argc,char**argv){int NMAX=atoi(argv[1]);F[0]=1;for(int i=1;i<40;i++)F[i]=F[i-1]*i;
 for(int n=1;n<=NMAX;n++){int L[64],h[64];for(int i=0;i<n;i++)L[i]=i+1;
  u64 mx=0,sum=0,cnt=0,nmx=0;
  for(;;){
   for(int i=n-1;i>=0;i--){h[i]=1;int j=i+1;while(j<n&&L[j]>L[i]){h[i]+=h[j];j+=h[j];}}
   u64 num=1,den=1;
   for(int i=0;i<n;i++){int k=0,j=i+1,prev=-1,run=0;
     while(j<n&&L[j]>L[i]){k++;
       if(prev>=0&&h[prev]==h[j]&&memcmp(&L[prev],&L[j],sizeof(int)*h[j])==0)run++;
       else{den*=F[run];run=1;}
       prev=j;j+=h[j];}
     den*=F[run];num*=F[k];}
   if(num%den){fprintf(stderr,"nondiv\n");return 1;}
   u64 c=num/den;sum+=c;cnt++;
   if(c>mx){mx=c;nmx=1;}else if(c==mx)nmx++;
   int p=-1;for(int i=n-1;i>=1;i--)if(L[i]>2){p=i;break;}
   if(p<0)break;
   int q=-1;for(int i=p-1;i>=0;i--)if(L[i]==L[p]-1){q=i;break;}
   for(int i=p;i<n;i++)L[i]=L[i-(p-q)];
  }
  printf("%d %llu sum=%llu trees=%llu argmax=%llu\n",n,mx,sum,cnt,nmx);fflush(stdout);}
 return 0;}
