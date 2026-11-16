# THE SKRAUN — MAIN: VISUELL DESIGNAVSTÄMNING EFTER R3-VFIX
**Datum:** 2026-11-16  
**Status:** RÅDGIVANDE DESIGNFÖRSLAG / KÄLLBASERAD ANALYS. **Ingen konstnärlig slutacceptans, ny MAIN-implementation, R4, B3c, merge eller oberoende VERIFICATION auktoriseras genom detta dokument.**

## 1. Källor och auktoritet

**Bindande:**
1. Användarens originalteckning: [SKRAUN_ORIGINAL_HANDDRAWN_REFERENCE_2026-11-16.jpg](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view), privat i Drive.
2. [DESIGN_DECISIONS_01-60_2026-11-16.md](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), särskilt 1, 3, 17–19, 33–37, 46–47, 54, 56, 59.
3. [SKRAUN_VISUAL_DIRECTION_2026-11-16.md](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md): uttryckligen ovanifrån, ljusgrå kropp, två gångposer A/B, två speglade horisontella orienteringar, tre storlekar; första gröna prototypen och tidigare begreppsbilder är inte slutgodkända.

**Kända fungerande/negativa tekniska belägg, INTE grafisk designauktoritet:**
- [Gray Skraun A/B sprite experiment](https://github.com/Odourman/the-skraun/blob/experiment/gray-topdown-skraun/experiments/p01_skraun_gray_topdown.asm) och privata [faktiska Stella-montaget](https://drive.google.com/file/d/1NHpVZa4DZ9AOv7Ew05Qiq_BtD3FYYRnn/view).
- [R3 ursprungliga äkta Stella-montage](https://drive.google.com/file/d/1N-sHAYWLPf3v_RFsQV9d7qAki7_lcQiZ/view). Huvudfiguren är vertikalt inverterad, fienderna endast 8-byte diagnostiska bitmappar och hindren syntetiska.
- [R3-VFIX-rapport](https://github.com/Odourman/the-skraun/blob/fix/romdev-r3-upright-20261116/docs/ROMDEV_R3_VFIX_MAIN_HANDOFF_2026-11-16.md) / [PR #16](https://github.com/Odourman/the-skraun/pull/16): orientering rättad i 3 ROM genom 36 P0 bytes vardera; 57 gamla autentiska Stella-bilder FAIL och 57 korrigerade PASS top/bottom-pixeltestet. Det bevisar INTE slutligt godkänd konst.
- [R3:s NO-GO för testad renderer](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md): 20 Hz vardera för tre fiender vid samma Y, 30/30 Hz separat halo/hinder, endast 2–4 statiskt beräknade cykler kvar före pil/orb, 89-byte P1-buffer. Detta bevisar INTE att varje möjlig original-TIA-kernel är omöjlig.

## 2. MAIN:s visuella nulägesbedömning

- **Skraun:** Grå figur med huvud/öron och två ögon är klart bättre utgångspunkt än gröna testspriten. Skraun känns däremot ännu som ett litet fyrkantigt "monsteransikte" med ben, inte säkert som ett fyrfotat varelse *rakt uppifrån*. Den handritade originalskissen är anatomisk referens och får inte misstolkas som godkänd frontkamera. R3-VFIX rättar en inversion, inte figurens identitet.
- **Riddare:** Nuvarande `EnemyArt0/1` är blott korta åttabytesmarkörer. Röda pixlar betyder inte att man ser en hjälm, ett svärd eller en attackpose. **Ej godkänt.**
- **Bågskytt:** `EnemyArt2` är en grön åttabytesmarkör, inte en begriplig silhuett med båge eller pil. **Ej godkänt.**
- **Miljö:** Svart spelplan, cyan HUD-streck och blå testpelare är tester för registerkostnad/färgkonflikt. Det saknas faktiskt skog, berg, dröm och natt. **Ej godkänt.**
- **Gameplayläsbarhet:** R3:s 20-Hz-fiender är borta 2 av 3 frames vid same-Y. Ett enstaka vackert stillbildsfångst kan inte legitimera sådant flimmer. Halons 30-Hz-guldfas får inte förväxlas med en kontinuerligt synlig ring.
- **Teknisk gräns:** Samma PF-pixel kan inte samtidigt ha en självständig gul halo och blått hinder i nuvarande single-PF-plan. Att byta färg mellan bildrutor eller varannan scanline är en kompromiss, inte två distinkta samtidiga lager.

## 3. Föreslagen grafisk identitet – Skraun

**Oförändrade etablerade krav:** ljusgrått fyrbent troll, ovanifrån, små öron/horn, två ögon, uttryck av mun/ansikte där läsbarhet medger, två utsträckta främre lemmar + två bakben, två A/B-poser, horisontell spegelvändning, 8-riktningsrörelse och 3 nivåstorlekar.

**Förslag till nästa stillbildsbaserade designprov:**
1. Återanvänd det bevisade **8×12-ursprungsrutnätet** som referens för liten skala (inte ett fast krav för framtida P1/andra objekt). Behåll ankarpunkterna öron/ögon/kropp/fötter, men gör *främre lemmars ändlägen mer olika* mellan A och B och separera bakbenen tydligare från varandra.
2. Granska en **silhuett utan ansiktsdetaljer** bredvid komplett sprite: en tittare ska först se en fyrbent kropp med huvud överst och ben nederst; ögonen ska sedan ge karaktär.
3. Behåll samma logiska anatomi på nivå 1, 2 och 3. Nuvarande NUSIZ0-radskalning 8×12, 16×24, 32×36 är en fungerande teknisk kandidat men grovkornig; *denna exakta skalning är inte automatiskt artistiskt bindande*.
4. Jämför A/B i ursprunglig låg upplösning, i ungefärlig faktisk TV-visningsstorlek och i förstoring. En förstoring får inte ensam avgöra om figuren är läsbar.
5. Ställ in verklig NTSC/TIA-lik grå kulör, testa mot minst en mörkgrön och en blågrå spelplan samt ringens guld. Justera kontrast utan att göra Skraun grön igen.

**Viktigt:** Skraun är inte ett humanoidt riddarmotiv. Följ användarens egen skiss för hur lemmarna ska uppfattas. R3-VFIX:s 12 rader är **orienteringsbaslinje**, inte konstnärligt orubblig slutdesign.

## 4. Föreslagen grafisk identitet – fiender

### Riddare (typ 1, typ 2 visuellt samma klass)
- **Läsbarhet vid enbart svartvit silhuett** ska vara första provet; färg är sekundär.
- Föreslaget tydligt *hjälm-/huvudparti*, bredare skuldror/sköld på ena sidan och **ett utskjutande svärd** på andra. Testa minst två poser: neutral och höjt svärd/förvarning enligt beslut 22/43. En separat attackpose kan senare behövas men är **inte auktoriserad spelimplementation nu**.
- Testa kandidatformat med 8-bitars P1-radbredd och ungefär 8–12 logiska höjdrader som *konstprover*. R3:s exakt 8-radersplatshållare är ingen designnorm. Längre/annorlunda bitmappar kan påverka P1-buffert, vertikal slotkonflikt och cycles: ingen ROM-feasibility PASS i detta förslag.
- **Färgförslag, inte fastställt:** dämpad roströd eller varmt stålgrå med tydlig kontrast mot skog/mountain/dream/night. Projektbesluten kräver riddare och svärd, inte en viss officiell riddarkulör.

### Bågskytt (grön enligt fastställd design)
- En **bågform** ut från silhuettens ena sida med igenkännbar hand/arm samt annan kroppsfördelning än riddaren. Endast en grön färgprick eller slinga räcker inte.
- Bågen och pilen ska läsas skilt: bågskyttens figur bör ha en särskild bågkontur, och verkligt pilobjekt får en separat projekt-/renderingsprövning.
- En stående bågform på 8 logiska pixlars bredd kan bli för trång; studera om en utstickande båge eller sned asymmetri är läsbar utan att låna P0/PF permanent. Detta är **en risk**, inte bevisad lösning.
- Föreslagen grön är varm/tillräckligt ljus på mörk spelplan utan att förväxlas med träd/skogshinder.

### Gemensam fiendetestregel

Visa *varje figurs silhuett isolerad*, sedan 2 riddare+bågskytt i en statisk konstkomposition, och därefter i enkel enskild original-TIA-kapabel diagnostik endast efter särskilt MAIN-tillstånd. Att alla tre ser bra ut separat är INTE bevis att de kan visas samtidigt: R3:s 20/30/60Hz-och-P1-resultat förblir en separat arkitekturgräns.

## 5. Föreslagen världsgrafik – fyra världar, åtta banor

Färger och motiv nedan är **konstnärliga förslag**, inte låsta palettregister eller nya spelregler. Behåll 2 fasta banlayouter per värld och få solida hinder enligt beslut 3,33,54.

| Värld | Föreslagen grundton | Hindersilhuetter / läsbara kännetecken | Risk att testa |
|---|---|---|---|
| 1–2 Skog | mörkt, dämpat grönt / skogsgrått | 2–4 tydliga trädstammar/kronor, stubbar, blockiga stenar | Grön bågskytt måste tydligt skiljas från vegetation |
| 3–4 Berg | kallt blågrått / stenkol | kantiga stenblock, stenformationer och avsatser | Ljusgrå Skraun måste skiljas från ljusa stenar |
| 5–6 Dröm | mörk, dämpad violett/blå | symboliska rundade ruiner, ring-/portalmotiv, oregelbundna klippformer | Drömgrafik får inte konkurrera med verklig gul haloring |
| 7–8 Natt | mycket mörkt marinblått/svart | glesa murar/ruiner och ljusare hinderkanter | Tydlig kontrast för grå Skraun, bågskytt, pil och halo; ingen förväxling med svart tom skärm |

Världar bör också vara **igenkännbara i gråskala genom hinderform och layout**, inte enbart genom COLUBK/COLUPF. Lek med få, sammanhängande Atari-block i stället för en detaljtät bakgrundsbild som kostar fler PF-skrivningar per line. Estetisk minimalistisk spelplan är tillåten; den får inte vara den oavsiktligt tomma R3-diagnostiken.

**Hårt teknikförbehåll:** Att rita ovanstående som konstbilder på en dator garanterar inte att samma scen samtidigt kan visas av TIA tillsammans med aktiv rörlig guldhalo. En PF-cell har en begränsad färg-/prioritetsmodell. R3:s förlust av ring/hinder eller 30 Hz växling är fortfarande ett faktum tills en annan renderer bevisas. Hinder/halo-kollisioners gameplaydata behöver föras separat från TIA-PF-pixlar.

## 6. Tydlig och avskalad HUD

Beslut 56: poäng och liv först; inte permanent level-text på bekostnad av spelplan. Visuell skiss: smalt separat översta band, exempelvis `SCORE 000000     ♥♥♥` som **läslig designmockup, inte fastställt teckensnitt eller slutlig ROM**. Banindikator kan visas kort vid banövergång; tal och liv ska läsas mot alla fyra världars bakgrunder.

R2/R3 har visat separat enkel HUD-rasterregion, men **inte fungerande numerisk poäng- och livskod eller fri tid för samtliga fiender/halo**. Inget av detta blir PASS av en snygg statisk HUD-design.

## 7. Föreslagen granskningsmatris innan implementation auktoriseras

**A. Konstnärlig läsbarhet – kan bedömas utan spelmotor**
- Skraun A/B, vänster/höger, alla tre nivåer: huvudet är överst, fyra extremiteter kan urskiljas och A/B syns i faktisk TV-lik storlek.
- Riddare: hjälm/svärd/sköld eller motsvarande synlig svärdsidentitet även utan rödfärg.
- Bågskytt: tydlig båge, asymmetrisk och skiljbar från riddare även i gråskala.
- Skog, berg, dröm, natt: läsbara som fyra världar via hinderformer + färgförslag. Två layouter per värld, några få hinder.
- HUD: poäng/liv lätt att läsa; ring, pil och svärd synliga även mot nattfärger.
- Originalteckning är referens; tidigare genererad konceptkonst och R3-placeholderbilder är INTE godkänd canon.

**B. Hårdvarugräns – kräver senare separat ROM-uppdrag**
- Exakt P0/P1 form på verklig Stella och pixelordning; ingen introducerad invertering.
- Samtidigt 2 riddare, 1 bågskytt + pil + orb + guldhalo och solida hinder med självständig position.
- Hårdvarans verkliga 76-cykels- och 128-bytebegränsningar under worst same-Y, med mätning och förväntad flimmerduty.
- Fyra världars PF-data och halomaskeffekt i ROM-kapacitet utan att lova fri ny TIA-grafik genom bankswitching.
- Full nivå3-haloreach, korrekt och tydlig kollisionsvisualisering, eventuella höger-PF2-krav, NTSC och senare PAL.

**C. Beslutskriterium för MAIN**
1. **Första grinden:** välj ett visuellt måldokument / figursilhuetter på designnivå; inga av de tekniska "PASS"-resultaten innebär art approval.
2. **Andra grinden (eventuellt):** ge en separat minimal *konst-i-Stella* diagnostic auktorisation för 1 Skraun + 1 riddare + 1 bågskytt + ett hinder per tema, för ren läsbarhet med faktisk Atari-TIA, inte som löfte om samtidighet eller nytt R4.
3. **Tredje grinden:** endast efter konst och teknik jämförts ska MAIN ta ett uttryckligt val om full-game renderer, begränsat flimmer eller annan hårdvarustrategi.

## 8. Risker vi INTE ska gömma

- Att förbättra sprites visuellt löser **inte** 2–4 lediga cykler, 89-byte P1-buffer eller same-Y rotation.
- Att tillverka riktiga riddare/bågskyttar med fler rader/animation kan göra raster- och RAM-budgeten *sämre*, inte bättre, än de åttabytesdiagnoser som gav R3:s NO-GO.
- 20 Hz eller 30 Hz visar inte alls samma upplevelse som en statisk pixelbild; designacceptans kräver hela frame-sekvenser i Stella.
- Att gömma hinder bakom halon eller fienderna genom forced positioning skulle ändra spelets regler; får inte införas som osynlig "optimering".
- En större ROM med bankswitching ger mer lagringsutrymme men **inte** fler TIA-sprites, PF-plan eller CPU-cykler per scanline.
- Det kan bli nödvändigt för MAIN att välja en uttrycklig visuell/hårdvarumässig kompromiss om ingen ny original-TIA-arkitektur kan visa fastställda mekaniker utan oacceptabelt flimmer.

## 9. Slutsats och gränsdragning

**MAIN:s rekommendation:** Bevara den ursprungliga ljusgrå Skraun-grunden, men gör en separat visuell designavstämning innan fler rasterstudier. Låt ny grafik definieras av *igenkännbara lågupplösta silhuetter och fyra tematiska spelmiljöer*. Låt den faktiska Atari-kompatibiliteten bevisas i senare separat auktoriserade, minimala ROM-diagnotiker.

Detta dokument är **en rådgivande specifikationskandidat**. Det godkänner inga nya bitmappar, skärmbilder, spelmekaniker, fiendehandlingar, renderingsscheman eller cartridgeformat. **Ingen R4, B3c, AI, merge eller oberoende VERIFICATION är härmed auktoriserad.** R3-VFIX är avslutad. Issue #15 hålls öppen för grafisk kvalitet.
