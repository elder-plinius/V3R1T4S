// Program B: literal transcription of the A316471 Mathematica algorithm.
// strut[n] = Union of sorted tuples over strut of each part of every integer partition of n-1, kept if branches are
// pairwise distinct and every pair of distinct branches has empty intersection of their own branch lists.
// Trees are canonical strings "(" + sorted child strings + ")"; intersection tested via string sets.
// Usage: progB N [nodisj]
package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

var strut = map[int][]string{}
var kids = map[string][]string{}
var nodisj bool

func partitions(n, max int, cur []int, out *[][]int) {
	if n == 0 {
		c := append([]int(nil), cur...)
		*out = append(*out, c)
		return
	}
	for p := min(n, max); p >= 1; p-- {
		partitions(n-p, p, append(cur, p), out)
	}
}

func get(n int) []string {
	if v, ok := strut[n]; ok {
		return v
	}
	if n == 1 {
		strut[1] = []string{"()"}
		kids["()"] = nil
		return strut[1]
	}
	var parts [][]int
	partitions(n-1, n-1, nil, &parts)
	seen := map[string]bool{}
	var res []string
	for _, c := range parts {
		lists := make([][]string, len(c))
		for i, p := range c {
			lists[i] = get(p)
		}
		idx := make([]int, len(c))
		for {
			tup := make([]string, len(c))
			for i := range c {
				tup[i] = lists[i][idx[i]]
			}
			sort.Strings(tup)
			key := "(" + strings.Join(tup, "") + ")"
			if !seen[key] {
				seen[key] = true
				if ok(tup) {
					res = append(res, key)
					kids[key] = tup
				}
			}
			// next tuple
			k := len(c) - 1
			for k >= 0 {
				idx[k]++
				if idx[k] < len(lists[k]) {
					break
				}
				idx[k] = 0
				k--
			}
			if k < 0 {
				break
			}
		}
	}
	strut[n] = res
	return res
}

func ok(tup []string) bool {
	for i := 0; i < len(tup); i++ {
		for j := 0; j < len(tup); j++ {
			if i == j {
				continue
			}
			if tup[i] == tup[j] {
				return false // UnsameQ
			}
			if nodisj {
				continue
			}
			set := map[string]bool{}
			for _, x := range kids[tup[i]] {
				set[x] = true
			}
			for _, y := range kids[tup[j]] {
				if set[y] {
					return false
				}
			}
		}
	}
	return true
}

func main() {
	N, _ := strconv.Atoi(os.Args[1])
	nodisj = len(os.Args) > 2
	for n := 1; n <= N; n++ {
		fmt.Println(n, len(get(n)))
	}
}
