# THE SKRAUN – MAIN IV -> RESEARCH II
## GLOBAL SOLUTION SEARCH: ALL 54 CURRENT PROBLEMS, RISKS AND MISSING FEATURES
**Date:** 2026-11-22
**Authority:** The user explicitly asked MAIN IV to send ALL 54 previously listed issues to the Research chat to search for solutions, original ideas and alternatives across project archives, Google Drive, Project Sources, tools and the global multilingual internet.
**Tracking:** https://github.com/Odourman/the-skraun/issues/47
**Class:** NEW, expressly authorized RESEARCH-ONLY / SOURCE_ONLY. NOT an ROM-development order, not graphics, not independent Verification, not a new canon or final architecture decision.
**Recipient:** RESEARCH II, report recommendations to MAIN IV, then STOP.

## 0. First principle: move toward a fun, fast, PLAYABLE game

Investigate boldly, be creative, and seek solutions rather than another catalogue of reasons Atari 2600 is difficult. Reuse older research; find new technically meaningful approaches, especially for the actual hardware failures. Avoid repeating an approach already falsified without identifying exactly what DIFFERENT hardware premise you are testing.

Keep the output actionable: your central deliverable is a SHORT ranked decision memo plus traceable supporting technical evidence, not an encyclopedia. A good single microtest proposal that could unblock real gameplay matters more than dozens of generic Atari tricks.

The initial inventory is 54 QUESTIONS and status claims from MAIN IV, NOT 54 established current ROM defects. **Audit each item against exact frozen artifacts**, classify as CONFIRMED_GAMEPLAY4A_DEFECT, UNIMPLEMENTED_CANON, REAL_INTEGRATION_RISK, LEGACY_ONLY, PARTIAL_OR_UNVERIFIED, or WRONG/OUTDATED. Correct errors or misleading classifications openly with source evidence. Do not promote a previous assistant summary to authority.

## 1. Mandatory source access and authority order

1. Test access to live GitHub, relevant Google Drive, Project Sources 00–04 / Project Instructions, earlier RESEARCH I/II, MAIN/ROMDEV/GRAPHICS/VERIFICATION handoffs, and web/research tools. Open actual documents, not only titles or memory. Report any missing source or tool by name; proceed with what is available.
2. Start with Project Sources 00–04 in the ChatGPT Project files or their originals, but remember they are **dated 2026-11-21 snapshots** and not live state.
3. Highest gameplay/graphics authority: direct user decisions; https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md (including later appendices), https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md and exact approved U1-LEG1 8x12 A/B on graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json. Same sprite source at L1/L2/L3; left/right display label reversal. Approved K1-T / R1 VISUAL DIRECTION is supported by the newer user decision and Graphics II commit 4960d1661ad9764ce257a59053a981f46b09cff2, NOT by any alteration of U1-LEG1.
4. Actual executable development state, independently check current branch/HEAD, Git blobs, issues, PRs, code, real DASM/Stella logs, and SHA. Most recent user-known frozen GAMEPLAY-4A is [PR #46](https://github.com/Odourman/the-skraun/pull/46) HEAD bc2ef9249b4e13701647850d89cb631c43190c65, conventional F8 8192B binary experiments/gameplay4a_f8_ntsc.bin SHA256 8bb19a9d58b6a4f608f1ab10adbb622b9e70d0f44b39e247c68feb3a974427bd. Confirm live; do not infer the best game from main (main HEAD at drafting 46d31504cccc5d17b521f7b9f01b7aded003de1a). In that ROM real K1 neutral/warning/strike and R1 draw/release are bounded developer-observed; R1 release phase 27 has actual 263 scanlines, while the rejected M1 arrow variant gave physical 360/partial frames and is NOT present in the safe ROM.
5. GAMEPLAY-3 [PR #44](https://github.com/Odourman/the-skraun/pull/44) HEAD 07de8f907421e22b8b444200389a21c42dca330d, H1 three same-Y NUSIZ copies (322 vs expected 348 displayed blue pixels, no independent sprites) and H2 separated-Y three rows (338/338, but shared X and P1 colour) are **bounded negatives**, not universal impossibility. Read actual scripts and Stella logs. GAMEPLAY-2 [PR #42](https://github.com/Odourman/the-skraun/pull/42) is the older playable stage progression checkpoint. GAMEPLAY-1 PR #41, PLAY1-H PR #37, failed PLAY1-X PR #39, older R3 and N7/F2b PR #32 are historic technical controls.
6. Reuse prior RESEARCH I/II and reviews: [N6-C Issue #30](https://github.com/Odourman/the-skraun/issues/30), [Research II original source-only contribution](https://github.com/Odourman/the-skraun/issues/30#issuecomment-7063415027), [MAIN review of Research II](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6C_RESEARCH_II_REVIEW_AND_NEXT_GATE_2026-11-21.md), [N3 worst-case fixtures](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json), [30 previously collected Atari tricks](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_SECOND_PASS_ALL_30_ATARI_TRICKS_AND_COMBINATIONS_2026-11-17.md), N7 negative and independent audit tracking [#33](https://github.com/Odourman/the-skraun/issues/33). Do not write the same research again: **explicitly compare candidate with previous known negative or existing analysis**.
7. Search connected Google Drive for the corresponding original research bundles, archived ROM logs and art reference if those have better provenance. Do not let stale Drive summaries override frozen git code or an authoritative user decision. Search filenames and concepts, including RESEARCH I, RESEARCH II, N3, N4, N5, N6-C, N7, F2b, S2-close, PLAY1-H/X, GAMEPLAY-1/2/3/4, K1-T, Ranger R1, U1-LEG1, Atari 2600, TIA, scanlines, timing, halo.
8. Source evidence categories are always distinct: USER_APPROVED_DESIGN; SOURCE_ONLY; DEVELOPER_OBSERVED; MAIN_REVIEWED; INDEPENDENT_VERIFICATION. A paper proof or green CI is not a new Stella ROM execution.

## 2. The full 54-point coverage checklist (RESEARCH MUST ADDRESS EVERY ID)

This list is an intake inventory, not automatically true or a directive to implement. Provide one row per ID with: current status, exact supporting source, one best path, one alternative (or explain why unnecessary), risk, and whether a *new* physical ROM test is needed.

### Group A – original 6507/TIA rendering and memory (IDs 01–08)
01. GAMEPLAY-4A single real R1 release transition frame **263 instead of 262**; isolate cycle/timer/WSYNC/overscan cause.
02. M1 arrow trial makes **360 and partial raster frames**; find alternate physical missile display architecture and first failure.
03. Unproven strict <=76 CPU cycles on every worst-case physical scanline including taken/page-crossing paths.
04. Actual TIA GRP/PF/RESP/Missile write-before-beam deadlines in tough coordinates not proven.
05. Actual maximum RIOT stack depth not measured.
06. 128B shared RAM/stack pressure; adding independent enemy state/projectile can overlap live ranges.
07. F8 bankswitch state/transition across all game paths remains bounded, not exhaustively proven.
08. A complete combined native renderer for all requested actors, halo, PF obstacles, orb, arrow, HUD remains unproven.

### Group B – enemies and combat (IDs 09–21)
09. Two independent K1-T knights plus one independent R1 Ranger simultaneously present in arena not implemented.
10. H1 same-Y NUSIZ triple clones and H2 three separated Y bands do NOT solve independent same-Y actors.
11. Main playable ROM still displays only **sequential P1 enemy waves**.
12. Knight independent X/Y position/AI not complete (current practice knight chases mainly horizontally).
13. Knight pathfinding/solid-obstacle detours incomplete.
14. Ranger retreat, useful line of sight, genuine 2D obstacle-aware pursuit-avoidance incomplete.
15. **No real visible moving arrow** in safe ROM.
16. Actual arrow lock-to-target-at-release, flight velocity, collision with Skraun/halo/solid PF, removal, one-arrow limit, per-world cooldown not runtime-proven.
17. Knight sword shape extends only inside native P1's 8 columns, may look too short; visual reach vs logical reach needs congruence, M1 might conflict with arrow.
18. Source CloseForSword directional distance test does not physically test obstacle blocking: possible logical through-wall hit, to be evaluated.
19. Source-only active sword vs physical hit/miss and both facings/levels/corner cases not fully paired-tested.
20. Reserve knight arrivals after ~2s, up to two active knights, not implemented as real concurrent spawn/AI.
21. Combined actors overlap/flicker/color switching and native 8x16 art readability at tight same-Y remain open.

### Group C – Skraun, magic halo, movement/collision (IDs 22–30)
22. Visible golden PF halo reacts to player Y but **not player X** in physical playable ROM.
23. Real 360-degree ring enclosing moving P0 in all directions not proven.
24. Visible halo radius and thickness vs logical damage geometry and different levels not fully consistent/proven.
25. PF-gold/world-colour model (including solid obstacles) with BL-orb visibility and world palette not tested as final readable rendering.
26. L3 actual all 8 joystick directions, wall gliding, corners, physical scanlines/stability unproven exhaustively.
27. Growth L2→L3 near obstacles/orbs and all eight maps may create trapping situations.
28. Visual big body vs collision rectangles and corner sliding may mismatch or allow tunnelling.
29. L3 horizontal x4 vs vertical x3 proportion, same immutable U1-LEG1 source and leg readability in each world still a user visual question.
30. Current ApplySwordDamage invulnerability is 45 nominal NTSC frames (~0.75s), while design goal ~1.0s; confirm precise gameplay deviation and candidate restoration without budget regression.

### Group D – actual eight worlds / progression (IDs 31–40)
31. Only two temporary synthetic PF obstacle layouts in running game; eight distinct authentic collision maps missing.
32. User-favoured source-only forest A_Glanta not yet in running ROM.
33. Mountain world's two finished maps/obstacles and natural palette not built.
34. Dream world's two finished maps, purple palette, static spirals not built.
35. Night world's two finished maps and safe readable contrast not built.
36. Eight layout clearance tests for L3, every orb pickup, spawns and available joystick routes not complete (Issue #23).
37. Ranger forest green currently tested; mountain/dream/night world-camouflage colours/contrast not physically proven.
38. Stage traversal 1→...→8→8→7→...→1→1 and full restocking on every visit coded in source but uninterrupted end-to-end playthrough unproven.
39. Provisional stage pause source 24 frames (~0.4s) vs design ~2s + readable transition effect; assess and recommend code/gameplay fix.
40. Orb persistence on L3 and pickup during transition, once-per-visit, after death/cross-stage edge cases not all physically regression-tested.

### Group E – HUD, sound, scores, feel (IDs 41–47)
41. Visible on-screen score/HUD absent.
42. Visible lives/HUD absent.
43. GAME OVER display with final numeric score incomplete although restart logic exists.
44. Readable stage intro/transition cue and indicator missing.
45. Complete prioritized TIA two-channel sound effects and stage-change jingle missing/incomplete.
46. Long-run score overflow, extra-life every 2000 across multiple thresholds, life count bounds, 16-bit arithmetic and arcade endurance risk.
47. Game balancing: L1 hard, L2 medium, L3 deliberately OP, knights/Ranger movement and fire intervals, halo feel, flicker nuisance and subjective fun not playtested enough.

### Group F – hardware/release/legacy provenance (IDs 48–54)
48. No original-hardware production-level proof for latest GAMEPLAY-4A.
49. Hyperkin RetroN 77 / Stella 7 practical compatibility/performance not tested for this ROM.
50. Long sessions/endurance across scores, deaths, repeated stage endpoints, highest level, FIRE and moving enemies not proven.
51. The actual triple-multiplex scheme may visibly flicker/smear or lose actors under realistic overlap, including same-Y + L3 P0.
52. Total 8KiB F8 ROM/bank/RAM budget for eight worlds+full actors+halo+HUD+sfx unproven. A mapper change is **researchable alternative ONLY** and not authorized.
53. Draft PR #41/#42/#44/#46 experimental heads not merged to main; no stable production branch/release integration plan.
54. No completed independent verification of GAMEPLAY-4A full integrated engine. Historic N7 Verification II issue #33 is separately authorized but status must be checked live; don't start/close it in RESEARCH.

**Legacy warning (separate from 54 items):** ART1 [Issue #19](https://github.com/Odourman/the-skraun/issues/19) documented an old P0 L3 full-width extra top scanline in a **different historical diagnostic ROM**. It must NOT be called a current GAMEPLAY-4A defect without new matching evidence. Check how/if that cause was bypassed in current kernel.

## 3. RESEARCH: find solutions everywhere and in many languages

Do a **real exploratory multilingual search** of the public internet, not English-only or a single search engine. Aim for diverse coverage across EN, SV, DE, FR, ES, IT, PT, NL, JA, PL, RU and where relevant ZH/KO; use native technical words, alternate terminology, old machine names, original Atari VCS/2600, 6502/6507, TIA, RIOT, Stella. Count only *material* new findings, not filler. Translate accurately and crosscheck original passages/ASM. If a language yields none, say so instead of inventing search success.

High-value search environments:
- AtariAge forums, source code attachments, archive threads and developer blogs; Atari Compendium/2600 FAQs; historical Stella Programmer's Guide; Atari 2600 Programming for Newbies and advanced guides.
- Stella **current actual debugger documentation and source** for cycle/scanline breakpoints, VSYNC, queued TIA writes, debugger commands, exact register trace.
- GitHub/GitLab/Codeberg Atari 2600 homebrew source: ASM, sprite multiplex kernels, moving missile/arrow, PF renderer, HUD score, two-row/three-stream or display-list kernels; reference ROM dumps only when legal and source publicly available. Examine precise examples from real games, not anecdotal rumours.
- 8bitworkshop/Steven Hugg versatile PF and three-stream kernels; code, developer notes, demos and TIA assumptions. Prior Research already considered them; identify what is NEW and the incompatible RAM/timing/colour facts.
- Chip-level TIA/VDEL/GRP/RESP/HMOVE source docs, circuit behaviour and model differences; DASM 6502 branch/page crossing, overscan timer design, safe frame scheduling, static opcode trace tools.
- Adjacent retro homebrew communities (6502, VIC/TIA-like beam racing) as **inspiration only**, never assume their display hardware behaviour transfers to original TIA.
- Game design/playtest: sprite readability, 60Hz movement, bounded flicker frequency and pattern, recognizable physical sword/arrow and interaction affordances.

Initial independently accessible **starting sources** (not automatically accepted conclusions):
- https://www.atariage.com/2600/programming/2600_101/docs/stella.html
- https://stella-emu.github.io/docs/debugger.html
- https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html
- https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html
- https://forums.atariage.com/blogs/entry/15090-4-timing-and-horizontal-positioning-minikernel-developers-guide/
- https://www.masswerk.at/rc2018/04/10.html
- https://github.com/jigo2600/jigo2600/blob/master/doc/TIA.md
- https://github.com/monteslu/romdev/blob/main/packages/romdevtools/src/platforms/atari2600/TROUBLESHOOTING.md
- https://github.com/Odourman/the-skraun

Sample broad query families to translate/reformulate: Atari VCS multiple distinct sprites on same scanline; P1 RESP1 NUSIZ1 VDEL1 midline retrigger; cycle exact PF2 GRP1 write deadline; no extra WSYNC overscan 263 frames; M1/M0 projectile two scanline enable raster outside hot kernel; source code of multisprite games; RIOT 128B stack highwater; asymmetric PF moving halo behind solids; original-hardware compatible efficient world map compression; multisprite flicker scheduling. Search dated forum posts, archived documents and technical answers rather than only recent SEO pages.

**For each useful external finding:** URL, author, date (or undated), original language, relevant quote or correctly paraphrased specific mechanism, exact register/CPU constraints, licence if code reuse proposed, applicability to OUR 8KiB F8 kernel, conflicts with actual prior fails, and reproducible tiny test to validate. Do not assert a game uses a trick just because somebody guesses it does. If no ASM and no reliable evidence, mark UNCONFIRMED INSPIRATION.

## 4. Prioritized technical work packages (quality over volume)

### A. Find actual root cause of R1 263-line frame and improve safe kernel budget
- Start from exact GAMEPLAY-4A assembler and real 5-phase Stella inputs: R1 phase 18=262, 21=262, 24=262, **27=263**, 30=262. Compare branches, all potential \`WSYNC\` paths, \`INTIM/TIM64T\`, VBLANK/overscan and each per-row P0/PF/P1/BL load including page crossings.
- **Do not guess** "the extra WSYNC is cause" without a model matching the failure transition. Build a table of 6507 instructions/cycles and **real TIA colourclock deadlines**, state changes and separate complete-frame counts; identify 1–3 discriminating observables and cheapest single authorized future ROM microtest.
- Look for simplifications which keep U1-L3, six P1 poses, orb, game-state and render correctness. Consider replacing an indirect draw with precomputed VBLANK pointer/row schedule or a leaner critical loop; quantify code size vs cycles and ROM bank placement. Do not insert an unmeasured timing patch into production code.

### B. Real Ranger arrow without a broken 360-line kernel
- Start from attempted M1 \`LDA (ArrowRowPtr),Y; STA ENAM1\` inner visible line and safe checkpoint's absence of it. Compare M1 vs M0 resource ownership and colours, correct RE(S)M positioning/HMM/HMOVE, relevant collision hardware flags, precomputed vertical enable / two line edge toggling, alternative compact missile raster scheduling, possible visible-only gating on sparse scanlines, offscreen row state, or a physically separate arrow colour/bitstream.
- State why **each** candidate has sufficient 76-cycle budget including the existing P0/P1/PF/BL writes, enough RAM incl stack and actual X/Y independent movement and useful one-arrow trajectory. If using M0, remember its colour shares P0; if using M1, it shares P1. BL orb cannot be stolen, and no invisible damaging projectile accepted.
- Require a real world-block and halo intercept plan, shot aim sampled at release, fixed direction thereafter, cooldown by world and max one in air. Source logic in the 360-line rejected branch is only an advisory fragment, not proven gameplay.

### C. Three independent actors: identify genuinely different physical render ideas
- Preserve two independently positioned light-blue knights and one world-camouflaged R1 Ranger, all **alive at the same time**, with independent X/Y, including S2-close historical **K1 x67 K2 x83 R x101 at Y78** and S3 with P0 L3 occupied. Both knights should still have readable 24f sword telegraph and strike, Ranger bow and arrow.
- Compare and build per-scanline resource ledger for: true P1 midline reuse/retrigger (RESP/GRP/COLUP/REF/NUSIZ, VDEL semantics), partial preloaded multi-scanline display schedule, controlled line interlace/flicker duty (report actual perceptual compromise, don't silently adopt), P0 loan only on rows where Skraun physically absent, altered object allocation for Ranger silhouette (M0/M1/PF at visible native quality), and any credible **novel** trick from external code.
- Explicitly explain why older N6-C F1/F2a, N7/F2b S2-close, GAMEPLAY-3 H1/H2, and R3 low-refresh failures are NOT the same as the candidate, or reject candidates that duplicate those failures. **No source-only chart is a physical PASS.**
- If strict same-Y fully distinct art appears physically infeasible under conventional kernel, rank 2–3 user-visible choices such as bounded localized row striping, short controlled flicker, visual spacing with unchanged logical concurrency, or more powerful original-console-compatible cartridge bank/RAM logic. Quantify impacts and **require new user authorization** before any compromise or mapper change.

### D. Moving X/Y magic halo and PF/BL colours
- Seek a physically credible dynamic 360° halo whose *visible* gold field follows BOTH player X,Y and visibly grows/thickens with L1/L2/L3, while logically crossing solids; preserve fixed solid visual geometry/collision and BL orb ownership. Avoid rejected PLAY1-X second PF2 write/CTRLPF mirror hack (measured broken scanlines and geometry).
- Compare source-only geometry: asymmetric PF buffers, ROM-driven row masks, 2-physical-line schedules, 8bitworkshop-style streams, selective PF write changes, blocky "rounded" halo alternatives, temporal colours, playfield shape vs logical attack hitboxes.
- Account for test colour model B (whole arena PF gold ON vs world OFF), including contrast under attack, world-camouflaged Ranger and orb readability. State which visual features require **additional** PF register writes before beam; identify test scene / first missed deadline if unworkable.

### E. Smooth L3 collision + eight real stages + arcade presentation
- Offer practical compact eight-layout representation with 4 world palettes, a few distinguishable solid obstacles each, world colour camouflage and static dream spirals, valid full L3 32x36 movement, sliding, safe growth/respawn, visible orb positions, two/three/four knight total-wave quota and reserves with at most two active.
- Account for real P0 8x12 bitmap scaling to L2/L3, 8 directions, no fake collision shrink, and defend all level3 routes with a reproducible **source-only path/growth model** before ROM.
- Seek simple scoreboard/lives HUD arrangement that does not steal vital per-row display resources; world transitions ~2 s, looping endpoint repeats 8/8 1/1, correct 2000 bonus arithmetic and 16-bit overflow behavior. Give actionable two-TIA-channel SFX ideas, priority conflicts and readability/accessibility/balance studies. Sound/playability are secondary to actual critical four technical blockers, but do not ignore them.

### F. Hardware correctness, QA and integrated plan
- Propose a **small risk-based** test plan for Stella vs real NTSC Atari/2600 compatible cart vs RetroN 77/Stella7, not an extra verification loop after every small test. Clarify what can only be proven on original hardware or with instrumented Stella logs; do not conflate screen captures with per-instruction timing.
- Compare realistic memory/cycle/ROM budgets on F8 (two 4KiB banks) with future source-only alternatives; no automatic expansion. Show minimum dynamic state and stack highwater strategy.
- Retain legacy ART1 Issue #19 separately and explain when it is relevant to current P0 L3 code, not as current defect by default.

## 5. Output contract: ONE compact decision packet plus reproducible technical appendix

Publish on an isolated **research branch** (suggestion: research/mainiv-54-issues-solution-hunt-20261122), not main, and deliver to MAIN IV via GitHub Issue #47. Reuse old evidence; no massive new general-history document. Suggested files:

1. **00_MAIN_DECISION_BRIEF.md**: 1–3 pages, key discoveries, ranked top FIVE approaches, for each: issue IDs, why promising vs last actual failure, risks, smallest ROM/Stella experiment MAIN might explicitly commission, go/no-go data to collect. End with a one-sentence **recommended next playable development step**.
2. **01_ALL_54_ISSUES_MATRIX.csv**: 54 rows with exact ID, actual evidence/commit, classification, severity, primary and alternative solution, source URL, outstanding physical test, confidence. Label historical-only cases accordingly. The previous MAIN list is input, not acceptance.
3. **02_TOP_TECHNICAL_CANDIDATES.md**: 5–10 strongest genuinely different approaches. For each record original source/link/language, full applicable TIA object owner, worst-case instructions/6507 cycle-window and beam deadline assumptions, RIOT live+stack, F8 ROM impact, case S2-close/L3 collision/halo when relevant, failure condition and reproducible bounded smallest physical test. Source-only calculation allowed, NEVER fabricate tested Stella.
4. **03_GLOBAL_SOURCE_REGISTER.md**: original-language references, translations, exact contribution, dates, search queries and jurisdictions/language reach, reliability and reuse/permission status. Document multiple linguistic routes, not a fabricated source count. Include negative searches when useful.
5. Optional **04_REPRO_SOURCE_ONLY/**: tiny pure Python or equivalent scripts, input SHA, deterministic output, only if they independently falsify an important candidate, not as a task in themselves.

**MAIN-facing final response must be concise**, with top 5 evidence-backed findings, best technical next step, 2 backup paths, cost to fun/playability, and links to packet. Do not merely say "need more research"; ask for one specific separate experiment if research supports it.

## 6. Strict boundaries & STOP
- **RESEARCH ONLY / SOURCE_ONLY**: research can inspect public documents, issues, past code and make non-executing source models, but may NOT edit gameplay ROM/ASM production sources, run a new ROM-development sprint, release graphics, change approved canon, choose new mapper or merger, trigger independent Verification II or declare full TIA feasibility from unexecuted estimates.
- No N8/N9/new GAMEPLAY-5 or later authorization is implied. Previous developer STOP remains intact.
- Existing achievements must remain: original upright light gray U1-LEG1 same A/B on all levels and correct left/right, eight-direction smooth L3 movement, 360° halo through solids, two knights + Ranger simultaneously, 8 open distinct worlds, world-coloured R1, readable K1-T T visor/sword, BL orb, score/lives and fast playable fun. Proposed changes to any of these are **OPTIONS for explicit user approval**, not silent decisions.
- Separate developer-observed from MAIN-reviewed and independent Verification; cite actual evidence and say NOT VERIFIED where evidence lacks.
- Finish once there is decision-grade evidence and the **top-ranked smallest next original-hardware compatible physical experiment**. Deliver source-only artifacts, post final short summary to [Issue #47](https://github.com/Odourman/the-skraun/issues/47), **STOP**. A GitHub issue/handoff does not automatically start your separate RESEARCH II chat.