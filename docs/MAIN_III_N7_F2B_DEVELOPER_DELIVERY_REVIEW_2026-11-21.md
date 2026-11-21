# THE SKRAUN – MAIN III: mottagning och huvudgranskning av fryst N7/F2b negativleverans

**Datum:** 2026-11-21. **Typ:** MAIN III genomförd begränsad evidensgranskning, **inte** oberoende VERIFICATION.  
**Beslut:** `MAIN_N7_F2B_DEVELOPER_DELIVERY_ACCEPTED_AS_BOUNDED_FAIL / F2B_TESTED_S2_FAIL / N6_C_FULL_ENGINE_OPEN / NO_N8_OR_MORE_ROM_AUTHORIZATION`.

## 1. Exakt fryst underlag

- [ROM DEVELOPMENT II till MAIN via Issue #31](https://github.com/Odourman/the-skraun/issues/31#issuecomment-7063794600). [Draft PR #32](https://github.com/Odourman/the-skraun/pull/32), `experiment/n7-f2b-three-enemy-retrigger-20261121` HEAD `25e5e22ab6eb91aeb69c0926ffa0a822b4fc201d`. GitHub compare mot main = **14 tillagda experiment-/test-/rapporteringsfiler**, inga produktionsändringar/merge; pr draft.
- [Utvecklarens fulla rapport](https://github.com/Odourman/the-skraun/blob/experiment/n7-f2b-three-enemy-retrigger-20261121/docs/n7_f2b/ROMDEV_N7_F2B_HANDOFF.md) blob `3054ad46b315bba4cc7b91117bda0fa59aa4a75f` och [reproducerbar PLAYTEST](https://github.com/Odourman/the-skraun/blob/experiment/n7-f2b-three-enemy-retrigger-20261121/PLAYTEST_N7_F2B.md).
- [Drive ZIP, original](https://drive.google.com/file/d/1ebh28Jv65B-yk-as4UJkb0CNA4jF4kgp/view), **1 988 198 byte**, SHA-256 `2b7d2b7ad044032c049ab791f1e31961d37217b1a7fa78647788f81c3dfe3a04`; MAIN hämtade **de faktiska ZIP-byten**, räknade SHA-256, kontrollerade ZIP-CRC för alla **13** poster och varje intern post mot `SHA256SUMS_BUNDLE.txt`: **11/11 manifestposter matchade**. Alla fyra underliggande Stella-/debugger-ZIP fick ZIP CRC PASS.
- Ur ZIP extraherad verklig ROM `ROM_FINAL/n7_f2b_minimal_ntsc.bin`, **4 096 byte**, SHA-256 `d15c4805b06c562cb76369dfe3efff3a8c9537f28de4945196d198957fc5368f`. ASM `ROM_FINAL/n7_f2b_minimal_ntsc.asm`, SHA-256 `a4d95c17ecad953605c7be8a9e0792c6779bf6af8990f420ff8a517233e25a22`. Båda matchar leveransmanifestet. MAIN har inte själv byggt ett nytt oberoende DASM-test; ursprunglig build anges i [CI](https://github.com/Odourman/the-skraun/actions/runs/44911856432).
- Äkta Stella 6.7.1-körningen för slutlig `25e5e22a` [Actions #44911856432](https://github.com/Odourman/the-skraun/actions/runs/44911856432) är `completed/success` men workflowen kräver uttryckligen **väntat negativt orakel**; grönt jobb är därför inte spelrenderings-PASS. Korrigerade debuggertracen [#44911486185](https://github.com/Odourman/the-skraun/actions/runs/44911486185) bygger en tidigare men byte-ekvivalent NOP-justerad kandidatkällversion och rapporterar `STA RESP1` vid CPU cykler 48–51, scanline 131 och nästa banditeration scanline 133. Rapportens mellanliggande felaktiga PC-trace räknas INTE som giltigt bevis.
- **Viktig skillnad:** Stella är original-TIA-emulering, **inte körning på fysisk 2600-konsol**. Inga påståenden om hardware-in-the-loop skall göras.

## 2. MAIN:s egen omläsning av faktiska bildpunkter

MAIN öppnade i den nedladdade ZIP:en `ARCHIVES/adjusted_original_Stella_12frames.zip` med **13 PNG TIA-bilder `TIA_000..012.png`, alla 320×228**, som härrör från 1400×1000 GUI-captures. Räkna bara `TIA_001..012` som 12 konsekutiva frame-steg efter initialrutans `TIA_000`.

En separat MAIN Python+PIL-omräkning (inte körning av utvecklarens eget orakel) använde R3:s tre originalmasker:
- K1: `18 3C 7E DB 5A 24 66 42`
- K2: `24 7E 5A DB 7E 3C 66 81`
- Ranger: `18 3C 7E 5A 7E 18 24 42`

Med dubblerade 16 fysiska rader, screenshot Y109–124, x=2*(67/83/101 + bit-offset) och observerade Stella RGB blå `(121,194,251)`, grön `(61,151,60)` visar **var och en av alla 12 efterföljande faktiska PNG** följande antal förväntade korrekta pixlar:

| Aktör | Krävda pixlar | Uppfyllda | Fullständigt source-exakta rutor |
|---|---:|---:|---:|
| K1 x67 | 120 | **0** | **0/12** |
| K2 x83 | 136 | **10** | **0/12** |
| Ranger x101 | 112 | **0** | **0/12** |

Samma omräkning överensstämmer per frame med det frysta `ANALYSIS/adjusted_source_exact_12frame_pixel_audit.json`; RGB-hash av de 12 visuellt felaktiga slut-crops är identisk genom den statiska S2-scenen. Orakeln kräver endast **positivt** bevis av väntade pixlar; en separat framtida full-PASS skulle också behöva utesluta extra, felplacerade pixlar och felaktig priority. Det påverkar **inte** giltigheten av denna konkreta FAIL, som redan förlorar majoriteten av nödvändiga pixlar.

**MAIN har därmed själv konstaterat ett konkret negativt pixelresultat på levererade bitmaps**, inte bara läst slutsatsen. Detta är ändå inte den särskilda, oberoende VERIFICATION II-grinden.

## 3. TIA/CPU och övrig scope

- Korrigerat `STA RESP1` startar i den faktiska debuggerbilden vid **scanline 131, CPU-cycle 48** (PC `$F0C9`), enligt levererade `TRACE_03.png` / `TRACE_04.png`. Efterföljande motsvarande `P1Band` position verifierades av utvecklarens spårning först på scanline **133** och är därmed inte en korrekt 16-kontinuerlig-rader kernel. MAIN registrerar detta som utvecklarobserverad debuggerbevisning; separat verifierare ska omköra tidsmåtten, inklusive färgklockor.
- `NUSIZ1=3` och manuell `RESP1` producerar synliga kopior men inte de tre **individuella** R3-figurerna på x67/83/101 med korrekt bitmap och typfärg. **F2b-schemats två faktiskt byggda varianter FÖRKASTAS för testad S2-close.**
- RIOT `$80..$83` + `$90..$BF` = **52B statiskt**; deklarerad stack = 2B statiskt härledd, inte uppmätt highwater; fysisk RAM+stack/full motor fortfarande **OPEN**.
- Scene1 permutation, Scene2 S3 P0 L3, faktisk B/ON-PF X80/X84, BL orb, M0 arrow, HUD, svärdets ~24f varning, 8 banor, gemensam 76cy/262 NTSC fullscen **har inte fått PASS/FAIL av denna körning**. Det är en korrekt STOP efter det primära S2-felet, inte leveransbrist som skall tvinga obehörig fortsättning.

## 4. MAIN-beslut och nästa roll

**ACCEPT AS BOUNDED NEGATIVE DELIVERY:** N7/F2b:s godkända experiment har avslutats enligt den snäva arbetsordern. Skillnaden mellan **build PASS** och **render FAIL** är korrekt registrerad. Ingen ny N7-iteration eller annan ROM kodas utan separat beslut; PR #32 skall förbli **draft/unmerged**, ingen N8-implementering eller ändrad art/gameplay.

**Nästa säkraste grind:** en **separat, explicit auktoriserad, read-only VERIFICATION II** av den frysta negativa S2-leveransen (integritet/kompilering/Stella pixelorakel och första scanline-fel). Självtest och MAIN:s egen manuella omräkning är inte samma sak som detta. Självständig verifiering får **inte** förväxlas med godkännande att försöka fler rendereridéer eller att minska antalet tre samtidiga fiender.

**Beslut som kräver ytterligare strategiskt ställningstagande efter VERIFICATION II:** antingen ett snävt RESEARCH II-spår med ett faktiskt nytt självständigt fysisk-kernel-förslag med dokumenterad kostnad, eller ett medvetet användarval av grafik-/visningskompromiss som bevarar gameplay. Påstå inte att "tre fiender är omöjliga" baserat på dessa två F2b-varianter.

**Gällande canon skyddad:** användargodkänd ljusgrå upprätt U1-LEG1, två ljusblå riddare som designriktning, världskamouflerad Ranger, tre samtidiga fiender fortsatt mål, guldhalo, liten orb och smidig level3-rörlighet med öppna banor. Inga nya färg-/storlekspixlar auktoriserade.

**Disposition:** `N7_F2B_DEVELOPER_SCOPE_DONE_BOUNDED_FAIL / MAIN_REVIEW_DONE / INDEPENDENT_VERIFICATION_PENDING / N6_C_FULL_ENGINE_UNPROVEN / N8_NOT_AUTHORIZED`.
