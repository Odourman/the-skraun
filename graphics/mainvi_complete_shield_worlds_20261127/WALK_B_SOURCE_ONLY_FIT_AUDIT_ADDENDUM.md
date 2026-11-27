# THE SKRAUN — GRAPHICS II: WALK_B source-only address correction
Date: 2026-11-27

Status: **SOURCE_ONLY / static source address audit**. This is an appendix to the frozen MAIN VI graphics package (commit `a0638febaa1a21146f686c9edf92348792211eb5`), NOT a change to the frozen artwork and NOT an authorized ROM implementation.

## Source checked
- Exact PR76/C commit `bd499a0736a8ed09c9e733e90387188176870039`
- `experiments/fullgame1_arrow_halo_20261125/bank3.asm`, original Git blob `8d839fee0eb4ec4ef9708490a25672b5a4819b13`
- Original `ORG $F7A8` six 17-byte mask tables, followed by `ds 9,0`, then `ORG $F820` for `WorldPFIndex`.
- Six P1 art pointers live at `EnemyArtLo/EnemyArtHi` after `ORG $F6A8`/jump and before `ORG $F6B8`.

## Actual source-address layout (no ROM build)
| Region | Inclusive byte addresses | Bytes |
|---|---|---:|
| K1NeutralBytes | `$F7A8–$F7B8` | 17 |
| K1WarningBytes | `$F7B9–$F7C9` | 17 |
| K1StrikeBytes | `$F7CA–$F7DA` | 17 |
| R1NeutralBytes | `$F7DB–$F7EB` | 17 |
| R1DrawBytes | `$F7EC–$F7FC` | 17 |
| R1ReleaseBytes | `$F7FD–$F80D` | 17 |
| Candidate C_SHIELD_CONTOUR WALK_B | `$F80E–$F81E` | 17 |
| Still unused before WorldPFIndex | `$F81F` | 1 |
| WorldPFIndex begins | `$F820` | fixed |

**Correction to the previous MAIN_HANDOFF:** a fourth 17-byte knight bitmap **does fit as static data** in the combined original nine `ds` padding bytes plus nine implicit gap bytes: 18 available contiguous bytes from `$F80E` to `$F81F`. Therefore relocation of the mask bytes alone is **not required by the address layout**. The frozen sources and original graphic pack remain intact.

**Unresolved code-space/pointer constraint:** `EnemyArtLo` + `EnemyArtHi` currently hold six pointers (12 bytes) at `$F6AB–$F6B6`; only `$F6B7` remains before fixed `ORG $F6B8`. Simply appending a seventh low/high pointer pair overruns that fixed address. A new per-knight WALK_A/B selector and pointer path need a separately scoped ROM-side design. `SelectEnemyArtImpl` and `ChooseP1` are not modified. There may be cycle/beam-deadline ramifications for new pose selection, and there is no claim of sufficient CPU time or safe code-placement from this calculation.

## Proposed scope for a separate MAIN order, if desired
1. Preserve all original Ranger entries, P0 U1-LEG1 art, aura and gameplay.
2. Allocate WALK_B data in the verified 17-byte gap and find/measure a source-safe pointer selection method.
3. Compile with DASM; inspect listing, symbol addresses, bank sizes, RAM and stack, and exact TIA cycle deadlines.
4. Test in Stella with authentic walking, warning/strike timing, multiplex and L3 aura; compare physical snapshots frame by frame.
5. STOP/return to MAIN on failed fit or unreadable real pixels. This is **not authorized by this audit**.

**Bottom line:** `WALK_B_SOURCE_DATA_FIT = SOURCE_ONLY_YES`, `WALK_B_RUNTIME_INTEGRATION = UNTESTED`. No merge, gameplay code edit, ROM build or independent Verification performed.
