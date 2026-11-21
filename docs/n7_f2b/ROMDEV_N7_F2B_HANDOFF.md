# THE SKRAUN – ROM DEVELOPMENT II → MAIN III: N7/F2b TECHNICAL HANDOFF
**2026-11-21 | FROZEN BOUNDED DIAGNOSTIC | F2b_FAIL_FOR_TESTED_SCENE**
**Issue:** [#31](https://github.com/Odourman/the-skraun/issues/31) | **Draft PR:** [#32](https://github.com/Odourman/the-skraun/pull/32) | **Branch:** `experiment/n7-f2b-three-enemy-retrigger-20261121`.

## 1. Beslut
**FAIL – F2b för den faktiskt implementerade original-TIA-sekvensen i S2-close, inklusive exakt EN snäv tidsjustering.** Det finns **inget** autentiskt tre-fiender-PASS: exakt egen source-bitmap, x67/83/101 och egen typfärg visas inte samtidigt 16/16 fysiska rader. **Inte** ett generellt omöjlighetsbevis för all F2b-teknik, inte ny fullspelsgrind eller oberoende Verification. Arbetet har STOPPATS i enlighet med MAIN III:s uttryckliga arbetsorder.

## 2. Auktoritativa källor och orakel
- [MAIN III order](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_N7_F2B_MINIMAL_NTSC_DIAGNOSTIC_AUTHORIZED_2026-11-21.md), [N3 exakta scen-fixtures](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json), [N6 beslut](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md).
- [RESEARCH II N6-C – source-only](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/RESEARCH_II_N6C_PHYSICAL_P1_DECISION.md), ursprungliga R3-maskerna och [U1-LEG1 källa](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json).
- **S2 close:** K1 x67, K2 x83, Ranger x101, alla logical arena Y78, 8 original-source-rader dubblerade till 16 fysiska rader:
  - K1 `18 3C 7E DB 5A 24 66 42`
  - K2 `24 7E 5A DB 7E 3C 66 81`
  - Ranger `18 3C 7E 5A 7E 18 24 42`
  - Gemensam symbolisk knight `COLUP1=$9E`, Ranger `$C6` (diagnostikvärden, **ej** fast konstpalett).
- Källa rymmer Scene0 S2, Scene1 permuterad S2 och Scene2 S3; endast Scene0 har körts och pixelklassats som faktisk Stella-resultat eftersom FAIL/STOP gäller.

## 3. Maskinbyggt original-6507/NTSC-artefakt
**Assembler:** `experiments/n7_f2b_minimal_ntsc.asm` med kod/data för originella maskerna, P0 U1-LEG1 A i L3, P1 `NUSIZ1=3` + explicit per-rad `RESP1`, `GRP1/COLUP1`, `VDELP1=0`, `HMOVE` i VBLANK. **Ingen** 20Hz-helframe-slottrick och ingen tyst fiende-Y-offset.
**DASM:** `dasm experiments/n7_f2b_minimal_ntsc.asm -f3 -oexperiments/n7_f2b_minimal_ntsc.bin -lexperiments/n7_f2b_minimal_ntsc.lst -sexperiments/n7_f2b_minimal_ntsc.sym`.
DASM på riktig Ubuntu-runner **SUCCESS**; 4 096 bytes; källkod, **faktisk BIN**, listing, symbols och manifest finns på N7-grenen.
- **Slut-ROM SHA256:** `d15c4805b06c562cb76369dfe3efff3a8c9537f28de4945196d198957fc5368f`
- **Slut-ASM SHA256:** `a4d95c17ecad953605c7be8a9e0792c6779bf6af8990f420ff8a517233e25a22`
- Första versionens ROM SHA256: `45b8fa0045383438f5b3bcc9d09b2cfac3f91a9b9822d0d5a7124e71c44ad361`.
- [Build+bilder från original](https://github.com/Odourman/the-skraun/actions/runs/44910859681), [bygg+bilder justerad](https://github.com/Odourman/the-skraun/actions/runs/44911307187), [automatiskt arkiverad BIN+listing](https://github.com/Odourman/the-skraun/actions/runs/44911486236).

## 4. Faktiska Stella-bilder (inte Python-mockup)
Autentisk Stella 6.7.1 körde den **faktiskt kompilerade ROM** i Xvfb. Tolv konsekutiva kommandon `frame #1` efter `frame #10` sparade **13 skärmdumpar vardera (initial + 12 efterföljande)** för original och justerad. TIA-utsnitten är 320×228 bildpunkter ur riktiga Stella Debugger-UI. Alla innehöll synlig färgad grafik och reproducerbart identiska RGB-data mellan rutorna i respektive statiska S2-test. Det är alltså **100% temporär persistens av den FELAKTIGA bilden**, inte 60Hz korrekta tre fiender.
- S2 original första källmask-miss på arena y78, screenshot y109, i den relevanta fienderaden; blue + camo visas men på fel X/med fel masks. Ytterligare 12 icke-önskade färgade pixels på nästa screenshotrow y125 (17:e row), korrigerade i justeringen.
- **Source-exakt pixelklassning av justerade fångster mot R3 original för 12/12 rutor:** K1 **0/12 fulla rutor**, K2 **0/12**, Ranger **0/12**. För varje ruta i den strikta byte/X/färg-baserade orakeln: K1 **0/120** förväntade TV-pixlar på korrekt X/Y/färg, K2 **10/136**, Ranger **0/112**. Därför **FAIL** trots visible sprites. Källmasker hos olika K1/K2/Ranger är inte utbytbara.
- **Flickerduty:** Den felaktiga bilden förblir i 12/12 fångster. Duty för var och en av de TRE *korrekta* fienderna är däremot **0/12**; ingen helfigur i rätt X/Y/färg enligt oraklet. Missförstå inte som att det bara finns svart bild.

## 5. Autentisk Stella debugger register-/deadline-spårning
**Baslinje:** [körning #44911067327](https://github.com/Odourman/the-skraun/actions/runs/44911067327), [råa bilder i Drive](https://drive.google.com/file/d/1Ix7D8Hc3kgKdvit453yTIoFOW9ks24Z5/view). Verkligt `STA RESP1` vid PC `$F0CA`, fysisk scanline **131**, **CPU-cykel 50–53**, colorclocks **150–159**. Samma PC i bandloopen nås först på **scanline 133** (inte 132) för nästa rad. Inget komplett korrekt 16-row output.
**EN timingjustering:** exakt **EN `NOP` (2 CPU-cykler)** bort från samma P1Band; inga ändrade R3-maskar/positioner, inga nya ägare/mapper och **ingen ytterligare arkitekturrevision**. Slut-ROM ovan.
**Korrigerat slut-ROM PC-spår:** [körning #44911486185](https://github.com/Odourman/the-skraun/actions/runs/44911486185), [Drive](https://drive.google.com/file/d/19ojDhXYTOqKQUnMVeajwHZLgTKgOw4ld/view): `STA RESP1` nu på PC `$F0C9`, fysisk scanline **131**, CPU-cykel **48–51**, colorclocks **144–153**. Nästa motsvarande PC når fortfarande scanline **133**. Skärmbilder `TRACE_03.png` (före), `TRACE_04.png` (efter) och `TRACE_10.png` (nästa). **F2b-fail kvarstår**.
En *mellanliggande trace-artefakt* efter ändringen hade gamla PC-breakpointadresser: den är **OGILTIG** som instruktionsmätning trots grönt workflow. Detta är åtgärdat i ovan sluttrace. Loggen visar `runToPc` och actual `step #1`; det är TIA-Debugger, inte source-only aritmetik.
**Hårdvarugrind:** 76 6507 CPU-cykler/fysisk rad; när P1Band-iterationer hoppade över en fysisk rad är det inget PASS för 16 heldubblerade källrader. Ingen falsk worst-row-/konsistent-262-frames-maskinläsbar complete trace påstås; bara visade real debugger scanline/cycle/position.

## 6. RAM/stack/ROM – bevisklass
ROM **4KiB konstaterat i verkligt DASM**, inga bankers eller coprocessor. `$80..$83`: fyra bytes scene/frame/color; `$90..$BF`: 3×16=48 bytes P1 originaldata i RIOT RAM, totalt **52B statiskt allokerade**. Max en aktiv `JSR`-retur i vår synliga käll-callgraph ger en *statiskt härledd* stack på **2B**. Med 128B fysisk RIOT och stack sammanräknat återstår ungefär **74B**, men **ingen riktig högvattenmätning av stacken** genom Stella Debugger har validerats. Den tidigare R3:s 89B buffer får inte smygsummas på dessa 52B. Fullspels-integration, BL/M0/HUD/fiendelogik, stabil 262-line frames och worst-case R3 PF-komposit är **inte bevisade**.

## 7. Scopebegränsning / negativa kontroller
- **S2:** F2b testad och **FAIL** → arbetsorderns stoppgrind utlöses. Två build-varianter inklusive maximalt EN timingjustering.
- **S2 permuterad, S3 P0 L3 x104+fiender x105/124/147, S1 vid X32/101/147:** kodad scen-data respektive föreskrivna framtida kontroller men **inte legitimt testade i riktig Stella med 12-exakt bilder** innan STOP. Inga S3 P0-integritets- eller collision-PASS påstås.
- **P3 B/ON PF maskerna** i slut-ROMs testdata: x80 vänster `00 00 0C`, höger `40 50 00`; x84 vänster `00 00 14`, höger `40 30 00`. **Endast ROM-data. INGEN fysisk PF-rad-PASS.** BL delar COLUPF, reserverad orb; M0 delar COLUP0, reserverad arrow; M1/HUD/24-frame sword/AI saknas avsiktligt.
- R3:s tidigare 20Hz per enemy är historisk negativ kontroll, inte ersättning för felet och inte kodad som fusk-PASS.
- Ingen oberoende VERIFICATION, main-merge, slutspels-GO, N8 eller ny konst.

## 8. Länkar till frysta bevis
| Material | URL | Bevis |
|---|---|---|
| Slutlig branch/PR + BIN/LST/SYM/SHA256 | [Draft PR #32](https://github.com/Odourman/the-skraun/pull/32) | källkod och verkligt DASM-artefakt |
| Original Stella 12-frame | [Drive original](https://drive.google.com/file/d/1k6xVjNUd6Mb9pHvzfvMcK4On9XhmdJCw/view) | faktisk Stella 6.7.1, första FAIL |
| Timingjusterad 12-frame | [Drive justerad](https://drive.google.com/file/d/1k_G4Fff_2ed3d_HiBX7ZzB9LdGQ7O7Mq/view) | fysisk verifiering efter EN NOP |
| Baslinje debuggerinstruktion | [Drive initial trace](https://drive.google.com/file/d/1Ix7D8Hc3kgKdvit453yTIoFOW9ks24Z5/view) | $F0CA 50→53 |
| Korrigerad debuggerinstruktion | [Drive sluttrace](https://drive.google.com/file/d/19ojDhXYTOqKQUnMVeajwHZLgTKgOw4ld/view) | $F0C9 48→51 |
| Reproduktion | [PLAYTEST](../../PLAYTEST_N7_F2B.md) | commands and evidence hygiene |

## 9. Överlämning och STOP
**Technical result: `F2b_FAIL_FOR_TESTED_SCENE`.** MAIN III avgör själv nästa gate eller eventuellt separat användarbeslut. ROM DEVELOPMENT II gör inga ytterligare ändringar i P1, N7, N8, renderer/full motor, grafik eller main; inga självständiga VERIFICATION-anspråk.
