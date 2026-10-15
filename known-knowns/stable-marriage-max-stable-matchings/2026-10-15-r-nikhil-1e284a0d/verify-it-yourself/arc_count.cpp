// Independent complete binary-CSP enumeration from the blocking-pair definition.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std; using U=uint64_t;
int n, mr[32][32],wr[32][32]; U support[32][32][32]; unsigned long long nodes=0,leaves=0;
vector<vector<int>> load(const char *f){ifstream in(f);if(!in)throw runtime_error("missing input");vector<vector<int>> a;string s;while(getline(in,s)){if(s.empty()||s[0]=='#')continue;istringstream z(s);vector<int> row;int x;while(z>>x)row.push_back(x-1);if(!row.empty())a.push_back(row);}return a;}
bool prune(array<U,32>&d){bool again=true;while(again){again=false;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j){U v=d[i],keep=0;while(v){int a=__builtin_ctzll(v);v&=v-1;if(support[i][j][a]&d[j])keep|=U(1)<<a;}if(!keep)return false;if(keep!=d[i]){d[i]=keep;again=true;}}}return true;}
unsigned long long dfs(array<U,32> d){nodes++;if(!prune(d))return 0;int choose=-1,sz=99;for(int i=0;i<n;i++){int k=__builtin_popcountll(d[i]);if(k>1&&k<sz)choose=i,sz=k;}if(choose<0){int match[32],inv[32];U used=0;for(int i=0;i<n;i++){match[i]=__builtin_ctzll(d[i]);if(used&d[i])throw runtime_error("duplicate woman");used|=d[i];inv[match[i]]=i;}for(int i=0;i<n;i++)for(int w=0;w<n;w++)if(mr[i][w]<mr[i][match[i]]&&wr[w][i]<wr[w][inv[w]])throw runtime_error("blocking leaf");leaves++;return 1;}U v=d[choose];unsigned long long total=0;while(v){U b=v&-v;v-=b;auto e=d;e[choose]=b;auto c=dfs(e);if(UINT64_MAX-total<c)throw runtime_error("overflow");total+=c;}return total;}
int main(int argc,char**argv){try{if(argc!=2)throw runtime_error("usage: arc_count profile");auto start=chrono::steady_clock::now();auto a=load(argv[1]);if(a.empty()||a.size()%2)throw runtime_error("odd/empty row count");n=a.size()/2;if(n>31)throw runtime_error("size limit 31");for(int i=0;i<2*n;i++){if(a[i].size()!=n)throw runtime_error("row length");U seen=0;for(int j=0;j<n;j++){int v=a[i][j];if(v<0||v>=n||(seen&(U(1)<<v)))throw runtime_error("not permutation");seen|=U(1)<<v;if(i<n)mr[i][v]=j;else wr[i-n][v]=j;}}for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j)for(int w=0;w<n;w++)for(int v=0;v<n;v++)if(w!=v&&!(mr[i][v]<mr[i][w]&&wr[v][i]<wr[v][j])&&!(mr[j][w]<mr[j][v]&&wr[w][j]<wr[w][i]))support[i][j][w]|=U(1)<<v;array<U,32>d{};fill(d.begin(),d.begin()+n,(U(1)<<n)-1);auto count=dfs(d);cout<<"{\"n\":"<<n<<",\"count\":"<<count<<",\"nodes\":"<<nodes<<",\"stable_leaves\":"<<leaves<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"complete\":true}\n";}catch(exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
