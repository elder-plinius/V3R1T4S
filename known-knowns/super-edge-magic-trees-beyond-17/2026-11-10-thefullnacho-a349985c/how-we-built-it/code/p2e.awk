# gentreeg -p line (n parent indices, 1-based, root 0) -> "n;u-v,..." (0-based vertices)
{ n = NF; s = n ";"; for (i = 2; i <= n; i++) { a = i - 1; b = $i - 1; if (a > b) { t = a; a = b; b = t }; s = s (i > 2 ? "," : "") a "-" b }; print s }
