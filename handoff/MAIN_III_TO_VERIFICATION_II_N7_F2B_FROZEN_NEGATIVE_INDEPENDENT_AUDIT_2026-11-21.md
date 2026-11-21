# THE SKRAUN – MAIN III → VERIFICATION II: oberoende N7/F2b negativ-S2 revision

**Utgiven av:** MAIN III. **Datum:** 2026-11-21. **Typ:** SEPARAT, UTTRYCKLIG VERIFICATION-AUKTORISATION, **endast** fryst N7/F2b-bevis, ingen implementation.  
**Resultat ska levereras tillbaka till MAIN III**, inte användas för automatisk utveckling/merge eller nya steg.

## 0. Bindande scope och verifieringsroll

Du är **VERIFICATION II**, oberoende av ROM DEVELOPMENT II. Du får läsa, reproducerbart bygga, testa och granska en fryst avgränsad experiment-FAIL; du får **inte** ändra ROM/assembler/ursprungliga tester, åtgärda defekter, skapa gameplaykompromisser, beställa RESEARCH eller börja N8. Eventuella **egna** verifieringsskript måste läggas separat från fryst utvecklarkod och märkas som verifierarens material. Läs först [din migrationsöverlämning](https://github.com/Odourman/the-skraun/blob/main/handoff/VERIFICATION_II_MIGRATION_2026-11-17.md), sedan [MAIN III:s actual evidence receipt](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N7_F2B_DEVELOPER_DELIVERY_REVIEW_2026-11-21.md).

Kontrollera live GitHub/Drive-åtkomst och följ source authority. Project Sources, chattminne eller en gammal migration är inte självständiga tekniska bevis.

## 1. Frysta bytes, status och originalkällor

- [N7 Issue #31](https://github.com/Odourman/the-skraun/issues/31#issuecomment-7063794600), [draft PR #32](https://github.com/Odourman/the-skraun/pull/32).
- Exakt fryst experiment-commit `25e5e22ab6eb91aeb69c0926ffa0a822b4fc201d` på branch `experiment/n7-f2b-three-enemy-retrigger-20261121`; **fäst dig vid SHA, inte bara ett rörligt branch-namn**.
- [Leverantörens tekniska slutrapport vid fryst commit](https://github.com/Odourman/the-skraun/blob/25e5e22ab6eb91aeb69c0926ffa0a822b4fc201d/docs/n7_f2b/ROMDEV_N7_F2B_HANDOFF.md), [PLAYTEST](https://github.com/Odourman/the-skraun/blob/25e5e22ab6eb91aeb69c0926ffa0a822b4fc201d/PLAYTEST_N7_F2B.md), [ASM](https://github.com/Odourman/the-skraun/blob/25e5e22ab6eb91aeb69c0926ffa0a822b4fc201d/experiments/n7_f2b_minimal_ntsc.asm).
- [Fryst Drive slutligt ZIP](https://drive.google.com/file/d/1ebh28Jv65B-yk-as4UJkb0CNA4jF4kgp/view), förväntad exakt längd **1 988 198 byte**, SHA-256 `2b7d2b7ad044032c049ab791f1e31961d37217b1a7fa78647788f81c3dfe3a04`; 13 ZIP poster.
- Slutlig ROM **4096 byte** SHA-256 `d15c4805b06c562cb76369dfe3efff3a8c9537f28de4945196d198957fc5368f`; ASM SHA-256 `a4d95c17ecad953605c7be8a9e0792c6779bf6af8990f420ff8a517233e25a22`.
- Äkta corrected-PC build/trace [GitHub Actions #44911486185](https://github.com/Odourman/the-skraun/actions/runs/44911486185) och slutlig utvecklaroracle/12-step Stella [#44911856432](https://github.com/Odourman/the-skraun/actions/runs/44911856432). Ett gammalt justerat workflow med föråldrade PC-breakpoints är **ogiltigt som timingbevis**.
- Datakontrakt: [N3 S0–S9 fixtures](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json), R3 source för K1/K2/Ranger, U1-LEG1/Skraun om relevant. Endast S2-close `K1 X67,K2 X83,Ranger X101,Y78` kvalificerades fysiskt innan första FAIL.

## 2. Oberoende verifieringspaket – strikt begränsade frågor

**V1 Integritet och build:** ladda ner fryst repo ZIP/ASM/BIN och Drive-paket på nytt; kontrollera byte- och SHA-ankare, dolda ändringar, ZIP CRC och eventuella inre manifest. Kompilera självständigt med DASM med exakta flaggor, bekräfta 4KiB SHA, resetvektorer, 6507/TIA och att branch/PR inte är mergad i main. Om verktyg/Drive saknas, redovisa BLOCKED; påstå inte byte-PASS från metadata.

**V2 Egna riktiga Stella-bilder:** kör den faktiska ROM:en i en separat Stella 6.7.1/NTSC-miljö och ta **minst 12 sammanhängande framesteg** efter deterministisk initiering. En reproducerbar orakel med **alla nödvändiga och även förbjuda/extra pixlar**, källa 8 maskerad byte ×2 fysiska rader, 8-bit P1 aktör, rätt X/typfärg ska redovisa K1/K2/Ranger var för sig. Skilj synliga blå/gröna kopior från **källkorrekt** figur; kontrollera att färgkod→verklig RGB, cropkoordinater och dubbelrad är spårbara. Förväntat från MAIN:s eget test av levererade PNG: K1 0/120, K2 10/136, Ranger 0/112 pixels/vald frame och 0/12 korrekt per aktör. **Reproducera själv**, inte kör bara utvecklarens Python-orakel som solevidens. Om avvikelse, exponera första exakta bit/pixel/kolumn och varför.

**V3 Opcode/beamdeadline:** bygg egen debugger-trace av `P1Band` över två intilliggande fysiska rader: dokumentera `STA RESP1` på PC `$F0C9`, fysisk scanline 131, cykler 48–51 och nästa motsvarande instruktionsförekomst på scanline **133** enligt utvecklaren. Visa råa skärmdumpar/loggar och **särskilj cycle, pixel position och color clock**. Om det inte går att reproducera: `INCONCLUSIVE` eller `COUNTEREXAMPLE`, inte automatisk verifiering.

**V4 Scope och STOP:** gör INTE S2 permutation, S3, B/ON PF, BL orb, M0, HUD, AI eller svärdsvarning till falska PASS. Statisk RIOT 52B och ~2B JSR-stack är **inte verklig högvattenmätning**; kontrollera detta scopeomdöme. Ingen 76cy/262-NTSC fullscene pass genom att några debugsteg syns. Två levererade varianter i S2; enbart EN NOP borttagen. Inga fler utvecklingstester på fryst ROM.

**V5 Rapport och beslut:** utfall måste vara `CONFIRM_BOUNDED_NEGATIVE`, `REFUTE_DEVELOPER_EVIDENCE` eller `INCONCLUSIVE`. Skriv criterion för criterion PASS/FAIL/NOT_TESTED/BLOCKED med råbevis, exakta SHA, nybyggnad, script/kommando, bilder, tidsstämplad Stella trace och *första* felande bit/scanline. Egen granskning **är inte** en ny spelrendererkod. Rapportera till MAIN III via GitHub Issue #31 samt separat verifieringsdokument och bifoga/referera original/eget evidenspaket.

## 3. Inga nya befogenheter genom denna handoff

- Endast **fryst negativ S2-grind** får oberoende verifieras. Varken VERIFICATION II eller MAIN:s egen omräkning får påstå att **alla** möjliga F2b-kombinationer är omöjliga.
- Ändra INTE `main`, `experiment/n7-f2b-three-enemy-retrigger-20261121` eller dess ASM/ROM/testdata. Gör inte PR merge; N8 fortsatt **inte auktoriserad**. Inga nya gameplay-/sprite-/Ranger-/halo-/Skraun-förenklingar utan separat användarbeslut.
- Ingen annan roll aktiveras automatiskt genom att detta finns på GitHub. Den separata VERIFICATION II-chatten måste **aktivt** öppna länken och kontrollera tillgång.
- MAIN III granskar din leverans, bedömer om N6-C eller teknisk arkitektur ska få ett annat **framtida** beslut. Denna granskningsorder är INTE en förevändning för ny ROM-utveckling.

**Status:** `N7_F2B_DEVELOPER_BOUNDED_FAIL_MAIN_ACCEPTED / VERIFICATION_II_SEPARATELY_AUTHORIZED / VERIFICATION_EXECUTION_NOT_YET_CONFIRMED / N6_C_FULL_ENGINE_OPEN / N8_NOT_AUTHORIZED`.
