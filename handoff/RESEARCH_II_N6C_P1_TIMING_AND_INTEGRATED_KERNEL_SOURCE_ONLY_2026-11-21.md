# THE SKRAUN – MAIN III → RESEARCH II: N6-C, exakt P1-positionering och gemensam rastertidsplan

**Utgiven:** 2026-11-21. **Avsändare:** MAIN III. **Mottagare:** RESEARCH II. **Status:** rådgivande SOURCE-ONLY research; **ingen ROM, ingen ny assemblerimplementation, ingen ändrad grafik/canon, ingen N7-auktorisation, ingen independent Verification**. Detta är en arbetsorder för teknisk **analys inom redan godkänt N6**, inte en order till ROM DEVELOPMENT.

## 0. Starta med egen åtkomstkontroll

Verifiera faktisk access till repo/Drive/web i den mottagande chatten; om GitHub/Drive saknas, rapportera det. Hämta aktuell main HEAD och Git blob SHA själv. Följ projektets authority order. Använd **inte Memory** som aktuell projektauktoritet. Behandla R3 frysta originaldata som den faktiska implementationsbaslinjen och användarens senare nya direktiv som förstahandsdesign för N6.

Läs i denna ordning:
1. [Gällande MAIN-status](https://github.com/Odourman/the-skraun/blob/main/docs/CURRENT_MAIN_STATE_2026-11-17.md).
2. [N6-C Issue #30](https://github.com/Odourman/the-skraun/issues/30) och [första verkliga N6-C-source-delrapport](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6C_SOURCE_ONLY_PHYSICAL_FEASIBILITY_INTERIM_2026-11-21.md).
3. [Användarens accepterade N6-kandidater](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md), [design 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [U1-LEG1](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md).
4. [N3 S0–S9 fixture](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json), [N3 full resurskontrakt](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md).
5. [N4 källmask/phase-deadline motexempel](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N4_PF_G1_SOURCE_TIMING_REPORT_2026-11-17.md), [N5 tre same-Y-forskning](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N5_P1_SAME_Y_FEASIBILITY_AND_GAME_DECISION_2026-11-17.md), [N6 källfärganalys](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md).
6. [30 Atari-trick och arkitekturkombinationer](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_SECOND_PASS_ALL_30_ATARI_TRICKS_AND_COMBINATIONS_2026-11-17.md) endast när en konkret metod behöver grundas – inte ny katalog.

## 1. Prioriterad teknisk blockerare – inget mer allmänt trickinventarium

**Kan P1 på Atari 2600, med P0 upptagen av level-3 Skraun, visa två ljusblå riddare + en världskamouflerad Ranger med fria X/Y i den täta same-Y-scenen, med en läsbar ~24 NTSC-frame svärdsförvarning och samtidigt PF-halo/hinder + BL-orb + M0-arrow, före varje beamdeadline och inom 76 cykler per fysisk rad?**

Detta är enda centrala frågan. **Visa en konkret register-/opcode-sekvens eller ett reproducerbart första motexempel, inte en teoretisk lista med knep.** 

Tidigare N6-C delprov:
- P0-utlåning som *enda* metod faller i S1 och S3: P0 upptaget av Skraun på alla 16/16 fiende-samma-Y-rader. P0-lån kan fortfarande hjälpa andra zoner.
- Enklaste trevägs-Venetian med HMP-only faller i S2 nära X67/83/101: 15/15 rad-till-rad-omställningar är större än ±8 clocks. Enkel GRP1 store efter föregående sprite får bara 8-color-clock-mellanrum, men STA kräver minst 9 colorclocks. **Endast dessa metodklasser motbevisade**, inte NUSIZ-kopior med klockäkta omskrivning, RESP1-reset, VDEL, alternate phases eller en annan integrerad motor.
- N6-B OFF scenery 2496 PF-byteändringar; ON halo OR scenery guld 4400 och 419 sexbytes-rader av 2288 källradfall; minsta PF-byteändringar är inte instruktioner/cykler. Ny box-ring 4680 och stepped-ring 4548, alltså inte billigare i denna källa. Bevara original halo-mask som kontroll.
- Original R3 A-rad minst 61 cykler, B minst 71 inkl WSYNC, en fiende P1 per hel bildruta; man får **inte** lägga en tredje fiende till existerande R3-kärna utan omdesign.

## 2. Exakta arbetspaket – i denna ordning

### N6-C/R1 – P1 som hårdvara, inte bara pixelmatematik

För S1 X32/101/147,Y78, S2 X40/80/120 och särskilt X67/83/101,Y78, S3 Skraun X104,Y80,L3 + knights X105/124 + ranger X147,Y80:
1. Räkna fysisk Y-överlappning och tidsfönster på minst tre konsekutiva rasterrader där P0 används av Skraun. Utred **klock-exakt** om någon av kombinationerna `RESP1/GRP1/HMP1/HMOVE/VDEL/NUSIZ1/REFP1` kan visa tre **oberoende** aktörer med samma 8-bitars källa som R3 diagnossprites, eller exakt var instruktioner/register latched too late.
2. Ta med färg `COLUP1`: båda riddarna **en och samma ljusblå TIA-byte** (exakt kod behöver inte godkännas för cycle-model), Ranger särskild världskamouflagefärg. I S2 med ranger i mitten behövs två typvärdesövergångar i P1 om aktörerna ritas i horisontell ordning.
3. Skillnaden mellan `GRP1`-byte och **riktig X-ompositionering** får inte döljas. Dela upp källhypoteser i taktade pipeline-per-rad, midline-kopior och multirad-lokal Venetian. Redovisa NUSIZ-hårdvarukopiors fasta avstånd; de får inte felaktigt räknas som tre fria X/Y.
4. Skissa P1 riddarpose med inbyggt svärd som *rasterresurs* (idle, raised, active, recover), **inte skapa ny konst**. M1 som reserv en smal blå svärdslinje måste bokföras men ingen falsk andra M1. Testa ~24 frames varning på källnivå; inga ogrundade 60Hz-påståenden.

### N6-C/R2 – en integrerad fysisk worst-line-tabell

Ta först ett och sedan helst två samtidiga fysiska rader för R3 X80/84 source mask X=98 motsvarande arena-Y78/79, med vald färgmodell B (inaktiv PF värld, aktiv hela PF guld). Source-exakt mask `[L0,L1,L2,R0,R1,R2]` och halo+hinder OR. För varje TIA-steg: fysisk rad, 6507 opcode+adressläge, CPU cycle start/end, färgklocka, register owner, bitmaps/position, COLUP0/1/F/BK, PF0/1/2, GRP0/1, RESP/HMP/HMOVE, M0/M1/BL enable, VDEL/NUSIZ. **Följ 76 cykler och verkligt pixelfönster – inte N4:s optimistiska figur eller genomsnitt.**
Redovisa `INTIM`/VBLANK/overscan, RIOT 128B **inklusive stack**, P1 index/fiendepositioner/HUD-state och minst konservativ RAM-bufferdesign. Reservomskrivningar i tomma scanlines får inte maskera samma radens deadlines.

### N6-C/R3 – kort beslut, inte ytterligare forskning utan slut

Sammanfatta per kandidat: `SOURCE-PHYSICALLY-PLAUSIBLE / COUNTEREXAMPLE / NOT-YET-DETERMINED`. Ange **första reproducerbara blockerande rasterposition, CPU-cycle, TIA register och motexempel**, eller en konkret sammanhängande, på papper source-möjlig opcode-tidtabell. Visa vad som fortfarande kräver riktig ROM och Stella Debugger. Om ingen trovärdig P1-metod framträder, föreslå exakt två rangordnade **minimala kreativa kompromisser** och vilka delar av spelets känsla de skulle ändra – ingen automatisk färgändring, kortare fiendefaror, färre fiender eller enklare gameplay.

Leverera Markdown/CSV/JSON och eventuell reproducerbar stdlib-Python source-only beräkning under en *egen forskningsgren eller nya källdokument* med versions-/SHA-ankare. Länka utdata i Issue #30, och lägg en kort slutsats till MAIN III. **Rör inte produktionskoden, inte N6-motsvarande rapport bakåt, inga ROM-binärer.**

## 3. STOP och överlämning till nästa roll

**Stoppa** om en nödvändig TIA-write skulle ske efter beamdeadline, om P0 stjäls från U1-LEG1, M0-pilen/BL-orben tyst försvinner, eller om tre fiender endast går att visa med R3:s gamla 20Hz-rundgång och otillräcklig varning. `N6-C` är OPEN tills någon faktiskt visar en enhetlig genomförbar timingmodell eller två dokumenterade motexempel med beslutsklar kompromiss.

**ROM DEVELOPMENT får INTE ett uppdrag nu.** När RESEARCH II har levererat ett kontrollerbart N6-C-underlag granskar MAIN III rapporten, tar explicit beslut och kan därefter – med separat auktorisering – lämna en **minimal N7 DASM/Stella-mikroROM** till ROM DEVELOPMENT. Senare leverans kontrolleras oberoende av VERIFICATION II.

Detta GitHub-dokument är en **publicerad handoff**, inte en garanti att separat RESEARCH II-chatt läser den automatiskt. Användaren/MAIN måste också aktivera den rollen genom att visa länken eller denna prompt i RESEARCH II-chatt.
