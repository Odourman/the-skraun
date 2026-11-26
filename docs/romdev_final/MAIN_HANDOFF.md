# The Skraun · Final renderer · MAIN V

**Bästa körbara versionen.** `THE_SKRAUN_FINAL_RENDERER_NTSC_F6.bin`, 16 384 byte, standard F6 NTSC. SHA-256 `17f68b45839ce07210f79db1ebca175b7badd9f62e5939e100399cb22dd1eeae`. Spelstatus `PLAYABLE_CHECKPOINT / DEVELOPER_OBSERVED`.

**Förbättring.** Skraun går, speglas och behåller sin vanliga kropp under halo. M0 visar fyra yttermarkörer i tur och ordning. BL är dedikerad till orben och M1 till pilen. Ranger behåller världsfärgen. Normal HUD visar ett poängfält. Samtliga 17 arkiverade provslut mäter 262 i Stella 6.7.1.

**Kvar.** Fullständig diagonal och kantnära maskkvalificering, räckvidd mot verkliga träffar i alla riktningar, fiendemasker och attackrättvisa i samtliga kombinationer, full beam- och stackkvalificering, ljudmix per händelse och fysisk hårdvara. Fyra tidsdelade kardinaler är den bästa provade helhetslösningen här. Detaljer per ytterligare alternativ finns i beslutsmatrisen.

## Bygg och spåra

- [FULLGAME-1](https://github.com/Odourman/the-skraun/issues/50)
- [PR63, den frysta negativa visuella basen](https://github.com/Odourman/the-skraun/pull/63)
- [PR64, bas för den nya utvecklingsgrenen](https://github.com/Odourman/the-skraun/pull/64)
- [Ny utvecklingsgren](https://github.com/Odourman/the-skraun/tree/experiment/fullgame1-final-renderer-20261126)

Verifiera uppackningen med `sha256sum -c SHA256SUMS.txt`. Med `base/05_BUILD_TOOLS` före systemverktygen i PATH, kör `python hud/experiments/game/build.py`. Byggscriptet kräver exakt ROM-hash. Bank 0 och 2 är byteidentiska med PR64. Bank3:s PF1 mellan $FA00 och $FCFF har fortfarande SHA-256 `4c52651d7eca55e8e5c5158d33c90bec6bbd4f85e1732e65cf94321cd2b5334d`.

## Utförda prov

| Prov | Faktiskt resultat |
| --- | --- |
| Känd rasterregression och 17 äldre scener | 634 synkade bildrutor i problemsviten på 262. Samtliga 17 slutpunkter på 262. Rå RAM, cykelloggar och input ingår. |
| Naturlig pendel | 4 401 synkade bildrutor på 262. Slutresultat L3, sju liv och 8 400 poäng. Uppstartens ofullständiga rasterintervall redovisas separat. |
| Riktad raster | 120 individuella naturliga och 24 syntetiska L3-bildrutor med halo, pil och flera fiender. Alla på 262. |
| Fryst kropp, två halovarianter och kroppsskala | PR63 0/72 källexakta aktiva masker. Ny variant 72/72 i tre nivåer, rörelse åt höger och båda gångposerna. Även sidovariant och kompakt variant byggdes och gav 72/72 vid samma typ av prov. |
| Halo och ROM-gränser | Första toppläsningen gav långa streck då DASM fyllde tabellgap med $FF. Sista ROM har explicit nollfyllnad från $FDA2 till $FDFF. Aktiv markör väljs per bild. Vid L1/L2/L3 är sidorna 2/4/8 färgklockor × 14 rader. Övre/nedre markörer är 4/8/8 klockor × 4 rader. |
| Samma-Y, tre fiender | Adaptiv 8/7/9 synliga av 24, maximala luckor 3/3/2. Rotationskandidat 8/8/8 och luckor 2/2/2. Det är uppmätt pixelnärvaro i tre isolerade fönster, med attackfas och pil. |
| Orb och arena | 32 uppgraderingar i riktade Stella-fixturer och inga orbförbrukningar i 16 L3-fixturer. 24/24 ban-/nivåfall sammanhängande i den separata källmodellen från startcentret. Full rörelse genom varje passage och pixelposition i alla orblägen är öppna. |
| HUD och förlust | 1357 på bana 1 och 2. Vänster pixelsiluett identisk, oönskade högerpixlar 296 → 0. Syntetisk svart förlust med 1357 förblev pixelidentisk över FIRE. Det syntetiska debugger-RESET-provet gick inte igenom. Separat naturlig förlustvideo visar FIRE följt av F2 och spelaren tillbaka i arenan. |
| Stack och beam | Stackprov med trap på spegeladresser $01E0–$01FF nådde observerat SP $F5 efter skrivning, samma som PR63 i provet. Stella-spår för WSYNC, GRP, färgregister och position ingår. Full deadlines-/latchkvalificering kvarstår. |
| Spelvideo | Oklippt livefångst med verkligt SDL-ljud, 480 × 360 i 4:3. En separat kort film visar naturlig förlust och RESET. Synken mäts över den samlade inspelningstiden. Lokal ljudsynk vid varje enskild händelse och mänsklig mixavlyssning är öppna. |

## Resursdelning under aktiv halo

| Kombination | P0 / M0 | P1 / M1 | BL / PF |
| --- | --- | --- | --- |
| Halo och blinkande orb | Guldfigur och fasad yttermarkör | Vald fiende med ordinarie färg | Liten BL i det lokala färgfönstret. PF återgår till miljöfärg. |
| Halo, pil, orb och konkurrerande fiender | En M0-position efter gemensam grundpositionering | M1 projektil positioneras separat. P1 fördelas med adaptiv schemaläggning. | Orben behåller sin blinkfas och får guld endast lokalt. |
| Normal strid | Grå kropp och avstängd halo-M0 | Befintlig P1/P1-kopia där geometri tillåter, M1 vid pil | Orben använder miljöfärg. |

Den befintliga tvålinjeskerneln och HUD-tabellerna ger den stabilaste uppmätta helheten. Markeringsformen kostar en extra placeringsväg de bildrutor där M0 är aktiv, utan nytt RAM. Den rena rotationen har jämnare uppmätta luckor i ett syntetiskt dubbelt hot, medan befintlig adaptiv ordning bevarar prioriteringen av enskilda hot och ordinarie spelutfall. Installera den alternativa versionen som diagnostisk byggvariant för jämförelse.

## Research under arbetet

Ms. Pac-Man-mönstret med återanvändning och lokalt flimmer ställdes mot ren helbildsrotation. För The Skraun mättes en syntetisk grupp med tre aktörer på samma Y och aktiva attacker. P1-retrigger över exakta samma-Y-figurer hade negativa N7-resultat. Ett nytt oberoende retrigger-spår har lägre prioritet än den här fungerande figuren, haloformen och orben. Boxing gav en visuell referens för en utsträckt pose inom P1. En storleksändring mitt i hugg behöver separat fysisk testning innan den ersätter de befintliga maskerna. Källor finns sist.

- [Racing the Beam, avsnitt om Pac-Man och Ms. Pac-Man](https://nikuwstash.pl/files/The.MIT.Press.Racing.the.Beam.The.Atari.Video.Computer.System.Mar.2009.eBook-DDU.pdf)
- [Georgia Tech, Atari 2600-arkitektur och multiplexering](https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/e/466/files/2008/08/ece4893lec2_4up.pdf?bid=466)
- [The Skraun, närstridsresearch](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6_USER_FEEDBACK_MELEE_SWORD_REFERENCE_AND_CREATIVE_TEST_MATRIX_2026-11-21.md)
- [HEALTH-3, uppmätta negativa och positiva alternativ](https://github.com/Odourman/the-skraun/blob/8681c8cebad4566d863bbe7b004509cb35e88280/docs/health3/01_MAIN_DECISION_BRIEF.md)
