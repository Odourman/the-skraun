# THE SKRAUN — R3-VFIX: SKRAUN ORIENTATION REGRESSION — SLUTRAPPORT TILL MAIN
**Datum:** 2026-11-16. **Roll:** ROM DEVELOPMENT; begränsad buggkorrigering och utvecklaregenkontroll, **ingen oberoende VERIFICATION**.

**Auktoritet:** [Bindande R3-VFIX-uppdrag](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_R3_VFIX_ORIENTATION_REGRESSION_2026-11-16.md), [MAIN:s tekniska radordningsaudit](https://github.com/Odourman/the-skraun/blob/main/docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md), [visuell riktning](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md).

**Oförändrad föregångare:** [R3 grenen](https://github.com/Odourman/the-skraun/tree/experiment/romdev-r3-decisive-scene-scheduler), fryst commit 863f67780836d0057c2947dfc87612e835da731b, [R3 draft PR #14](https://github.com/Odourman/the-skraun/pull/14). Gamla ROM, SHA, Stella-bilder och negativa teknikslutsatser ligger kvar.

**Isolerad korrigeringsgren:** [fix/romdev-r3-upright-20261116](https://github.com/Odourman/the-skraun/tree/fix/romdev-r3-upright-20261116), [VFIX draft PR #16](https://github.com/Odourman/the-skraun/pull/16) mot R3:s experimentgren, inte main; ingen merge.

## 1. EXAKT FEL OCH MINSTA MÖJLIGA KORRIGERING

De tre R3-ROM:erna anropar GRP0 från den 177-byte långa Troll3-tabellen via LDA Troll3,X i den synliga rutinen, medan X räknas ned från 176 till 1. Första synliga aktiva index är därför **101**, sista **66**. Det ursprungliga aktiva intervallet låg åt fel håll: lägsta adresserna 66–68 innehöll **huvud/öron $24**, högsta 99–101 **fötter $C2**. Visningen på verkliga Stella-bilder blev följaktligen fötter överst och huvudet nederst.

R3-VFIX **vänder exakt de 36 aktiva Troll3-bytesen [66..101]** i alla tre sources. Resultat på faktisk bild: översta tre raderna **$24 = 00100100** (huvud/öron), de nedersta tre **$C2 = 11000010** (bakben/fötter). De godkända 12 logiska referensraderna från MAIN:s spriteaudit upprepas 3 fysiska scanlines på nivå 3, 4× horisontell TIA P0 (8× i native 320px PNG).

**VIKTIGT INVARIANT:** faktisk jämförelse av alla 4096 ROM-bytes före/efter finner exakt **36 ändrade bytes per ROM**, och varenda differens ligger på samma 36 ursprungliga Troll3-adresser. ROM-vectors, code, sprites P1, deras separata RAM-koordinater, PF, halo, hinder, HUD, input, sprite scheduler, VSYNC/VBLANK, TIM64T och hitboxes/spelregler ändrades INTE. Inga rastercykler tillkom.

## 2. TRE FÄRDIGA NYA DASM NTSC-BINÄRER

| R3-kandidat | **Före VFIX SHA-256** | **Efter VFIX SHA-256** |
|---|---|---|
| overlap: tre fiender same-Y | f25c8622c115f85717b1fd51ff2a30cfb6fa293e95aceb228257c0655067775c | **2c29a696c3a7b5c05ba84a829f6ae64cbc58886778d929799d057048645f8f55** |
| partial: två overlap + archer separat | 411f7ce389e0853f071011e0ab2be34ad90c47f352ea524f1ad39e98891d501c | **89098ad4026cd4e770381d30c2469fe5faac3cbde2fd3d27d38f33a85ef98221** |
| stagger: tre skilda Y-band | 94ae477a944a042a6e605b6046b4e833b0cf3387bc62906e75491e47a649f226 | **53b00adf2325cfd84a6fac52cd504db6349b46922da5a259ac1b7ad2923c54e3** |

Tre äkta ROM:er 4096 bytes vardera, originalkompatibel Atari 2600 / 6507 / TIA. Källa: experiments/romdev_r3_overlap.asm, experiments/romdev_r3_partial.asm och experiments/romdev_r3_stagger.asm i VFIX-grenen. Exakt kodradordning och skillnader finns i draft PR #16. DASM .lst och .sym, SHA256SUMS och original-ROM-kopior finns i testpaketet.

## 3. NYTT OBLIGATORISKT STELLA-PIXELTEST: GAMMAL FAIL, NY PASS

**Riktig Stella Debugger 6.7.1**, inte en modellad bild. [GitHub Actions slutlig GREEN test #43925833442](https://github.com/Odourman/the-skraun/actions/runs/43925833442) körde:
- DASM och exakta 3×4KiB BIN + .lst och .sym.
- Stella Debugger, 19 autentiska saveSnap-captures per ROM, där 12 är direkt efterföljande 60Hz frames och de övriga inkluderar x80, x56, x104, nästa frame för färgfas och både vänster/höger riktningsbyte.
- Direkt debuggeravläsning med **262 scanlines i 19/19 tillstånd per variant**, totalt **57/57 262-linjers bildrutemätningar**.
- Den tidigare R3-testsviten tests/romdev_r3_frames.py: **PASS** för rörelse, identisk Skraun bounding box 64×36, fiendeduty, ring/PF2 och inga HMOVE-förskjutningar, samt tests/romdev_r3_static.py: **PASS** för oförändrade statiska rastercykler och PF-writer deadlines.
- Nytt tests/romdev_r3_vfix_orientation.py: **explicita 8-bit-radpixlar över samtliga 12 logiska rader, samtliga tre vertikala repetitionerna och alla åtta horisontella bitceller**, från exakta RGB-skärmpixlar; inte bara bbox/totalgråpixlar.

**NEGATIV KONTROLL GENOMFÖRD:** workflow hämtar de *frysta äkta original-R3*-bilderna och original-BIN från [original R3 direct Stella Actions #43919941150](https://github.com/Odourman/the-skraun/actions/runs/43919941150). Samma nya orientation-only CLI körs mot original och **måste få icke-noll exitkod med det faktiska felet: old HEAD-TOP 0xC2, expected 0x24**. Detta fel är arkiverat i VFIX_EXPECTED_ORIGINAL_FAIL.log. Körning med rättade ROM-bilder ger PASS 57/57. Det fördjupade före/efter-testet bekräftar att **varje av de 57 gamla bilderna FAILAR** head-first kontraktet och **varje av 57 nya PASSer**, inklusive x56/80/104 och riktningsbyte. Ingen gammal bild cherry-pickas bort.

Den faktiska horisontella P0-positionen och 64×36 pixelformen är oförändrade; inom en variant ligger samma y-center före/efter. De tre diagnostikernas olika 1–2 rader absoluta rasteroffsets fanns redan i frysta R3 och ändras inte av VFIX.

**Faktisk P1-occlusion kan ändra pixelräkningen trots samma läge:** i partial vid P0 x104, på blue scene frame, ändrades den redan starkt skymda röda andra riddaren från **8 till 6 synliga pixlar**, eftersom Skrauns nu korrekta radform täcker andra bitar. Vid x80 har riddaren fortsatt 136 pixlar. Riddarnas uppmätta 20/30/60Hz display-duty är oförändrad; deras läsbarhetsproblem blir inte löst av VFIX.

## 4. FIENDEMASKERNAS RADORDNING OCH STATUS

P1:s tillfälliga testgrafik är en separat 8-byte ART-array per fiende, lagd med DrawOneRow från **art-index Y=0 uppåt i P1Buf** och hämtad i stigande bufferrowordning när den synliga rasterlinjen fortskrider. Till skillnad från P0:s 177-byte Troll3-tabell finns därför **ingen motsvarande nedräknande art-tabellreversal i den aktuella P1-vägen**. VDEL1 kan fördröja en fysiskt synlig rad men vänder inte ordningen. Det är ett **kodflödesfynd, INTE godkänd fiendeorientering/konstnärlig grafik**. Verklig riddar-/bågskyttdesign är INTE gjord och inte godkänd.

**Obligatorisk artistisk status:**
- **Skraun:** orientation correction candidate; ljusgrå overhead bitmap med rätt head-before-feet i Stella, men ingen separat användaracceptans av exakt nivå3-silhuett/pose.
- **Enemy images:** temporary 8-byte test silhouettes; inga igenkännliga användargodkända svärdsriddare eller grön bågskytt med båge.
- **Obstacle columns:** synthetic diagnostics; INTE faktiskt banunderlag eller färdiga hinder.
- **HUD:** placeholder; INTE score/lives/HUD-grafik.
- **Forest/mountain/dream/night artwork:** NOT IMPLEMENTED. Inga världsbakgrunder eller 2-step A/B-animation är gjorda inom VFIX.

Jämförelsebilden visar enbart autentiska gamla och nya Stella 6.7.1-bilder plus 4× uppförstorad färgmask av **verkliga uppmätta** grå P0-pixlar. Ingen AI-genererad bild, ingen ny konstgrafik.

## 5. RESURSER OCH TEKNISKT NO-GO OFÖRÄNDRAT

- **R3:s godkända begränsade schedulingresultat kvarstår:** same-Y tre fiender 20Hz var; partial 30/30/60Hz; separata Y-band 60Hz var. Även andra riddarens P0-overdraw vid x104 kvarstår kraftig.
- **Halon/hinder:** 30Hz per färgplan i olika fulla frames, eller 60Hz samma PF-färg med sammansmälta hinder/ringkonturer. Nivå3 större halo och right PF2 oförändrade.
- **CPU:** statiskt beräknat worst physical B 72/76, 73/76, 74/76 cykler, bara 4/3/2 lediga före pil/orb och full HUD; TIA 76cykler/scanline. Ingen extra instruktionscykel i VFIX.
- **RAM:** 89-byte P1-buffer plus R3 state, huvudarkitektur underutvecklad för riktiga fiende-AI/attack/arrow/orb/score; ingen buffertändring.
- **Slutsats:** R3:s avgörande teknikbeslut **NO-GO FÖR FULLSTÄNDIG SPELMOTOR** består. Orienteringsfixen är ett isolerat skärmgrafiskt felrättande, inte ett renderer- eller gameplay-GO.

## 6. REPRODUCERA OCH ÖVERLÄMNA

1. Checka ut experimentgrenen fix/romdev-r3-upright-20261116.
2. Kör .github/workflows/romdev-r3-vfix.yml i GitHub Actions (eller följ dess DASM/Stella-kommandon med Stella 6.7.1, originalkompatibel 6502).
3. Workflown laddar frysta original-R3-evidensen, bygger tre VFIX-ROM, stegar emulatorn, sparar 57 nya äkta originalbilder, kontrollerar 57×262, och kör ny orientation-only-test mot ORIGINAL (förväntat FAIL) och FIX (PASS).
4. Se R3_VFIX_ORIGINAL_FAIL_FIXED_PASS_PIXEL_ORIENTATION.json och VFIX_EXPECTED_ORIGINAL_FAIL.log; verifiera SHA256SUMS mot ovan och byte-diff mot frysta R3-ROM.
5. Slutlig samlad ZIP med rättade tre ROM:er, source, list/sym, original före/efter Stella PNG, negativ och positiv regression, textloggar och denna rapport levereras separat från både R3 och main.

**Ingen R4, B3c, fiende-AI, ny art, fler rasterarkitekturtester, merge till main eller oberoende VERIFICATION har genomförts.**
