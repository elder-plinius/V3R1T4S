#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
#include <cstdlib>
#include <cstddef>
#include <new>
// Process-local live C++ allocation cap. Header preserves max_align_t alignment.
static size_t live_bytes=0;
struct alignas(std::max_align_t) AllocationHeader{size_t bytes;};
void* operator new(size_t n){if(n>512ull*1024*1024-live_bytes)throw std::bad_alloc();auto h=(AllocationHeader*)std::malloc(sizeof(AllocationHeader)+n);if(!h)throw std::bad_alloc();h->bytes=n;live_bytes+=n;return h+1;}
void operator delete(void*p) noexcept{if(p){auto h=((AllocationHeader*)p)-1;live_bytes-=h->bytes;std::free(h);}}
void operator delete(void*p,size_t) noexcept{operator delete(p);}
void* operator new[](size_t n){return operator new(n);}
void operator delete[](void*p) noexcept{operator delete(p);}
void operator delete[](void*p,size_t) noexcept{operator delete(p);}
using namespace std;
using U=unsigned __int128;
struct C{int a,b,c,i,j;};
string dec(U x){if(!x)return "0";string s;while(x){s+=char('0'+x%10);x/=10;}reverse(s.begin(),s.end());return s;}
vector<C> readfile(string path,int n){ifstream f(path);if(!f)throw runtime_error("open failed"); vector<C>cs;set<tuple<int,int,int>> seen;string line;regex re("([0-9]+) ([0-9]+) ([0-9]+) ([123])N([123])");smatch m;while(getline(f,line)){if(!regex_match(line,m,re))throw runtime_error("malformed line");C c{stoi(m[1])-1,stoi(m[2])-1,stoi(m[3])-1,stoi(m[4])-1,stoi(m[5])-1};if(c.a<0||c.a>=c.b||c.b>=c.c||c.c>=n)throw runtime_error("range/order");if(!seen.emplace(c.a,c.b,c.c).second)throw runtime_error("duplicate");cs.push_back(c);}if(cs.size()!=size_t(n*(n-1)*(n-2)/6))throw runtime_error("missing triple");return cs;}
struct Result{U value;size_t states;size_t width;};
Result count(int n,const vector<C>&cs){vector<vector<pair<uint32_t,int>>> rules(n);for(auto c:cs){int t[3]={c.a,c.b,c.c};uint32_t mask=0;for(int k=0;k<3;k++)if(k!=c.i)mask|=1u<<t[k];rules[t[c.i]].push_back({mask,c.j});} unordered_map<uint32_t,U> cur,nxt;cur[0]=1;size_t states=1,width=1;uint32_t full=(1u<<n)-1;for(int depth=0;depth<n;depth++){nxt.clear();for(auto [s,v]:cur){uint32_t left=full^s;while(left){int x=__builtin_ctz(left);left&=left-1;bool ok=true;for(auto [mask,j]:rules[x])if(__builtin_popcount(s&mask)==j){ok=false;break;}if(ok)nxt[s|(1u<<x)]+=v;}}cur.swap(nxt);states+=cur.size();width=max(width,cur.size());}return {cur.count(full)?cur[full]:0,states,width};}
#ifndef LIBRARY
int main(int argc,char**argv){try{if(argc!=3)throw runtime_error("usage count n assignment");int n=stoi(argv[1]);if(n<3||n>25)throw runtime_error("n range 3..25");auto cs=readfile(argv[2],n);auto start=chrono::steady_clock::now();auto r=count(n,cs);cout<<"{\"n\":"<<n<<",\"count\":\""<<dec(r.value)<<"\",\"states\":"<<r.states<<",\"max_width\":"<<r.width<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;}catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 2;}}
#endif
