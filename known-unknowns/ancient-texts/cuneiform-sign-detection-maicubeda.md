# Cuneiform sign detection on the open MaiCuBeDa 3D-rendering benchmark: beat the published AP@50/AP@75 under a frozen split

🏺 **Ancient texts and fragments** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

The Mainz Cuneiform Benchmark Dataset (MaiCuBeDa Hilprecht, heiDATA doi:10.11588/DATA/QSNIQ2, CC BY-SA 4.0, version 1.1 released 2025-08-06 with description dated 2023-08-29, its 11 files (ids, sizes, MD5) unchanged from version 1.0 released 2023-08-30; about 9.3 GB: three ~3 GB zips (MSII / VirtualLight / Mixed) that hold only char/line/word/wedge crops and W3C JSON-LD annotation files, not whole-segment renderings, plus annotations.ttl, line/word/translit metadata; Journal of Open Archaeology Data 2025, doi:10.5334/joad.172) is the open benchmark for locating cuneiform signs on 3D-scan renderings. Stotzner, Homburg and Mara (ICCV 2023 workshops, arXiv 2308.11277) train a RepPoints/ResNet-18 single-class detector on 512x512 patches cut from 873 segments of 490 tablets (10,311 patches, 21,228 sign annotations) with a 2:1:1 segment-level split, and report in Table 2 (VOC 11-point interpolated AP, section 4.1) per training base and test rendering; best per test rendering: Mixed test AP@50 0.636 / AP@75 0.431 ('Complete with IA' = all renderings + HeiCuBeDa photographs, illumination augmentation); VL test AP@50 0.626 / AP@75 0.545 (Complete with IA) and AP@90 0.364 (VL with IA); MSII test AP@50 0.632 (Complete) / AP@75 0.437 (MSII). A June 2026 eBL paper (arXiv 2606.22608, DETR on a separate photo dataset of Lewenstein et al. 2026) does not evaluate on MaiCuBeDa and releases only weights and inference outputs on Zenodo, so MaiCuBeDa remains the only open, checkable benchmark. Status 2026-10-08 (vetter): no published result found exceeding the 2023 Table 2 values on MaiCuBeDa (the JOAD 2025 dataset paper cites only the 2023 baselines); heiDATA's HTML landing page is behind the Anubis bot filter, but the Dataverse API and /api/access/datafile/{id} return 200 to plain curl GET (HEAD returns 503; ranged GET returns 206), verified on readme.txt, utils.zip and the first KB of both large zips.

## What counts as a win

On MaiCuBeDa version 1 (heiDATA file ids and hashes recorded), the claimant names one test rendering R in {Mixed, VirtualLight, MSII}, publishes a deterministic segment-level 2:1:1 train/val/test split rule (e.g. sorted segment-id hash) and a deterministic 512x512 patch-cropping rule, and freezes (hash) the split and patch list before any training; no patch may overlap across splits. A detector trained ONLY on the train split (val for model selection) produces a frozen class-agnostic detections file (COCO JSON, hash committed before scoring) that, scored with pycocotools on the test patches of rendering R, achieves AP@50 AND AP@75 strictly above the BEST AP@50 and the BEST AP@75 reported for test rendering R in any row of Table 2 of arXiv 2308.11277 (re-read immediately before claiming). In addition the claimant retrains the paper's RepPoints/ResNet-18 baseline under the same frozen split with the same training base as one Table 2 row and freezes its detections (hash); the verifier's rescoring of that file must land within 0.03 AP@50 of that row's paper value, proving the split is comparable. Evaluation is sign-class-agnostic (localisation only) at 512x512 patch level, pycocotools defaults, all annotations counted unless a documented filter is applied identically to both files.

## Partial wins

- **p1:** Same protocol (frozen split, frozen detections, reproduced baseline), beating the best Table 2 AP@50 for the chosen test rendering by at least 0.02 absolute, or beating AP@90 0.364 on VirtualLight test patches.
- **p2:** Cross-rendering generalisation: a detector trained only on one rendering type (e.g. MSII) scores AP@50 on the held-out test patches of another rendering (e.g. VirtualLight) at least 0.05 above the Table 2 row for the same train-to-test direction (re-read live), with frozen detections, the same frozen split, and the reproduced baseline control.

## How a win is checked

The verifier downloads via plain curl GET from the heiDATA API only the annotation files and the zip of the chosen test rendering (about 3 GB; ranged GET works, HEAD does not), verifies hashes, regenerates the split and patch list from the published rules, checks that both frozen detections files' hashes predate scoring, rescores both (new system and reproduced baseline) with pycocotools, and checks no patch overlap across splits. No retraining by the verifier; under one hour on a 10-core Mac with a normal connection.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/DATA/QSNIQ2>

## Sources

- <https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/DATA/QSNIQ2>
- <https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/DATA/8TCR5C>
- <https://arxiv.org/abs/2308.11277>
- <https://ar5iv.labs.arxiv.org/html/2308.11277>
- <https://arxiv.org/abs/2606.22608>
- <https://zenodo.org/records/17395154>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Small anchor-free detectors (YOLO-n/s, FCOS-lite) at 512 px train in CPU-hours on 10k patches; sign boxes are small and dense, so tune anchor-free heads and NMS thresholds for crowded scenes.
- Multi-rendering fusion: stack MSII curvature, VirtualLight and Mixed renderings of the same patch as channels (the paper trains them separately).
- Test-time augmentation with illumination rotations (the dataset's VirtualLight directions) and box-level weighted fusion directly targets AP@75/AP@90.
- Use the wedge-level annotations (4,700 wedges in the dataset) as auxiliary supervision for sign boundaries.
- Reproduce the RepPoints baseline first on the frozen split; without it no comparison survives the CRITERION skeptic.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The paper's exact split is not shipped; comparing to its numbers without the reproduced-baseline control on your own split is apples to oranges. 'Complete' training rows also use HeiCuBeDa photographs (doi:10.11588/data/IE8CCN), which must be fetched separately if that row is reproduced.
- Patches overlap at segment level: a random patch-level split leaks near-identical crops into test and inflates AP by 10+ points. Split by segment (as the paper does) and verify no patch overlap across splits.
- AP numbers depend on the AP definition, the IoU protocol and which annotations are counted. Table 2 is VOC 11-point interpolated AP (section 4.1: 'we use the interpolated precision/recall curve with 11 recall levels', citing Everingham et al. 2010), not the pycocotools 101-point default named in the criterion; 18 of its 28 AP@90 values and 4 of its 28 AP@75 values are exact multiples of 1/11 (0.364 = 4/11, 0.545 = 6/11). Score the same frozen detections both ways, say which number is set against Table 2, and document any annotation filtering.
- The rendering zips contain no whole-segment rendering, so the 512x512 patches cannot be cut from 'the zip of the chosen test rendering' alone. Their central directories (listed 2026-10-18) hold only PNG crops (85,821 to 86,711 per zip in char/, croppoly_char/, word/, line/, wedge/ and croppoly_wedge/, each named after its parent segment) and 3,258 to 3,282 JSON annotation files (charannotations/, lineannotations/, wordannotations/). The 1,080 sign annotation files (charannotations/*.json) present in all three zips are byte-identical; in the one file checked (HS_1153_03_front.png.json) every target names the same heidIcon IIIF image (heidicon.ub.uni-heidelberg.de/iiif/2/..., 1088x1990) in all three zips, not a separate image per rendering. State where the segment images of rendering R come from, and hash them.
- Not every annotation is a sign: charannotations/HS_0044_03_front.png.json (the same file in all three zips) holds four editor test annotations ('Ein Polygon!', 'Ein Rechteck!', 'Knie', 'Fuss') with no image source, so 'all annotations counted' also counts non-signs. Document the filter that removes them and apply it identically to both detections files.
- Training-time augmentation that uses the test rendering (e.g. VirtualLight directions reserved for test) is leakage.
- The eBL 2026 DETR dataset is not released; its numbers cannot be used as a record or checked here.
- heiDATA HEAD requests return 503 and the HTML landing page sits behind a bot filter: use plain GET (ranged if needed) on /api/access/datafile/{id}; never retry through a challenge page.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/ancient-texts/cuneiform-sign-detection-maicubeda.md
```

Already set up? Say `run V3R1T4S on cuneiform-sign-detection-maicubeda`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `cuneiform-sign-detection-maicubeda`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
