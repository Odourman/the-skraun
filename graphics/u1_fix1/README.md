# THE SKRAUN U1-FIX1 – targeted standing sprite correction

One corrected 8x12 source family U1, two poses A/B and LEFT as exact mirror of RIGHT. Frozen original U1 is embedded only as unchanged comparison. Source-derived static design images, **NOT Stella, ROM or art PASS**.

Read `MAIN_II_U1_FIX1_REPORT.md` and examine `00_L1_BLIND_FACING.png` before its separate key; no human evaluation has been performed.

To regenerate using Python 3 with Pillow:
```
python generate_u1_fix1_previews.py
python validate_u1_fix1.py
python build_release_zip.py
```
The manifest is fixed for the frozen submission and will deliberately fail if a source or picture changes. `build_release_zip.py` produces a byte-repeatable archive with frozen ZIP entry timestamps. This delivery is **stopped after one attempt**. No private original drawing is included.
