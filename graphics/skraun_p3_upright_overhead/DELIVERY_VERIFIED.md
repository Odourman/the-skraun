# GRAPHICS P3 – Verified delivery, 2026-11-16

**Status: design-only proof completed. No final art approval. No Stella or ROM development.**

## Full binary artifact
- **Google Drive complete ZIP:** https://drive.google.com/file/d/196UpbC1Kl400BcMj5zZ44Y48p7-WW7-W/view
- **File:** `THE_SKRAUN_GRAPHICS_P3_UPRIGHT_OVERHEAD_2026-11-16.zip`
- **Exact bytes:** `321411`
- **External ZIP SHA-256:** `84129bc78fa5a0884fb3866fe6b20f18ba7b4ff2b0f3d2aa2d784431b2d86a2a`
- **Full package:** 41 files, 40 listed in internal SHA256SUMS.txt (manifest itself excluded)
- ZIP CRC, 40/40 SHA entries, exact source bitmap geometry, 16 native 8×12 glyphs, left-right mirrors, A/B limb motion and six equal-cadence GIFs validated locally
- Extraction into fresh directory, deterministic image regeneration and post-regeneration manifest check: **PASS**
- Actual uploaded Drive ZIP was downloaded back; downloaded byte length and SHA-256 match local ZIP exactly

## Source in this branch
`P3_SOURCE_BITMAPS.json`, `P3_GRAPHICS_ONLY_PIXEL_DATA.inc`, `generate_previews.py`, `validate_p3.py`, `package_release.py`, `README.md`, `MAIN_II_P3_FINAL_REPORT.md`, `SHA256SUMS.txt`.

Source contains exactly TWO new U1/U2 8×12 families and two unchanged frozen references Q1/P1-A. Images and GIFs are inside complete Drive ZIP and generated deterministically by the checked-in generator; they are **source-derived design previews, not Stella captures**. Private original sketch has not been added to either location.

## Main II aesthetic gate

**Upright visual interpretation improved** under new direct user clarification superseding the prone P1/P2 visual hypothesis. **Combined original-character identity + physically strict overhead reading not proven at native Level 1.** U1 preserves more face but reads frontally; U2 better posture/arm separation but generic. This is an honest negative result for full approval. User/MAIN II owns acceptance.

No P4/v0.4, ROM/Stella, ART1 defect repair (#19), R4, B3c, gameplay, issue #15 closure, main merge or independent VERIFICATION. STOP after P3.
