// Program B (Go) for the capturing/nesting set-partition family; independent of Program A.
// Partitions: "block containing lowest unused element" over bitmasks.
// capture(A,B) <=> |B strictly between min A and max A| >= 2  (or roles swapped)
// nest(A,B)    <=> some gap (x,y) of consecutive elements of A holds >= 2 elements of B (or swapped)
//                  (two elements of B inside (x,y): the consecutive-in-B pair among them lies inside too)
// cross(A,B)   <=> merged A/B label word has >= 4 runs
// Connectivity of block graphs by BFS.
package main

import (
	"fmt"
	"math/bits"
	"os"
	"strconv"
)

var n int
var full uint32
var blocks []uint32
var c245, c246, c249, c335, c336 int64

func between(lo, hi int) uint32 { // bits for elements strictly between positions lo and hi (0-based)
	if hi-lo < 2 {
		return 0
	}
	return ((uint32(1) << uint(hi)) - 1) &^ ((uint32(1) << uint(lo+1)) - 1)
}

func capt1(a, b uint32) bool {
	lo := bits.TrailingZeros32(a)
	hi := 31 - bits.LeadingZeros32(a)
	return bits.OnesCount32(b&between(lo, hi)) >= 2
}

func nest1(a, b uint32) bool {
	prev := -1
	for m := a; m != 0; m &= m - 1 {
		p := bits.TrailingZeros32(m)
		if prev >= 0 && bits.OnesCount32(b&between(prev, p)) >= 2 {
			return true
		}
		prev = p
	}
	return false
}

func cross(a, b uint32) bool {
	runs, last := 0, -1
	for i := 0; i < n; i++ {
		bit := uint32(1) << uint(i)
		lab := -1
		if a&bit != 0 {
			lab = 0
		} else if b&bit != 0 {
			lab = 1
		}
		if lab >= 0 && lab != last {
			runs++
			last = lab
		}
	}
	return runs >= 4
}

func connected(adj [][]bool) bool {
	k := len(adj)
	if k <= 1 {
		return true
	}
	seen := make([]bool, k)
	q := []int{0}
	seen[0] = true
	for len(q) > 0 {
		v := q[0]
		q = q[1:]
		for w := 0; w < k; w++ {
			if adj[v][w] && !seen[w] {
				seen[w] = true
				q = append(q, w)
			}
		}
	}
	for _, s := range seen {
		if !s {
			return false
		}
	}
	return true
}

func evaluate() {
	k := len(blocks)
	an := make([][]bool, k)
	ac := make([][]bool, k)
	for i := range an {
		an[i] = make([]bool, k)
		ac[i] = make([]bool, k)
	}
	cro, cap, nes := false, false, false
	for i := 0; i < k; i++ {
		for j := i + 1; j < k; j++ {
			a, b := blocks[i], blocks[j]
			if cross(a, b) {
				cro = true
			}
			if capt1(a, b) || capt1(b, a) {
				cap = true
				ac[i][j], ac[j][i] = true, true
			}
			if nest1(a, b) || nest1(b, a) {
				nes = true
				an[i][j], an[j][i] = true, true
			}
		}
	}
	if cro && !cap {
		c245++
	}
	if cro && cap {
		c246++
	}
	if cap && !nes {
		c249++
	}
	if connected(an) {
		c335++
	}
	if connected(ac) {
		c336++
	}
}

func rec(used uint32) {
	if used == full {
		evaluate()
		return
	}
	free := full &^ used
	low := free & (-free)
	rest := free &^ low
	sub := rest
	for {
		blocks = append(blocks, low|sub)
		rec(used | low | sub)
		blocks = blocks[:len(blocks)-1]
		if sub == 0 {
			break
		}
		sub = (sub - 1) & rest
	}
}

func main() {
	lo, _ := strconv.Atoi(os.Args[1])
	hi, _ := strconv.Atoi(os.Args[2])
	fmt.Println("n A326245 A326246 A326249 A326335 A326336")
	for n = lo; n <= hi; n++ {
		full = (uint32(1) << uint(n)) - 1
		c245, c246, c249, c335, c336 = 0, 0, 0, 0, 0
		blocks = blocks[:0]
		rec(0)
		fmt.Printf("%d %d %d %d %d %d\n", n, c245, c246, c249, c335, c336)
	}
}
