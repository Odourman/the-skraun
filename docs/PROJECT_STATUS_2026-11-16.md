# THE SKRAUN – Aktuellt projektläge, 16 november 2026

**MAIN sammanfattning efter kontroll av GitHub och Google Drive.**

## Käll- och implementationsgräns

1. Beslut 01–60 på `main` definierar spelets regler. Användarens nya handritade referens och uttryckliga bekräftelse av ljusgrått, ovanifrånperspektiv, två poser och enbart horisontell spegling är aktuell visuell riktning.
2. Experimenten `experiment/p02-halo-p1`, `experiment/p02-playfield-b2` och `experiment/gray-topdown-skraun` är **separata grenar**. Ingen har slagits ihop med den stabila källkoden.
3. Tester som byggningen, automatisk PNG-analys och ett isolerat Stella-prov är **egenkontroller**, inte oberoende VERIFICATION.

## Kontrollerad kod- och teststatus

| Del | Status | Evidens |
|---|---|---|
| Speldesign 01–60 | Dokumenterad | `docs/DESIGN_DECISIONS_01-60_2026-11-16.md` |
| P01 grundprototyp | Körbar 4K NTSC; tre storlekar, grundrörelse | `src/main.asm`; ordinarie CI godkänd |
| P01 oberoende verifiering | **Öppen, ej godkänd** | https://github.com/Odourman/the-skraun/issues/1 |
| P02-A P1-haloring | ROM och Stella-bilder; otillräcklig level-3-bredd och blockerar P1 | https://github.com/Odourman/the-skraun/pull/2 |
| P02-B1 statisk playfield-ring | Bounded Stella test PASS, ring 96×84 bildpixlar | `docs/P02_B1_PLAYFIELD_RESULT_2026-11-16.md` |
| P02-B2 statisk halo med P0-troll | Bounded Stella test PASS, tre storlekar | https://github.com/Odourman/the-skraun/pull/3 |
| P02-B3 dynamisk ring | Plan och testgrind dokumenterade, **ingen ROM ännu** | `docs/P02_B3_DYNAMIC_RING_GATE.md` i B2-grenen |
| Ny grå overhead-Skraun | ROM byggd, 3 storlekar och grundrörelse i Stella; grafiken är fortfarande preliminär | https://github.com/Odourman/the-skraun/pull/4 |
| Grå Skraun med statisk haloring | 4K ROM och tre Stella-bilder godkända i begränsad egenkontroll, men **ingen rörlig halo** | https://github.com/Odourman/the-skraun/pull/5 |
| Skog/berg/dröm/natt, riddare, grön bågskytt, kollisioner, poäng och ljud | **Inte implementerade** i de testade prototyperna | Återstår |

## Nytt visuell implementationstest

- Användarens handritade ursprungsform, privata foto i projektets Drive: https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view
- Godkänd visuell riktning: ljusgrått, ovanifrån, 2 korta gångposer med arm- och benrörelser, vänster = exakt bitvis spegling av höger. Ingen ny vy uppåt/nedåt.
- Grå experimentkällkod: `experiments/p01_skraun_gray_topdown.asm` i PR #4.
- Godkänd DASM- och Stella-egenkontroll: https://github.com/Odourman/the-skraun/actions/runs/43882932038
- ROM SHA-256: `387ad9dd3fc3cbceeaca61122963de5b79ecc482dc0e17d22a4c6827b756fd99`, storlek 4 096 byte.
- Skärmbilder: 16×12, 32×24, 64×36 pixlar i Stella-bilder; motsvarar horisontellt 8/16/32 TIA-color-clocks. Den grå figuren behöver estetisk overhead-kontroll, timing och oberoende test.
- Google Drive-evidens: https://drive.google.com/drive/folders/1udBPud9jpVzvMevcgKL8duib94GyV_yJ

## Prioriterad fortsättning

1. Kontrollera att A/B-animationerna faktiskt syns i Stella och testa grå P01:s scanline-/cykelbudget, inte bara spelarspritens bildmått.
2. Gör den minsta grå figuren visuellt igenkännlig ovanifrån, baserat på originalteckningen. Beakta kontrast mot framtida skog/berg/dröm/natt, särskilt grå sten.
3. Utred P02-B3a (flyttbar ospeglad playfield-ring i tre X-lägen) i **ny separat experimentgren** med bildtest, timing och tydlig riskredovisning. P02-B2 är fortfarande statisk.
4. Integrera inte grå figur eller ny ring på `main` förrän aktuella scope och mätningar håller. P01-oberoende verifiering ska inte antas passerad.

**Övergripande slutsats:** Speldesignen är långt gången, men spelet är fortfarande i hårdvaru- och kärngrafikprototypstadiet. Det finns ingen färdig spelbar kampbana och inga riktiga bakgrundsvärldar i ROM ännu.

## KORRIGERING AV SPRITEORIENTERING – 2026-11-16

Efter användarens observation verifierades att den tidigare kombinerade P02-grå-RING-ROM:en ritade trollet upp och ned. Rasterloopen läste bitmaptabeller via nedräknande index 191→0, men figurtabellerna lagrades i fel vertikal ordning. Samma metod förekommer i det tidiga B2-experimentet; dess gröna screenshot-test bevisar bara storlek/ring, inte rättvänd sprite.

**Fix:** [draft PR #6](https://github.com/Odourman/the-skraun/pull/6) i grenen `fix/p02-gray-halo-upright`, separat från `main`. Riktig Stella 6.7.1 bekräftar korrekt radorientering pixel för pixel på nivå 1–3, 4K NTSC ROM SHA-256 `7dda240f58656277e5508ad444368b2c33cad0ee9c9a5c259b27e0a7eda44bed`. Full audit i `docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md`, evidenspaket på Google Drive. P01/hela P02 är **inte oberoende verifierade**.

Roller: MAIN = den här huvudchatten; ROM DEVELOPMENT = separat implementation/självtest; VERIFICATION = separat oberoende granskning. Startprompter finns i `handoff/ROM_DEVELOPMENT_START.md` och `handoff/VERIFICATION_START.md`.

## MAIN uppdatering – A/B/C accepterade som egenkontroller, P02-B3b auktoriserad (2026-11-16)

Efter jämförelse med faktiska GitHub PR #8–#10, byggkörningar och samlad rapport har MAIN **accepterat A, B och C som klara avgränsade utvecklaregenkontroller**. Ingen gren har slagits ihop med `main` och inget oberoende VERIFICATION har genomförts.

- A: två riktiga gångposer, vänster/höger, tre storlekar och 8-riktningsrörelse i Stella. Den diagnostiska vänsterkantsmarginalen är inte en generell kernellösning eller färdig banagräns.
- B: `REFP0` hårdvaruspegling genomförd och utvecklartestad. Fyra bitmaptabeller reduceras till två och **24 ROM-byte** sparas; integrerad timing ej slutligt mätt.
- C: P02-B3a visar asymmetrisk ring i tre fasta X-centra 56/80/104 och grå P0. Debugger visar 262 scanlines vid provat läge. Beräknat högst **64 av 76 CPU-cykler/scanline** för synlig rutin (statisk kalkyl, **inte** full värstafallsmätning). Ingen fri joystickföljning, hinder eller fiender.
- Jämförbar originalrapport: https://github.com/Odourman/the-skraun/blob/experiment/romdev-c-b3a/docs/ROMDEV_ABC_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md . Samlat evidens: https://drive.google.com/drive/folders/1MyI-ZuVqSj_MwQRebn7C0emfxlU5jdeX .
- **Nytt uttryckligt MAIN-uppdrag:** https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_B3B_AUTHORIZED_SCOPE_2026-11-16.md – B3b, faktisk horisontell joystickföljning i 4-TIA-klocksteg och begränsat PF-hindrars/processorbudget-test. Ingen B3c, fiendekod eller produktionsintegration nu.
- **VERIFICATION vilande**, eftersom oberoende kontroll ska samlas för senare större leveranspaket. Öppna historiska verifieringsärenden stängs inte av detta beslut.

Tidigare statusuppgifter längre upp på sidan visar dåtidens läge; **denna sektion är senare och ersätter formuleringen att B3a inte var byggd**.

## Senaste MAIN-beslut: B3b accepterad som egenkontroll; P02-R1 auktoriserad (16 november 2026)

Detta är senaste lägesuppdateringen och ersätter äldre framtidsformuleringar ovan som beskrev B3b som ännu inte genomförd.

- ROM DEVELOPMENTs B3b utvecklartest [PR #11](https://github.com/Odourman/the-skraun/pull/11) visar 13 joystickstyrda 4-TIA-klockslägen och synkroniserad asymmetrisk PF-ring/P0. Realtidsbilder i [grön Stella-körning](https://github.com/Odourman/the-skraun/actions/runs/43901341243) och fyra verkliga joysticklägen med 262 scanlines i [Stella Debugger](https://github.com/Odourman/the-skraun/actions/runs/43900278446). Detta är **egenkontroller**, inte oberoende verifiering.
- Två 4K-ROM-varianter: dynamisk SHA-256 `7d96bcb71532643307922f62814900b09a1525ede06795c17417607634efd060`; prekomponerade syntetiska hinder SHA-256 `31b859d711bb08228b03015f9039b1df97c77628ab3637f754ad3df77b599bbe`.
- **Allvarliga begränsningar:** Endast 1 horisontellt steg per 16 NTSC-bildrutor (~267 ms), enbart 13 testpositioner, 63/76 cykler värstafall **statiskt beräknat** (13 cyklers marginal). Generell runtime-hinderkomposition i oförändrad kernel behöver minst ~79/76 cykler och saknar visuell separation mellan ring och hinder. Två riddare + bågskytt + pil + orb + HUD har inte testats i gemensam kernel.
- Full leveransrapport: https://github.com/Odourman/the-skraun/blob/experiment/romdev-b3b-horizontal-follow/docs/ROMDEV_B3B_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md . Evidensmapp: https://drive.google.com/drive/folders/1fn4RTvPreT6dsVQD5HUaLYIRPfLffz8h .
- **MAIN:s enda nya implementationsauktorisation:** [P02-R1 renderer architecture feasibility](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R1_RENDERER_FEASIBILITY_AUTHORIZED_2026-11-16.md) – diagnostiskt förbättrad respons, jämförelse av PF/hybrid/hinderrendering, konservativ budget för framtida fiender och HUD. Ingen B3c, ingen färdig stridsmotor, ingen produktionsmerge.
- **VERIFICATION fortfarande vilande** fram till en senare större sammanhängande milstolpe. Ingen oberoende PASS har utfärdats.

## Senaste MAIN-beslut – R1 accepterad som egenkontroll; R2 separat auktoriserad (2026-11-16)

MAIN granskade den frysta R1-rapporten, GitHub [draft PR #12](https://github.com/Odourman/the-skraun/pull/12), assemblergrenen samt [GitHub Actions run #43906912249](https://github.com/Odourman/the-skraun/actions/runs/43906912249). Den slutliga PR-headen ligger två dokumentationscommits efter den sista godkända Stella-körningen; kodfilerna har inte ändrats däremellan. **R1 är avslutad som teknisk utvecklaregenkontroll, men är INTE oberoende verifierad, produktionsgodkänd eller mergad.**

Resultat: 2-frame diagnostisk SWCHA-kontroll (1 frame respons vid testad fas), 13 X-positioner, fyra reproducerbara 4KiB NTSC-ROMs, 528 byte deduplicerad hindermask, faktisk extra P1-sprite på PF-rader, 262 scanlines i testade tillstånd. Värstafallscykler FAST 63/76, OPT 64/76, SCORE 63/76, P1 71/76 är **statiskt beräknade** med DASM-symboler. Ring och hinder inom samma PF-cell har fortfarande inte självständigt synliga färglager. Rimlig kapacitet för 2 riddare + bågskytt + pil + orb + HUD **är inte bevisad**; R1:s naiva belastningsmodell anger ≥102/76 för ett utvalt same-Y-fall, inte att alla framtida kernels är omöjliga. Nivå 3:s ringradie är fortfarande inte testad.

R1 full rapport: https://github.com/Odourman/the-skraun/blob/experiment/romdev-r1-renderer-feasibility/docs/ROMDEV_P02_R1_RENDERER_FEASIBILITY_MAIN_HANDOFF_2026-11-16.md
R1 Drive-bevis: https://drive.google.com/drive/folders/1AwRVTCgs5Dz99Zwj0-7n3A4IAfJVILf7

**NÄSTA ENDA AKTUELLA ROM DEVELOPMENT-AUKTORISATION:** P02-R2, en avgränsad renderer- och sprite-schemaläggningsförstudie av tvålinjers-PF, olika kernelzoner/selek­tiva TIA-uppdateringar och verkliga same-Y-belastningsfall med hinder och nivå3-ringsräckvidd. Fullt scope: https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R2_RENDERER_SCHEDULING_AUTHORIZED_2026-11-16.md . Drive: https://docs.google.com/document/d/1tFiRcbfWgyitOPOTJZqz2oDD5nzp9-eWT7V6rPYszjk/edit

**B3c, B3d/B3e, fiende-AI, färdig HUD, produktionsmerge och nästa utvecklingsfas är INTE auktoriserade. VERIFICATION förblir vilande** tills MAIN lämnar över ett betydande fryst systempaket.

## SENASTE MAIN-BESLUT 2026-11-16 — R2 egenkontroll accepterad, R3 separat auktoriserad

MAIN har kontrollerat R2:s exakta GitHub PR #13 (`experiment/romdev-r2-two-line-scheduler`, head vid granskningspunkten `2cb9eafa0f5964e89553f791ff18ea9d9362fe8e`), källkod, slutrapport, frysta lyckade GitHub Actions-körningar och originalbevis i Drive. ROM-källorna har inte ändrats mellan den slutliga ROM-/bildtestade commiten `47c0309c4929df991a67ef1db3b218e8b0f67a42` och granskad PR head; endast rapport och workflow har tillkommit.

**R2 är godkänd ENBART SOM AVSLUTAD UTVECKLAREGENKONTROLL.** Fem verkliga 4K NTSC-ROM-varianter, 20 Stella-spelbilder och 16 Stella Debugger-tillstånd med 262 scanlines rapporteras; oberoende VERIFICATION saknas och PR #13 är fortfarande draft, inte mergad. [Slutrapport](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r2-two-line-scheduler/docs/ROMDEV_P02_R2_RENDERER_SCHEDULING_MAIN_HANDOFF_2026-11-16.md) · [Stella #43912037744](https://github.com/Odourman/the-skraun/actions/runs/43912037744) · [Debugger #43911806707](https://github.com/Odourman/the-skraun/actions/runs/43911806707) · [Drive originalbevis](https://drive.google.com/drive/folders/16SutItHKN8sm64i387X1ScbR0sVCh19L).

**Tekniska begränsningar**: Tvålinjerskernel med P1 68/76 beräknade rastercykler mot 71/76 för R1; olika P1-bitmappar 76/76 utan marginal, med fast 64-TIA-clock avstånd snarare än fria fiende-X. Separat HUD-kernel har 64/76 arena utan P1. Guld/blå linjeinterlace ger visuell separation mellan vissa angränsande rader men halverar de guldfärgade ringraderna och kostar 74/76. Ingen av dessa bevisar full nivå3-ring, tre fritt placerbara fiender, pil, orb och hinder på värsta samma-Y-bandet. 262-scanline-debuggervärden är äkta bildrutelängdsmätningar men cykelvärdena är huvudsakligen statiska DASM-beräkningar.

**NY SEPARAT AUKTORISATION:** [P02-R3 beslutsgrundande scen- och fiendeschemaläggningsförstudie](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R3_DECISIVE_SCENE_SCHEDULER_AUTHORIZED_2026-11-16.md) – högst 2–3 riktade diagnos-ROM, tre fritt placerbara fiendepositioner med Y-överlapp och prövad begränsad frame-fördelning, faktisk nivå3-ring + synliga hinder samt pil/orb/HUD-resursreservation. Målet är ett ärligt go/no-go eller konkret hårdvaru-/designval, inte ännu en obegränsad experimentserie. [Drive-handoff](https://docs.google.com/document/d/1d7vvLACrwzBx1WXbk4JLo2lSpxclPhEtPlxGr7ub9zc/edit).

**INGEN B3c, B3d, B3e, R4, fiende-AI, produktionsmergning eller oberoende VERIFICATION** tillåts under R3. MAIN avgör nästa steg först när fryst R3-underlag har granskats.

## SENASTE MAIN-BESLUT 2026-11-16 – R3 tekniskt NO-GO, visuell regression och R3-VFIX

MAIN har granskat [draft PR #14](https://github.com/Odourman/the-skraun/pull/14), originalbilderna från [R3:s Stella-montage](https://drive.google.com/file/d/1N-sHAYWLPf3v_RFsQV9d7qAki7_lcQiZ/view), källkodens `Troll3`-tabell och den tidigare kända [upright-fixen](https://github.com/Odourman/the-skraun/blob/main/docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md).

**BEKRÄFTAT FEL:** P0/Skraun visas vertikalt UPP OCH NED i R3. Den nedräknande `lda Troll3,x`-kerneln läser raderna från högre index först men R3:s logiska huvud/öron-rad `$24` ligger vid lägre aktiva index än fotraden `$C2`. Det är motsatt den tidigare rättade grafiktabellen. R3:s gröna tester kontrollerar bbox/pixelantal/förflyttning, men INTE top-versus-bottom eller användarens visuella godkännande. **Grafiskt R3 = FAIL, även om begränsad teknisk schedulingevidens kan behållas.**

R3:s tre pyttesmå EnemyArt-tabeller är **TEKNISKA PLATSHÅLLARE**; de ser inte ut som riktiga riddare eller grön bågskytt. Den svarta arenan med blå testkolumner och cyan HUD-rand är inte världarnas färdiga skog/berg/dröm/natt-bakgrunder. Ingen sådan spelgrafik är godkänd. User feedback är explicit registrerad i [issue #15](https://github.com/Odourman/the-skraun/issues/15).

**Tekniskt R3-NO-GO kvarstår:** Tre same-Y fiender renderas endast 20 Hz var; vid två fiender 30/30 Hz; full synlig halo och självständigt blå hinder alternerar 30/30 Hz (eller sammanfaller i en enda PF-färg); 2–4 CPU-cykler återstår statiskt; pil/orb och full HUD/AI saknas. Detta är ett utvecklaregenkontrollerat, NEGATIVT arkitekturutfall, INTE ett bevis att all tänkbar Atari 2600-teknik omöjliggör spelet.

**MAIN:s ENDA NYA AUKTORISATION:** [R3-VFIX](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_R3_VFIX_ORIENTATION_REGRESSION_2026-11-16.md), en separat, smal rättning av trollraderna i tre R3-diagnoser med nya **verkliga Stella-pixelregressioner som ska FAIL:a på original-ROM:erna och PASS:a efter korrigering**. Inga nya fiendesprites, världsbakgrunder, R4, B3c eller produktionsmerge auktoriseras genom detta. Google Drive-kopia: https://docs.google.com/document/d/1ZtVzhxtfJgT8y4C01Td2kNSatHYdIX3m3Br9Adb9nMQ/edit . Oberoende VERIFICATION förblir vilande till större milstolpe.

## SENASTE MAIN-BESLUT 2026-11-16 – R3-VFIX godkänd som avgränsad utvecklaregenkontroll

MAIN granskade den verkliga [draft PR #16](https://github.com/Odourman/the-skraun/pull/16), den verkliga diffen för `experiments/romdev_r3_overlap.asm`, `partial.asm` och `stagger.asm`, huvudkontraktet i `tests/romdev_r3_vfix_orientation.py`, samt lyckad [Stella Debugger + pixelregression #43925833442](https://github.com/Odourman/the-skraun/actions/runs/43925833442) och [slutpaket #43926438951](https://github.com/Odourman/the-skraun/actions/runs/43926438951). CI:s ROM/källkodscommit är `bdb9aae200e63dd00386a2added6e773474e9572`; slutliga PR-head `164a1233550a86e55d2b3a9489aad2455b8ef665` har endast två ytterligare commits för **workflowpaketering och rapport**, inga nya assembler- eller testkodändringar. Ingen produktionsmerge gjord.

**Godkänd omfattning:** Alla tre frysta R3-ROM:er har korrigerad head-above-feet-radordning i Skrauns 36 aktiva GRP0-bitmapbyte (gamla aktiva huvudet `$24` låg före fotraden `$C2` men nedräknande raster läste baklänges). Kod- och ROM-diff begränsad till 36 bytes per variant. Gamla original-Stella-bilder (57 st) FAIL:ar det nya pixelorienteringskontraktet som negativ kontroll; 57 autentiska nya bilder PASS:ar alla 12 logiska rader, alla x-lägen och testade riktningsbyten. 57 autentiska debugger-bildrutor visar 262 NTSC scanlines. Cykler, P1-buffer, spelregler, halo/PF och rörelse är inte ändrade.

**Nya ROM SHA256** (4096 B var): overlap `2c29a696c3a7b5c05ba84a829f6ae64cbc58886778d929799d057048645f8f55`; partial `89098ad4026cd4e770381d30c2469fe5faac3cbde2fd3d27d38f33a85ef98221`; stagger `53b00adf2325cfd84a6fac52cd504db6349b46922da5a259ac1b7ad2923c54e3`. Leveransrapport: https://github.com/Odourman/the-skraun/blob/fix/romdev-r3-upright-20261116/docs/ROMDEV_R3_VFIX_MAIN_HANDOFF_2026-11-16.md . Package ZIP in GitHub Actions artifact: https://github.com/Odourman/the-skraun/actions/runs/43926438951/artifacts/14256391823 . ZIP inner SHA256 `d314ef719ccf57815e7edd4b1ae8c04779d32c3e5c27dda453e6e9be7a46f215`.

**Fortfarande öppet – grafiskt godkännande:** Skrauns riktiga överhuvudtaget bildmässiga slututformning och animation, de igenkännliga röda riddarna med svärd, grön bågskytt med båge, hinder/miljö för skog/berg/dröm/natt, samt läsbar HUD. Originalets tillfälliga 8-byte fiendegrafik och blå testkolumner får aldrig markeras final. [Issue #15](https://github.com/Odourman/the-skraun/issues/15) hålls **öppen** som grafisk gate men orienteringsdelmomentet är åtgärdat.

**Arkitektur:** R3:s negativa fullspelsbedömning kvarstår oförändrad (same-Y fiender 20Hz var, ring vs hinder 30/30Hz eller sammanfallen PF-färg, endast 2–4 statiskt beräknade rastercykler, ej pil/orb/full HUD). Felet VFIX har inte löst detta. **Ingen ny R4, B3c, ny grafikimplementation eller produktionsmerge har auktoriserats. VERIFICATION förblir vilande till större sammanhängande milstolpe.** Nästa prioritet för MAIN är ett medvetet grafiskt/tekniskt vägval, inte automatisk fortsatt kodning.

## VISUELL DESIGNAVSTÄMNING – RÅDGIVANDE FÖRSLAG EFTER R3-VFIX (2026-11-16)

MAIN har granskat användarens originalteckning, [riktningen för grå topdown Skraun](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), det faktiska grå A/B-montaget och R3:s ursprungliga autentiska Stella-bilder. Föreslaget visuellt granskningsunderlag finns i [MAIN:s detaljerade grafiska designförslag](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_POST_R3_VISUAL_DESIGN_REVIEW_PROPOSAL_2026-11-16.md), även i [Google Drive](https://docs.google.com/document/d/1MneyvSpbArowmkYW_ocP0jEYKb032ojqh-6e0R6mHE0/edit).

**Förslag, INTE nya bindande designval:** Ljusgrå fyrbenta Skraun behålls som utgångspunkt men inte slutgodkänd silhuett. Riddare bör gå att känna igen på hjälm/svärd och bågskytten på grön asymmetrisk båge även utan kulörer. Skog, berg, dröm och natt bör vara visuellt olika genom få tydliga hindersilhuetter, färg och layout snarare än detaljerad/långsam bakgrund; HUD prioriterar poäng/liv. Tidigare fiende-/hinderbilder i R3 är bara testmarkörer. Alla visuella förslag måste i en eventuell framtida särskilt auktoriserad ROM-konstdemonstration testas i verklig Stella med TIA/6507-resursgränser. Hög prioritet att synliggöra 20/30-Hz-flicker genom frame-sekvenser i stället för enskilda skärmbilder.

**Inget nytt implementationsscope har startats:** R3-VFIX är avslutat i utvecklaregenkontroll, R3:s NO-GO för testad fullmotor kvarstår, issue #15 är fortsatt öppen för visuell kvalitet. Ingen R4, B3c, fiende-AI, slutgrafikimplementation, main-merge eller oberoende VERIFICATION är auktoriserad i denna grafiska genomgång.

## MAIN GRANSKNING GRAPHICS v0.1 – VISUELL KANDIDAT C ENDAST PRELIMINÄR (2026-11-16)

MAIN har kontrollerat [separat GRAPHICS-gren](https://github.com/Odourman/the-skraun/tree/graphics/skraun-pixel-candidates-v0-1-20261116) HEAD `e3da7c4efb9ee031543821ba945a8ca2d91c66dd`, `sprites.json` med tre 8×12-kandidater och 2 poses, `SKRAUN_PIXEL_DATA.inc`, `skraun_C_preview.svg`, `halo_pf_static_art_mask.json`, README och [Drive-designrapport v0.1](https://docs.google.com/document/d/1zMKBqW84Oe6nPXUYEfrqOE4JxqusD3m8E5C3QVTSPZ8/edit). 

**BESLUT:** v0.1 är accepterad **ENBART SOM KÄLLBASERAT GRAFIKUTKAST**. Kandidat C är preliminärt bäst för lemseparation, men är INTE konstnärligt slutgodkänd: huvud/ögon och främre humanoida perspektiv dominerar ännu, medan fastställt visuellt krav är fyrfotad Skraun rakt ovanifrån. Första fem logiska raderna är identiska i A/B/C; C:s två frame-poser skiljer sig i främre och bakre lemrader och är horisontella speglingar. Statiska bitmapdata är inte Stella-testade.

**HALOVARNING:** Grafikutkastet för statiska 40×24 PF-masker med 8 scanlines per band har höjd 80, 128 och **176 scanlines** för nivå 1/2/3. Detta är inte etablerad attackräckvidd eller tekniskt uppfylld dynamisk halo. Kräver TV-aspekt/proportion, edge clipping, R3-jämförelse och synliga hinder. Gemensam PF-färgkonflikt kvarstår.

**LEVERANSGAP:** GitHub `graphics/skraun_v0_1` hade fem källfiler och angiven Drive-grafikmapp endast ett Google Doc. Den uppgivna kompletta 14-filers-ZIP:en med hash `034e9c221fed003e1bf163f4dbddef7711be8dc72214d727a9f17a73f068eedf` har INTE lokaliserats eller hashkontrollerats i det publicerade underlaget. Ingen verifierad arkivbaserad bedömning av GIF, knight/archer eller världskontrastbilder görs ännu. Ingen påstådd ZIP-verifiering.

**GRAPHICS FÅR FORTSÄTTA DESIGNUPPDRAGET I v0.2**, fokuserat på C-refined vs genuin C-overhead, igenkännliga 8-bitars riddar- och bågskyttssilhuetter, fyra världars sparsmakade hindergrafik, korrekt halo-skala och en faktiskt tillgänglig komplett Drive ZIP. Bindande scope: https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_V0_2_VISUAL_REFINEMENT_2026-11-16.md ; Drive-kopia https://docs.google.com/document/d/1bIeHN96Y0CyU4MD2dSrAXNkTces-jJ3RfsNMzC1nZDk/edit .

**INGEN ROM-IMPLEMENTATION, R4, B3c, main-merge, oberoende VERIFICATION eller issue #15-stängning** godkänns genom detta grafiska uppdrag. MAIN väntar med estetisk acceptans tills v0.2 kan granskas i faktisk pixelstorlek.

## MAIN GRAPHICS v0.2 GRANSKAD – v0.3 ENDASTA NÄSTA GRAFIKUPPDRAG (2026-11-16)

MAIN har granskat källorna i [GRAPHICS v0.2-grenen](https://github.com/Odourman/the-skraun/tree/graphics/skraun-v0-2-refinement-20261116/graphics/skraun_v0_2), exakta 8×12-bitmatriserna i `skraun_sprites_v02.json` och `enemy_sprites_v02.json`, 40×24×8 skannlinjers miljöer och halomasker, samt faktiskt öppnat samtliga 8 bildförhandsvisningar och två 2-frame GIF-animationer ur [komplett Drive ZIP](https://drive.google.com/file/d/13lmZX_SbFm27fceYJuE0DdYiZhO7U2q_/view). ZIP har **20 poster/314330 byte**, SHA256 `17227108204134d2fc3cb3dccad69f7633d8d092dd824aa6172bd88c09e9f9ff` matchar oberoende lokal omräkning, 19 interna SHA-poster matchar, `verify_graphics_v02.py` PASS. **v0.2 godkänns som AVSLUTAD REPRODUCERBAR GRAFIKLEVERANS, EJ konstnärlig slutgrafik/Stella/ROM-godkännande.**

C-overhead är bästa tillfälliga arbetsbasen, C-refined reserv. Även C-overhead liknar vid faktisk storlek till viss del frontal humanoid snarare än tydligt fyrbent varelse rakt ovanifrån; dess A/B-poser skiljer **6 bitmapceller**, C-refined **10**. Riddarens svärdsvarning jämfört med idle skiljer endast **4 celler** på högra kanten i fyra övre rader, bågskyttens dragpose endast **2 celler i samma rad**; dessa attackförvarningar och fiendernas topdown-perspektiv är inte ännu godkända. Världarnas åtta symmetriska 40×24 PF-koncept har skogsträd/bergblock/drömpelare/nattmurar men för liten grafisk distinktion om färgerna tas bort.

Halodokumentet: ursprung nivå3 **88 färgklockor×176 skannlinjer** (91,7% av 192 rader), visuellt alltför hög och kantklippt. Alternativ A nivå3 **96×80**, B **128×112** är istället breda ovaler enligt samma konceptuella 4:3-NTSC-visning: fysisk bredd≈1,6×color-clock, bredd/höjd≈**1,92** resp. **1,83**. Dessa är konstförslag, inte auktoriserad attackradie eller fungerande självständigt färgad halo/hinder-PF.

**ENDAST GRAPHICS DESIGN FÅR FORTSÄTTA v0.3** via [bindande MAIN-designbrief](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_V0_3_OVERHEAD_READABILITY_FINAL_DESIGN_GATE_2026-11-16.md) och [Drive-kopia](https://docs.google.com/document/d/1Oc0IEFpPFP9td5CFbKbXVUCQ-ACPdYxMnsFiboUKgkY/edit). V0.3 ska leverera två övertygande overhead-Skraun-förslag eller tydligt konstatera begränsningen, topdown-riddare med klart svärdsvarsel, grön topdown-bågskytt med synlig bågdragning, fyra gråskale-särskilda miljöer och EN proportionaliserad rund halvåg ringfamilj med exakt TIA/4:3-mått. Samlat ZIP, bildbevis, GIF, testskript och källpixeldata. **Stopp efter v0.3 för MAIN:s estetiska beslut.**

**Ingen ROM DEVELOPMENT eller ny R4/B3c, ingen gameplayimplementation, inget main-merge, ingen oberoende VERIFICATION och issue #15 förblir öppen.** R3:s negativa tekniska kapacitetsresultat gäller fortfarande.

## SENASTE MAIN-GRIND: GRAPHICS v0.3 AVSLUTAD – SLUTLIG 8×12-SPRITE INTE GODKÄND (2026-11-16)

MAIN har kontrollerat det kompletta originalpaketet från Google Drive: https://drive.google.com/file/d/1-nlqRBYSmFJG0xRm90DpDBFYud7tgCPh/view . ZIP 386046 byte, 27 poster; omräknad SHA256 `e74757e9877d7f7ea6837721a30633b0d224c13ac4ff189d1fb12aca6a797e26`; ZIP CRC PASS, 26/26 SHA256-manifestposter PASS och `verify_graphics_v03.py` PASS. Textoriginal i separat GitHub `graphics/skraun-v0-3-final-readability-20261116`, HEAD `a98764192e352711370239727775701f8d8336c9`. Alla design-PNG/GIF är icke-Stella mockups. MAIN har jämfört originalteckningen med 8×12 Q1/Q2 och ett separat icke auktoriserat 8×14-förslag samt fiender, fyra världars monokroma bilder och halo i TV-proportioner.

**BESLUT:** v0.3 levererad och GRAPHICS avslutar tilldelat uppdrag. Q1 `splayed_quad` är främsta provisoriska 8×12-testbasen (10 A/B-bitar ändrade), Q2 (12 ändrade) reserv för jämförelse. Ingen är övertygande som fyrbent topdown vid nivå1; den frontalansiktsdominerade originaltolkningen är det grundläggande hindret, och det ritade 8×14-experimentet löser inte automatiskt perspektivet. **NO-GO för att godkänna någon av dessa som final figur**; ingen 8×14 produktionsdimension auktoriseras. Detta är inte bevis att alla tänkbara 8×12 är omöjliga.

**Förbättrade arbetskandidater:** riddare med 12 ändrade svärd-varningspixlar, grön bågskytt med 11 ändrade båg-/skjutpixlar; ingen slutlig fiendesprite accepterad. Skogskronor/stubbar, stegade berg, drömspiraler och nattmurar är godtagbara **tematiska konstnärliga riktningar**, men inga exakta PF- eller TIA-implementeringar eller fritt samtidiga objekt är godkända. Endast **rund 4:3 visuell halo-familj** (40cc×64, 56cc×80, 72cc×112, approx 1,000/1,120/1,029 bredd-höjd) behålls som estetisk **proportionsreferens**; kollisionsradie och spelfunktion är INTE beslutade. Nivå3-klippning i koncept: ca 40,32 % sidokanter och 41,94 % över/under för testade centrum.

Fullständigt och auktoritativt MAIN-beslut: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_V03_FINAL_DELIVERY_DECISION_2026-11-16.md . R3 tekniska NO-GO (20Hz fiender same-Y; 30Hz separata halo/scen; 2–4 statiska rastercykler över) kvarstår. Nästa huvudfråga är **hur en verkligt topdown fyrbent karaktär ska förenklas** utifrån originalets frontalritade identitet, innan en senare avgränsad Stella-konstdiagnostik kan auktoriseras. **Ingen automatiskt auktoriserad v0.4, R4, B3c, ROM-kod, dimensionsbyte, merge till main eller oberoende VERIFICATION.** Issue #15 fortsatt öppen.

## MAIN – GRAFISK PERSPEKTIVSTUDIE P1, EN AVGRÄNSAD NY ORIENTERING (2026-11-16)

Efter avslutad GRAPHICS v0.3 samt MAIN:s NO-GO för Q1/Q2 och ett omotiverat 8×14-format har MAIN gjort ett separat kvalitativt och bitmapkonkret perspektivprov. Det kritiska felsambandet är att Q1/Q2 har små öron/huvud högst upp i bitmapparna och två ben längst ned; det bevarar originalskissens FRONTALVY även när formen beskrivs som topdown. Detta kolliderar visuellt med beslutad kamera rakt ovanifrån och regeln om enbart höger- och vänstervända horisontella spegelbilder. En verkligt topdown fyrbent varelse som är vänd åt höger bör i stället ha **huvudet mot högra bitmapkanten**, rygg/kropp längs den horisontella axeln och **fyra tassar på kroppens övre och undre kontur**, med vänsterbild som bitvis spegling. Detta är en **NY ARBETSHYPOTES, INTE SLUTGODKÄND VISUELL DESIGN ELLER ÄNDRING I SPELREGLER**.

MAIN skissade två grova 8×12-masker H1/H2 med horisontell kropp och jämförde med v0.3 Q1. De ger mer fyrfotad topdown-riktning utan nya rasterrader, men är ännu generiska och inte tillräckligt karakteristiska. Skisserna är inte grafikcanon eller Stella-bevis. Det nuvarande R3-VFIX-testets 'head above feet' kontrollerar med rätta den GAMLA sprites radorientering, men får inte användas som krav på en ny medvetet sidriktad kropp; en sådan behöver ett separat per-facing huvud-höger/huvud-vänster-kontrakt när ROM-implementation en dag auktoriseras. Bevara alla gamla regressioner och historiska ROM-evidens oförändrade.

**NYTT ENDA DESIGN-SCOPE:** GRAPHICS P1, **en separat avgränsad designstudie efter v0.3** (INTE en ny obegränsad v0.4-omgång). Två genuint olika 8×12 overhead-kandidater med horisontell kroppsaxel, A/B och vänster-/högerspegling, bevarade öron/ögon/grått/fyrbent och originalidentitet, jämförda med Q1 vid korrekt 4:3-fysisk skala; dokumentera även om motivet i stället blir insekt/sköldpadda. En samlad jämförbar leverans och sedan STOPP för MAIN:s beslut. Scope i GitHub: https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_P1_HORIZONTAL_AXIS_PERSPECTIVE_PROOF_2026-11-16.md ; Google Drive: https://docs.google.com/document/d/1969WMNNJoCZYwsYFkIfWRuqDr2d4ACnxDyi7V6hCHsM/edit .

**R3:s fullmotor-NO-GO gäller oförändrat.** Ingen ny ROM/6502, R4, B3c, fiende-AI, permanent byte till 8×14, visuellt slutgodkännande, merge, oberoende VERIFICATION eller stängning av issue #15. Endast det beskrivna grafiska representationsprovet auktoriserat.

## MAIN GRAPHICS P1 SLUTGRANSKNING / P01-ART1 BEGRÄNSAD STELLA-AUKTORISATION (2026-11-16)

MAIN kontrollerade faktiskt GRAPHICS P1-arkivet i Drive: https://drive.google.com/file/d/1ouk4vL_gBVcb3Jc_-EP5UKSQLV1mEaSC/view , exakt 376608 byte, ZIP SHA256 `d716e93cf6f15f5944fb9716efffd1217d2c716dbc3909906c2ba382aa728cd1`, 15 ZIP-poster, ZIP CRC PASS, 14/14 interna SHA256SUMS-poster PASS, lokal `verify_p1.py` PASS; 7 PNG designbilder, 2 tvåbildrute-GIF, giltiga 8×12 bitmasker, montering av två gångposer och spegling. GitHub-källgren `graphics/p1-horizontal-axis-perspective-proof-20261116`, HEAD `b5bc31a3485faf67199631c01768bf221f061292`. Dessa är konst-/pixelmockups, INTE Stella-ROM eller oberoende VERIFICATION.

**DESIGNBESLUT:** GRAPHICS P1 avslutas som källgranskad perspektivstudie. Horisontell ryggrad, huvud åt höger när högerorienterad och åt vänster när spegelvänd, samt fyra tassar ovan/under kroppen är en tydligare tvåorienterings- och topdown-modell än Q1:s gamla vertikala kropp. **Kandidat A rundad rygg väljs endast som huvudreferens för ett senare isolerat P0-spriteprov**, kandidat B behålls som kontroll mot mer insektslik form och Q1 som gammal frontvänd kontroll. Varken A/B/Q1 är estetiskt slutgodkända; A riskerar sköldpadds-/skalbaggeläsning och förlorar delar av originalteckningens mun, horn, mimik. Ingen produktionsdimension 8×14 väljs. Grafikärende #15 hålls öppet.

**NY SEPARAT ROM-AUKTORISATION FRÅN MAIN:** P01-ART1 ett litet P0-only verkligt Stella-läsbarhetsprov, med högst tre 4 KiB NTSC-diagnostiska ROM:er, A jämfört med B/Q1, 3 nivåer, gångpose A/B, vänster/höger, riktiga pixelorienteringstester, 262 NTSC-scanlines, cykel/RAM/ROM-redovisning och användbart autentiskt skärmbildsbevis. Inga fiender, hinder, halo eller spelmekanik. R3-VFIX:s gamla huvud-överst-kontroll behålls för den frysta äldre spritesen; den nya sidriktade P0-spriten måste kontrolleras med huvud-höger/huvud-vänster och tassarnas över-/undersida, utan ändringar i gammal ROM-evidens.

Detaljerat MAIN-beslut GitHub: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_P1_HORIZONTAL_AXIS_REVIEW_AND_DECISION_2026-11-16.md ; Drive https://docs.google.com/document/d/1mwxM_DhPszymDVwd3lC_ToqnBfSsQzHa9GMWi7Zat2c/edit . P01-ART1 bindande arbetsorder GitHub https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P01_ART1_SKRAUN_STELLA_VISUAL_READOUT_AUTHORIZED_2026-11-16.md ; Drive https://docs.google.com/document/d/1WYSIlDjrg8ij55awe1zhTEPx-lxs2xlJSbnSKEsiKxM/edit .

**INGEN R4, B3c, P01-ART2, ny grafikversion, gameplay, main-merge eller oberoende VERIFICATION** auktoriserad här. R3 fullspels-NO-GO står kvar: same-Y fiender cirka 20 Hz, halo/hinder konkurrerar om samma PF och ger 30/30Hz eller färgkonflikt, värsta rastermarginal 2–4 statiskt beräknade cykler, pil/orb/HUD ännu ej bevisade. En tekniskt PASS på en ensam P0-sprite ger INGEN fullspelsrenderer-PASS.

## MAIN II – P01-ART1 SLUTGRANSKNING OCH GRAPHICS P2 BESLUT (2026-11-16)

**P01-ART1 avslutad som reproducerbar utvecklardiagnostik, INTE teknisk eller estetisk PASS.** MAIN II laddade själv ned den faktiska inner-ZIP:en, kontrollerade 361942 byte, SHA256 `3dcdc3e1837a8543e36ff9577aa7dad5528b811180b261419b2363e463a16c4e`, ZIP CRC, 275/275 manifesthashar, tre 4096-byte ROM-hashar och 36 verkliga Stella 320×228 PNG-pixelmatriser mot frysta A/B/Q1-masker. **24/36 PASS** (hela nivå 1 och 2), **12/36 FAIL** (samtliga nivå3: extra fullgrå 64-pixelrad vid PNG Y94, +48 extra grå pixlar A/Q1, +64 B). Verklig Stella Debugger dokumenterade 36×262 NTSC scanlines. Röd strikt Actions-test #43947105697 är legitimt FAIL; grön packnings-Action #43948698028 avser bara arkiv-/manifestintegritet. Original ROM-test-PR [#18](https://github.com/Odourman/the-skraun/pull/18) **DRAFT/UNMERGED**, fruset historiskt evidens; ingen fix.

**Kvalitetsgrindar:** utvecklararbetsorderns spårnings-issue [#17](https://github.com/Odourman/the-skraun/issues/17) stängdes med uttrycklig **diagnostik levererad, INTE art/teknisk signoff**; separat tekniskt reproducerat nivå3-fel [#19](https://github.com/Odourman/the-skraun/issues/19) är **OPEN och INTE auktoriserat för reparation**; användargodkännande av Skrauns figur och all övrig konst [#15](https://github.com/Odourman/the-skraun/issues/15) **OPEN**; oberoende P01 [#1](https://github.com/Odourman/the-skraun/issues/1) **OPEN**. Horisontell P1 A är mest fyrbent, men läses sköldpadda/skalbagge; B insektslik och Q1 frontal. **INGEN originalhorn/mun/ögon/identitet är godkänd vid nivå1.**

**MAIN II:s enda nya auktorisation:** ett **enda tidsmässigt avgränsat GRAPHICS P2 IDENTITETSSTUDIE, BARA DESIGN**, efter användarens fortsätt-instruktion. [Bindande P2-handoff](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_GRAPHICS_P2_SKRAUN_IDENTITY_SILHOUETTE_PROOF_AUTHORIZED_2026-11-16.md), [spårningsissue #20](https://github.com/Odourman/the-skraun/issues/20), [Drive-kopia i grafikmappen](https://docs.google.com/document/d/1EHCu8RPBH3aMPMQCB7nIJwrjsq7jQn7Rw9W7pJN8xZU/edit). **Två** genuint olika 8×12 fyrbenta overhead-silhuetter: I1 prioriterar horn/öron + öppen mun, I2 prioriterar karaktäristiskt långa framlemmar/bakfötter; båda 2 A/B-poser, exakta vänster/höger-speglar och 3 *konceptuella* skalenliga nivåer. **P1 A är fryst benchmark.** Företrädesvis bedöms riktig igenkännbarhet på nivå1 i original pixelstorlek, inte automatisk källtest-PASS. DESIGN-PREVIEW ≠ STELLA. Privat originalteckning får inte publiceras. En samlad jämförbar designleverans och sedan **STOPP** för MAIN/user-godkännande. Om inga övertygar: rapportera negativt och begär nytt separat vägval, **INGEN automatisk P3/v0.4**.

**ALLT ROM-SCOPE STOPPAR:** ingen P01-ART2, nivå3-fix, R4, B3c, större spriteformat, nya game rules, fiender/halo/UI-spelimplementation, main merge, oberoende VERIFICATION eller stängning av #15. R3 fullspelsrenderer har fortsatt tekniskt **NO-GO** för testad arkitektur (same-Y fiender 20Hz, halo mot olika-färgade hinder 30/30Hz eller samma färg, statiskt 2–4 cykler kvar, pil/orb/HUD ej bevisade).

## MAIN II — GRAPHICS P2 FINAL NEGATIVE IDENTITY DISPOSITION 2026-11-16

MAIN II har laddat ned och granskat den faktiska GRAPHICS P2-käll- och designleveransen: Drive ZIP `THE_SKRAUN_GRAPHICS_P2_IDENTITY_2026-11-16.zip` **168904 byte**, SHA-256 `5bc754ba215a212778744ada1e3bffab7bc2eb1a5ddfb1da138c612d21891e15`, ZIP CRC och **23/23 SHA-manifestfiler PASS**. Valideringsskript `validate_p2.py` kördes separat och passerade. GitHub P2-grenen innehåller **8 nya design-/källfiler** jämfört med fryst P1-gren, inga gamla P1-filer ändrade, ingen ROM eller merge. MAIN jämförde originalteckningen (privat) med de verkliga 8x12- och L1-4:3-förhandsvisningarna.

**BESLUT: GRAPHICS P2 LEVERANS ACCEPTERAD SOM AVSLUTAD NEGATIV DESIGNSTUDIE; IDENTITY FAIL; INGEN SLUTSPRITE.** I1 kodar negativt utrymme för ögon/mun/horn men känns inte som original-Skraun i faktisk L1-storlek; I2 separerar lemmar bättre men uppfattas som insekt/krabba. Frysta P1 A är fortfarande fyrbent topdown-referens men sköldpadda/skalbagge, inte final figur. Att projektet misslyckats med dessa 8×12-kandidater bevisar **inte** att varje tänkbar 8x12 är omöjlig, men samma optimering upprepas inte automatiskt.

[MAIN II:s bindande P2-review](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_GRAPHICS_P2_IDENTITY_REVIEW_AND_DECISION_2026-11-16.md); [P2 ärende #20](https://github.com/Odourman/the-skraun/issues/20) stängt som avslutad **leverans, inte art-pass**. Originalteckningens identitetskännetecken kvarstår som ouppfylld kravbild. [Visuell grind #15](https://github.com/Odourman/the-skraun/issues/15), [ART1 L3-fel #19](https://github.com/Odourman/the-skraun/issues/19) och [oberoende P01-grind #1](https://github.com/Odourman/the-skraun/issues/1) är alltjämt OPEN. R3:s fullspels-NO-GO gäller. Ingen ny P3/v0.4, ART1-reparation, ROM/ART2/R4/B3c, formatbyte, kamerabeskärning, slutgodkännande, merge eller VERIFICATION auktoriserad. Nästa steg kräver ett uttryckligt MAIN/användarval om kompromiss mellan strikt overhead/8×12/originalidentitet eller ett separat tekniskt kostnadsprov.
