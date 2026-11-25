# THE SKRAUN - ROM DEVELOPMENT IV -> MAIN V MIGRATION (2026-11-25)

DATE-SCOPED MIGRATION HANDOFF. No code changes, no MAIN acceptance, no independent Verification.

## Complete transfer
Google Drive ZIP: https://drive.google.com/file/d/1oAPDlnYL5TF9eE_xZIK3b1sStCNNSRrW/view
Name: THE_SKRAUN_MAIN_V_MIGRATION_2026-11-25.zip
Size: 12,279,203 bytes.
SHA-256: 02e8f4b0dee3b941a4c314199c0ce543eeaee6d2957245d0534a936759a8acde.
The 32-entry archive includes 00_START_HAR.md, copy-ready 01_NY_MAIN_V_STARTPROMPT.md, full status and source register, source code and 16KiB ROMs for both baselines, 491-file prior handoff, GitHub Actions evidence, source banks/build.py, screenshots, research, dated Project Sources 00-04 and manifest.

## Live-checked exact state
- FULLGAME-1 Issue #50 OPEN: https://github.com/Odourman/the-skraun/issues/50
- PR #51 draft/unmerged HEAD 8ab2840c99785b499c3499b89a23246fca026fa9.
- PR #52 draft/unmerged sparse PF experiment HEAD 7528bb52105240642fd5e1d1edce18472b8d0ee5: NEGATIVE arrow_first=263. DO NOT integrate.
- PR #53 draft/unmerged adaptive scheduler HEAD 7a2f34e267a46bfcac909a5d96d6589f98f8ec67: last frozen bounded developer PASS; actual F6 ROM d2a0a1b57ac9c78b2af14f77800f7c1ecf99aaa43f60e8c4216974f18aed2a0e (16,384 B). Actions #45530532678: 17/17 chosen end frames scanEnd 262; not all-frame/beam/hardware proof.
- Latest ROMDEV4 arrow/halo implementation: branch experiment/fullgame1-arrow-halo-romdev4-20261125 HEAD 80acf144c7bd795bf6792ca478d28c542bbd2627. F6 ROM a9189404275d4c3e5f04c246033290384c64d0ffcc127ff73229522d9a81e8a3, 16,384 B; assembler PASS, Stella REGRESSION FAIL https://github.com/Odourman/the-skraun/actions/runs/45602662669: stage2_L3=263, other 16 selected final frames 262.
- Latest CI saved 120 intermediate states but 0/120 individually observed _scanEnd values. NO 120-frame PASS. Full cycle/beam/RIOT/stack correctness unproven. A complete visible three-level 360-degree halo is not proven.
- Earlier LOCAL experiment SHA 564ac02c7a748dfe7c77c96e4b1f22a9267876959470e4fa781cb8c0a8a94fa9 has different bytes from current GitHub SHA. Its synthetic 24/24 results cannot validate newest ROM.

## Binding sources and roles
Canon: https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md
Visual direction: https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md
Frozen U1-LEG1 source: https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json
Original ROM scope: FULLGAME-1 Issue #50, max 16 KiB F6 or justified F6SC. MAIN coordinates and reviews, ROM DEVELOPMENT implements within current explicit authority, research is advisory, independent Verification is separate, and no main merge or public release is automatic.
Old dated Project Sources 00-04 / Memory / migration prompts are navigation only. Latest user decisions and exact canon override obsolete N7/MAIN III status.

## First MAIN V action
Upload the migration ZIP in the new MAIN chat; paste 01_NY_MAIN_V_STARTPROMPT.md. Confirm live GitHub and Drive access, exact branches, code/ROM SHA, then focus on stage2_L3=263 failure versus frozen PR53, physical ArrowY, readable X/Y halo on L1-L3, retained adaptive warnings. Require 17-scene Stella run, 120 actually measured consecutive frames, worst-case 76-cycle beam deadlines and RIOT/stack accounting before claiming PASS. Do not silently restart coding in MAIN or call this a finished release.

Disposition: MIGRATION_HANDOFF_READY / PR53_BASELINE_PRESERVED / ROMDEV4_ARROW_HALO_STAGE2_L3_FAILED / RELEASE_NOT_READY.
