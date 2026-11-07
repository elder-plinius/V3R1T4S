# The record we beat

## Source

| field | value |
|---|---|
| URL | https://esolangs.org/wiki/Brainfuck_constants |
| fetched (UTC) | 2026-11-03T19:45:41Z |
| HTTP status | 200 |
| page sha256 | d78c05da7dbb20b80f70cceea943fdd429372ae6abfbb3fe810cc29471db0dd4 |
| size | 136940 bytes |
| page last edited | 25 June 2025, 15:33 (oldid 160357) |
| re-fetches | three panel skeptics re-fetched the same URL on 2026-11-03 (20:18–20:29 UTC); all byte-identical (same sha256) |

## The extracted cell

Section `114514`, quoted from the fetched page (codes byte-identical to the page's):

- `+++[>++++++++<-]>+++[<++++++++>-]<+++++++[>++++++++<-]>+++++[<++++++++>-]<++[>++++++++<-]>++` (92, 2)
  non-wrapping — leaves the value in a cell
- `>++++++[<+++++>-]<+[>+++++>++++++>++++++++<<<-]>>>--------.<<.>+++.<---------.` (78, 4) non-wrapping —
  prints UTF-8 bytes
- `++++[->----<]>.-[+<------>]<+.-[+++>--<]>+.+[+++<----->]<.` (58, 2) non-wrapping ("using signed chars") —
  prints UTF-8 bytes
- unnumbered "Other versions": a BF-RLE form `62+[>1847+<-]>.` (page note: "114514=62×1847 but its too long,
  so encoded in BF-RLE"; expands to 1916 instructions and leaves the value in a cell) and a 468-instruction
  CESU-8 printer.

## The convention quoted

> The shortest known Brainfuck code sequences are listed for each constant, along with number of program
> instructions and cells taken. ... The non-wrapping solutions do not require this though the ones marked
> with "(soft)" do require cell values outside the 0-255 range (For numbers greater than 255 "soft" means
> that it uses negative cells).

The object uses only non-negative cells (the page's non-soft convention) and, like the listed 92-instruction
sequence, holds 114514 in a single cell under the page's >255 wide-cell convention.
