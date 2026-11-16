# THE SKRAUN — ROM DEVELOPMENT P01-ART1: STELLA VISUAL READOUT
**MAIN II technical handoff, 2026-11-16. Developer self-tests ONLY, no independent VERIFICATION.**

**Binding scope:** [P01-ART1 order](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P01_ART1_SKRAUN_STELLA_VISUAL_READOUT_AUTHORIZED_2026-11-16.md), [MAIN II issue #17 and latest clarifying comment](https://github.com/Odourman/the-skraun/issues/17), [MAIN P1 disposition](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_P1_HORIZONTAL_AXIS_REVIEW_AND_DECISION_2026-11-16.md), decisions 01–60 and original visual direction. No new art, gameplay, R4 or B3c.

## 1. DECISIVE RESULT

**TECHNICAL FAIL, transparently measured:** three real original-compatible 4K NTSC ROMs, 36/36 distinct captured Stella sprite states, 72 additional one-frame-at-a-time gait captures, and 36/36 directly measured 262-NTSC-line debugger states. The strict full-raster source-vs-Stella GRP0 pixel test passes **24/36** states (all level 1 and 2) but fails **12/36** (all level 3): its first active raster row y94 shows **every one of the 64 native PNG pixels gray** instead of the correct exact row mask. Remaining 35 rows agree with original source. The strict Actions test appropriately has **red/FAIL** status; a 262-line frame is not equivalent to correct sprite pixels.

This is an actual defect in this isolated P0 diagnostic rendering, NOT proof that the original source art has changed or a proof that the hardware can never render a quadruple-width player correctly. Source of that specific one-line rendering glitch has not been independently established. Do NOT promote the prototype to production and do NOT waive the failure.

**ART IDENTITY: no artistic PASS.** Even in the 24 correct smaller cases, A looks turtle/beetle-like; B more insect-like; Q1 is the old standing/frontal-axis control. Neither A nor B visibly preserves the eyes, prominent horns/ears or expressive open mouth in the user's original hand-drawn monster, though its horizontal four-legged perspective is stronger than Q1.

## 2. REAL 6507/TIA BUILDS, EXACT ROM SHA

| Candidate | Source filename under experiments/ | Genuine ROM SHA-256 (4,096 bytes) |
|---|---|---|
| **A_rounded_back** | romdev_p01_art1_A_rounded_back.asm | 13894728fb9a4804ced1954e49d3ba9b70c366b2dd254a545a14e6e1a641127c |
| **B_low_long_back** | romdev_p01_art1_B_low_long_back.asm | b307bcce4e0301304057e00d489be8f8aabf9ca7f9d34006bf4d05ff67a669b9 |
| **Q1_splayed_quad** | romdev_p01_art1_Q1_splayed_quad.asm | f80069acf7d8aa183d135aa25aa0d506ea4d90d8fba4395bf100245c0d58b82f |

DASM builds on the isolated branch use arguments -f3, -o build/ART1_NAME.bin, -l build/ART1_NAME.lst, -s build/ART1_NAME.sym. The ROM sources plus untouched exact input JSON are committed on [experiment/romdev-p01-art1-p0-stella-readout](https://github.com/Odourman/the-skraun/tree/experiment/romdev-p01-art1-p0-stella-readout). Draft [PR #18](https://github.com/Odourman/the-skraun/pull/18) targets main but is **not merged**.

**Source authority:** original [P1 A/B exact source JSON](https://github.com/Odourman/the-skraun/blob/graphics/p1-horizontal-axis-perspective-proof-20261116/graphics/skraun_p1_horizontal_axis/SKRAUN_P1_PIXEL_MASKS.json), reviewed graphics HEAD b5bc31a3485faf67199631c01768bf221f061292; [historical v0.3 original Q1 JSON](https://github.com/Odourman/the-skraun/blob/graphics/skraun-v0-3-final-readability-20261116/graphics/skraun_v0_3/SKRAUN_V03.json); original Drive P1 archive SHA-256 d716e93cf6f15f5944fb9716efffd1217d2c716dbc3909906c2ba382aa728cd1 (15 members, **design previews, not Stella**). User's actual hand drawing reviewed in Drive: ears/horns, eyes, mouth and four mobile limbs. Every logical 8x12 data bit and its mirrored facing is preserved. Q1 JSON requires key names **A_left/B_left**; new P1 candidates require **left_A/left_B**, explicitly enforced without fallbacks. The 12-row data are intentionally stored bottom-first ONLY to match this kernel's descending visual scanline index; no source bitmap content was redesigned.

## 3. ACTUAL STELLA, 36 LOGICAL STATES, 72 MOTION FRAMES

The three real programs use **P0 only** on plain black background (COLUBK=$00). Gray player COLUP0=$0C is actual Stella 6.7.1 RGB (210,210,209). NUSIZ0 0/5/7 gives 1x/2x/4x horizontal 8/16/32 TIA color clocks, i.e. 16/32/64 native PNG pixels. Vertically, the source rows repeat 1/2/3 times giving nominal 12/24/36 actual physical scanlines. B has an intentionally blank logical first row; its visible colored bbox at level 1/2 can be 11/22 scanlines even while the scheduled sprite region is 12/24. Do not mistake this for missing art.

The diagnostic state machine spends 48 frames per scale×facing, cycling **L1 right, L1 left, L2 right, L2 left, L3 right, L3 left**, automatically alternating **A/B every 8 NTSC frames**. This is a stationary animation demonstration, not gameplay or 8-way joystick code. Exact captured states are 3 candidate ROM×3 level×2 facing×2 pose =36 distinct emulator images. Additional **24 consecutive single-frame screenshots per ROM** (72 total) show the same level1/right sprite held motionless while A/B alternates; because the traced beginning was StageFrame2, the 24 sampled pictures show A6, B8, A8, B2. That is correct 8-frame switch cadence (16 frames for a complete A→B→A loop), approximately 3.75 cycles/second at NTSC60.

**DIRECT EMULATOR EVIDENCE, not an estimate:** [GitHub Actions #43947105697](https://github.com/Odourman/the-skraun/actions/runs/43947105697) actually built and ran three ROMs with DASM and Stella 6.7.1 under X11/Xvfb software rendering. Stella Debugger _scanEnd was **262 for each of the 12 state readings per ROM**. Directly recorded Stage [0,0,1,1,2,2,3,3,4,4,5,5], StageFrame [1,9] repeated, Level 1/1/1/1/2/2/2/2/3/3/3/3, Facing 0/0/1/1 repeated, Pose 0/1 repeated. The first earlier CI run mistakenly expected StageFrame 2/10; the test oracle was fixed to the actual debugger 1/9; **ROM source and ROM SHA never changed**.

**NATIVE STELLA RAW PNG, not a generated preview:** 320x228 images from Stella Debugger frame #n and saveSnap are in the artifact. Contact sheets are clearly labeled nearest-neighbor crops of these actual images, plus optional 4:3 nearest-neighbor display resize to 640x480 and APNG/GIF of consecutive emulator frames. Source PNGs remain independently available, untouched.

## 4. EXACT ROW ORIENTATION, VERTICAL-INVERSION NEGATIVE CONTROL, AND THE REAL FAIL

The strict committed [P01-ART1 pixel test](https://github.com/Odourman/the-skraun/blob/experiment/romdev-p01-art1-p0-stella-readout/tests/romdev_p01_art1_stella.py) checks individual sampled cell coordinates from **real rendered GRP0 gray pixels** and insists on entire 12 logical top-first rows, their 1/2/3 vertical duplicates and 1/2/4 horizontal scale. This is much stronger than sprite bounding boxes/pixel totals. It tests left-right mirrors and nominal four paw positions, where A/B must have the head **RIGHT in right pose, LEFT in left pose**. Q1 has its own historical *head at top* visual anatomy.

MAIN II source audit was correct: **A pose A is almost vertically symmetric**. Deliberately reversed 12-row A pose A reference differs in only **4/96 bit cells** while keeping the same bbox/pixel count. The new oracle **rejects** that inversion. A pose B's inversion changes 20/96, B pose A 28/96, B pose B 36/96. This is a **negative oracle test** with deliberately wrong reference data, NOT a fourth custom Stella ROM.

Full original-PNG analysis pinpoints **the same extra top line in all twelve level3 captures**. The first physical line in the quadruple-width mode appears as binary **11111111** regardless of actual top row. A intended top row **01000100** produces 48 extra gray pixels; B intended **00000000** produces 64 extras; Q1 intended **00100100** produces 48 extras. Each mismatch is limited to raw PNG Y=94 and has **zero missing pixels**; all later raster rows are exact. 12/36 **FAIL**. No false green pixel verdict, no hidden exception. A separate [all-36-state diagnostic ledger script](https://github.com/Odourman/the-skraun/blob/experiment/romdev-p01-art1-p0-stella-readout/diagnostics/romdev_p01_art1_full_failure_ledger.py) reports each case and every one of 72 walking frames without changing the strict failing test.

## 5. STATIC CPU VS DIRECT DEBUGGER / ROM AND RAM LEDGER

**STATIC calculated (not debugger per-instruction trace):** the real visible P0 output path from the assembler, after STA WSYNC, consists of TXA(2), SEC(2), SBC zp(3), branch not taken(2), CMP zp(3), branch not taken(2), TAY(2), LDA (MapPtr),Y max(6), TAY(2), LDA (GfxPtr),Y max(6), STA GRP0(3), JMP(3), DEX(2), BNE(3). **Worst 41 6507 cycles per visible P0-output line**, counting both possible page crossings; blank branches are shorter ~20–25. This is only isolated P0 and gives NO proof of full renderer CPU headroom.

**DIRECT measured:** 36 snapshots' saved real Stella Debugger readings all show 262 NTSC scanlines. No claim of direct per-instruction trace, original-hardware timing or PAL testing.

**RAM allocated** exactly 12 RIOT bytes $80..$8B: Stage, StageFrame, Level, PlayerX, PlayerY, SpriteH, Facing, Pose, 2-byte MapPtr and 2-byte GfxPtr. Remaining nominal 116 bytes are not allocated to this test and stack still needs separate protection.

**ROM allocated** exactly 450 emitter-address bytes at $F000–$F1C1 plus four reset vectors at $FFFC–$FFFF = **454/4096** used; unused ORG hole $F1C2–$FFFB = **3642** contiguous bytes. All three ROMs have identical layout and exactly four 12-byte A/B left/right source-compatible sprite tables. This is based on actual DASM listing and symbols, not counting only nonzero ROM binary bytes.

## 6. VISUAL READABILITY / ORIGINAL ART IDENTITY

- **A / rounded back:** better horizontal overhead body axis than Q1, visible upper/lower fore/rear paw projections and a bitwise exact head-right/left mirror. At actual level1 Stella scale, however, its round shell-shaped silhouette looks **turtle/beetle-like**, not unambiguously a troll. The original expressive grinning mouth and recognizable horns/ears are NOT clear. At bigger levels the pixel outline is bigger, not more informative.
- **B / low long back:** narrower axis, longer separated appendages, but a stronger **insect/segmented beetle** impression. Level1 is still too sparse to convey the intended personality. It does not beat A for character identity.
- **Q1 / historical upright:** recognizable as a little upright/front-facing figure, but it does NOT satisfy horizontal body axis/four-legged-overhead perspective. Correct historical control, not production direction.
- **Gait:** real A/B bitmaps do change the feet/limbs; the 16-frame cycle looks like simple paw twitching at 8x12, often merely **a few blinking pixels**. These are actual frames from the same stationary sprite, not a locomotion/gameplay proof.

**ART IDENTITY FAIL / no final artistic approval for A, B or Q1.** A is only MAIN's preferable *physical perspective hypothesis* for an eventual separate user-authorized visual design step. An authentic 4KiB emulator PASS at smaller sizes cannot confer missing horn/mouth identity. User and MAIN retain the final acceptance gate.

## 7. STATUS, HANDOFF AND STOP

| Gate | Result |
|---|---|
| Exact source provenance, 3×4096-byte DASM NTSC P0-only ROM, 4 art mask tables each | **PASS** |
| 36 actual Stella captures and 72 consecutive frame captures, 262 NTSC all checked | **PASS** |
| Full exact P0 raster orientation, scale and mirror across all 36 states | **FAIL: 24 PASS + 12 level3 first-row FAIL** |
| Deliberate vertical inversion negative reference for primary A pose A | **PASS oracle**, not an extra ROM |
| Smallest 8×12 sprite reads as unique horned four-legged Skraun | **VISUAL/ART IDENTITY FAIL or not user-approved** |
| R3 full-scene renderer 20/30Hz, arrow/orb/headroom NO-GO | **UNCHANGED** |
| P01-ART2, R4, B3c, enemies, halo, obstacles, HUD, AI, merge main, independent VERIFICATION | **NOT STARTED; not authorized** |

**Recommendation MAIN II:** accept ART1 as a bounded *honest negative feasibility/identity readout*, but NOT as a character-art or full P0 visual-correctness PASS. The precise level3 top scanline defect requires a separately authorized P0 kernel defect-fix if this diagnostic code will ever be reused. MAIN should evaluate the captured level1 actual images and original personality before authorizing any next art design step. **ROM DEVELOPMENT STOPS HERE.**

## 8. ORIGINAL EVIDENCE AND DELIVERY

- [GitHub Actions #43947105697: three real ROMs, 108 authentic Stella PNGs, 36×262 NTSC, strict source-raster test FAIL as required](https://github.com/Odourman/the-skraun/actions/runs/43947105697).
- [Draft PR #18 unmerged](https://github.com/Odourman/the-skraun/pull/18).
- [Issue #17 MAIN II tracking/hand-off](https://github.com/Odourman/the-skraun/issues/17).
- [Drive ART1 evidence folder](https://drive.google.com/drive/folders/11s5rWZTkpHVplOCRcAhGSPnzC4C-iT5l).
- One self-contained package includes exact 3 ROM and SHA, ASM, .lst/.sym, all 108 untouched original PNG, debugger trace, negative test, full 36-state ledger, nearest-neighbor actual-Stella viewing aid, GIF/APNG source-frame sequences, file checksum manifest, reproducible scripts and this report. Links added on package validation.

**No further scope is started.**

## 9. FRYST SLUTPAKET, FÖRKLARAD RÖD TESTGRIND OCH HASHKONTROLL

- **GitHub Actions reproducible package SUCCESS:** https://github.com/Odourman/the-skraun/actions/runs/43948698028 . Paketeringen PASS betyder INTE att den underkända original-Stella-pixelregressionen har gjorts grön. Workflown kontrollerar uttryckligen att originaltestet #43947105697 fortfarande har conclusion=failure och bevarar alla 12 level3-Fail.
- **En komplett inner-ZIP:** THE_SKRAUN_P01_ART1_COMPLETE_MAIN_II_DELIVERY_2026-11-16.zip, SHA-256 **3dcdc3e1837a8543e36ff9577aa7dad5528b811180b261419b2363e463a16c4e**, 361942 bytes, 285 ZIP entries, fil-CRC PASS, **275 av 275 filer i SHA256-manifestet PASS**. Innehåller 3 ROMs, 108 autentiska Stella original-PNGs, tillhörande .asm/.lst/.sym, 36 state-ledger, 72 gångframes CSV, verkliga Stella debugger-sessioner och 262-line traces, två exakta input JSON, original real-frame NN crops / 4:3 visning / APNG (~60Hz) / saktad GIF, statisk cykel/RAM/ROM-redovisning, tester och denna rapport.
- **Drive nedladdning:** https://drive.google.com/file/d/1BNS9A9KiuGHrQ1WRUwhxWwZJo05N5MGx/view?usp=drivesdk . Detta är GitHub Actions **yttre wrapper-ZIP** på 273532 bytes med inner-ZIP plus PACKAGE_SHA256.txt; packa först upp wrappern för att få ovanstående självständiga inner-ZIP. Drive metadata kontrollerad, mappen https://drive.google.com/drive/folders/11s5rWZTkpHVplOCRcAhGSPnzC4C-iT5l .
- **Full käll-/experimentrevision:** https://github.com/Odourman/the-skraun/pull/18 (DRAFT, INTE MERGED).
- **Strikt originaltest FAIL:** https://github.com/Odourman/the-skraun/actions/runs/43947105697. Detta är AVSIKTLIGT bevarad negativ faktisk evidens, inte ett fel som tyst har åtgärdats.

**SLUT: TECHNICAL FAIL som fullständigt 36/36-pixelkrav; VISUAL READABILITY begränsad; ART IDENTITY INTE GODKÄND. Inga nya sprites, P01-ART2, R4/B3c, main-merge eller oberoende VERIFICATION.**
