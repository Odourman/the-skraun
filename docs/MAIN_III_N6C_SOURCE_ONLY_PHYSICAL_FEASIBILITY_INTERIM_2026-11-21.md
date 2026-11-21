# THE SKRAUN — MAIN III N6-C: kombinerad källprövning, felklasser och kvarstående rastergrind

**Datum:** 2026-11-21  
**Klasse:** `N6C_SOURCE_ONLY_PARTIAL_TESTED / UNIFIED_76C_TIMELINE_OPEN / N7_NOT_AUTHORIZED`  
**Plattform/testkontrakt:** Original Atari 2600 NTSC, 6507/TIA, högst 76 cykler per fysisk rasterrad och 128 byte RIOT RAM inklusive stack.  
**INTE utfört:** Ingen ny ROM, DASM, Stella-körning, körbar gameplay, ny bildgrafik, godkänd halokontur eller oberoende VERIFICATION. Detta dokument stänger **inte** Issue #30.

## 0. Beslut i korthet

1. **Det av användaren valda färgtestet B är fortfarande den tekniskt rimligaste förstahandsriktningen**: låt PF och BL dela världsfärgen när halo är OFF, guld när halo är ON. Därmed behöver inte guld och världsfärg växlas flera gånger *inom samma arenarad*. B eliminerar just den färgkonflikten, men inte PF-byteändringar, tre P1-fienders fria X/Y, pil, orb, Skrauns P0 eller P1-varning.
2. **Den billigare, fyrkantiga halon är inte demonstrerad.** Två syntetiska PF-cellkvantiserade ringformer hade *högre* PF-byteändringskostnad än originalet i samma frysta 13-X/R3-hinderscen och förlorade mycket källformsinformation. Ett färgpulsalternativ utan ring är billigare att rita men kan inte själv visa attackradien. Behåll originalmasken som arbetskontroll; ingen ny form fastställs.
3. **Enbart F1 ("låna P0 till en fiende där Skraun inte finns") är **inte tillräckligt**:** på S1 och S3 använder P0 Skraun under samtliga 16 fysiska rader där tre fiender delar Y-band. P0-lån hjälper i andra Y-zoner, inte det avgörande värstafallet.
4. **Naiv F2 (trevägs-Venetian + enkel `HMOVE` varje rad) är **inte tillräckligt**:** alla 15 övergångar mellan de tre olika X-platserna i täta S2 kräver större steg än HMP:s ungefär -8..+7 färgklockor. P1 måste återpositioneras på annat sätt, eller ritas via mer avancerat NUSIZ/GRP/RESP/VDEL-schema. De tre aktörernas exakta bildinformation och 24-rutors svärdsvarning är fortfarande obevisade.
5. **Enbart kortare L3-kropp löser inte konflikten.** 36 till 30 fysiska P0-rader ger 16/16 fortsatta samtidiga P0+tre-fiender-rader i S1 och S3, och 8/16 i S6 för båda storlekar. Låt därför användarens godkända storleksplan ligga kvar så länge vi saknar påvisad vinst för att ändra proportioner.
6. **R3:s gamla kernel kan inte enkelt byggas på:** i originalassemblerns vanliga tvålinje-loop beräknas **A-linjen minst 61** 6507-cykler och **B-linjen minst 71** cykler inklusive `STA WSYNC`, innan eventuella sidkorsningscykler. Den ROM:en ritar bara **en** av tre P1-fiender per bildruta, inte alla samtidigt. Nästa arkitektur behöver byta P1/PF-dataplan, inte lägga extra objekt-/svärdskod efter den befintliga B-loopen.

**Samlad rekommendation:** Behåll tre fiender och ljusblå riddare med svärd **inuti P1-poserna** som förstahandsmål. Forska vidare enbart i en verklig **F3-hybrid**: P0-lån där P0 är ledig, och en annan klock-/positioneringssäker P1-metod när P0 är upptagen. Om en konkret sådan instruktionstidsplan inte kan visas utan osynliga fiender ska vi presentera kreativa omval i stället för att repetera R3:s 20Hz-helframeblink. **Inget GO för N7 ännu.**

## 1. Källkedja och metod

- [Issue #30 – auktoriserat N6-C source-only-uppdrag](https://github.com/Odourman/the-skraun/issues/30).
- [N3 S0–S9 kontrakt + de exakta syntetiska/observerade fixture-positionerna](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json).
- [N6 användarbekräftad design- och stoppmatris](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md).
- [N4 fysisk raster-/färggränsanalys](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N4_PF_G1_SOURCE_TIMING_REPORT_2026-11-17.md).
- [R3 original-GitHub-assembler på fryst experimentgren](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), återspelat binärt och bekräftat Git-blob-SHA `3c9ed79078eee6a0c63100614a593f92e240b5e8`.
- Maskdata `R3_SOURCE_EXACT_MASKS.json` och original-ASM kopierade byte-identiskt i detta reproducerbara paket. Kontroll: 13 X från 56 till 104 i steg 4, 176 fysiska R3-arena-rader per X; de ursprungliga halo-/hinder-mönstren **var alternativa R3-renderingslägen**, inte en befintlig fungerande samtidig tvåfärgsscen.
- Primärhårdvara [1979 Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): P0/P1 två åttabitars-player, P0/M0, P1/M1, PF/BL delar respektive färgregister, 3 färgklockor/CPU-cykel, `RESPx` som positioneringsstrobe, `HMOVE` med timingvillkor och HMP ungefär ±8 färgklockor.

Det inkluderade `N6C_SOURCE_ONLY_ARCHITECTURE_PROBE.py` gör om mask- och Y-beräkningar från de frysta underlagen. S1/S2/S3/S6-fiendepositioner motsvarar de uttryckligen deklarerade N3-fixture-koordinaterna. S2 saknar angiven Skraun-position i N3 och därför markeras P0-ägarskap där som `UNKNOWN`, inte ledigt.

## 2. C1 – haloform: registrerade resultat, inte estetisk godkänning

PF = OR av guldhalokontur och R3-källornas hinder; **en** `COLUPF`-färg under HALO-ON (guld). Byteändringar räknas från föregående fysiska radens högra PF0/1/2 till nuvarande vänster PF och därefter samma radens högra PF. Dessa är minsta ändrade registervärden, **inte** faktiska fulla CPU-instruktionskostnader.

| Kandidat | PF-byteändringar i 13×176 radfall | Rader med sex ändrade bytes | Gemensamma halo-och-hinderceller | Källform avvikelse |
|---|---:|---:|---:|---|
| **Original R3 halo i B** | **4 400** | **419** | **104** | Oförändrad originalgeometri |
| Fyrkantig 13 PF-celler bred, 72 rader hög | 4 680 | 437 | 96 | Bevarar bara 156 av 2 392 originalbelysta halo-cellinstanser; extra 2 288 |
| Grov trebreddsring, samma bbox | 4 548 | 426 | 96 | Bevarar 468 av 2 392 originalbelysta halo-cellinstanser; extra 1 768 |
| **B med enbart global färgpuls**, utan ritad halo | **2 496** | **403** | 0 | **Ritar ingen halo alls**; ingen lokal attackradie i bilden |

**Tolkning:** Vi har prövat två konkreta lågdetaljformer utan någon uppmätt vinst. Det är inget bevis att ingen billigare form finns. Den visuella skillnaden är mycket stor och formerna är varken konstnärligt godkända eller bevisat gameplay-trogna. Den lägsta skrivkostnaden utan synlig halo har ett **tydligt gameplayproblem**: spelaren ser inte lokal räckvidd och kan misstolka träffar. Bevara 360° logisk räckvidd om denna fallback ens övervägs.

**Kritiska B/ON originalrader i N4-källmasken**: Originalets *source-kodade* loop-index `X=98` är **arenaY 78/79**, *inte TV-line98*. Med 16 historiska HUD-rader blir det nominalt synligt index 94/95 (faktisk absolut TV-line kräver emulator/signalprotokoll). OR-källa i B:

| Ringposition | Arena-Y | Vänster PF0/PF1/PF2 | Höger PF0/PF1/PF2 | Ändrade PF-bytes från föregående halva/rad |
|---|---:|---|---|---:|
| X80 | 78 | `00-00-0C` | `40-50-00` | 5 |
| X80 | 79 | `00-00-0C` | `40-50-00` | 6 |
| X84 | 78 | `00-00-14` | `40-30-00` | 5 |
| X84 | 79 | `00-00-14` | `40-30-00` | 6 |

På B/ON behövs ingen *växling mellan guld och hinderfärg på den fysiska raden*. Det räddar dock inte sex PF-registervärdeändringar, `GRP0`, `GRP1`, `ENABL`, `ENAM0` och fri fiendepositionering i samma renderer. Den mest kritiska scenen får inget GO från detta färgresultat.

## 3. C2 – två fysikaliskt olika fiendemetoder

**F1: tillfälligt P0-lån när Skraun saknar pixlar i den Y-zonen.** Detta är legitimt att studera eftersom TIA-player kan byta roll per zon, men ett belagt nej till att F1 ensam löser all same-Y:

| N3-fall med R3:s diagnostiska fiendehöjd 16 | Rasterrader med tre fiender samtidigt | Där P0 är Skraun | Y-områden där P0 potentiellt kan lånas |
|---|---:|---:|---:|
| S1, tre fiender Y78 + Skraun L3 Y78 | 16 | **16** | **0** |
| S3, svärdsvarning Y80 + Skraun L3 Y80 | 16 | **16** | **0** |
| S6, tre fiender Y80 + Skraun L3 Y88 | 16 | **8** | **8** |
| S2, tre fiender nära Y78 eller permuterade | 16 | P0 ej specificerad i denna fixture | **OKÄNT**, inte gratis P0 |

Även där P0 är ledig måste NUSIZ0 x4 (stor Skraun) kunna bli en enskild blå riddare och återställas utan att M0-pilen, P0:s horn/ben eller HMOVE-förflyttningar skadas. S1/S3 är fulla blockerare för F1 som **universell** lösning, men inte för P0-lån som lokal optimering.

**F2: Y-lokal 2-/3-vägs-Venetian endast där fiendernas faktiskt använda rasterintervall överlappar.** Den gamla N6 source-radreproduktionen visar 6/5/5 unika R3-spritekällrader av 8 för trevägsvisning och cirka 29–37 % av de ursprungliga ljusa fysiska pixelinstanserna, **utan** att visa en fungerande P1-reset. Ny N6-C-granskning av X-växlingar:

- S1 ordning X32→101→147→32 ger stora horisontella omställningar varje fysisk rad vid trevägsvarvning.
- S2 nära X67→83→101→67 ger **15 av 15 övergångar** större än vad enbart ±8 färgklockors HMP kan justera; fem är högra→vänstra omställningar. 
- Vid X67→83 är mellanrummet efter en åttafärgklocksbreddsprite bara **8 färgklockor**. En enda enkel 6507 `STA GRP1` till TIA tar **minst 3 CPU-cykler = 9 färgklockor**. Den definierade **naiva** metoden "skriv GRP1 efter att den föregående ritas och innan nästa börjar inom samma rad" får därför **FAIL för just denna täta scen**. Förladdning, NUSIZ-kopior med verkliga fria X, VDEL, rörelse mellan rader och helt annan instruktionssekvens är inte uteslutna av denna begränsade klassprövning.

**Slutsats för F2:** Enkla "var tredje rad"-illustrationer visar att aktörens silhuett kan samplas, men de löser inte P1:s horisontella ägande. Inget verifierbart 60Hz-samtidighetspass, läsbar 24-rutors svärdsvarning eller full 76c-schedule finns ännu.

## 4. C3 – verifierbar verklig R3-instruktionskostnad vs önskad helt ny motor

Fryst original-R3 assembler har `R3Pair` med två fysiska rasterrader. Från opcodes i själva filen, med standard-6502-baskostnader och **utan** sidkorsningspåslag, blir summorna:

| Gammalt R3-kodavsnitt | Beräknad nedre opcodesumma inkl `STA WSYNC` | Utrymme före 76 cykler (under bästa fall) | Vad faktisk R3 gör |
|---|---:|---:|---|
| A-rad | 61 | högst 15 | P0 + sex PF-store; en P1 aktör är redan vald globalt för bildrutan |
| B-rad | **71** | **högst 5** | P0 + sex PF-store + laddning av nästa P1-rad; en P1-aktör per bildruta |

**Varning:** Detta är **inte** verklig hårdvarumätning eller en ny B-färgad ROM. Varje `LDA (ZP),Y` kan få extra sidkorsningscykel, likaså andra indexerade läsningar; WSYNC-stall, exakt horisontell beamfas och TIA-latchmodellen har inte räknats. Se `output/N6C_OLD_R3_AB_OPCODE_CYCLE_LOWER_BOUND.csv` för samtliga opcodes och cykelintervall. En ny kernel kan vara mycket annorlunda (förberäknade sparse PF event, färre dynamiska index, byte-live overlaid RIOT), så det vore fel att förklara hela spelet omöjligt från R3:s gamla B-loop.

**Den begärda nya, gemensamma fysisk-rad/opcode/beamdeadlines/RIOT-planen är **INTE LEVERERAD**:** F1 saknar P1-plan när P0 används av Skraun; F2 saknar demonstrerad fri-X-ompositionering och samma TIA-write-/GRP-budget i de värsta raderna. De tidigare dokumenterade 23 byte R3-state + 89 byte R3-P1Buf = 112 byte får inte adderas naivt till COL1:s separat 28 byte (140 byte >128 byte före stack). Ny design måste ersätta eller överlagra buffertar. Bankbyte eller Superchip löser inte TIA:s antal pixellager eller rasterdeadlines.

## 5. N3 S0–S9 täckning (inga falska PASS)

| Scen | Ny N6-C source-evidens | Ny återstående grind |
|---|---|---|
| S0 Skraun källa och 3 storlekar | Gamla P0-U1 originalkälla oförändrad, beräknat 30/36 P0-Y-band | Exakta riktiga P0-masker och rörelse/ART1-radfel i ny kärna |
| S1 tre same-Y | 16/16 band P0 upptaget: F1 kan inte vara universallösning; F2 ompositionering väntar | Fritt X/Y och tre individuellt synliga figurer |
| S2 ordning, nära X, HUD-gräns | Sammanlagt 15 X-omställningar per 16-raders trevägsband; nära X67/83/101 >HMP-only | Korrekt RESP1/HMOVE/GRP-pipeline och bildgräns |
| S3 aktiv svärdsvarning i P0-overlap | P0 belagt 16/16, F1 blockerad som universallösning | Egen P1-svärdspose och ~24-bildrute läsbarhet, tvinga inte extrafiende bort |
| S4 kritisk ring/hinder X80/84 | B/ON en färg, källmaskrad 98 = arena78/79, fem-sex PF-byteändringar | 76c plus TIA faktiska cell-deadlines, BL och aktörer |
| S5 X56/104 och retur | Alla 13 R3 positioner, två syntetiska konturer faktiskt beräknade | Rörligt PF-/sprite-resultat och rätt höger PF2 |
| S6 pil+orb+HUD | P0 8/16 av trebandsrader upptagna; PF/BL samma B-color plan | M0-pil X92Y98, BL orb X116Y112, full realistisk färg och cykler |
| S7 sword/arrow collisions/timer | Ingen ny körbar proof | Separat gameplay-hitbox, attackfönster, AI, timer/underflow |
| S8 alla fyra världar | Identisk TIA-kopplingsprincip; ljusblå knights kandidat | Stella/CRT/PAL och färgläsbarhet i varje värld |
| S9 L3 rörlighet/level kartor | Ingen ny gameplay proof | Verklig joystick, solid/kant-/orbväxling och öppna banor |

## 6. Rekommenderat snävt beslut och nästa falsifiering

**MAIN-rekommendation 2026-11-21:**

1. **Frys för denna prövning** färg B, samma ljusblå för två riddare, ranger-kamo, P1-integrerad svärdsanimation, liten värld/guld-orb och original U1-LEG1 storleksplan. Ingen spelförlust i antal fiender, färgidentitet, 360°-attack eller nivåsystem.
2. **Avslå som universallösning:** ensam P0-utlåning F1 (S1/S3). **Avslå som tillräcklig:** naiv F2 med HMP-only eller direkt same-line-färdig-STA i de täta 8-färgklocksglappen. Behåll möjligheten till *hybrid med avancerad klockplan*, inte okritisk trots dokumenterade begränsningar.
3. **Behåll original halokontur som testkontroll**, eftersom de två explicita enklare alternativen var dyrare och visuellt annorlunda. Undvik att låsa alla hinder-/halopixlar medan P1-scheduler fortfarande saknas.
4. **Nästa absolut nödvändiga N6-C-problem** är en enda **konkret, cykel-/fasredovisad P1-ompositioneringsrutin under S2 nära och S3 P0-överlapp**, kombinerad med den beräknade B/ON PF-maskrad 78/79. Den måste bokföra `RESP1, HMP1, HMOVE, GRP1, COLUP1, GRP0, PF0/1/2, ENABL, ENAM0` före respektive TIA-deadline; rapportera separat alla 76 cykler på minst 2–3 konsekutiva verkliga scanlines och RAM/stack-live ranges. **N6-C är fortfarande OPEN** tills detta finns eller alla tillräckliga kandidatklasser kan falsifieras.
5. **Förbered ENDAST som framtida N7-förslag, inte start:** en liten NTSC-ROM med 3 separata fiende-X (S2 nära, S1 och S3), en synlig riddar-svärdsvarningspose över 24 ramar och P0 L3 på samma Y; med användarvalt B/ON-PF som förberedd variant och en faktisk Stella `GRP1/RESP1/HMOVE`-cykeltrace. Den ska ha en enda hård STOP: antingen kan den visa egna X/Y med acceptabel läsbarhet och tidsfönster, eller inte. **Ingen N7/ROM-implementation får påbörjas utan separat uttrycklig autorisation.**

## 7. Leverans och reproduktion

`python3 N6C_SOURCE_ONLY_ARCHITECTURE_PROBE.py` kör i leveransmapp och verifierar fryst R3 Git-blob. Den skriver:

- `output/N6C_HALO_MASK_CANDIDATE_RESULTS.json` – maskdiffar, registerändringar för original, box, stepped och puls.
- `output/N6C_CRITICAL_PF_RASTER_SOURCE_EVENTS.csv` – X80/X84 och X56/X104 konkreta PF-byte- och source-rowfall.
- `output/N6C_N3_P1_Y_OCCUPANCY_RESULTS.json` och `output/N6C_ENEMY_P0_Y_OCCUPANCY.csv` – tre-fiender-Y och P0 lånebehov.
- `output/N6C_P1_3WAY_POSITION_TRANSITIONS.csv` – F2-påstått HMP-only fall och X-hoppen.
- `output/N6C_P0_HEIGHT_30_VS_36.csv` – nej till att 30 i stället för 36 löser S1/S3.
- `output/N6C_OLD_R3_AB_OPCODE_CYCLE_LOWER_BOUND.csv` – rad A/B och faktisk historisk opcodesekvens med baskostnad, *inte* ny scanlinekörning.
- `output/N6C_SUMMARY.json` – maskinläsbar klassificering och samtliga delresultat.

**Sanningsstatus:** source replay; kontrollerad programmerarmodell, inte oberoende Verification. **`N6C_PARTIAL_SOURCE_ANALYSIS_COMPLETE; N6C_UNIFIED_BEAMSAFE_KERNEL_UNPROVEN; N7_NOT_AUTHORIZED.`**
