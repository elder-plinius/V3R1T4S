/* Four-person six-gate trade. A,B,A and C,B,C visit the same16 person/partner
   pairs and have identical boundary matchings, for distinct perfect matchings
   A,B,C on four men. Outside gates in the interval must be disjoint. */
static long square_attempts=0,square_success=0;
static int square_trade(Word*W){
 square_attempts++;if(W->len<6)return 0;
 for(int tr=0;tr<8;tr++){
  int r=rndint(W->len-1),lim=W->len-r-1;if(lim>40)lim=40;int q=r+1+rndint(lim);
  Gate x=W->g[r],y=W->g[q];if(!disjoint(x,y))continue;
  int S[4]={x.a,x.b,y.a,y.b},pos[6],np=0;uint64_t mask=0;for(int i=0;i<4;i++)mask|=UINT64_C(1)<<S[i];
  for(int k=r;k<W->len;k++){Gate g=W->g[k];int a=(mask>>g.a)&1,b=(mask>>g.b)&1;if(a!=b)break;if(a&&b){pos[np++]=k;if(np==6)break;}}
  if(np!=6)continue;
  int M[MAXN];memcpy(M,initial,sizeof M);for(int k=0;k<r;k++){Gate g=W->g[k];int t=M[g.a];M[g.a]=M[g.b];M[g.b]=t;}
  int old[4];for(int i=0;i<4;i++)old[i]=M[S[i]];
  for(int j=0;j<6;j++){Gate g=W->g[pos[j]];int t=M[g.a];M[g.a]=M[g.b];M[g.b]=t;}
  const int PM[3][4]={{1,0,3,2},{2,3,0,1},{3,2,1,0}};int bi=-1;
  for(int b=0;b<3;b++){int ok=1;for(int i=0;i<4;i++)if(M[S[i]]!=old[PM[b][i]])ok=0;if(ok)bi=b;}
  if(bi<0)continue;int ai=(bi+1+rndint(2))%3,j=0;
  for(int layer=0;layer<3;layer++){int h=layer==1?bi:ai;for(int i=0;i<4;i++)if(i<PM[h][i])W->g[pos[j++]]=(Gate){S[i],S[PM[h][i]]};}
  square_success++;return 1;
 }
 return 0;
}
