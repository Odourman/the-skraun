# THE SKRAUN – MAIN III: PLAY1 faktisk ROM-/bildgranskning och avgränsat PARTIAL-beslut

**Datum:** 2026-11-21. **Roll:** MAIN III, käll-/artefakt-/pixelgranskning. **INTE oberoende VERIFICATION och INTE en egen ny DASM/Stella-exekvering.**  
**Beslut:** `MAIN_REVIEWED_PLAY1_BOUNDED_PARTIAL_ACCEPTED / REAL_GAMEPLAY_LOOP_OBSERVED / FIXED_PF_HALO_FAIL / NO_NEW_ROM_AUTHORIZATION`.

## 1. Frysta källor och bevis som faktiskt granskats

- Användarens separata PLAY1-godkännande i MAIN och [bindande PLAY1-order](../handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_PLAY1_SINGLE_ARENA_GAMEPLAY_ROM_AUTHORIZED_2026-11-21.md), [Issue #34](https://github.com/Odourman/the-skraun/issues/34#issuecomment-7064757783).
- [Draft PR #35](https://github.com/Odourman/the-skraun/pull/35) är OPEN/DRAFT/UNMERGED på `experiment/play1-single-arena-orb-halo-20261121` vid kontrollerad HEAD **`8247a3ba2b723c88336b63d5666503bed72cf2af`**. Bas i fryst P01-COL1 `90f89441b41a2e82408581b81d3743b1423e5cdb`. Ingen merge till main.
- [ROM DEVELOPMENT II:s slutrapport](https://github.com/Odourman/the-skraun/blob/8247a3ba2b723c88336b63d5666503bed72cf2af/docs/play1/ROMDEV_PLAY1_MAIN_HANDOFF_2026-11-21.md) och [PLAYTEST](https://github.com/Odourman/the-skraun/blob/8247a3ba2b723c88336b63d5666503bed72cf2af/PLAYTEST_PLAY1.md).
- Faktisk [Google Drive ZIP: sju verkliga gameplayscener + ROM/källa](https://drive.google.com/file/d/13z4FaozqetXq7DxQIaCL0kL3GiPe5M6x/view): **275074 byte**, SHA-256 **`c7a900b8587ebd443b3e81236e11547ce71cd936ce357a1a97314edf5ecec835`**, **38 ZIP-poster, samtliga CRC PASS**. MAIN laddade ned de faktiska ZIP-byten och öppnade original TIA PNG, inte bara producentens sammanfattning.
- Fysisk ROM från ZIP `build/play1/play1.bin`: **4096 byte**, SHA-256 **`cbc296309d60a35debb7bd6980ea5f61db5101bff48c4397f4c5569a8d33aedd`**. ASM från samma ZIP `experiments/play1_single_arena.asm`: SHA-256 **`69898159cd4261a7f77365ef7e21da1bb30194770762f4f7292c9f52b542f606`**. SHA-256 båda överensstämmer med manifestet i zip och developer handoff. [Genuin Actions gameplay run #44918066283](https://github.com/Odourman/the-skraun/actions/runs/44918066283): `completed/success`, HEAD `dcaf55571dfa66e3daa81ff954f8eeb1fce5a1a2` för gameplay-testet, senare ROM-fryst branch HEAD `8247a3ba...`. Grön testworkflow täcker de sju definierade målen, **inte** full PLAY1-kvalifikation.
- Separat [Google Drive äldre 12-frame ZIP](https://drive.google.com/file/d/1yePL7EPHQM723XAKNTmIIHxxPFS6omKJ/view): **491997 byte**, SHA-256 **`06ab2abe9bee6dfa36a6cf46cb71aac75eef23ce7a9adc79f0121cacea7c20f7`**, **39 poster, CRC PASS**. **VIKTIG PROVENIENS:** Denna ZIP innehåller **en TIDIGARE PLAY1-ROM** SHA256 `99a93069d42a60ec7615cbba4c7c8748fc343d572736266580dde65b3e99e4af`, ASM SHA256 `b0033c331136708e79927ff8e44decc7eebd9dbc9aeb4f71120513047ca51125`. Det är 13 stillastående TIA-bilder med identiska RGB-hashar och föregår finala 7-scene gameplay ROM. **Räkna inte dem som 12 konsekutiva frames av slut-ROM.** Detta ändrar inte sanningen i den slutliga 7-scene gameplayserien.

## 2. MAIN:s egen omräkning av faktiska originalbilder (inte utvecklarens Python-orakel)

Öppnade `build/play1/gameplay/*/ACTUAL_STELLA_TIA.png` i den nedladdade 38-posters ZIP:en med Python/PIL+NumPy. Exakt 320×228 RGB pixlar per bild. Självständigt isolerade grå Skraun RGB (210,210,209), guld-PF RGB (234,194,84), P1 blå (121,194,251).

| Verkligt Stella-scenario | P0 grå bbox (vänster,överkant,höger exkl,nederkant exkl) | Guldpixlar | P1 blå källmask-pixlar |
|---|---|---:|---:|
| `baseline` | (146,114,162,126) 16×12 | 0 | 120 |
| `l1_fire` | (146,114,162,126) 16×12 | 3744 | 120 |
| `movement_pickup` | (172,132,204,156) 32×24 | 0 | 120 |
| `level2_fire` | (172,132,204,156) 32×24 | 4784 | 120 |
| `level3_after_respawn` | (156,126,220,162) 64×36 | 0 | 120 |
| `halo_fire_target` | (156,126,220,162) 64×36 | 5676 | 0 |
| `halo_follow_move` | (172,126,236,162) 64×36 | 5616 | 0 |

**Konkret MAIN-fynd – statisk halo, separat bevis:** Jämför de sista två autentiska slut-ROM-bilderna. Skrauns fysiska x-bbox flyttar sig **16 TV-pixlar** (8 TIA/spelenheter), medan guld-PF-geometrins extrema bbox förblir **x24..295, y55..182**. De två guldmaskerna skiljer sig i **444** pixlar totalt, men efter att alla pixlar som upptas av Skraun i någon av de två bildrutorna undantagits är guldmaskerna **IDENTISKA: 0 pixelavvikelser**, kvarvarande **5424 guldpixlar** i vardera bild. Skillnaden beror på P0-ocklusion över en **arenafixerad** PF-geometri, inte någon följande X/Y-ring. Detta stämmer också med faktiskt assembler: `Visible:` läser `HaloPF2Rows,x` och maskerar med `HaloVisualMask` (nivåberoende, **inte** `PlayerX/Y`). Den logiska attackrutinens X/Y utgår däremot från `PlayerX/PlayerY`.
- R3 P1 originalmask 120 synliga blå pixlar före och 0 efter observerat attacktest. Orbpickup-/attackscripts använder genuina `joy0Right`/`joy0Down`/`joy0Fire` debugger-kommandon; inte direkt skrivning av spel-RAM enligt kontrollerat `INPUT.script` och faktisk arbetsordning. PLAY1 har alltså **en faktiskt fungerande begränsad joystick/orb/attack-upplevelse**, inte bara pappersspel.
- Screenshots visar inte per definition en estetiskt lyckad ring: testets **hela bakgrund blir röd i kill-feedbackscenen**. Det är diagnostisk feedback och kan behöva designgranskas senare; denna MAIN-rapport godkänner inte slutgrafik eller nya paletter.

## 3. Fysisk tids-/minnesgrind – endast faktiskt bevisad nivå

- PLAY1 är **verklig 4 KiB DASM-byggd** och faktiskt Stella-körd, men MAIN har **inte själv kompilerat eller själv drivit Stella**. `MAIN_REVIEWED` gäller faktiskt läst autentiskt material och byte-/bildjämförelse, inte `INDEPENDENT_VERIFICATION`.
- Utvecklaren härleder **73 instruktioners CPU-cykler efter WSYNC + 3 WSYNC = 76/76 på värsta synliga scanline** ur verklig DASM-listing. TIA-skrivningar hävdas vid `GRP0 c3`, `PF0 c10`, `PF1 c17`, `PF2 c27`, `GRP1 c34`, `ENABL c44`. Det är **SOURCE_STATIC**, inte uppmätt riktig debugger-instruktionscykel/beam highwater. Noll beräknad radslack innebär att en dynamiskt följande halo **inte bara kan läggas till med fler cykler på samma rad**.
- Källallokerat RIOT **38B**, statiskt härledd returstack ca **4B**, men inget live uppmätt stack-highwater eller komplett integrerad tre-fiender-motor.
- Sju separata Stella-scenarier är **inte** en 12-frame hållbarhetssekvens av slut-ROM. L3 hörnblockering/kollisionsregression har i huvudsak ärvts från COL1 och inte självständigt instrumenterats för alla fyra hinder i PLAY1. Ingen sådan överräckning får användas till fullspel-GO.
- **Huvudbegränsning:** Halo visuell geometri måste följa Skrauns både X och Y, tjocklek/räckvidd ska öka med level, utan att kroppskollision, rörlighet, P1-testmål eller TIA-sanning förstörs. Föreslagen fortsatt fysisk metod måste frigöra/omfördela resurser eller förbereda geometri **före** kritiska rasterrader; en ren Python/PF-källtabell är inte en fysisk kvalificerad lösning.

## 4. MAIN-beslut, stopp och kortaste väg framåt

**ACCEPT AS BOUNDED `PLAY1_PARTIAL`:** Den beställda körbara prototypen har en verklig spelbar grundloop (Skraun/orb/level/FIRE/P1-testdöd) och synlig växande test-B-PF. **Följande visuell halo = FAIL**. Det är ett nyttigt, konkret steg framåt. Inget N8/N9/fullspel eller ett godkänt tre same-Y-fiender fullrenderer bevisas. PR #35 fortsätter **DRAFT och UNMERGED**; ROM DEVELOPMENT II:s PLAY1-uppdrag är **STOPPAT efter leverans**.

**Nästa rekommenderade, EJ AUKTORISERADE, enda snäva test:** `PLAY1-H`: på en **separat ny gren från frysta PLAY1-slutbytes/commit**, pröva EN minimal fysisk strategi för att positionera synlig B/PF-halokontur utifrån Skrauns X/Y, utan att försöka lösa hela P1/three-enemy-kernel samtidigt. Visa **minst två Skraun-positioner separerade både horisontellt och vertikalt**, alla tre levelmasker, och om P0+PF/P1/BL fortsätter vara fysiskt rimliga. En enkel målmedveten profilering av kritisk 76/76-WSYNC och RIOT krävs; enbart ett centerberoende source-orakel räcker inte. Om ny arch/mapper eller gameplaykompromiss verkar krävas, STOP och föreslå tydliga alternativ i MAIN. **Detta dokument är INTE ny implementationstillåtelse; separat användarbeslut krävs.**

**Verification policy:** Inga nya oberoende verifieringsloopar för PLAY1 PARTIAL. Redan [Issue #33](https://github.com/Odourman/the-skraun/issues/33) gäller enbart gammal fryst N7-FAIL och måste inte blockera nästa separat godkända gameplayprototyp.

**Status:** `PLAY1_DEVELOPER_DELIVERY_RECEIVED / MAIN_REVIEWED_BOUNDED_PARTIAL / VISUAL_DYNAMIC_HALO_UNSOLVED / N6_C_FULLSCENE_OPEN / N8_N9_NOT_AUTHORIZED / PLAY1_H_NOT_AUTHORIZED`.
