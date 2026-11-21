# THE SKRAUN – MAIN, samlad design- och beslutslogg 01–60

**Datum:** 2026-11-16  
**Plattform:** Atari 2600 (originalkompatibel hårdvara som mål)  
**Status:** Designbeslut, **inte** bevis på fungerande ROM eller teknisk verifiering  
**Underlag:** Överlämningsrapporten `Inklistrad text.txt` (beslut 01–19), senare beslut i samma chatt (20–37) och användarens uttryckliga delegation att MAIN får följa egna rekommendationer (38–60).

## Styrande designprinciper

1. The Skraun är ett snabbt, ovanifrån sett arkadspel: fyrfotat troll mot jagande riddare och en grön, flyende bågskytt per bana.
2. **Level 1 är svårt; level 2 medelsvårt; level 3 ska kännas övermäktigt (OP).** Ingen automatisk skalning av fiendestyrka för att neutralisera detta.
3. Åtta banor i fyra världar: skog (1–2), berg (3–4), drömvärld (5–6), mörk nattvärld (7–8).
4. Hårdvarutrogen Atari 2600-grafik – inga löften om NES-liknande detaljnivå, flimmerfrihet eller fullständig genomförbarhet innan ROM-tester.
5. Research och designbeslut skiljs från implementation och oberoende verifiering.

## Tidigare fastställda beslut 01–19 (från överlämningsrapporten)

| Nr | Beslut |
|---|---|
| 01 | Symmetriskt fyrfotat troll; ingen klubba; i stället magisk 360° haloattack. |
| 02 | Kortare attackåterhämtning med stigande trolllevel. |
| 03 | Tjockare halo och större yttre räckvidd med stigande level. |
| 04 | Halon förstör pilar på samtliga levels. |
| 05 | En träff sänker level med ett steg; träff på level 1 kostar ett liv. |
| 06 | Tre startliv; fler liv kan ges av poäng. |
| 07 | Vid livsförlust fortsätter samma bana; besegrade fiender förblir besegrade. |
| 08 | En orb på varje bana kan samlas in högst en gång under det banbesöket; ingen återkomst efter livsförlust. |
| 09 | Trollets level bibehålls mellan banor. |
| 10 | Cirka en sekunds blinkande osårbarhet efter träff. |
| 11 | Halon är aktiv i cirka 0,5 sekunder. |
| 12 | Trollet får röra sig fritt under aktiv halo. |
| 13 | Riddare orsakar skada med svärdshugg; kroppskontakt räcker inte. |
| 14 | Bågskyttens pil riktas mot trollets position vid avfyrningen; den är inte målsökande. |
| 15 | Skottintervall för bågskytten per värld: skog ~3 s; berg ~2,5 s; dröm ~2 s; natt ~1,5 s. |
| 16 | Bågskytten försöker fly när trollet närmar sig. |
| 17 | Riddare per bana: skog 2, berg 2, dröm 3, natt 4. En bågskytt på varje bana. |
| 18 | Högst två aktiva riddare samtidigt; banan är klar först efter att samtliga riddare och bågskytten har besegrats. |
| 19 | En extra riddare kommer efter ~2 s från en skärmkant, på rimligt avstånd från trollet, när plats frigjorts. |

## Tidigare beslut 20–37 (direkta användarval i denna chatt)

| Nr | Beslut |
|---|---|
| 20 | Trollet springer lika snabbt på alla tre levels. |
| 21 | Riddare rör sig något långsammare än trollet. |
| 22 | Före hugget stannar riddaren och höjer svärdet i ~0,4 s. |
| 23 | Efter hugget behöver riddaren ~1,0 s återhämtning före nästa förvarning/hugg. |
| 24 | Högst en pil i luften. En ny pil kräver både att föregående försvunnit och att skottintervallet löpt ut. |
| 25 | Medelsnabb pilhastighet som inte ökar mellan världarna; exakt värde via speltest. |
| 26 | Orben ligger kvar om trollet redan är level 3; den kan samlas in efter eventuell nedgång till level 2. |
| 27 | Orben placeras varierande bland ett fåtal i förväg bestämda, synliga, säkra, nåbara platser. |
| 28 | Riddare 100 poäng; grön bågskytt 250 poäng; samma värden i alla världar. |
| 29 | Ett extraliv vid varje nytt 2 000-poängssteg (2 000, 4 000, osv.). |
| 30 | Efter livsförlust återuppstår trollet på banans fasta, normalt säkra startposition på level 1 med ~1 s osårbarhet. |
| 31 | Automatisk övergång efter sista fienden, med kort effekt och ~2 s till nästa bana. |
| 32 | Oändlig loop utan extra svårighet: 1→2→…→8, sedan 8→7→…→1, sedan 1→2→…→8 osv. Ändbanorna spelas igen vid vändningen. Level, liv och poäng bibehålls. |
| 33 | Varje bana får ett fåtal solida miljöhinder (t.ex. träd, stenar, formationer, ruiner). |
| 34 | Solida hinder stoppar bågskyttens pilar. |
| 35 | Trollets magiska halo passerar genom hinder och kan träffa fiender bakom dem inom räckvidden. |
| 36 | Solida hinder stoppar riddarnas svärdshugg. |
| 37 | Riddare använder enkel hinderundvikning och fortsätter förföljelsen när vägen är fri. |

## MAIN:s delegerade designbeslut 38–60

Dessa val är gjorda med användarens uttryckliga delegation att MAIN får fortsätta enligt egna rekommendationer, utan att fråga om varje detalj. De är designmål; en teknisk reservation anges separat där det krävs.

| Nr | Beslut | Motiv / reservation |
|---|---|---|
| **38** | Bågskytten använder samma typ av enkla undanmanöver runt hinder som riddarna, men rör sig huvudsakligen bort från trollet. | Dela så mycket AI-logik som möjligt. |
| **39** | Bågskytten försöker söka fri skottlinje och byta position om hinder skymmer. | *Tekniskt oprövat:* enklaste tillräckliga siktkontroll måste provas; ingen avancerad vägplanering får antas gratis. |
| **40** | Bågskytten är något långsammare än trollet och gör ett kort stopp i samband med skott. | Ska gå att hinna ikapp; skottet riktas alltjämt mot trollets position vid **avfyrning**, inte före stoppet. |
| **41** | En pil avlägsnas när den träffar trollet, aktiv halo, solitt hinder eller skärmkanten. | Samma projektilobjekt kan då återanvändas. |
| **42** | Pilens riktning och rörelsevektor är fixerade från avfyrning till att den försvinner. | Bekräftar att inga målsökande pilar finns. |
| **43** | Riddarens huggriktning låses vid start av svärdets ~0,4 s förvarning. | Spelaren får möjlighet att väja undan. |
| **44** | Riddarens svärd orsakar skada endast under ett kort aktivt huggfönster, inte under förvarning eller återhämtning. | Behåll tydlig telegraph/attack/återhämtning. Exakt fönster speltestas. |
| **45** | Fiender kan inte skada varandra och blockerar inte varandra fysiskt. | Undvik AI-låsningar; enkel visuell separation får läggas till om den är billig. |
| **46** | Trollet kan röra sig i åtta riktningar med joystick; diagonal rörelse ska inte ge oskälig hastighetsfördel. | Diskret, enkel hastighetsutjämning; inte flyttal. |
| **47** | Tre tydliga trollstorlekar behåller samma silhuett och identitet; ögon/bakben och halo anpassas men mängden detaljer hålls hårdvarutrogen. | Hårdvarutest behövs för tydliga, olika stora figurer. |
| **48** | Första speltestvärdena för återhämtning **efter** halons 0,5 s aktiva tid: level 1 ~1,0 s, level 2 ~0,6 s, level 3 ~0,25 s. | *Preliminära balanseringsvärden*; level 3 får hög attackfrekvens och ska kännas OP. |
| **49** | Hålls joystickknappen nere aktiveras en ny halo så snart den föregående attacken och återhämtningen är klara. | Kräver inte upprepat knapphamrande. |
| **50** | Under den ~1 s långa osårbarheten kan trollet fortfarande röra sig och attackera, men inte förlora ytterligare level/liv. | Undviker att begränsa spelkontrollen efter skada. |
| **51** | Banans orb syns från banstart, kan samlas in via kontakt på level 1–2 och ligger kvar om trollet är level 3. | Överensstämmer med tidigare beslut; ingen fiendedöd krävs för att orben ska synas. |
| **52** | Vid banstart placeras de två första riddarna och bågskytten på förutbestämda platser på avstånd från trollet; reserverade riddare följer tvåsekundersregeln. Vid livsförlust återplaceras enbart överlevande fiender säkert. | Säker återstart utan att återuppliva besegrade fiender. |
| **53** | En ännu ej tagen orb kan plockas upp under den ~2 s långa banövergången om spelaren hinner; vid övergången försvinner oanvänd orb. | Ingen automatisk gratisuppgradering; spelaren väljer när den hämtas. |
| **54** | Åtta fasta, distinkta banlayouter med få hinder; slumpvariationen begränsas i första hand till orbens i förväg utvalda positioner. | Förutsägbar AI och minnesbudget. |
| **55** | Trollet stoppas av solida hinder; vid diagonal rörelse ska det om möjligt kunna glida längs en fri kant i stället för att fastna helt. | Kräver test av kollisionslogik. |
| **56** | Spelets HUD prioriterar läsbar **poängsumma och antal liv**. Trollets level ska i första hand synas på dess storlek/halo; banbyte kan visa kort banindikator. | Undvik ett överlastat grafiskt gränssnitt. |
| **57** | Tydliga korta ljudeffekter för halo, träff, besegrad fiende, orb och extraliv. Kort jingle vid banbyte; ingen kontinuerlig bakgrundsmusik under aktiv strid. | TIA:s två ljudkanaler används med prioritering av viktigaste effekten. |
| **58** | När sista livet är slut visas enkel GAME OVER-indikering och slutpoäng; eldknapp eller konsolens RESET startar en ny omgång. | Snabb arkadmässig omstart. |
| **59** | God läsbarhet prioriteras i alla världar, särskilt i nattvärlden. Trollet, aktiva svärdshugg, pil och halo måste vara läsbara; undvik störande konstant flimmer. | En teknisk ambition, **inte** ett löfte om flimmerfri grafik. |
| **60** | Varje gång en bana besöks på nytt, även då bana 8 eller 1 omedelbart upprepas vid vändning, startas dess fiender och orb om för **det nya banbesöket**. Trollets level, liv och poäng bibehålls. | Annars skulle återbesökta banor vara tomma, vilket strider mot den oändliga arkadloopen. |

## Konsistens och viktiga följdregler

- Bågskyttens skottintervall räknas från senaste **avfyrning**. Nästa skott kräver att intervallet har gått ut, att föregående pil har försvunnit och, enligt beslut 39, en användbar skottlinje.
- Bågskyttens korta stopp inför skott får inte låsa siktpunkten i förväg: målet registreras när pilen **lämnar** bågskytten.
- När banan väl är avslutad startar övergången enligt beslut 31; kvarvarande orb får inte föras över till nästa bana.
- Livsförlust på pågående bana återställer **inte** besegrade fiender eller förbrukad orb. Nytt banbesök vid ordinarie banövergång återställer däremot båda.
- Ingen ökning av fiendehastighet, skottfrekvens, antal fiender eller poängvärden bara för att spelaren har vänt banordningen. Den ursprungliga världsskillnaden består: skog är som skog och natt är som natt.
- De korta tidsvärdena är designparametrar för test, inte verifierade slutvärden.

## Tekniska osäkerheter och föreslagen testordning

**Hög risk – ingen produktionsimplementering bör påstås vara bevisad:**

1. Rörligt troll med tre storlekar, igenkännbara bakben/ögon och 360° flerfärgad halo som även omsluter stora trollformen.
2. Samtidig presentation av troll + två riddare + grön bågskytt + orb + pil (+ halo); detta överstiger antalet oberoende TIA-player-sprites. Sprite-multiplexering/alternativ grafik och acceptabelt flimmer måste provas.
3. Visuellt sammanfall mellan haloringens räckvidd och dess träffdetektering, även genom solida hinder.
4. Riddarnas och bågskyttens hinderundvikning och bågskyttens skottlinje utan att överskrida tids-/RAM-budgeten.
5. Korrekt och konsekvent visning av nattvärldens kontrast, halo/blink och poäng-/livindikator på verklig hårdvara.

**Föreslagen arbetsordning (inte påstående om utförd implementation):**

A. Statisk hårdvarutrogen trollgrafik på alla tre levels och enkel rörelse.  
B. Halo – grafik separat från kollisionslogik; därefter sammanslagning.  
C. Fyra karaktärer + pil + orb + fasta hinder på en provskärm.  
D. Rörelse, hinderundvikning, svärd och pil; mät processorcykler/scanlines och RAM.  
E. Leveloppning, övergång, poäng/liv och fram-/bakvänd banloop.  
F. Oberoende verifiering i emulator och på riktig Atari 2600-kompatibel hårdvara, inklusive relevanta NTSC/PAL-varianter.

## Källstöd för tekniska reservationer

- *Stella Programmer's Guide*, historisk TIA-/kärneldokumentation: https://www.atariage.com/2600/programming/2600_101/docs/stella.html
- Atari Compendium, plattformens specifikationer och bank-switching: https://www.ataricompendium.com/faq/faq.html
- Game Developer, intervju med Champ Games om modern Atari 2600-programmering och extra cartridge-hårdvara: https://www.gamedeveloper.com/programming/how-champ-games-tricks-old-hardware-with-new-cartridges-on-the-atari-2600
- Batari Basic manual (som dokumentation av TIA-objekt/multisprite-begränsningar, inte som beslut om programspråk): https://www.randomterrain.com/bb_files/atari-2600-memories-batari-basic-commands.html

**Gränsdragning:** Designbeslut 38–60 har fattats inom delegerat scope. Inget har skrivits, assemblerats eller verifierats som körbar ROM i denna genomgång. Exakta cykelbudgetar, grafikmetod, joystickrespons och nivåbalans är fortfarande öppna för tekniska test och speltest.

## SENARE ANVÄNDARKORRIGERING TILL BESLUT 01: TROLLETS UPPRÄTTA SPRITE (2026-11-16)

**ÄNDRINGSNOT, bevarar den historiska tabellen oförändrad:** Användaren förtydligade uttryckligen efter P1/P2 att spelplanen fortfarande är sedd ovanifrån men **Skraun ska hela tiden stå upprätt**, alltså ingen kropp som ligger i horisontell djur-/fyrfotalayout. Huvud med horn/ögon/mun uppe i den stående figuren, armar åt sidorna, ben/fötter nedåt. Figuren har **två** visuella facings, vänster/höger som exakt spegel, oavsett joystickens åtta rörelseriktningar; vertikal rörelse får inte rotera figuren eller kräva separat up/down-sprite.

Den gamla beslut 01-frasen **"fyrfotat troll"** får därmed **inte användas som krav på liggande quadruped/fyra tassar runt en horisontell rygg**. Denna senare direkta användarkorrigering har företräde för **visuell kroppshållning och perspektivtolkning**. Beslut 01:s magiska 360° halo, övriga spelregler och alla gamla oförändrade källfiler består. Världen är fortfarande overhead, men ett stiliserat upprätt trollansikte behöver inte ritas som om även ansiktet måste fotograferas optiskt exakt från 90 grader ovanför.

[Uppdaterad visuell riktning](SKRAUN_VISUAL_DIRECTION_2026-11-16.md) och [MAIN II:s detaljerade GRAPHICS P3-beslut](MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md). Ingen ny sprite, mer ROM eller dimension är härmed godkänd.

## Kompletterande uttryckligt användarkrav efter beslut 01–60: framkomliga banor även på nivå 3 (2026-11-16)

Användaren skrev uttryckligen: **"ok, fortsätt. Tänk på att banorna ska vara så pass fria att spelaren kan röra sig lätt även på nivå 3, utan att krocka och fastna överallt"**.

**Bindande komplettering**, i samma gameplayautoritet som tidigare användarbeslut, till #33 (få solida hinder), #46 (8 riktningar), #47 (tre storlekar), #51/52 (orb och säkra startpositioner), #54 (8 fasta olika banor) och särskilt #55 (glid längs fri kant). **Samtliga åtta banor ska ha gott om öppet strids- och rörelseutrymme för det största trollet på nivå 3, inte bara för nivå 1.** Inga obligatoriska trånga öppningar, onödiga återvändsfickor, ständiga hörnfastningar eller orbplaceringar där en spelare övergår från nivå 2 till nivå 3 och hamnar inne i solid geometri. Vid diagonal rörelse ska en fri axel fortsatt kunna ge glidning runt hinder. Bevara hinder som verkligt solida, magisk haloring genom hinder och full nivå-3-storlek/styrka – lös problemet med banornas öppna layout och korrekt kollisionsbeteende, inte med dold nergradering.

**Viktigt statusförbehåll:** Exakta åtta kanoniska hinderkartor och faktisk hinderkollision är ännu inte färdiga/testade. [MAIN II:s fullständiga nya design-/acceptansgrind](MAIN_II_LEVEL3_ARENA_FREE_MOVEMENT_AND_COLLISION_GATE_2026-11-16.md) innehåller enbart **preliminära** planeringsmått (32×36 konceptuell figur, testmarginal 4 vardera sidan → cirka 40 enheter bred eller 44 rader hög fri passage), inte ett fastställt framtida kollisionshitbox-beslut. Referens-Pythonprov på tre **syntetiska** 160×176-geometrier avslöjar trånga nivå-3-hinder och tillväxtfällor men verifierar inga riktiga spelbanor. [Tracking #23](https://github.com/Odourman/the-skraun/issues/23) öppet. Ingen ny ROM, Stella, collision implementation eller global art/verifierings-GO implicit auktoriserad.


## Nyare användarbeslut — 2026-11-21: Ranger med världskamouflage

**Bindande senare användarförtydligande till tidigare "grön bågskytt":** Bågskytten är en **Ranger som avsiktligt gömmer sig i miljön**, och hans färg ska följa världen. Användarens exempel: **grön i skogen, lila som spiralerna i drömvärlden**. Den gamla formuleringen om *alltid grön* får därför bara gälla skogsvärlden, inte de övriga. Färgvalen för berg/natt och exakta TIA-koder är ännu design-/Stella-testkandidater, inte låsta godkännanden. Inga gameplay-, AI-, skott-, kollision-, svärdsvarnings-, grafikkvalitets-, artwork- eller mapperkrav ändras av denna färgändring.

Se [exakt användarbeslut och avgränsning](MAIN_III_USER_DECISION_RANGER_WORLD_CAMOUFLAGE_2026-11-21.md) och [N6 source-only färg-/objektarkitektur](MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md). N6 har ingen godkänd integrerad original-TIA kernel, och detta beslut ger ingen ROM- eller independent Verification-autorisering.

## Nyare användarbekräftad inriktning — 2026-11-21: N6 jämförelse av halo, ljusblå riddare och svärdsposer

**Auktoritet:** Efter användarens konkreta punkt 1–7 om tekniskt billigaste halo, ljusblå rustning, separat svärd eller animation, tre samtidiga fiender, magiskt färgskiftande orb, statiska spiraler och möjlig mindre höjd på L2/L3 svarade användaren: **"Ja, bra. Följ dina rekommendationer. Det låter bra!"**.

**Nya bekräftade designriktningar:** Föredra **ljusblå riddarrustning** framför äldre röd som framtida kandidat; de två riddarna ska som första tekniska test ha **samma exakta ljusblå TIA-värde**. Bevara två samtidiga riddare + en världskamouflerad ranger tills ett annat verkligt tekniskt bevis och nytt användarbeslut motiverar ändring. **Svärd i riddarens egna P1-animationsposer** testas före egen M1-linje; träffar är logiska och bara aktiva under hugget; ~0,4 s tydlig förvarning oförändrad. **Haloform optimeras** utifrån verkliga PF-skrivningar och synlig attackradie utan krav på helt rund konst. **Enkel liten orb** prövas med världsfärg under inaktiv halo och guld vid aktiv halo, med eventuell tydlig effektblinkning. **Drömspiraler statiska.** Få enkla PF-hinder och öppna åtta banor fortsatt.

**Fortfarande testkandidater, inte godkända nya slutvärden:** exakt ljusblå TIA-nyans, slutlig halokontur, alternativ BL-orb-glimt, M1-svärdslinje, alternative L2 16×20 och L3 32×30 gentemot ursprunglig plan 16×24 och 32×36. Original U1-LEG1 8×12 A/B för L1 är fortfarande godkänd och fryst. **Användarens godkännande av fortsatt N6-jämförelse är inte godkännande av en ny assemblerad ROM, N7, ny art eller oberoende Verification.**

Se [exakt N6 jämförelse- och STOP-kontrakt](MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md), [N6 teknik-/meleegrund](MAIN_III_N6_USER_FEEDBACK_MELEE_SWORD_REFERENCE_AND_CREATIVE_TEST_MATRIX_2026-11-21.md) och [B guldfärgad arena-PF](MAIN_III_N6_B_GOLD_PLAYFIELD_CREATIVE_REVIEW_2026-11-21.md). Den gamla röda R3-diagnostiken är fortsatt historiskt sann, men styr inte den nya framtida ljusblå färgtestkandidaten.
