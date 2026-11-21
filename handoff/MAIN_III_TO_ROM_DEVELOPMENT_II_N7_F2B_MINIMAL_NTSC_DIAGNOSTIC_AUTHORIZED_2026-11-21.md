# THE SKRAUN – MAIN III → ROM DEVELOPMENT II – N7/F2b minimal NTSC diagnostic (AUKTORISERAD)

**Datum:** 2026-11-21. **Avsändare:** MAIN III. **Mottagare:** ROM DEVELOPMENT II.  
**Auktorisationshändelse:** Efter att MAIN III uttryckligen rekommenderat **en enda minimal N7/F2b ROM** (inte en hel spelmotor) svarade användaren **"Ok, bra fortsätt"**. MAIN tolkar det som ett positivt beslut om just denna snävt definierade N7-diagnostik. **Inget senare steg, fullspelsintegration, nytt grafikspriteuppdrag, mapperbyte, merge eller oberoende Verification godkänt.** Den faktiska ROM-utvecklingen startar först när ROM DEVELOPMENT II öppnar denna arbetsorder i sin egen chatt.

## 0. Läs och verifiera verkligt tillstånd före arbete

Kontrollera själv live GitHub, aktuella projektfiler och verktyg (GitHub, Drive, DASM, Stella, Debugger, testmiljö). Börja inte utifrån Memory eller gammal migrationsstatus. Håll rätt roll: ROM DEVELOPMENT implementerar och egenkontrollerar; MAIN beslutar; VERIFICATION II är separat.

Läs:
1. [MAIN III senaste status](https://github.com/Odourman/the-skraun/blob/main/docs/CURRENT_MAIN_STATE_2026-11-17.md).
2. [MAIN III granskning av RESEARCH II N6-C](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6C_RESEARCH_II_REVIEW_AND_NEXT_GATE_2026-11-21.md) och [N6-C issue #30](https://github.com/Odourman/the-skraun/issues/30).
3. [RESEARCH II:s originalrapport, separat forskningsgren](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/RESEARCH_II_N6C_PHYSICAL_P1_DECISION.md) blob `37f045b93ba40d9ee7d326ef390c138ea5801115`; [reproducerbart Python-underlag](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/N6C_COMPACT_SOURCE_REPLAY.py) blob `837876a0ada55c9a00c9feb520dbed877443da40` och [JSON](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/N6C_SOURCE_COUNTEREXAMPLES.json) blob `1cc2c316b2866fde06870f2869ffad638ee7ce94`.
4. [N3 S0–S9 exakta adversarial fixtures](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json), [N3 owner/collision contract](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md).
5. [N6 användarens valda färg-/fiende-/spritekontrakt](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md), [gällande designbeslut](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md) och [frysbar U1-LEG1 A/B-källa](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json).
6. **Frys R3-negativkontrollen**, inte kopiera dess felaktiga slutsatser: [original R3 ASM](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), källblob `3c9ed79078eee6a0c63100614a593f92e240b5e8`.

## 1. En och endast en huvudfråga

**Kan original Atari 2600:s `P1`, med `NUSIZ1/RESP1/GRP1/COLUP1` och eventuellt `VDEL/HMOVE`, visa tre individuella fritt X-positionerade enemy-bitmaps i samma fysiska 16-raders Y-band, medan `P0` är upptagen av den godkända stora Skraun-figuren?**

Varken R3:s 20 Hz/fiende-helframe-rotation, tre identiska hårdvarukopior vid fasta avstånd, eller tyst förskjutning av fiendens logiska X/Y får kallas PASS. Varje individ måste behålla egen original källmask, position och färgtyp: **K1/K2 symboliskt samma ljusblå TIA-byte**, Ranger separat världskamouflerad TIA-byte. **Exakt ny palettkod är diagnostiskt val, ej godkänd slutlig konst.**

## 2. Obligatoriska prov, i ordning

### P1 – ren fysisk F2b-låsningsprövning
- Skapa en NY experimentgren (ex. `experiment/n7-f2b-three-enemy-retrigger-20261121`); inga ändringar på `main`, inga gamla draft-PR-merges. Ett enda självständigt NTSC-DASM `.asm` och en motsvarande ROM `.bin`, gärna testscener valbara i samma byggnad via kontrollerad meny/state/testdata, inte en motor.
- Starta med **S2-close**: R3 fienderna K1 X67, K2 X83, Ranger X101 på Y78, exakta 8-byte original R3-masker dubbelrenderade 16 fysiska rader som negativ/orakelreferens, egen bitmap/färg/horisontell start för alla. Ta också med minst en **permuterad eller spegelvänd X-ordning** så lösningen inte är hårdkodad för en rangordning.
- Mät verklig `RESP1` strobe-position, main-/NUSIZ-copy / retrigger-latch, `GRP1/COLUP1` write-completion, `NUSIZ1`, `VDEL` och `HMOVE` per fysisk rad i Stella Debugger. Pröva explicit forskningsresultatets **5/16 F2a resetkonflikt**; visa om F2b faktiskt kan förbättra resultatet, inte bara visa nya pappersbilder.
- Frys minst **12 konsekutiva NTSC-bildrutor** från samma deterministiska scen. Gör source-pixel-/X-klassning per fiende, inklusive antalet synliga rader, posfel och flickerduty. R3 20Hz per actor är FAIL-kontroll, inte resultatstandard.

### P2 – större Skraun P0 blockerar P0-lån
- Kör **S3** med godkänd U1-LEG1 P0 L3 vid X104/Y80 och K1 X105, K2 X124, ranger X147/Y80; P0 får inte skrivas över eller flyttas av `HMOVE`/andra registerändringar. Skilj skymning/priority från försvunnen/korrumperad pixelbit.
- Kör S1 tre same-Y X32/X101/X147 som extra negativ kontroll, om den tillför mätning utan att utöka scope. Allt förblir begränsat till positionering och rendering; ingen AI eller inbyggd attackmotor.

### P3 – B guld-PF på samma ROM, utan att förfalska omfattningen
- Pröva i samma ROM/datautgåva B/ON original `PF0/1/2` halo OR scenery på verkligt frysta R3 källmask X80/X84, original R3 source-loop X=98 -> arena Y78/79 (inte fysisk tv-line 98). PF X80: vänster `00 00 0C`, höger `40 50 00`; X84: vänster `00 00 14`, höger `40 30 00`. Hela arena-PF guld då aktiv halo; världen färgad när av, `BL` är delad `COLUPF`-domän.
- För P3 ska ROM DEVELOPMENT **inte påstå** att M0/BL/HUD, fullt rörlig halo, svärdsanimation, AI, collision eller 128B integration är godkänd bara för att några register är avsedda/reserverade. Om fysisk kombination inte ryms: redovisa konkret missad deadline, sen skrivning, färg-, P0- eller P1-korruption. **Misslyckat samtest är en accepterad ärlig leverans.**
- En full svärdsvarning i ~24 bildrutor kräver ännu en godkänd/byggd P1-pose. **Skapa inte ny konst som implicit del av denna arbetsorder**. F2b:s R3-diagnostik har egna K1/K2/R-bitmaps. Ingen 24-frame svärd-readability-PASS får hävdas.

## 3. Absoluta tekniska och redovisningsmässiga grindar

- NTSC original 6507/TIA, **högst 76 CPU-cykler per fysisk rad** inkl WSYNC, branches, page crossing; korrekt beam/colorclock-deadlines, horisontell position, 262 linjer per helt frame och konsekutiv 12-frame sekvens. Inga fel ompostade sprites, svällda WSYNC, osynlig Ranger eller försvunnen Skraun för en fiktiv 60Hz-pass.
- **RIOT 128 byte inkl stack**: mät live state/stack highwater och redovisa faktisk RAM-användning. Anpassa bufferdesign hellre än att naivt lägga gamla R3 state23B+P1Buf89B+COL1 28B=140B.
- Första leveransen riktas mot standard **4KiB NTSC**. Om 4KiB inte räcker eller krav krockar: rapportera exakt problem till MAIN, **ändra inte automatiskt cartridge mapper, Superchip RAM, PAL-format eller annat projektval**.
- Felscenario måste ange **första felande scanline, CPU-cycle, colorclock, TIA-register**, berörd actor-position, P0 och PF mask, och hur felet reproduceras. Fysiskt verifierad detalj bara från verklig DASM/Stella-exekvering, inte hypotetisk 76cy-tabell.
- Ingen ändring av stable huvud-ROM, speldesign, banlayout, kollision, extra aktörer, Skrauns godkända U1-LEG1 A/B-pixlar eller status hos tidigare ROM-prototyper. Ingen main-merge eller utvidgning till N8/full gameplay. Inga falska självständiga VERIFICATION-claims.

## 4. Filer som ROM DEVELOPMENT II ska leverera till MAIN III

1. Ny experimentgren med faktiska assemblerkällor och reproducibla build/test-skript, `.bin` **om den går att bygga**, DASM-kommandon/logg, ROM-byte, SHA256-manifest (inte enbart en markdownrapport).
2. Stella Debugger trace/klocktabell för P1 F2b, inklusive verkliga `RESP1/NUSIZ1/GRP1/COLUP1/HMOVE/VDEL` opcodes; helst minst 2–3 sammanhängande kritiska fysiska rader i S2 och S3, och rapport för värsta fysiska 76cy-line.
3. Minst 12 riktiga konsekutiva skärmbilder eller motsvarande pixel-exakta captures för vardera huvudsakligt stresscenario; redovisa varje fiendes duty, byte-for-byte source-pixel-orakel, P0 full footprint och faktisk PF status.
4. RAM/stack- och frame-count-resultat (inklusive reservägare M0/BL), en kort `PLAYTEST.md`, en teknisk `ROMDEV_N7_F2B_HANDOFF.md`, och repo/branch/commit + käll-/binär-hashar.
5. Samma resultat även om diagnosen misslyckas; ange första verkliga FAIL och en begränsad slutsats `F2b_PASS_ONLY_FOR_TESTED_SCENE / F2b_FAIL_FOR_TESTED_SCENE / INCOMPLETE`. **Ingen full-spels-GO** från detta mikroprov.
6. Självtester redovisas som ROM DEVELOPMENT egenkontroll; när MAIN bedömt fryst leverans kan VERIFICATION II separat få en explicit oberoende verifieringsorder.

## 5. STOP / rollgräns

- Vid första faktiskt deterministiska F2b hårdvarufel: redovisa, försök högst en välmotiverad arkitekturjustering inom **samma** F2b-diagnostiska syfte, inte ny bred arkitekturforskning. Om felet består: STOP och överlämna till MAIN. Ingen automatisk övergång till smygande fiende-Y-offset, färre fiender, permanenta 20Hz halvfigurer eller andra gameplaykompromisser.
- Om detaljer saknar faktisk verktygsåtkomst, rapportera konkret blockering med underlag; påstå inte att DASM/Stella har körts.
- MAIN III tar emot, granskar och avgör separat **nästa** beslut. RESEARCH II:s råd är inte kodimplementationsauktoritet, och VERIFICATION II förblir oberoende.

**Status efter denna arbetsorder:** `N7_F2B_MINIMAL_DIAGNOSTIC_AUTHORIZED_FOR_ROM_DEV_II / EXECUTION_NOT_YET_CONFIRMED / N6_C_STILL_OPEN / N8_NOT_AUTHORIZED / VERIFICATION_NOT_STARTED`.
