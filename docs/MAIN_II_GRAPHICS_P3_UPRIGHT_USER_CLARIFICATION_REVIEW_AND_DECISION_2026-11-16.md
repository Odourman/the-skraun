# THE SKRAUN — MAIN II: GRAPHICS P3 UPRIGHT-CHARACTER REVIEW AND VISUAL CLARIFICATION
**2026-11-16 | MAIN decision | Design only | NO final art or ROM approval**

## Authority clarification — direct user instruction supersedes earlier interpretation
The user directly specified: **The GAME IMAGE/PLAYFIELD is viewed from above, but SKRAUN always STANDS UPRIGHT in the drawn sprite; it has only horizontal LEFT and RIGHT visual facings as exact mirrors; moving up/down must not rotate the figure or add up/down facings.** The previous P1/P2 horizontal BODY AXIS / quadruped-prone/skraun lying on the ground was incorrect.

**Implementer interpretation for design review:**
1. World/playfield/gameplay are overhead.
2. Skraun is rendered as a stylized **upright, head-above-torso, arms-outward, two legs/feet below** character. Do not turn it into a prone animal/crab/turtle/insect.
3. Exactly two sprite facings LEFT/RIGHT, left is **bit-exact horizontal mirror** of right. Movement may be eight-way under decision #46; when moving vertically, retain last horizontal visual facing. The precise joystick input implementation is a later ROM task, not implemented here.
4. **Do not impose a physically literal optical 90-degree-overhead view of the troll's FACE as a separate hard acceptance gate.** The user wants the **game image** overhead and the **character upright, recognizable**. Atari-style symbolic facial visibility is an artistic convention, not permission to change game-plane camera or make a lying side profile. A face that looks somewhat frontal in an upright sprite is not by itself a FAIL; readability, identity, and facing remain subject to user approval.
5. Original [design decision 01's phrase 'fyrfotat'](DESIGN_DECISIONS_01-60_2026-11-16.md) and earlier [visual direction](SKRAUN_VISUAL_DIRECTION_2026-11-16.md) are preserved as historical source wording, but their **prone/four-paws anatomical interpretation is superseded** by this newer direct user instruction for VISUAL PRESENTATION. The original 360-degree halo mechanic and all gameplay decisions are unchanged. Do not silently rewrite historical decisions or art sources.
6. The private original user drawing remains in Drive and must NOT be inserted in public GitHub or graphical ZIP.

## Evidence independently audited by MAIN II
- [GRAPHICS P3 source branch](https://github.com/Odourman/the-skraun/tree/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead), 9 **added** text/source files vs current main, zero modifications of old sources, not merged. No P3 PR found at review.
- Downloaded exact full [Drive P3 ZIP](https://drive.google.com/file/d/196UpbC1Kl400BcMj5zZ44Y48p7-WW7-W/view), **321411 bytes**, SHA-256 `84129bc78fa5a0884fb3866fe6b20f18ba7b4ff2b0f3d2aa2d784431b2d86a2a`. ZIP CRC PASS; 41 members; **40/40 manifest SHA-256 PASS**.
- Executed shipped `validate_p3.py`: PASS for **exactly two new 8×12** U1/U2 source families, frozen historical Q1 and P1-A controls, A/B motion, exact per-row horizontal reversals, 16 true-size BMP-equivalent PNG glyphs, 6 two-frame GIFs, 4x3 nearest-neighbor source previews, and nonexecutable assembler art data. In a separate clean copy, ran `generate_previews.py`: **33/33 regenerated PNG/GIF files byte-for-byte identical**, validator still PASS.
- Inspected full original user hand drawing **privately**, P3 `00_MAIN_II_P3_DECISION_SHEET.png`, `03_L1_UNZOOMED_CONTEXT_CROPS.png`, `05_EXACT_8x12_ROWS_ALL_DIRECTIONS.png`, `09_UPRIGHT_VS_PRONE_DIRECTION.png`; authentic P01-ART1 Stella exists for historical reference but **all P3 imagery is design-only, not Stella**.

## Comparative evaluation at actual L1
- P1-A is indeed the old prone body-axis negative control, **not preferred future character representation**. This is a correction of P1/P2 interpretation, not new sprites mysteriously becoming wrong pixels.
- Frozen Q1 is upright but with a simplified almost frontal silhouette and weak distinct left/right visual facings.
- **U1 (head-priority)** now stands recognizably more upright and retains two horn points, dark eye holes and mouth shape more faithfully to the user original than U2. But features remain very small at actual level-1 8×12; **not final user aesthetic PASS**. U1 A/B source changes **7** bits.
- **U2 (body-priority)** has stronger shoulders/arms and separated legs/feet, but loses original face/personality and looks more like a generic figure. U2 A/B source changes **8** bits.
- Even source-exact left/right mirror is **not proof that the two facings look distinguishable at 8×12**. For U1, right-vs-left changes **10 of 96 source cells** in pose A and **12/96** pose B; many facial/crown rows are nearly symmetric. Evaluate perceptual facing separately before final art approval.
- Treat author report's **'strict overhead + identity not proven'** carefully: the goal of a physically strict overhead view **of facial anatomy** was incorrectly treated as equivalent to the user's overhead GAME camera. Do not reject U1 solely for a stylized front-readable upright face. Nonetheless, neither candidate is yet user-approved.

## MAIN formal disposition
1. **GRAPHICS P3 STUDY ACCEPTED AS COMPLETED, REPRODUCIBLE SOURCE-ONLY WORK**, not production art or Stella proof.
2. **U1 selected only as current visual direction/reference**, not final sprite and not production-source promotion; U2 remains comparative reserve, Q1 upright history, P1-A prone negative reference.
3. **Visual approval gate #15 remains OPEN** pending user assessment of U1 at actual size and two directional facings; no more unbounded art iterations. Original identity not waived.
4. No P4/v0.4, P01-ART2, ART1 L3 fix, ROM DEV, R4, B3c, change in dimensions, merge, independent Verification, enemy/world/halo production scope are authorized. [ART1 L3 defect #19](https://github.com/Odourman/the-skraun/issues/19) and R3 full-engine technical NO-GO remain unchanged. [P01 independent gate #1](https://github.com/Odourman/the-skraun/issues/1) OPEN.
5. Next high-value action: **get user visual assessment of the real original-size U1/U2/Q1/P1-A comparison under the CORRECT upright character instruction**, especially whether U1 approximates their intended troll; only then consider a separately scoped real Stella test or alternative sprite representation. No automatic work begins from this document.
