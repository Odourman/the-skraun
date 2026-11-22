# THE SKRAUN – ROM DEVELOPMENT II → ROM DEVELOPMENT III

**Migrationsdatum:** 2026-11-22. **Dokumenttyp:** roll- och källöverlämning, INTE ny implementationsorder, canonändring, gameplaykompromiss, oberoende verifiering eller main-merge.

## 0. Läsordning, auktoritet och livekontroll

Börja med ChatGPT Project Sources 00–04, men behandla dessa filer som daterade navigationssnapshots (2026-11-21) – de slutar före PLAY1/PLAY1-H/PLAY1-X. Kontrollera varje ny fråga om aktuellt läge mot live GitHub och vid behov Google Drive.

1. Projekt: https://github.com/Odourman/the-skraun
2. MAIN III:s levande daterade status: https://github.com/Odourman/the-skraun/blob/main/docs/CURRENT_MAIN_STATE_2026-11-17.md
3. Senaste relevanta MAIN-review: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_PLAY1_X_NTSC_TIMING_NEGATIVE_REVIEW_2026-11-22.md
4. Användarbeslut 01–60 och senare uttryckliga korrigeringar: https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md
5. Visuell riktning: https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md
6. Fryst U1-LEG1-pixeloriginal: https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json
7. Issues/PR + deras EXAKTA huvudcommit, byggloggar, autentiska Stella-PNG och SHA, inte enbart README/Memory.
8. Historisk Google Drive-projektrot: https://drive.google.com/drive/folders/1tSipzf7bucrqFOwHBEH61fKvyl0z7D1z. Äldre 2026-11-17 ROMDEV-migration är historik och ersätts för ny chat av detta dokument.

Vid konflikt: ett senare uttryckligt användarbeslut och specifikt gällande MAIN-auktoriserat scope väger tyngre än gamla sammanfattningar; exakta käll-/ROM-byten och godkända pixelmasker är primärbevis. Research är rådgivande; MAIN-review är inte oberoende VERIFICATION. ChatGPT Memory är inte projektauktoritet.

## 1. Rollbyte, utan automatisk ny uppgift

- Mottagare är **ROM DEVELOPMENT III** (efterträdare till ROM DEVELOPMENT II), inte MAIN III. Ägaren är fortfarande MAIN III.
- ROM DEVELOPMENT III får analysera, föreslå begränsade tekniska hypoteser och läsa/bevara frozen evidence, men **får INTE skapa ny ROM/implementation förrän MAIN III ger en ny, separat uttryckligen användargodkänd arbetsorder** med branch, underlag, scope och stoppgräns.
- N7, PLAY1, PLAY1-H och PLAY1-X-implementationsordrar är förbrukade. De ska aldrig läsas som en pågående uppgift efter migration.
- N8, N9, full spelmotor, mapperbyte, spriteproduktion, åtta produktionsbanor, main-merge och fortsatt X2/dubbel-PF2 är inte auktoriserade. Ingen oberoende Verification automatiskt efter en liten prototyp; separata N7 Verification II Issue #33 tillhör en annan roll.
- Efter en ny uttrycklig arbetsorder: gör praktiska små testbara ROM-iterationer, bygg med DASM, kör Stella, mät faktiska cykler/scanlines/pixlar, leverera bevis, stoppa efter scope. Skilj SOURCE_STATIC, DEVELOPER_OBSERVED, MAIN_REVIEWED och INDEPENDENT_VERIFICATION.

## 2. Exakt fryst utvecklingskedja och nuvarande beslut

### N6-C fullrenderer fortfarande OBEVISAD
Issue #30: https://github.com/Odourman/the-skraun/issues/30. Kravet på tre samtidiga fiender i normalarena är inte löst. R3:s 20 Hz rotationsförsök och F2a/F2b-motexempel ger inga allmänna bevis på omöjlighet.

### N7/F2b, gammal negativ tre-fienderdiagnostik
PR #32: https://github.com/Odourman/the-skraun/pull/32, draft, fryst commit `25e5e22ab6eb91aeb69c0926ffa0a822b4fc201d`. ROM SHA256 `d15c4805b06c562cb76369dfe3efff3a8c9537f28de4945196d198957fc5368f`. Endast S2-close två fysiskt testade varianter: `F2b_FAIL_FOR_TESTED_SCENE`; MAIN har accepterat avgränsat negativt. Separat VERIFICATION II read-only #33 OPEN utan rapport senast vid kontroll 2026-11-22. Ingen N7-fortsättning i ROMDEV III.

### PLAY1 – första riktiga spelbara syntetiska arenan, PARTIAL
PR #35: https://github.com/Odourman/the-skraun/pull/35 (draft, unmerged). Fryst commit `8247a3ba2b723c88336b63d5666503bed72cf2af`. 4096B NTSC ROM SHA256 `cbc296309d60a35debb7bd6980ea5f61db5101bff48c4397f4c5569a8d33aedd`; ASM SHA `69898159cd4261a7f77365ef7e21da1bb30194770762f4f7292c9f52b542f606`. 7 verkliga Stella gameplayfall visar P0 8-way, fyra syntetiska hinder, verklig BL orb-upgrade L1→L2→L3, FIRE och R3 P1 träningsdummy. Synlig PF-guldmask fixerad till arenan, följer INTE P0. MAIN review: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_PLAY1_REAL_GAMEPLAY_DELIVERY_REVIEW_2026-11-21.md.

### PLAY1-H – bevara som senaste bättre spelbara NTSC-PARTIAL-bas
**FROZEN BASE FÖR EVENTUELLT NYTT SPELBART STEG, men ingen ny kodauktorisation.** PR #37: https://github.com/Odourman/the-skraun/pull/37 (draft, unmerged). Branch `experiment/play1-h-moving-visible-halo-20261121`; exakta HEAD `79b9739e77741c74ae5228f3c63d64449af7bc9f`. 4KiB ROM SHA256 `6e5e203ff2715fac650b76a620bc1e3e3b0084d67e82452842edd7b5e1903bca`; ASM SHA256 `0aa5cf5d14e1eba0b786965fe316327810de01d36a4a32202651e06f36255c16`. Spelbar begränsad loop i åtta genuina Stella-scenarier med K0 full-body hinder / glid / L3, orb, verklig FIRE, P1 R3 120 pixlar före träff, nivå L1/2/3 verklig P0 16×12/32×24/64×36 TV-pixlar. Verklig Y-rörelse på halon: 1516 icke-ockluderade guldpixeländringar när P0 går upp8; X +8 ger exakt 0 ändringar utanför P0/P1-ocklusion. **PLAY1_H_PARTIAL**, inte godkänd 360-graders visuellt följande halo, och konservativ worst-case synlig kernel upp till ~77/76 cykler är SOURCE_STATIC och ännu inte full tracebevisad. RAM statiskt 42B plus ~4B härledd return stack, inte mätt runtime-highwater. MAIN III:s verkliga review: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_PLAY1_H_ACTUAL_ROM_STELLA_DELIVERY_REVIEW_2026-11-21.md. Faktiska autentiska Stella 8 scener: https://github.com/Odourman/the-skraun/actions/runs/44920971754.

### PLAY1-X – sista frysta testet, tydligt negativt
**SENASTE UTFÖRDA ROM DEVELOPMENT II-TEST, inte spelbar bas.** PR #39: https://github.com/Odourman/the-skraun/pull/39 (draft, unmerged). Branch `experiment/play1-x-precomputed-asymmetric-halo-20261121`, fryst commit `306c133992a769c88882b626f8af8f3a43f0396a`. 4096B ROM SHA256 `d4a83d0b41ba6850e4b7686feed41c6da136dd95adb6f5184ed5d0f93536cde3`; ASM SHA256 `b8c89c205aef9dc99d75ab156bd7882bfa3dd98c515917780bd3098a04f45730`. En enda asymmetrisk förberäknad PF2-högermask + en EXTRA `LDA (HaloRightPtr),Y; STA PF2` i redan överfull synlig kernel, -3-cykel lokal korrigering. Nio verkliga Stella GUI/TIA-scenarier med riktiga joystick/FIRE-kommandon. Faktisk frame L1 **273**, L2 **285**, L3 **297** fysiska rasterrader (NTSC ska vara 262), P0 fysiskt **16×23 / 32×47 / 64×71** i stället för **16×12 / 32×24 / 64×36**, P1 **168/144** blå pixlar i stället för 120. X A→B ändrar 4208 guldpixlar men renderer är ogiltig, B→C ändrar 0. SOURCE_STATIC min ~81/76 CPU-cykler, upp till ~84/76 inklusive indexsidkorsningar. Första mer långsamma provet autodetekterades av Stella som `PAL*`; det var INTE ett PAL-beslut. Sista märktes `NTSC*` men 273/285/297 är fortfarande FEL fysisk NTSC-timing. Resultat `PLAY1_X_FAIL_FOR_TESTED_IMPLEMENTATION`. Inget generellt TIA-omöjlighetsbevis, ingen ROM eller X kod ska föras över till PLAY1-H. MAIN III **har granskat faktiska originalbevis** och accepterat bounded FAIL: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_PLAY1_X_NTSC_TIMING_NEGATIVE_REVIEW_2026-11-22.md. [Issue #38](https://github.com/Odourman/the-skraun/issues/38#issuecomment-7077469699), [strict CI #44937101836](https://github.com/Odourman/the-skraun/actions/runs/44937101836) korrekt `failure` just pga första spritefel. ROM/ASM/lst/sym SHA-manifest https://github.com/Odourman/the-skraun/blob/306c133992a769c88882b626f8af8f3a43f0396a/experiments/play1_x_SHA256SUMS.txt.

## 3. Spelcanon som aldrig får tappas vid migration

Användargodkänd nivå 1 är upprätt ljusgrå U1-LEG1 8×12, exakt original A/B, horisontell spegling och omvänd `VISUAL RIGHT`/`SOURCE LEFT`-tolkning; samma källa på nivå 2/3 med preliminära visningsstorlekar 16×24 och 32×36. Åtta joystickriktningar med diagonal glidning längs hinder och fri, smidig framkomlighet på L3. Åtta distinkta banor i skog, berg, dröm, natt. Två riddare samtidigt PLUS världskamouflerad Ranger – träningsriddare i PLAY1 är endast ett godkänt temporärt testmål. Riddare skadar enbart via förvarnade svärdshugg, aldrig kroppskontakt. Halo är 360 grader, aktiv ungefär 30 NTSC-frames och rörlig med P0 medan den blir större/tjockare per level, kan träffa igenom hinder och förstöra pilar. Test B: PF världsfärg OFF/guld ON inklusive hinder, BL-orb färg följer PF. Statiska drömspiraler. Ingen tyst gameplay-/grafikförminskning, ändrad fiendekapacitet eller 16-frame trög B3b-halo får bli ny canon.

## 4. Tekniska bevisgrindar och negative lessons

- En original Atari 2600 6507 ger **76 CPU-cykler per fysisk rasterrad**, inklusive TIA-beamdeadlines; mål **NTSC 262 rader**. Stella `PAL*`/`NTSC*` är automatisk formatdetektion, inte tekniskt acceptansbevis.
- RIOT 128B totalt inklusive stack. Ange RAM-map och stack-highwater som statiskt härledd eller verkligt mätt separat.
- En DASM `Complete. (0)` och en 4096B ROM bevisar bara assemblering/storlek. Emuleringsraster, exakta källpixlar, TIA-register, fysiska scanlines och relevanta worstcase-mått måste också visas.
- Stoppade tekniker: R3 same-Y 20Hz-tidsdelning, N7/F2b prövad S2-close, B3b X-follow var 16:e frame, PLAY1-H CTRLPF mirror→repeat flyttade fasta hinder och förvanskade sprites, PLAY1-X extra PF2 per rad gav 273/285/297 fysiska rader. Pröva inte automatiskt samma teknik igen.
- Skilj `SOURCE_ONLY`, `DEVELOPER_OBSERVED`, `MAIN_REVIEWED`, `INDEPENDENT_VERIFICATION`. MAIN III:s självständiga omräkning av utvecklarens originalbilder är `MAIN_REVIEWED`, **inte** oberoende Verification II.
- Stella testades med GitHub Actions ubuntu/DASM/Stella 6.7.1 Xvfb/Debugger; tillgängliga anslutna GitHub/Google Drive-verktyg bör kontrolleras och användas automatiskt. Lokal klient kan sakna installerad DASM/Stella, använd verklig CI/Stella, inte fabricerade screenshots.

## 5. Nästa rollkontroll och STOP

På första meddelandet i nya ROM DEVELOPMENT III: kontrollera access till GitHub och Drive med verkliga pluginverktyg, verifiera senaste MAIN-status/PR #39 och dess hash och MAIN review 2026-11-22, jämför de gamla Project Sources 00–04 med detta senare underlag. Bekräfta status `MIGRATION_RECEIVED / ROMDEV_III_IDLE_WAITING_FOR_EXPLICIT_MAIN_ORDER`. Inga nybranches, ROM-fixar, experiments, Issues, PR, testjobb eller nya implementationer bara av detta dokument. MAIN III beslutar om en separat, avgränsad ny spelbar riktning efter användarens uttryckliga tillstånd.

**Källhierarki är styrande; denna migration är en daterad navigationsöverlämning, inte ny canon eller ny implementationstillåtelse.**
