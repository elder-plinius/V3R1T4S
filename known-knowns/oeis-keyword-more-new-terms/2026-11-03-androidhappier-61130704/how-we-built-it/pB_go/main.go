// A361864 independent program: partitions generated as "block containing the lowest unused element" over bitmasks.
// Medians kept as exact rationals (num, den) with den in {1,2}; outer median as a rational; integer test by num%den.
package main

import (
	"fmt"
	"math/bits"
	"os"
	"sort"
	"strconv"
)

type rat struct{ p, q int64 } // value p/q, q>0

func less(a, b rat) bool { return a.p*b.q < b.p*a.q }

func median(xs []rat) rat {
	s := make([]rat, len(xs))
	copy(s, xs)
	sort.Slice(s, func(i, j int) bool { return less(s[i], s[j]) })
	m := len(s)
	if m%2 == 1 {
		return s[m/2]
	}
	a, b := s[m/2-1], s[m/2]
	return rat{a.p*b.q + b.p*a.q, 2 * a.q * b.q}
}

func blockMedian(mask uint32) rat {
	var el []rat
	for m := mask; m != 0; m &= m - 1 {
		el = append(el, rat{int64(bits.TrailingZeros32(m)) + 1, 1})
	}
	return median(el)
}

var full uint32
var count int64
var meds []rat

func rec(used uint32) {
	if used == full {
		md := median(meds)
		if md.p%md.q == 0 {
			count++
		}
		return
	}
	free := full &^ used
	low := free & (-free)
	rest := free &^ low
	// iterate over all subsets of rest
	sub := rest
	for {
		blk := low | sub
		meds = append(meds, blockMedian(blk))
		rec(used | blk)
		meds = meds[:len(meds)-1]
		if sub == 0 {
			break
		}
		sub = (sub - 1) & rest
	}
}

func main() {
	lo, _ := strconv.Atoi(os.Args[1])
	hi, _ := strconv.Atoi(os.Args[2])
	for n := lo; n <= hi; n++ {
		full = (uint32(1) << uint(n)) - 1
		count = 0
		rec(0)
		fmt.Printf("%d %d\n", n, count)
	}
}
