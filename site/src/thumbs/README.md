# site/src/thumbs/

Hand-made thumbnails for the gallery view of the open problems. Leave this folder empty and the page draws every
thumbnail itself (`site/src/thumbs.js`, a picture generated from the problem's id and category).

To give one problem its own picture, add `<target id>.webp` (or `.png` or `.jpg`) here, where `<target id>` is the
problem's exact `id` in `bank/targets.json`. `site/build.py` copies it to `thumbs/` in the build and the card shows it
in place of the drawn one.

- Shape: 16:10 (320 × 200 or 640 × 400 px); it is shown cropped to that ratio.
- At most 200 KB, a regular file (no symlinks), its first bytes must match its extension, its header must give
  16 to 1280 px on each side, and it must be complete (nothing cut off or appended) and a still picture (no APNG
  or animated WebP).
- Keep it plain: no text that repeats the title, nothing that needs a licence you do not have.
- Anything else in this folder (other names, unknown ids, oversized files, pictures too large in pixels) is skipped
  with a warning in the build log. This README and dotfiles are ignored.
