// Program B (independent of totA.c): maximum cycle length of a totalistic CA that counts the node itself
// (OEIS A357952 definition) on each graph read as graph6 from stdin. For every rule R subset {0..n}
// (node v is ON next iff |closedNbhd(v) cap ON| in R), build the functional graph on all 2^n states,
// peel transient states by in-degree (Kahn), then measure every remaining cycle. Prints one line per graph
// "G <graph6> <max>" and a summary with the overall maximum, a witness and the histogram of per-graph maxima.
package main

import (
	"bufio"
	"fmt"
	"math/bits"
	"os"
	"runtime"
	"sort"
	"strings"
	"sync"
)

type result struct {
	idx   int
	g6    string
	best  int
	rule  int
	state int
	n     int
}

// parseG6 decodes a graph6 string (n < 63) into closed-neighbourhood bitmasks.
func parseG6(s string) (int, []uint32) {
	n := int(s[0]) - 63
	if n < 1 || n > 62 {
		panic("bad graph6 order: " + s)
	}
	var bitsList []int
	for _, ch := range []byte(s[1:]) {
		x := int(ch) - 63
		for b := 5; b >= 0; b-- {
			bitsList = append(bitsList, (x>>uint(b))&1)
		}
	}
	closed := make([]uint32, n)
	for v := 0; v < n; v++ {
		closed[v] = 1 << uint(v)
	}
	k := 0
	for j := 1; j < n; j++ {
		for i := 0; i < j; i++ {
			if bitsList[k] == 1 {
				closed[i] |= 1 << uint(j)
				closed[j] |= 1 << uint(i)
			}
			k++
		}
	}
	return n, closed
}

func solve(idx int, g6 string) result {
	n, closed := parseG6(g6)
	S := 1 << uint(n)
	// counts[s*n+v] = number of ON nodes in closed neighbourhood of v in state s
	counts := make([]uint8, S*n)
	for s := 0; s < S; s++ {
		for v := 0; v < n; v++ {
			counts[s*n+v] = uint8(bits.OnesCount32(uint32(s) & closed[v]))
		}
	}
	succ := make([]int32, S)
	indeg := make([]int32, S)
	alive := make([]bool, S)
	queue := make([]int32, 0, S)
	res := result{idx: idx, g6: g6, best: 0, rule: -1, state: -1, n: n}
	for R := 0; R < (1 << uint(n+1)); R++ {
		for s := 0; s < S; s++ {
			t := 0
			base := s * n
			for v := 0; v < n; v++ {
				if (R>>uint(counts[base+v]))&1 == 1 {
					t |= 1 << uint(v)
				}
			}
			succ[s] = int32(t)
			indeg[s] = 0
			alive[s] = true
		}
		for s := 0; s < S; s++ {
			indeg[succ[s]]++
		}
		queue = queue[:0]
		for s := 0; s < S; s++ {
			if indeg[s] == 0 {
				queue = append(queue, int32(s))
			}
		}
		for h := 0; h < len(queue); h++ {
			x := queue[h]
			alive[x] = false
			y := succ[x]
			indeg[y]--
			if indeg[y] == 0 {
				queue = append(queue, y)
			}
		}
		// every alive state lies on a cycle
		for s := 0; s < S; s++ {
			if !alive[s] {
				continue
			}
			L := 0
			x := int32(s)
			for {
				alive[x] = false
				L++
				x = succ[x]
				if int(x) == s {
					break
				}
			}
			if L > res.best {
				res.best, res.rule, res.state = L, R, s
			}
		}
	}
	return res
}

func main() {
	sc := bufio.NewScanner(os.Stdin)
	sc.Buffer(make([]byte, 1<<20), 1<<20)
	var lines []string
	for sc.Scan() {
		l := strings.TrimSpace(sc.Text())
		if l == "" || strings.HasPrefix(l, ">") {
			continue
		}
		lines = append(lines, l)
	}
	out := make([]result, len(lines))
	jobs := make(chan int, 1024)
	var wg sync.WaitGroup
	W := runtime.NumCPU()
	if e := os.Getenv("WORKERS"); e != "" {
		fmt.Sscan(e, &W)
	}
	for w := 0; w < W; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := range jobs {
				out[i] = solve(i, lines[i])
			}
		}()
	}
	for i := range lines {
		jobs <- i
	}
	close(jobs)
	wg.Wait()
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	hist := map[int]int{}
	best := result{best: -1}
	order := 0
	for _, r := range out {
		fmt.Fprintf(w, "G %s %d\n", r.g6, r.best)
		hist[r.best]++
		order = r.n
		if r.best > best.best {
			best = r
		}
	}
	var rs []string
	for k := 0; k <= order; k++ {
		if (best.rule>>uint(k))&1 == 1 {
			rs = append(rs, fmt.Sprint(k))
		}
	}
	fmt.Fprintf(w, "summary order=%d graphs=%d max_cycle=%d witness=%s rule_mask=%d rule={%s} state=%d\n",
		order, len(out), best.best, best.g6, best.rule, strings.Join(rs, ","), best.state)
	var ks []int
	for k := range hist {
		ks = append(ks, k)
	}
	sort.Ints(ks)
	for _, k := range ks {
		fmt.Fprintf(w, "hist %d %d\n", k, hist[k])
	}
}
