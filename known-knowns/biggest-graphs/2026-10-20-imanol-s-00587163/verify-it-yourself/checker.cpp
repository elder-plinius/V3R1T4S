// Standalone checker: simple undirected edge list, maximum degree, all-pairs BFS diameter.
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;

static bool parse_int(const string &s, long long &v) {
    if (s.empty()) return false;
    char *end = nullptr;
    errno = 0;
    v = strtoll(s.c_str(), &end, 10);
    return errno == 0 && end && *end == '\0';
}

int main(int argc, char **argv) {
    if (argc != 5) {
        fprintf(stderr, "usage: checker EDGES N DELTA DIAMETER\n");
        return 2;
    }
    long long n = atoll(argv[2]), delta = atoll(argv[3]), want = atoll(argv[4]);
    if (n <= 0 || delta < 0 || want < 0) { printf("FAIL bad arguments\n"); return 1; }
    ifstream in(argv[1]);
    if (!in) { printf("FAIL cannot open edge list\n"); return 1; }
    vector<vector<int>> adj(n);
    unordered_set<unsigned long long> seen;
    string line;
    long long edges = 0;
    while (getline(in, line)) {
        size_t p = line.find_first_not_of(" \t\r");
        if (p == string::npos || line[p] == '#' || line[p] == '%') continue;
        istringstream ss(line);
        string a, b, extra;
        if (!(ss >> a >> b)) { printf("FAIL malformed line: %s\n", line.c_str()); return 1; }
        if (ss >> extra) { printf("FAIL extra column: %s\n", line.c_str()); return 1; }
        long long u, v;
        if (!parse_int(a, u) || !parse_int(b, v)) { printf("FAIL non-integer label: %s\n", line.c_str()); return 1; }
        if (u < 0 || v < 0 || u >= n || v >= n) { printf("FAIL label out of range: %s\n", line.c_str()); return 1; }
        if (u == v) { printf("FAIL loop at %lld\n", u); return 1; }
        int x = (int)min(u, v), y = (int)max(u, v);
        unsigned long long key = ((unsigned long long)(unsigned)x << 32) | (unsigned)y;
        if (!seen.insert(key).second) { printf("FAIL repeated undirected edge %d-%d\n", x, y); return 1; }
        adj[x].push_back(y);
        adj[y].push_back(x);
        ++edges;
    }
    for (long long i = 0; i < n; ++i)
        if ((long long)adj[i].size() > delta) { printf("FAIL degree of %lld is %zu > %lld\n", i, adj[i].size(), delta); return 1; }
    long long diam = 0;
    deque<int> q;
    vector<int> dist(n);
    for (long long s = 0; s < n; ++s) {
        fill(dist.begin(), dist.end(), -1);
        dist[s] = 0;
        q.clear();
        q.push_back((int)s);
        long long reached = 1;
        while (!q.empty()) {
            int u = q.front(); q.pop_front();
            for (int v : adj[u]) if (dist[v] < 0) { dist[v] = dist[u] + 1; ++reached; q.push_back(v); }
        }
        if (reached != n) { printf("FAIL graph disconnected from vertex %lld\n", s); return 1; }
        long long ecc = 0;
        for (long long i = 0; i < n; ++i) ecc = max(ecc, (long long)dist[i]);
        diam = max(diam, ecc);
    }
    if (diam > want) { printf("FAIL diameter %lld > %lld\n", diam, want); return 1; }
    printf("vertices %lld edges %lld max_degree_checked %lld diameter %lld\n", n, edges, delta, diam);
    printf("PASS\n");
    return 0;
}
