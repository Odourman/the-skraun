# THE SKRAUN – MAIN III: PLAY1-H verklig Y-följning, avgränsad X-FAIL, mottagningsbeslut

**Datum:** 2026-11-21. **Roll:** MAIN III, faktisk artefakt- och pixelgranskning, **INTE** independent VERIFICATION, inte egen ny DASM-/Stella-emulator-exekvering.  
**Beslut:** `MAIN_REVIEWED_PLAY1_H_BOUNDED_PARTIAL_ACCEPTED / Y_POSITION_DEPENDENCE_OBSERVED / X_FOLLOW_FAILED / X_MIRROR_CANDIDATE_REJECTED / TIMING_WORST_CASE_NOT_PROVEN / NO_NEW_ROM_AUTHORIZATION`.

## 1. Exakt auktoriserat scope och fryst källproveniens

- [Bindande MAIN-order](../handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_PLAY1_H_MOVING_VISIBLE_HALO_AUTHORIZED_2026-11-21.md), [Issue #36](https://github.com/Odourman/the-skraun/issues/36#issuecomment-7065181239), [draft PR #37](https://github.com/Odourman/the-skraun/pull/37). Användaren godkände endast PLAY1-H, att den synliga PF-guldhalon följer Skrauns **X och Y**, medan befintlig PLAY1-spelbarhet bevaras.
- Originalbas fryst PLAY1 `8247a3ba2b723c88336b63d5666503bed72cf2af`. Ny PLAY1-H branch `experiment/play1-h-moving-visible-halo-20261121` HEAD fryst `79b9739e77741c74ae5228f3c63d64449af7bc9f` vid MAIN:s granskning. [PR #37](https://github.com/Odourman/the-skraun/pull/37) **OPEN, DRAFT, UNMERGED**, bas `experiment/play1-single-arena-orb-halo-20261121`, inte `main`. Ingen ny main-merge.
- [Verklig utvecklarrapport vid fryst commit](https://github.com/Odourman/the-skraun/blob/79b9739e77741c74ae5228f3c63d64449af7bc9f/docs/play1_h/ROMDEV_PLAY1_H_MAIN_HANDOFF_2026-11-21.md), [PLAYTEST](https://github.com/Odourman/the-skraun/blob/79b9739e77741c74ae5228f3c63d64449af7bc9f/PLAYTEST_PLAY1_H.md), [ASM](https://github.com/Odourman/the-skraun/blob/79b9739e77741c74ae5228f3c63d64449af7bc9f/experiments/play1_h_single_arena.asm).
- **Faktisk GitHub Actions-artifact**, inte bara rapporttext, från [åtta-scener-real-Stella #44920971754](https://github.com/Odourman/the-skraun/actions/runs/44920971754), artifact id `14714180091` `PLAY1H-original-DASM-Stella-physical-ABC`: MAIN hämtade de verkliga **319846 ZIP-byten**, SHA256 **`a81be0452a36dcd4b949b334d7415c74d91922d554b7d5f90e2a3575f2a478e6`**, exakt **50 medlemmar**, **50/50 CRC PASS**. 
- Inne i ZIP: `build/play1h/play1h.bin` **4096 byte** SHA256 **`6e5e203ff2715fac650b76a620bc1e3e3b0084d67e82452842edd7b5e1903bca`** och faktisk `experiments/play1_h_single_arena.asm` SHA256 **`0aa5cf5d14e1eba0b786965fe316327810de01d36a4a32202651e06f36255c16`**. Båda matchar GitHub-rapporten, det frysta manifestet och ZIP:s `SHA256SUMS`. `DASM.log` visar `Complete. (0)`. Denna **samma ROM-hash** ligger i det åtta-sceners originalarkivet och i slutlig repo-binär; det är inte ett tidigare, inkompatibelt ROM-test.
- Testworkflowen har HEAD `f7fc7cad6cadb6f7204e4ec6bc8760fcf56115f7`, medan finala branch HEAD är `79b9739...`. GitHub compare förklarar att de efterföljande ändringarna var `bin/lst/sym/manifest`, freeze-workflow, rapport och PLAYTEST; `ASM` **ändrades inte** mellan test-head och final och ZIP:s *faktiska ROM-bytes* har samma frysta slut-SHA. [Freeze Actions #44921229617](https://github.com/Odourman/the-skraun/actions/runs/44921229617) `completed/success` men är inte en oberoende verifiering.

## 2. MAIN:s separata omräkning från verkliga åtta Stella 320x228 TIA PNG

MAIN öppnade alla åtta `build/play1h/moving/*/ACTUAL_STELLA_TIA.png` direkt i ZIP, räknade RGB-masker separat med PIL/NumPy (inte genom att exekvera utvecklarens eget `tests/play1h_pixels.py`) och läste `STELLA.log` med Stella 6.7.1, `Display Format: NTSC*`, `Bankswitch Type:4K*` samt exakt **ROM MD5 `d2229aebda6bf5bbed2ca87e259286ac`** förenlig med de granskade ROM-byten. Joystick-/FIRE-testskriptet skickar riktiga Stella debugger joystick events och inga gameplay-RAM-injektioner.

| Originalscen | P0 grå TV bbox (x0,y0,x1,y1) | Blå P1-pixlar | Guld-PF-pixlar |
|---|---|---:|---:|
| baseline L1 OFF | (146,114,162,126) | 120 | 0 |
| pickup_L2_off | (172,132,204,156) | 120 | 0 |
| L1_on | (146,114,162,126) | 120 | 3744 |
| L2_on | (172,132,204,156) | 120 | 4784 |
| A_L3_on | (156,126,220,162) | 0 | 5676 |
| B_L3_right8 | (172,126,236,162) | 0 | 5616 |
| C_L3_right8_up8 | (172,118,236,154) | 0 | 5632 |
| D_L3_right8_down8 | (172,128,236,164) | 0 | 5632 |

**MAIN:s separata konkreta X/Y-fynd**, samma klassning och siffror som utvecklarrapport:
- A→B: grå P0 förflyttas **+16 TV-pixlar (+8 spel-/TIA-X)**. Guldmaskernas symmetriska skillnad = **444** pixlar, men **efter att ha exkluderat P0/P1-ocklusion på båda skärmbilderna** återstår **0 guldpixeländringar**. Ingen synlig X-följning i testad ROM.
- B→C: P0 upp **8 fysiska skärmrader**. Guldmaskernas symmetriska skillnad = **1840** pixlar, varav **1516** ligger utanför P0/P1; ändringsbbox **[96,106,224,173]**. Detta bevisar fysisk **Y-positionellt beroende** guldgeometri i de testade lägena, inte att hela önskade 360° kontur och dess koppling till radie/tjocklek är godkända.
- Den första mellanversionens **1608** guldpixeländringar är ett separat *tidigare* test. För **frysta finala åtta scener gäller 1516**.
- Övre fasta hinderlinjen y60 ändras med **0** guldpixlar vid A→B; Y-varianten har således inte i detta test samma observerade scenförstörelse som X-experimentet. Nivå 2 återger P0 32×24, original R3 P1 120 blå pixlar; efter L3-träff 0; BL-orb-färgbyte från 2832 till 2816 världsfärgade pixlar vid verklig pickup.
- Y-rörelsen var fri upp8; D ned8 blev **+2** rader före hinderstopp. Det är ett avgränsat verkligt L3-kollisionsprov, inte alla hinder-/hörnfall.
- Fyra solida hinder och en diagnostisk R3-testdummy är **inte** en färdig bana eller ett avslutat krav på två riddare plus Ranger.

## 3. Reproducerat faktiskt negativt X-experiment – ska INTE återinföras

MAIN laddade även ned **det separata originalarkivet** från [X-reflection-försöket run #44920592381](https://github.com/Odourman/the-skraun/actions/runs/44920592381), testcommit `c16c2c2667ef476943d3c6f09ffe80820124fb42`, artifact `14712723857`: **244799 byte**, SHA256 **`01ec9c430099006aa77b9b392baa408de3b436a979eca58a9a2719c693f7325c`**, **39/39 ZIP CRC PASS**. Detta är **INTE** slutlig Y-ROM (separat käll-SHA `67249d03...`, ROM-SHA `15261024...`).
- Fysisk X-beroende CTRL-PF repeat/reflection ändrade faktiskt **64 guldfärgade pixlar på den fasta övre hinderraden y60**.
- Den faktiska `L2_on`-bilden visar **P0 bbox (172,133,204,167) = 32×34** (skall vara 32×24) samt **144 blå P1 pixlar** (originalmask = 120). Alltså konkret skadad bitmap/-timing, inte en acceptabel X-strategi.
- Koden ändrades tillbaka; denna negativa X-kandidat får inte tolkas som att alla TIA-alternativ är omöjliga. Bevara positiv Y-variant och stoppa just den förstörande reflektionsgenvägen.

## 4. Tekniskt bevisläge och MAIN-beslut

- **Riktig original-Atari 2600 4 KiB NTSC DASM/Stella-ROM:** JA i avgränsat emulerat test. **Inte** fysisk konsol-test; `Stella` är emulator. Testad 262-NTSC konsistens är debuggerobservationsnivå och inte full instruktions-/frame-exhaustive proof.
- Käll-/DASM-härledd P0/PF1/PF0/PF2/P1/BL-rasterlayout visar c3/c10/c15/c27..28/c34..35/c42..44 registerskrivningar; villkorliga fall och indirekta sidkorsningar innebär konservativ **upp till ~77 av 76 CPU-cykler** i en synlig fysisk rad. **Detta är SOURCE_STATIC risk, inte uppmätt fysisk Stella full-path fail eller PASS**. Separat bestämd timing-/side-effect-skuld kvarstår, och en full korrekt N6-C renderer får inte antas.
- Statiskt RIOT **42B ($80..$A9)**, statiskt beräknat upp till ca4B returstack; ingen uppmätt Stella stackhighwater, heller inte full fiendeintegrationsbudget.
- **MAIN-disposition:** `ACCEPT_AS_BOUNDED_PLAY1_H_PARTIAL`. Vi har **en spelbar bas**, tydligt **verkligt Y-framsteg**, konkret **X-FOLLOW FAIL** och ett **förkastat förstörande X-experiment**. Denna leverans är **STOPPAD**, PR #37 ska kvarstå **DRAFT/UNMERGED**, liksom PR #35. Ingen main-merge, N8/N9, mapperändring, sprite-/art-beslut, tyst fiendereduktion eller upprepade oberoende verifieringsloopar auktoriseras.
- **Kortaste framtida spelinriktning, endast rådgivande:** fortsätt inte med samma mirror/repeat-växling eller B3b:s 16-frames-stegning. Nästa verkliga X-arkitekturidé behöver åstadkomma **asymmetrisk horisontell PF-geometri/aktörscentrering som inte flyttar solida hinder**, troligen genom förberedda X-indexerade maskval eller annan arbetsfördelning **före kritiska rasterrader**. Den måste prövas med **verklig DASM/Stella** på minst två skilda X plus ett Y och med explicit P0/P1/PF/BL/cycle-fail-early; inga antaganden att en sådan tabell ryms i 4KiB/128B eller att 76cy är löst. Detta är **inte en ny implementationstillåtelse** och inte förevändning för ny bred verifierings-/source-only-runda. MAIN tar separat användarbeslut innan någon ny ROM-testfamilj får starta.

**Status:** `PLAY1_H_DEVELOPER_DELIVERED_PARTIAL / MAIN_REVIEWED_BOUNDED_PARTIAL / PHYSICAL_Y_DEPENDENCE_OBSERVED / X_FOLLOW_FAILED / N6C_FULL_RENDERER_OPEN / N8_N9_NOT_AUTHORIZED / VERIFICATION_33_SEPARATE`.
