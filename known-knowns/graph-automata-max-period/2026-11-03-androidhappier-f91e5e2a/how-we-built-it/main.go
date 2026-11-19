// Program B (independent of totF.c): max cycle length of a totalistic CA on each graph6 graph from stdin.
// Usage: totB [self|nbr] [thresh]. nbr: count ON neighbours (A357953); self: count ON closed neighbourhood (A357952).
// Rule R: node v is ON next iff its count is in R. A count never exceeds Kmax = maxdeg (+1 for self), so bits of R
// above Kmax never matter and R ranges over all subsets of {0..Kmax} in plain binary order (complete).
// Per state s, the successor under R is the OR of the masks of vertices whose count is k, over k in R; the masks are
// stored sparsely (only counts that occur in s). Cycles: Kahn in-degree peeling removes transient states, then
// every remaining cycle is walked. Output: hist of per-graph maxima, graphs with max >= thresh, FNV-1a over the
// per-graph max sequence (input order), summary with a witness.
package main

import (
	"bufio"
	"fmt"
	"math/bits"
	"os"
	"strconv"
	"strings"
)

func main() {
	self := len(os.Args) > 1 && os.Args[1] == "self"
	thresh := 1 << 30
	if len(os.Args) > 2 {
		thresh, _ = strconv.Atoi(os.Args[2])
	}
	rd := bufio.NewReaderSize(os.Stdin, 1<<20)
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()
	hist := map[int]int64{}
	var h uint64 = 1469598103934665603
	best, bestRule, bestState := 0, 0, 0
	bestG := ""
	order := 0
	var graphs int64
	succ := make([]int32, 2048)
	indeg := make([]int32, 2048)
	queue := make([]int32, 2048)
	onCycle := make([]bool, 2048)
	for {
		line, err := rd.ReadString('\n')
		line = strings.TrimSpace(line)
		if line != "" && line[0] != '>' {
			n := int(line[0]) - 63
			order = n
			nb := make([]uint32, n)
			k := 0
			for j := 1; j < n; j++ {
				for i := 0; i < j; i++ {
					byteIdx := 1 + k/6
					bit := (int(line[byteIdx]) - 63) >> uint(5-k%6) & 1
					if bit == 1 {
						nb[i] |= 1 << uint(j)
						nb[j] |= 1 << uint(i)
					}
					k++
				}
			}
			D := 0
			for v := 0; v < n; v++ {
				if d := bits.OnesCount32(nb[v]); d > D {
					D = d
				}
			}
			kmax := D
			if self {
				kmax++
			}
			S := 1 << uint(n)
			// sparse per-state lists: cnt value and vertex mask
			start := make([]int32, S+1)
			var ks []uint8
			var ms []uint32
			for s := 0; s < S; s++ {
				var m [16]uint32
				for v := 0; v < n; v++ {
					c := bits.OnesCount32(uint32(s) & nb[v])
					if self {
						c += (s >> uint(v)) & 1
					}
					m[c] |= 1 << uint(v)
				}
				start[s] = int32(len(ks))
				for c := 0; c <= kmax; c++ {
					if m[c] != 0 {
						ks = append(ks, uint8(c))
						ms = append(ms, m[c])
					}
				}
			}
			start[S] = int32(len(ks))
			gbest := 0
			for R := 0; R < 1<<uint(kmax+1); R++ {
				for s := 0; s < S; s++ {
					var t uint32
					for q := start[s]; q < start[s+1]; q++ {
						if (R>>ks[q])&1 == 1 {
							t |= ms[q]
						}
					}
					succ[s] = int32(t)
					indeg[s] = 0
					onCycle[s] = true
				}
				for s := 0; s < S; s++ {
					indeg[succ[s]]++
				}
				qn := 0
				for s := 0; s < S; s++ {
					if indeg[s] == 0 {
						queue[qn] = int32(s)
						qn++
					}
				}
				for hd := 0; hd < qn; hd++ {
					x := queue[hd]
					onCycle[x] = false
					y := succ[x]
					indeg[y]--
					if indeg[y] == 0 {
						queue[qn] = y
						qn++
					}
				}
				for s := 0; s < S; s++ {
					if !onCycle[s] {
						continue
					}
					L := 0
					x := int32(s)
					for {
						onCycle[x] = false
						L++
						x = succ[x]
						if int(x) == s {
							break
						}
					}
					if L > gbest {
						gbest = L
					}
					if L > best {
						best, bestRule, bestState, bestG = L, R, s, line
					}
				}
			}
			graphs++
			hist[gbest]++
			if gbest >= thresh {
				fmt.Fprintf(w, "high %d %s\n", gbest, line)
			}
			h ^= uint64(gbest)
			h *= 1099511628211
		}
		if err != nil {
			break
		}
	}
	mode := "neighbours"
	if self {
		mode = "self"
	}
	var rs []string
	for k := 0; k < 31; k++ {
		if (bestRule>>uint(k))&1 == 1 {
			rs = append(rs, strconv.Itoa(k))
		}
	}
	fmt.Fprintf(w, "n=%d mode=%s graphs=%d maxperiod=%d witness_graph6=%s witness_rule_mask=%d witness_state=%d rule={%s}\n",
		order, mode, graphs, best, bestG, bestRule, bestState, strings.Join(rs, ","))
	for c := 0; c < 4096; c++ {
		if v, ok := hist[c]; ok {
			fmt.Fprintf(w, "hist %d %d\n", c, v)
		}
	}
	fmt.Fprintf(w, "fnv %016x\n", h)
}
