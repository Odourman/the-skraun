# THE SKRAUN — MAIN III N6: gemensamt färg- och objektkontrakt, källbaserade kombinationstester

**Datum:** 2026-11-21. **Beslutsklass:** `N6_STARTED / SOURCE_ONLY_A_B_COMPLETE / UNIFIED_PHYSICAL_SCHEDULE_UNPROVEN / NO_N7_GO`. **Ingen** ROM, DASM-implementation, ny bitmap, kartändring, mapper, PR-merge, ROM DEVELOPMENT-arbetsorder eller independent Verification. Färgprincipen **världskamouflerad ranger** kommer från användarens nya uttryckliga beslut; föreslagna faktiska färgkoder och resursallokeringar är ännu **inte** implementerade eller visuellt accepterade.

## 0. Resultat och tekniskt beslut

1. **Spara färgskrivningar där det är möjligt utan att ändra spelet:** två riddare bör använda **samma exakta röda TIA-kod** som första testvariant. Rangers distinkta kamouflagefärg ska följa världen, inte bytas till riddarrött för att optimera. Skraun ljusgrå, guldhalo guld, orb bör helst guld, pil kan kandidatera som Skraun-grå M0.
2. **Låt blivande grafikmotorn schemalägga ALLA objekt med samma registerkalender**, inklusive P0, P1, PF, BL, M0, HUD, AI och logisk soliditet. R3:s separata PF- och P1-arbetsvägar kan inte bara fogas ihop.
3. **Nytt source-exakt kvantitativt resultat:** för 13 genuina R3-X-lägen ×176 fysiska arena-rader (=2288 radfall), hade blinda 6-PF-byte-skrivningar varit 13728 hypotetiska stores. En source-byte-delta-schemaläggare kräver i en **adaptiv varannan-rad-hypotes** 3944 PF-byte-store-händelser totalt. Men av de **416 faktiska samtidiga HALO+SCENERY-krav-radfallen** behöver **331/416 (79,6%) fortfarande 5 eller 6 PF-byte-stores** i denna kandidat, plus färgsättnings- och aktörsjobb. **Totalbesparingen gäller till stor del enkla/tomma rasterrader, INTE automatiskt den värsta scenen.** Detta är en minimi-/händelseräkning, inte cykeluppmätt vinst.
4. **Samma-Y P1-radinterleave blev mindre pessimistisk:** R3 8-source-row originaldiagnostiksprites dubbelritas över 16 fysiska rader. Tvåvägs-fördelning kan visa alla 8 källrader för vardera riddaren, men endast hälften av fysiska pixlar. Trevägs-splitt mellan riddare/riddare/ranger visar **6/5/5 distinkta källrader av 8**, 22/60,20/68,20/56 av respektive objekts dubblerade ljusa source-pixelinstanser. Tidigare slentrianpåstående att bara 2–3 källrader skulle visas var för pessimistiskt. **Detta visar bara bildsample-kapacitet; ingen verklig 76-cykels-RESP/GRP/COLUP1-kernel finns ännu.**
5. **Gate:** **INGET GO för N7 eller produktionsarkitektur**: de hårda kombinerade X80/X84 PF/BL-färgkonflikterna, fria same-Y P1-positioner, P0-occlusion och minnes-/rasterbudget saknar fortfarande en enda uppvisad fullt laglig fysisk tidsplan. N6:s källbaserade del A/B har nu framtagna konkreta kandidatmodeller och reproducerbar data; **N6-C, integrerad ägar- och cykelplan, står OPEN**. Det är avsiktligt mer precist än att kalla en plan 'fungerande'.

## 1. Ursprungskällor och vad som gäller

- GitHub `Odourman/the-skraun` main läst LIVE före N6, HEAD `9867050cda0ca9fff9abaf518ee14b9d498c3369`.
- [Beslut 01–60 med tillägg](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md): Skraun upprätt ljusgrå, U1-LEG1 fryses; två samtidiga svärdsriddare och en ranger, en pil, en kvarliggande orb och 360° rörlig guldhalo; solida hinder stoppar kropp/svärd/pil men inte halo; ~0,4 s läsbar huggvarning; fyra världar; poäng/liv HUD.
- [U1-LEG1 accepterad konst](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md): original exakta A/B-källmasker, perspektiv och riktning; grå färg.
- [N3 S0–S9 samt objekt- och färgkontrakt](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md), [fixtures](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json).
- [N4 färg-/PF-negativ](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N4_PF_G1_SOURCE_TIMING_REPORT_2026-11-17.md), [N5 R3 36 autentiska Stella-bildrutor](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N5_P1_SAME_Y_FEASIBILITY_AND_GAME_DECISION_2026-11-17.md), [3-pass Let Me Out!-överföring](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_THREE_PASS_LET_ME_OUT_TRANSFER_TO_THE_SKRAUN_2026-11-21.md).
- Fryst **R3 exakt `romdev_r3_overlap.asm` Git-blob SHA1** `3c9ed79078eee6a0c63100614a593f92e240b5e8` återverifierad av replay-skript med Git blob-protokoll. Källor tillverkade från gamla autentiska N4/N5-arkiv, inte återskapade från minnet. För S1/S2/S3 är fienderna de frysta **diagnostiska** 8-radersmaskerna (inte slutligt godkänd riddar-/rangerkonst).
- Atari 1979 [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html): fysiska TIA-färgdomäner, 76 6507-cykler per rad, NUSIZ, VDEL. [Video Chess/IEEE 1983](https://www.atariage.com/2600/archives/design_case.html): raden-varannan-interleave är en historiskt verifierad mekanism, inte bevis för just Skrauns X/Y-scenario.

## 2. Ny användarauktoritet: Ranger i miljökamouflage

**User decision 2026-11-21:** "Bågskytten ska vara kamouflerad. Det ska vara poängen. Han är en Ranger som gömmer sig i miljön." Användaren gav tidigare konkreta exempel **grön i skogen** och **lila i drömvärlden som spiralerna**. Detta har **företräde över äldre formuleringar att bågskytten alltid måste vara grön**. Ranger måste fortfarande gå att upptäcka med rörelse/attackinformation; inget beslut om permanent osynlighet, träffimmunitet, ändrad pilriktning eller AI. De föreslagna stenblå- och dimblå-färgerna i berg/natt är **MAIN designkandidater**, inte tidigare explicit valda TIA-koder.

### 2.1 TIA-färggrafen: endast fyra register, inget magiskt extra lager

| Register | Fysisk ägare | Primär konfiguration | När den hjälper | Hård stop-regel |
|---|---|---|---|---|
| `COLUP0` | P0 och M0 | Ljusgrå Skraun; **M0 kan prövas som lika ljusgrå pil** | Undvik färgväxling mellan Skraun och projektil om M0 används | M0 är en smal 1-bit-figur och måste röra sig fritt, även när P0 är aktiv. Om pil får annan färg krävs ny ägarplan. |
| `COLUP1` | P1 och M1 | **Båda riddare exakt samma rött** (kandidat); ranger får *egen världskamouflagekod* | Eliminerar särskilt riddare↔riddare-färgbyte; ranger↔riddare-kostnad kvar | Tre olika oberoende X/Y-sprites visas inte av färgval ensamt. M1 kan inte få fritt pilfärgval. |
| `COLUPF` | PF och BL | PF = hinder i världsfärg **eller** aktiv guldhalo; BL = möjlig guldorb när COLUPF verkligen är guld på dess rad | BL och PF-ring kan vara GULD tillsammans utan Venetian om exakt samma rasterfärg och former tillåter | PF-hinder i annan färg samtidigt + guld-BL på samma rad är INTE automatiskt möjligt. |
| `COLUBK` | Global BK | En lågmäld, mörk bakgrundston per värld | Byte mellan världar/zoner utanför kritiska pixellinjer kan vara billigt | Ändrar alla oöverlagda pixlar, kan inte maska en rörlig guld-ring. |

`NUSIZ0` delar bitfält för P0-storlek och M0-projektilbredd: att bibehålla P0 x4 med önskat M0-missilbreddsvärde är principiellt möjligt, men kräver exakt registerbyte, horisontell positionering och Skraun-källbild utan HMOVE-förskjutning. **Inget extra färgregister** uppstår. P1/M1 samma villkor.

### 2.2 Objektfärgplan, preliminär; skilj exakt registerlikhet från visuell släktskap

| Objekt | Kontinuitet | Första testvärde eller öppen kandidat | Varför |
|---|---|---|---|
| Skraun | FAST ljusgrå | R3-prototyp `COLUP0=$0C`; exakt luminans senare i NTSC/Stella | Fryst visuell identitet, P0 ska inte användas som permanent röd fiende |
| Två riddare | FAST samma röda TIA-byte, **förslag** | R3 hade olika `$44/$48`; välj en *gemensam* kandidat först (t.ex. `$48`) | Ingen riddare↔riddare-färgövergång i P1 |
| Ranger | **Världskamouflage FAST SOM PRINCIP** | Skog grön; dröm lila; berg stenblå; natt dimblå. **Faktiska fyra TIA-byte OPEN** | Medvetet smälta in i miljön; P1 får färgbyte när typ skiftar |
| Halo | FAST visuellt guld | R3-prototyp `COLUPF=$2E`, NTSC-visuellt måste fastställas | Samma magiska 360-gradersattack på alla tre levels |
| Orb | FAST synlig och nåbar | Guld som **kandidat**: BL kan dela guld-`COLUPF` på rätt rad | Samma hardware hue som aktiv halo förbättrar samspel men PF/BL-scenen saknar fri gul färg när stenrader använder COLUPF |
| Pil | FAST tydlig hotbild | M0 i P0-ljusgrå är **kandidat**; alternativ ägare kräver källtest | En missil i taget enligt canon; ingen dold rangerfärgad pil i berg/natt antas |
| Hinder | Världsbundet, distinkt från guldhalo | Skog olivgrön, berg blågrå, dröm lila, natt blågrå: **endast estetiska kandidater** | Håller PF-sten/solids olika halo; färgen är INTE kollisionslogik |
| HUD | FAST kontrast, separat band | Neutral ljus text, delar P0/P1 färgdomäner endast inom HUD-zon | Score/lives prioriteras; måste återställa register innan arenakernel |

**Viktig korrigering:** att skogens ranger och PF-träd har *samma färgfamilj*, eller till och med samma exakta TIA-byte i `COLUP1` respektive `COLUPF`, **sparar i sig noll P1↔PF-färgskrivningar**. Dessa är helt separata register. Den verkliga beräkningsvinsten kommer av färre COLOR-BYTEN INOM EN OCH SAMMA registerdomän och från förutsägbara bytes per rasterzon. Att göra både riddare och ranger röda för att spara P1-färg skulle urvattna användarbeslutet och **rekommenderas inte**.

### 2.3 Fyra världar, försiktig plan

| Värld | BK kandidat | PF hinder/spiral kandidat | Ranger, camouflage | TIA-/spelrisk |
|---|---|---|---|---|
| Skog 1–2 | Mycket mörkt skogsgrönt | Olivgrön vegetation/stubbar | **Grön** som buskar/träd, jämförbar luminans eller aningen ljusare | Upptäckt beror på rörelse, inte stark kulör. |
| Berg 3–4 | Mörkt blågrå | Skiffer/stenblå | **Dämpad stenblå** | Grå Skraun måste särskiljas från sten/berg. |
| Dröm 5–6 | Mycket mörk violett | Lila spiraler/ruiner | **Lila** som spiralerna | Färre statiska PF-spiralbyten behövs; extra dynamiska spiralanimationsregister får inte smygas in. |
| Natt 7–8 | Nästan svart/mörkt marinblå | Dimblå ruiner | **Dämpad blågrå** | Mörkt rangerkamouflage får inte göra avfyrning och farlig pil oläsbara. |

**Ingen slutgiltig Atari NTSC-hexpalett** är legitim att låsa från bara konceptfärger. Gör fyra världars contrast-/camouflage test i verklig Stella först. PAL och CRT/RetroN77 kan återge färger annorlunda. När ranger rör sig och stannar för skott ska det fortfarande kunna observeras som en avsiktlig spelmekanisk signal; kamouflage får vara svårt, inte bugglikt omöjligt.

## 3. Sammansatt kernelplan (K0–K6), med konkreta HALT/OPEN

| Kernel-zon | Vem ritar vad | Färger/förberedelse | Källstatus | Problem att lösa före N7 |
|---|---|---|---|---|
| `K0 HUD` | P0/P1/PF till score/lives bara i HUD:s egna scanlines | Neutral kontrast, skriv tillbaka P0/P1/PF-färg och NUSIZ/GRP/ENABL innan arena börjar | Provrutiner finns, ingen verklig score/lives i R3 | Exakt zonövergång och riktig HUD-text, inte cyan placeholder. |
| `K1 SCENE_QUIET` | P0 Skraun; P1 fiender på skilda Y; PF en världsfärg på hinder; BL orb där guld möjligt | Sparsam PF-delta och Y-bandsbyte | Historiskt/enskild R3/N4 source | BL guld på samma rasterrad som världsfärgat PF-hinder kräver GULD-fönster eller särskild fri Y-zon. |
| `K2 HALO_FREE` | PF guldhalo när scenen inte kräver kontrasterande PF-bitar samma Y | P0 gray; BL orb kan samritas med gul PF; M0 ljusgrå pil | SOURCE_CONDITIONAL | HL/HM-positioner och 1/2/3nivå exakt, inte bara R3 L3. |
| `K3 HALO+SCENERY` | PF-mask för båda visuella lager i samma bildruta | **T1:** source-delta+adaptiv fysisk rad-Venetian. **T1b:** genuint färgklockskorrekt midline COLUPF | **UNPROVEN** | 4 riktiga färgbyten vid X80/X84 om två färger på samma rad; adaptiv Venetian offrar faktiska PF-pixlar och kräver fortfarande 5/6 PF-byte stores på många rader. |
| `K4 TWO-ENEMY-SAME-Y` | P1 dela en av två aktörer mellan jämna/udda fysiska rader; normal Y-reuse annars | Två identiskt röda riddare → inga knight↔knight-hue switch | SOURCE_ROW_ARITHMETIC_ONLY | Varje P1 horizontal reset och maskbyte måste faktiskt få plats inom egna 76 cykler, inklusive PF och P0. |
| `K5 THREE-ENEMY-SAME-Y` | P1 tre olika aktörers X + bitmap + färg, överlappande även P0 | Trevägs-Venetian kan lämna 5/6 unika artkällrader, kamouflerad ranger behöver separat COLUP1 | SOURCE_ROW_ARITHMETIC_ONLY; **highest blocker** | S2 nära X och S3 svärdsförvarning; 3-way artifacts, HMOVE/timing och P0-skymning. Även om fiender i RAM är tre får de inte bli osynliga ofarliga. |
| `K6 ORB/ARROW-CONFLICT` | BL orb + M0 arrow + PF + P0/P1 samtidigt | Orb guld endast om aktuell COLUPF är guld; grå M0 med P0 | SOURCE_RESOURCE_GRAPH_ONLY | Orb ligger kvar om L3, synlig direkt från banstart; säkra förutbestämda orbplatser kan **kandidatera** till helt PF-tomma horisontella Y-band (måste kontrolleras i de ännu ej fastställda 8 kartorna), men det går inte att låtsas att alla sådana band finns. |

**Spelregel och färg måste hållas isär:** en stens faktiska soliditet och halons genomträngning simuleras i logiska hitboxar/RIOT, **inte** från display-PF som kan alternera/randas. Att en värld har lila PF får inte ändra hur stenar stoppar pilar eller hur guldhalo går igenom.

## 4. N6-A: source-exakt PF-delta, 13 X ×176 fysiska rader

### 4.1 Reproducerbarhet

Kör `python3 N6_SOURCE_ONLY_REPLAY.py` i detta paket. Replay importerar **ENDAST** den frysta N4-filen `R3_SOURCE_EXACT_MASKS.json`, original R3 `.asm`, N4- och N5-baslinjereferenser. Git-blob SHA för käll-ASM verifieras programmässigt. Källbild: R3 19-bytars halo/scenery-tabeller vid X56,60,...104 och fryst 177-entry RingRowMap. Varje maskrad dubblas till en tvåfysisk-radsgrupp. Dessa är **176 diagnostiska arena-rader**, inte skärmens alla 262 och **inte 13 positioner samtidigt**.

För en fysisk rad: PF vänster sida är de tre bytena före beamens mitt, PF höger sida de tre efter mitt. Rekonstruktionen räknar minst nödvändiga ändrade bytes mellan **föregående fysikradens högra PF-värden → nuvarande vänstra PF → nuvarande högra PF**. Optimistisk 0/1/2/3/4/5/6-byte-ändringsräkning: **inga** faktiska 6507-indexladdningar, ROM-hämtningar, tidsfönster eller svar på P1-cykelkonflikter ingår. Ett PF-värde som inte ändras behöver ingen *funktionell* ny STA under dessa villkor, men det finns **ingen dokumenterad generell zero-cost select/dispatch**. Den faktiska dynamiska kontrollkostnaden kan äta upp vinsten.

Fem separata jämförelser:

| PF-policy | Byte-skrivningar över 2288 radfall | Jämför 6/rad =13728 | Bevarad halo/source-PF-cell-densitet | Bevarad solid/source-PF-cell-densitet | Färgkostnad / observation |
|---|---:|---:|---:|---:|---|
| Endast halo | **3592** | 73,8% färre | 100% | 0% | Försvinner hinder – **inte tillåten fullscene** |
| Endast scen | **2496** | 81,8% färre | 0% | 100% | Ingen halo – **inte tillåten fullscene** |
| OR-merga allt i EN färg | **4400** | 68,0% färre | 100% | 100% | Båda maskerna ritas men **samma färg**; spelaren tappar visuellt distinkt gold-vs-solid. **EJ tillåtet utan user acceptance** |
| Fasta varannanrad gold/solid | **2992** | 78,2% färre | 50% | 50% | Endast halva bådas ursprungliga fysiska PF-cellinstanser; värsta läsbarheten |
| **Adaptiv Venetian vid faktisk halo/scenery Y-konflikt** | **3944** | 71,3% färre | **81,52%** | **50,00%** | Bättre halo än fast parity; fortfarande half-res hinder. Kräver totalt **416** intrascen fysiska rad-till-rad-färgövergångar för 13 X-spår sammanlagt, inte frikostigt gratis. |

**Varning för stora procenttal:** 2288 radfall inkluderar många fysiska rader där både maskerna är helt tomma. Besparingen under tomma rader är mycket större än under de 416 konfliktraderna. Totalt resultat är alltså **inte** 71,3% fri CPU-budget i den kritiska kerneln.

### 4.2 Just de svåraste källraderna, X80/X84 source mask 98

Både X80 och X84 har 2 haloceller och 3 hinder-/sceneryceller i source-modeln på denna maskrad och **fyra** färggränser om båda ska bevara sina nyanser i samma fysiska rad (N4). Den direkta tvåfärgsvarianten saknar fortfarande exakta programmerade fyra `COLUPF`-deadline-skrivningar samt alla andra TIA-jobb. X80/X84 har här ingen identisk dubbelbokad cell, men andra X och rader HAR sådana cellöverlapp.

- X80/84 adaptiv parity, första fysikrad/arenaY78: **4 nödvändiga PF-byteändringar**, visar bara halo.
- X80/84 adaptiv parity, nästa fysikrad/arenaY79: **5 nödvändiga PF-byteändringar**, visar bara hinder och **byter COLUPF färg** från guld till världsfärg.
- Av **416** source-rader där båda visuella kategorier behövs i samma Y-område enligt originalmaskerna behöver `PARITY_ONLY_ON_CONFLICT` **85×4, 295×5, 36×6** PF-byteändringar. **331/416 = 79,57% kräver minst fem** innan CPU ska rita P0, P1, M0, BL eller läsa radrenderdata. Alltså inte ett gratis Lovande-PASS.
- `OR_MERGED_SINGLE_COLOR` behöver minst 5 eller 6 PF-ändringar i **samtliga 416** samtidiga färgkonfliktrader, men då blir scenen inte tvåfärgad. Dess enhetliga guld PF kan ge mycket mindre färgkonflikt, men påverkar objektidentitet och kanonisk visuell skillnad.

**N6-A RESULT:** **Analytisk mekanism bevisad:** PF-byte-delta minskar antalet nödvändiga värdeändringar i vissa rader. **Ej bevisat:** 6507 kan genomföra de sparsamma byte-stores inom rätt fysiska colorclock-fönster samtidigt med P1, P0, BL och proj och full visuell kvalitet. Venetian är testbar visuell reserv, **inte en accepterad exakt-utseende-pass**.

## 5. N6-B: tre separata aktörer och COLOR-lower bound

R3 källkod anger tre diagnostiska fiendefärger `EnemyColor: dc.b $44,$48,$C6`. Det finns alltså även **en onödig extra röda-riddare↔röda-riddare-färgskillnad**. Att i en framtida renderer ge båda riddare exakt samma röda TIA-byte kan sänka den nödvändiga antals-färgövergångar i **en hypotetisk** horizontell same-line P1 tre-aktörsström, men fri X och GRP1-retrigger måste fortfarande lösas separat.

| Source stress-X från N3 | X-sorterade aktörer | Tre separata R3-färger ger minst | Båda riddare samma röda ger minst |
|---|---|---:|---:|
| S1 original | Knight1(32)→Knight2(101)→Ranger(147) | 2 | **1** |
| S2 X permuterad | Knight2(40)→Ranger(80)→Knight1(120) | 2 | **2** |
| S2 X nära | Knight1(67)→Knight2(83)→Ranger(101) | 2 | **1** |
| S3 skymning | Knight1(105)→Knight2(124)→Ranger(147) | 2 | **1** |

**Detta är antalet nödvändiga övergångar i FÄRGVÄRDE, inte ett beräknat antal färg-STA eller vunna CPU-cykler.** Tre alltför tätt placerade sprites kan vara fullständigt omöjliga att rendera genom direkt `GRP1+COLUP1`-byte i mellanrummet även när färgerna är lika. S2:s täta x=67,83,101 och S3 x=105,124,147 är stop-fall.

**Ny egen kontroll av Venetian-sampling (R3-exakta 8 source-rader, 2 fysiska rader/källrad):**

| P1-policy | Aktör | Fysiska rader tilldelade av 16 | Olika source bitmap-rader bevarade av 8 | Upplysta källpixelinstanser bevarade |
|---|---|---:|---:|---:|
| 2-vägs radvarvning | Knight1 | 8 | **8/8** | 30/60 =50% |
| 2-vägs radvarvning | Knight2 | 8 | **8/8** | 34/68 =50% |
| 3-vägs radvarvning | Knight1 | 6 | **6/8** | 22/60 =36,7% |
| 3-vägs radvarvning | Knight2 | 5 | **5/8** | 20/68 =29,4% |
| 3-vägs radvarvning | Ranger | 5 | **5/8** | 20/56 =35,7% |

Nuvarande ursprungliga 8-row diagnos-bitmap är inte framtida GODKÄND fiendekonst. En riktig svärdsvarningssekvens finns inte i R3. Ovanstående kan alltså INTE bevisa att en riktig svärdsanimation förblir tydlig, bara hur mycket källdata en radkvot kan visa. Med trevägs-delning kan 5 eller 6 unika 8-raders segment bevaras, bättre än tidigare löst uppskattade 2–3; den fysiska pixelmängden minskar fortfarande kraftigt. Rotera eventuellt parityfas mellan bildrutor bara som **framtida kandidat**: det återställer källrader över tid men kan ge störande tidflimmer och ökad register-/positionskostnad.

**N6-B RESULT:** fast/sluten nyans för knight pair är en konkret rimlig förenkling; tre-fienders god läsbarhet same-Y med en enda P1 och fri X/Y är **fortfarande OPEN**, P0-occlusion och P1↔PF tidsdeadlines inte lösta.

## 6. N6-C: exakt gemensam hårdvaruresursplan — HOLD, inte faux PASS

| Samtidighet / scenario | Måste finnas fysiskt i samma kärnplan | Känt analytiskt hinder | N6 beslut |
|---|---|---|---|
| S0 | Fryst godkänd U1-LEG1 P0 på alla tre storlekar | x4 level3 och P1 ompositionering fick inte flytta P0 | **OPEN** som gemensam kärna |
| S1/S2 | Två röda riddare plus kamouflerad ranger, alla egna X/Y och Y=78 | 3 olika GRP1, x-sort, ranger hue, 76c och PF samtidigt | **HARD RISK/OPEN** |
| S3 | P0 L3 + aktiv huggvarning + två fiender | 94,1% skymning av en knight i föregående R3-deltest | **HARD RISK/OPEN** |
| S4/S5 | 360 gold ring + distinkt solida hinder | N4 4 inomrad-färgövergångar X80/84; ADAPTIVE stripe minskar pixlar | **HARD RISK/OPEN** |
| S6 | Orb som kvarstår vid level3, pil, HUD samtidigt | BL guld kontra PF-världsfärg; M0-grå pil och andra TIA-lägen saknar integrerad timing | **HARD RISK/OPEN** |
| S7 | Riddarvarning 0,4s, pil flyger, död/respawn, orb pickup | En pixelrender PASS får inte ersätta joystick- och timerproven | **OPEN** |
| S8 | Alla fyra färgteman, ranger aktivt kamouflerad | Låg kontrast önskad men faror måste gå att uppfatta; PAL/NTSC/CRT skiljer sig | **OPEN/PALETTE_UNMEASURED** |
| S9 | Fri 8-riktnings Level3, solid glidning, säker orb-growth | Kolliderar med helraster och 128B liveness om stor P1-buffer behålls | **OPEN** |

**Kritisk säkerhetsmarginal:** R3:s redan testade source-estimat 72/73/74 av 76 CPU-cykler för vissa synliga rader lämnar bara 4/3/2. Att *lägga till* ett extra 3-cykel TIA-byte-store på en 74-cykelsrad överskrider 76. Alla ändrade färg-, sprite-, P1/BL/M0- eller PF-skrivningar kräver därför att en **ny kernel ersätter gammal beräkningskostnad**. I Let Me Out! gav en verklig full 76/76-rad + 2-cykel INY 263 frame lines; det är varningen, inte en färdig lösning.

**Minnesgräns:** 128B internt RIOT **inklusive return stack**. R3 gammal 23B state+89B P1Buf=112B; COL1 separat 28B är INTE en drop-in. Ingen konkret N6 RAM-adressbok har bevisat same-frame: två knights+one ranger pos/AI/anim/hit/cue, orb, pil, level/lives, PF mask pointers, register predecode buffer, stack. Extra cartridge RAM kan prövas med separat användarbeslut och mapperspec, men tillför **ingen** ny TIA-cykel eller färg. Normal F8/F6 8/16K ROM bank också separata beslut; R3 4K-diagnos är ingen allmän spelgräns.

### 6.1 Föreslagen men ännu ej bevisad fysisk arbetsuppdelning

1. **VBLANK:** läs SWCHA/INPT, uppdatera rörelse/kollision AI, orb/pil och varningstimer, sortera aktörernas X/Y-intervallevents, bygg en **kompakt lista** av endast verkligt ändrade PF-byte, ranger/knight `COLUP1`-färgtid, BL enable och M0-placering. *Kräver byte-live RAM- och VBLANK worst-case-räkning; inga otestade RAM-buffrar reserverade ännu.*
2. **HUD-band:** färdig avgränsad poäng/liv-mask; återställ TIA-färg och grafikkopior före arenan.
3. **Arena rasterlinje:** välj förberäknad K1/K2/K3/K4/K5 variant beroende på faktisk kollision av Y-banden. Uppdatera PF endast när värdet ändras, men bara om source-exakta fysiska registerdeadlines tillåter. Preload P1 före dess grafikhändelse, respektive M0/BL; logiska hinder finns separat.
4. **Overscan:** timerpoll med INTIM-underflow-bevakning plus garanterad WSYNC-fas efter den typ av Let Me Out!-fel som gav 289 i stället för 262 scanlines. Här har ingen ny Skraun-patch eller cykelmätning gjorts.

Denna text är en **arbetsarkitektur på konceptnivå**, INTE en bekräftad 76-cykels assemblerloopp. En sådan kontroll behöver `physical_scanline`, `tia_colorclock`, `opcode`, `cycle_start/end`, `write_latched`, `PF0/1/2`, `GRP0/1`, `COLUP0/1/F/BK`, `RESPx`, `HMOVE`, `VDEL`, `ENABL/ENAM0`, plus RAM/stack highwater och frame count för samma state.

## 7. Förbättringar inför nästa beslut och tydlig STOP/GO

**Godkänt av MAIN som teknisk DIREKTION, inte som implementation:**
- Bygg **ett** färgkontrakt med ljusgrå P0, två likröda knight P1-hues, ranger camo per world, guld PF/BL när kompatibelt, grå M0 arrow kandidat, separata mörka världsbakgrunder. Icke godkända exakta TIA-byte och faktisk gameplaygrafik behålls öppna.
- Pröva originalsource **0..6 verkliga PF-byteändringar per linje** snarare än att anta att max två ändringar gäller även vår rörliga ring; vid konflikt visar detta underlag 4/5/6 stores, inget gratis universalknep.
- Utvärdera BL-orb i PF-tomma **horisontella** Y-rader när de verkliga banlayouterna skapas: möjlig mappdesign som bevarar få säkra orbplatser. Det är ett förslag, **ingen** ny låst karta/spawnregel.
- När fienderna ligger långt från P0 i Y kan P0 möjligen återanvändas i en annan rasterzon för del av fiendevisningen **med bevisad korrekt registeråterställning**; det löser inte S3 där P0 och fiender överlappar. Beakta M0/Skraun grå färgdomän om P0 får röd fiendekulör på andra Y-rader.
- Ett första framtida mikroROM-uppdrag (kräver separat uttrycklig authorization) måste **inte** testa tre oberoende effekter: det ska testa den värsta gemensamma PF+P1+P0-raden, med BL+M0 aktiva, och även med en 24-frame sword cue. Visuell kvalitetsacceptans och riktig spelbar ROM är nästa separata grindar, inte automatisk pass.

**NEJ till direkt N7 nu.** Första öppna N6-gaten är en verkligt möjlig **enhetlig per-fysisk-rad event-/timing-/RAM-tabell med specificerade registerdeadlines för samtliga N3 S0–S9**. Om ingen sådan kan konstrueras utan ett pixel- eller gameplaytapp behöver användaren välja kompromiss/hårdvara uttryckligen. Inget tyst färgskifte av Skraun, inga osynliga riders/ranger och inga falska 60Hz-PASS.

## 8. Leverabler och metodgräns

- `N6_SOURCE_ONLY_REPLAY.py` — deterministiskt källbaserat arkivprogram. **Inga externa paket / ingen ny ROM / ingen grafik som ger falsk skärm-PASS.**
- `output/N6_SOURCE_13X_176ROWS_PF_EVENTS.csv` — 11 440 rader (5 policies ×13 X ×176); per fysiskt source-kandidat-rad exakta PF-byte-delta och source-art pixelkostnad. **OBS** 5×2288=11440.
- `output/N6_P1_SOURCE_ROW_STRIPES.csv` — hur många exakta R3 source bitmaprader/pixlar två-/trevägs-Venetian matematiskt kan representera, utan verklig TIA-radkod.
- `output/N6_P1_COLOR_SWITCH_BOUNDS.csv` — färgövergångar givet de fyra verkliga/syntetiska N3 X-ordningarna om två riddare delar exakt TIA-rött.
- `output/N6_SUMMARY.json` och `output/N6_REPLAY_LOG.json` — full aritmetik med arkivexakt källa, varningar och resultat. `source_inputs/` är återpublicerade frysta N4/N5-källskärvor för beviskedjan, **inte vidareutvecklad spelkod**.

**Slutlig klassning:** `N6_A_SOURCE_MODEL_DONE`, `N6_B_SOURCE_MODEL_DONE`, `N6_C_UNIFIED_TIA_CPU_RIOT_BEAM_PROOF_OPEN`, `N7_NOT_AUTHORIZED`, `SOURCE_ONLY_NOT_VERIFICATION`.

## 9. N6 tillägg 2026-11-21: adaptiv fiende-Venetian vid PARTIELL Y-överlappning samt omprövningsgrind

**Auktoritet:** användaren betonade uttryckligen att MAIN inte ska 'piska en död häst', utan pröva verkliga lösningar och **överväga kreativa omval om ett krav visar sig orimligt**, utan att ge upp vid första negativa test. Detta auktoriserar att analysera och rangordna alternativ i N6; **ingen specifik canon-ändring, N7 ROM eller permanent avkortad fiendebesättning är härmed godkänd**.

### Kontinuerligt Y-sorterad, adaptiv P1-ägarskap i stället för statisk varannan-rad hela arenan

- Dela inte om aktörer bara ligger på skärmen samtidigt. För en 16-physical-line R3 source sprite, sätt ett levande rasterintervall [Y, Y+15] per actor och räkna överlapp per fysisk Y. Om endast en actor lever på aktuell Y får P1 full rasterradsampling, även om andra aktörer existerar ovanför/under.
- Om två delar samma fysisk Y kan P1 **kandidatmässigt** ha 2-way even/odd raster line interleave lokalt. Om tre delar samma Y pröva kort 3-way interleave (det kan kräva mer mask-/positioneringsarbete än 76c tillåter). Välj prioritet för riddarens ~24f windup om tekniskt möjligt; den får inte döljas.
- Exempel: Knight1 fysisk Y40–55, Knight2 Y48–63, Ranger Y52–67. Schemapartition: 40–47 K1 only (8 lines); 48–51 K1/K2 (4); 52–55 K1/K2/R (4); 56–63 K2/R (8); 64–67 R only (4). Källa: intervalldelningsanalys här, **inte assemblerad emulatorbevisning**.
- Caveat: samma P1 hardware generator kan bara ge en fri X vid en given tid utan extra reposition/GRP. **Att skriva olika GRP1 per fysisk rad är inte samma sak som att flytta dess horisontella läge.** RESP1 (coarse)/HMP1(HMOVE)/NUSIZ/VDEL positioneringsdeadlines, artefakter vid ompositionering, same-line order och X-permutation måste räknas på all Y-positionering; en 2-way actor m.m. kräver ibland växlande stora X hopp varje fysisk rad. R3 gamla HMOVE sidoskift för P0 måste vara negativ kontroll.
- En alternativ ägarstrategi värd att jämföra: om P0 (Skraun) inte är aktivt i rasterbandet kan **P0 temporärt användas av en fiende** medan P1 ritar övriga, förutsatt korrekt P0 originalgrafik, 4×-bredd på level 3, P0/M0 grå färgkoppling, repositioning/restore och inga samtidiga Skraun-hits. Detta är en ny arkitekturhypotes, inte en gratis andra aktör: M0 pil och flera Skraun Y-närvarofall kan ta bort möjligheten. Får bara användas om inga aktiva P0-originalpixlar förloras.
- NUSIZ copies när mask/X följer lagliga spacing kan användas lokalt, inte göra fria X till fasta X; GRP rewrite mellan kopior måste beam-timed. Extra 3-line-prototype only if each 76c physical line legal, source pixel preserved enough and all TIA owners included.

### Kreativa omval: minsta intrång först, explicit tradeoff

| Fallback | Typ av ändring | Teknisk hypotetisk vinst | Kostnad / nödvändig användarbedömning |
|---|---|---|---|
| 0. Dynamisk P0/P1/Y-scheduler, två röda samma TIA-byte, sparse PF | **Ingen canon-ändring** | Delar rasterresurser när verkligt lediga | Kräv full käll-/ROM-bevisning; fortfarande beam/stack-problem |
| 1. Förändra fiendernas visuella *höjd* eller varningspose, behåll silhuett/roll | **Mindre grafikjustering** | Färre Y-overlap rader och eventuellt mindre trevägsbehov | Kräver ny ART + user-godkänd läsbarhet; inte reducera varningsfönster tyst |
| 2. Ändra halons *visuella* ritning men behåll 360° logisk räckvidd | **Grafik-kompromiss** | Kan minska PF0/1/2 och 2-färgs inom samma line, speciellt om endast en färg krävs | Tydlig preview krävs, ring genom hinder och effekt bibehålls logiskt |
| 3. Lokalt 2-/3-vägs-Venetian eller begränsat frame-flicker | **Visuell kompromiss** | Fler objekt samtidigt inom samma frame | Färre fysiska pixlar och risk för svärd/ranger osynlighet, måste prövas 60Hz rörligt |
| 4. Ändra aktiva fiender till exempel 1 knight + 1 ranger plus reservspawn | **Större gameplay-ändring** | Minskar worst same-Y P1 samtidighet från tre till två | Användaren måste godkänna före ändrad active-knights canon; antal totalt kan hållas |
| 5. Superchip/annan mapper/extra CPU | **Hårdvaru- och kompatibilitetsval** | Mer RAM/beräkningsförberedelse | TIA scanline/färger oförändrade, original-cart/RetroN77 kompatibilitet måste särskilt prövas |

**N6-C beslutsregel:** Testa minst två VERKLIGT OLIKA komplett-kernelalternativ: (A) lokal Y-sort + P0/P1 owner-lending och minskad PF write scheduling; (B) samma design men lokal P1 Venetian där Y-overlap. För båda: worst S1,S2,S3 Y/close/permuted X/24f sword tell + S4,S5,S6 gold/solid/orb/arrow. Kräv 76-cycle deadline och 128B+stack; ignorera inte app/AI/HUD. Redovisa första fysiska counterexample för varje. Om båda faller, skriv ranked *specific creative compromise proposals* med sannolik påverkan, **inte** fler upprepade varianter av samma R3 20Hz helframe-flicker. Inget N7 eller självständig Verification får inledas som implicit nästa steg.
