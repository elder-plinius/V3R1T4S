# The record we compared against

Every fetch: one plain request with an honest User-Agent, no retries. The pages themselves are not included. Response headers were not recorded at fetch time (only the HTTP status, size and sha256).

## DS1 (Radziszowski, Small Ramsey Numbers, Electron. J. Combin. Dynamic Survey DS1)
- Status page: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1, fetched 2026-10-25T07:34:37Z, HTTP 200, 17621 bytes, sha256 9095c60e25308c53990c3c3c3961e9e91b65600f7bf2cd5b191149b55bd70443; page text "This Version DS1: Apr 24, 2026".
- Full text: https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf, fetched 2026-10-25T06:19:34Z and 2026-10-25T07:44:20Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc both times; fetched again by the panel run on 2026-10-25T11:04:12Z, HTTP 200, same sha256.
- Extracted cell: R(3,4,7) >= 152, reference ExT (section 6.1.2, Table XIb "Known nontrivial lower bounds for 3-color Ramsey numbers of the form R(3,k,m)"). Table XIb as extracted by pdftotext -layout (row k = 3 is R(3,3,m) for m = 4..16, row k = 4 is R(3,4,m) for m = 4..9, row k = 5 is R(3,5,m) for m = 4..7; the line under each row gives the references):

```
        m          4      5       6      7       8        9     10     11    12    13    14    15    16
    k
                  30    45       61     85     103      129    150   174    194   217   242   269   291
    3
                 Ka2   Ex2      ExT   Ex18    Ex18     Ex18    ExT   ExT    ExT   ExT   ExT   ExT   ExT
                  55     89     117   152      193     242
    4
                KrLR   Ex17    Ex17   ExT     6.2.g    ExT
                  89    139     181    241
    5
                Ex17   Ex17    Ex17   6.2.g

```

## Further searches
The NOVELTY and CRITERION skeptics searched again on their own (newer arXiv papers, repositories, this repository's claims); their fetches and results are in panel/novelty.md and panel/criterion.md.
