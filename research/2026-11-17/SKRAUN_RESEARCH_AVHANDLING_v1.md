# THE SKRAUN – RESEARCH HANDOFF v1
## Full-game architecture, 17 november 2026

**Roll:** RESEARCH (rådgivande). **Leverans:** systematisk källundersökning, verklig assemblergenomgång, 30-trick-matris, arkitekturjämförelse och falsifierbara minsta tester. **Ingen ROM är byggd, ingen projektfil i GitHub/Drive har ändrats och ingen ny utvecklingsgrind är godkänd.**

**Forskningsstatus:** Omfattande första jämförande rapport, inte ett slutligt bevis för möjlig full-game-renderer. Internationell sökning har genomförts på åtta språk men nya primärkodfynd hittades huvudsakligen på engelska. Ingen påstådd fullständig täckning av alla historiska forum, ROM:er eller Atari-hårdvarurevisioner.

## Del I. Executive summary

**Viktigast:** R3 ska inte stegvis 'lappas' till en färdig motor. I den faktiska same-Y-diagnosen ger P1 enbart 20 Hz per fiende, PF kräver ett val mellan 30 Hz färgväxling och guldaktiga hinder, och värsta B-rasterraden har **2–4 statiskt uppskattade cykler kvar** före projektil/orb/AI. Detta är en NO-GO för just testad motor. [P06]

**Mest lovande kombination för fortsatt RÅDGIVANDE prövning:** ett nytt **kontrakterat multikernel-system** där P0 är konstant reserverad för Skraun, fiender använder P1 med explicit samma-Y-budget, PF-beskrivningen görs till *sparse register-change stream* i stället för brutala sex PF-skrivningar på varje rad, HUD har separat kernel och kollision förbereds under VBLANK/overscan. Det är en hypotes, inte ett verkligt PASS. [T01][T02][T03][P06][P07]

**Första avgörande forskningsfrågan före ny renderer-auktorisation:** kan en vanlig 2600, utan specialcartridge, rita (a) samma-Y två riddare + grön bågskytt med oberoende X och begriplig förvarning, (b) stor Skraun, (c) gul halo och synliga, tydligt åtskilda solida hinder **i samma frame**, utan att ta bort pil/orb-kapacitet och utan 76-cykel-övertramp? Det räcker inte att enstaka komponenter fungerar. [P01][P06]

**Nytt prioriterat fynd:** äldre 'Venetian blinds'-teknik är mer relevant än tidigare R1-audit antog, men bara som en testbar *fiendespecifik* fallback: fördela P1-aktörers rasterrader inom samma frame, i stället för att låta hela karaktärer försvinna under två bildrutor. Historiskt dokumenterat i *Video Chess*, modernt exempel *Kovi Kovi* med E7/RAM-kernel; **inte bevisat** att tre små vapenförande motståndare blir läsbara på 8–12 rader. [T05][T06] En ren Venetian-lösning för enbart P1 kan dessutom förlora 2/3 av rasterdetaljerna vid tre same-Y-aktörer och får inte på förhand kallas flimmerfri.

**Nytt aktuellt jämförelsespår:** Steven Huggs 2025 'versatile playfield kernel' använder [registeradress, värde]-par och `STA $00,X` i stället för att uppdatera allt varje rad. Artikeln anger upp till cirka **9 cykler per scanline för PF-deltaflödet** under sina tabell- och sidgränsantaganden. Tre-strömsversionen har 32 byte per display list och uppdaterar ett register per ström/rad, men författaren varnar för grafik-tearing och RAM-kostnad. Detta är **inte** ett färdigt Skraun-svar. [T02][T03]

### Rangordning av forskningsspår

1. **A: specialiserade multikernels + sparse PF + strikt same-Y adversarial test**, utan att anta genomförbarhet. Bäst balans mellan vanlig hårdvara och möjlig processorbudget; huvudproblemet är tre fiender i samma band samt separat PF-färg.
2. **B: fiendespecifik intra-frame line interleave + specialiserade multikernels.** En reell historisk metod; risk för svårläst svärd/båge och LCD-artefakter.
3. **C: tre-register-stream/displaylist-arkitektur.** Kontrollerbar och intressant, men generellt 32B per list och 3 registerskrivningar/linje skapar trängsel.
4. **D: alternativ resursägarskap:** M0 för pil, BL för orb eller liknande, PF för halo och särskild statisk scenkod. Kan avlasta fiendebitmaps men ger inte automatiskt två PF-färgplan.
5. **E: cartridge-RAM eller hårdvarustöd (F6SC/E7/DPC+/CDFJ)** om vanlig TIA verkligen inte räcker. Beslut kräver stöd i faktisk distribution, kompatibilitet med originalkonsol/RetroN 77 samt användarval.

## Del II. Verkligt nuläge och källauktoritet

Aktuellt kontrollerat 2026-11-17 via ansluten GitHub, inte Memory: GitHub repo `Odourman/the-skraun` (main), designbeslut 01–60 [P01], senare användarkorrigering för upprätt trolldesign och U1-LEG1 8×12 + exakt spegelvänd R/L [P02], R3 [P06], kollision K0 [P07], åtta **icke-kanoniska** banutkast [P08]. Issues **#1, #15, #19, #23 och #24 OPEN** vid vår läsning [P10–P14]. P01-COL1 är en uttryckligen auktoriserad, smal och köad ROM-order; **issue OPEN är inte bevis att den har exekverats**. Upprepa inte detta test från RESEARCH. ART1 PR #18 är draft; 24/36 autentiska Stella-states pixel-exakt, samtliga 12 L3-states har extra översta grå rad och ett strikt rött test [P12][P15].

**Fast design som inte får tyst ändras:** Skraun upprätt på overhead-arena, ljusgrå U1-LEG1 med A/B och semantiskt godkänd vänster/höger, samma 8×12-källa i L1/L2/L3 med preliminära renderstorlekar 8×12/16×24/32×36; åtta arenor/fyra världar; 8-vägs joystick och konstant faktisk fart; level-3 OP och rymlig miljö; 2 riddare plus flyende grön bågskytt synliga som riktiga fiender; 360° gul halo som följer troll och passerar hinder; svärd/pilar stoppas av hinder; orb, ljud, poäng och liv; så lite flimmer som möjligt. [P01][P02][P08]

**R3 i verklig DASM/Stella, utvecklaregenkontroll:** tre 4096B 6507 ROMs; same-Y scen (32,78), (101,78), (147,78) ger 4/12 frames per fiende (20Hz); delvis överlapp 6/12,6/12,12/12; separerade Y 12/12 var. R3:s färgvariant kan antingen visa gul halo och blå hinder i 6/12 respektive 6/12 *alternativa frames*, eller sammanfoga båda i samma PF-färg. Värsta B-linjer 72/73/74 av76, som **statiskt beräknade** värden; 262 NTSC scanlines verifierat direkt i Stella, inte full CPU-profil. R3 P1Buf 89B och annan state 23B = 112/128 RIOT RAM, med stackrisk och 9 säkert fria mellan $97..$9F. Pil, orb, all AI, riktig kollision och riktig HUD saknas. Detta är inte någon allmän omöjlighetssats. [P06]

**K0 i Python, inte Atari:** 8 icke-kanoniska kartor × 3 nivåer, 24 uppsättningar hinderrektanglar och cirka 444 preliminära ROM-databyte. Strikta substeps undvek modellens corner-cutting; ett svep över 4 klockenheter avvisades för klibbig rörelse trots formell säkerhet. Alltså programmeringsmodell och urval, inte ROM-spelkänsla eller CPU-cykelmätning. [P07]

### Två viktiga åtskilda begränsningar

- **TIA fysisk scen:** endast 2 åttabitars-players; två missiles som delar spelarens färg; ball som delar PF-färg; en PF-mask för ett givet rasterögonblick. Enbart mer ROM/RIOT RAM skapar inte fler register eller fler CPU-cykler på en fysisk scanline. [T01]
- **Logisk spelsimulering:** rörelse/kollision/AI kan göras i VBLANK/overscan där tidsbudget finns, men de synliga objekten och deras X-koordinater måste faktiskt levereras till kerneln i tid. Blank-perioderna har enligt klassiska guide cirka 70×76=5320 cykler nominellt under NTSC, men VSYNC/VBLANK/overscan måste hållas korrekta och hela mängden är inte fri spelbudget. [T01]

**RAM-gräns som diskvalificerar naiv 'lägg till display list' i R3:** R3 112B fasta state/buffert + tre-stream-kernelns två 32B listor = **176B före stack och extra pekare**. Det överskrider 128B med 48B. Detta är en *härledd additionskontroll*, inte ett argument mot en helt ersättande stream-arkitektur där 89B P1Buf kan tas bort. Full RAM-liveness krävs före sådant val. [P06][T03]

## Del III. Alla 30 historiska trick – självständig omprövning

Följande tabell innehåller **samtliga 30 med egen kostnad, belägg och ett minsta falsifierande prov**. För full sökbar bedömningsmatris, se `30_TRICK_TEKNISK_MATRIS.csv`. 'Dokumenterat' avser den historiska tekniken; inte att den klarar The Skraun.

| # | Teknik | Slutsats | Minsta praktiska skiljelinje |
|---:|---|---|---|
| 01 | Sprite multiplexing | Hög, men ej bevisad för same-Y. **Kostnad:** P1-retiming/slots och Y-luckor; konflikter på samma rasterrad. **Belägg:** Cyloid game.asm; River Raid asm; R3 scheduler. | Jämför 1/2/3 P1-aktörer med X/Y helt fria, 12 sekventiella frames, cykel-/RAM-ledger. |
| 02 | Mid-scanline GRP-omskrivning | Forska, X-begränsning central. **Kostnad:** Extremt snäva X-deadlines; en instruktion kan förstöra PF. **Belägg:** 8bitworkshop retrigger-exempel i 8-bit book; P02-R2 kopietest. | Tre oberoende bitmappar i vänster/mitt/höger och permuterade X, med P0+PF aktiva. |
| 03 | Venetian blinds | Omprövas som reserv för P1-fiender, ej P0. **Kostnad:** Minskad effektiv vertikal upplösning; tearing på LCD; vapenförvarning kan försvinna. **Belägg:** Video Chess enligt AtariAge design case; Kovi Kovi (E7). | Två/tre P1-aktörer vid identisk Y, 1/2 resp. 1/3 scanline-duty, autentiska 12-frame bilder; 4:3. |
| 04 | Sprite flickering | Undvik som grundmotor. **Kostnad:** 20 Hz per tre aktörer, ojämn synlighet och TV-beroende. **Belägg:** Pacman4K ASM av Debro; AtariAge diskussion 2023. | A/B 20/30/60Hz med rörelse, bildsekvens/CRT/LCD, synlighet per aktör. |
| 05 | Dynamic playfield sprites | Redan provad; isolerat bevis räcker inte. **Kostnad:** PF/Hinder delar COLUPF och geometrisk rasterresurs. **Belägg:** Skraun B3b/R3. | Halo+minst tre hinder under exakt samma scanline, båda färger varje frame. |
| 06 | Mid-frame sprite resizing | Inte tillåtet ändra U1-LEG1 grafik; jämför endast inofficiellt. **Kostnad:** Bredd/streck kan skifta och ge glitch; #19 förstalinje-fel. **Belägg:** Hugg three-stream kernel; P01/ART1 skalförsök. | Testa oförändrade 8x12 masker och 3 storlekar; ingen designändring. |
| 07 | Asymmetric playfield | Dyr befintlig resurs. **Kostnad:** 6 PF-writes samt adressering; deadlinebegränsad. **Belägg:** Skraun B3b; Combat/8bitworkshop PF-teknik. | Samma PF-bitar vid tre X-lägen, inga ghost columns; minst två färgzoner om möjligt. |
| 08 | Two-line kernel | Hög som byggsten, ej helhetslösning. **Kostnad:** Halverad vertikal färg/bitmapkontroll eller kräver VDEL. **Belägg:** River Raid källkommentar; R2 DASM. | Full arena med P0, minst ett P1, gul halo, blå hinder och tvålinjerskontur. |
| 09 | VDEL delayed graphics | Hjälpte historiskt; otestad i full Skraun. **Kostnad:** Hjälper deadlines men ger inga fler players. **Belägg:** River Raid VDELP1; Adventure VDEL01. | Kontrollera A/B korrekt radordning, alla 3 level och två fiendebitmappar. |
| 10 | HMOVE fine positioning | Nödvändig riskkontroll. **Kostnad:** HMOVE blanking och förändring av P0 vid P1-reposition. **Belägg:** River Raid; Combat; R3 HMOVE fix. | Skraun stilla och P1 omplaceras i raster; visa noll oönskad P0-förskjutning. |
| 11 | Late HMOVE | Reserv med mycket låg prioritet. **Kostnad:** Möjliga HMOVE bars/versionsberoende. **Belägg:** Stella TIA-specifik diskussion; ingen Skraun-kod bevisad. | Real Stella + olika TIA-revisioner, ärligt särskilj observation och antagande. |
| 12 | Raster color changes | Bra sekundärt, ej lagerlösning. **Kostnad:** Kan inte ge två samtidiga PF-färger på samma pixel inom en PF-plan. **Belägg:** Hugg versatile PF; R2 interlace. | Gemensam rasterrad med halo+hinder; verif. båda synliga 60Hz utan fusk. |
| 13 | 48-pixel score kernel | Senare specialiserad HUD. **Kostnad:** Kräver P0/P1 och HUD-rader i eget band. **Belägg:** Bumbershoot 48px kernel; Combat score. | Värsta HUD + första aktiva fienderaden, inga state-spill. |
| 14 | Multiple display kernels | Hög som arkitektur, zoner måste vara reella. **Kostnad:** Byten kostar rader/cykler; dynamiska Y-överlapp kan strypa. **Belägg:** Pitfall! nio kernelstråk; R2 HUD; Hugg three-stream. | Flytta fiender till gränserna och mitt i halo, mät länkning utan bortfall. |
| 15 | NUSIZ duplication | Reserv för visuella effekter/temporära formationer. **Kostnad:** Kopior är inte tre fria individuella fiender. **Belägg:** Space Invaders; R2 två P1-kopior. | Värsta scen med tre distinkta bitmappar + olika X-avstånd; testa tillåtenhetsmatris. |
| 16 | REFP mirroring | Låst godkänd metod. **Kostnad:** Billigt; visuellt höger/vänster kräver riktig semantik. **Belägg:** Skraun A/B och formell U1-LEG1. | Exakt U1-LEG1 källpixlar + semantiska R/L i Stella. |
| 17 | Missile/ball reuse | Stark för pil/orb men resurskonflikt. **Kostnad:** M0 P0-färg, M1 P1-färg, BL PF-färg; endast smala vertikala former. **Belägg:** Combat M0/M1; Pitfall ball liana; Cyloid M0. | Rita M0-pil och BL-orb med två riddare + ring + PF-hinder; ägarskapsledger. |
| 18 | SCORE mode | Reserv för värld/kontrast. **Kostnad:** Vänster/höger färg, inte separata guld/stenpixlar inom samma halva. **Belägg:** R1 SCORE experiment; Hugg versatile PF. | Flytta ring+hinder från vänster till höger, testa färger på gemensam rad. |
| 19 | Playfield priority | Låg för huvudkonflikt. **Kostnad:** Färgproblem kvarstår; kan dölja fiender/Skraun. **Belägg:** Combat och Pitfall!. | Skraun/knight/hinder-överlapp, logisk hitbox oberoende av prioritet. |
| 20 | Hardware collision latches | Komplement, ej fysiksanning. **Kostnad:** Använder ritad komposit, kan sammanblanda halo/hinder. **Belägg:** Combat; Adventure; River Raid. | Rita halo genom hinder och kör oberoende fysiska kollisionsnegativ. |
| 21 | RIOT timer scheduling | Hög som planering. **Kostnad:** Budget varieras med 60Hz, kan skapa time debt. **Belägg:** Stella Guide; Cyloid even/odd GameLogic. | Mät verklig timer debt min/max med 3 fiender och diagonalkollision. |
| 22 | Stack/RAM mirroring | Endast efter liveness-analys. **Kostnad:** Stacköverflöd, live-range-konflikt; stack ska reserveras. **Belägg:** River Raid overlays; R3 112B RAM. | Generera byte-för-byte minnes- och stacklivslängdsrapport. |
| 23 | Undocumented 6502 opcodes | Låg. **Kostnad:** Portabilitet/emulatorvariation, ingen ny TIA-fysik. **Belägg:** Pacman4K kommenterar användning. | Individuell tidsvinst mot dokumenterade 6507-instruktioner, emulator/hårdvara. |
| 24 | Precomputed tables/cycle-exact | Hög, men precompute måste spara verkliga skrivningar. **Kostnad:** ROM-krav vs viss reducerad runtime; X/Y-kombinatorisk tillväxt. **Belägg:** R1 528B dedup; K0 444B kandidat; Hugg tabeller. | Generera samtliga verkliga X/halo-konturstate; räkna minsta antal PF writes och deadline. |
| 25 | Stack-based TIA writes | Avråd tills tydlig lokal cykelvinst. **Kostnad:** Mycket spröd kontrollström/stack. **Belägg:** Historiska teknikkataloger, ingen specifik Skraun-kod. | Isolerad mot normal STA med symbol-/stackbevis. |
| 26 | Timing-based horizontal scrolling | Ej huvudspår. **Kostnad:** Skraun har åtta fasta icke-scrollande arenor. **Belägg:** River Raid rullande flod som närliggande analogi. | Endast om designen uttryckligen ändras. |
| 27 | SCABS/FE banking | Ej aktuell; OBS FE och SCABS namn varierar i källor. **Kostnad:** Mapperbyte, ingen extra bildfysik. **Belägg:** Stella mapperlista/Atari Compendium. | Testa enbart formatidentifiering + kompatibilitet om nya cartridge beslut tas. |
| 28 | Superchip/extra RAM | Reell kandidat om RAM blir hindret. **Kostnad:** Mer arbets-RAM, inte CPU/rasterfärg. **Belägg:** Stella F8SC/F6SC dokumentation. | Exakt RIOT+SC RAM-budget och originalhårdvaru-/ROM-loader-test. |
| 29 | DPC custom chip | Sekundärt långsiktigt hårdvaruspår. **Kostnad:** Hårdvarukrav/kostnad; nya TIA sprites ej möjliga. **Belägg:** Pitfall II DPC arkitektur; Stella stöd. | Mät om datastream faktiskt minskar TIA visible deadlines, inte bara 6507 prep. |
| 30 | DPC+/CDF/ARM | Endast explicit plattformsbeslut. **Kostnad:** Reproducerbarhet och RetroN77-stöd oprövade; TIA deadlines kvarstår. **Belägg:** Stella CDF/DPC+ dokumentation; Kovi Kovi E7 annat format. | Kompatibilitetsmatris Stella/originalkonsol/RetroN77 och realistiskt minimalt ROM. |

### Nya eller underutnyttjade tekniker utanför de 30

**31 – Adressstyrt deltaflöde för TIA-register, historiskt dokumenterad 2025:** Hugg väljer ett *enda* PF/CTRL/färg-register per par rasterrader. Vinner tid enbart om ring+hindermaskens pixelgeometri kan uttryckas av dessa *förändringsbegränsningar*. En perfekt ring behöver ofta PF0/PF1/PF2 bytas samtidigt; då faller teorin. Gör därför *representability compiler* offline som konkret förtest. [T02]

**32 – Tre-ströms displaylist-schemaläggning, dokumenterad 2025:** Separata strömmar för PF/P0/P1, inkluderar HMOVE-faser och dynamiskt byte mellan kodsekvenser. Egna data-/RAM-kostnader och risk att sprite/arena 'slits'. Ser lovande ut för *vissa* flyttbara objekt, men inte redan uppmätt same-Y och inte gratis. [T03]

**33 – Färgbytets oanvända bit som M0-enable, dokumenterad AtariAge 2008 och tidigare Skraun-research:** Om COLUP0 D0 används som signal till ENAM0 via `ASL`, kan en separat enable-tabell sparas för ett extra kontursegment; per rad minst en `ASL` och en `STA` samt eventuell per-rad-färgladdning. Detta är en extra **datakodning**, ingen tredje bitmap. Använd inte utan att kartlägga M0-pil och den frysta U1-LEG1-figuren. [P05]

**34 – Körbar Venetian-self-modifying kernel i cartridge-RAM:** *Kovi Kovi* beskriver E7 16K och ~2KiB extra RAM för att lagra/uppdatera displaylogik och interlace-fyllning. Det är en **annan hårdvaruklass** än Skrauns 4K-baserade diagnoser och får inte överföras rakt av. [T06]

**35 – Spelberoende 'actor-visibility contract' (ny forskningsmetod, ingen ny TIA-opkod):** Genomför för varje tänkbar samlad scen en explicit garantitabell för varje farligt objekt och varje 12/60-framestest. Varje projektil, svärdstelegraf och pil ska ha definierad synlighets-/attackfas även vid overlap. Det kan avslöja att en grafisk lösning tekniskt visar mycket men spelmässigt är orättvis.

## Del IV. Internationella sökfynd och begränsningar

Sökningar gjorda i engelska, tyska, franska, spanska, portugisiska, italienska, japanska och svenska; en sökning om venetian blinds och äldre AtariAge arkiv tillkom. **De flera icke-engelska sökningarna producerade övervägande sekundära beskrivningar eller återciterade engelska källor.** Spansk källa om *Space Invaders* återger begränsningen att NUSIZ-kopior fungerar på fasta avstånd och att varierande fiender tenderar att flimmra; den behandlas endast som sekundär diskussion, inte som original assemblerbevis. [T01][T04]

Tre publicerade internationella/historiska spår är särskilt viktiga:

- AtariAge-författararkivet om *Video Chess* beskriver Bob Whiteheads *Venetian blinds*, fyra schackpjäser på varannan scanline och ytterligare fyra på de alternerande raderna. Det ger fler figurer men gles grafik. **Historiskt belagt, ingen Skraun-ROM.** [T05]
- *Kovi Kovi* beskriver self-modifying E7 cartridge RAM-kernel samt teknik för att jämna ut vertikala luckor. **Dokumenterad utvecklaruppgift, men ingen offentlig assembler i denna granskning.** [T06]
- AtariAge-forum 2023 rapporterar olika resultat av 30Hz/varannan-frame-flimmer i Stella, Javatari och RF-kopplad LCD. Det är en utvecklares observation, inte kontrollerad full skärm/studie. Men det motiverar fysisk skärmskillnad som testvariabel. [T04]

Sökfrågor/språk och fullständig begränsningslogg finns i `SOKLOGG.md`. Ingen ny primär kod i franska/tyska/portugisiska/italienska/japanska/svenska identifierades under just denna granskningsomgång. Detta är en dokumenterad **söklucka**, inte ett negativt bevis om litteraturens innehåll.

## Del V. Källkod och spel – 11 relevanta, tydlig bevisklass

1. **Cyloid (Keith Adler, 2026; verklig ASM läst).** `game.asm` har P0=tank, P1=flicker-multiplexade mål/boss, M0=projektil och PF=hinder; första 30 raders resursplan, tvålinjerskernel och uppdelat jämna/udda frames. `TankGfxBuf`/`TankColBuf` om 8 byte vardera förbereds före raster. Koden vid ungefär rad 791 väljer `FlickerIdx`, och kring 1679 börjar cykelsatt 2-radskernel. **Överförbart:** konsekvent TIA-ägarskap, dubbelroll mellan frames, precompute av P0. **Inte löst:** tre tydligt telegraferade samma-Y fiender och separat halo-PF-färg. [C01]
2. **Pacman4K (Dennis Debro, 2007/2014; verklig ASM läst).** Källa rad 42–43 anger själv valt 20Hz-flimmer i stället för större ROM-kostnad för variabel flimmeralgoritm. Balanserad speed-tabell och tight kernel visar möjlig komprimerad fullspelslogik. **Överförbart:** ärlig redovisning av flimmer som medveten kompromiss, inte mirakel. **Rättigheter:** repo ber att originalkoden inte distribueras vidare; detta paket innehåller ingen tredjepartskod. [C02]
3. **Combat (Larry Wagner; kommenterad disassembly läst).** Resurs- och spelvarianttabeller, R/L rotations-/kolisionsrutiner (`COLIS`, `ROT`), `VDELP0,X`, `CXM0FB,X`, `CXPPMM` runt rader 221/717/1059/1184. **Överförbart:** små tillståndsmaskiner, ballistiska/hindertriggers och separata visningsfaser. **Inte överförbart:** två spelare och enklare fastställda scenkrav gör det inte till ett tre-fiender+halo-bevis. [C03]
4. **River Raid (Carol Shaw; Thomas Jentzsch disassembly läst).** Källhuvudet specificerar 160-raders kernel; 32-raders block, vardera 12×2 rasterrader +8 ledning. Objekt- och PF-pekare med prioritet/färg/REFP; `DisplayKernel` från ca rad 518 och `VDELP1` runt 387. **Överförbart:** verkligt välavvägd multi-kernel/blockarkitektur där sysslor flyttas till blockgränser. **Begränsning:** endast ett huvudsakligt objekt per flodblock enligt kommentar och fiendernas spatiala frihet inte samma som The Skrauns. [C04]
5. **Pitfall! (David Crane; Jentzsch disassembly läst).** Källkommentar anger *nio* specialiserade display-kernelloopar under en bild; mellan ungefär rad 480–810 syns många skeden för lian, förgrundsobjekt, Harry och gropar. **Överförbart:** specialiserade korta kernels framför en enda generaliserad som gör allting på alla rader. **Begränsning:** förutbestämd vertikal scenstruktur, inte tre fritt jagande fiender och stor cirkel. [C05]
6. **Adventure (Warren Robinett; kommenterad disassembly läst).** Vid omkring rad 56–70 positioneras P0/P1/Ball och HMOVE; `VDEL01` runt rad 87; väggmissiles ENAM0/ENAM1 kring 289/291; kring 821–833 läses ball-PF/missile collision. **Överförbart:** konkret pixelresursåteranvändning och objektsstatus. **Begränsning:** världen och fiendefärgerna uttrycks inte med Skrauns rörliga halo. [C06]
7. **Raiders of the Lost Ark (Howard Scott Warshaw; Halkun disassembly läst).** Rumsberoende state i RAM: `kernelRenderState` $d4, `p0DrawStartLine` $e0, PF-pekare $e1–$e4, `dynamicGfxData` och blockdata $e5–. **Överförbart:** rumsspecifik kernel-/resursuppdelning, RAM-livstider som varierar med rum. **Begränsning:** rumstyper är inte samma som tre överlappande fritt rörliga karaktärer. [C07]
8. **8bitworkshop Versatile Playfield Kernel (Steven Hugg, 2025; kodexempel läst).** `LDA (pointer),Y`, `TAX`, därefter `STA $00,X` med [adress, värde]-par; uppdaterar en PF-/färgreg per två linjer, uppgiven upp till 9 cykler/rad. **Överförbart:** glesa registerändringar, om ett faktiskt PF-kompositionsverktyg kan uppfylla geometri. **Begränsning:** begränsning i antal registerbyten och retroaktiv ringens högsta nyansering. [C10]
9. **8bitworkshop Three-Stream Versatile Kernel (Hugg, 2025; kodexempel läst).** `dlist1`/`dlist2` och tredje PF-flöde; zero-terminerad sekvens väljer nästa segment; 3 registerändringar/rad; 32 byte per dlist i exemplet och författaren varnar för tearing. **Överförbart:** explicit resursägarskap och move-sekvens som data. **Begränsning:** RAM/tearing och svåra X-repositioneringar. [C11]
10. **Space Invaders (Atari original; historisk mekanism, modern klon identifierad).** NUSIZ kan ge extra identiska kopior i fasta X-avstånd. Modern `Julio-Rats`-ASM finns och ska inte misstas för Ataris original. **Överförbart:** massor av identiska fiender; **inte** fritt placerade riddare och bågskytt. Original 2600-kodens exakta instruktioner inte granskade i denna körning. [C08]
11. **Video Chess / Kovi Kovi (historisk programmerarhistoria respektive utvecklartråd).** Dokumenterad intra-frame Venetian, för Kovi med E7 self-modifying kernel och interlace. **Överförbart:** synlighetskompromiss inom samma bildruta snarare än 20Hz helframe. **Begränsning:** tillgänglig källa här är dokumentär/forum, inte en genomläst originalassembler för dessa två fall. [T05][T06]

**Ytterligare kontrollerade index men ännu inte koddjupgranskade:** Berzerk, River Raid alternativa versioner, Space Invaders original, 6502-disassembly-katalog. De får inte tillskrivas opublicerade instruktioner eller mätvärden. [C09]

## Del VI. Fem alternativa helspelsarkitekturer

**Gemensam adversarial worst case (måste gälla alla):** U1-LEG1 L3 32×36; aktiv L3-halo; minst tre fiender på exakt samma Y, med oberoende X; riddare med telegraph + bågskytt som skjuter; pil och orb; solida hinder som samtidigt syns skilda från guld; score+liv; full joystick och AI; bild i NTSC utan overrun. Att flytta isär fiender vertikalt är inte godkänt.

| Motor | Grafik/fiender | CPU/schemaläggning | RAM/ROM | Flimmer/läsbarhet | Kompatibilitet/risk |
|---|---|---|---|---|---|
| **A Traditionell PF + P1, optimerad R3** | Samma 20Hz same-Y och PF-färggrundproblem om ingen principiell ändring | R3 72–74/76 avgörande rader | 112B R3 RIOT; ROM-masker stora | Mycket hög risk | Vanlig 2600, men **NO-GO** för direkta fortsättningen |
| **B Specialized multikernels + sparse PF** | P0 alltid, P1 fiender, PF-halo, statiska hinder i separat metod måste konstrueras | Tar bort onödiga PF-writes, dedikerad HUD, hårda överlapp ändå svåra | Kan ersätta P1Buf med kortare segment; kräver liveness och ring-compiler | Hög risk när tre same-Y | Vanlig 2600; **preliminärt förstahandsforskningsspår** |
| **C Tre-ströms display lists** | PF/P0/P1 flöden, rörliga sprites men bara 3 writes/scanline i exemplet | Uppgivet inga fria dolda skrivslots på kritiska rader; tear-risk | 32B×2 dlist; kan inte adderas till R3:s 112B utan omskrivning | Kritisk läsbarhetsrisk | Vanlig 2600; sannolikt stort ombyggnadsarbete |
| **D Venetian-enemy + multikernel** | P1-fiender interfolieras mellan scanlines för alla samtidiga aktörer; P0 fortfarande hel | Extra P1-bitmap- och repositioneringsstrob, eventuella glapp | Litet/medel, beror på radscheduler | Ingen helframe-20Hz nödvändigt men 2/3 vertikal pixelandel för tre; visuellt oprövat | Vanlig 2600 i enkel form; E7-version kräver ny cartridge |
| **E Hårdvaruassisterad cart** | Mer dataströmmar/extra RAM kan avlasta prep men samma TIA-register | ARM kan beräkna men skrivdeadlines kvarstår | F6SC 128B extra; E7 större RAM; DPC+/CDF ny mapper/driver | Möjlig förbättring, **inte bevisad** färg/fiendelösning | Kräver explicit val och kompatibilitetsprov för Stella/RetroN77/fysisk konsol |

**Färgbudgetens falsifierande test:** Om halo och hinder båda ligger i en och samma PF-plan, och båda är på samma rasterrad, delar de vid varje given punkt register `COLUPF`. Om de måste synas två olika färger på samma scanline under överlapp kan en enda PF-plan inte uppfylla det med en konstant COLUPF; mitt-i-linjen-färgbyte skulle bara dela färgzonen geometriskt, inte ge oberoende mask för bägge. En andra ritresurs eller accepterad bildkompromiss krävs. Detta är härlett ur hårdvaruspecen, inte en optisk smakfråga. [T01]

**Störst risk i alla A–D:** att ett hypotetiskt större 8/16/32K-bygge löser ROM-data men inte fysiskt möjliggör 4 karaktärer + två grafiklager på samma rasterrad. Inget antagande om PAL-50 med fler totala lines får maskera att PAL fortfarande har 76 cycles per fysisk scanline.

## Del VII. Rangordnat vägval till MAIN

**Rekommendera ännu inte någon produktionskernel.** Den bästa första forskningsarkitekturen är **B + en snäv del av D**, eftersom Hugg och historisk *Pitfall/River Raid* visar två *andra* sätt att reducera överflödigt TIA-arbete. Men att klara minst tre P1-aktörer same-Y i läsbart skick och samtidig halo/hinder skiljer en bra renderer från en attraktiv demo. Vi behöver två **korta, målmedvetna avgörande testkontrakt** som MAIN kan välja att auktorisera efter genomgång av pågående P01-COL1.

Välj **inte** mapperbyte som första reaktion. F6/F8 är rimligt när ROM-tabeller faktiskt blir större än 4K; Superchip endast om RAM-liveness motiverar det; ARM/CDFJ inte förrän man har en reproducerbar och kvantifierad 6507-vinst och distributörskompatibilitet. Stella listar DPC+/CDF-versioner, men det är *inte* en uppmätt RetroN77-garanti. [T07][T11][T12]

## Del VIII. Rekommenderad experimentplan (förslag, INTE auktorisation)

### Gate 0 — kontrollera P01-COL1, inga parallella kopior

**Befintligt auktoriserat:** P0-only 4K NTSC kroppskollision, 8-vägs glidning, växande L3, fryst U1-LEG1, riktiga Stella/DASM/loggar. GitHub issue #24 OPEN vid kontroll; ingen färdig ROM i det kontrollerade underlaget. RESEARCH föreslår ingen ny egen COL1-gren. [P09][P10]

### Gate 1 — PF-registerändringsrepresenterbarhet (SOURCE-ONLY, kan analyseras utan implementation)

**Hypotes:** tillåtna rörelser av full halo + tre välseparerade solida hinder kan komprimeras till högst en PF-registernyuppdatering per 2 scanlines på merparten av raderna, utan att förstöra separata färgobjekt. **Input:** verkliga källmasker/geom. för X56, X80, X104 och worst-case X+Y, L3, P0 och 3 same-Y P1 aktörer. **Mät:** antalet unika PF0/PF1/PF2-värdebyten per scanline och skrivdeadlines; beräkna om 1/2-linjers och 3-stream-regel kan ge samma bild. **Negativ kontroll:** konstruerad ring/hinder-konflikt där PF0+PF1+PF2 behöver uppdateras samma 2-radersfönster. **PASS:** alla faktiska källmasker kan renderas exakt och med bevarad distinkt färg utan orealistiska writes; **FAIL:** någon konfiguration kräver fler samtidiga PF-registeruppdateringar eller ytterligare färgplan än tillåtet. **MAIN följd:** vid FAIL avvisa den varianten innan ROM-tid spenderas; pröva nästa arkitektur. Inga Stella-bilder kan ersätta detta dataprov.

### Gate 2 — samma-Y-P1-vapenläsbarhet: Venetian kontra 20Hz fullframe (ny ROM endast om separat MAIN-auktoriserad)

**Hypotes:** tre individuella P1-aktörer med samma Y men olika X kan ha bättre användbar förvarning med scanline-interleave än med R3 20Hz frame duty. **Samma scen:** exakt U1-LEG1 P0/3 storlekar, två urskiljbara riddare med upphöjt svärd, grön bågskytt med båge, från riktiga tillåtna masks, tätt överlapp både vid arena och P0. **Gör jämförelse:** R3 4/12 vs 1/2- och 1/3-line duty med 12 sekventiella frames; alla X-permutationer inkl. nära/nära/långt; samma halo+hindermask **måste vara aktiv** i slutligt stressprov. **Mät:** faktisk scanline-by-scanline GRP/COLUP/PF/RESP/HMOVE deadlines, 6507 instruktionscykler, använd RAM/stack/ROM och 262 lines; exakta per-fiende pixlar och vapenförvarning i 12-frame gif + 4:3. **Negativ kontroll:** deliberately övertrassera cycle budget/telegraf och säkra att testen blir FAIL. **PASS:** ingen missad 0,4s varningsfas/fiende, konstgjorda X-begränsningar krävs inte, grafiken identifierbar i faktisk storlek och inga frame/rasteroverruns; **FAIL:** fiender osynliga/oläsliga på aktiva raster, oönskad 20Hz plötsligt kvar, deadline missas eller P0/PF korrupt. Då återstår explicit användarbeslut om tolererad flimmerkompromiss eller alternativa mekaniker/hårdvara; inte automatic R4.

### Gate 3 — halo + hinder i två distinkta färger, worst-case

**Hypotes:** en fysisk frame kan visa rörlig L3-guldhalo, tre solida hinder och tre fiender utan att samma PF-mask får samma färg i gemensamma pixlar. Jämför metod 1 separata resurser (PF-guld + annan visual/zon för hinder), metod 2 gles-PF med annan explicit pixelrepresentation, metod 3 annan beräknad understruktur. **Mät:** autentisk TIA-pixelvis RGB/scanlines över 12 frames; exakta PF-mask- och COLUP* writes; CPU- och RAM-lek; även logisk soliditet separat från ritning. **Negativ kontroll:** original R3 'OR sammanfogning' där hinder är guld och R3 30Hz frame-separation. Båda SKA ge FAIL i färgkravet. **PASS:** obruten guldattack, hinder visuellt tydliga och separat färgade samma frames där overlap verkligen sker, pilar/svärd stoppas medan halo går igenom. **FAIL:** 30Hz uppdelning, gemensam färg, sprites försvinner eller minsta ny registerdeadlines bryts.

### Gate 4 — helscens-RAM/CPU/scopegrind före eventuell engine cutover

Om och endast om Gate 2–3 lyckas i bounded tests: kombinera riktig rörelse+COL1-resultat, AI-states, en pil, orb, två riddare, bågskytt, HUD/liv/score och ljud i worst-case. Kräv **verklig** per-raster och blank-period trace, 128-byte live-RAM/stacktabell, 4K/8K/F8/F6 budget per bank och PAL/NTSC separat. **Negativ kontroll:** same-Y tre aktörer + pilen mitt i halo + L3 vid kanten samtidigt och med hörnglidning. **PASS:** alla synlighetskontrakt och logiska mekaniker utan övertramp samt tolerabelt faktiska bilder/TV; **FAIL:** inget huvudprogrambeslut. MAIN auktoriserar varje fortsättning separat.

## Del IX. Varningar – frestande men fel spår

- Släpp inte in R3 som huvudkernel bara för att enbart 262 scanlines och tre ROM-hashar är korrekta.
- Sänk inte level3-sprite, halo-reach, spelares hastighet eller hinderantal i hemlighet.
- Använd inte skilda Y-band som garantier om fiende-AI fortfarande tillåter full positionering.
- Kalla inte 30Hz/20Hz vackra stillbilder för en felfri animation; kontrollera konsekutiva rasterframes och fysisk skärmrenders.
- Påstå inte att PF och ball ger två självständiga färgplan; de delar färgregister.
- Lägg inte på dlist 64B ovanpå R3:s 112B utan att först kasta om RAM-arkitekturen.
- Flytta inte beräkningar till VBLANK om tillgänglig blank-budget inte är mätt, och flytta framför allt inte extra STA till en rasterrad med 2 cykler kvar.
- Anta inte DPC+/CDF+/E7 emulatorstöd för RetroN77 utan praktisk kontroll; stöd i Stella är en annan fråga.
- Kopiera inte källkod från Pacman4K in i spelet; repo reserverar återpubliceringsrätt och projektet ska respektera licenser.
- Återtolka inte produktion eller independ. VERIFICATION som utförd bara för att researchdokument är stort.

## Del X. Kort handoff till MAIN

**Viktigaste nya fynd:** 2025 års verifierbart publicerade *versatile PF*- och *three-stream*-kernels erbjuder en principiellt annan tidsfördelning än R3:s fixerade PF-uppdateringar; historisk Venetian kan ge en kandidat till bättre same-Y-fiendesynlighet. Inga av dem är nu ett Skraun-PASS.

**Testa först i research:** SOURCE-ONLY analyserad PF-registerändringsrepresenterbarhet på exakta masker och värtfall. Den har högst förmåga att *billigt diskvalificera* en falsk lösning. **Första nya ROM-försök för MAIN att överväga:** en avgränsad P1 same-Y Venetian-vs-R3-jämförelse, bara om resultaten kan mätas med oförändrad U1-LEG1 och samtidiga hinder/halo. Ingen ny ROM auktoriseras av rapporten.

**Mest konkreta kodförebilder:** *River Raid* och *Pitfall!* för verkliga multikernels; *Cyloid* för faktisk P0/P1/M0/PF-ägarskap och färdig ASM; Huggs 2025-kernels för data-driven registerplanering. **Reserv:** originalkompatibel P1-line-interleave med strikt synlighetskrav, sedan separat hårdvarustudie.

**Kvarstående STOP-villkor:** tre fritt placerade fiender på samma Y, same-frame olika färger för halo/hinder, 76 cykler/rad, 128 bytes inklusive stack, P01-COL1 och #19/#15/#1 acceptansgrindar. **Ingen gameplaykompromiss eller teknisk cutover är implicit godkänd.**

### Käll- och evidensnot

Referenser [Pxx], [Txx] och [Cxx] ovan pekar på exakta lästa eller observerade källor i `KALLREGISTER.csv`. En post som anges 'index/sökresultat' är medvetet **inte** behandlad som läst assembler. Söklogg och källstatus möjliggör kritisk eftergranskning. Den bifogade matrisen är rådgivande och innehåller inga påhittade per-instruktionsmätningar.


**Tillägg:** För direktklickbara radreferenser i faktiskt läst historisk assembler, se `KODSTUDIER_EXAKTA_RADER.md`.