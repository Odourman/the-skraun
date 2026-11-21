# THE SKRAUN – PROJECT SOURCE 00: LÄS FÖRST

**Snapshotdatum:** 2026-11-21. **Status:** ChatGPT Project Source-navigering, **inte** ny canon, implementationstillstånd eller ersättare för aktuell GitHub. **Ägare:** MAIN III. Detta är en konsolidering och up-to-date ingångspunkt för chattar som annars börjar i migrations-/P01-/R3-dokument från 16–17 november.

## 1. Regel före varje större uppdrag

Kontrollera **live** GitHub [Odourman/the-skraun](https://github.com/Odourman/the-skraun), gällande branch/commit, bindande beslut och exakt auktoriserat arbetsscope via anslutna verktyg. För ärenden med Google Drive-källor: kontrollera relevanta faktiska Drive-filer, inte bara gamla kopior. Project Sources är daterade snapshots. ChatGPT Memory är **aldrig** sanningskälla för canon, ROM, gate, branch, sha eller leveransstatus. Ett issue/handoff i GitHub startar **inte** en separat rollchatt automatiskt.

## 2. Source-of-truth efter ämne, inte "nyast vinner"

- **Spelregler och användarbeslut:** [DESIGN_DECISIONS_01–60 + senare tillägg](DESIGN_DECISIONS_01-60_2026-11-16.md). Läs datum, formellt beslut och senare uttryckliga korrigeringar. Ingen researchrapport får ändra gameplay ensam.
- **Godkänd Skraun-konst:** [SKRAUN_VISUAL_DIRECTION](SKRAUN_VISUAL_DIRECTION_2026-11-16.md), exakt [U1-LEG1 8×12 A/B source på grafikgren](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json). Äldre P1/P2 "horisontell quadruped" och tidig grön testfigur är arkiv/negativa kontroller.
- **Aktuell status och begränsningar:** [CURRENT_MAIN_STATE](CURRENT_MAIN_STATE_2026-11-17.md) med senare daterade tillägg, men läs **det senaste gällande avsnittet och exakta Issues/Handoffs**, inte äldre "N7 not authorized" som fortfarande finns kvar som historik.
- **Senaste fullständiga N6-C granskning:** [MAIN III N6-C Research II review](MAIN_III_N6C_RESEARCH_II_REVIEW_AND_NEXT_GATE_2026-11-21.md), [Research II originalleverans](https://github.com/Odourman/the-skraun/issues/30#issuecomment-7063415027), [Issue #30](https://github.com/Odourman/the-skraun/issues/30).
- **Nuvarande enda godkända nya implementation:** [N7/F2b bindande ROM DEVELOPMENT II handoff](../handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_N7_F2B_MINIMAL_NTSC_DIAGNOSTIC_AUTHORIZED_2026-11-21.md) och [Issue #31](https://github.com/Odourman/the-skraun/issues/31). N7/F2b är EN diagnostisk 4KiB NTSC-ROM, **inte full spelmotor**, inte N8.
- **Gällande färg-/objektstudie:** [N6 användargodkänd jämförelse](MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md), [N6 färgmodelldata](MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md).
- **Nivå 3 framkomlighet:** [Issue #23](https://github.com/Odourman/the-skraun/issues/23) och [exakt acceptansgrind](MAIN_II_LEVEL3_ARENA_FREE_MOVEMENT_AND_COLLISION_GATE_2026-11-16.md).

## 3. Projektets gällande gate vid snapshot

- **MAIN III är huvudchatt/ledare**; ROM DEVELOPMENT II implementerar bara uttryckligen auktoriserat scope; RESEARCH II är rådgivande; GRAPHICS II får inga tysta konstuppdrag; VERIFICATION II är oberoende.
- **N6-C Issue #30 = OPEN**. RESEARCH II visar avgränsade P0-/P1-motexempel; ingen enhetlig fullt beam-/CPU-/RIOT-säker renderer har bevisats.
- **N7/F2b Issue #31 = auktoriserat men ännu ej byggt/rapporterat vid kontrollen**: 2026-11-21, issue OPEN/0 comments, ingen N7-namngiven experimentgren påträffad i sökningen. När ROM DEVELOPMENT II faktiskt levererar uppdateras status utifrån **verklig commit/build/Stella-evidens**.
- **N8, produktionsintegration, mapperbyte, nya konstpixelmasker, mer gameplay, main merge och oberoende N7-Verification är INTE auktoriserade** av N7-beslutet.
- Inget undantag för att "gå vidare själv" när ett test lyckas.

## 4. Övriga Project Sources i denna uppdateringssvit

- [01 – Spelcanon och grafiska beslut](PROJECT_SOURCE_01_GAME_CANON_2026-11-21.md).
- [02 – Teknisk status, roller och grindar](PROJECT_SOURCE_02_STATUS_GATES_AND_ROLES_2026-11-21.md).
- [Separat förslag till ChatGPT Project Instructions](CHATGPT_PROJECT_INSTRUCTIONS_SUGGESTED_2026-11-21.md). Instruktionstexten ska klistras in i projektets egna instruktioner manuellt och kontrolleras mot nuvarande instruktioner; GitHub kan inte skriva över ChatGPT-projektinställningar.

**OBS:** Historiska Drive-dokument från 16–17 november, tidigare handoffs och README-avsnitt kan fortfarande vara värdefulla för proveniens. De får inte användas som den senaste implementeringsordern.
