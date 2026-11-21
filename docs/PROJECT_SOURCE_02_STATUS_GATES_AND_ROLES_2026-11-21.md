# THE SKRAUN – PROJECT SOURCE 02: TEKNISK STATUS, ROLLER, STOPPGRÄNSER

**Snapshot:** 2026-11-21. Aktuell status måste alltid verifieras mot live GitHub före handling. **Inga regler i denna text auktoriserar implementation utöver befintlig N7/F2b-order.**

## 1. Snapshot av verklig status

| Område | Status | Primärkälla |
|---|---|---|
| Godkänd nivå-1-spelarbild | U1-LEG1 8×12 A/B positivt godkänd som design, inte generell körande ROM-art | [Visuell riktning](SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [fryst grafik](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json) |
| Äldre P01/P02/R3 | Delvisa autentiska DASM/Stella-egenkontroller, *inte* en godkänd fullscen; R3 same-Y 20Hz och PF-konflikter otillräckliga | [CURRENT_MAIN_STATE](CURRENT_MAIN_STATE_2026-11-17.md), [N5](MAIN_III_N5_P1_SAME_Y_FEASIBILITY_AND_GAME_DECISION_2026-11-17.md) |
| N6-C full scen | **OPEN**: endast source-only delmodeller, inga bevis för gemensam beam-safe 76c/128B-grafikmotor | [#30](https://github.com/Odourman/the-skraun/issues/30), [MAIN-review](MAIN_III_N6C_RESEARCH_II_REVIEW_AND_NEXT_GATE_2026-11-21.md) |
| RESEARCH II | Källbaserad rapport från separat gren, bounded results accepted av MAIN | [Issue #30 RESEARCH](https://github.com/Odourman/the-skraun/issues/30#issuecomment-7063415027), [MAIN-review](MAIN_III_N6C_RESEARCH_II_REVIEW_AND_NEXT_GATE_2026-11-21.md) |
| N7/F2b | **Explicit godkänt för ROM DEVELOPMENT II, en minimal diagnostisk 4K NTSC ROM – ännu inte utfört vid denna snapshot** | [#31](https://github.com/Odourman/the-skraun/issues/31), [bindande handoff](../handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_N7_F2B_MINIMAL_NTSC_DIAGNOSTIC_AUTHORIZED_2026-11-21.md) |
| N8/full spelmotor/merge/extra mapper | **Inte auktoriserat** | [#31](https://github.com/Odourman/the-skraun/issues/31) |
| Oberoende N7 Verification | **Inte auktoriserad/utförd**; framtida separat order efter fryst utvecklarleverans | [#31](https://github.com/Odourman/the-skraun/issues/31) |
| L3-banornas rörlighet | Bindande krav men faktisk 8-kartors kollisionsverifiering ännu OPEN | [#23](https://github.com/Odourman/the-skraun/issues/23) |
| Andra tester | Global visuell grind #15, ART1 L3 första-radproblem #19, P01 independens #1 kvar öppen/ej slutgiltigt PASS | [Issues](https://github.com/Odourman/the-skraun/issues) |

**Kontroll vid framställning:** Issue #31 var OPEN med 0 kommentarer och sökning efter N7-gren gav inga träffar 2026-11-21. Detta är inte en försäkran om status i framtida chattar. När en verklig N7-commit publiceras är denna rad föråldrad och ska ersättas genom en ny daterad status/Project Source.

## 2. Vad N7 exakt får och inte får göra

**Tillåtet efter användarens "Ok, bra fortsätt":** ROM DEVELOPMENT II får bygga EN separat reproducerbar 4KiB original-Atari-2600 NTSC F2b-test-ROM med riktiga `NUSIZ1/RESP1/GRP1/COLUP1`-tidstämplar; prova två ljusblå R3 knight-masker och en kamouflerad Ranger med tre fria X på Y78 (S2-close X67/83/101), plus S3 med P0 L3 Skraun samtidigt. Kontrollera 12 sammanhängande bildrutor, max76 CPU-cykler/rad, TIA beam-deadlines, NTSC 262 och RAM128B incl stack. Källankrad B/ON guld-PF X80/X84 som deltest; reservera M0 arrow/BL orb/HUD är inte samma sak som faktiskt ritad helscen. Kräv källkod, binär om byggbar, DASM/Stella/Debugger-loggar, hashes och första konkreta FAIL. En misslyckad ärlig diagnos uppfyller uppdragets syfte.

**Inte tillåtet:** Automatisk N8/full gameplay, AI, rörelse-/kollisionsmotor, nya användargodkända bitmaps, release, main-merge, ändrat antal fiender, sänkt spelkrav, ny mapper, oberoende Verification utan separat beslut. 24f svärdsvarning saknar godkänd source-pose och är en senare separat visuell testgrind.

## 3. Roller och arbetsgränser

- **MAIN III:** leder, granskar primärbevis, accepterar/avslår scope-gates och registrerar beslut. Får inte kalla ROM DEVELOPMENT:s egenkontroll oberoende Verification.
- **ROM DEVELOPMENT II:** implementerar endast aktuell specifik N7/F2b-order, bygger med DASM, kontrollerar i Stella Debugger, levererar full evidens. Ingen fri fortsättning till N8 eller produktion.
- **RESEARCH II:** rådgivande, käll- och dokumentstudier med reproducerbara bevis. Ingen ROM-kod eller canonbyte utan separat order.
- **GRAPHICS II:** separat auktoriserad konst/sprites/bana; aktuell N7-order innehåller INTE ett nytt grafikuppdrag.
- **VERIFICATION II:** bygger/testar **oberoende** först efter särskild MAIN-order och fryst överlämning. Granskar inte sitt eget producentarbete.
- **Användaren:** tar ställning till väsentliga konst-, gameplay- och hårdvarukompromisser. Ett uttryckligt godkännande av ett avgränsat steg är inte godkännande av kommande steg.

## 4. Projektets hårdvarusanning

Original Atari 2600: **76 6507 CPU-cykler per fysisk rasterrad, 128B RIOT RAM inklusive stack**. Två player-objekt, missiles M0/M1, Ball, PF, BK och delade färgdomäner `COLUP0` P0/M0, `COLUP1` P1/M1, `COLUPF` PF/BL. 4KiB-prototypformat gäller aktuellt N7-test, inte bevis för framtida slutlig kassettstorlek.

**Research II:s bounded counterexamples**: F1 P0-only som tredje slot faller i S1/S3 vid P0-busy 16/16; F2a en vanlig P1 huvudkopia/linje har 5/16 approximerade `RESP1` prepositioneringskonflikter i S2 close; naiv heltids-`GRP1/COLUP1` i gap faller i 7/16 S2 och 3/16 S3, men förladdade stores kan i source-modell undgå dessa isolerade gap. **F2b NUSIZ/RESP1 retrigger är fortfarande obevisat, inte uteslutet.** Inga ett-i-taget träffsäkra P1-prover är fullspels-GO. Se [granskningen](MAIN_III_N6C_RESEARCH_II_REVIEW_AND_NEXT_GATE_2026-11-21.md).

## 5. Uppdateringsprotokoll för Project Sources

Efter varje avslutad implementations-/Verification-/användarbeslutsgrind: MAIN granskar konkret source, ROM, SHA, issue och test; skriver ny kort daterad snapshot; instruerar användaren att ersätta eller avmarkera gammal ChatGPT Project Source och Project Instructions. **Aldrig tyst ändra historiska dokument eller låta två inkompatibla "CURRENT" vara primära.** ChatGPT Project-instruktionerna kan inte ändras genom en GitHub-commit; användaren måste klistra in den gällande texten i Project-inställningarna.
