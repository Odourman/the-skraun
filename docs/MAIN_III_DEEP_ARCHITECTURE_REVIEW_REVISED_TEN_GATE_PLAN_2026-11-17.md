# THE SKRAUN — MAIN III: fördjupad arkitekturprövning och reviderade tio nästa steg
**2026-11-17 | Projektledning, verifierad research och villkorad plan | INGEN ny ROM-, grafik-, mapper-, merge- eller oberoende Verification-auktorisation från detta dokument**

## 0. Beslutet i korthet

**Den gamla ordningen var inte optimal.** Den prioriterade en enda PF-färgrad före tillräckligt tidiga fullscenskrav, samma-Y P1-risk och fullständig RAM-/registerplan. Den riskerade också att fastna på att Stella `saveSes` producerar noll byte trots att tidigare COL1-arbetsorder uttryckligen accepterar en fullständig **mätt ELLER korrekt konservativt beräknad** cykelbudget med rätt märkning. Huvudmålet är fortfarande ett **verkligt roligt och tillräckligt läsbart originalkompatibelt Atari 2600-spel**, inte ett evigt diagnostikprojekt.

**Ny arbetsmodell:** två parallella förberedelsespår: (A) fryst COL1-bevisning och oberoende avgränsad acceptans, (B) konkurrerande falsifierbara fullscenarkitekturer på SOURCE-ONLY nivå. Dessa möts i en **tidig gemensam resurs- och worst-case-scen-grind**. Ingen ny fullrenderer eller gameplay-integration förrän de snäva färg- och fiendescheman som den kräver överlever mikro- och helscenevideoprov.

Detta dokument ersätter som aktuell rekommendation [tidigare tio-stegsplan](MAIN_III_TEN_RECENT_TEN_NEXT_TECHNICAL_ROADMAP_2026-11-17.md) men ändrar **inte** dess dokumenterade historik, fastställd spelcanon eller redan skrivna arbetsorder.

## 1. Kontroll av LIVE-källor och oförändrade grindar

- GitHub main observerad HEAD `fa2df256cec758833dff0f6db8c8266d86928e87`, normal repo CI [44080971191](https://github.com/Odourman/the-skraun/actions/runs/44080971191) SUCCESS. Ingen ny produktionsengine från våra status-commits.
- P01-COL1 befintlig [draft PR #27](https://github.com/Odourman/the-skraun/pull/27), branch `experiment/p01-col1-single-arena-collision-20261117`, observerad HEAD `90f89441b41a2e82408581b81d3743b1423e5cdb`. Den auktoriserade isolerade ROM:en är **4096 bytes** SHA-256 `f36217f9ae96a1e927795ca639b9d6b6cca68ad3e8e4f296afadcdb52d6a6ad2`.
- Faktisk [Stella 6.7.1 Actions #44078170646](https://github.com/Odourman/the-skraun/actions/runs/44078170646): 19 namngivna debuggerstyrda TIA GUI-bildscener, fyra solidkontaktriktningar, två hörnslide-negativ, positiva joystickkontroller, L3 90-frame resa, L2→L3 uppgradering tillåten/nekad, samtliga automatiserade assertions PASS. Testkällan är `.github/workflows/p01-col1-controlled-states.yml`, oförändrad originell P0-kollision ASM. SELECT demonstreras via **debuggerstyrd RAM-state-injektion efter RIOT-read** och inte verklig extern konsolknapp. 262 frame synligt som 0-index `_scanEnd #261`, inte maskinläsbar komplett CPU trace.
- [Drive original 19-case ZIP](https://drive.google.com/file/d/1B2oKbzx59GvGk2ip15fDrEwwHeVEy1Yb/view) verifierad som åtkomlig: 678660 bytes enligt Drive-metadata. ROM DEVELOPMENT rapporterar 138 medlemmar, SHA-256 `e49d5187a977c9c580ff46c16d50089424c79cebe5500458a06ac221d96331f4`, ZIP CRC PASS, men MAIN III har **inte i denna prövning oberoende binärnedladdat och SHA-verifierat ZIP:en**; N1 ska göra det.
- COL1 statiska konservativa DASM-uppskattningar enligt ROM DEVELOPMENT: högst ~63/76 synliga CPU-cykler i just COL1, VBLANK-arbete uppskattat <=2040/2752 timer-cykler, 28 bytes RIOT symbolvariabler och ca fyra stackbytes via två JSR-nivåer. DETTA ÄR **EJ uppmätt worst-case 6507 instruktionsspår** och får ej felaktigt jämföras med R3:s integrerade ~72–74/76 linje som om samma kod kördes.
- Research original [RESEARCH v1](https://drive.google.com/file/d/1_eCr20tCfJjyvnZLBZ_SQPcZqIkGfw_f/view), [original 30-raders teknisk matris](https://drive.google.com/file/d/1p7a52GmmjFnCKRfGwHRQrsO-ftSgB03A/view), [RESEARCH II 30k rapport](https://drive.google.com/file/d/1MtA0edh0hCOa-OoIBDNITml7k18FYvJD/view), [RESEARCH II ZIP](https://drive.google.com/file/d/1RJKpeaOZ_oatsOy9a4bwuEr0AE98IHIL/view) samt projektets egna all-30-auditer, PF-REP1/B/C och original R3 har granskats. **Research är rådgivande och inte automatiskt ny implementation**.
- [#1](https://github.com/Odourman/the-skraun/issues/1), [#15](https://github.com/Odourman/the-skraun/issues/15), [#19](https://github.com/Odourman/the-skraun/issues/19), [#23](https://github.com/Odourman/the-skraun/issues/23), [#24](https://github.com/Odourman/the-skraun/issues/24), [#25](https://github.com/Odourman/the-skraun/issues/25) är öppna. #1 avser den **äldre P01 `src/main.asm`-artefakten**, inte automatiskt den nya COL1. #19 avser en **annan ART1-testkernel** med extra L3 topp-rad, inte automatiskt åtgärdad av COL1:s bevis.
- Inga åtta kanoniska banor: de 8 rymliga skisserna och 24 collision K0-tabelluppsättningarna är rådgivande, källtestade alternativ, inte fysisk helrenderad gameplay.
- Oförändrat **bindande**: exakt U1-LEG1 upprätt ljusgrå A/B med semantiskt omvänd LEFT/RIGHT och L1 8x12, L2 16x24, L3 32x36; två samtidiga svärdsriddare + grön flyende bågskytt; hårda hinder som blockerar kropp/svärd/pil, men genomsläppliga för 360-graders gul halo; orb, HUD, liv/poäng, väl synlig ~0.4 s svärdsförvarning, minimal störande flicker, 8 rymliga banor/4 världar; Level3 ska vara lättmanövrerad och kraftfull. Ingen tyst grafisk/designmässig kompromiss.

## 2. Är spelet tekniskt möjligt?

**Hittills NEJ till ett bevisat GO; men också NEJ till ett generellt omöjlighetsbevis.** R3 visade tre same-Y P1-aktörer med 20Hz vardera, 30/30Hz halo-vs-hinder eller sammansmält gul PF, bara statiskt 2–4 cykler kvar på värsta linje, 112/128 RIOT bytes innan stack, pil, orb, AI och riktig HUD. Dessa resultat avfärdar R3 som direkt helspelssystem, **inte** all original-TIA-programmering.

**PF-researchen:** 13 riktiga ursprungs-R3 halo/scenery X-masker i 88 två-radsgrupper; enkel Hugg one-write/2-lines klarar inte 6–12 multiwrite-bursts per X. PF-REP1B:s hypotetiska femcykelscheduler missar 56/60 av 416 blandade rader (X80/X84), men tvåcykels känslighet gör detta till en modell-negativ, ej universellt hardwareproof. PF-REP1C:s naiva Venetian tappar 34/184 halo och 48/96 hinder-cellelement; ingen statisk enkel Ball/Missile ger separat andra fritt formbar färgmask. **Vid exakt överlappad PF-cell kan ingen pixel vara samtidigt gul och blå**: om båda geometrier måste täcka samma pixel behöver en explicit *visuell prioritet* (gold-forward/stone-forward/annan godkänd bildlösning), skild från oförändrad FYSISK soliditet och halo-skada. Slutligt estetiskt val kräver användarsamråd om det verkligen blir nödvändigt.

### Det viktigaste NYA historiska alternativet: 3-line kernel

Will Nicholes originalhardware-kompatibla [Duck Attack! tekniska specifikation](https://willnicholes.com/2010/08/04/technical-specs/) redovisar en **3-raders kernel** (228 CPU-cykler totalt över tre fysiska linjer i stället för 76 på en), tre former på samma fysiska rad/frame utan obligatorisk helframeflimmer **genom att bland annat omforma/repositionera BL**. [AtariAge-utvecklaren](https://forums.atariage.com/topic/149552-duck-attack-new-atari-2600-homebrew-ntsc-pal/) förklarar att en "tank" skapas med TIA Ball, samt pilar; 32K ROM men endast vanlig intern RIOT 128B enligt originalskaparen. **Det är inte en tredje oberoende P1 med godtyckliga gröna/röda 8-bit-mönster, och BL är färgkopplad till PF.** [Upphovsrättsnot](https://willnicholes.com/copyright-information/) anger att källkod inte får kopieras/redistribueras utan tillstånd. Studera endast offentligt dokumenterad teknik, implementera egen kod om godkänd.

**Ny falsifierbar hypotes:** nivå 1 har 12 fysiska rader för 12 originalrader, nivå 2 har 24=2×12 och nivå 3 36=3×12. **En level-känslig 1-/2-/3-raders arbetsfördelning** kan tänkas utnyttja den redan fasta P0-radrepetitionen för att flytta *förberedelse* till lediga faser och ge P1/PF tid på kritiska rader. MEN tre rader skapar inte fler än 3×76 tillgängliga CPU-cykler eller nya TIA-färgplan, och alla **fysiska** deadlines måste mötas; andra aktörers vapen- och silhuettrad-upplösning får inte förstöras. Det är alltså en **konkurrerande arkitekturhypotes**, inte ny godkänd renderer eller ändrad 8×12-konst.

Övriga primärkällor: [1979 Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) med 76/scanline, fysiska TIA-färgägare och prioritet; [Stella Debugger](https://stella-emu.github.io/docs/debugger.html) med `_fCycles`, `_sCycles`, `_fWsyncCycles`, conditional breaks; [Hugg 2025 versatile](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html) och [three stream](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html), som inte är tre same-Y fria fiender; [IEEE Spectrum Video Chess Venetian](https://www.atariage.com/2600/archives/design_case.html?SystemID=2600) som historiskt pixel-interleave för schackbräden.

### Här finns en konkret integrationsfälla

**Naiv direkt kombination är omöjlig:** R3:s 23 RAM-state +89B P1Buf = **112B**; nya COL1 använder **28B** i sitt eget isolerade schema. 112+28=**140B > 128B** och STACK, fiende-AI, HUD, pil/orb saknas. Man får INTE lägga dem bredvid varandra i RAM. De kan överlappa funktionella variabler eller ersätta P1Buf, men det kräver **ny gemensam live-range layout** med exakta tidsfaser, inte "kopiera fungerande rutin till R3". Likaså har R3 diagnostic ~2102 bytes emitterat ROM och COL1 ~1067; naiv 3169 av4096 lämnar lite för resten, men är ingen fast slutlig kodgräns. Även standard F8/F6 bankning skulle kräva dokumenterat separat beslut innan implementation; bankad ROM ger inte fler rastercykler.

## 3. Samtliga 30 trick — uppdaterad rangordning för just THE SKRAUN

Samtliga index avser [RESEARCH v1:s kompletta 30-radsmatris](https://drive.google.com/file/d/1p7a52GmmjFnCKRfGwHRQrsO-ftSgB03A/view) och tidigare [Skraun all-30 renderer-audit](R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md) / [visuell audit](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md).

| Prioritet | Trick nummer | Konkreta villkor / varför |
|---|---|---|
| **HÖG / först source-only** | **#2** mid-scanline GRP, **#7** asym PF, **#8** two-line och NY 3-line hypotes, **#12** rasterfärger, **#14** flera kernels, **#21** RIOT timer, **#24** förberäknade streams | De enda plausibla tids-/registerbesparingarna för same-Y, halo+hinder, world/UI-kernel utan designstöld. Exakt registerliveness och fysiska skriverdeadlines krävs. |
| **HÖG som villkorad byggsten** | **#1** sprite multiplex, **#9** VDEL, **#10** HMOVE, **#16** REFP0, **#17** missile/ball | #16 har P0-sprite-PASS. Övriga kräver olika aktör-X, färgägarskap, pil/orb-reservation, HMOVE-bars/regressionskontroll. |
| **RESERV med stor synlig kostnad** | **#3** Venetian, **#4** frame-flicker, **#6** NUSIZ midframe, **#15** NUSIZ kopior, **#18** SCORE, **#19** PF-prioritet | 20Hz hela fiender eller 1/3 rad-detalj kan förstöra spelvarning. SCORE/PRIO skapar inte två fritt valda färgmasker. NUSIZ-kopior ger inte tre oberoende X/bitmappar. Ingen användargodkänd sådan kompromiss. |
| **SEKUNDÄRT efter fungerande renderer** | **#5** dynamisk PF-sprite, **#13** 48px HUD, **#20** TIA collision latches, **#22** RAM/stack-overlay, **#25** stack-push-TIA, **#26** scrolltrick | #5 redan delvis testad men färgkonflikt olöst. #13 kan ge riktiga score/lives i egen zon. #20 får inte ersätta logisk soliditet. #22 bara med liveness och mätt stack. #25 hög risk. #26 lågt värde i fasta arenor. |
| **LÅG / separat plattformsbeslut** | **#11** late HMOVE, **#23** odokumenterade opcodes, **#27** SCABS/FE, **#28** extra cartridge-RAM, **#29** DPC, **#30** DPC+/CDF/ARM | Klipper inte undan TIA registerägare eller 76 cykler. Om RAM/ROM stoppar en annars synlig fungerande kernel kan standardmapper/extra RAM analyseras, aldrig tyst användas. |

**NY tekniknot #31** från RESEARCH II: förladdade `X=gold`, `Y=solid` och `STX/STY COLUPF` 3-cyklers stores i stället för `LDA #color; STA` 5 cykler. Kritisk invändning: R3 använder X som rastrex- och Y som PF-maskindex. Det behövs bevis att färger kan hållas live utan att samma register samtidigt behövs till annan adressberäkning. **NY jämförelse #32** här: 1/2/3-raders nivåanpassade kernels, härledd från #8+#14 och Duck Attack!, inte visad fungerande i Skraun. #31/#32 kompletterar de historiska 30; de ersätter inte några gamla poster.

## 4. Fryst fullscens-orakel som alla nya kernel-förslag ska klara

Använd **samma** scenkatalog och bokför *vilka* krav varje separat prov ännu inte testar. Inget enda fall får utropas som fullspel-GO.

| Scenario | Omutligt krav | Negativ kontroll / risk |
|---|---|---|
| S0 | U1-LEG1 A/B exakt mask + rätt facings vid 8x12,16x24,32x36, konstant responsiv joystick | Tidigare ART1 extra topp-rad och P0-HMOVE shifting |
| S1 | Tre självständiga aktörer på **samma Y** med X32/101/147, två röda riddare och grön archer | R3 20Hz var och 12-frame frånvaro |
| S2 | Same-Y aktörer med annan X-sorteringsordning, relativt nära men utan exakt pixelöverlapp | För sena RESP/GRP/COLUP1 writes, ett av objekten saknas |
| S3 | P0 Level3 och en riddare delvis överlappar på skärmen | Original R3 ~94% ocklusion trots "aktiv" fienderam; kräver definierad bildprioritet och läsbart angrepp |
| S4 | Gold halo X80/X84, R3 original row 98 med 3–4 COLUPF-gränser, samtidigt solida hinder i annan färg | PF-REP1B femcykelnegativ, två geometrikällor en PF-cell |
| S5 | Halo X56/X104 nära kanter, tvåfärgs PF och korrekt spelarcenter | Höger PF2, clips/ghost columns och skriverdeadlines |
| S6 | Samtidig pil, orb, HUD poäng+liv, vald P0/P1/PF färg och 3 fiender | Missile/Ball/PF ägare dubbelbokad eller RAM/stack-brist |
| S7 | 0,4s = ungefär24 NTSC bildrutors riddarförvarning, aktiva hugg, pilar blockerade av hinder, halo genom hinder | Warnings/danger bör vara läsbara i 12/24 frame-sekvenser, inte bara en stillbild |
| S8 | Ett tiotal representativa sparade X/Y/storleks-/färg-/gräns tillstånd över fyra världskontraster | Färgerna i natten gör gray/grön/guld oläsliga |
| S9 | L3 fria stråk + säker orb-uppgradering i en syntetisk arena; senare alla åtta separat | K0 source-flow räcker inte till AI, projektiler och verklig spelkänsla |

**Atari 2600-data:** totalt **76 CPU cycles PER fysisk scanline** (inklusive WSYNC/instruktionsfetch), original PAL kräver separat framtida verifiering. Om 3-raderskernel används är 228 endast 3×76 på tre olika deadlines, inte 228 cykler tillgängliga före första radens vänster-PF-write. Alla flera-colorclock cells vid exakt same-pixel konflikt kräver ett explicit visuellt beslut innan slutskärm.

## 5. Den REVIDERADE tiostegsplanen — Plan A/B/C för varje grind

Statusorden har strikt betydelse:
- **A** = primär lämplig teknisk väg;
- **B** = rimligt planerat alternativ, måste prövas mot samma krav;
- **C** = avgränsat stopp/fallback; **aldrig** dold reducering av fiender/halo/P0/level-storlekar.
Alla återkommande implementeringssteg är en **framtida plan**, inte redan auktoriserad Work-order. RESEARCH levererar rådgivande source-only; ROM DEVELOPMENT skapar/testar verklig ROM efter separat MAIN-order; VERIFICATION granskar bara frysta leveranser.

### N1 — Kvalificera frysta COL1-resultat och uppdatera relevant gate
**Ägare:** MAIN III. **Nu tillåtet som mottagningsgranskning.**
**A:** Rehämta original 19-scenars ZIP, kontrollera 138/138 CRC, SHA/ROM och exakt workflows/commit; klassificera testernas genuina Stella-visuella bboxes, memory-injected SELECT, 262-linje och otestade fysiska konsolknappar. Korsa med realtids-commit, inga gammal `pid`-fel återupplivade.
**B:** Om arkivhämtning blockeras, använd publicerad GitHub Actions rå-logg, exakt branch source och hashreferenser, redovisa att självständig ZIP-hash inte är omgjord.
**C/STOP:** Om ROM-hash, screenshot eller testcase inte går att reproducera, begär begränsad harnessreparation i samma PR, ingen ny arkitektur.
**PASS/leverans:** Fryst specifik #24 evidensmottagning (source, ROM, test, kod-diff) med vad som fortfarande INTE är bevisat.

### N2 — Stäng eller begränsa COL1:s 6507-/stackgrind utan perfektionism
**Ägare:** ROM DEVELOPMENT inom existerande #24, MAIN accepterar, VERIFICATION senare oberoende.
**A:** Oberoende käll-/DASM-listingrekonstruktion av **konservativa** faktiska worst-case instruction path och branches/pagecross för PositionP0, CandidateValid×upp till4, VBLANK timer, synliga WSYNC/GRP0, JSR/RTS stack; korrelera med Stella frame/pixel och faktiska gameplay scenfall. Originalorder uttrycker "**measure OR calculate with clear labeling**".
**B:** Mät med Stellas verkliga debugger breakpoints/pseudoregister `_fCycles`, `_sCycles`, `_fWsyncCycles`, `_scanEnd`; använd trace/GUI om möjligt. `saveSes` exporterar **prompt session**, är inte en automatisk riktig instruction profiler. Om exporter är 0B, byt bevismetod, inte mål.
**C/STOP:** Osäker statisk övre gräns eller verklig frame överkörning => fail-closed riktad fix. Om konservativ gräns håller men maskinläsbar trace saknas, acceptera bara ett tydligt **calculated-bound developer PASS** och lämna mätning öppet för verifierare, utan att låsa alla orelaterade forskningsspår.
**PASS:** Underbyggd 262-raders och tillräcklig cykel-/stackmarginal för denna isolerade 4K P0-ROM. INTE full renderer eller #1 P01 baseline.

### N3 — Fastställ gemensamt scen-, ägar- och gameplaykontrakt
**Ägare:** MAIN III + rådgivande RESEARCH; source/design, ingen ny ROM.
**A:** Frys orakelscen S0–S9 och tabell med P0,P1,M0,M1,BL,PF,BK, audio/HUD, per-frame färg/bitmap/position och physics ownership; samla 12/24-frame krav på riddarvarning och pilar. Separera faktiska kompatibilitetskrav från estetiska val som användaren måste avgöra.
**B:** Om en enda syntetisk scen är överkrävande som universell input, kör minimal men **adversarial scenmatris** med varierade X/Y och zon-gränser; behåll samma alla fastställda objekt.
**C/STOP:** Om visuell guld/solid pixelprioretet eller tillåten handling vid verkligt pixelöverlapp kräver ny estetik: rapportera alternativ och be användaren, inte dölj kompromissen.
**PASS:** För alla senare prov en versionerad testlista, visuell referens/kontrakt och per-objekt write-ägare med orsak till varje test.

### N4 — SOURCE-ONLY färg/PF-halo/fysiska deadline-rapporten
**Ägare:** RESEARCH, eventuellt MAIN:s oberoende source-review. Inga nya ROMs.
**A:** Exakta R3 X80/X84 row98 mask + S4/S5; guld vs solid i samma frame, PF0/1/2 vänster/höger legal writes, `COLUPF` 3/5 cykler och `X/Y` live intervals; alla pagecross/branch. Utvärdera färgprioriteter som **hypotetiska**.
**B:** Jämför överlappad multi-line/sparse PF och specialzon/colour-owner metoder. Hugg 2025 kan vara inspiration men den enkla one-register/2-line varianten är redan source-exakt FAIL.
**C/STOP:** Första logiskt oförenliga fysiska deadline, färgresurs eller dubbelfärgad pixel -> exakt reproducerbart motexempel och sluta med just den kandidaten; återstående koncept får nytt separat source-only prov.
**PASS:** Minst en komplett programmerbar eventsekvens genom source-register/colour deadlines, utan att låna P0/P1 eller förstöra projektil/orb.

### N5 — SOURCE-ONLY 3 same-Y fienders synlighet och level-aware kernel-jämförelse
**Ägare:** RESEARCH, inga ROMs innan ny MAIN-order.
**A:** Pröva #1/#2/#8/#9/#10/#14/#24: P1-retrigger/GRP1/NUSIZ/HMOVE för tre distinkta vapenbärande fiender X-fritt inom en frame, räkna varje separat bitmap+färg TIA-slot och aktörsidentitet över 12 och 24 frames.
**B:** Pröva fiendespecifik Venetian / level-aware 1-2-3-line kernel med Duck Attack som **mekanismexempel**; visa om 12-line riddarpose och 0,4s varning behåller tillräcklig detalj. OBS Duck Attack Ball är inte gratis tredje P1 och PF/Ball färg delas.
**C/STOP:** Om bara R3 20Hz helframeblinks, 1/3 vertikala bitar, konstgjord Y-separation eller bundna X-avstånd fungerar, rapportera **visuell/teknisk blocker**, föreslå inte tyst ändrade fiender.
**PASS:** Kandidat med faktiskt möjlig P1-position/färg/bildsekvens och sammanhängande telegraph; källa först, senare fysisk mikroROM krävs.

### N6 — Välj BARA en eller två fysikaliskt plausibla helscene-kontrakt
**Ägare:** MAIN III efter N3-N5, med RAM/ROM/CPU ledger.
**A:** Beräkna per 6507-rad: fullt `PF0/1/2 COLUPF GRP0/1 COLUP0/1 RESP/HMOVE ENAMx ENABL` med deadline, plus 128B RIOT byte-live-områden/stack, state machine timermax VBLANK/overscan och 4K ROM active/holes. Prioritera specialiserade zonkernels med nivåanpassat radantal om källprov ger det stöd.
**B:** Tre-stream registertabeller eller alternativa statiska ägare, men **byt ut** dyr befintlig 89B P1Buf — lägg aldrig dlist64B ovanpå R3 112B RAM. Standard bankning undersöks först om verkliga ROM-behov indikerar det.
**C/STOP:** Om ingen fullscenmodell inklusive alla objekt har tillräckliga resurser/skrivfönster, neka ny ROM och skriv ett rankat motexempel; endast verkligt användarval kan ändra gameplay/visuell ambition eller hårdvarumål.
**PASS:** Godkänd *enkel mikro-provkandidat* med allokering och negativa kontroller, **inte** fullspelsrenderer GO.

### N7 — Separata minimala autentiska DASM/Stella mikro-ROM-prov
**Ägare:** ROM DEVELOPMENT **enbart efter separat dokumenterad MAIN-arbetsorder för varje mikroprov**.
**A:** En P0+PF färg/samtidighetsmikroROM för farlig originalrad X80/X84 98, inklusive rätt 1/2/3level P0 vid relevant Y; 262 NTSC, två tydliga färger **i samma 60Hz frame**, pixel-deadline, ROM SHA och ramledger.
**B:** Om källa visar annan bättre metod, bevisa den under samma krav inklusive 2 färger och negativ en-färg/30Hz regression. Vid positiv P1 source prov: separat mikroROM för same-Y tre distinkta P1-fiendeposer med svarande input/X-swap, 12/24-rams synlighetslogg.
**C/STOP:** Missad deadline, återgång till 20Hz eller fel färg => fail; ingen fortsättning till full renderer av den metoden. Inte tillåtet "visuellt ungefär" eller försvunnen orb/pil.
**PASS:** Bevarade två kompletta isolerade fysiska byggresultat, eller uttalat STOP för ett misslyckat spår. **INTE** integration.

### N8 — En kombinerad värstascen-renderer utan full AI
**Ägare:** ROM DEVELOPMENT efter separat MAIN-auktorisation, ingen R4/B3c utan sådan.
**A:** S0–S8 på faktisk 6507/TIA i SAMMA frame: P0 U1-LEG1 L3, två riktiga knights + grön archer samma Y, cyan/blå solids, guldhalo, en pil och orb **som synliga eller tydligt reserverade objekt**, HUD-band där poäng+liv får plats; räkna detaljförluster och pixel-prioritet. 262 linjer, verkliga worst frame, RAM/stack/ROM, source+BIN SHA, 12/24 frame sekvenser.
**B:** Zonväxling/specialiserad 1/2/3-line kernel vid olika P0-levels, men samma fulla krav i varje relevant överlappsscen; ingen falsk permanent Y-separation.
**C/STOP:** Om det bästa försöket återfallit till 30/30 guld/hinder eller 20Hz same-Y, ingen "full renderer PASS". Tydligt redovisa efterfrågade användarbeslut endast om flera färdiga alternativ verkligen finns.
**PASS:** Fullfärgs- och aktörsbärande statisk/styrd scen vars värsta fysiska raster/budget håller, INTE komplett spel-AI eller åtta kartor.

### N9 — Första faktiskt spelbara vertikala skivan
**Ägare:** ROM DEVELOPMENT under en separat fler-delad, tydligt begränsad integrationsorder med MAIN beslutade delgrindar; GRAPHICS ändrar inte U1-LEG1 utan nytt särskilt scope.
**A:** En **enda syntetisk öppen arena** med riktig 8-riktningsjoystick, K0 solid-body/slide, nivå 1–3 orb, två angripande riddare med låst ~0.4s telegraph, grön bågskytt flyr och skjuter max en icke-homing pil, ~0.5s ringattack genom solids, fastlagd invulnerability, poäng och liv, hörbara korta effekter, vinst/bana slut. Inga ändrade spelregler, inga "fake gameplay" tester.
**B:** Dela denna integrationsorder i oberoende del-leveranser: först real FI/TIA indata+attack och collision med resursmätning, därefter AI/projektil, därefter orb/score/audio/HUD; återställ slutändan alla aktörer varje frame innan PASS.
**C/STOP:** Vid cycle/RAM/regressionsbrott, återgå till **den första minsta uppmätta delmodulen** med reproducerbart FAIL. Ingen automatisk specialcart eller reducering av fienderna för att avsluta.
**PASS:** Spelbar och speltestbar en-arena ROM som visar att grunderna faktiskt fungerar tillsammans med läsbar strid och respons.

### N10 — Oberoende Verification, speltest och beslut om åtta fulla banor
**Ägare:** Verifierande separat chatt granskar FRYST N9; MAIN bestämmer fortsättning, GRAPHICS separat estetik.
**A:** Oberoende reproducerbart build/hashes, actual Stella NTSC raster/CPU/RAM/stack och synliga 12/24-frame attacker, mänsklig kontroll/svårighet/Level3 framkomlighet, jämförelse med godkänd visuell canon. Här kan en begränsad, sen emulatorkompatibilitets- och originalkonsoltestplan läggas om tillgång finns.
**B:** Om programmet fungerar tekniskt men är visuellt svårläst, logga separat för estetik/fiendetelegraph på #15, inte ändra spel och stänga grindar av bekvämlighet.
**C/STOP:** Om full mekanik fortfarande saknas, markera NOT DONE och gå tillbaka till N7–N9, utan påhittad åttabansacceptans.
**PASS:** MAIN:s separat dokumenterade GO/NO-GO för **nästa** fas: integrera åtta kanoniska öppna miljöer, fyra världars färg-/kontrastdesign, faktisk bana 1→8→1-loop, reinforcement waves, poängljud och senare PAL/extern hårdvarutestning. **Färdigt åttabanorspel ingår INTE i N10.**

## 6. Riskregister — kontrollera innan motsvarande steg

| Risk / ägare | Motmedel (A/B/C styr inom plan) |
|---|---|
| **R01 6507 rasterdeadline** (N4–N8) | Per-TIA-write completion time och beamcell plus branch/page crossing, inte endast 76-genomsnitt |
| **R02 falskt extra cycles via 3-line** (N5/N6) | 3×76 fysiska deadlines och full U1-source-match, inte "228 innan vänster PF0" |
| **R03 same-Y 3 enemies** (N5–N9) | Permutera X och Y, mät duty/telegrafer, negativa R3 20Hz kontroll |
| **R04 halo + stone samma PF-cell** (N3/N4/N8) | Två separata färger när separata pixlar; dokumenterad synlig prioritet vid exakt cellöverlapp |
| **R05 P1/BL/M0 ägarkonflikt** (N3/N6/N8) | Objektbok 7 resurser med aktör och verkliga 12-frame fönster |
| **R06 RIOT >128 / stack** (N6/N8/N9) | Byte-live ranges, SPlow, ingen naiv R3+COL1 buffer addition |
| **R07 ROM 4K-kodtak** (N6/N9) | Faktisk compiler map per bank; standard F8/F6 endast efter dokumenterad MAIN-order; specialchip inte implicit |
| **R08 SELECT/testharness falsk kontroll** (N1/N2) | Märk memory-injection exakt; fysiskt keypress separat |
| **R09 Stella screenshots och trace false-green** (N1/N2/N7) | Pre/after state + negativa kontroller; svart saveSnap/0B saveSes räknas inte bevis |
| **R10 ART1 radfel återkomst** (N7/N8) | Pixel-exakt L3 A/B 36 rader/alla facings, separat gammal #19 förblir öppen |
| **R11 diagonal full-body hörntrick** (N9) | K0 1-step oracle, two-axis original projection, 90-frame free roam |
| **R12 orb growth near solids** (N9/N10) | Safe centre foreach pickup + full-sized body, ingen teleport |
| **R13 svärd/pil/halo fysik** (N9) | Solid blocker independent PF flicker; halo-through-walls, one non-homing arrow |
| **R14 fiende-AI & attack-timers** (N9) | VBLANK/overscan full-path timermax, 0.4s cue, refill rules, deterministic replay |
| **R15 oläsliga svärd/archer** (N5/N8/N10) | 12/24-frame raw frames i 4:3 + human motion, ingen stillbilds-PASS |
| **R16 fyra världar och nattkontrast** (N3/N10/fas2) | Först stresspaletter, inga åtta kanoniska kartor före visuellt och fysisk GO |
| **R17 originalkonsol kontra emulator** (N10/fas2) | Stella-version, NTSC/PAL/RetroN-matris, tydligt märk vilka riktiga cart/hårdvaruvärden ej provats |
| **R18 licens/primärkod** (alla) | Källor används som teknikreferens, ingen kopiering av Duck Attack-proprietär kod utan tillstånd |
| **R19 nya källor supersederar rapport** (alla) | Alltid läs senast HEAD/PR/run och authority order, dokumentera rebase; status-commits ≠ gameplay |
| **R20 falsk helspel-GO efter mikrokernel** (N7/N8) | Varje PASS får exakt lista över *borttagna* element; inget helspelspåstående förrän alla resurser prövats samtidigt |

## 7. Nästa konkreta åtgärd och projektledningsgräns

1. MAIN gör N1: autentisk 19-case ROM-kod-/harness-inspektion och originalpakets SHA/CRC samt avgränsad disposition.
2. ROM DEVELOPMENT får **inte ett dubbelt COL1-jobb**. Den ursprungliga #24-kedjan får, om det behövs, endast kompletteras med en exakt konservativ DASM-/Stella-cykelstackgranskning; arbetsordern tillåter redan mätning **eller** tydligt konservativ beräkning. MAIN får bedöma att developer-evidence är färdig för scope och separat Verification utan att vänta på en felaktig `saveSes`-förväntan.
3. MAIN/RESEARCH kan förbereda SOURCE-ONLY N3–N5 i en separat rådgivande plan, men inga nya ROM-byggningar har beordrats av denna rapport.
4. När det finns verkliga negativa/perfekt positiva bevis från N3–N6, utfärda en specifik arbetsprompt med branch, testdata, exakt STOP och vilket enda ROM-mikroprov som får köras. *Inte före*.
5. Fortsätt skilja mellan **kan fungera på TIA**, **kan ritas av denna kod**, **är faktiskt observerat i Stella**, **är spelbart i rörelse** och **har godkänts oberoende**. Ingen av de senare fyra följer automatiskt av den föregående.

**Samlad verklighetsbedömning:** Projektet kan tekniskt fortsätta men har en ännu olöst **hög risk** för samtidiga visuella resurser och fiendeläsbarhet. Den reviderade planen köper information innan dyra implementationsfaser, nyttjar kreativa historiska tekniker utan att lova magisk extra TIA och bevarar varenda användargodkänd spelregel och sprite.

## 8. MAIN III direkt genomförd N1-mottagningskontroll — 2026-11-17

Efter denna huvudrapport faktiskt **hämtade** MAIN III [original 19-case ZIP från Drive](https://drive.google.com/file/d/1B2oKbzx59GvGk2ip15fDrEwwHeVEy1Yb/view) som rå binär i en isolerad körmiljö och kontrollerade oberoende från ROM DEVELOPMENTs tidigare påståenden:
- ZIP-fil exakt **678660 byte**; direkt omräknad SHA256 **`e49d5187a977c9c580ff46c16d50089424c79cebe5500458a06ac221d96331f4`**.
- **138 ZIP-medlemmar**, samtliga CRC-pass (Python `zipfile.ZipFile.testzip() == None`); inga korrupta medlemmar.
- Arkivets `p01-col1.bin` är **4096 byte** och direkt omräknad SHA256 **`f36217f9ae96a1e927795ca639b9d6b6cca68ad3e8e4f296afadcdb52d6a6ad2`**, exakt samma som fryst original och GitHub Actions-körning.
- Exakt **19 genuina TIA-pane PNG** med den avsiktliga grå P0-masken; MAIN III läste varje PNG och beräknade oberoende gray-pixel bounding-box. Alla 19 matchar utvecklartestets rapporterade positioner. Fyra blockerade kontaktpar visar identisk box före/efter. Diagonaltest 1 visar X oförändrat/Y+1, diagonaltest 2 X−2/Y oförändrat. **90-frames rörelse ger x+120 skärmbildspixlar**, konstant 64×36-bbox. Grow safe 64×36, grow blocked 32×24; dessa demonstreras med dokumenterad debugger-injektion, INTE mänskligt F1-val.
- Detta är N1:s **fil-/pixelmottagning PASS**, ej independent Verification, fysisk hårdvarumätning eller full spelmotor, och statisk worst-case 6507-cykelbudget har ännu inte oberoende instruktionsbevisats.

**Disposition:** N1:s praktiska paketreplay är därmed **GENOMFÖRT** i MAIN III; nästa aktiva tekniska prioritet är N2:s konservativa DASM-/timinggranskning, medan SOURCE-ONLY N3–N5 kan förberedas parallellt. N2 är inte ett argument för att stoppa orelaterad research. Inga nya kodorder eller kvalitetsgrindar öppnas/stängs automatiskt.
