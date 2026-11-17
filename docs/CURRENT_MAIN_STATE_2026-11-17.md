# THE SKRAUN — MAIN III ENTRY STATE / STATUS SNAPSHOT
**Kontrollerad 2026-11-17 av MAIN II. Ny MAIN III måste alltid verifiera live GitHub och Google Drive.** Detta är ett kort mottagningsindex, inte ett nytillkommet gameplay- eller implementationsbeslut.

## Överlämningen
- Full Github-migration: [MAIN II → MAIN III](../handoff/MAIN_II_TO_MAIN_III_MIGRATION_2026-11-17.md).
- Exakt startprompt: [MAIN III startprompt](../handoff/MAIN_III_STARTPROMPT_2026-11-17.md).
- Full Drive-migration: https://docs.google.com/document/d/1QdaWnlqMevGmjX6gaYUttTCvJ7yn0XCPukBEpUzyEfA/edit
- Drive-startprompt: https://docs.google.com/document/d/1XLphoOEHNGxGH5mC4Yd6BJCDflOyx56xYuEBPIYyGwo/edit
- Projektets Drive-mapp: https://drive.google.com/drive/folders/1tSipzf7bucrqFOwHBEH61fKvyl0z7D1z
- Full historisk GitHub-status (mycket lång): [PROJECT_STATUS_2026-11-16](PROJECT_STATUS_2026-11-16.md); Drive status https://docs.google.com/document/d/1K_89EdAIFPOsftgYI32ULHZG5w_gvzFulMzTp-nqjLo/edit.
- Live pre-migration main SHA vid avläsning: `8e3cc8f2d3f0a93adfd4dc9d72142b58fd8ba10b` (historisk; migrations-commits flyttar HEAD).

## Kontrakt — oförändrat
[Design 01–60 + nya användarkrav](DESIGN_DECISIONS_01-60_2026-11-16.md). [U1-LEG1 visuellt godkänd](SKRAUN_VISUAL_DIRECTION_2026-11-16.md), ljusgrå 8×12 A/B, framtida visuell HÖGER = original LEG1 LEFT och framtida VÄNSTER = original RIGHT; L2/L3 samma masker men större; L3 ska vara fri att manövrera även i alla åtta glesa banor. Resten av spelet enligt originalspec: två svärdsriddare + grön flyende bågskytt, gul 360° halo genom solida hinder, en orb, liv/poäng, åtta fasta banor/fyra världar, så lite flimmer som möjligt. Level3 OP; ingen genväg med oförklarad nedskalning eller ändrade fiender. De åtta öppna banutkasten är fortfarande KANDIDATER, INTE kanoniska banor.

## AKTUELLT KRITISKT (kontrollerat 2026-11-17)
**P01-COL1:** [autorisationsorder](../handoff/MAIN_II_TO_ROM_DEV_P01_COL1_ONE_ARENA_COLLISION_DIAGNOSTIC_AUTHORIZED_2026-11-16.md), [issue #24](https://github.com/Odourman/the-skraun/issues/24) OPEN, [ROM DEVELOPMENT draft PR #27](https://github.com/Odourman/the-skraun/pull/27), branch `experiment/p01-col1-single-arena-collision-20261117`, observerad head `d970c4ccf5fe23123ace5486a37b72825f193fa5`. [Real DASM/Stella Actions run 44073915789](https://github.com/Odourman/the-skraun/actions/runs/44073915789): `Source collision/model/art validation` SUCCESS, `Assemble true NTSC 4KiB ROM` SUCCESS, `Compiled ROM 6502 instruction, RIOT timer and joystick self-test (model)` SUCCESS. **Real Stella screenshot/debugger step FAIL**, log: `line 19: pid: unbound variable`. Mycket sannolik orsak är en `Stella's`-apostrof i en komentar inne i enkelciterad `bash -c` i workflow. Behöver kontrollerad minimal fix av ROM DEVELOPMENT i samma PR; ingen riktig Stella-visuell eller 262-line/P0 pixelproof kan räknas PASS ännu. [Vanlig CI run 44073915808](https://github.com/Odourman/the-skraun/actions/runs/44073915808) SUCCESS på samma SHA, men ersätter inte teststeget.

**PF-REP1 research:** [#25](https://github.com/Odourman/the-skraun/issues/25) OPEN, unmerged [draft PR #26](https://github.com/Odourman/the-skraun/pull/26). Source-only PF-REP1, PF-REP1B, PF-REP1C faktiskt publicerade/validerade, [PF-REP1C](MAIN_II_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_SOURCE_AUDIT_2026-11-17.md). De utesluter direkt enkel Hugg en-reg/2-rader, statiska Ball/Missile trick och vissa Venetian-upplägg som pixel-exakt lösning under snäva antaganden; inte universellt bevis, inte ny ROM-/graphics-integrationstillåtelse.

**R3 fullscen:** testade original-TIA-rendern fortfarande NO-GO: 20Hz same-Y tre P1-fiender, 30Hz halo/hinder eller merged-colour, 2–4 statiskt beräknade scanline-cykler före AI/pil/orb; separat RAM 89-byte P1-buffer. Ej färdig spelmotor. Inga R4/B3c utan separat beslut.

**Andra öppna grindar:** [#15 global visual](https://github.com/Odourman/the-skraun/issues/15), [#19 ART1 level3 radfel](https://github.com/Odourman/the-skraun/issues/19), [#23 fri L3 navigering och åtta kartor](https://github.com/Odourman/the-skraun/issues/23), [#1 oberoende P01 Verification](https://github.com/Odourman/the-skraun/issues/1). Användarens positiva U1-LEG1 designbesked är INTE formell Stella fullscen-PASS.

## Källprioritet och rollfördelning
MAIN III ledare/grind; ROM DEVELOPMENT gör riktiga 6502/DASM/Stella och egenkontroller; GRAPHICS gör bara separat auktoriserad design; RESEARCH rådgivande; VERIFICATION en annan oberoende granskare av frysta leveranser. Ingen ny ospecificerad implementation från migrationsdokumentet. Research får inte automatiskt ändra speldesign. Inga nya R4/B3c, särskilda cartmapper/ARM, artförändringar eller main-merge på migrationens mandat. Allt väsentligt måttat med exakt SHA, PR/run, GitHub/Drive-källa.

## Omedelbar prioritet
1. Live verifiera båda systemen och PR #27 HEAD/Actions. Kontrollera sannolik shell-citeringsbugg och få den korrigerad av ROM DEVELOPMENT inom redan godkänd #24, följt av RIKTIG Stella pixel-/262-line bevis.
2. Registrera uppdaterad status/handoff efter faktiska ändringar; inte duplicera COL1.
3. Fortsätt PF-REP1 som avgränsad research och planera nästa fullscenarkitektur först när den snäva fysiska resurs-/cycle-tröskeln har ordentligt stöd.
4. Självständiga utvecklings-/administrativa beslut kan tas av MAIN; fråga bara användaren om ett verkligt estetiskt/gameplay kompromissval. Inget backgroundarbete kan utlovas utan verklig automation.
