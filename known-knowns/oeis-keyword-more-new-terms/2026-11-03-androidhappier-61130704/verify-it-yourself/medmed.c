/* A361864: count set partitions of {1..n} whose block-medians have integer median.
   Enumerate restricted growth strings; values doubled: 2*median(B) is an integer.
   Outer median over k values v_i = 2*median(B_i):
     k odd  -> median = v_mid/2, integer iff v_mid even
     k even -> median = (v_a+v_b)/4, integer iff (v_a+v_b) % 4 == 0 */
#include <stdio.h>
#include <stdlib.h>
static int n; static int rgs[32]; static long long cnt;
static int cmpi(const void*a,const void*b){return *(const int*)a-*(const int*)b;}
static void check(int k){
  int elems[32][32], sz[32]={0}, v[32];
  for(int i=0;i<n;i++){int b=rgs[i]; elems[b][sz[b]++]=i+1;} /* already increasing */
  for(int b=0;b<k;b++){int s=sz[b]; v[b]= (s&1)? 2*elems[b][s/2] : elems[b][s/2-1]+elems[b][s/2];}
  qsort(v,k,sizeof(int),cmpi);
  int ok = (k&1)? (v[k/2]%2==0) : ((v[k/2-1]+v[k/2])%4==0);
  if(ok) cnt++;
}
static void rec(int i,int k){
  if(i==n){check(k);return;}
  for(int b=0;b<=k;b++){rgs[i]=b; rec(i+1, b==k?k+1:k);}
}
int main(int argc,char**argv){
  int lo=atoi(argv[1]), hi=atoi(argv[2]);
  for(n=lo;n<=hi;n++){cnt=0; rgs[0]=0; rec(1,1); printf("%d %lld\n",n,cnt); fflush(stdout);}
  return 0;
}
