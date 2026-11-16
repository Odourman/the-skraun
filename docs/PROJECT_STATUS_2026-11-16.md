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
