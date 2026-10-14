#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;
using U=uint64_t;
long long C[64][16];
void choose_init(){for(int n=0;n<64;n++){C[n][0]=1;for(int k=1;k<=min(n,15);k++)C[n][k]=(n?C[n-1][k-1]:0)+(n?C[n-1][k]:0);}}
vector<U> read_code(const string& path,int n,int w){
 ifstream f(path);if(!f)throw runtime_error("input absent");vector<U> a;string s;
 while(getline(f,s)){if((int)s.size()!=n||s.find_first_not_of("01")!=string::npos)throw runtime_error("invalid input word");U x=stoull(s,0,2);if(__builtin_popcountll(x)!=w)throw runtime_error("invalid weight");a.push_back(x);}return a;
}
vector<vector<int>> combinations(int w,int t){vector<vector<int>> out;vector<int>s(t);iota(s.begin(),s.end(),0);do{out.push_back(s);int j=t-1;while(j>=0&&s[j]==w-t+j)j--;if(j<0)break;s[j]++;for(int k=j+1;k<t;k++)s[k]=s[k-1]+1;}while(true);return out;}
int main(int argc,char**argv){try{
 if(argc!=7)throw runtime_error("usage: scan seed n w forbidden_t max_blockers output_prefix");
 auto start=chrono::steady_clock::now();string path=argv[1],prefix=argv[6];int n=stoi(argv[2]),w=stoi(argv[3]),t=stoi(argv[4]),cap=stoi(argv[5]);
 if(n>=63||n<w||w>=16||t>w||cap<0)throw runtime_error("unsupported parameters");choose_init();auto code=read_code(path,n,w);auto sub=combinations(w,t);
 vector<int> owner(C[n][t],-1);vector<int> seen(code.size(),0);vector<int> support(w);
 for(int i=0;i<(int)code.size();i++){U x=code[i];int j=0;while(x){support[j++]=__builtin_ctzll(x);x&=x-1;}for(auto&z:sub){int rank=0;for(int k=0;k<t;k++)rank+=C[support[z[k]]][k+1];if(owner[rank]>=0)throw runtime_error("seed subset collision");owner[rank]=i;}}
 unordered_set<U> in(code.begin(),code.end());vector<long long>hist(code.size()+1);ofstream out(prefix+".tsv");long long total=0,retained=0;int stamp=0;vector<int> blockers;
 const U stop=1ULL<<n;for(U x=(1ULL<<w)-1;x<stop;){total++;if(!in.count(x)){
  ++stamp;U y=x;int j=0;while(y){support[j++]=__builtin_ctzll(y);y&=y-1;}blockers.clear();
  for(auto&z:sub){int rank=0;if(t==4)rank=C[support[z[0]]][1]+C[support[z[1]]][2]+C[support[z[2]]][3]+C[support[z[3]]][4];else for(int k=0;k<t;k++)rank+=C[support[z[k]]][k+1];int a=owner[rank];if(a>=0&&seen[a]!=stamp){seen[a]=stamp;blockers.push_back(a);}}
  hist[blockers.size()]++;if((int)blockers.size()<=cap){retained++;sort(blockers.begin(),blockers.end());out<<x;for(int a:blockers)out<<' '<<a;out<<'\n';}
 }U low=x&-x,up=x+low;x=up+(((up^x)/low)>>2);}
 double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();ofstream js(prefix+".json");js<<"{\"total_words\":"<<total<<",\"incumbent_words\":"<<code.size()<<",\"outside_words\":"<<total-code.size()<<",\"max_blockers_retained\":"<<cap<<",\"retained\":"<<retained<<",\"elapsed_seconds\":"<<sec<<",\"blocker_histogram\":{";bool first=true;for(int i=0;i<(int)hist.size();i++)if(hist[i]){if(!first)js<<',';first=false;js<<'\"'<<i<<"\":"<<hist[i];}js<<"}}\n";js.close();cout<<"total="<<total<<" outside="<<total-code.size()<<" retained="<<retained<<" seconds="<<sec<<'\n';return 0;
 }catch(exception&e){cerr<<e.what()<<'\n';return 1;}}
