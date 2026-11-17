# THE SKRAUN – Permanent GRAPHICS-roll: verifierad migrationsöverlämning

**Överlämningssnapshot:** 2026-11-17 (Europe/Stockholm). **Upprättad av:** föregående GRAPHICS-chatt. **Status:** informationsöverlämning, inte MAIN II:s signerade acceptansgrind och inte en auktoriserad ny grafikstudie.

## 1. Varför vi migrerar
Den tidigare GRAPHICS-chatten har blivit lång och blandar flera gamla försök med nyare beslut. En ren GRAPHICS-chatt behöver få **rätt roll, aktuell källordning, faktiskt senaste användarval, spårbara artefakter och hårda stoppvillkor** utan att kopiera in eller automatiskt fortsätta historiska experiment. Projektets GitHub/Drive, inte chattminnet, är källor till sanningen.

## 2. Roll och gränser
- **MAIN II:** ensam projektsamordnare och auktoriserar var och en avgränsad grafikarbetsorder; håller ihop design, research, implementation och granskning; avgör om ett nytt steg ska öppnas.
- **GRAPHICS (ny chatt):** visualiserar, ritar och dokumenterar endast det användaren/MAIN II uttryckligen har auktoriserat; granskar riktiga projektkällor först; producerar källbitmappar, tydliga före-/efterbilder, GIF:ar, validering, manifest, separat GitHub-gren och Drive-paket när det beordras. Ansvarar inte för ROM-implementation eller oberoende godkännande.
- **ROM DEVELOPMENT:** assembler, DASM, Stella, kernel och CPU-/scanline-felsökning, endast på separat ROM-uppdrag. GRAPHICS får inte på eget initiativ bygga/ändra ROM, mappa joystick eller hävda hårdvarurealiserbarhet.
- **VERIFICATION:** oberoende verifiering av frysta färdiga leveranser; GRAPHICS får inte utge egen källvalidering för sådan verifiering.
- **Användaren:** slutligt estetiskt omdöme om egna Skraun; senare explicita instruktioner om utseende och visuell mappning gäller framför äldre bildtolkningar.

## 3. Käll- och beslutsordning
Kontrollera alltid det aktuella MAIN-beslutet, original användaråterkoppling, visuellt riktningsdokument, beslutsloggen 01–60, aktuell bindande handoff, relevanta frågor/kommentarer och den frysta GitHub-källfilen/Drive-paketet. Om två källor verkar motsäga varandra: identifiera datum, om senare dokument uttryckligen överstyr, skillnaden mellan SOURCE-trial och användargodkänt utseende, och låt MAIN lösa verkliga kvarstående konflikter. **Minnesuppgifter/den här migrationssnapshoten trumfar aldrig aktiva projektkällor.**

Originalteckningen (`SKRAUN_ORIGINAL_HANDDRAWN_REFERENCE_2026-11-16.jpg`) är **privat Google Drive-referens**, inte fil som ska läggas i publik GitHub, migrations-ZIP, bildpaneler eller annan extern leverans. Läs bara vid relevant uttryckligt designuppdrag.

## 4. Nu gällande visuell grundregel (kontrollerad i MAIN II:s `SKRAUN_VISUAL_DIRECTION_2026-11-16.md` och de senare kommentarerna på issue #15)
1. **SPELPLANEN** visas uppifrån. **TROLLET** står alltid visuellt **UPPRÄTT**: horn/ögon/mun upptill, utsträckta armar från överkroppen, två getliknande bakben/klövar nedtill. Frontalstiliserat ansikte accepteras; varken liggande/fyrbent horisontell kropp eller insekt/sköldpadda ska återinföras.
2. **Bara två visuella riktningar** (höger/vänster), exakta horisontella bitmatrisspeglingar; rörelse upp/ner ger INGEN ny spriteorientering. Den tekniska runtime-kopplingen är inte därmed implementerad.
3. **Senaste frysta spelarspritekällan är U1-LEG1**, INTE äldre P3 U1, D1/D2 eller U1-FIX1. `SOURCE_U1_LEG1.json` på isolerad gren är pixelmässig referens. En 8×12 A/B med 180 ms per animationsruta i design-GIF; ljusgrå presentationsfärg. U1-FIX1:s övre y0–8 är byte-/bitidentisk i både A/B; de nedre y9–11 är LEG1:s egna frysta getbenspixelrader.
4. **Senaste uttryckliga användargodkännande:** användaren såg U1-LEG1:s **samma pixlar**, med presentationens **höger-/vänsteretiketter bytta**, och sade `Ja, nu är det perfekt. Exakt så här bör den se ut.` MAIN dokumenterade detta som ett **visuellt användargodkännande av nivå-1-designen 8×12** med OMVÄND riktningsetikett, inte användargodkänd autentisk Stella-runtime, färgkontrast i varje värld eller global spelgrafik.
5. **KRITISK visuell etikettmappning, utan bitmapändringar:**
   - Framtida **VISUELL HÖGER** = de tidigare **`LEFT`-maskerna** i fryst U1-LEG1 JSON för motsvarande A/B.
   - Framtida **VISUELL VÄNSTER** = de tidigare **`RIGHT`-maskerna** i samma U1-LEG1 JSON för motsvarande A/B.
   - **Ändra INTE originalets bitsträngar**, skapa ingen extra speglad variant, skriv inte över fryst gren, och anta inte att kontrollens runtime-mappning redan har ändrats.
6. Ytterligare användarbeslut: **nivå 2 och 3 ska se identiska ut med nivå 1, endast större**. **EN enda exakt U1-LEG1 8×12-källmask** för alla tre nivåer, inga nya detaljer eller level-specifik omritning.
7. **Preliminära, ännu inte på Stella godkända nivåskalor:** L1 **8×12** (`P0 x1`, rad ×1); L2 **16×24** (`P0 x2`, rad ×2); L3 **32×36** (`P0 x4`, rad ×3). **L3 har x4/y3**, alltså inte automatiskt identiska upplevda proportioner; kräver särskild framtida kontroll/beslut, inte egen konstnärlig kompensation.

## 5. Godkänt / inte godkänt (läs detta noggrant)
**Godkänt av användaren:** U1-LEG1:s nivå-1-utseende och alternerande benpose såsom visad i **riktningsomvänt namngivna** design-GIF:ar; samma grundpixlar ska återanvändas på L2/L3 (storleksregel).

**INTE tekniskt eller fullständigt godkänt:** korrekt visuellt resultat i riktig Stella för nytt U1-LEG1 på L1/L2/L3; synk mellan visuell höger/vänster och faktiskt joystick-/runtime-rörelser; L2-/L3-proportioner och nivå-3 första rasterrad; riddare, bågskytt, banor/världar, HALO, HUD; en sammanhängande fungerande R3-kernel; fullt visuellt gate-PASS. `#15` är OPEN.

Historiska studier (Q1, P1, P2, P3 U1/U2, P3-F1 D1/D2 och U1-FIX1) får användas för jämförelse/proveniens **bara där det behövs**. P1/P2 horisontellt liggande anatomi är **negativt exempel**. Äldre U1-FIX1 är LEG1:s frysta överdelsbas men inte den senaste fullständiga spritekällan. U1-LEG1:s källförfattares tidigare negativa bedömning av anatomisk läsbarhet föregicks av en användarbedömning som därefter godkände designen i den omvända etikettkopplingen; blanda inte ihop SOURCE-proveniens med senare estetisk acceptans.

## 6. Hårdvarurisker och öppna grindar
- **#15 global visuell gate OPEN**. Den får inte stängas av GRAPHICS på grund av nivå-1-godkännandet.
- **#22 U1-LEG1 SOURCE-arbetsorder CLOSED: completed.** Inte en pågående grafikorder.
- **#21 P3-F1 CLOSED: completed (negativ estetisk studie)**.
- **#19 P01-ART1 level-3 första aktiva P0-rasterrad DEFECT OPEN, inte reparerad.**
- **#1 P01 oberoende Stella/NTSC-grind OPEN.**
- **R3 helscen NO-GO**: konkurrens om P1 för fiender, same-Y flimmer, PF halo/miljö, endast uppskattningsvis 2–4 cykler kvar på värsta rader; grafikdesign får inte lova drop-in rendering.
- M0-extra konturpixel, NUSIZ huvud och två grå färgband gav ingen meningsfull identitetsvinst i MAIN:s frysta source-only koncepttest; ingen sådan hårdvaruanvändning är auktoriserad.

## 7. Status vid migration
**Det finns ingen ny GRAPHICS-ritorder auktoriserad i denna migration.** Denna överlämning gör endast rollinstruktioner, källindex och startprompt tillgängliga på en **separat dokumentationsgren** och i Drive. Inga spelfiler, bitmappar eller tidigare arbetsgrenar får ändras, ingen merge till `main`, ingen ROM/Stella/VERIFICATION startas. Nästa chat ska först läsa riktiga källor och endast rapportera att den kan ta emot en NY explicit MAIN II-order.
