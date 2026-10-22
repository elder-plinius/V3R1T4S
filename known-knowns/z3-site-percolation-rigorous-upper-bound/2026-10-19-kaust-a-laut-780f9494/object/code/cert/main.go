// Certificate engine for the 3D block coupling (box blocks, coarse Z^3), rigorous interval arithmetic.
//
// Block states e in {0,1}^B. G(e) = the largest open component (connectivity inside the block); ties are broken by
// the larger sum over the six faces of the number of G's sites on that face, then by the first component found in
// site order; G is empty if its size is below minSize. T_f(e) = trace of G(e) on face f (face-local bit set).
//
// mode counts: writes, for each face f, the exact number of states with k open sites and trace S on f.
// mode laws:   reads outward-rounded float intervals for pw[k] = p^k (1-p)^(n-k), r_f(T) and 1 - r_f(T)
//              (made exactly from the counts by cert.py), and writes, for each entry face fin and entry trace T,
//              lower and upper bounds of  sum over states e with T_fin(e) = T, G(e) nonempty  of
//              pw[k(e)] * prod over the other faces f (in increasing order, child i = i-th of them) of
//              r_f(T_f(e)) if bit i of x is 1, else 1 - r_f(T_f(e)),   for every pattern x of the 5 children.
//              Every float product and sum is rounded outward (next float down for lower bounds, up for upper
//              bounds), so the true value lies between the two printed floats.
// usage: cert a b c workers minSize counts <out>
//        cert a b c workers minSize laws <intervals file> <out>
package main

import (
	"bufio"
	"fmt"
	"math"
	"math/bits"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
)

var a, b, c, n, minSize int
var nbr [][]int
var fmask [6]uint64
var fsites [6][]int

func setup() {
	n = a * b * c
	id := func(x, y, z int) int { return (x*b+y)*c + z }
	nbr = make([][]int, n)
	L := [3]int{a, b, c}
	for x := 0; x < a; x++ {
		for y := 0; y < b; y++ {
			for z := 0; z < c; z++ {
				for _, d := range [][3]int{{1, 0, 0}, {-1, 0, 0}, {0, 1, 0}, {0, -1, 0}, {0, 0, 1}, {0, 0, -1}} {
					X, Y, Z := x+d[0], y+d[1], z+d[2]
					if X >= 0 && X < a && Y >= 0 && Y < b && Z >= 0 && Z < c {
						nbr[id(x, y, z)] = append(nbr[id(x, y, z)], id(X, Y, Z))
					}
				}
				s := [3]int{x, y, z}
				for f := 0; f < 6; f++ {
					side := 0
					if f%2 == 1 {
						side = L[f/2] - 1
					}
					if s[f/2] == side {
						fmask[f] |= 1 << uint(id(x, y, z))
						fsites[f] = append(fsites[f], id(x, y, z)) // increasing site order = lexicographic in the other coords
					}
				}
			}
		}
	}
}

func faceWeight(m uint64) int {
	w := 0
	for f := 0; f < 6; f++ {
		w += bits.OnesCount64(m & fmask[f])
	}
	return w
}

func designated(e uint64, stack []int) uint64 {
	var seen, best uint64
	bestSize := 0
	for s := 0; s < n; s++ {
		m0 := uint64(1) << uint(s)
		if e&m0 == 0 || seen&m0 != 0 {
			continue
		}
		comp := m0
		seen |= m0
		stack = append(stack[:0], s)
		for len(stack) > 0 {
			v := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, u := range nbr[v] {
				m := uint64(1) << uint(u)
				if e&m != 0 && seen&m == 0 {
					seen |= m
					comp |= m
					stack = append(stack, u)
				}
			}
		}
		size := bits.OnesCount64(comp)
		if size > bestSize || (size == bestSize && faceWeight(comp) > faceWeight(best)) {
			best, bestSize = comp, size
		}
	}
	if bestSize < minSize {
		return 0
	}
	return best
}

func trace(g uint64, f int) int {
	t := 0
	for j, s := range fsites[f] {
		if g>>uint(s)&1 == 1 {
			t |= 1 << uint(j)
		}
	}
	return t
}

func down(x float64) float64 {
	if x > 0 {
		return math.Float64frombits(math.Float64bits(x) - 1)
	}
	return 0
}

func up(x float64) float64 {
	if x == 0 {
		return math.SmallestNonzeroFloat64
	}
	return math.Float64frombits(math.Float64bits(x) + 1)
}

func fmtf(x float64) string { return strconv.FormatFloat(x, 'g', -1, 64) }

func main() {
	a, _ = strconv.Atoi(os.Args[1])
	b, _ = strconv.Atoi(os.Args[2])
	c, _ = strconv.Atoi(os.Args[3])
	W, _ := strconv.Atoi(os.Args[4])
	minSize, _ = strconv.Atoi(os.Args[5])
	mode := os.Args[6]
	setup()
	if n > 32 {
		panic("block too large for this engine")
	}
	N := uint64(1) << uint(n)
	var wg sync.WaitGroup

	if mode == "counts" {
		out := os.Args[7]
		type cnt [6]map[[2]int]int64
		parts := make([]cnt, W)
		for w := 0; w < W; w++ {
			wg.Add(1)
			go func(w int) {
				defer wg.Done()
				var C cnt
				for f := range C {
					C[f] = map[[2]int]int64{}
				}
				stack := make([]int, 0, 64)
				for e := uint64(w); e < N; e += uint64(W) {
					g := designated(e, stack)
					k := bits.OnesCount64(e)
					for f := 0; f < 6; f++ {
						C[f][[2]int{k, trace(g, f)}]++
					}
				}
				parts[w] = C
			}(w)
		}
		wg.Wait()
		fo, _ := os.Create(out)
		bw := bufio.NewWriter(fo)
		fmt.Fprintf(bw, "dims %d %d %d minSize %d n %d fsize %d %d %d %d %d %d\n", a, b, c, minSize, n,
			len(fsites[0]), len(fsites[1]), len(fsites[2]), len(fsites[3]), len(fsites[4]), len(fsites[5]))
		for f := 0; f < 6; f++ {
			tot := map[[2]int]int64{}
			for w := 0; w < W; w++ {
				for key, v := range parts[w][f] {
					tot[key] += v
				}
			}
			keys := make([][2]int, 0, len(tot))
			for key := range tot {
				keys = append(keys, key)
			}
			sort.Slice(keys, func(i, j int) bool {
				if keys[i][0] != keys[j][0] {
					return keys[i][0] < keys[j][0]
				}
				return keys[i][1] < keys[j][1]
			})
			for _, key := range keys {
				fmt.Fprintf(bw, "C %d %d %d %d\n", f, key[0], key[1], tot[key])
			}
		}
		bw.Flush()
		fo.Close()
		return
	}

	// laws
	inF, out := os.Args[7], os.Args[8]
	pwLo := make([]float64, n+1)
	pwHi := make([]float64, n+1)
	var rLo, rHi, sLo, sHi [6][]float64
	for f := 0; f < 6; f++ {
		m := 1 << uint(len(fsites[f]))
		rLo[f], rHi[f], sLo[f], sHi[f] = make([]float64, m), make([]float64, m), make([]float64, m), make([]float64, m)
	}
	fin0, err := os.Open(inF)
	if err != nil {
		panic(err)
	}
	sc := bufio.NewScanner(fin0)
	sc.Buffer(make([]byte, 1<<20), 1<<20)
	pf := func(s string) float64 { v, err := strconv.ParseFloat(s, 64); if err != nil { panic(err) }; return v }
	for sc.Scan() {
		w := strings.Fields(sc.Text())
		if len(w) == 0 {
			continue
		}
		switch w[0] {
		case "pw":
			k, _ := strconv.Atoi(w[1])
			pwLo[k], pwHi[k] = pf(w[2]), pf(w[3])
		case "r":
			f, _ := strconv.Atoi(w[1])
			T, _ := strconv.Atoi(w[2])
			rLo[f][T], rHi[f][T], sLo[f][T], sHi[f][T] = pf(w[3]), pf(w[4]), pf(w[5]), pf(w[6])
		}
	}
	fin0.Close()
	type acc struct{ lo, hi [6][][32]float64 }
	accs := make([]*acc, W)
	for w := 0; w < W; w++ {
		wg.Add(1)
		go func(w int) {
			defer wg.Done()
			A := &acc{}
			for f := 0; f < 6; f++ {
				A.lo[f] = make([][32]float64, 1<<uint(len(fsites[f])))
				A.hi[f] = make([][32]float64, 1<<uint(len(fsites[f])))
			}
			stack := make([]int, 0, 64)
			var tr [6]int
			var lo, hi [32]float64
			for e := uint64(w); e < N; e += uint64(W) {
				g := designated(e, stack)
				if g == 0 {
					continue
				}
				k := bits.OnesCount64(e)
				for f := 0; f < 6; f++ {
					tr[f] = trace(g, f)
				}
				for fin := 0; fin < 6; fin++ {
					lo[0], hi[0] = pwLo[k], pwHi[k]
					i := 0
					for f := 0; f < 6; f++ {
						if f == fin {
							continue
						}
						m := 1 << uint(i)
						a1, a0 := rLo[f][tr[f]], sLo[f][tr[f]]
						b1, b0 := rHi[f][tr[f]], sHi[f][tr[f]]
						for x := m - 1; x >= 0; x-- {
							lo[x|m] = down(lo[x] * a1)
							hi[x|m] = up(hi[x] * b1)
							lo[x] = down(lo[x] * a0)
							hi[x] = up(hi[x] * b0)
						}
						i++
					}
					L, H := &A.lo[fin][tr[fin]], &A.hi[fin][tr[fin]]
					for x := 0; x < 32; x++ {
						L[x] = down(L[x] + lo[x])
						H[x] = up(H[x] + hi[x])
					}
				}
			}
			accs[w] = A
		}(w)
	}
	wg.Wait()
	fo, _ := os.Create(out)
	bw := bufio.NewWriter(fo)
	fmt.Fprintf(bw, "dims %d %d %d minSize %d n %d\n", a, b, c, minSize, n)
	for fin := 0; fin < 6; fin++ {
		for T := 0; T < 1<<uint(len(fsites[fin])); T++ {
			var L, H [32]float64
			for w := 0; w < W; w++ {
				for x := 0; x < 32; x++ {
					L[x] = down(L[x] + accs[w].lo[fin][T][x])
					H[x] = up(H[x] + accs[w].hi[fin][T][x])
				}
			}
			fmt.Fprintf(bw, "L %d %d", fin, T)
			for x := 0; x < 32; x++ {
				fmt.Fprintf(bw, " %s %s", fmtf(L[x]), fmtf(H[x]))
			}
			fmt.Fprintln(bw)
		}
	}
	bw.Flush()
	fo.Close()
}
