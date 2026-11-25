# THE SKRAUN – HEALTH-2 handoff till MAIN V

**Datum:** 2026-11-25  
**Isolerad gren:** `experiment/health2-deep-debug-optimization-20261125`  
**Baseline ROM:** F6 NTSC, 16 384 byte, SHA-256 `bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5`

## Resultat

- HEALTH-2 sparar nu hela 128-byte RIOT RAM-dumpen per naturlig joystickscen och kontrollerar avsett tillstånd tillsammans med `_scanEnd`. Syntetiska fixtures och naturliga speltester hålls åtskilda.
- Senaste Actions [#45672925822](https://github.com/Odourman/the-skraun/actions/runs/45672925822): 9 PASS, 3 FAIL, 1 UNPROVEN. Stage 2/Level 2-övergången fick separat PASS. Den äldre `stage2_L3`-scenen når Stage 2/Level 2, inte Level 3. Ranger draw/release-scenerna missar sina avsedda tillstånd. GameOver följt av restart är obevisat.
- 120/120 individuellt mätta NTSC-frame-endpoints är 262 rader. Det bevisar inte 76 CPU-cykler per rad eller TIA-skrivningars beam deadlines.
- Stella-sessionerna hittade inte förväntade `.sym`/`.lst`-filer. Den nya dynamiska cycle-summeringen stannade fail-closed; inga dynamiska CPU-countervärden rapporteras.
- Stack high-water och RAM-livslängder är inte mätta. `_sp=$FF` efteråt är endast punktmätning.
- DASM byggde shared fine-positioneringskandidat. Källmodellen ger +5,31 cykler i medel och regressionsfönster −8…+20; den är långsammare vid 105/160 X och avvisas. Fysisk pixel-/TIA-jämförelse saknas.
- Ingen ny halo-kontur, renderer för tre fiender, full kollisions-/framkomlighetsmatris eller naturlig komplett banloop har bevisats.

## MAIN V:s nästa beslut

1. Reparation av Stella symbol-/listing-laddning med verifierad absolut sökväg, ROM SHA, bank och debugger-PC.
2. Mät ett dyrt raster-/INTIM-path med faktisk per-scanline cycle- och TIA-write timing.
3. Lägg till stack sentinel/high-water i separat diagnostisk build och först därefter stressa kombinerad halo, attacker, pil, HUD, ljud och stage-byte.
4. Håll positioneringspatchen avvisad. Nästa kandidat ska ha fysisk TIA-position och pixel oracle innan den kan räknas som förbättring.

Fullständig redovisning, fyndregister, evidensklassificering och kvarstående risker finns i [01_HEALTH2_FINAL_REPORT.md](01_HEALTH2_FINAL_REPORT.md). Hela native DASM/Stella artefakten finns på [Actions run #45672925822](https://github.com/Odourman/the-skraun/actions/runs/45672925822).

**Bevisstatus:** developer-observed/source-only. Ingen MAIN review eller oberoende Verification har utförts. Ingen ändring gjordes i aktiv ROMDEV-gren, `main`, mapper eller spelcanon; ingen merge eller release.
