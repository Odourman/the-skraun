# The Skraun · del B · MAIN VI

**DEVELOPER_OBSERVED. B2 rekommenderas för MAIN-granskning och användarens visuella speltest.**

B2 integrerar den godkända sköldkonturen, båda gångposerna, varning och hugg samt åtta nya playfield-tabeller. Samtliga ändrade ROM-byten är i bank 3. Banks 0–2 är byteidentiska med PR77, inklusive träffmodell, orb, spelregler och ljudmotor.

| Version | Kodcommit | SHA-256 för ROM |
|---|---|---|
| PR77 accepterad bas | `37dc1cc7f354b0382d32778025f121037ade9684` | `39bab1bd354f8dfdfd8d179e4f4ba3299c0a6a35f8e3ab634e8d2fcde1475168` |
| B1 reserv | `b5eb82195c5f74718c0823a91666012802f28912` | `1ceab1fbca7e27b3437b5db12c27df6fb3f25a79c4d460fac3a4b09872b4f03d` |
| B2 spelkandidat | `0fce7ccd6ab6d47703bf7233b7a7c928eb338704` | `8d4f0b27ff84fcef5dda046581b60b9cf45f90db5f27889f852b02fd721a564e` |

Fryst PR77-dokumentation `f55ff2cdcfa714ba020ad4bab34dc2172c65b89a`. Den signerade PR77-ROM:en byggdes kallt med DASM och matchade Drive samt båda ROM-kopiorna i native CI. PR77:s tidigare 404-länk gick att ladda ned med den anslutna åtkomsten. Den filen var 13 258 555 byte med SHA-256 `680f7ace4fde57003cae67e091ba28a9b0635598710317602e0c8c460683aadf`, och alla 898 manifestposter matchade. [PR77:s ZIP på Drive](https://drive.google.com/file/d/1ZzsuQcWFUHgJkBkntZpPgqPSc3QOhvKn/view).

Grafiken kommer från `a0638febaa1a21146f686c9edf92348792211eb5` med WALK_B-auditen i `5eeef639741077c50a71317d2b58679dbb7f454b`. Den ursprungliga grafik-ZIP:en verifierades mot SHA-256 och alla 208 manifestposter. [Draft PR78](https://github.com/Odourman/the-skraun/pull/78).

## Resultat från verklig Stella

| Prov | Resultat för B2 |
|---|---|
| PR77:s kontaktmatris | 396/396, varav 164 träffar och 232 missar |
| Orb | 219/219 giltiga prov. 37 geometriskt omöjliga kombinationer särredovisas. Inkluderar båda orbplatserna, alla banor, båda tillväxtstegen, paus, blockerad tillväxt och nedgradering. |
| Ny riddargrafik | Båda riddarna visade båda gångposerna åt båda håll vid L1 och vid L3 med halo. Varning och hugg observerades i båda riktningarna för båda riddarna. |
| Dubblerad P1 | Samma mask på båda positionerna i fem av 16 rutor för var och en av gångposerna när dubbelvillkoren var uppfyllda. Noll dubbleringar i riktade prov med olika Y respektive motstående riktning. |
| Nya riddarens kropp och kant | 72 riktade prov över fyra poser, båda riktningar och tre nivåer. Samtliga gav samma träffutfall som PR77, 36 träffar och 36 missar. Kropp, sköld och svärd mättes separat i Stella-bilden. 60 masker matchade inom två pixlar. De 12 övriga överlappade Skrauns P0-bild på L1, vilket inskränker det visuella beviset där. Båda attackposerna och gångposerna kontrollerades dessutom i fria P1-rutor. |
| Rörelse mot ny terräng | 48/48 jämförelser gav identiskt stopp och diagonalt glid som PR77. Alla åtta banor och tre nivåer ingår. |
| Terrängpixlar | B1 och B2 matchade den frysta PF-strömmen på båda skärmhalvorna i normal- och attackbilder för alla åtta banor. Den del av sista fysiska raden som redan hunnit gå i VBLANK ingår inte i jämförelsen. |
| Paus, P1 och livscykel | 462/462 pausrutor utan spök eller kvarvarande P1-data. L3-lånet fördelade kroppsfaserna 8+8+8 och lånefasen 24 rutor i det riktade provet. Det syntetiska svärdprovet gav nedgradering 3→2 i den synliga fasen och oförändrad L3 i lånefasen. Förlust, RESET och osårbarhet efter respawn provade. |
| Naturligt spel via joystick | En sammanhängande 120-sekundersvideo med Stella-ljud, 7 192 aktiva rutor inklusive banpauser, 5 136 rutor med aktiv strid, 22 banövergångar, fem liv kvar och 16 avfyrade pilar. |
| Joystickpolicy med korrigerat orbcentrum | PR77 och B2 fick byteidentiska inputs. Efter jämförelse av samtliga RAM-snapshots i två körningar skilde endast bildpekarens byte `$B6/$B7`. Enkel policy nådde L3 och 22 övergångar på 7 200 rutor. Det taktiska skriptet förlorade på ruta 395 i båda kandidaterna. Automatiserad input är underlag för regression. |

## Teknik och avgränsningar

- F6/NTSC, 4×4 096 byte. PR77→B1 ändrar 186 byte i bank 3. B1→B2 ändrar 120 byte där. PR77→B2 ändrar 306 byte. Exakt diff, bankhashar samt DASM-listor och symboler ingår.
- PF1 ligger `$FA00–$FCFF`. Strömmen är exakt 768 byte med SHA-256 `8ee7ac1ee211a84fd9101b105ce86c3b08d412cc02db50e34f5af41678a4826b`. Speglade udda och upprepade jämna banor använder samma CTRLPF- och indexlogik.
- WALK_B ligger `$F80E–$F81E` inklusive nollguard. `$F81F` är fri, `WorldPFIndex=$F820`, pekartabeller `$F6AB/$F6B1`. Gångvalet sker i VBLANK från aktuell position via `(2*KnightX - EnemyBottom) & 8`. Stillastående koordinater fryser posen. Det byggda programmet prioriterar varning och hugg. Den nya hjälprutinen på `$FED2` används via JMP, så inga extra stackposter uppstår. Statisk vägkostnad mot B1 i neutralfallet är +23 CPU-cykler för WALK_A och +3 för WALK_B. Det synliga rasterprogrammet och dess skrivinstruktioner behåller sina adresser. 
- 18 893 normala 262-radersintervall i B2-sessioner utan timerinjektion. Där ingår 14 790 intervall från tre naturliga joystickkörningar och 17/17 i den tidigare 264-fixturen. Flera riktade sessioner använder liknande testfall. Den separata historiska `TIM1T=$07`-injektionen gav 19×262 och 1×250 som i PR77. Ingen naturlig 250- eller 264-radersruta observerades. 76 CPU-cykler per scanline.
- Hårdvaruregister i 27-rutors native kombinationsspår. Arena-PF1 skrev på cykel 17 och färg-/blankrader på 26 eller 28. Arena-GRP0 på 3 och GRP1 på 33 eller 43 med VDEL-överföring vid nästa GRP0. Spåret omfattar de provade kombinationerna. Det är ingen garanti för varje nåbart tillstånd.
- 128 byte RIOT inklusive stack, inga nya permanenta RAM-byte. Statisk bankmedveten graf omfattade 15 767 tillstånd och högst sju stackposter. Konservativt lägsta SP `$F1`. Native stacktrap i riktad 442-rutorssession visade minsta loggade SP `$F2` efter startup. Trapfältets SP och den statiska gränsen har olika innebörd.
- Kollisionerna använder fortfarande rektangulära hinder. Exempel på bana 2 vid spel-Y48. På L1 stannar spelaren vid X95 och på L3 vid X83. Provytan (4×9 pixlar) i hinderkanten vid X100 är helt öppen i bilden som i PR77. Alla nivåer gled 8 steg i Y vid 12 rutor diagonal input. På bana 1 minskade samma typ av glapp i stickprovet från 36 till 20 tomma pixlar. Fotografi finns i `evidence/B2-contact`. Om MAIN vill ta bort det återstående glappet är minsta riktade ändring att fylla den befintliga solida innerkanten i grafik på bana 2 och mäta på nytt.
- Svärdet behåller 16/9/24 rutor för varning, hugg och vila. Spelets träff räknar kropparnas avstånd och det synliga P1-läget. T.ex. gav ett aktivt L1-hugg skada vid åtta enheters centeravstånd. Det ska inte läsas som att varje tecknad spets har en egen pixelperfekt träffyta. Skölden är visuell. Ingen ytterligare ankarskiftning behövdes i de riktade jämförelserna.
- Fysisk Atari, RetroN 77, PAL och användarens bedömning av flimmer och tydlighet är **NOT TESTED** här. Ingen oberoende verifiering. Leveransen avslutar del B. Svårighetsbalansering ligger i den efterföljande separata arbetsordern.

Testkommandon i `REPRODUCE.md`. Första spelinstruktioner och videoguide i `PLAYTEST.md`.
