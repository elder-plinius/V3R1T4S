// Canonical-geodesic criterion for site percolation on Z^3 (parallel, sign-flip symmetric).
//
// Parent rule of the BFS tree of the open cluster of 0: among the neighbours of v at distance d(v)-1, take the one in
// the smallest direction index (+x,-x,+y,-y,+z,-z). A tree path v_0..v_N is a neighbour-avoiding walk (NAW) whose
// forced-closed set F contains (i) every site off the path adjacent to v_i and v_j with j - i >= 3 (a shortcut), and
// (ii) at every turn v_{k-1} v_k v_{k+1}, the square corner u = v_{k-1} + v_{k+1} - v_k when, seen from v_{k+1}, its
// direction ranks before the direction of v_k (if open, u would be at distance k and the preferred parent).
// If 0 is in an infinite cluster, some tree path of length N is followed by a valid extension y (a neighbour of v_N
// off the path, adjacent to no other path vertex, not in F) joined to infinity off the path and F, so
// theta(p) <= K_N(p) theta(p), K_N(p) = sum over N-step walks of ext(walk) p^(N+1) (1-p)^|F|.
// Comparisons between directions of different axes depend only on the axes, so |F| and ext are invariant under the
// 8 sign flips; walks are enumerated with the first step along each axis positive and weighted 2^(axes used).
// Output: "EXT N f:count ..." (count = sum of ext over walks with |F| = f) and "TOTAL N a_N".
// usage: par N workers
package main

import (
	"fmt"
	"math/bits"
	"os"
	"strconv"
	"sync"
)

const S = 49 // walks of up to S/2 - 2 = 22 steps fit

var dirs = [6]int{1, -1, S, -S, S * S, -S * S}
var N int

type walker struct {
	onPath, inF [S * S * S]bool
	adj, minIdx [S * S * S]int32
	steps       [64]int
	ext         []int64
	total       int64
}

func (w *walker) add(y int, k1 int32) (added [8]int, na int, nf int) {
	// place y as v_{k1}; returns the newly forced W-sites (the caller adds the corner)
	w.onPath[y] = true
	for _, e := range dirs {
		z := y + e
		if w.onPath[z] {
			continue
		}
		if w.adj[z] > 0 && w.minIdx[z] <= k1-3 && !w.inF[z] {
			w.inF[z] = true
			added[na] = z
			na++
			nf++
		}
		if w.adj[z] == 0 {
			w.minIdx[z] = k1
		}
		w.adj[z]++
	}
	return
}

func (w *walker) remove(y int) {
	for _, e := range dirs {
		z := y + e
		if !w.onPath[z] {
			w.adj[z]--
		}
	}
	w.onPath[y] = false
}

func (w *walker) dfs(x, k, f int, axes uint) {
	if k == N {
		e := int64(0)
		for _, d := range dirs {
			y := x + d
			if !w.onPath[y] && w.adj[y] == 1 && !w.inF[y] {
				e++
			}
		}
		mult := int64(1) << uint(bits.OnesCount(axes))
		w.ext[f] += e * mult
		w.total += mult
		return
	}
	for di, d := range dirs {
		ax := uint(di >> 1)
		if axes&(1<<ax) == 0 && di&1 == 1 {
			continue // first step along a new axis is taken positive (sign-flip symmetry)
		}
		y := x + d
		if w.onPath[y] || w.adj[y] != 1 {
			continue
		}
		added, na, nf := w.add(y, int32(k+1))
		w.steps[k] = di
		if k >= 1 && w.steps[k-1] != di {
			dp := w.steps[k-1]
			if (dp ^ 1) < (di ^ 1) {
				u := y - dirs[dp]
				if !w.inF[u] {
					w.inF[u] = true
					added[na] = u
					na++
					nf++
				}
			}
		}
		w.dfs(y, k+1, f+nf, axes|1<<ax)
		for i := 0; i < na; i++ {
			w.inF[added[i]] = false
		}
		w.remove(y)
	}
}

func main() {
	N, _ = strconv.Atoi(os.Args[1])
	W, _ := strconv.Atoi(os.Args[2])
	if N > S/2-2 || N < 3 {
		panic("bad N")
	}
	c := S / 2 * (1 + S + S*S)
	// jobs: canonical 3-step prefixes
	type job struct{ d [3]int }
	var jobs []job
	for a := 0; a < 6; a++ {
		for b := 0; b < 6; b++ {
			for g := 0; g < 6; g++ {
				jobs = append(jobs, job{[3]int{a, b, g}})
			}
		}
	}
	ch := make(chan job, len(jobs))
	for _, j := range jobs {
		ch <- j
	}
	close(ch)
	ext := make([]int64, 4*N+16)
	var total int64
	var mu sync.Mutex
	var wg sync.WaitGroup
	for t := 0; t < W; t++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			w := &walker{ext: make([]int64, 4*N+16)}
			w.add(c, 0)
			for jb := range ch {
				// replay the prefix with the same rules as dfs; skip non-canonical or invalid prefixes
				x, f := c, 0
				var axes uint
				var undo [3]struct {
					y      int
					added  [8]int
					na     int
				}
				ok := true
				k := 0
				for ; k < 3; k++ {
					di := jb.d[k]
					ax := uint(di >> 1)
					if axes&(1<<ax) == 0 && di&1 == 1 {
						ok = false
						break
					}
					y := x + dirs[di]
					if w.onPath[y] || w.adj[y] != 1 {
						ok = false
						break
					}
					added, na, nf := w.add(y, int32(k+1))
					w.steps[k] = di
					if k >= 1 && w.steps[k-1] != di {
						dp := w.steps[k-1]
						if (dp ^ 1) < (di ^ 1) {
							u := y - dirs[dp]
							if !w.inF[u] {
								w.inF[u] = true
								added[na] = u
								na++
								nf++
							}
						}
					}
					undo[k].y, undo[k].added, undo[k].na = y, added, na
					f += nf
					axes |= 1 << ax
					x = y
				}
				if ok {
					w.dfs(x, 3, f, axes)
				}
				for k--; k >= 0; k-- {
					for i := 0; i < undo[k].na; i++ {
						w.inF[undo[k].added[i]] = false
					}
					w.remove(undo[k].y)
				}
			}
			mu.Lock()
			for i, v := range w.ext {
				ext[i] += v
			}
			total += w.total
			mu.Unlock()
		}()
	}
	wg.Wait()
	fmt.Printf("TOTAL %d %d\n", N, total)
	fmt.Printf("EXT %d", N)
	for f, v := range ext {
		if v != 0 {
			fmt.Printf(" %d:%d", f, v)
		}
	}
	fmt.Println()
}
