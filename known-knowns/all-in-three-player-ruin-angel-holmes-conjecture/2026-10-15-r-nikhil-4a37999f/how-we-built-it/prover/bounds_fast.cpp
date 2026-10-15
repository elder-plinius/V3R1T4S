#include <array>
#include <vector>
#include "unordered_map"
#include <numeric>
#include <cstdint>
#include <algorithm>
using I=int64_t;using Line=std::array<I,3>;using State=std::array<I,9>;using Pair=std::array<I,2>;
template<size_t N>struct Hash {size_t operator()(std::array<I,N> const& a)const noexcept{size_t h=1469598103934665603ULL;for(I x:a){h^=uint64_t(x)+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);h*=1099511628211ULL;}return h;}};
struct Kernel{
 std::vector<Line> poly;std::unordered_map<Line,int,Hash<3>> signs;std::unordered_map<Line,I,Hash<3>> weights;std::unordered_map<std::array<I,10>,Pair,Hash<10>> memo;I pow6[24];
 Kernel(const I*p,int m){for(int i=0;i<m;i++)poly.push_back({p[3*i],p[3*i+1],p[3*i+2]});pow6[0]=1;for(int i=1;i<24;i++)pow6[i]=pow6[i-1]*6;}
 int sign(Line const&l){auto it=signs.find(l);if(it!=signs.end())return it->second;bool pos=false,neg=false;for(auto p:poly){__int128 v=0;for(int k=0;k<3;k++)v+=(__int128)p[k]*l[k];pos|=v>0;neg|=v<0;}int s=pos&&neg?2:pos?1:neg?-1:0;signs.emplace(l,s);return s;}
 Line canonical(Line a){I g=std::gcd(std::gcd(a[0],a[1]),a[2]);if(g)for(I&v:a)v/=g;for(I v:a)if(v){if(v<0)for(I&w:a)w=-w;break;}return a;}
 Pair calc(State const&s,int d){if(!d)return {0,4};std::array<I,10> key;std::copy(s.begin(),s.end(),key.begin());key[9]=d;auto it=memo.find(key);if(it!=memo.end())return it->second;Pair out={0,0};
  for(auto ij:std::array<std::array<int,2>,3>{{{0,1},{0,2},{1,2}}}){int i=ij[0],j=ij[1];Line l;for(int k=0;k<3;k++)l[k]=s[3*i+k]-s[3*j+k];int r=sign(l);I unit=pow6[d-1];
   if(r==2){I w=(i==0?9:4)*unit;out[1]+=w;weights[canonical(l)]+=w;}
   else if(!r){if(i==0){out[0]+=5*unit;out[1]+=5*unit;}}
   else{int small=r<0?i:j,big=r<0?j:i;if(small==0){out[0]+=5*unit;out[1]+=5*unit;}State t=s;for(int k=0;k<3;k++){t[3*small+k]=2*s[3*small+k];t[3*big+k]=s[3*big+k]-s[3*small+k];}auto q=calc(t,d-1);out[0]+=q[0];out[1]+=q[1];}
  }
  memo.emplace(key,out);return out;
 }
};
extern "C" int compute_bounds(const I*vertices,int vertex_count,const I*aa,const I*bb,int depth,I*out,I*split){
 if(depth<1||depth>18||vertex_count<1||vertex_count>1000)return -1;
 Kernel k(vertices,vertex_count);State a,b;std::copy(aa,aa+9,a.begin());std::copy(bb,bb+9,b.begin());auto x=k.calc(a,depth);k.memo.clear();auto y=k.calc(b,depth);out[0]=x[0];out[1]=x[1];out[2]=y[0];out[3]=y[1];
 I best=-1;Line choice={0,0,0};for(auto const&it:k.weights){if(it.second>best||(it.second==best&&it.first<choice)){best=it.second;choice=it.first;}}
 if(best<0)return 0;for(int i=0;i<3;i++)split[i]=choice[i];return 1;
}
