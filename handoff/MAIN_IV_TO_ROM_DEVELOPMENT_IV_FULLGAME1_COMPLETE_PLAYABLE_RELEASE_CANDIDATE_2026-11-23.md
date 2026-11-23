# THE SKRAUN – MAIN IV -> ROM DEVELOPMENT IV
## FULLGAME-1: FÄRDIGSTÄLL HELA SPELET – EN KOMPLETT SPELBAR ROM

**Datum:** 2026-11-23
**Issue:** https://github.com/Odourman/the-skraun/issues/50
**Auktorisation:** NY DIREKT UTTRYCKLIG ANVÄNDARORDER SOM GÄLLER HELA SPELET, INTE BARA NÄSTA DELSTEG
**Roll:** ROM DEVELOPMENT IV implementerar, testar och levererar. MAIN IV granskar slutleveransen och tar beslut om release.
**Mål:** Ett snabbt, roligt, komplett, originalkompatibelt Atari 2600-arkadspel med färdig, körbar ROM och allt nödvändigt spelinnehåll.

## 0. Detta ersätter tidigare STOP för NY implementation

Användarens aktuella order:

"Extremt nu. Gör en prompt åt Rom development och be den göra klart HELA spelet. Den får fria händer till att improvisera och fixa själv. Vi ska få en helt spelklar redo Rom. Där det uppstår problem får Rom development fria händer till att improvisera. Den ska använda sig av Google Drive och GitHub. Project sources och instructions. Den ska försöka få spelet så likt vad vi kommit fram till som möjligt. Den får ändra kreativa ideer om absolut nödvändigt för att spelet ska fungera."

Detta är **FULLGAME-1: FULLSTÄNDIG IMPLEMENTATIONSAUKTORISATION**. ROM DEVELOPMENT IV får driva projektet från den senaste riktiga spelbara checkpointen till ett helt färdigt, sammanhängande spel i **EN** utvecklingsinsats med många interna iterationer. Tidigare statusar "NO_NEW_IMPLEMENTATION" eller "ingen N8" gällde dåvarande avgränsade arbetsorder och hindrar inte denna senare uttryckliga användarauktorisation.

**Sluta återvända efter varje mikrotest för nytt tillstånd.** Om en kernel fallerar ska du mäta, förstå, omkonstruera och prova ett nytt fysiskt tillvägagångssätt. Fortsätt på egen hand inom denna fullspelsorder. Behåll fungerande ROM-checkpoints och rapportera betydande ändringar, men arbetsmomenten ska inte bli en lång rad väntande MAIN-gates. Slutlig fryst leverans och MAIN:s releasegranskning sker separat.

**Viktig gräns:** Fria händer betyder inte att du får deklarera felaktig kod som godkänd, ignorera den fysiska Atari 2600 eller fejka alla de fiender som saknas. Prioritera ett spel som verkligen fungerar. Avvik minimalt och öppet från användarens design endast när du har ett konkret tekniskt eller spelmässigt skäl.

## 1. Kontrollera KÄLLORNA på riktigt innan du ändrar kod

Du har i den separata chatten tillgång till anslutna verktyg. Kontrollera att GitHub, Google Drive, Project Sources-filerna, Project Instructions och relevanta projekt-/filverktyg faktiskt fungerar. Använd dem aktivt och automatiskt. Om en källa inte går att läsa, dokumentera bortfallet i stället för att gissa.

**Börja med Project Sources 00–04** som ingång, men minns att de är daterade snapshots från 2026-11-21 och inte överordnad liveauktoritet. Följ sedan den exakta källordningen:

1. Senaste uttryckliga användarbeslut, inklusive **denna fullspelsauktorisation**, och bindande spelcanon.
2. https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md
3. https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md
4. Fryst godkänd U1-LEG1 8x12 A/B-källa: https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json
5. K1-T och Ranger R1 exakta animationsmasker och utseendebeslut: https://github.com/Odourman/the-skraun/blob/4960d1661ad9764ce257a59053a981f46b09cff2/graphics/mainiv_tvisor_ranger_ref_20261122/P1_SOURCE_MASKS_TOP_BOTTOM_MIRRORED.json
6. Skogsdesign A_Glanta och tidigare grafikförslag – återanvänd där det passar, men bygg färdiga miljöer i stället för att fastna på source-only-kandidater.
7. Aktuella originalfiler, commits, verkliga DASM/Stella-testloggar, PR och Issues; äldre RESEARCH I/II, särskilt https://github.com/Odourman/the-skraun/issues/47 och https://github.com/Odourman/the-skraun/issues/30 ; historiska misslyckanden med N7, R3, PLAY1-X, H1/H2, M0/M1/H3.
8. Google Drive: migrationsmaterial, gammal research, grafik, testpaket och verkliga originalkällor. Bedöm proveniens och låt inte gamla Drive-statusar ersätta fryst källkod och senare uttryckliga användarbeslut.

**Exakt senaste spelbara baseline vid orderns utfärdande** (kontrollera live i start):
- https://github.com/Odourman/the-skraun/pull/49
- Branch experiment/gameplay5-arcade-combat-push-20261122
- HEAD **6d76ad267a465d7f3e2e0a707d0c1dd425d80cd2**
- ROM experiments/gameplay5_f8_ntsc.bin, exakt **8192 byte vanlig F8 NTSC**
- ROM SHA256 **b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca**
- GAMEPLAY-5:s 13/13 utvalda Stella-scener gav 262 rader; detta är **avgränsat DEVELOPER_OBSERVED**, inte full originalhårdvaruverifiering.
- M0-pilen **FAIL** för testad 286/287-raderskernel; M1 äldre test **FAIL** för 360-raderskernel.
- Två riddare och Ranger samtidigt fortfarande fysiskt **OBEVISAT**; H1/H2/H3 är avgränsade negativa försök, inte universell TIA-omöjlighet.
- X/Y-haloeffekten är fortfarande PARTIAL: Y-följer, inte riktig X-följning.
- Synlig HUD, åtta verkliga skogs-/bergs-/dröm-/nattbanor, full AI, spelbalans och komplett release saknas.
- main vid utfärdande **46d31504cccc5d17b521f7b9f01b7aded003de1a**, inte synkad med spelbar experimentgren. Låt den vara orörd tills separat MAIN-beslut.

Återbygg och SHA-jämför utgångs-ROM:en innan större ingrepp. Skapa en **NY isolerad fullspelsgren**, förslag experiment/fullgame1-complete-skraun-20261123, direkt från den frysta GAMEPLAY-5-commiten. Behåll tidigare branches, commits, ROM-hashar och negativa exempel som orörda kontrollpunkter. Skapa EN DRAFT PR mot tidigare spelutvecklingsgren och använd den som löpande utvecklingslogg; MAIN-merge först efter slutlig granskning.

## 2. MÅSTE BLI ETT FÄRDIGT SPEL – helheten

Detta är inte en forskningsrapport, teknologi-PoC, animerad presentation eller en ny tränings-ROM. Det är FULLSTÄNDIG spelproduktion inklusive designintegration och slutlig speltest. Du har uttryckligt tillstånd att själv lösa alla mellanliggande programmeringsuppgifter.

### Spelarfigur och rörelse
- Skraun är **UPPRÄTT ljusgrå med horn, ansikte, långa armar och getlika ben**, inte horisontell fyrfotad sprite. Bevara det frysta godkända U1-LEG1 8x12 A/B-originalet och rätt spegelriktning; återanvänd identisk källa på L1/L2/L3.
- Tre tydliga levels: ursprungliga planerade L1 8x12, L2 16x24, L3 32x36 källpixel-/kroppskoncept; verklig TIA-skärmbredd i colorclocks kan vara 2x dessa logiska bredder. Undvik att blanda fysiska TV-pixlar med ursprungliga bit-/hitbox-mått. Välj slutliga mått med spelbar kollisionssanning och dokumenterat motiv.
- Åtta joystickriktningar, samma upplevda hastighet på alla levels, diagonaler utan orimlig snabbhet, glid längs öppna hinderkanter, inga tillväxtfällor eller onödiga fastlåsningar på nivå 3.

### Halo och kamp
- Den **360-graders magiska halon** ska följa Skraun i både **X och Y**, växa i tjocklek/räckvidd med L1→L3, passa runt rätt spelposition och kunna verka genom hinder. Skraun får röra sig samtidigt. Aktiv ~0,5s och återhämtning L1 ~1s, L2 ~0,6s, L3 ~0,25s (balansera men bevara stark L3-känsla), hållen FIRE upprepar attack automatiskt.
- Synligt guld/markör runt Skraun och magisk effekt under attack måste förmedla det verkliga logiska träffområdet. Den preliminära guld-PF-modell B kan behållas, ersättas eller omkonstrueras om det krävs för effektiv beam-säker rendering. En kantigare ring, rasterstrimmor eller annan hållbar visuell teknik är okej om 360°-funktionen är tydlig. Halon förstör pilar även bakom hinder.
- Skraun skadas en level per verklig träff; vid level1 kostar det ett liv. Cirka 1 sekunds blinkande osårbarhet utan kontrollförlust, återstart i samma arena på level1 utan att återställa redan besegrade fiender/uttagen orb.

### Fiender, animationer och riktig AI
- **Två riddare samtidigt + en Ranger samtidigt** är det starkt önskade spelmålet. Två riddare ska kunna ha egna X/Y-pos, jaktlogik, svärdsvarning och skadefönster; Ranger eget X/Y, flykt, kort stillestånd vid skott och sikta på Skrauns position vid verklig release. De ska finnas logiskt samtidigt; målet är också att vara igenkännbara fysiskt samtidigt, även vid överlappande Y.
- Använd K1-T 8x16 ljusblå riddare med tydligt T-visir och 3 riktiga poser; svärd skadar ENDAST i aktivt hugg (~0,4s varning med låst riktning, kort strike, ~1s recovery), inte vid kroppskontakt, genom solid vägg, eller mellan attacker. Tydlig visuell förvarning är viktigare än häftig AI.
- Ranger R1, 8x16 mask med synlig båge, neutral/draw/release, världskamouflerad men läsbar (grön skog, lila dröm, god kontrast i berg/natt). Ranger söker skottlinje och undanmanövrerar hinder.
- Ranger ska avfyra **RIKTIGA SYNLIGA RÖRLIGA PILAR** som låser vektorn vid avfyrningen, inte homar. En pil max i luften; skottintervall skog ~3s, berg ~2,5s, dröm ~2s, natt ~1,5s. Pil stoppas av hinder, aktiv halo, spelare eller skärmkant. Synlig pil och faktisk träff ska överensstämma.
- Banans ursprungliga antal riddare: skog 2, berg 2, dröm 3, natt 4, med högst två samtidigt aktiva och reserver som kommer ~2s efter ledig plats. Ranger en per bana. Besegrad fiende ska stanna död tills banbesök återställs. Fienderna blockerar inte varandra och skadar inte varandra.

### Världar, banor, progression och liv
- **ÅTTA FÄRDIGA BANOR**, inte två återanvända testlayouter: skog 1–2, berg 3–4, dröm 5–6 med STATISKA drömspiraler, natt 7–8. Distinkta solida hinder och läsbara världsfärger, öppna arenor där Level3 kan röra sig utan att bli instängd. Använd gärna skog A_Glanta som första del av slutbanorna, men leverera färdig grafik även för resterande världar.
- BL-orb synlig från start; en per banbesök, L1→L2→L3; ligger kvar om redan L3; kan hämtas senare vid levelnedgång; säker spawn och upptagsplats och ingen gratis orb vid transition. Samma bana vid död, orb- och fiendedödstatus bibehålls. Banan klar endast när samtliga riddare + Ranger besegrats.
- 1→2→...→8→8→7→...→1→1→2 pendel-loop utan artificiellt ökande svårighet. Återbesök återställer nytt fiendebesök och ny orb; liv, level och poäng behålls över banor. Kort effekt och ~2s mellan banor med sista chans ta kvarvarande orb.
- Tre startliv, 100 poäng/riddare, 250/Ranger, extraliv vid varje 2000-gräns; korrekt hantering av 16-bitspoäng, overflow och livstak. GAME OVER visar slutpoäng, FIRE eller RESET startar nytt spel. Ingen fusk- eller debugknapp ska krävas för normalt progress.

### Presentationskrav och spelkänsla
- **Synlig HUD** med poäng och liv (och diskret arenaindikator), färgkontrast i alla världar, tydlig nivå- och stridsläsbarhet, ingen störande konstant flimmer. Spela hela spelvarv och balansera svår L1, medel L2 och mäktig L3; fiender ska gå att undvika och slå.
- Tydliga korta TIA-ljud för svärdsvarning/hugg, Ranger release, pil, orb, halo, skada, fiendedöd, extraliv och banbyten; kort jingle, ingen ständig stridsmusik. Ljudprioritet inom de två kanalerna.
- Bra kontroller, snabbt tempo, logisk träffdetektering, stabil uppdatering, ingen osynlig skada och inga kosmetiska animationer som fejkar gameplay. Lägg hellre lite mindre detaljgrafik än att offra ett fungerande spel.

## 3. TEKNISK FRIHET: Bygg om motorn – inte bara fyll på gamla kerneln

GAMEPLAY-5 visade att den befintliga fysiska raden kan vara alldeles för full. **Du är uttryckligen auktoriserad att ersätta/omarkitektera hela den synliga kerneln, layout, object-scheduler, RAM-placering, grafikdatatabeller och offscreen-spellogik** om det behövs. Använd tidigare fel som mätdata, inte som hinder för nya idéer.

- Prioritera en **gemensam verklig TIA-rasterarkitektur** för P0 Skraun, multipla fiender, Ranger-pil, BL orb, PF hinder/halo, bakgrund och HUD. Gör en fysisk rad- och registerägarskapsplan; tidigare kopieringsförsök H1/H2/H3 var bara testade varianter.
- Utforska realistiskt helt andra kernels: bandbaserade render-/positionsscheman, tidigare förberedda displaylist-/rasterdata, register-reuse på lediga rader, VDEL/GRP/flera frame-buffrade faser, begränsad adaptiv visningsväxling, tvålinjers rader, andra objektallokeringar, ny datakompression, prekomponerade PF-halomasker eller full omskrivning. Sök fungerande publika Atari 2600-homebrew-källor, men bedöm beamtiming på vårt riktiga fall och återanvänd kod endast med korrekt licens.
- Om tekniskt motiverat får du byta till en **vanlig original-Atari-2600-kompatibel cartridge-/banklösning** (t.ex. relevant F6/F4/Superchip eller annat dokumenterat originalkompatibelt format) för mer ROM-/cartridge-RAM, efter konkret budgetmätning. Dokumentera format, vad originalkonsolen behöver i cartridge-hårdvara och huruvida RetroN77/Stella 7 kan stödja ROM:en. Mer RAM/ROM ger aldrig automatiskt fler 76-cykels rasterinstruktioner eller extra TIA-playerobjekt. En proprietär modern specialhårdvarufunktion som krävs för själva renderingen får inte föras in tyst; prioritera original-TIA och normal originalkonsolkompatibilitet.
- Kör äkta DASM och Stella fortlöpande, Gopher2600/8bitworkshop/andra tillgängliga verktyg när det förbättrar resultatet. Använd GitHub Actions för automatiska test och artefakter. Var självgående med felsökning av fel och verktygsproblem.
- **262 NTSC-rader per komplett bildruta** och **76 CPU-cykler per fysisk rasterrad**, verkliga TIA-beamdeadlines; 128 RIOT RAM-byte inklusive stack och exakt objektägarskap. Om PAL-build tillkommer, gör det separat med rätt regionstiming och utan att förstöra NTSC. "Grön CI" och 13 snapshots bevisar inte att hela spelet fungerar.
- Bevara faktisk orörlig U1-LEG1-pixelkälla och användarens senaste K1-T/R1-art när möjligt; spelbarhet prioriteras men inga tysta pixelbyten. Färdiga banor och andra saknade konst-/ljudresurser får produceras inom detta hela-spel-uppdrag: detta är uttryckligen tillåten **nödvändig implementation**, inte en separat automatiskt startad GRAPHICS II-chatt.

## 4. Om tekniken sätter stopp: improvisera SÅ HÄR

**Du HAR uttryckligt mandat att göra nödvändiga kreativa och tekniska förändringar.** Du behöver inte återkomma och fråga MAIN om varje kompromiss. Men du får inte kalla en nödlösning identisk med tidigare canon om den inte är det.

Följ denna prioriteringsordning:

1. Fysisk Atari-kompatibilitet, verkligt fungerande input/attack/skada/banloop, stabil bild och inga kraschande register-/RAM-fel.
2. Behåll spelets **kärna** så långt det över huvud taget går: igenkännbar upprätt Skraun på tre levels, snabb åttariktad rörelse, 360° halo som blir mäktigare, hotfulla riddare med förvarnat svärd, bågskytt med synlig pil, åtta distinkta världsscener, poäng/liv/loop.
3. Föredra kompromisser i DETALJER: pixelfärg, palett, kartdekoration, exakt visuellt radmönster, liten sprite-/objektmask, attackens grafiska ytterkontur, några få animrutor eller audioönskemål.
4. Pröva på riktigt en mer omfattande motor, alternativt standardcartridge-RAM/ROM, och en mätbart acceptabel **visningsmässig** interlace/flicker-lösning, INNAN du ändrar stora spelmekaniska kärnkrav. Logisk samtidig AI är viktig även om TIA måste turordna visning under korta ögonblick. Läsbar 0,4s varning och verklig angriparposition ska bevaras.
5. Bara om tillräckliga fysiska försök visar att en kärnfunktion inte kan nås på vald originalkompatibel hårdvara får du välja den **minsta möjliga spelbara kreativa avvikelsen**, t.ex. ett justerat visuellt visningsschema eller smartare arena-/fiendeplacering. Om antal synliga fiender, attackens räckvidd, kroppens storlek eller annan avgörande mekanik måste ändras: markera det uttryckligen som **USER-DELEGATED NECESSARY DEVIATION**, med tekniskt underlag, exakt konsekvens och jämförelse mot bäst trogna alternativ. Detta är uttryckligen delegerat endast i den mån det verkligen är nödvändigt för färdigt spel.
6. Om det trots seriösa ombyggnader och rimliga fallbackspår inte går att få alla centrala krav att fungera: **leverera den bästa ärligt spelbara ROM:en** med en exakt avvikelse-/bristlista. ALDRIG påstå "hela spelet färdigt" om en faktisk huvudsaklig funktion saknas, om RAM korruptas, om fiender bara är sekventiella proxies eller om pilen är osynlig.

Skapa ett tydligt DESIGN_DEVIATIONS.md eller motsvarande med varje slutlig avvikelse, varför den var nödvändig, vilka alternativ som prövats och vilken upplevd påverkan den har. Användarens delegation är ett mandat att improvisera, **inte ett bevis för att användaren har sett och estetiskt slutgodkänt varje avvikelse**.

## 5. Riktig sluttestning – hela spelet, inte en serie demonstrationsbilder

Bygg automatiska/faktiska verkliga tester för:

- Från knapptryck till verkligt spel, rörelse vänster/höger/upp/ner/diagonal, L1/L2/L3, glid längs samtliga riktningar och öppna nivå-3-vägar utan fastlåsning.
- Minst en komplett verklig varvsekvens **1→2→3→4→5→6→7→8→8→7→6→5→4→3→2→1→1**, orbåterställningar och fiendekvoter; poäng/liv/level kvar över banbyten; korrekt död/restart.
- Två riddare och Ranger i samtidiga logiska spellägen och fysisk igenkännbarhet i sannolikt svåra X/Y-scener, deras varningar/AI/attacker och verklig rangerpil i flera följande råa Stella-frames (inte enbart pixelkomposit).
- Kontinuerlig registrering av rasterrader under längre spelpass med olika inputs, fiendedöd, halo, orb, nivå3, Rangerpil, GAME OVER, återstart, stage endpoints. Uppdaterad worst-case 76-cykel/TIA-registreringsledger och faktisk RAM/stack högvattenanalys. Fysiska originalhårdvaruprov om sådan hårdvara är tillgänglig; markera exakt vad som saknas.
- Korrekta källmask-/skärmpixelorakel för Skraun, K1-T och Ranger, world-palett, hållbar läsbarhet under flicker och guldhalo. Tydlig separation mellan faktiskt emulerade tester, source-only och manuellt subjektivt speltest.
- Synligt liv-/poäng-HUD, extraliv vid åtminstone flera 2000-gränser, bonus, invulnerability, respawn, alla banövergångar, att spelaren inte kan fastna på nivå3.
- Portable 1-sides PLAYTEST/CONTROLS för användaren och, om lämpligt, särskilda README/RELEASE_NOTES med ROM-format och emulator/flashcart-instruktioner.

**PASS-etiketter:** SOURCE_ONLY, DEVELOPER_OBSERVED, MAIN_REVIEWED och INDEPENDENT_VERIFICATION får aldrig blandas ihop. Ditt eget test är inte oberoende Verification. En *spelbar och komplett releasekandidat* kan lämnas till MAIN för slutlig kvalitetsgranskning; en offentlig slutrelease eller merge till main sker först efter MAIN:s uttryckliga releasebeslut.

## 6. SLUTLEVERANS – gör jobbet färdigt och STOPPA

Publicera på din NYA branch och EN DRAFT PR, utan att röra main:

1. **THE_SKRAUN_COMPLETE_NTSC.bin** eller tydlig motsvarande fil, rätt mapperstorlek och SHA-256, byggbar originalkonsolkompatibel körbar ROM, inte diagnos.
2. Komplett DASM assemblerkälla och alla datatabeller för rörelse, 8 banor, AI, svärd, pil, halo, musikljud, HUD, kollisionslogik och spelprogresstion; bygginstruktioner, exakta verktygsversioner, source- och ROM-SHA.
3. Autentiskt Stella/Gopher2600-testmaterial: faktisk kontinuerlig speltest, riktiga bilder/video eller frame- och registerloggar, bestämd PASS/PARTIAL/FAIL med exakta sceninputs, raster, CPU, stack, pixels. Negativa experiment följer med separat för reproduktion.
4. Enkel PLAYTEST.md med joystick/FIRE/RESET, installation i Stella/RetroN77 där testad, samt beskrivning av 8 banor och gameover.
5. En tydlig funktionstabell: funktion IMPLEMENTED_AND_TESTED / IMPLEMENTED_UNVERIFIED / COMPROMISED / MISSING; separat slutlig DESIGN_DEVIATIONS.md och KÄNDA_PROBLEM.md. Inga gömda brister.
6. En kort MAIN_IV_FINAL_DELIVERY.md: vad som fungerar, exakt bästa ROM/hash, vad som är tekniskt bevisat, kvarvarande release-risker, och REKOMMENDATION om slutlig MAIN-review/fristående releaseverifiering. Inga långa administrativa avhandlingar i stället för kod.

**En enda övergripande uppgift**. Ingen ny auktorisation krävs för interna omtag och mellanliggande delsteg, så länge de syftar till det här hela spelet. Ingen automatiskt startad separat GRAPHICS/RESEARCH/VERIFICATION-chat, ingen merge till main eller offentlig release utan separat MAIN-beslut. Om extra appar/kopplingar behövs verifieras åtkomst och används via sina verktyg, inte via påhittade resultat.

Slutstatus: FULLGAME1_DELIVERED / ROMDEV_IV_STOPPED / MAIN_IV_FINAL_REVIEW_REQUIRED.

**FULLGAME-1 ska börja när ROM DEVELOPMENT IV får denna order i den separata chatten.** En GitHub-issue eller handoff startar inte en chatt automatiskt.

---

## TILLÄGG 2026-11-23 – NYTT BESLUT: HÖJ ROM-TAKET TILL 16 KiB

**Ny direkt användarinstruktion:** överväg och använd ROM-utrymme **upp till 16 KiB** för att förbättra hela The Skraun. MAIN IV fastslår att **16 KiB är tillåtet och föredraget som huvudmål** inom den redan auktoriserade FULLGAME-1, Issue #50. Det är inte en ny mikrosprint eller omstart av GAMEPLAY-5. Den tidigare 8 KiB F8-ROM:en är endast fryst start/checkpoint.

**ROM DEVELOPMENT IV ska agera enligt följande:**

1. Utvärdera och vid fördel använda **vanlig original-Atari-kompatibel F6: fyra banker × 4096 byte = 16384 byte**. F6 väljs via hotspots $1FF6–$1FF9; säkerställ korrekta resetvektorer/startkod/banktrampoliner och kör bankväxling utanför kritisk rasterrad. Skapa ny isolerad FULLGAME-1 implementationsgren direkt från fryst GAMEPLAY-5 HEAD 6d76ad267a465d7f3e2e0a707d0c1dd425d80cd2, inte från main.
2. Om faktisk RAM-budget motiverar det är **F6SC** också tillåten **inom samma 16 KiB-tak**: dokumentera extra 128 byte cartridge-Superchip-RAM, dess separat adresserade läs-/skrivfönster och ROM-område samt kompatibilitet. Förväxla inte extra cartridge-RAM med de 128 RIOT RAM-byten (inklusive stack) på baskonsolen.
3. Använd extra ROM-byte för färdiga åtta banor, grafiktabeller, kompakt AI, Ranger-pil, mer genomarbetad rasterarkitektur, X/Y-halomasker, HUD, ljudeffekter, nivåer och speltestbar helhet. Välj fritt bankfördelning efter riktig CPU-/TIA-/RAM-budget; en möjlig idé är separata renderer-, AI-, värld-/grafik- och HUD/ljud/systembanker, men lås inte arkitekturen i förväg.
4. **16 KiB löser inte 76 cykler/rasterrad, beamdeadlines eller antalet TIA-grafikobjekt.** Mät fortfarande verklig Stella-timing, kompletta rasterrader, RAM/stack och faktisk samtidighet med två riddare och Ranger. Inga fejkpilar eller sekventiella proxy-fiender får betecknas som full implementering.
5. Testa den valda ROM-typen på faktisk Stella (F6 eller F6SC explicit identifierad) och om möjligt RetroN 77/Stella 7 samt originalkompatibel cartridge. RetroN 77-kompatibilitet på communitynivå är inte ett PASS för denna specifika spel-ROM.
6. **16 KiB är ny högsta ROM-gräns.** Större ROM eller annan specialmapper kräver nytt användarbeslut. En fullständigt fungerande 8 KiB-version är inte förbjuden, men 16 KiB får användas utan extra tillstånd. Dokumentera banklayout, mapper, SHA, originalkompatibilitet och eventuella alternativ.
7. **Viktig authority clarification:** GAMEPLAY-5 (Issue #48) är redan avslutat. Men senare FULLGAME-1 (Issue #50, 2026-11-23) är en **uttrycklig ny fullspelsorder** och upphäver standby-villkoret för just det nya uppdraget. ROM DEVELOPMENT IV ska inte svara med GAMEPLAY-5:s gamla STOP när den mottar FULLGAME-1. Läs hela Issue #50, denna fullständiga uppdaterade handoff och projektkällorna, och **genomför FULLGAME-1 hela vägen**.
8. MAIN-merge, offentlig release och independent Verification kräver fortfarande separat slutligt MAIN-beslut. Slutleverera en körbar komplett releasekandidat med verkligt DASM/Stella-testad funktionalitet och ärligt avvikelseregister. STOP först vid FULLGAME-1:s slutleverans.

**Källor:** Stella officiell mapperlista https://stella-emu.github.io/docs/ ; bankswitch-praktik https://forums.atariage.com/topic/83915-bank-switching-best-practices/ ; RetroN77-community https://forums.atariage.com/topic/280100-retron77-compatibility-list/page/10/ .
