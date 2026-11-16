# THE SKRAUN — GRAPHICS P3: Upright Overhead Character Proof

**2026-11-16 | MAIN II | Endast grafisk kandidatstudie | Ingen ROM/Stella | Ej slutgodkänd**

## 1. RESULTAT OCH REKOMMENDATION

**KÄLLKONTROLL: PASS. UPRIGHT-KROPPSKOMPOSITION: BÄTTRE ÄN P1/P2. STRIKT TOPDOWN + UNIK ORIGINALIDENTITET VID L1: INTE BEVISAD.**

Detta är ett ärligt **NEGATIVT FULLSTÄNDIGT IDENTITETS-/KAMERARESULTAT**, inte ett påstående att ingen 8×12-form kan fungera. De två designförsöken visar en stående kropp med huvud uppe, armar åt sidorna och separata ben nedåt, medan P1-A var en liggande kropp med huvud åt höger. Ändringen stämmer med användarens uttryckliga rättelse, men den grafiska motsättningen finns kvar: ett ansikte med två stora ögon och tydlig mun avtecknar sig vid 8×12 gärna *framifrån*, inte som en fysikaliskt strikt lodrät kamerabild ovanifrån. Det får inte döljas bakom ett topdown-etikett.

**U1 är rekommenderad estetisk studie-kandidat**, aldrig en färdig sprite: flest av originalets ansiktskännetecken, två små horn, två negativa ögonpunkter och en mörk öppning mellan dem, på bekostnad av kroppens djup/overhead-känsla. **U2 är den medvetet annorlunda kropps-studien**, med mindre huvud och bredare axlar, utsträckta armar och två stora fötter; har svagare identitet, kan uppfattas som människa/robot/krabba. Ingen ska dömas enbart utifrån stora 8×12-pixeltavlor: kontrollera först hela L1-skärmen och därefter ozoomat L1-utsnitt i verklig 4:3-skalning.

| Fråga | Q1, tidigare upprätt referens | P1-A, liggande negativ kontroll | U1, ansikte | U2, kropp |
|---|---|---|---|---|
| Står upprätt i bild? | Ja, men platt/frontal | **Nej** | **Ja** | **Ja** |
| Tycks ligga på mage/sköldpadda? | Nej | **Ja** | Nej i huvudsak | Nej i huvudsak |
| Två horn och ögon? | Känt från tidigare källor | Saknar tydlig identitet | Tydligast kodade | Små/svåra |
| Öppen mun? | Frontal antydan | Nej | 2 mörka rasterceller som öppning; L1 otydlig | Inte pålitligt läsbar |
| Axlar/armar/händer? | Ja, mycket förenklade | Tassliknande | Ja, korta | **Ja, större sidoseparation** |
| Ben och fötter nedåt? | Ja | Nej, tassar på över/undersida | Ja | **Ja, breda fötter** |
| Strikt rakt-uppifrån-perspektiv bevisat? | Nej | Nej som upprätt figur | **Nej**, ansiktsplanet ser frontalt ut | **Nej**, kropp läsbar men huvud frontal/stiliserad |
| Unikt Skraun igenkänt vid oförstorad L1? | Inte säkert | Nej | **INTE BEVISAT** | **INTE BEVISAT** |

**Ingen visuell kandidat slutgodkänns.** P3 får avslutas som ett komplett avgränsat *visuellt belägg* och överlämnas till MAIN II/användaren för självständigt estetiskt val.

## 2. Exakta maskdata och ändringar

Källa: `P3_SOURCE_BITMAPS.json`. Höger är källraderna A/B; vänster är exakt bitreversering av **varje** 8-bitars rad. Row 0 är horn/huvud, rader 5–7 armar/överkropp, rader 9–11 ben/fötter. Logiskt 12 rader oavsett level; för varje figur används samma höger/vänsterformat även när spelaren förflyttas uppåt/nedåt. Ingen vertikal-facingsprite har skapats.

- U1 A/B: **7** ändrade bitceller; huvudrader 0–4 är identiska. Underkropps- och armceller växlar. U1 kontra fryst Q1: **18/17** bitceller A/B.
- U2 A/B: **8** ändrade bitceller; huvudrader 0–4 är identiska. Över-/underkropps- och armrörelser. U2 kontra fryst Q1: **26/26** bitceller A/B.
- U1 kontra U2: **20/25** bitceller A/B. Det är två avsiktligt olika familjer, inte en 1–2-pixelskorrigering.
- Fryst Q1 och P1-A är bokstavligen hämtade från GitHub-prototyperna utan egen omritning; kontrollrader och L/R-reversering valideras igen i `validate_p3.py`.

### 8x12, nivåer, färg

- L1: 8 color clocks × 12 scanlines. L2: 16 × 24. L3: 32 × 36, med förstoring x1/x2/x4 och rader x1/x2/x3 **endast i designbilder**.
- Provisorisk grå visningsfärg RGB (210,210,209), samma som faktisk ART1:s Stella COLUP0=$0C-provkod. Inget nytt TIA-färgbeslut fattat.
- För 4:3 approximativ visning förstoras 160×192 color-clock-rastret till 640×480 med nearest-neighbor. Detta är inte exakt CRT eller Stella. Ingen ny P0-test eller reparation av den frysta P01-ART1-kärnan.

## 3. Prioriterat granskningsmaterial

1. `01_L1_NATIVE_160x192.png` — opåverkad originalrastorskärm med 8×12-glyfer i både A och B, utan förstorade rutpixlar.
2. `02_L1_TV_4x3_FULL_A_B.png` — samma bilder i jämförbar 4:3-TV-approximation, helt skärmområde.
3. `03_L1_UNZOOMED_CONTEXT_CROPS.png` — **oförstorade utsnitt** ur punkt 2 (visningsupplösning 640×480, ingen extra zoom), avsedda för direkt L1-jämförelse.
4. `00_MAIN_II_P3_DECISION_SHEET.png` — liten, konsekvent L1-crop ovanför en tydligt **förstorad** binär cellmatris. U1/U2 står upprätt; P1-A ligger ner.
5. `04_BLACK_WHITE_SILHOUETTES_ENLARGED.png` och `05_EXACT_8x12_ROWS_ALL_DIRECTIONS.png` — källsilhuetter och alla 16 fasta A/B/right/left-layouter, granskning och felsökning, inte normalt spelavstånd.
6. `06_ALL_THREE_LEVELS_CONCEPTUAL.png`, `07_L1_FOREST_NIGHT_FLAT.png`, `08_AB_GAIT_BIT_DIFFERENCES.png`, `09_UPRIGHT_VS_PRONE_DIRECTION.png`, `10_UP_DOWN_REUSES_SAME_TWO_FACINGS.png` — samma källmasker, tydligt designmärkta.
7. `GIF_*.gif` — två källpose per riktning med samma 140 ms per bild. Källan ändras inte under upp/ned-färd; en särskild presentationsbild visar det utan några nya up/down-masker.

Alla PNG/GIF är **DESIGNFÖRHANDSVISNINGAR – INTE STELLA**. Kringbeskärningar och förstorade rutnät är konsekvent märkta. Det privata originalfotot återges inte i någon fil.

## 4. Källkontroll kontra tekniskt bevis

`validate_p3.py` gör automatisk kontroll av format, sann källspegling, två fasta poser, över- och underkropps/arm-animation, frysta Q1/P1-A-kontroller, icke-exekverbar `.inc`, motsvarande 8×12-PNG-pixelbyte, 4:3-schemat, GIF-ramantal/timing och SHA-256 för alla levererade filer. Skriptet ger enbart **SOURCE/PACKAGE PASS**, aldrig konstnärlig eller hårdvarumässig acceptans.

P01-ART1:s verkliga Stella-protokoll visade 24/36 källpixelkorrekta tillstånd (L1/L2); alla 12 L3-lägen misslyckades med en extra fylld topprad, tekniskt #19. Det är ett fryst separat experiment och ändras inte av P3. Tidigare R3-flimmer-/PF-/CPU-begränsningar förblir öppna.

## 5. Gränser och stopp

**Ingen ny kanon-sprite antas; endast MAIN II och användaren kan godkänna estetiken.** Ingen ROM-utveckling, Stella-körning, ny dimension, upp/ner-bitmap, ny GRAPHICS P4, automatisk v0.4, R4/B3c, merge, kodändring, mekanikändring, issue #15-stängning eller oberoende VERIFICATION har genomförts. P3 stoppas här.
