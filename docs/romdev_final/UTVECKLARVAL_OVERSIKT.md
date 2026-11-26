# Utvecklarval för The Skraun

Ordningen börjar med de tio val som närmast påverkar hur spelet syns och spelas. Jämförelserna gäller de angivna provscenerna. UNKNOWN i matrisen betyder att jämförbar kostnad saknas.

## 01 Renderer

Utgångsläge är PR63:s tvålinjeskernel.

- **PR63 och rune** (REJECTED). Större visuell effekt. Förvränger kroppen. 264 i äldre fallet; 0/72 källexakta halo-masker.
- **Ren tvålinje** (IMPLEMENTED). Bevarar PF-timing och VDEL. P1 överlappar fortfarande logiska aktörer. 262 i problemreplay; 72/72 källexakta halo-masker.
- **PR61 enradskernel** (CANDIDATE). Möjlig högre vertikal upplösning. Kräver nytt orb-färgfönster och rastertest. SOURCE_ONLY för denna jämförelse.
- **Vertikalt specialiserad kernel** (NOT_TESTED). Möjlig P1-återanvändning. Ny RESP/REF/VDEL-beviskedja. UNKNOWN.

**Billigast.** Befintlig tvålinjeskernel med kortare blankförberedelse.

**Tekniskt bäst i provad användning.** Tvålinjersläge, bevisad rasterstabilitet i testade pass.

**Bild och spelbarhet.** Tvålinjersläge, exakt gångmask vid halo.

**Rekommendation och levererad lösning.** Vald, lägsta risk för fungerande PF, pil och orb Implementerat val är Tvålinjersläge med separat P0, M0, P1, M1 och BL. Reserv är PR64 för felsökning.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 02 Haloform

Utgångsläge är Rune ersatte P0.

- **Två sidomarkörer** (REJECTED). En enklare M0-bana. Visar ingen övre/nedre räckvidd. 72/72 kroppsmatch under halo.
- **Fyra kardinalmarkörer** (IMPLEMENTED). Fyra riktningar och separata streck. En markör per fas; klipper vid kanten. 72/72 kroppsmatch; 24 aktiva per nivå.
- **Första kaptabellen** (REJECTED). Fyra riktningar möjliga. DASM fyllde ett läsbart intervall med $FF. 18/24 kroppsmatch per nivå; långa oavsiktliga streck.
- **Åtta oktagonsegment** (NOT_TESTED). Tydligare diagonaler möjliga. Kräver fler faser eller flera objekt. UNKNOWN.
- **Pulserande strålar** (NOT_TESTED). Möjlig bättre identitet. Kostnad vid flytt och lokal färg okänd. UNKNOWN.
- **Enbart gul kropp** (REJECTED). Ingen extra positionering. Visar ingen räckvidd. SOURCE_ONLY.

**Billigast.** Två sidomarkörer har kortare kod, CPU-jämförelse UNKNOWN.

**Tekniskt bäst i provad användning.** Fyra riktningar med skyddad M0-tabell.

**Bild och spelbarhet.** Fyra riktningar ger den tydligaste provade zonen.

**Rekommendation och levererad lösning.** Vald inom mandatet Implementerat val är Gul P0 och fyra fasade kardinalmarkörer. Reserv är Sidomarkörer i teknisk felsökning.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 03 TIA-resursdelning

Utgångsläge är BL delades mellan orb och halo.

- **BL som halo i orbens avfas** (REJECTED). Fler samtidiga markörer. Mer BL-positionering och PF-färgkonflikt. Tidigare fysisk blinkning bekräftad.
- **BL endast orb** (IMPLEMENTED). Färre objektkonflikter. Högst en M0-markör per bild. BL fast bredd, lokalt guld.
- **Lokal PF-halo** (NOT_TESTED). Möjliga längre segment. Kan färga eller skriva över fastställd miljö. UNKNOWN.

**Billigast.** Fast BL-ägare kräver noll extra BL-positioner för halo.

**Tekniskt bäst i provad användning.** Separata ägare undviker stale BL under halo.

**Bild och spelbarhet.** Separata markörer, stadig orbfas och pil.

**Rekommendation och levererad lösning.** Vald. Halon disponerar M0 även när pil finns. Implementerat val är P0+M0, P1+M1, BL+PF. Reserv är Behåll BL för orben.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 04 Fiendescheduler

Utgångsläge är Adaptiv P1 + villkorlig NUSIZ-kopia.

- **Adaptiv + exakt dubbelkopia** (IMPLEMENTED). Prioriterar varning/hugg. Flera samtidiga fullmasker saknas. Samma Y 8/7/9 av 24; lucka 3/3/2.
- **Ren turordning** (CANDIDATE). Jämnare när alla tre konkurrerar. Ingen prioritering av ett akut hot. Samma Y 8/8/8 av 24; lucka 2/2/2.
- **P1-retrigger samma Y** (REJECTED). Möjlig ökad samtidighet. Källkorrekta tre masker obevisade. Historiskt N7 S2-FAIL i två varianter.
- **Vertikal P1-återanvändning** (NOT_TESTED). Mindre flimmer vid höjdseparation. Fysiska beamdeadlines öppna. UNKNOWN för ny integration.

**Billigast.** Ren rotation har enklare källväg; CPU UNKNOWN.

**Tekniskt bäst i provad användning.** Adaptiv kvar för enskilt hot, rotation jämnare i dubbelscenen.

**Bild och spelbarhet.** Dubbelscen gynnar rotation marginellt, enskilt hot gynnar prioritet i koden.

**Rekommendation och levererad lösning.** Behåll det adaptiva beteendet som helhet Implementerat val är Adaptiv prioritet med rättvisa turer. Reserv är Rotationsvarianten vid ny isolerad jämförelse.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 05 Pil

Utgångsläge är M1-band i två rasterrader.

- **Fast M1** (IMPLEMENTED). Ingen egen färgskrivning. P1-färgen kan växla. Legacy-pilscener 262.
- **Tidsdelad M1** (NOT_TESTED). Kan frigöra vissa rader. Lucka före träff ökar. UNKNOWN.
- **M0-projektil** (NOT_TESTED). Gemensam guldton. Tar halons markör. UNKNOWN.

**Billigast.** Befintlig M1 utan extra färgskrivning.

**Tekniskt bäst i provad användning.** Befintlig fri M1 under M0-halo.

**Bild och spelbarhet.** Färg kan förbättras om nattprovet visar behov.

**Rekommendation och levererad lösning.** Behåll fysisk pil i alla faser Implementerat val är M1 med spelmotorns befintliga riktning och P1-delad färg. Reserv är Fortsätt med befintlig M1.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 06 Riddarpose

Utgångsläge är Integrerad varning, hugg, återhämtning.

- **Integrerad P1** (IMPLEMENTED). Inget separat vapen. Full pixelbevisning av hugg återstår. Tre äldre riddarprover har matchande state.
- **Boxing-liknande NUSIZ** (NOT_TESTED). Större visuell räckvidd. Kan förvränga kropp och dubblera pil. UNKNOWN.
- **Separat svärd** (REJECTED). Ingen. Bryter beslut. Utanför uppdraget.

**Billigast.** Maskbyte utan skalningsskrivning.

**Tekniskt bäst i provad användning.** Integrerat maskbyte, villkorad NUSIZ.

**Bild och spelbarhet.** Tydlig pose och varningsfärg, fulla riktningstest återstår.

**Rekommendation och levererad lösning.** Vald, behåll föredragen ljusblå grundton Implementerat val är Befintliga P1-maskposer och låst spegling. Reserv är P1-maskpose.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 07 Rangers spegling

Utgångsläge är P1 vände mot spelaren.

- **Tidigare facing** (REJECTED). Kort. Neutral Ranger tittar mot förföljaren. Befintlig källväg.
- **Tillståndsbaserad facing** (IMPLEMENTED). Släpp följer aktuell pil. Pixelprov i alla världar och båda riktningar öppet. Källräknad extra jämförelse, ingen RAM.
- **Bestående senaste flyktriktning** (NOT_TESTED). Exakt efter vertikal rörelse. Kräver livslängdsbevis för nytt state. UNKNOWN.

**Billigast.** Tidigare jämförelse billigast i källan.

**Tekniskt bäst i provad användning.** Ny gren utan RAM, färg lika miljö.

**Bild och spelbarhet.** Bow pose passar riktning bättre.

**Rekommendation och levererad lösning.** Vald, exakt pilvektor och kamouflage bevaras Implementerat val är Flykt bort, drag mot spelare, släpp enligt ArrowDX. Reserv är Återställ facingkod isolerat vid fel.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 08 Skrauns storlekar

Utgångsläge är 8×12, 16×24, 32×36.

- **8×12, 16×24, 32×36** (IMPLEMENTED). Stark visuellt stor L3. Längre vertikal överlappning. 72/72 kroppsmatch vid aktiv halo.
- **8×12, 16×20, 32×30** (CANDIDATE). 4/6 färre fysiska kroppsrader. Ojämn repetitionshöjd och förändrad kollision. 72/72 kroppsmatch vid aktiv halo.

**Billigast.** Kompakt sparar 40 tabellbyte, ROM-längden densamma.

**Tekniskt bäst i provad användning.** Ordinarie kropp proportionerlig och bevarad kollision.

**Bild och spelbarhet.** Båda fungerar i testad halo; original ger kraftigare L3.

**Rekommendation och levererad lösning.** Behåll storlek. Kompakta kroppens reducerade vertikala kollision är en synlig kompromiss Implementerat val är Originalstorlekar och konsekvent kollisionsmodell. Reserv är Kompakt för separat jämförande speltest.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 09 Orb

Utgångsläge är BL två på/två av med halo-delning.

- **Fast BL och befintlig blinkning** (IMPLEMENTED). Oberoende halo-position. Alla 16 kombinationers pixel-XY ej verifierade. 32/32 syntetiska tillväxtprov; 16 L3-fall utan upptag.
- **Långsammare blinkning** (NOT_TESTED). Längre varje synlig period. Längre sammanhängande frånvaro. UNKNOWN.
- **Nya längre X-avstånd** (NOT_TESTED). Säkrare avstånd från start möjligt. Tillväxt och fri väg måste bevisas på nytt. UNKNOWN.

**Billigast.** Ingen BL-halo ger lägre objektkostnad.

**Tekniskt bäst i provad användning.** Lokal COLUPF och fast bredd.

**Bild och spelbarhet.** Samma förutsägbara blinkning, testad uppgradering.

**Rekommendation och levererad lösning.** Vald utan avståndsändring Implementerat val är BL två på/två av och två X per bana. Reserv är PR64 för jämförande färgprov.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 10 Miljö och färg

Utgångsläge är R3 inklusive godkänt motivbyte.

- **Fryst R3-PF1** (IMPLEMENTED). Motiven bevaras. Ingen ytterligare ROM-kompression. SHA-256 kontrollerat; 8-bane pendel.
- **Representationsekvivalent kompression** (NOT_TESTED). Kan spara lagring. Avkodning kan kosta rastercykler. UNKNOWN.
- **Global guld-PF** (REJECTED). Enkel färgskrivning. Förlorar miljöfärgen. Utanför uppdraget.

**Billigast.** Befintlig datastruktur.

**Tekniskt bäst i provad användning.** Byte-identiskt motiv och samma färgtabell.

**Bild och spelbarhet.** Samma godkända banor.

**Rekommendation och levererad lösning.** Vald Implementerat val är Exakta 768 bytes PF1, samma palett. Reserv är Återställ endast rendererdiff.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 11 HUD och förlust

Utgångsläge är BCD HUD; tidigare fontkalkyl.

- **Förberäknade poängrader** (IMPLEMENTED). Bibehållen font. Mer ROM för tabeller. PR64: 100 sifferpar × fem rader per register; 262 regression.
- **Beräkna font varje bild** (REJECTED). Färre tabellbyte. För sen VBLANK. 264/310 i svårsekvens.
- **En poängkopia** (IMPLEMENTED). Samma läsbara position. 12 ytterligare PF/CTRLPF-skrivningar per bild. Båda världsspeglingar: vänster 384→384, höger 296→0 pixlar.
- **Dubblerad poäng** (REJECTED). Färre skrivningar. Onödig kopia. 296 oönskade pixlar i höger HUD-halva.
- **Tvåsiffrigt liv** (NOT_TESTED). Möjliggör över 9. HUD-deadline och designbeslut behövs. UNKNOWN.

**Billigast.** Uppslag minskar CPU; tidigare kalkyl använder färre tabellbyte.

**Tekniskt bäst i provad användning.** Uppslag med exakt font och stabil bild.

**Bild och spelbarhet.** Samma siffror; svart förlust och RESET.

**Rekommendation och levererad lösning.** Vald Implementerat val är PR64:s uppslag, enkel poängrad och svart förlust. Reserv är Fryst PR64.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 12 Spelmotor

Utgångsläge är FULLGAME-1, standardkollision.

- **Befintlig motor** (IMPLEMENTED). Logiken bevarad. Ytterligare kollisions- och återfödelsegränsfall öppna. 4401 synkade pendelbilder, L3, 8400, 7 liv.
- **Tabellstyrd kollisionsoptimering** (NOT_TESTED). Kan spara CPU. Måste vara likvärdig i alla 24 fall. UNKNOWN.
- **Rörelselås vid halo** (REJECTED). Ingen uppmätt vinst. Bryter fri rörelse. HEALTH-3 negativt.

**Billigast.** Behållen kod, annan CPU UNKNOWN.

**Tekniskt bäst i provad användning.** Bevisad pendelloop och orb.

**Bild och spelbarhet.** Bekant respons och fria rörelser.

**Rekommendation och levererad lösning.** Vald, utan permanent gameplaykompromiss Implementerat val är Bevarade bank 0 och 2. Reserv är PR64.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 13 Ljud

Utgångsläge är Två kanaler, prioriterade envelopes.

- **Befintlig tvåkanalsmotor** (IMPLEMENTED). Verkligt ljud i spelvideon. Ingen subjektiv avlyssning. SDL 44,1 kHz float stereo; PCM med signal.
- **Ny prioriterad mix/envelope** (NOT_TESTED). Kan ge tydligare samtidiga händelser. Ej kvalificerad. UNKNOWN.
- **En kanal** (NOT_TESTED). Sannolikt enklare kod. Sämre separering av effekter. UNKNOWN.

**Billigast.** Ingen ny förbrukning.

**Tekniskt bäst i provad användning.** Ändra ljud först efter händelsevis mätning.

**Bild och spelbarhet.** Mixrangordning UNKNOWN.

**Rekommendation och levererad lösning.** Behåll fungerande originalmix Implementerat val är Befintligt AUDC/AUDF/AUDV, verklig PCM fångad. Reserv är Tidigare envelope.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 14 Resurser

Utgångsläge är Standard F6 och RIOT 128 B.

- **VBLANK-position och nollguard** (IMPLEMENTED). M0-index når ingen kod eller $FF-fyllnad. Global stack- och beamgräns obevisad. Snapshot f5 efter stackskrivning i provet, samma som PR63.
- **Implicit ORG-fyllnad** (REJECTED). Färre källrader. Felaktiga ENAM0-värden. Lång markör med $FF i maskområdet.
- **Annan mapper** (REJECTED). Eventuellt mer utrymme. Ny kompatibilitetsevidens och nytt mandat. Utanför uppdraget.

**Billigast.** Ny kod återanvänder befintliga scratchpekare.

**Tekniskt bäst i provad användning.** DASM och Stella samt stackprov.

**Bild och spelbarhet.** Tillräckligt i testade sekvenser.

**Rekommendation och levererad lösning.** Vald med explicit $FDA2–FDFF-nollfyllnad Implementerat val är Samma mapper, inga nya RAM-byte. Reserv är PR64 vid regression.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.

## 15 Bild och ljudbevis

Utgångsläge är Tidigare endast kort ny video.

- **Livevideo med SDL-ljud** (IMPLEMENTED). Visar en hel sammanhängande sekvens. Ljudsynk uppskattad. 4402 fångade SDL-presenteringar; faktiskt emulatorljud.
- **Stella-PNG-bildsteg** (IMPLEMENTED). Exakt pixeljämförelse. Fixturer är syntetiska. 144 rörelsebilder per visuell variant.
- **Principbilder** (REJECTED). Ingen kostnad för testbygge. Kan ej bevisa rendering. Ingen emulatorobservation.

**Billigast.** PNG är lättast att granska pixelvis.

**Tekniskt bäst i provad användning.** Livevideo + rå Stella-session.

**Bild och spelbarhet.** Videon visar riktig rörelse, PNG visar mask och faser.

**Rekommendation och levererad lösning.** Använd båda Implementerat val är Kontinuerlig live Stella-video och korrekta PNG. Reserv är Råbilder om videoformat saknas.

**Bevis.** Se motsvarande ID i matrisen och råmaterialet.
