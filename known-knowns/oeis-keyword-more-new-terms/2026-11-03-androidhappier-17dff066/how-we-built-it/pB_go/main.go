// Program B (A331783): transcription of ldrsi/disjunsQ. For each integer partition of n-1, every multiset of trees with
// those sizes (nondecreasing index tuples within equal-size groups, i.e. the Union of Sort/@Tuples) is tested with disjunsQ:
// one branch -> ok; else non-leaf branches pairwise distinct, and every two branches equal or with disjoint sorted
// child lists (merge test). Trees get int32 ids; children stored as sorted id slices (with multiplicity).
// Usage: progB N [nodisj]
package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
)

var kids [][]int32 // kids[id] sorted child ids with multiplicity
var bySize [][]int32
var nodisj bool

func disjoint(a, b []int32) bool {
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] == b[j] {
			return false
		} else if a[i] < b[j] {
			i++
		} else {
			j++
		}
	}
	return true
}

func disjunsQ(u []int32) bool {
	if len(u) == 1 {
		return true
	}
	for i := 0; i < len(u); i++ {
		for j := i + 1; j < len(u); j++ {
			a, b := u[i], u[j]
			if a == b {
				if len(kids[a]) > 0 {
					return false // repeated non-leaf branch
				}
				continue
			}
			if !nodisj && !disjoint(kids[a], kids[b]) {
				return false
			}
		}
	}
	return true
}

func partitions(n, max int, cur []int, f func([]int)) {
	if n == 0 {
		f(cur)
		return
	}
	for p := min(n, max); p >= 1; p-- {
		partitions(n-p, p, append(cur, p), f)
	}
}

func main() {
	N, _ := strconv.Atoi(os.Args[1])
	nodisj = len(os.Args) > 2
	kids = append(kids, nil)
	bySize = make([][]int32, N+1)
	bySize[1] = []int32{0}
	fmt.Println(1, 1)
	for n := 2; n <= N; n++ {
		var count int64
		var newT [][]int32
		partitions(n-1, n-1, nil, func(c []int) {
			// groups of equal parts (c is nonincreasing)
			k := len(c)
			idx := make([]int, k)
			// recursive odometer with nondecreasing constraint inside equal-part groups
			var rec func(pos int)
			u := make([]int32, k)
			rec = func(pos int) {
				if pos == k {
					if disjunsQ(u) {
						count++
						if n < N {
							t := append([]int32(nil), u...)
							sort.Slice(t, func(a, b int) bool { return t[a] < t[b] })
							newT = append(newT, t)
						}
					}
					return
				}
				lst := bySize[c[pos]]
				start := 0
				if pos > 0 && c[pos-1] == c[pos] {
					start = idx[pos-1]
				}
				for x := start; x < len(lst); x++ {
					idx[pos] = x
					u[pos] = lst[x]
					rec(pos + 1)
				}
			}
			rec(0)
		})
		for _, t := range newT {
			bySize[n] = append(bySize[n], int32(len(kids)))
			kids = append(kids, t)
		}
		fmt.Println(n, count)
	}
}
