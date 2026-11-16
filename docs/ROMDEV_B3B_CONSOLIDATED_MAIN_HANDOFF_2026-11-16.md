# The Skraun – ROM DEVELOPMENT P02-B3b: samlad överlämning till MAIN
**Datum:** 2026-11-16. **Roll:** implementation och utvecklaregenkontroll, inte oberoende VERIFICATION.

**Bindande scope:** [MAIN:s B3b-auktorisation](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_B3B_AUTHORIZED_SCOPE_2026-11-16.md). B3c och senare steg är inte påbörjade. Inga ändringar har gjorts i main av B3b.

## 1. Sammanfattning av uppnått och öppna risker
- **B3b horisontell joystickföljning: PASS** i ett avgränsat level-2 NTSC-experiment över 13 sammanhängande TIA-x-positioner 56,60,64,68,72,76,80,84,88,92,96,100,104. Rörelsen läses från SWCHA, inte SELECT. Testade verkliga hållna styrsignaler höger, vänster och reversering. P0 och asymmetrisk ring följer samma registerindex utan inbördes lagg.
- **Visuell coexistence med tre syntetiska hinder: PASS för förkomponerade PF-OR-masker** i detta 4K-test; faktiskt renderade pixlar matchar (ring ELLER hinder) minus områden som döljs av P0.
- **Generell runtime-komposition för fler hinder: FAIL i oförändrad kernel**. 63 av 76 CPU-cykler är redan uppbundna på värstafalls-scanline. Minst fyra ytterligare byte-läsningar för dynamisk scenery-mask skulle kräva minst ~16 ytterligare cykler, 63+16=79 >76 innan övrig kompositionskostnad.
- **Full produktionsrendering med hinder, tre synliga fiendeaktörer, pil och HUD: BLOCKED som genomförbarhetsbevis**. Ett nytt separat MAIN-beslut om forskning/redesign behövs, inte en tyst fortsättning till B3c.

## 2. Exakta filer, ROM och reproducibilitet
Separat branch: [experiment/romdev-b3b-horizontal-follow](https://github.com/Odourman/the-skraun/tree/experiment/romdev-b3b-horizontal-follow) skapad från B3a. main HEAD vid uppdragsstart: 8e11940ae5ddfd7d759d920af6972712375c1ada.

| ROM | Assemblerfil | Byte | SHA-256 |
|---|---|---:|---|
| Bas-B3b | experiments/romdev_b3b_dynamic.asm | 4096 | 7d96bcb71532643307922f62814900b09a1525ede06795c17417607634efd060 |
| B3b med hinder | experiments/romdev_b3b_obstacles.asm | 4096 | 31b859d711bb08228b03015f9039b1df97c77628ab3637f754ad3df77b599bbe |

Kommandon: dasm experiments/romdev_b3b_dynamic.asm -f3 -obuild/romdev-b3b-dynamic.bin -lbuild/romdev-b3b-dynamic.lst -sbuild/romdev-b3b-dynamic.sym; motsvarande för romdev_b3b_obstacles.asm. SHA-256 och ROM-storlekar är verifierade via GitHub Actions. Ingen bank-switching, ingen 13×192-raderskartbank och ingen större ROM har implementerats.

## 3. Verkliga Stella-pixel- och rörelsetester
- Stella 6.7.1 under Xvfb, direkt styrt med xdotool: 77 originalbilder för bas-ROM och 77 för hinder-ROM = **154 verkliga emulatorbilder**. Alla 13 mellanlägen uppträder under sammanhängande hållning och flera faktiska riktningsbyten, med steg på högst 4 color-clocks åt gången. Ingen fast position väljs av SELECT.
- Ringens faktiskt avlästa bildmått 80×64 bildpixlar (40 TIA-color-clocks × 64 scanlines); P0 är 32×24. Ringsilhuetten är exakt samma pixelmängd för alla 13 centra efter horisontell översättning, utan oavsiktlig spegling eller klippning.
- Horisontell centrumavvikelse mellan ring och P0 = **0 TIA-color-clocks**, mot mål högst 2. P0 Y konstant = 99 i Stella-capture, ring Y konstant. Grå P0-radordning överensstämmer pixel-för-pixel med direkt assemblerade Troll2-bytes, 440 grå bildpixlar och korrekt upprätt radorientering. En separat ny automatiserad testassertion för exakt sprite-maske har lagts till; tidigare fungerande realbildstest och en lokal bytejämförelse ger samma resultat.
- Aktuell diagnostisk hastighet är ett steg per **16 NTSC-bildrutor** (~267 ms per 4-clock-steg), med inputpolling som gör att första responsen kan invänta 0–15 rutor (~0–250 ms). Detta är för långsamt för den färdiga spelmotorn. Resultatet visar *logiskt synkroniserad följning*, inte färdig spelkänsla. Intervallet 56..104 är **testbegränsning, inte framtida spelregel eller permanent skärmgräns**.
- [Godkänd full Stella-bildsekvens och hindertest](https://github.com/Odourman/the-skraun/actions/runs/43900333332), med verkliga PNG-bilder, SHA och loggar. Efter detta har endast testscripts, arbetsflödespaketering och rapport ändrats; assemblerade kandidatbyte och ovanstående SHA är samma.

## 4. Uppmätt Stella Debugger, skild från beräknad CPU-budget
En separat [Stella Debugger-körning](https://github.com/Odourman/the-skraun/actions/runs/43900278446) körde först riktiga joysticktryck i emulatorns normalläge, gick sedan till debugger och avläste **262 scanlines** i följande fyra separat fångade tillstånd:
| Tillstånd | RAM Mode | TIA-center | Stella Debugger scanlines |
|---|---:|---:|---:|
| Start | 6 | 80 | 262 |
| Hållen höger | 12 | 104 | 262 |
| Hållen vänster | 0 | 56 | 262 |
| Reversering höger→vänster | 9 | 92 | 262 |

Detta är **verkligt mätta bildrutelängder**, inte en C-/Pythonmodell. Instruktion-för-instruktion worst-case trace i full framtida motor är **NOT TESTED**.

## 5. Statiskt cykelbokslut från DASM-listning och riktiga symboladresser
Testscripten tests/romdev_b3b_cycle_ledger.py enumererar **4992 cases**: 2 ROM-kandidater × 13 center × 192 synliga rader och räknar 6502-instruktionscykler med både grenfall och sidkorsning för de faktiskt sammanlänkade dataadresserna. CSV:n levereras tillsammans med ROM.
- **Max 63/76 CPU-cykler per synlig scanline**, med nästa WSYNC-skrivning inräknad; konservativ statisk ledig marginal **13 cykler**. Detta är **beräknat**, inte en direkt debuggerprofilerad cykeltrace.
- Senaste högerhalvans PF0-write beräknat till cykel **42**, PF1-write cykel **50** efter WSYNC. Dessa uppfyller den testade rastervägen men är inte tillstånd för fler P1-/HUD-skrivningar i samma tidsslott.
- Per synlig rad används **6 playfield-registerwrites** (PF0/PF1/PF2 vänster respektive höger), **1 GRP0**, **1 WSYNC** och fyra indirekt-indexerade PF-table-lookups. P1 nyttjas inte.
- VBLANK-pekarsättning och P0-positionering har separats med explicit WSYNC; ett tidigare försök gav **263 scanlines**, nu är det 262 också efter faktiska riktningsbyten.

## 6. ROM-/RAM-/PF- och fienderesurser
- Maskdata: **13×4×33=1716 byte**, vertikalt komprimerade med symmetri; radmapp + grå sprite **2×193=386 byte** (inklusive en padding-byte vardera), pointertabeller **8×13=104 byte**, P0 X-tabell **13 byte**.
- **RAM** $80..$89 = **10 byte nyttjade av B3b-isolatet**, 118 byte kvar i testmotorn. Inte en reservation som säkert räcker för ett framtida spel.
- **ROM:** total 4096 byte; sista masker vid $FC15..$FC35, vilket lämnar **966 byte sammanhängande före vektorer vid $FFFC**. ORG-hål före maskerna finns också, men kräver omdisponering för användning. 4K-storlek är inte evidens för att hela spelet får plats.
- P0=Skraun, P1=ledig. Men två samtidiga riddare, en bågskytt, en pil, en orb och poäng-/liv-HUD kräver fler överlagrade objekt än två fritt placerbara TIA-player-sprites. Multiplex, missile/ball, playfield eller kontrollerat flimmer skulle behöva egen separat feasibilityprövning. **Inga fiender, projektiler eller HUD är implementerade eller tidtestade här.**

## 7. Separat hinder/visuell konflikt-probe
- Tre korta fasta syntetiska PF-hinderkolumner i y82..109 vid ungefär TIA-x 56,88,108 är OR-komponerade **vid ROM-maskgenerering**, alltså ingen extra synlig CPU-tid.
- Stella-pixelkontrollen visar guldmask = (ring ELLER hinder) minus pixlar som ligger under grå P0. Samma y och samma fördelning i samtliga 13 lägen; överlappande ring och hinder delar **samma COLUPF-färg**.
- Vid centrum x72,76,92 sammanfaller vardera **176 bildpixlar** som inte visuellt kan särskiljas. Hinder döljs dessutom där P0 skrivs ovanpå PF. Detta är en **visuell läsbarhetskonflikt**, inte att magins logiska räckvidd upphör; designbeslut 35 (halon passerar solida hinder) ändras inte.
- Minst fyra extra dynamiska scenery-byte-läsningar kostar minst **16 CPU-cykler**, alltså minst **79/76** utan OR-operationernas egen kostnad. **Den nuvarande samma-scanline-kerneln kan därför inte generellt kombinera godtyckliga framtida hinder vid runtime.**
- Att i stället förkomponera 1716 byte mask per hinderlayout skulle för åtta olika banor ge omkring **13 728 byte** redan innan animations-, fiende- och HUD-kod. Inte genomförbart som samma 4K-kopierade arkitektur.

## 8. Fel som upptäcktes och korrigerades
1. En snabbvariant använde signerad BPL-nedräkning med X=191 och lämnade bildloopen för tidigt (svarta bilder). Lösningen använder en padding-byte och osignerad X=192..1 med DEX/BNE.
2. Lång VBLANK-pekaruppsättning följd av P0-positionering passerade scanlinegränsen och gav 263 scanlines. Extra WSYNC och justerat radantal gav 262.
3. Harness hade fel förväntat Y-värde från 263-kandidaten; korrigerades till P0 y=99 efter NTSC-synken.
4. Pixeltestet tar hänsyn till att P0-grå pixel prioriteras framför playfielden. Ytterligare exakt ROM-bitmap-test infördes.
5. Debugger-kommandot för joystick påverkade inte tillförlitligt emulerad SWCHA vid steppad körning. Den slutliga mätningen använder **verklig xdotool-joystick innan debugger öppnas**, med separata skärmbilder. Grön workflow utan läsbar screenshot används inte som bildbevis.

## 9. PASS / FAIL / BLOCKED / NOT TESTED
| Delmål | Status |
|---|---|
| B3b: 13 horisontella lägen via verklig joystick, fram/back/reversering | **PASS** |
| P0/ring alignment, rättvänd P0, fast Y, kontur utan clipping | **PASS** |
| Riktiga NTSC Stella Debugger 262 scanlines i flera verkliga joysticktillstånd | **PASS** |
| Hinder och ring förkomponerade med PF-OR i begränsad visuell scen | **PASS** som isolerat visuellt prov |
| Generisk scenery + halo runtime-OR i den befintliga 63/76-kerneln | **FAIL** (minst 79/76 cykler) |
| Full produktionsintegrerad samexistens med framtida banor/fiender/HUD | **BLOCKED** som tekniskt bevis |
| Diagonal/vertikal B3c, tre dynamiska skalor, FIRE, B3d/B3e, kollisionslogik, PAL, fysisk konsol | **NOT TESTED / EJ AUKTORISERAT** |
| Oberoende VERIFICATION | **Ingen gjord, enligt MAIN:s instruktion** |

## 10. Rekommendation och länkad evidens
MAIN kan acceptera **B3b som avgränsad utvecklaregenkontroll** för en joystickföljande komprimerad asymmetrisk haloring i 13 horisontella lägen. MAIN bör **inte** utan ytterligare separat auktorisation behandla denna renderer som produktionsklar eller automatiskt börja B3c. Nästa genomförbarhetsgrind bör jämföra hybrida ring-/hinder-renderers och raster-schemaläggning, skydda level-3-räckvidd och testa samtidig kapacitet för två riddare, bågskytt, pil och HUD. En precomposed-scenestrategi kräver annan ROM-datadesign/bankad data, men ingen bankswitching-arkitektur väljs genom denna rapport.

**Evidens:**
- [Full 154-bilders Stella-sekvens med hindervariant och symboler](https://github.com/Odourman/the-skraun/actions/runs/43900333332)
- [Direkt Stella Debugger efter riktiga joystick-signaler, fyra 262-line-tillstånd](https://github.com/Odourman/the-skraun/actions/runs/43900278446)
- [DASM-symbolbaserad statisk worst-case-ledger](https://github.com/Odourman/the-skraun/actions/runs/43900062518). Det workflowets senare bildtest föll på gammalt harness-y-värde; själva cykelberäkningen passerade och nyare bildkörningar visar PASS.
- [Drive-evidensmapp](https://drive.google.com/drive/folders/1fn4RTvPreT6dsVQD5HUaLYIRPfLffz8h)

## 11. Slutlig CI- och leveranskontroll
- **Slutlig, grön bild-/ROM-/hinder-/sprite-/cykelregression:** [GitHub Actions run #43901341243](https://github.com/Odourman/the-skraun/actions/runs/43901341243), inklusive extra test för exakt assemblerad P0-radmask, testfiler, två kompletta 4K-ROM, SHA256SUMS, DASM-listning/symboler, 154 Stella-bilder och enumererad cykel-CSV.
- **Direkt Stella Debugger med faktisk joystickinmatning före debuggerläge:** [run #43900278446](https://github.com/Odourman/the-skraun/actions/runs/43900278446). Fyra olika RAM Mode-värden och 262 scanlines i varje, inga illustrerade bilder.
- Google Drive: [B3b:s slutliga Stella-/source-/ROM-arkiv](https://drive.google.com/file/d/1JSoosf9xjUiPAIC2BQhgL-s7l-CbgYzl/view?usp=drivesdk), [fyra joystick-/debuggertillstånd](https://drive.google.com/file/d/1cfas8NzvtadExBnFxuiHOphCxAwIwtNt/view?usp=drivesdk) och [bildmontage med enbart riktiga Stella-pixlar](https://drive.google.com/file/d/18ZYn53VcgsZj8k_zOeWyDK17IXtZAvYI/view?usp=drivesdk).
- Avgränsad, omersatt **draft PR #11**: https://github.com/Odourman/the-skraun/pull/11 (base=experiment/romdev-c-b3a, inte main, ingen merge).
- ROM-källorna efter uppsättning av slutliga bildtestscript har inte ändrats; den aktuella SHA256SUMS i den godkända jobbartefakten är leveransens binära auktoritet. Inga utlovade senare utvecklingssteg har utförts.
