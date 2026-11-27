// Exact maximum of a hinge on residues modulo 135. No external libraries.
// In a mod-9 row, all offsets are constant down a column. The weights of
// the three mod-27 children have a common weak ordering in every column.
// Nonnegative increasing hinge increments put either fine token in a
// heaviest child, and convexity puts both there when they use the same row.
#include <algorithm>
#include <array>
#include <stdexcept>
#include <cstdint>
#include <numeric>
#include <map>
#include <vector>

using I = int64_t;
using Wide = int64_t;
using Four = std::array<I,4>;
using Tab = std::array<I,16>;
struct Band { Four all, top, offset; };
struct Layout { std::vector<Band> roots[2]; };
static I pos(I x) { return std::max<I>(0,x); }

// A table indexed by the 9, 27, 45, 135 tokens used in this mod-9 band.
static inline Tab band_table(const Band &s, const Four &background, const I *coef) {
    Tab out;
    for (int pure=0; pure<4; ++pure) {
        I base=0, best_wide=0, best_fine=0, best_together=0;
        I wide=(pure&1)?coef[1]:0, fine=(pure&2)?coef[2]:0;
        for (int k=0;k<4;++k) {
            I h=background[k]+s.offset[k]+wide, a=s.all[k]-s.top[k], b=s.top[k];
            I low=pos(h), high=pos(h+fine);
            I low45=pos(h+coef[5]), high45=pos(h+fine+coef[5]);
            I gain45=a*(low45-low)+b*(high45-high);
            I gain135=b*(pos(h+fine+coef[6])-high);
            I combined=gain45+b*(pos(h+fine+coef[5]+coef[6])-high45);
            base+=a*low+b*high;
            best_wide=std::max(best_wide,gain45);
            best_fine=std::max(best_fine,gain135);
            best_together=std::max(best_together,combined);
        }
        out[pure]=base;
        out[pure|4]=base+best_wide;
        out[pure|8]=base+best_fine;
        out[pure|12]=base+std::max(best_wide+best_fine,best_together);
    }
    return out;
}
static inline void join(Tab &left, const Tab &right) {
    // Descending order leaves the entries for proper subsets intact.
    for (int s=15;s>=0;--s) {
        I best=left[s]+right[0];
        for (int r=s;r;r=(r-1)&s) best=std::max(best,left[s^r]+right[r]);
        left[s]=best;
    }
}
static inline Tab row_table(const std::vector<Band> &bands, const Four &base, const I *coef,
                            bool has3, bool has15) {
    Tab largest{};
    for (int col=0;col<(has15?4:1);++col) {
        Four y=base;
        if (has3) for (int k=0;k<4;++k) y[k]+=coef[0];
        if (has15) y[col]+=coef[4];
        Tab t=band_table(bands[0],y,coef);
        for (size_t j=1;j<bands.size();++j) join(t,band_table(bands[j],y,coef));
        for (int mask=0;mask<16;++mask) largest[mask]=std::max(largest[mask],t[mask]);
    }
    return largest;
}
static I max_hinge(const Layout &layout, I base, const I *coef) {
    I best=0;
    for (int c=0;c<(coef[3]?4:1);++c) {
        Four y{base,base,base,base};
        y[c]+=coef[3];
        Tab choices[2][4];
        for (int row=0;row<2;++row) {
            for (int bits=0;bits<4;++bits) {
                int active=bits&((coef[0]?1:0)|(coef[4]?2:0));
                if (active!=bits) choices[row][bits]=choices[row][active];
                else choices[row][bits]=row_table(layout.roots[row],y,coef,bits&1,bits&2);
            }
        }
        for (int shallow=0;shallow<4;++shallow)
            for (int deep=0;deep<16;++deep)
                best=std::max(best,choices[0][shallow][deep]+choices[1][3^shallow][15^deep]);
    }
    return best;
}
static Layout prepare(const I *a,const I *offset) {
    Layout lay;
    for (int r=0;r<9;++r) {
        if (r%3==0) continue;
        Band b{};
        I by_leaf[3][4]={};
        bool seen[4]={};
        for(int h=0;h<3;++h) for(int k=0;k<4;++k) {
            int x=r+9*h;
            while(x%5!=k+1) x+=27;
            by_leaf[h][k]=a[x];
            b.all[k]+=a[x];
            b.top[k]=std::max(b.top[k],a[x]);
            if (a[x]) {
                if (seen[k] && b.offset[k]!=offset[x]) throw std::domain_error("offset varies in column");
                b.offset[k]=offset[x];
                seen[k]=true;
            }
        }
        if (std::accumulate(b.all.begin(),b.all.end(),0)==0) continue;
        bool common_max=false;
        for(int h=0;h<3;++h)
            common_max|=std::equal(b.top.begin(),b.top.end(),by_leaf[h]);
        if (!common_max) throw std::domain_error("no common heaviest child");
        lay.roots[r%3-1].push_back(b);
    }
    if (lay.roots[0].empty() || lay.roots[1].empty()) throw std::domain_error("empty branch");
    return lay;
}
using Signature=std::array<I,72>;
static std::map<Signature,int> ids;
static std::vector<Layout> layouts;
static Signature signature(const Layout &l) {
    std::array<int,4> perm{0,1,2,3};
    Signature best{}; best.fill(INT64_MAX);
    do {
        using Record=std::array<I,12>;
        using Node=std::array<Record,3>;
        std::array<Node,2> root{};
        for(int t=0;t<2;++t) {
            int j=0;
            for (const Band &b:l.roots[t]) {
                for(int c=0;c<4;++c) {
                    int k=perm[c];
                    root[t][j][3*c]=b.all[k];
                    root[t][j][3*c+1]=b.top[k];
                    root[t][j][3*c+2]=b.offset[k];
                }
                ++j;
            }
            std::sort(root[t].begin(),root[t].end());
        }
        if(root[1]<root[0]) std::swap(root[0],root[1]);
        Signature sig{};
        int n=0;
        for(const auto &node:root) for(const auto &band:node) for(auto x:band) sig[n++]=x;
        best=std::min(best,sig);
    } while(std::next_permutation(perm.begin(),perm.end()));
    return best;
}
extern "C" int hinge_register(const I *a,const I *s) {
    try {
        Layout layout=prepare(a,s);
        auto res=ids.emplace(signature(layout),layouts.size());
        if (res.second) layouts.push_back(layout);
        return res.first->second;
    } catch (const std::domain_error &) {
        return -1;
    }
}
// Each job: baseline minus threshold, 7 coefficients, fixed-label weight.
extern "C" int hinge_batch(int idx,int jobs,const I *queries,I *answers) {
    if (idx<0 || size_t(idx)>=layouts.size() || jobs<0) return -1;
    const Layout &source=layouts[idx];
    Layout layout=source;
    int last=-1;
    for(int j=0;j<jobs;++j) {
        const I *q=queries+9*j;
        if(q[8]!=last) {
            for(int t=0;t<2;++t) for(size_t z=0;z<source.roots[t].size();++z)
                for(int k=0;k<4;++k) layout.roots[t][z].offset[k]=source.roots[t][z].offset[k]*q[8];
            last=q[8];
        }
        Wide mx=0, mass=0;
        for(int t=0;t<2;++t) for(const Band &b:layout.roots[t]) {
            mass+=std::accumulate(b.all.begin(),b.all.end(),Wide(0));
            mx=std::max<Wide>(mx,*std::max_element(b.offset.begin(),b.offset.end()));
        }
        mx+=std::max<I>(0,q[0]);
        for(int k=1;k<=7;++k) { if (q[k]<0) return -1; mx+=q[k]; }
        if(mx*mass>=(I(1)<<50)) return -1;
        answers[j]=max_hinge(layout,q[0],q+1);
    }
    return 0;
}
