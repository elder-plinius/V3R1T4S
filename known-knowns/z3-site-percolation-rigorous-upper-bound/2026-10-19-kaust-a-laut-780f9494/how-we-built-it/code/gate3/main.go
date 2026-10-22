// Gate probe for larger blocks (same model as gate.py; floats, a guide only).
// Enumerates every state of an a x b x c block once (G = largest open component, ties: first found in site order),
// stores the six face traces of G and the open count, then for each requested p writes, for the root and for
// every entry face, the law of the children's eta pattern grouped by the entry trace T_in. gate_lp.py runs the LPs.
// usage: gate3 a b c workers out_prefix p1 [p2 ...]
package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"sync"
)

var a, b, c, n int
var nbr [][]int
var faceIdx [6][]int // site -> face-local index or -1
var fsize [6]int
var opp = [6]int{1, 0, 3, 2, 5, 4}
var rule = "L0" // L0: ties -> first found; L1: ties -> largest sum over faces of trace sizes, then first found
var fmask [6]uint64
var minFaces = 0 // GATE_MINFACES: G must touch at least this many faces, else empty
var minSize = 0 // GATE_MINSIZE: a largest component smaller than this counts as empty

func faceWeight(m uint64) int {
	w := 0
	for f := 0; f < 6; f++ {
		w += popcount(m & fmask[f])
	}
	return w
}

func setup() {
	n = a * b * c
	id := func(x, y, z int) int { return (x*b+y)*c + z }
	nbr = make([][]int, n)
	for x := 0; x < a; x++ {
		for y := 0; y < b; y++ {
			for z := 0; z < c; z++ {
				for _, d := range [][3]int{{1, 0, 0}, {-1, 0, 0}, {0, 1, 0}, {0, -1, 0}, {0, 0, 1}, {0, 0, -1}} {
					X, Y, Z := x+d[0], y+d[1], z+d[2]
					if X >= 0 && X < a && Y >= 0 && Y < b && Z >= 0 && Z < c {
						nbr[id(x, y, z)] = append(nbr[id(x, y, z)], id(X, Y, Z))
					}
				}
			}
		}
	}
	L := [3]int{a, b, c}
	for f := 0; f < 6; f++ {
		axis, side := f/2, 0
		if f%2 == 1 {
			side = L[axis] - 1
		}
		faceIdx[f] = make([]int, n)
		// face-local index: lexicographic order of the other two coordinates
		cnt := 0
		for x := 0; x < a; x++ {
			for y := 0; y < b; y++ {
				for z := 0; z < c; z++ {
					s := [3]int{x, y, z}
					faceIdx[f][id(x, y, z)] = -1
					if s[axis] == side {
						faceIdx[f][id(x, y, z)] = cnt
						cnt++
					}
				}
			}
		}
		fsize[f] = cnt
	}
}

// packed record: k (6 bits) | traces (6 x up to 9 bits)
type rec struct {
	k  uint8
	tr [6]uint16
}

func analyse(e uint64, stack []int) rec {
	var seen, best uint64
	bestSize := 0
	for s := 0; s < n; s++ {
		if e>>uint(s)&1 == 1 && seen>>uint(s)&1 == 0 {
			comp := uint64(1) << uint(s)
			seen |= comp
			size := 1
			stack = append(stack[:0], s)
			for len(stack) > 0 {
				v := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				for _, u := range nbr[v] {
					m := uint64(1) << uint(u)
					if e&m != 0 && seen&m == 0 {
						seen |= m
						comp |= m
						size++
						stack = append(stack, u)
					}
				}
			}
			if size > bestSize {
				best, bestSize = comp, size
			} else if size == bestSize && rule == "L1" && faceWeight(comp) > faceWeight(best) {
				best = comp
			}
		}
	}
	if bestSize < minSize {
		best = 0
	}
	if minFaces > 0 {
		nf := 0
		for f := 0; f < 6; f++ {
			if best&fmask[f] != 0 {
				nf++
			}
		}
		if nf < minFaces {
			best = 0
		}
	}
	var r rec
	r.k = uint8(popcount(e))
	for f := 0; f < 6; f++ {
		var t uint16
		for s := 0; s < n; s++ {
			if j := faceIdx[f][s]; j >= 0 && best>>uint(s)&1 == 1 {
				t |= 1 << uint(j)
			}
		}
		r.tr[f] = t
	}
	return r
}

func popcount(x uint64) int {
	c := 0
	for x != 0 {
		x &= x - 1
		c++
	}
	return c
}

func main() {
	a, _ = strconv.Atoi(os.Args[1])
	b, _ = strconv.Atoi(os.Args[2])
	c, _ = strconv.Atoi(os.Args[3])
	W, _ := strconv.Atoi(os.Args[4])
	out := os.Args[5]
	if len(os.Args[1]) > 0 && os.Getenv("GATE_RULE") != "" {
		rule = os.Getenv("GATE_RULE")
	}
	if v := os.Getenv("GATE_MINFACES"); v != "" {
		minFaces, _ = strconv.Atoi(v)
	}
	if v := os.Getenv("GATE_MINSIZE"); v != "" {
		minSize, _ = strconv.Atoi(v)
	}
	setup()
	for f := 0; f < 6; f++ {
		for s := 0; s < n; s++ {
			if faceIdx[f][s] >= 0 {
				fmask[f] |= 1 << uint(s)
			}
		}
	}
	N := uint64(1) << uint(n)
	recs := make([]rec, N)
	var wg sync.WaitGroup
	for w := 0; w < W; w++ {
		wg.Add(1)
		go func(w int) {
			defer wg.Done()
			stack := make([]int, 0, 64)
			for e := uint64(w); e < N; e += uint64(W) {
				recs[e] = analyse(e, stack)
			}
		}(w)
	}
	wg.Wait()
	// exact integer count tables C[f][k][T] (for an exact certificate later)
	cf, _ := os.Create(out + "_counts.txt")
	bw := bufio.NewWriter(cf)
	for f := 0; f < 6; f++ {
		cnt := make(map[[2]int]int64)
		for e := uint64(0); e < N; e++ {
			cnt[[2]int{int(recs[e].k), int(recs[e].tr[f])}]++
		}
		for key, v := range cnt {
			fmt.Fprintf(bw, "%d %d %d %d\n", f, key[0], key[1], v)
		}
	}
	bw.Flush()
	cf.Close()
	fmt.Fprintln(os.Stderr, "enumerated", N, "states")

	for _, ps := range os.Args[6:] {
		p, _ := strconv.ParseFloat(ps, 64)
		pw := make([]float64, n+1)
		for k := 0; k <= n; k++ {
			pw[k] = math.Pow(p, float64(k)) * math.Pow(1-p, float64(n-k))
		}
		// trace laws and r tables
		var r [6][]float64
		for f := 0; f < 6; f++ {
			g := opp[f]
			dist := make([]float64, 1<<uint(fsize[g]))
			for e := uint64(0); e < N; e++ {
				dist[recs[e].tr[g]] += pw[recs[e].k]
			}
			r[f] = make([]float64, 1<<uint(fsize[f]))
			for T := range r[f] {
				s := 0.0
				for S, v := range dist {
					if S&T != 0 {
						s += v
					}
				}
				r[f][T] = s
			}
		}
		// laws: root (64 patterns) and per entry face fin: L[fin][T][32]
		type acc struct {
			root [64]float64
			L    [6][][32]float64
		}
		accs := make([]*acc, W)
		for w := 0; w < W; w++ {
			wg.Add(1)
			go func(w int) {
				defer wg.Done()
				A := &acc{}
				for f := 0; f < 6; f++ {
					A.L[f] = make([][32]float64, 1<<uint(fsize[f]))
				}
				var rr [6]float64
				var full [64]float64
				for e := uint64(w); e < N; e += uint64(W) {
					R := &recs[e]
					if R.k == 0 {
						continue
					}
					wt := pw[R.k]
					for f := 0; f < 6; f++ {
						rr[f] = r[f][R.tr[f]]
					}
					// full 6-child product law
					full[0] = 1
					for f := 0; f < 6; f++ {
						m := 1 << uint(f)
						for x := m - 1; x >= 0; x-- {
							full[x|m] = full[x] * rr[f]
							full[x] = full[x] * (1 - rr[f])
						}
					}
					for x := 0; x < 64; x++ {
						A.root[x] += wt * full[x]
					}
					// entry face fin: marginalise face fin out, children = other faces in order
					for fin := 0; fin < 6; fin++ {
						L := &A.L[fin][R.tr[fin]]
						for x := 0; x < 64; x++ {
							// drop bit fin, compress
							lo := x & ((1 << uint(fin)) - 1)
							hi := (x >> uint(fin+1)) << uint(fin)
							L[lo|hi] += wt * full[x]
						}
					}
				}
				accs[w] = A
			}(w)
		}
		wg.Wait()
		of, _ := os.Create(fmt.Sprintf("%s_p%s.txt", out, ps))
		ow := bufio.NewWriter(of)
		fmt.Fprintf(ow, "dims %d %d %d p %s fsize %d %d %d %d %d %d\n", a, b, c, ps, fsize[0], fsize[1], fsize[2], fsize[3], fsize[4], fsize[5])
		var root [64]float64
		for _, A := range accs {
			for x := range root {
				root[x] += A.root[x]
			}
		}
		fmt.Fprint(ow, "root")
		for _, v := range root {
			fmt.Fprintf(ow, " %.17g", v)
		}
		fmt.Fprintln(ow)
		for fin := 0; fin < 6; fin++ {
			for T := 0; T < 1<<uint(fsize[fin]); T++ {
				var row [32]float64
				for _, A := range accs {
					for x := range row {
						row[x] += A.L[fin][T][x]
					}
				}
				fmt.Fprintf(ow, "L %d %d", fin, T)
				for _, v := range row {
					fmt.Fprintf(ow, " %.17g", v)
				}
				fmt.Fprintln(ow)
			}
		}
		ow.Flush()
		of.Close()
		fmt.Fprintln(os.Stderr, "p", ps, "done")
	}
}
