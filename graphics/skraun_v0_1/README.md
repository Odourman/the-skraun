# The Skraun – GRAPHICS: pixelkandidater v0.1 (2026-11-16)

**Status:** Grafiskt designunderlag, ej MAIN-godkänt, ej Stella-testat, ej ROM-integrerat, ej oberoende verifierat.

## Uppdrag
GRAPHICS har studerat användarens **privata** originalteckning i Google Drive samt de bindande [60 spelbesluten](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [visuell riktning](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [MAIN:s designavstämning](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_POST_R3_VISUAL_DESIGN_REVIEW_PROPOSAL_2026-11-16.md) och tidigare autentiska Stella-bilder. Originalfotot har **inte** kopierats hit.

## Tre 8×12-pixelkandidater
- **A – Originalnära:** mer igenkännbar än den äldre P01-stillposen, men huvudet dominerar fortfarande.
- **B – Lång kropp:** tunnare, riskerar att se för spinkig ut i spelstorlek.
- **C – Tydliga tassar:** **rekommenderas till MAIN för estetiskt beslut**, eftersom framben och bakben går att särskilja bäst. Detta är ingen konstnärlig acceptans.

Samtliga levereras i två gångposer A/B. Vänsterbild är exakt horisontell spegling av respektive högerbild. Logisk rad 0 innehåller öronen (`%00100100`); logisk rad 11 innehåller fötterna (`%11000011`). Raderna är lagrade **top-first** i `sprites.json`.

Lämpliga teststorlekar från befintlig P01-prototyp: NUSIZ0 0/5/7 ger 8/16/32 color-clock-bredd och 12/24/36 scanlines med radrepetition. Grått `COLUP0=$0C` är ett förslag, inte en beslutad slutpalett.

### Dokument
- `sprites.json` – exakta källbitmappar.
- `SKRAUN_PIXEL_DATA.inc` – grafiktabeller `dc.b`, både top-first och bottom-first; **inte en färdig ROM**.
- `skraun_C_preview.svg` – direkt genererad pixelperfekt designförhandsvisning, ingen Stella-skärmbild.

**Teknisk varning:** Använd inte 12-byte-tabellerna direkt i R3-VFIX:s 177-indexerade buffert. En faktisk integrationsgren behöver kontrollera radordning, X-spegling, 76-cykelbudget, P0/P1-konkurrens och visuellt resultat i Stella. R3 same-Y-fiendeflimmer (20 Hz) och PF-halo/hinder-konflikten är inte lösta av detta konstmaterial.

**Status:** [Issue #15](https://github.com/Odourman/the-skraun/issues/15) ska fortsätta vara öppet tills MAIN uttryckligen godkänner grafiken. Inga nya implementationssteg, ROM-kodändringar eller merge görs här.
