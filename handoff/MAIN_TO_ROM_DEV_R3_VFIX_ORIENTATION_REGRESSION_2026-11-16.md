# THE SKRAUN — MAIN AUTHORIZED CORRECTION: R3-VFIX SPRITE ORIENTATION REGRESSION (2026-11-16)

**Authorization type:** narrow defect correction and developer regression tests; **NOT R4, B3c, a renderer redesign or visual asset approval.**
**Reason:** user reviewed authentic R3 Stella images and pointed out upside-down Skraun, unrecognizable placeholder knight/archer graphics and poor placeholder backgrounds.
**GitHub issue:** https://github.com/Odourman/the-skraun/issues/15
**R3 original:** [DRAFT PR #14](https://github.com/Odourman/the-skraun/pull/14), branch `experiment/romdev-r3-decisive-scene-scheduler`, reviewed SHA `863f67780836d0057c2947dfc87612e835da731b`. Maintain the original experiment, ROM hashes, raw screenshots and original NO-GO conclusions untouched.

## A. Confirmed source-level bug, not a subjective preference

The three R3 source files use a decrementing visible line index and `lda Troll3,x / sta GRP0`, so high index data are drawn before lower index data.

Their `Troll3` table puts logical **head/ears** row `$24=00100100` at lower indexed active rows and **feet** `$C2=11000010` at higher indexed active rows. The resulting top-down display is feet-first, an upside-down player.

The older known-upright source `fix/p02-gray-halo-upright/experiments/p02_gray_static_halo.asm` uses the opposite active-row ordering for its own descending kernel and has corresponding pixel assertions in `tests/check_gray_static_halo.py`. The R3 code uses an **indexed 177-entry table** with a different active offset: do NOT blindly reverse the entire ROM or change the PF/ring tables. Work out the exact active logical row sequence, repeat factors and correct display direction.

The current `tests/romdev_r3_frames.py` only checks bounding boxes, gray pixels, translation and presence. They cannot distinguish vertical inversion of a visually asymmetric head/feet sprite. Current green CI therefore is not visual correctness proof.

## B. Authorized implementation and tests

ROM DEVELOPMENT may independently:
1. Create a separate branch `fix/romdev-r3-upright-20261116` from the frozen R3 experiment; do not commit a correction over the evidence branch or merge to `main`.
2. Fix P0's actual top/bottom orientation in **all three R3 sources** without altering the ring, horizontal positioning, mode, P1 row buffers, movement logic or design decisions. If a change beyond row data is unavoidable, log exact behavioral/cycle impacts and request MAIN decision before broadening it.
3. Add a **failing-on-original, passing-on-fixed** test for actual Stella-rendered *distinguishing pixel rows* (head/ears vs legs/feet), with ground truth taken from `docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md` and the user's fixed visual reference. Verify at x56/80/104 and during left/right input reversal, all R3 scenarios, ensuring orientation is correct at level 3 and visible shape remains 64×36 (or explain mismatch).
4. Build original-compatible NTSC ROMs with DASM, record exact new ROM SHA-256, 262 real Stella scanlines in meaningful states, actual source, `.lst/.sym`, authentic Stella snapshots and known limitations. Re-run visibility/duty tests where the fix could affect P0 occlusion.
5. Keep original R3 successes as **bounded developer timing/scheduling results** and the R3 game-architecture result as **NO-GO**, unless new test evidence requires a narrower technical conclusion. Report any pixel errors / frame timing introduced.
6. Add an **explicit visual status label** in result documentation and screenshots: `Skraun: orientation correction candidate; enemy images: temporary 8-byte test silhouettes; obstacle columns: synthetic diagnostics; HUD: placeholder; forest/mountain/dream/night artwork NOT IMPLEMENTED.`
7. Report whether the P1 test bitmaps' own vertical orientation has an analogous reversal; do not incorrectly claim final artwork is recognizable.

## C. Art constraints: do NOT conflate corrected bitmap with final graphics

The user's hand-drawn Skraun and `docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md` govern gray overhead figure, ears/head above, feet below, two-step A/B animation and horizontal mirroring (when that animation exists).

The game needs **recognizable** (not just distinct colored pixel blobs) sword knights and a green archer with bow, and four visually distinguishable world themes (forest/mountain/dream/dark-night), following decisions 01–60, but **implementing finished sprites and world backgrounds is NOT authorized in this correction**. Such assets need a separate user/MAIN visual design approval and later renderer integration. Never present diagnostic placeholder art as production art.

Do not claim that fixing orientation solves the underlying same-Y 20Hz sprite flicker, 30Hz halo/scene competition, PF color merging, 2–4 cycles of static headroom, 89-byte P1 buffer RAM pressure or arrow/orb reservation. Those remain R3's real hardware blockers.

## D. Finish / handoff

Deliver ONE corrected reproducible three-ROM developer test package to MAIN, links to new branch/PR, authentic before-versus-after Stella images, exact code differences, new SHA-256, orientation assertions that fail on the old frozen ROM, 262 NTSC confirmation, explicit known artistic placeholders and NO-GO limitation. Stop after the correction and seek separate MAIN authorization for any larger art renderer/gameplay architecture.

**No R4, no B3c, no final sprite/background creation, no `main` merge and no independent VERIFICATION.** MAIN intentionally batches independent gates later.
