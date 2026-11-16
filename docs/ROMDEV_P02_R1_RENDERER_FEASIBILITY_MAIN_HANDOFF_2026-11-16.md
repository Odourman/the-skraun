# THE SKRAUN – P02-R1 renderer architecture feasibility / MAIN handoff
**Datum:** 2026-11-16. **Uppdrag:** [MAIN:s bindande P02-R1-autorisering](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R1_RENDERER_FEASIBILITY_AUTHORIZED_2026-11-16.md).  
**Roll:** ROM DEVELOPMENT; **enbart utvecklaregenkontroller, ingen oberoende VERIFICATION.**  
**Gren:** [experiment/romdev-r1-renderer-feasibility](https://github.com/Odourman/the-skraun/tree/experiment/romdev-r1-renderer-feasibility), skapad från den accepterade B3b-experimentgrenen. main var 3f6fac98084c1bd7d771a33eeb22cb401a855895 vid R1-start. **Ingen main-merge, inget B3c eller senare steg implementerat.**

## 1. Samlad slutsats före MAIN:s nästa beslut
1. **R1-A PASS** för snabb horisontell SWCHA-ingång i det avgränsade level-2-testet. 4 TIA-color-clocks per steg, ett steg varannan NTSC-frame. Direkta Stella Debugger-mätningar visar byteförändring inom **1–2 emulerade frames**, korrekt **13-lägeskedja x56..104**, vändning och 262 NTSC-scanlines. Detta innebär inte ett godkänt färdigt rörelsesystem, diagonsgränsen är inte permanent och vertikal rörelse, FIRE och full spelhastighet var utanför R1.
2. **R1-B partiell PASS** för tekniska delmetoder men **BLOCKED för oberoende scenery+halo-lager**. Exakt maskdeduplicering sparar **528 ROM-byte** i en fast-hinder-variant utan pixeländringar eller extra instruktioner, men hinder och ring fortsätter att smälta ihop i samma färg-PF-plan. SCORE-mode kan skilja skärmhalvor, inte objekt; P1 kan inte reserveras permanent åt ring i ett spel med flera fiender.
3. **R1-C syntetiskt P1 PASS**, men **integrerad fiende/pil/orb/HUD-headroom FAIL/BLOCKED** för denna kernel. Den extra faktiska gröna P1-spriten ökar statisk värstafallskostnad från **63/76 till 71/76 CPU-cykler** per scanline (fem kvar). En enda extra minimal missil-enable kostar minst fem och äter upp reserven; efter ytterligare boll/orb är nedre gräns **81/76**. Tre fristående fiender har heller inte tre fria player-sprite-slots på samma rasterrad.
**MAIN-rekommendation:** R1 som avgränsad feasibilityuppgift är klar. **Använd inte denna 63-cykel-PF-kernel som produktionsgrund för B3c**. Nästa separata MAIN-auktorisation bör gälla ny horisontell/tidsdelad kernel/hybrid studie med bevarad scenery, kontroll av level-3-ringens räckvidd och verklig overlap-stress. Ingen permanent renderermetod eller bankformat väljs i R1.

## 2. Faktiska byggda NTSC-ROM och reproducerbarhet
Fyra olika **4 096-byte**, originalkompatibla 4K-ROM utan bankswitching, alla faktiskt assemblerade med DASM och körda i Stella 6.7.1:

| Variant | 6502 source i experimentgrenen | SHA-256 |
|---|---|---|
| FAST PF, 2-frame SWCHA | experiments/romdev_r1_fast_pf.asm | 02aad43f1e7c10315ca54b50e1ee953e5e2e9ee2401a082754d325ff2ac67e90 |
| OPT PF, precomposed hinder och aliasmasker | experiments/romdev_r1_optimized_pf.asm | a088b4fd434562edbdc102ba54242fe2477e0b973bfea274fec5856a9e486e57 |
| SCORE PF, färg per skärmhalva | experiments/romdev_r1_score_contrast.asm | 316067c9c275a93de11dff1d211c50742bd7eae05e7e86a3f600500fbff7632a |
| P1-load, separat grön syntetisk sprite | experiments/romdev_r1_p1_stress.asm | 6c0bf9dca066a0777d6e6ef2b63bfe7ae54fe7025749a5cd40693ad02d6c92e9 |

DASM-kommandon för var och en: **dasm [källa.asm] -f3 -o[ROM.bin] -l[listing.lst] -s[symbols.sym]**. Original-assembler, ROM, DASM-listningar, symboltabeller och SHA256SUMS ligger både i GitHub Actions-artifakten och i Drive-evidensen. Sista gröna fyra-kandidatbygget: [#43906912249](https://github.com/Odourman/the-skraun/actions/runs/43906912249), med **492 riktiga Stella-skärmbilder** samt objekt/HUD-budgettabeller. Tester och skript:
- tests/romdev_r1_real_stella.py (riktiga pixlar, orientering, runtime snapshots, PF OR, SCORE och P1 synlighet).
- tests/romdev_r1_static_ledger.py (DASM-adresser, samtliga sidkorsningar och grenfall).
- tests/romdev_r1_mask_aliases.py (alla 52 historiska PF-masker byte-exakt från ROM).
- tests/romdev_r1_object_headroom.py (minimal, uttryckligen syntetisk cykel-/objektslots-CSV, **inte** AI eller fungerande HUD).

## 3. R1-A – exakta verkliga joystickresultat och latens
R1-A tar bort B3b:s artificiella 16-frame-rörelsegrind och använder låga biten i Frames: SWCHA avläses och centerindex uppdateras **varannan frame**. Två TIA-orienteringar/skala/fast Y är oförändrade; inga nya spelregler.

**Direkt mätt med riktig Stella Debugger, frame-step på faktisk emulerad ROM** (active-low debugger input 0=nedtryckt, 1=släppt):  
Start + höger 1 frame + höger ytterligare 1 + höger 4 + vänster 1 + vänster ytterligare 1 + vänster 4:
**Mode = [6,7,7,9,8,8,6]**.  
Fortsatt exakt två-frame-steppning åt vänster och höger:
**Mode = [5,4,3,2,1,0,1,2,3,4,5,6,7,8,9,10,11,12]**.  
Mode0..12 mappas till **TIA-center x56,60,...,104**. Inga utelämnade värden. För testad fas kom första respons efter en frame och nästkommande steg varannan frame. Övre responsgräns **2 frames** härleds ur den två-frame-polling som är bunden till frame-count. **262 NTSC scanlines** avlästa direkt i debugger under testsekvensen. [R1-A direkt debugger / bevarad textsessionsfil](https://github.com/Odourman/the-skraun/actions/runs/43906553221).

**Separat visuellt test** tog 123 verkliga original-Stella-bilder per kandidat under hållna riktningar och reversering = **492**. Dessa F12-skärmdumpar är asynkrona i förhållande till emulerade frames: de visar bara ett urval av mellanlägen; **hävdar inte 13 på varandra följande unika mellanskärmdumpar**. Den deterministiska debuggersekvensen ovan bevisar däremot hela logiska 13-lägesgridden. Figuren är rättvänd via pixeljämförelse mot assemblerade ROM-byte, 32×24 bildpixlar; en standardring 80×64 bildpixlar och oförändrad Y och centering vid testade lägen (horisontell felcentrering noll TIA-color-clocks); inga oavsiktliga rasterreflektioner eller klippningar.

**Diagnostisk hastighet:** 4 color-clocks / 2 NTSC frames, cirka 120 color-clocks/s över en hållning, en explicit testtakt och **inte** slutligt gameplay-val. B3b:s x56..104 är bara en skyddad prototyprange; en permanent horisontell skärmkant är inte beslutad.

## 4. R1-B – separat grafikteknisk jämförelse

| Arkitektur | Resultat | Verklig funktion / teknisk nackdel |
|---|---|---|
| Asymmetrisk PF, vanlig | PASS för rörlig ring | Full PF0/PF1/PF2 vänster/höger per synlig linje, 4 indirekta maskläsningar och 6 PF-registerskrivningar; en enda samtidig grafikplan och PF-färg; hinder saknas i FAST-varianten |
| Optimerad asy. PF, fixed scenery OR | PASS för pixelidentiskt optimerad grafik; BLOCKED för oberoende hinder | 52 original 33-byte-masker =1716 byte, 16 identiska block återanvänds, **36 unika block=1188 byte**, **528 bytes sparade** i ROM utan extra CPU per rasterrad; visad hinder/PF-ring delar COLUPF och smälter ihop på överlappande pixlar |
| CTRLPF SCORE mode | PASS för halva-skärmen-färgeffekt; FAIL för sann objektseparation | PF använder COLUP0 i vänster halva och COLUP1 i höger; den goldfärgade ringen blir halvsidesfärgad (vit/grön i experimentet) och hindren får exakt samma sidofärg. SCORE delar inte en PF-cell i två färger |
| Syntetisk hybrid PF + P1 | PASS för extra verklig sprite; BLOCKED för full enemy render | P1 kan synas på samma Y som P0 och PF; dock förbrukar bara **en** extra sprite redan 8 cykler och P1:s framtida knight/archer-slot; inte oberoende halo på samma plats |

**Hinderdiagnos:** tre korta syntetiska block/kolumner y82–109 är pre-OR:ade med ring-maskerna i ROM, inga nya runtime-cykler för just de tre hindren. Stella visar att unionen ger sammanfallande pixlar med samma färg och att P0 skymmer PF-pixlar i sin silhuett. Collider-/träffmodellen får **inte** härledas ur PF-bilden. Designbeslutet att magin går genom hinder lämnas oförändrat.

**Alternativa färg-/tidsknep, konsekvenser:** PF-omfärgning mellan rasterrader kan ge zonfärger (minst ytterligare 5 CPU-cykler med en konstant LDA+STA), men skiljer inte ring/hinder inom samma rad. Tidsdelad visning på alternerande bildrutor skulle halvera respektive objekts visuella duty cycle till 30Hz vid NTSC60 och skapa flimmerrisk, **NOT TESTED i körbar ROM**; det kan inte betecknas som godkänd lösning. PF-row partitioning offrar simultan ring/hinder-visibility på samma Y. P1-only halo var tidigare för smal i nivå3 och konsumerar fiendespriten; M0/M1/BL är smala TIA-objekt, kan inte frikostigt skapa en bred 360-graders ring utan många extra writes. Scanline-scheduled/hybrid renderer med separerade aktörsrader eller bredare kombinationer kräver nya tester.

**ROM-skalning:** En 4K-hinderlayout kräver i testet 1188 bytes unika PF-masker; det är **ingen garanti att åtta olika banor kan återanvända samma 16 block**. Naiv duplication skulle ge ca **9,5 KiB** för 8 liknande optimerade layouter (eller **13,728 bytes** utan dedup), före skog/berg/dröm/nattens fiender, hinderlogik, ljud och HUD. Större bankad ROM ger datautrymme men inte fler 76 CPU-cykler per scanline. R1 gör inget produktionsval om bankformat.

**Nivå3-problemet:** R1 använder endast nivå2 och en 40-color-clock-rings ytterkontur. Det är **NOT TESTED** att en nivå3-ring får större radius/tjocklek än nivå3-spriten, täcker korrekt skaderäckvidd och går genom hinder samtidigt som objektslots är tillgängliga. Den gällande level3-designen får inte inskränkas för att passa demonstrationen.

## 5. R1-C – verkliga rasterbudgeten och syntetisk objekt/HUD-last
**Direkt Stella Debugger**: körning [#43906728214](https://github.com/Odourman/the-skraun/actions/runs/43906728214) med tre isolerade ROM-kandidater P1/SCORE/OPT, och **Mode 6→12→0** per kandidat, samtliga avlästa _scanEnd exakt **262** (9 skilda tillstånd). R1-A:s exakta frame-stegning har också 262. Detta är en **direkt mätning av bildrutelängd**, men **inte** en framtida fiende-/HUD-profil.

**STATIC CALCULATION – 6502 med riktiga DASM-symboler och sidkorsning**, 4 kandidater ×13 center ×192 rasterrader = **9984 analyserade cases**, inklusive grenfall och nästföljande WSYNC:

| Faktiskt byggd kernel | Worst cycles /76 | Marginal /76 | Senaste höger PF0-write | Höger PF1-write |
|---|---:|---:|---:|---:|
| FAST | 63 | 13 | 42 | 50 |
| OPT / hinder | **64** | **12** | 42 | **51** |
| SCORE | 63 | 13 | 42 | 50 |
| P1-stress | 71 | 5 | 42 | 50 |

P1:s senaste GRP1-datawrite i den syntetiska belastningen omkring cykel **63**. Skilda latenser beror på de faktiska indexerade ROM-datans placeringar/sidkorsningar. Inget här säger att alla framtida objekt kan samexistera.

**Syntetisk lower-bound object/HUD CSV** i tests/romdev_r1_object_headroom.py, från verklig assembled-kernel:
- P0 + PF-ringen: **63** cykler, 13 kvar.
- Plus **en** P1-bitmap: **71**, 5 kvar (direkt assemblerad).
- Plus minimal ENAM0 (pil enable, utan positionering): minst **76**, 0 kvar (ENDAST kalkyl).
- Plus en BL-orb-enable: minst **81**, minst 5 över (ENDAST kalkyl).
- Ytterligare en separat GRP1-bitmapload/store för annan fiende: minst **78** redan utan motsvarande reposition/HMOVE, och P1 är **inte tre samtidiga oberoende horisontella sprite-objekt**.
- Den avgränsade modellen för 2 knights + 1 archer + 1 arrow + 1 orb + en enkel HUD-glyph ger **minst 102/76** på samma belastade linje om man naivt lägger objekten till denna kernel. Detta är en **lägre gräns** för ett valt naive overlap-scenario, inte ett bevis att alla alternativa kernels är matematiskt omöjliga.
- Fyra extra dynamiska scenery-read: minst **16** cykler före OR-overhead; FAST 63+16=**79 >76**, utan att ens räkna resten av kompositionskoden.
- En färgändring i PF med LDA immediate + STA COLUPF: +5, ger 68/76 FAST och 76/76 med P1; inte per-objekt-independent färg.

**TIA-slot-/minnesreservation:** P0 upptagen av Skraun. P1 är den enda andra player-spriten. NUSIZ-kopior är kopior av samma bitmap, inte tre individuella fienders beteenden. M0/M1 är smala och delar player-färg, BL har PF-färg/priority; PF är den enda 40-kolumns-planen. Två riddare och bågskytt och pil och orb kan behöva bättre Y-zonering, tidskritisk multiplexering, annat ROM-arrangemang och eventuellt begränsat uppmätt flicker, och HUD en separat zon eller annan scheduler. **Ingen aktör-AI, skada, kollision, orb eller faktisk HUD har implementerats** under R1. RAM i de isolerade fyra ROM:erna är **$80..$89 = 10 byte**, inte något bevis om reserverad RAM för färdig motor. Ytterligare 15–20 byte för enbart 5 aktörers X/Y/state är grov rådgivande förkalkyl, inte full AI-budget. R1 ändrar inte sanningskällan för kollisionsgeometri: separat från playfieldens visuella OR-bitar. Kollisions-/AI-beräkningar under VBLANK/overscan är **NOT TESTED**.

## 6. Varför några tidiga CI-jobb var röda
Tidiga kandidater byggde ROM:erna korrekt men ett Python-test hade syntaxfel. Efter det försökte F12-skärmdumpar kräva samtliga center trots att snabba programsteg passerar mellan asynkrona screenshot-call; testet korrigerades för att göra granskning av faktiska fångade pixlar, och **exakt frame-by-frame ALL13** lades i en separat direkt-debuggersekvens. En testjämförelse för hinder försökte slå upp ett center som saknades i FAST-skärmbilder och byttes till faktisk geometrisk översättning från referenscenter x56. Att en run är grön och har 262 frames räcker aldrig ensamt för att hävda full fiende- eller color-layer-feasibility. **Slutlig full regression #43906912249 är grön.** Dessa incidenter var tester/capture-harness, inte nya spelregler.

## 7. Beslutstabell, avgränsning och rekommenderad fortsättning
| Gate | Status | Evidensgräns |
|---|---|---|
| R1-A input response <=2 frames, steg 1–4 frames, 13 center, reversering | **PASS** | Riktig Stella Debugger Mode-sekvens och 262 NTSC, fortfarande prototyprange/testhastighet |
| Upright P0 och aligned ring / fast Y | **PASS** | ROM-byteexakt test + faktiska Stella-pixlar, inget level3-test |
| Optimerad PF-maskbesparing 528 ROM-byte, mask-/pixelidentitet | **PASS** | Alla 52 byte-exakta originalmasker, 492 Stella-bilder |
| Två skärmhalvsfärger via SCORE | **PASS**, men endast färgeffekt | Ingen separat färg för ring+hinder inom samma PF-cell |
| Sann separat, lättläst hinder och halo på samma pixlar | **FAIL i alla fyra provade kernels** | Delad PF-plan; P1-halo ej realistisk som enda fienderesurs |
| Extra syntetisk P1 på överlappande Y, 262 frames | **PASS begränsat** | 71/76 och fysisk sprite, inga övriga aktörer eller AI |
| 2 knights + archer + arrow + orb + HUD, full effekt på samma rasterrader | **BLOCKED/FAIL i oförändrad kernel** | Statisk nedre gräns >=102/76 för naiv komposition, inte direkt spelprofil |
| Level3-räckvidd, vertikal/diagonal B3c, attack, B3d AI, B3e collision, PAL, riktig hårdvara | **NOT TESTED / EJ AUKTORISERAT** | Ingen senare implementation |
| Oberoende VERIFICATION | **INTE GENOMFÖRD** | MAIN har uttryckligen uppskjutit detta |

**Föreslagen nästa MAINGATE:** nytt specifikt auktoriserat arkitekturexperiment med (a) PF-scenen kvar tydlig när halo går genom hinder, (b) realistisk budget för P0/P1 + 2 riddare/bågskytt/pil/orb/HUD på hårdaste sammanfallande raden, (c) nivå3-ringens fulla lovade radie, (d) verklig 262-line/frame+worst-case profilerad scanline CPU, (e) explicit test av om zonindelning/tidsdelning ger tolerabel läsbarhet. Separata ROM-banked datatester kan följa, men ingen permanent bankformat väljs av ROM DEVELOPMENT här. **R1 avslutas utan att påbörja B3c.**

## 8. Exakta revisions- och evidenslänkar
- Full grön 4-ROM/492-Stella/CPU- och object-headroom-körning: https://github.com/Odourman/the-skraun/actions/runs/43906912249
- Exakt 13-center frame-stepped joystick-/latensmätning i Stella Debugger: https://github.com/Odourman/the-skraun/actions/runs/43906553221
- Direkt Stella Debugger: 3 renderer-ROM × 3 positionslägen = 9 bildrutelängdsmätningar: https://github.com/Odourman/the-skraun/actions/runs/43906728214
- Original Stella-bildmontage (FAST/OPT/SCORE/P1, endast äkta emulatorbilder): https://drive.google.com/file/d/1SfLoaSVDQQ_L0P0kHCPBx9qEqvDi-Jj8/view?usp=drivesdk
- Slutlig GitHub Actions-artifakt med källor+ROMs+492 bilder+listnings/symbolfiler+CSV: https://drive.google.com/file/d/17H-XPKkGtj0WDZ19OEMpatk135odLyM0/view?usp=drivesdk
- Frame-steg-session: https://drive.google.com/file/d/1mVgV1LV_qBIdyBnJTum7jbxhSrOty39I/view?usp=drivesdk
- Limiting P1/SCORE/OPT debugger: https://drive.google.com/file/d/1cutIww0lBTWVvRcl4-dF1Q0vLXdCwOao/view?usp=drivesdk
- Samlad Drive-mapp: https://drive.google.com/drive/folders/1AwRVTCgs5Dz99Zwj0-7n3A4IAfJVILf7

**Ingen oberoende VERIFICATION, ingen merge till main, ingen B3c/B3d/B3e/kollisionsimplementation.**
