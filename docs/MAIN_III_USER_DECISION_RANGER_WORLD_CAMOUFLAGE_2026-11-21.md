# THE SKRAUN — Användarens beslut: Ranger kamoufleras efter värld

**Datum:** 2026-11-21. **Auktoritet:** uttryckligt senare användarbeslut om VISUELL karaktärsidentitet. **Ändrar inte gameplay, TIA-teknisk status, fiendemasker, ROM eller mapper.**

## Exakta användaruttalanden

1. "Jag tycker att bågskytten ska vara kamouflerad. Det ska vara poängen. Han är en Ranger som gömmer sig i miljön"
2. "På skogsbanan kan den vara grön. På dröm banan lila som spiralerna i bakgrunden...osv..."
3. 2026-11-21 gav användaren MAIN uppdraget "Vi börjar med 1 **N6 – Ta fram en gemensam grafikarkitektur**" inklusive "Vi måste fundera på vilka färger och hur vi ska göra för att spelet ska fungera så tekniskt bra som möjligt."

## Beslut och företräde

Den tidigare generiska formuleringen i [beslut 01–60](DESIGN_DECISIONS_01-60_2026-11-16.md) och tidigare [N3 S1–S9](MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md) att bågskytten alltid måste vara grön är **ersatt endast i denna färgfråga**. Ranger har världsbundet miljökamouflage med användarens uttryckliga exempel **grön skog** och **lila drömvärld**. Bergs och nattvärldens exakta kulörer är ännu inte uttryckligen användargodkända; förslag stenblå och dimblå får endast behandlas som kandidater. Ingen exakt PAL/NTSC TIA-hexfärg låses utan test.

- Ranger är fortfarande samma flyende/skjutande fiendetyp som beslutat; fritt X/Y, synlig i alla giltiga spellägen, samma AI, samma poäng och svårighetsregler.
- "Gömmer sig" är **avsedd kamouflageutmaning**; inte automatisk osynlighet, stöld av svärdsförvarning, minskad pilvarning eller försvinnande ur sprite-/kollisionsmodellen.
- Deras exakta R3 gamla gröna `$C6` skärmbilder är frysta historiska prover för tidigare R3, inte en order att färga alla fyra världarna gröna.
- Se [N6 kombinatorisk register-/färgstudie](MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md) för tekniskt **föreslagen** två-identiska-röd-knights, världscamo-ranger, gold PF/BL, gray P0/M0. Den skapar inga nya kanoniska färgbytesvärden eller en fungerande rendering.
