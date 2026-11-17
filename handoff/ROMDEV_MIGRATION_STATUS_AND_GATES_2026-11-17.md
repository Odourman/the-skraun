# THE SKRAUN — ROM DEVELOPMENT MIGRATION: VERIFIED SOURCE STATUS AND GATES
## Snapshot 2026-11-17; **documentation-only handoff**, never an implementation authorization

**Purpose:** preserve the exact ROM DEVELOPMENT role, evidence, source of truth, and active scope when handing from an old conversation into a clean new one. Future chat MUST check live GitHub, Drive and latest MAIN decisions. Nothing in this handoff changes canon, closes a gate, approves art, alters a ROM or authorizes a later step.

### 1. Authority and ownership

1. User's explicit gameplay/visual instruction and later decisions, MAIN II's concrete binding scopes and approvals.
2. The **actual current main** branch docs, relevant named authorization and latest MAIN issue decision, including user-approved GRAPHICS source references (exact original JSON and bitmap hashes).
3. Actual experimental branch commit, PR, original files, evidence ZIP and genuine DASM/Stella/Debugger output for the scope at issue.
4. Research/30-trick feasibility studies as **advisory**, not authority to implement or change user design. Chat history and Memory can guide discovery but do not certify latest state.

**MAIN II:** coordination, acceptance, new scope, sequencing and user decisions. **ROM DEVELOPMENT:** implements only explicitly authorized isolated ROM work, executes developer self-tests and reports. **GRAPHICS:** separately approved artwork studies and exact sprite source. **RESEARCH:** advisory. **VERIFICATION:** independently checks a substantial frozen package only when MAIN explicitly requests it. One role must not silently become another.

Root: https://github.com/Odourman/the-skraun . Current Github main is changing through other conversations: **read live HEAD**, not any fixed SHA below. Root Drive folder: https://drive.google.com/drive/folders/1tSipzf7bucrqFOwHBEH61fKvyl0z7D1z . The historical docs/PROJECT_STATUS_2026-11-16.md contains many append-only older 'LATEST' sections; **read to the actual end** and reconcile against later issue comments. The legacy handoff/ROM_DEVELOPMENT_START.md describes an OLD static-gray-halo assignment; valid general role rules remain, but its 'current task' is NOT authoritative.

### 2. Chronology and frozen historical outcomes

**R1/R2/R3** (all isolated diagnostic experimental branches; no main merge; no independent verification):
- R1 PR #12, R2 PR #13, R3 PR #14, original research and actual DASM/Stella deliverables remain historical. R3 same-Y three enemies each visible 4/12 NTSC frames=20Hz; partial 30/30/60Hz and vertically staggered 60Hz possible only with Y separation. Gold halo versus blue synthetic scenery compete at 30/30Hz on alternating frames or merge as one PF color. Worst physical 6507 visible scanline path has only ~4/3/2 statically calculated cycle margin under R3 probes. Real project requires two recognizable knights, green archer, orb, arrows, halo, HUD, eight real maps, 8-way responsive motion; this coexistence has **NOT** been proved. Original technical conclusion: **R3 FULL SCENE NO-GO**, not an absolute impossibility theorem for every future renderer/mapper.
- R3 original Skraun upright regression found; isolated [R3-VFIX PR #16](https://github.com/Odourman/the-skraun/pull/16) corrected exactly 36 active P0 table bytes per candidate, with original 57 Stella images failing new top/head test and 57 corrected passing; original R3 ROM and photos untouched, no approved new enemies/scenery/world assets. MAIN received this bounded developer correction; no broader architecture improvement or art approval.
- **P01-ART1:** three original 4K NTSC P0-only ROMs with exact historic P1 A_rounded_back, P1 B_low_long_back and original v0.3 Q1; 36 Stella candidate × level × pose × facing captures, 72 additional consecutive real Stella gait frames; debugger 36/36 observed 262 NTSC lines. Exact full rendered bitmap test **24/36 PASS, 12/36 FAIL** (ALL level3 snapshots have spurious full-width 64-pixel gray top scanline at raw PNG y94). Artifact build success is not pixel-test PASS. P1 A turtle/beetle, P1 B insect-like, Q1 too front/upright; no approved original expressive troll identity. MAIN II **accepted diagnostic package as complete without approving renderer/art**, and **closed tracking issue #17** on 2026-11-16. MAIN opened/retained [defect #19](https://github.com/Odourman/the-skraun/issues/19) WITHOUT repair authorization. Original [draft PR #18](https://github.com/Odourman/the-skraun/pull/18) stays unmerged; strict failing test https://github.com/Odourman/the-skraun/actions/runs/43947105697 stays red, green package-only run https://github.com/Odourman/the-skraun/actions/runs/43948698028 is just audited packaging.
- ART1 full original evidence [inner 361942-byte ZIP in outer Drive ZIP](https://drive.google.com/file/d/1BNS9A9KiuGHrQ1WRUwhxWwZJo05N5MGx/view?usp=drivesdk), inner exact SHA256 3dcdc3e1837a8543e36ff9577aa7dad5528b811180b261419b2363e463a16c4e; source/real outputs in [ART1 technical report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-p01-art1-p0-stella-readout/docs/ROMDEV_P01_ART1_MAIN_II_STELLA_VISUAL_READOUT_2026-11-16.md). 285 inner ZIP entries/275 manifest hashes independently checked by MAIN II. Do not rerun/repair older ART1 automatically; it is frozen diagnostic evidence.

### 3. Current user-approved art and Level3 design

Earlier horizontal P1 candidate A and Q1 are NOT the authoritative player bitmap for COL1. Later MAIN's [Level3 movement gate](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_LEVEL3_ARENA_FREE_MOVEMENT_AND_COLLISION_GATE_2026-11-16.md) and explicit COL1 work order identify **U1-LEG1** as user-approved source art for the single-player test, kept bit-exact with A/B poses in three sizes, and horizontal visual label reversal: **visual RIGHT=LEG1 source LEFT; visual LEFT=LEG1 source RIGHT**. Current exact source: https://github.com/Odourman/the-skraun/tree/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1 . The intended sprite is light gray overhead, caprine/monster, four legs, original user horn/eye/mouth identity. Any other visual changes must go through MAIN/GRAPHICS, not ROM DEV.

L3 remains 32 color-clock width×36 scanline height; moving/fighting must remain comfortable even at size3 on eight planned spacious worlds. Sparse obstacles and safe orb pickup, safe spawning, sliding along walls without corner-clipping, halo passing through solids and 8-way movement remain rules. The official eight map sources are NOT approved or implemented in the test. K0 source-only study used synthetic maps and failure controls and is **not a completed game physics ROM**.

### 4. Latest already authorized P01-COL1, separate active draft

Binding MAIN II order (READ WHOLE FILE): https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_ROM_DEV_P01_COL1_ONE_ARENA_COLLISION_DIAGNOSTIC_AUTHORIZED_2026-11-16.md .

Tracking [issue #24](https://github.com/Odourman/the-skraun/issues/24) open. New active development [DRAFT PR #27](https://github.com/Odourman/the-skraun/pull/27) on experiment/p01-col1-single-arena-collision-20261117; base main. Snapshot while inspecting: PR HEAD d970c4ccf5fe23123ace5486a37b72825f193fa5. **PR #27 and main may change within minutes; always fetch live HEAD before any updates.** Its source files include experiments/p01_col1_single_arena.asm, tests/col1_source_oracle.py, tests/col1_cpu_runtime.py, and .github/workflows/p01-col1-stella.yml.

COL1 authorization: build exactly ONE 4096-byte NTSC original-compatible ROM P0-only with exact U1-LEG1 A/B both facings; one temporary SYNTHETIC open four-hinder playfield arena, all three levels, real 8-way joystick, strict K0 original X/Y projected-axis and diagonal legal checks, no tunneling, smooth wall sliding, level2→level3 growth rejection when collision, no gameplay enemies or halo, true TIA sprite/PF semantics, actual 262 NTSC and believable CPU/RIOT/stack resource evidence. K0 original Drive frozen source model: https://drive.google.com/file/d/174OGOSl7eHkAqAtB53oFWTTrVlclTcre/view , SHA256 7f69f2a2c699ccd417be78e94f2cc44680d5c581fa83ff619e228869e8f57537 . User-approved U1 LEG1 sprite not redrawn.

**Snapshot of current developer testing, not an acceptance:**
- Actual source oracle had 332232 comparisons and separate 6502/RIOT model PASS in newest checked CI [#44073915789](https://github.com/Odourman/the-skraun/actions/runs/44073915789). The DASM actual 4K build + listing/symbol had passed that step.
- **Real Stella GUI test STOPPED/FAIL** with shell error "pid: unbound variable", before capture/orientation/262 scanline could be established. This is a testharness runtime issue, not proof of all-source/ROM correctness. A newer CI #44074141244 was IN PROGRESS while the migration documents were created; **retrieve current latest CI instead of treating either as final**.
- Source-only and CPU emulator model outputs cannot be labeled actual Stella or direct physical-6507 cycle traces. No actual COL1 independent VERIFICATION.
- PR #27 is an active possibly concurrent work branch. Before modifying it: check latest sha, issue24 and its authorizations, newer comments, newer commits, workflow results, and other current writers. Never reset, cherry-pick blindly, or overwrite another session's work. If occupied, read/report and coordinate with MAIN rather than race.

### 5. Parallel RESEARCH is NOT ROM authorization

[PF-REP1 issue #25](https://github.com/Odourman/the-skraun/issues/25) and [DRAFT PR #26](https://github.com/Odourman/the-skraun/pull/26) study source-only TIA/PF shape and color deadlines, mouse/missile/P1 channel ownership, Venetian line alternation and negative constraints. The latest MAIN report on main [PF-REP1C](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_SOURCE_AUDIT_2026-11-17.md) summarizes that no simple multi-lane/colour solution has been proved for combined R3; not a full kernel GO. This is research, not permission to start R4/B3c, new special mapper, weaken user's P0/halo/obstacles/night/characters or drop approved game features.

### 6. Gate disposition to preserve

- [#1](https://github.com/Odourman/the-skraun/issues/1) P01 independent verification: OPEN.
- [#15](https://github.com/Odourman/the-skraun/issues/15) visual art/character/world gate: OPEN.
- [#17](https://github.com/Odourman/the-skraun/issues/17) P01-ART1 deliverable TRACKING: CLOSED after MAIN II receipt, DOES NOT signify all-state TECHNICAL PASS.
- [#19](https://github.com/Odourman/the-skraun/issues/19) ART1 L3 first-scanline defect: OPEN, NOT authorized fix.
- [#23](https://github.com/Odourman/the-skraun/issues/23) Level3 map navigation gate: OPEN.
- [#24](https://github.com/Odourman/the-skraun/issues/24) P01-COL1 isolated single-arena collision ROM: OPEN, **authorized only within its binding work order**, active PR27, no all-runtime PASS yet at inspected snapshot.
- [#25](https://github.com/Odourman/the-skraun/issues/25) PF-REP1 research source-only: OPEN.
- #18 and #27 are **draft unmerged PRs**; main untouched by the old experiment deliverables. Independently verify live gates before acting.

### 7. What the successor must do

Start by actually reading main HEAD/last status section, MAIN's exact COL1 authorization, PR27/issue24 source and latest CI, U1-LEG1 approved masks and K0 reference in Drive. Issue a **MIGRATION RECEIPT** identifying scope, exact refs and what is missing. Within the **already authorized** one-ROM COL1 work ONLY, pick up from the current source tip if no race, produce real test evidence or a truthful negative outcome; otherwise present the blocker. Do not invent a future full-scene renderer fix, fix ART1 #19, invent sprites/maps, merge code, run independent VERIFICATION, or start R4/B3c/P01-ART2 without an explicit new MAIN order. Stop and deliver to MAIN II at the end of authorized scope.

### 8. Evidence hygiene and reproducibility

For each actual ROM diagnostic, report: source ref/commit and changed paths; exact 4096B BIN SHA256; genuine DASM command, .lst/.sym; actual original Stella/Debugger images and 262 trace; joystick/motion/collision negative controls; 6507 CPU static budget separately from debugger-measured timing; real RIOT RAM stack margin and 4K ROM use; failures, untested states and exact reproducer; source-only research not disguised as runtime proof; artifacts links in GitHub and Google Drive. Do NOT label artificially generated bitmap previews or unrun models "Stella".

**MIGRATION DOCUMENT STATUS:** informational/coordination only. New documentation lives on handoff/rom-development-new-chat-migration-20261117 as a draft PR, separated from production main and from active COL1 branch. It changes no physical ROM source, sprites, game canon or existing gates.
