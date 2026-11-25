# THE SKRAUN | MAIN V och ROM DEVELOPMENT — REVISION 2 SOURCE_ONLY

**Inget implementationsuppdrag.** R2 kandidatdata för PR60 baseline `2af9855fbe8d3edbe6d01609d3e539547b744aef`.

När MAIN ger separat ROM-order: byt enbart tabellraderna efter `ORG $FA00` och `PlayPF1:` i `experiments/fullgame1_arrow_halo_20261125/bank3.asm` fram till `ORG $FD00` mot **03_PLAYFIELD_DATA.asm**. Kontrollera ORG och bevara befintliga `WorldPFIndex`, `Visible`, `VisibleArrow`, `WorldPFPtr`, `CTRLPF`, bankning och all fiend-/U1-kod. **PF1-byte 768, hash `253bd7180259cf699a4315379b900ca47801ae6259f0955a002bc601f5ef98f8`.**

Rekommenderade (ej införda!) WorldRects i `05_COLLISION_RECOMMENDATIONS.json` och `05_COLLISION_CANDIDATES_NOT_APPLIED.asm`, totalt 8×16 byte. Kontrollera byteordningen `x0,x1,y0,y1` med bank0 `InstallWorldMap` och `CandidateValid`; behåll kollisionsmodell separat från synlig port-/spiralöppning. Front-end använder fyra verkligt solida AABB, inte pixel-maskkollision.

Färger och guldfärgade hinder under halo, spelarnas storlekar, sprites, kontroller, AI, orber, pilar och nivå-3-regler ändras inte.

Före GO: fysisk Stella med verkliga spelinput, samtidiga fall, 262 NTSC, TIA beamdeadlines, korrekt synlig mask/ordning/mirroring, kollision/diagonalglid vid L3, säkra orbpositioner. SOURCE_ONLY BFS är inte oberoende verifiering. Ingen merge utan nytt beslut.
