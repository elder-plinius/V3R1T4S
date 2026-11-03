// Program B (independent of otA.c): maximum eventual-cycle length of outer-totalistic CA on graphs.
// Reads graph6 lines on stdin. For each graph: D = max degree. Rules (B,S) with B,S subsets of {0..D}.
// Completeness of the restriction: the count c(v) of ON neighbours satisfies 0 <= c(v) <= deg(v) <= D, so the
// membership of any count > D in B or S is never consulted; every rule over {0..n-1} induces exactly the same
// successor map as its restriction to {0..D}. Hence max over 4^(D+1) restricted rules = max over all 4^n rules.
// Cycle lengths: successor map built directly per rule; nodes of in-degree 0 are peeled repeatedly (Kahn);
// remaining nodes lie on cycles; each cycle is walked once to measure its length.
// Output: "g6 maxperiod" per graph when -pg, then summary line.
package main

import (
	"bufio"
	"fmt"
	"math/bits"
	"os"
)

func parseG6(s string) (int, [][]bool) {
	n := int(s[0]) - 63
	a := make([][]bool, n)
	for i := range a {
		a[i] = make([]bool, n)
	}
	var bitsArr []int
	for _, ch := range s[1:] {
		x := int(ch) - 63
		for b := 5; b >= 0; b-- {
			bitsArr = append(bitsArr, (x>>uint(b))&1)
		}
	}
	idx := 0
	for j := 1; j < n; j++ {
		for i := 0; i < j; i++ {
			if bitsArr[idx] == 1 {
				a[i][j] = true
				a[j][i] = true
			}
			idx++
		}
	}
	return n, a
}

func main() {
	pg := len(os.Args) > 1 && os.Args[1] == "-pg"
	sc := bufio.NewScanner(os.Stdin)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	best, graphs, nn := 0, 0, 0
	var bestG string
	var bestB, bestS, bestStart int
	hist := map[int]int{}
	for sc.Scan() {
		line := sc.Text()
		if len(line) == 0 || line[0] == '>' {
			continue
		}
		n, a := parseG6(line)
		nn = n
		graphs++
		N := 1 << uint(n)
		nb := make([]uint, n)
		D := 0
		for v := 0; v < n; v++ {
			for u := 0; u < n; u++ {
				if a[v][u] {
					nb[v] |= 1 << uint(u)
				}
			}
			if d := bits.OnesCount(nb[v]); d > D {
				D = d
			}
		}
		// cnt[s*n+v] = ON neighbours of v in state s
		cnt := make([]int, N*n)
		for s := 0; s < N; s++ {
			for v := 0; v < n; v++ {
				cnt[s*n+v] = bits.OnesCount(uint(s) & nb[v])
			}
		}
		succ := make([]int, N)
		indeg := make([]int, N)
		alive := make([]bool, N)
		queue := make([]int, 0, N)
		gbest := 0
		M := 1 << uint(D+1)
		for B := 0; B < M; B++ {
			for S := 0; S < M; S++ {
				for s := 0; s < N; s++ {
					t := 0
					for v := 0; v < n; v++ {
						c := cnt[s*n+v]
						var on bool
						if (s>>uint(v))&1 == 1 {
							on = (S>>uint(c))&1 == 1
						} else {
							on = (B>>uint(c))&1 == 1
						}
						if on {
							t |= 1 << uint(v)
						}
					}
					succ[s] = t
				}
				for s := 0; s < N; s++ {
					indeg[s] = 0
					alive[s] = true
				}
				for s := 0; s < N; s++ {
					indeg[succ[s]]++
				}
				queue = queue[:0]
				for s := 0; s < N; s++ {
					if indeg[s] == 0 {
						queue = append(queue, s)
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
				for s := 0; s < N; s++ {
					if !alive[s] {
						continue
					}
					L := 0
					x := s
					for {
						alive[x] = false
						L++
						x = succ[x]
						if x == s {
							break
						}
					}
					if L > gbest {
						gbest = L
					}
					if L > best {
						best, bestG, bestB, bestS, bestStart = L, line, B, S, s
					}
				}
			}
		}
		hist[gbest]++
		if pg {
			fmt.Fprintf(w, "%s %d\n", line, gbest)
		}
	}
	set := func(m int) string {
		r := "{"
		f := true
		for k := 0; k < 32; k++ {
			if (m>>uint(k))&1 == 1 {
				if !f {
					r += ","
				}
				r += fmt.Sprint(k)
				f = false
			}
		}
		return r + "}"
	}
	fmt.Fprintf(w, "n=%d graphs=%d maxperiod=%d witness_graph6=%s B=%s S=%s witness_state=%d\n", nn, graphs, best, bestG, set(bestB), set(bestS), bestStart)
	for k := 0; k <= 256; k++ {
		if hist[k] > 0 {
			fmt.Fprintf(w, "hist %d %d\n", k, hist[k])
		}
	}
}
