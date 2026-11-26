// Fast seeded bit-swap tabu search using bitset incidence and incremental conflict/boundary masks.
// usage: bstfast n w d s seed seconds outfile seedfile [tabu_min tabu_max max_no_improve_restart]
#include <bits/stdc++.h>
using namespace std;using u32=uint32_t;using u64=unsigned long long;
static int n,w,d,s,ol,BW;
static vector<u32> cb,bestcb;
static vector<u64> onebits; // n*BW, bit v set if word v has coordinate bit
static vector<u64> conf, boundary; // s*BW symmetric pair masks
static vector<int> confdeg,confpos,confverts;
static vector<int> tabu_rem,tabu_add;
static vector<u32> padlib;
static string seedfile;
static int basem=0;
static int penaltyCur=0,bestPenalty=0;
static double timelimit;static chrono::steady_clock::time_point tstart;
static int tabu_min=5,tabu_max=15,max_no_improve_restart=100000;
static inline int popc(u32 x){return __builtin_popcount(x);}
static inline double elapsed(){return chrono::duration<double>(chrono::steady_clock::now()-tstart).count();}
static inline bool getb(const vector<u64>&a,int idx,int v){return (a[(size_t)idx*BW+(v>>6)]>>(v&63))&1ULL;}
static inline void setb(vector<u64>&a,int idx,int v,bool val){
    u64 &z=a[(size_t)idx*BW+(v>>6)];u64 bit=1ULL<<(v&63);
    if(val)z|=bit;else z&=~bit;
}
static inline void setpair(vector<u64>&a,int i,int j,bool val){setb(a,i,j,val);setb(a,j,i,val);}
static inline int popmask_range(const u64* x,int words){
    int z=0;for(int i=0;i<words;i++)z+=__builtin_popcountll(x[i]);return z;
}
static void addconfvert(int v){
    if(confpos[v]>=0)return;confpos[v]=confverts.size();confverts.push_back(v);
}
static void delconfvert(int v){
    int p=confpos[v];if(p<0)return;int last=confverts.back();confverts[p]=last;confpos[last]=p;confverts.pop_back();confpos[v]=-1;
}
static void edge_update(int i,int j,bool isconf){
    bool old=getb(conf,i,j);
    if(old==isconf)return;
    setpair(conf,i,j,isconf);
    if(isconf){confdeg[i]++;confdeg[j]++;if(confdeg[i]==1)addconfvert(i);if(confdeg[j]==1)addconfvert(j);}
    else{confdeg[i]--;confdeg[j]--;if(confdeg[i]==0)delconfvert(i);if(confdeg[j]==0)delconfvert(j);}
}
static void compute_all(){
    fill(conf.begin(),conf.end(),0);fill(boundary.begin(),boundary.end(),0);
    fill(confdeg.begin(),confdeg.end(),0);fill(confpos.begin(),confpos.end(),-1);confverts.clear();
    penaltyCur=0;
    for(int i=0;i<s;i++)for(int j=i+1;j<s;j++){
        int dd=popc(cb[i]^cb[j]);
        if(dd<d){penaltyCur+=d-dd;edge_update(i,j,true);}
        else if(dd==d)setpair(boundary,i,j,true);
    }
}
static u32 random_word(mt19937 &rng){
    u32 x=0;int c=0;while(c<w){int b=rng()%n;if(!((x>>b)&1)){x|=1u<<b;c++;}}return x;
}
static int penalty_against(u32 x,int upto){
    int pen=0;for(int i=0;i<upto;i++){int dd=popc(x^cb[i]);if(dd<d)pen+=d-dd;}return pen;
}
static void build_padlib(){
    if(!padlib.empty())return;
    int best=INT_MAX;
    unordered_set<u32> ss(cb.begin(),cb.end());
    u32 x=(1u<<w)-1;u64 limit=1ULL<<n;
    while(true){
        if(!ss.count(x)){
            int pen=penalty_against(x,basem);
            if(pen<best){best=pen;padlib.clear();}
            if(pen==best)padlib.push_back(x);
        }
        u64 c=x&-(int)x,rr=x+c;u64 nx=(((rr^x)>>2)/c)|rr;
        if(nx>=limit||nx<=x)break;
        x=(u32)nx;
    }
    cerr<<"padlib size "<<padlib.size()<<" minpen "<<best<<" base "<<basem<<"\n";
}
static void init_state(mt19937 &rng){
    cb.clear();
    ifstream in(seedfile);string line;
    while((int)cb.size()<s&&getline(in,line)){
        if(line.empty()||line[0]=='#')continue;
        string z;for(char c:line)if(c=='0'||c=='1')z.push_back(c);
        if((int)z.size()!=n)continue;
        u32 x=0;int cnt=0;for(int i=0;i<n;i++)if(z[i]=='1'){x|=1u<<i;cnt++;}
        if(cnt==w&&find(cb.begin(),cb.end(),x)==cb.end())cb.push_back(x);
    }
    basem=cb.size();build_padlib();
    while((int)cb.size()<s){
        u32 x;int tries=0;
        do{x=padlib.empty()?random_word(rng):padlib[rng()%padlib.size()];tries++;}
        while(find(cb.begin(),cb.end(),x)!=cb.end()&&tries<1000);
        cb.push_back(x);
    }
    fill(onebits.begin(),onebits.end(),0);
    for(int v=0;v<s;v++)for(int b=0;b<n;b++)if((cb[v]>>b)&1)setb(onebits,b,v,true);
    fill(tabu_rem.begin(),tabu_rem.end(),0);fill(tabu_add.begin(),tabu_add.end(),0);
    compute_all();bestPenalty=penaltyCur;
}
static void write_code(const string&outfile){
    ofstream o(outfile);
    for(int i=0;i<s;i++){for(int b=0;b<n;b++)o<<((cb[i]>>b)&1?'1':'0');o<<'\n';}
}
static int check_penalty(){
    int z=0;for(int i=0;i<s;i++)for(int j=i+1;j<s;j++){int dd=popc(cb[i]^cb[j]);if(dd<d)z+=d-dd;}return z;
}
static int search(const string&outfile,unsigned seed){
    mt19937 rng(seed);init_state(rng);bestcb=cb;
    long iter=0,steps=0,restarts=0;int noimp=0;int globalbest=penaltyCur;
    double nextreport=5;
    while(elapsed()<timelimit){
        if(penaltyCur==0){write_code(outfile);cerr<<"SOLVED iter "<<iter<<" restarts "<<restarts<<" steps "<<steps<<" time "<<elapsed()<<"\n";return 1;}
        if(confverts.empty()){cerr<<"inconsistency no conflicts but penalty "<<penaltyCur<<"\n";return 0;}
        iter++;steps++;
        if((steps&1023)==0&&elapsed()>=timelimit)break;
        // choose a random conflicted vertex, then a random conflicted neighbour
        int a=confverts[rng()%confverts.size()];
        const u64* ca=&conf[(size_t)a*BW];
        int deg=confdeg[a];int pick=rng()%deg;int b=-1,seen=0;
        for(int wi=0;wi<BW;wi++){u64 bits=ca[wi];while(bits){int v=wi*64+__builtin_ctzll(bits);if(seen++==pick){b=v;break;}bits&=bits-1;}if(b>=0)break;}
        if(b<0){cerr<<"bad conflict pick\n";return 0;}
        int best_c=-1,best_p=-1,best_q=-1,best_new_pen=INT_MAX;long ties=0;
        for(int which=0;which<2;which++){
            int c=which?b:a,o=which?a:b;
            u32 ck=cb[c],ok=cb[o];
            u32 P=ck&ok,Q=(~ck)&(~ok)&(n==32?0xffffffffu:((1u<<n)-1));
            const u64* cf=&conf[(size_t)c*BW];const u64* bd=&boundary[(size_t)c*BW];
            for(int p=0;p<n;p++)if((P>>p)&1){
                const u64* bp=&onebits[(size_t)p*BW];
                for(int q=0;q<n;q++)if((Q>>q)&1){
                    const u64* bq=&onebits[(size_t)q*BW];
                    int inc=0,dec=0;
                    for(int z=0;z<BW;z++){
                        u64 notp=~bp[z];
                        inc+=__builtin_popcountll((cf[z]|bd[z])&bq[z]&notp);
                        dec+=__builtin_popcountll(cf[z]&bp[z]&~bq[z]);
                    }
                    int pen2=penaltyCur+2*(inc-dec);
                    bool tabu=(tabu_rem[c*n+p]>iter||tabu_add[c*n+q]>iter);
                    if(tabu&&pen2>=bestPenalty)continue;
                    if(pen2<best_new_pen){best_new_pen=pen2;best_c=c;best_p=p;best_q=q;ties=1;}
                    else if(pen2==best_new_pen){if(rng()%++ties==0){best_c=c;best_p=p;best_q=q;}}
                }
            }
        }
        if(best_c>=0){
            int c=best_c,p=best_p,q=best_q;u32 oldx=cb[c],newx=oldx^(1u<<p)^(1u<<q);
            // apply bit incidence
            setb(onebits,p,c,false);setb(onebits,q,c,true);
            cb[c]=newx;penaltyCur=best_new_pen;
            // recompute only row c conflicts/boundaries
            for(int t=0;t<s;t++){
                if(t==c)continue;
                int nd=popc(newx^cb[t]);
                edge_update(c,t,nd<d);
                bool isb=(nd==d),oldb=getb(boundary,c,t);
                if(isb!=oldb)setpair(boundary,c,t,isb);
            }
            int ten=tabu_min+(int)(rng()%(tabu_max-tabu_min+1));
            tabu_rem[c*n+p]=iter+ten;tabu_add[c*n+q]=iter+ten;
        }
        if(penaltyCur<bestPenalty){bestPenalty=penaltyCur;noimp=0;}else noimp++;
        if(penaltyCur<globalbest){globalbest=penaltyCur;bestcb=cb;cerr<<"progress bestpen "<<globalbest<<" iter "<<iter<<" restarts "<<restarts<<" time "<<elapsed()<<"\n";}
        if(best_c<0||noimp>=max_no_improve_restart){
            restarts++;
            if((restarts&15)==0)cerr<<"restart "<<restarts<<" globalbest "<<globalbest<<" steps "<<steps<<" time "<<elapsed()<<"\n";
            init_state(rng);iter=0;noimp=0;
        }
        if((steps&1048575)==0){
            int cp=check_penalty();
            if(cp!=penaltyCur){cerr<<"PENALTY MISMATCH "<<cp<<" vs "<<penaltyCur<<"\n";return 0;}
        }
        if(elapsed()>nextreport){nextreport+=5;cerr<<"status best "<<globalbest<<" cur "<<penaltyCur<<" restarts "<<restarts<<" steps "<<steps<<" time "<<elapsed()<<"\n";}
    }
    cerr<<"TIMEOUT globalbest "<<globalbest<<" restarts "<<restarts<<" steps "<<steps<<" time "<<elapsed()<<"\n";
    if(!bestcb.empty()){
        string bp=string(outfile)+".pen"+to_string(globalbest);
        ofstream bo(bp);
        for(int i=0;i<s;i++){for(int b=0;b<n;b++)bo<<((bestcb[i]>>b)&1?'1':'0');bo<<'\n';}
        cerr<<"wrote beststate "<<bp<<"\n";
    }
    return 0;
}
int main(int argc,char**argv){
    if(argc<9){cerr<<"usage: bstfast n w d s seed seconds outfile seedfile [tabu_min tabu_max max_no_improve_restart]\n";return 2;}
    n=atoi(argv[1]);w=atoi(argv[2]);d=atoi(argv[3]);s=atoi(argv[4]);
    unsigned seed=(unsigned)strtoul(argv[5],0,0);timelimit=atof(argv[6]);seedfile=argv[8];
    ol=w-d/2;BW=(s+63)/64;
    cb.reserve(s);onebits.assign((size_t)n*BW,0);conf.assign((size_t)s*BW,0);boundary.assign((size_t)s*BW,0);
    confdeg.assign(s,0);confpos.assign(s,-1);tabu_rem.assign((size_t)s*n,0);tabu_add.assign((size_t)s*n,0);
    if(argc>=12){tabu_min=atoi(argv[9]);tabu_max=atoi(argv[10]);max_no_improve_restart=atoi(argv[11]);}
    tstart=chrono::steady_clock::now();
    return search(argv[7],seed)?0:1;
}
