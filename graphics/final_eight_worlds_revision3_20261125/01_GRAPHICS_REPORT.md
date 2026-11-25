# THE SKRAUN — GRAPHICS II / MAIN V — FINAL WORLD GRAPHICS REVISION 3

**2026-11-25 | SOURCE_ONLY | Requires MAIN V + user visual approval.**

Revision 3 is a tightly scoped correction of **exactly three** R2 base motifs:
1. Stage 1 bottom leaf tree `01_round_A`: visible narrow trunk from 5 to **8 PF1 entries** (10→16 rasterlines); rounded crown retained.
2. Stage 2 bottom leaf tree `02_round_B`: visible trunk from 4 to **8 PF1 entries** (8→16 rasterlines); asymmetric seven-cell canopy and bit7=0 for REPEAT retained.
3. Stage 4 top mountain `04_peak_B`: apex brought near the middle; slopes broaden on **both** sides into the same 7-cell wide base, with the same exact bounding box and placement.

**All 13 other original R2 motifs are completely unchanged.** All 8 world tables remain 96 bytes each; stage 3/5/6/7/8 entire PF1 tables byte-identical to R2. Stage 1/2 upper firs and stage 4 bottom rounded mountain also identical.

| Proof | Outcome |
|---|---|
| Frozen R2 head | `299de38d6e8fbefbc1057d70682b56b76dd177f2` |
| R2 source-byte SHA256 | `253bd7180259cf699a4315379b900ca47801ae6259f0955a002bc601f5ef98f8` |
| **R3 source-byte SHA256** | `c879daa4b5bcc1bb19aa71ee632c48996b0885963bd102dd8e76bd50761354d4` |
| Bytes changed | **32/768** = 9 on stage 1, 14 on stage 2, 9 on stage 4 |
| Original PF1 format | 8×96B; 2 real rasterlines/table byte; mirror odd and repeat even |
| AABB collision proposals | All **32** bounding boxes recomputed and **numerically unchanged** from R2 |
| Source-only L3 geometry | All eight tested free-center models connected from spawn |
| New DASM / Stella rendering | **NOT RUN**; no genuine new ROM screenshots |

The R3 previews are generated directly from the exact new PF1 byte stream with nearest-neighbour scale. Original approved art and R2 preview are preserved in the complete ZIP. R3 has no extra TIA writes, RAM, kernel modifications, mapper changes or sprite edits.

**Full 123-file package:** `THE_SKRAUN_MAIN_V_FINAL_EIGHT_WORLDS_REVISION3_SOURCE_ONLY_2026-11-25.zip`, 518866 bytes, SHA256 `065d41688bf3610f7cf2040809686b279f996a89d998947219ebe94329231a97`; 122 SHA entries and ZIP CRC pass, reproducible generator. [Drive mirror](https://drive.google.com/file/d/1GO0H469DbTpf3qWYxhDvDQPJOozirH5g/view).

**STOP:** No integration order, no independent Verification and no main merge.