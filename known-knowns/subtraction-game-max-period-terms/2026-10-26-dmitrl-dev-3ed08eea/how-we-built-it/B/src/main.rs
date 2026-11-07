// Implementation B (independent of A): literal first-repeat definition with a hash map.
// Values are computed from the value array (not from the window), the window key is packed oldest-first,
// and the period is p - q at the first p >= n-1 whose window was already seen at q.
// Usage: subper_b wl|sg n threads [lo hi]
use std::collections::HashMap;
use std::env;
use std::thread;

fn period(n: usize, moves: &[usize], sg: bool, vals: &mut Vec<u8>, seen: &mut HashMap<u128, usize>) -> usize {
    vals.clear();
    seen.clear();
    let bits = if sg { 5 } else { 1 };
    let mask: u128 = if bits * n >= 128 { u128::MAX } else { (1u128 << (bits * n)) - 1 };
    let mut key: u128 = 0;
    let mut p = 0usize;
    loop {
        let v: u8 = if sg {
            let mut present: u64 = 0;
            for &s in moves {
                if s <= p { present |= 1u64 << vals[p - s]; }
            }
            (!present).trailing_zeros() as u8
        } else {
            let mut win = 0u8;
            for &s in moves {
                if s <= p && vals[p - s] == 0 { win = 1; break; }
            }
            win
        };
        vals.push(v);
        // oldest-first packing: new value enters at the top field, the oldest leaves at the bottom
        key = (key >> bits) | ((v as u128) << (bits * (n - 1)));
        key &= mask;
        if p + 1 >= n {
            if let Some(&q) = seen.get(&key) {
                return p - q;
            }
            seen.insert(key, p);
        }
        p += 1;
    }
}

fn main() {
    let a: Vec<String> = env::args().collect();
    let sg = a[1] == "sg";
    let n: usize = a[2].parse().unwrap();
    let threads: u64 = a[3].parse().unwrap();
    assert!(n >= 1 && n <= if sg { 25 } else { 64 });
    let (lo, hi): (u64, u64) = if a.len() >= 6 { (a[4].parse().unwrap(), a[5].parse().unwrap()) } else { (0, 1u64 << (n - 1)) };
    let chunk = (hi - lo + threads - 1) / threads;
    let mut hs = Vec::new();
    for t in 0..threads {
        let a0 = lo + t * chunk;
        let a1 = std::cmp::min(hi, a0 + chunk);
        hs.push(thread::spawn(move || {
            let mut hist: HashMap<usize, u64> = HashMap::new();
            let (mut best, mut arg) = (0usize, 0u64);
            let mut vals = Vec::with_capacity(1 << 16);
            let mut seen = HashMap::with_capacity(1 << 12);
            let mut moves = Vec::with_capacity(64);
            let mut m = a0;
            while m < a1 {
                moves.clear();
                for s in 1..n { if (m >> (s - 1)) & 1 == 1 { moves.push(s); } }
                moves.push(n);
                let per = period(n, &moves, sg, &mut vals, &mut seen);
                *hist.entry(per).or_insert(0) += 1;
                if per > best { best = per; arg = m; }
                m += 1;
            }
            (hist, best, arg)
        }));
    }
    let mut hist: HashMap<usize, u64> = HashMap::new();
    let (mut best, mut arg) = (0usize, u64::MAX);
    for h in hs {
        let (hh, b, g) = h.join().unwrap();
        for (k, v) in hh { *hist.entry(k).or_insert(0) += v; }
        if b > best || (b == best && g < arg) { best = b; arg = g; }
    }
    let set: Vec<String> = (1..n).filter(|s| (arg >> (s - 1)) & 1 == 1).map(|s| s.to_string()).chain(std::iter::once(n.to_string())).collect();
    println!("mode {} n {} range {} {} max {} set {}", if sg { "sg" } else { "wl" }, n, lo, hi, best, set.join(" "));
    let mut ks: Vec<_> = hist.keys().cloned().collect();
    ks.sort();
    for k in ks { println!("{} {}", k, hist[&k]); }
}
