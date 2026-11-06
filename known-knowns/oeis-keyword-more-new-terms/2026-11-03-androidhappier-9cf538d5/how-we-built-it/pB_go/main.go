// A325786 Program B: different generator and test. Every composition of n is a subset C of Z_n
// containing 0 (its cut points = partial sums mod n), encoded as an (n-1)-bit mask. Completeness is
// rotation-invariant and equals: the circular difference set {c'-c mod n : c,c' in C} covers all nonzero
// residues (arc sums are those differences; the full circle gives n). Necklaces are counted by Burnside-free
// orbit weighting: each complete composition whose part sequence has minimal period p contributes 1/p
// (its rotation class has exactly p distinct compositions); sum is accumulated as a rational with common denominator via counting per (k,p).
package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
)

func main() {
	lo, _ := strconv.Atoi(os.Args[1])
	hi, _ := strconv.Atoi(os.Args[2])
	for n := lo; n <= hi; n++ {
		if n == 0 {
			fmt.Println(0, 0)
			continue
		}
		total := new(big.Rat)
		// cnt[k][p]
		cnt := map[[2]int]int64{}
		for m := uint64(0); m < (uint64(1) << uint(n-1)); m++ {
			pts := []int{0}
			for i := 1; i < n; i++ {
				if m>>(uint(i-1))&1 == 1 {
					pts = append(pts, i)
				}
			}
			cover := make([]bool, n)
			got := 0
			for _, a := range pts {
				for _, b := range pts {
					d := ((b-a)%n + n) % n
					if d != 0 && !cover[d] {
						cover[d] = true
						got++
					}
				}
			}
			if got != n-1 {
				continue
			}
			k := len(pts)
			parts := make([]int, k)
			for i := 0; i < k; i++ {
				nx := n
				if i+1 < k {
					nx = pts[i+1]
				}
				parts[i] = nx - pts[i]
			}
			p := k
			for d := 1; d < k; d++ {
				if k%d != 0 {
					continue
				}
				ok := true
				for i := 0; i < k; i++ {
					if parts[i] != parts[(i+d)%k] {
						ok = false
						break
					}
				}
				if ok {
					p = d
					break
				}
			}
			cnt[[2]int{k, p}]++
		}
		for kp, c := range cnt {
			total.Add(total, new(big.Rat).SetFrac64(c, int64(kp[1])))
		}
		fmt.Println(n, total.RatString())
	}
}
