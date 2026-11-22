# THE SKRAUN — ROM DEVELOPMENT III till MAIN IV
## GAMEPLAY-5 ARCADE COMBAT PUSH — sammanhållen slutleverans
**Datum:** 2026-11-22. **Auktorisation:** MAIN IV överlämning GAMEPLAY-5 samt Issue #48, samtliga A–E inom en och samma sprint. **Bevisklass:** DEVELOPER_OBSERVED, med SOURCE_ONLY där tester saknas. **Slutstatus:** `GAMEPLAY5_DELIVERED / ROMDEV_III_STOPPED / MAIN_IV_REVIEW_REQUIRED`.

### Fryst proveniens och leverans
- Exakt startcommit GAMEPLAY-4A: `bc2ef9249b4e13701647850d89cb631c43190c65`. **Fysisk DASM-återbyggnad** till byte-identisk 8192B F8 ROM SHA-256 `8bb19a9d58b6a4f608f1ab10adbb622b9e70d0f44b39e247c68feb3a974427bd`; originalkällorna orörda.
- Enda GAMEPLAY-5-arbetsgren: `experiment/gameplay5-arcade-combat-push-20261122`; **ett Draft PR #49** mot tidigare gameplay-experiment, aldrig main.
- **Föredragen faktiskt körbar ROM: `experiments/gameplay5_f8_ntsc.bin`, 8192B konventionell F8 NTSC.** Äkta DASM SHA-256 **`b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca`**. Fryst käll-SHA: bank0 `1bf336fabd8308a2c578236101eaaa239d224e4391f235d22def3cbd3ceb5e12`; bank1 `ba3be13cc749c4da1b45a536b15480be8e2f51f89f48d6c0b3fbc31b9e5525bf`. Verklig separat DASM bank0/1 4096B vardera, .lst/.sym och build-loggar + SHA-fil. [Framgångsrik fryst one-shot-byggning](https://github.com/Odourman/the-skraun/actions/runs/45047118057). Exakt bytekedja finns i `experiments/gameplay5_SHA256SUMS.txt`.
- MAIN vid senaste livekontroll `46d31504cccc5d17b521f7b9f01b7aded003de1a` oförändrad. Ingen merge, inga user-godkända figurer eller U1-LEG1-masker ändrade.

### A. NTSC-timing — PASS BOUNDED, worst-case NOT VERIFIED
- Fryst GAMEPLAY-4A R1-source-phase 18/21/24/27/30 gav faktiskt **262,262,262,263,262** linjer. Diagnostik och Research II Issue #47 bekräftar inte ensam första avvikande CPU-instruktion; ingen sådan bevisas här heller.
- Två verkliga DASM/Stella-omfördelningar `TIM64T=#33 + 2 final WSYNC` respektive `#32 + 3 final WSYNC` gav **262 på samtliga fem problemfaser**. `#33 + 2` valdes: [riktig tidmätning](https://github.com/Odourman/the-skraun/actions/runs/45046548302). Käll-ROM-tabell `PlayL2P0` har också sidriktats från äldre `$F5FE` till `$F600`, utan en enda spritebyte-ändring. Detta reducerar den ursprungliga ABS/indirekta ROM-läsningens page-cross-risk men är INTE isolerat orsaksbevis för enstaka 263.
- **13/13 särskilda normala spel-Stella-scener fick `_scanEnd=262`**: start, K1 neutral/warning/strike/recovery, fem R1-faser + draw/release, stage2 L3 och gameover/restart. Verkliga utdata i [Actions #45046813014](https://github.com/Odourman/the-skraun/actions/runs/45046813014), med oförändrade mask-pixelorakel: K1 neutral116, warning134, strike130; Skraun P0 L1 98, L2 392, L3 1200 grå tv-pixlar. Input endast joystick/FIRE och debuggerläsningar, inte ram/PC-fusk.
- **NOT VERIFIED:** all-frames/frame-edge över alla fasgrenvarianter, värsta `<=76` 6507-cykler per fysisk rad, fördelad PF0/PF1/PF2/GRP1/BL beamdeadline, första exakt avvikande PC/cycle med instrumenterat trace, komplett SP nested call-stackhögvatten. 262 betyder INTE sådant bevis.

### B. Ranger-pil — verkligt fysiskt M0 NEGATIVT
- Källalternativ `gameplay5m0_bank0.asm`/bank1: en verklig gray-color M0 TIA-missil som behåller P0 Skraun, P1 K1/R1 och BL-orb som separata objekt. M0 X-placeras offscreen; Y synkas mot 192-radskernelns **två ENAM0 edge events**, inte GAMEPLAY-4:s misslyckade M1 indirekta fetch/STA per rasterrad. Bank0 source-only riktning låses vid actual release, 180-frame cooldown, maxenpil, försöker återanvända damage/hinder/halo-logik. Alla dessa logiska egenskaper är **INTE bevisad gameplay**.
- Två verkliga 4096B DASM-banker sammanfogades till exakt 8192B F8 och kördes med riktig Stella 6.7.1 och 7 normal-play R1-bågfaser. Mätt `_scanEnd=` **286,286,287,287,286,286,286**, alltså **M0_FAIL_FOR_TESTED_KERNEL**. [Fysisk återskapbar misslyckad workflow #45046341969](https://github.com/Odourman/the-skraun/actions/runs/45046341969); .bin/.lst/.sym/screenshot och logg finns i Actions-artefakt. Den nya per-rad `CPX ArrowOnScan` plus tyngre P0-kernel förefaller förenlig med +24-linjers belastning, men exakt första överruninstruktion **NOT VERIFIED**.
- **Ingen pil finns i vald säkra GAMEPLAY-5-ROM** och ingen osynlig pil får orsaka skada. Ingen faktisk pil-X/Y-positionsserie eller block/halo/bodyhit är godkänd. Negativt för den prövade M0-arkitekturen, **inte** generellt pilomöjlighet. Det gamla M1-per-rad-experimentet upprepades inte. Distinkt M1 edge-cached fallback byggdes inte när M0-rasterförlusten visade huvudkernelns otillräckliga slack.

### C. Strid, spelbarhet — source/fysik tydligt separerat
- Behåller **riktiga K1-T 8x16** neutral→24f svärdsförvarning/låst riktning→7f aktiv strike (endast hugg skadar)→60f rest och **riktig R1 8x16** neutral/draw/release i samma normalt körbara ROM. P1-enemyslot är fortfarande *en åt gången* som träningsrendering och får INTE presenteras som slutlig 2-riddare+Ranger.
- Källa `SwordLineClear` skär nu av svärdsslag genom solid rektangel mot de verkliga 48 RIOT-byte-cacheobjekten `$C0..$EF` utifrån lägsta/högsta PlayerX/KnightX och aktuell fast träningsfiende Y96. Anrop endast under aktiv strike, varning/recovery förblir skadefria. **SOURCE_ONLY** för faktisk blockerad-huggbana: de nuvarande skogshindren ligger utanför huvudfiendens horisontella y96; inga båda-vändningarnas obstacle/no-obstacle par är bevisade i Stella. Ingen falsk full LOS-PASS.
- Source `Invulnerable` har uppdaterats 45→60 NTSC-frames, banövergång `StagePause` 24→120 frames (2s); dessa källändringar testades i kompatibilitetsregressionerna, men exakt långvarig skadeperiod och bonus-tröskel har inte mätts fullständigt.
- Behöll tidigare verkliga diagonaljoystick/glid, U1-LEG1 A/B höger/vänster och samma källbitmap på L1/L2/L3, två BL-orb-besök till L3, stage1→2, lives/score, FIRE/halo och återstart. Scenens orber är fortfarande en per bana, inga stillastående utsmyckningsspritar.

### D. Materialiskt nytt H3 tre-fiendersförsök — FAIL FÖR TVÅ TESTADE SCHEMAN
- H3 bank0 har **tre separata logiska X/Y-identiteter** i befintliga RIOT RAM-byte: K1 (`$AF/$89`), K2 (`$A3/$A4`), Ranger (`$B8/$B9`), start x67/83/101 och Y78; K2 jagar, Ranger flyr på två axlar. **Det är inte ett fullt tre-actors-state-/combat-system i vald ROM**: det är en egen reproducerbar diagnostik, där tre RENDERINGAR måste prövas oberoende.
- **Samma-Y** bank1: P1 NUSIZ-kopior med aktiv bitmap- och palettbyte K1 neutral→R1 neutral under fysisk rasterrad, till skillnad från H1 enbart kloner. **Äkta Stella _scanEnd 93 / 94**, ingen fullständig bild med korrekta tre masker/färger. **FAIL**.
- **Separerad-Y** bank1: använder tre skilda 16-radstabeller plus faktiska tidsstyrda P1-ägarskiften med `RESP1` och `COLUP1` vid Y-bandgränser, till skillnad från H2 samma X/färg. **Äkta Stella _scanEnd 277 / 287**, med verkliga pixelbilder men inte 262 eller tre oberoende korrekta positioner. **FAIL**.
- [H3 verklig DASM/Stella-körning #45047010682](https://github.com/Odourman/the-skraun/actions/runs/45047010682), exakta .bin/.asm/.lst/.sym och TIA-crops; JSON `H3_REAL_PIXELS_AND_FRAMES.json`. Alla rapporterade utfall är DEVELOPER_OBSERVED, inte global omöjlighet. Ingen flicker/Y-offset-kompromiss adopterad.

### E. X/Y-rörlig halo — EJ IMPLEMENTERAD / BUDGETDEFER
A och C gav robustare spelbar baseline, men B:s fysiska +24–25 rader och D:s 93/94/277/287-linjeöverrun visar att nuvarande rasterloop inte har uppmätt säker slack ens för ny missil/ägarskifte. Att lägga till en ny PF2-skrivning skulle dessutom upprepa tidigare uppmätt PLAY1-X 273/285/297-linjers negativt test. Därför **ingen ny fysisk X-bucket-halokernel inom denna budget**. Befintlig guld-PF testmodell/B, aktiv halo över hinder och dess visuella **Y-only PARTIAL** bibehålls; ingen räckvidd, Level 3 OP-rytm eller spelkontroll krympt. Allmän X/Y följning är fortfarande OPEN.

### Hård budget och tillförlitlighet
- Verklig F8: bank0 4096 + bank1 4096 = **8192 byte**. RAM 128 RIOT-byte totalt inklusive stack. Ny säkra ROM använder oförändrade game registers och rektangelcache `$C0..$EF`; `$90/$91` återanvänds som kortvarig min/max-X-scratch i overscan efter färdig VBLANK movement. Ingen avvisad M0-position-/P1-owner-state ligger i slut-ROM.
- Status **DEVELOPER_OBSERVED BOUNDED**: dokumenterade 13 fysiska 262-bildrutor, korrekta P0/K1-pixlar. **NOT VERIFIED**: alla beamdeadlines, full 76c CPU-högvatten och 128B worst-case runtime SP stacklivstid, full L3 kollisionsväg, 2000-bonus i just denna nya ROM, 8-stage komplett pendulum och same-Y 3 enemy canon.
- Detta är inte oberoende Verification och inte MAIN-godkännande.

### Utfallstabell
| Krav | Status |
|---|---|
| Fryst GAMEPLAY-4A-bas reproducerad exakt | PASS, real DASM |
| Ny bästa 8192B F8 NTSC checkpoint, SHA + reproducibel källa | PASS |
| 5/5 ursprungligen problematiska Ranger-tidpunkter exakt 262 | PASS BOUNDED |
| 13/13 normala spelbilder exakt 262 med U1/K1/R1/BL/L3 | PASS BOUNDED |
| K1 och R1 exakta mask-/stridsposer samma ROM | PASS BOUNDED |
| 60f osårbarhet, 120f stage-pause | SOURCE_ONLY + bounded regression |
| Fysiskt bevisat väggblockerat hugg båda vändningar | NOT VERIFIED |
| Riktig rörlig synlig M0-pil och skada | FAIL for tested M0 architecture |
| Tre oberoende K1/K1/R1 samtidigt korrekt fysisk display | FAIL for tested H3 same-/separate-Y approaches |
| X/Y fysisk halo | NOT IMPLEMENTED / Y-only PARTIAL preserved |
| Worst-case 76c per rad, colourclock beamdeadline, SP highwater | NOT VERIFIED |

### Tre återstående största blockerare och EN spelbar riktning
1. **TIA synlig-kernelbudget/beam ownership** för en faktisk M0/M1 projektil ovanpå P0(L3)/P1/BL/PF. M0 edge-compares spillde 24–25 extra fysiska rader; ingen rörlig pil är godkänd.
2. **Samtidiga P1-identiteter**: H3 same-Y missade fungerande bild (93/94), separerad Y 277/287; kräver helt annan raster-ägarschemaläggning eller framtida uttryckligt val, inte antagande att logisk AI = fysiskt tre masker.
3. **Hård timingsäkerhet och minne**: ofullständig full 76c-beamdeadline/RIOT stack-highwater och ännu oprövad hugg-hinderbana/nya fulla grafiklager.

**En nästa rekommenderad spelbar riktning till MAIN IV (endast rådgivande, inte ny implementation):** spela och bedöm den nu fysiskt förbättrade K1/R1/Level3-ROM:en; vid ett separat framtida beslut satsa på en helrads-budgeterad fiende-/projektilkernel i stället för ännu en per-rad instruktion i den överbelastade befintliga loopen. Inte godkänna färre fiender eller mindre halo för att vinna cykler.

**STOP.** Ingen ytterligare N8/GAMEPLAY-6, mapperändring, main-merge, ny grafikorder, fullspelsutbyggnad eller automatiskt startad independent Verification. MAIN IV behöver uttryckligen granska.
