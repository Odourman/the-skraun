# THE SKRAUN — MAIN III N3: gemensamt värstascen-, resursägar- och gameplaykontrakt
**Version 1.0.0 | 17 november 2026 | N3 SOURCE-ONLY – avslutad dokumentations-/analysgrind | INGEN ny ROM, sprite, gameplayändring, mapper eller independent Verification**

## 0. Beslut och användning
**N3 levererar ett gemensamt falsifierbart scenkontrakt för RESEARCH N4/N5, senare ROM DEVELOPMENT N7/N8 och oberoende verifiering av framtida frysta resultat.** Det är INTE en ny engine-arkitektur, ett pass för R3 eller ett godkännande av en färg- eller flimmerkompromiss. **Alla testexempel som inte uttryckligen hämtats från en tidigare riktig ROM är syntetiska diagnostiska koordinater, inte officiella åtta nivåer.** Matcher för nya kernels måste ha källa/commit, version, mask/rad/färg/aktörstest och ärliga begränsningar.

**Senaste verifierade GitHub före N3:** main `47db8a332c333bee74afb5317a139f1831880b51`; P01-COL1 draft [PR #27](https://github.com/Odourman/the-skraun/pull/27), HEAD `90f89441b41a2e82408581b81d3743b1423e5cdb`; N2-granskningen finns [här](MAIN_III_P01_COL1_N2_WORST_CASE_CPU_RIOT_STACK_AUDIT_2026-11-17.md). Öppen PF [#25](https://github.com/Odourman/the-skraun/issues/25); tidigare [R3 NO-GO](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md) för den testade klassen. 19/19 genuina utvecklar-Stella COL1 cases och N2 konservativ beräknad P0-kollision PASS i begränsat scope, INTE full renderer.

**Filer:** detta dokument (normativ scenbeskrivning) + [maskinläsbar scenkatalog](MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json) (samma 10 ID och testinvarianter, avsedd som fryst indata för jämförelse; inga kodexekveringar).

## 1. Fyra auktoritetsnivåer – får inte blandas
- **Bindande spelcanon från användaren:** [beslut 01–60 inklusive senare korrigering](DESIGN_DECISIONS_01-60_2026-11-16.md) och [fast U1-LEG1 visuellt beslut](SKRAUN_VISUAL_DIRECTION_2026-11-16.md). Skraun UPPRÄTT och ljusgrå, ögon/horn/mun upp, armar åt sidor, getben; identiska 8×12 A/B source-cell-data vid level 1/2/3 med endast storleksskalning; visuellt RIGHT kommer från original LEG1 LEFT, visuellt LEFT från original RIGHT. Vid vertikal joystick ska varken figuren roteras eller en ny UP/DOWN-sprite användas.
- **Tekniska testmål/arbetsantaganden, INTE canon:** exakt 8×12,16×24,32×36 fysisk mask enligt prototyp; kollisionshitbox är tills vidare full fysisk kropp; 160×176 arena +16 HUD är R3/COL1 diagnostic-layout; 262 NTSC, 76 6507-cykler/physical scanline. Måttens slutliga spelanvändning skall visas/valideras; 4:3 skärmpresentation kan ge andra uppfattade proportioner vid x4/y3.
- **Källa som redan faktiskt observerats:** R3 hade 3 aktörer same-Y vid 20Hz var (4/12 frames), mellanfas 30/30/60Hz, full same-color PF gold-merging eller 30/30Hz gold/blue whole-frame alternation, ~2–4 statiskt beräknade rastercykler över, 89B P1Buf samt 23B state. ART1 separat first-top L3 sprite-kernel defekt #19; COL1 annan diagnostisk kernel, N2 statiskt ≤63/76, VBLANK ≤2372/2752, 28B variabler+4B returstack. Dessa värden får **aldrig adderas naivt eller beskrivas som samma arkitektur.**
- **Hypotes som ännu inte prövats:** sparsamma PF-skrivningar, exakt horisontella COLUPF-gränser med X/Y färgregister, multipla specialkernels, VDEL, same-Y P1 reposition/GRP1 retrigger eller enemy-only Venetian, nivåanpassad 1-/2-/3-radersfördelning. Ett source-only tidsschema är inte en fungerande original-TIA-ROM.

## 2. Fysiska spel- och bildkoordinater
- X i denna testkatalog = **TIA color clocks 0–159**. R3:s sparade 320-pixelbilder visar normalt två screenshot-pixlar per färgklocka; en faktisk PF-celldel är fyra färgklockor. Y i scenobjekt = preliminär **arena-ankare 0–175** där befintlig diagnostik har 16-raders HUD inom 192 synliga rader. **Kandidatens egen exakta top/bottom, P0 start/slut, spegel/row-order, sprite height och Y-ankare måste deklareras innan resultat jämförs.** Blandade R3 EnemyY (special 2-line output) och COL1 PlayerY får aldrig tolkas automatiskt som identiskt raster-origo.
- R3:s kända enemy stress-cells är (32,78), (101,78), (147,78). Originalets halo-mask omfattar X=56,60,…,104 i 13 positioner; den svåra **source**-situationen är X80/X84 **R3/PF-REP1B källmaskrad 98**. Det är INTE utan särskild koordinatöversättning den fysiska TV-scanlinen 98; nästa forskningsrapport måste visa faktisk rasterrad + beam-klocka. De är förankrade i fryst R3-data. Övriga X/Y i fixture är markerade syntetiska. En P0 på (104,80) är **syntetisk stressposition** informerad av tidigare partiell skymning, inte en påstådd R3 spelar-variabel.
- Enkel 262-raders NTSC-kontroll: ungefär 3 VSYNC +37 VBLANK +192 synligt +30 overscan. **Detta är referenssegmentering, inte en ny bindande exakt linjefördelning för varje kernel.** Per verklig fysisk linje högst 76 CPU-cykler inklusive WSYNC/beamfönster; en 2-/3-line kernel får ALDRIG spendera 152/228 cykler före en registerdeadline på den första linjen. Alla faktiska PF-cell-deadlines, RESP/GRP/HMOVE och färgändringar måste räknas mot färgstrålens tidpunkt.
- Tider för NTSC diagnostic: ~0,4s riddarvarning ≈24 bildrutor vid 60Hz, 0,5s halo ≈30 rutor, ~1,0s återhämtning ≈60. Dessa är **testkonverteringar**, inte nya kanoniskt låsta frameantal; balanseringsvärden och verklig FPS testas senare.

## 3. TIA:s register och färgägarbok – hårdvarufakta
| Fysisk generator | Primära register och styrning | ÄRVD färg | Reserverat innehåll / konflikt | Tillåtet forskningsalternativ |
|---|---|---|---|---|
| **P0** | GRP0, RESP0, HMP0, REFP0, NUSIZ0, VDELP0 | COLUP0 | **Upprätt Skraun, låst U1-LEG1 A/B**. Ingen ny permanent ansikts-P1 som stjäl enemy-slot. | Del av HUD-kernel **endast utanför riktig arena** om latched graphic/position reset bevisas. |
| **P1** | GRP1, RESP1, HMP1, REFP1, NUSIZ1, VDELP1 | COLUP1 | Två olika röda riddare och en grön archer, **tre aktiva med oberoende X/Y**. TIA har BARA en P1-generator; full same-Y 20Hz R3 ej accepterad som renderer-GO. | GRP1 retrigger, source-exakt special-/flerlinjekernel; same-Y måste bevisas, kan ej påstås genom tre fasta NUSIZ-kopior. |
| **M0** | ENAM0, RESM0, HMM0, NUSIZ0 missile-width | **COLUP0 = P0** | Pil kan bli Skraun-grå; alternativ P0-nionde pixel stjäl pilkapacitet. Inte gratis separat gul/blå skikt. | Dynamisk roll endast om P0-färg/arrow-ägarskap och samtidighet bevisas. |
| **M1** | ENAM1, RESM1, HMM1, NUSIZ1 missile-width | **COLUP1 = P1** | När P1 växlar riddarröd ↔ archgrön kan M1 inte behålla en egen färg utan extra rasterplan. | Endast med explicit COLUP1-timing och actor synlighet. |
| **PF** | PF0/PF1/PF2, CTRLPF, spegling/asymmetri | COLUPF | Både gul 360° halo och distinkta **solida hinder** vill ofta dela en fysisk PF-cell/linje; min 4 color-clocks per cell. Ändra inte logisk collision utifrån visuellt PF. | Selective delta-write + exact midline COLUPF writes som inte missar deadline; geometrisk prioritet vid exakt pixelöverlapp explicit redovisad. |
| **BL** | ENABL, RESBL, HMBL, VDELBL, CTRLPF ball-width | **COLUPF = PF** | Orb kan **inte** automatiskt vara självständigt färgsatt och kvarstå medan PF alternerar gold/hinder. Statiska enbit-breddar ritar inte godtycklig ring. | Möjligen orb/effect efter explicit roll/årstid/färgevent proof. |
| **BK** | COLUBK | COLUBK | Färgar ALLA avmaskerade pixlar i aktuell zon. En gul 'bakgrundshaloring' smetar ut hela raden utan separat konturmask. | Bakgrundsfärgzoner med klock-exakta horisontella övergångar, ej automatisk ny sprite. |
| **HUD** | Egen zon/kärna, kan låna P0/P1/PF | Delar alla ovanstående | **Riktig läsbar poäng + antal liv**; den gamla R3 16-row cyan placeholdern är INTE faktiska score/lives. HUD↔arena-gränsen måste nollställa PF/GRP/färg/position. | 48px score-kernel i separat band om crossing/timing bevisas. |
| **Audio** | AUDC0/1, AUDF0/1, AUDV0/1 | Ej grafik | Två ljudkanaler, halo/träff/enemy/orb/liv + banjingle, utan konstant spelmusik. | Prioritetschema i VBLANK/overscan, men delar CPU-tid med AI/fysik. |

**Slutsats:** 7 grafiska objekt men bara 4 färgdomäner (P0+M0; P1+M1; PF+BL; BK). Det finns alltså **INGET fristående val av gul/stenfärg för BL/M0/M1**. Den exakta objektägaren per rad/frame för pil, orb, halo/hinder är **ÄNNU EJ BESLUTAD**. Det är det N4–N6 ska utreda; N3 låser bara konflikterna och deras mätkrav.

## 4. Gameplay-/fysikkontrakt (oberoende av ritväg)
| Interaktion | Oföränderligt resultat | Spårbarhetsstatus |
|---|---|---|
| Skraun BODY mot solid obstacle / arena edge | BLOCK. Diagonalt glid bara längs fri axel, utan corner-cutting; open L3. | #33,#46,#55 samt senare användarinstruktion |
| Riddarens svärd mot solid | BLOCK; aktiv huggträff endast inom kort aktivt window. Ingen skada under varning/återhämtning. | #13,#22–23,#36,#43–44 |
| Bågskyttspil mot solid, halo eller edge | Pil försvinner; max en pil samtidigt, riktning låst vid avfyrning. | #14,#24,#34,#41–42 |
| Halo mot solid | Magi PASSERAR; kan träffa fiende/pil bakom solid inom faktisk ringradie. | #04,#35 |
| Kroppskontakt med riddare | Ingen skada, endast ett AKTIVT svärdshugg gör det; fiender skadar eller blockerar inte varandra fysiskt. Spelarens bodies får ingen ny obehörig studsmekanik. | #13,#45 |
| Riddare windup och timing | Stannar/höjer svärd ~0.4s, huggriktning låst VID windup start; kort attackaktivt fönster följt av ~1s recovery. | #22–23,#43–44 |
| Archer | Grön, huvudsakligen flyr, skjuter från fri sikt om möjligt; kort stopp; låser AIM vid PILENS avfyrning; intervall skog~3s/berg~2.5s/dröm~2s/natt~1.5s. | #14–16,#38–40 |
| Skraun attack / damage | 360° gul aktiv halo ~0.5s, cooldown beroende på level, eld hålls för auto-retrigger, kan röra sig under halo och ~1s skadeskydd; träff sänker level, vid L1 förloras liv. | #02–05,#10–12,#48–50 |
| Orb | En per banbesök, syns från start, safe locations, L1->L2 eller L2->L3; vid L3 står kvar, får hämtas efter senare nivåförlust. Ingen osynlig teleport för tillväxt. | #08,#26–27,#51–53 samt L3-tillägg |
| Enemy count / reserves | Två aktiva riddare + en archer; natt totalt fyra riddare men reserves inte simultant över två; reserv kommer ~2s efter ledig plats från rimlig kant. | #17–19,#52 |
| Score, death, stage | 100 riddare, 250 archer, extraliv /2000p, tre startliv, statepersist vid död/banövergång; 8→7→…→1 med upprepade ändbanebesök och återställd orb/fiender på varje nytt besök. | #06–09,#28–32,#52–60 |

**Specifik nej-claim:** TIA:s hårdvarukollisionslatches räcker inte för full gameplaytruth: en PF-halo som passerar väggar och PF som blinkar/färgbyter kan inte ges samma betydelse som solid kropp/svärd/pil. Beroende hitbox/stater måste förberedas i RIOT-/overscan-CPU.

## 5. RAM-, ROM-, stack- och tidskontrakt
- RIOT har **128 byte inklusive returstack**, inte 128B plus 6507 stack. N2 COL1: $80..$9B = 28B variabler, max två JSR-nivåer =4 returstackbytes, N2 ≤2372/2752 VBLANK konservativt. R3: 23B state +89B P1Buf =112B varav stackrisk + minst 9 tydligt lediga mittbytes. **R3 112 + COL1 28 =140 >128 även före stack, fiende-AI, pil/orb, HUD**. Detta visar att ett framtida kombinationssystem måste ERSÄTTA/överlagra R3 buffert eller omdesigna, inte importera COL1 slaviskt. N3 är inventering, inte ny allocation.
- Framtida manifest SKA bokföra lagrade P0 X/Y/level/facing/pose, ring aktiv/cooldown, player invulnerable, lives/score, två knight + archer X/Y/state/timers/sword-facing, reservknight/level, arrow X/Y + fixerad vektor/active, orb X/Y/status, solid rect pointers, rendering PF mask pointers, P1 row-buffer eller display-list, stack high-water, sound priority, stage/loop index. Byte-live-tid (VBLANK/visible/overscan) skall vara explicit om RAM överlagras.
- Varje fysisk visible scanline kräver PC/opcode/cycles med absolut WSYNC-offset, PF0/PF1/PF2, GRP0/1, COLUPF, COLUP0/1, RESP/HMOVE, CTRLPF, ENAM0/1, ENABL händelser. För varje registerskrivning ska verklig BEAM-färgklocka och celldeadline redovisas. Räcker inte med 'genomsnittlig 74/76' eller '3 line => 228 cykler'.
- Under VBLANK/overscan: räkna **värsta 60Hz-rutan** (t.ex. 3 actors AI + collision + arrow/orb + scoring + sound + new knight spawn + growth) mot faktisk RIOT timer, samt worst if music/score/jingle. NTSC 262 med korrekt VSYNC/VBLANK/HUD/arena/overscan. ROM-bankswitch endast efter separat uttrycklig plan och verifierad faktisk ROM-kostnad; ingen DPC/ARM/Superchip automatism.
- Alla nya ROM-krav: fryst branch + commit + SHA256 source/BIN, riktiga DASM .lst/.sym och original Stella 6.7.1 RAW frames (12-frame +24-frame för anfall), exakta aktörspixlar, 262-line riktig debugger, controller input log F1-vs-RAM injection märkt. Independent Verification först efter MAIN fryser leverans.

## 6. Testscenerna — separata scen-ID och negativa kontroller

### S0 — U1-LEG1 P0 identity and movement at all levels
**Prioritet:** BASELINE; **vidare grind:** N3/N8/N9. **Aktuell evidens:** sprite source and isolated COL1 demonstrated; full-scene UNTESTED.

**Testsyfte:** Freeze exact source sprite, P0 spatial/screen origin, two A/B frames and LEFT/RIGHT semantics before trying other resource owners.

**Fryst indata:** [{"level":1,"width":8,"height":12},{"level":2,"width":16,"height":24},{"level":3,"width":32,"height":36}].

**Testhändelser:** (1) A/B each level, visual RIGHT maps original LEG1 LEFT; visual LEFT maps original LEG1 RIGHT; (2) cardinal up/down retain facing; eight direction travel and source match; (3) level 3 first/top and final/bottom row and no HMOVE cross-object shift.

**Skall redovisas/bestå:** (1) P0 origin source U1-LEG1 pixel-perfect at its approved source cells; (2) same two base poses and no redrawn graphics as level changes; (3) no extra/missing raster row from ART1 #19 regression; (4) identical gameplay speed policy at all levels, no illegal diagonal corner cut.

**Negativ kontroll:** R3 prior upside-down orientation, ART1 top-row ghost, P0 moved when repositioning P1.

**Bevis som KRÄVS senare:** raw 12/24/36 scanline masks and renderer-to-source pixel comparison; actual 12-frame Stella screenshot sequence for moving P0 when authorized; input log shows real read versus debugger RAM injection.

### S1 — Three independent same-Y opponents, original R3 negative control
**Prioritet:** P1; **vidare grind:** N5/N7/N8. **Aktuell evidens:** R3 three actors 20Hz NEGATIVE; alternatives source-only.

**Testsyfte:** Find whether two distinct sword knights and a green archer at equal Y can remain readable without R3 full-frame 20 Hz slot rotation.

**Fryst indata:** [{"enemy":[{"type":"knight1","x":32,"y":78},{"type":"knight2","x":101,"y":78},{"type":"archer","x":147,"y":78}],"troll":{"x":80,"y":78,"level":3},"coordinate_status":"adversarial fixture; enemies exact R3 observed positions, troll new candidate centre"}].

**Testhändelser:** (1) 12 consecutive frames, then 24 frames while knight telegraph changes; (2) identical source art/position and independently track each actor; (3) same-Y Y=78, no designer-enforced separation.

**Skall redovisas/bestå:** (1) three individually identifiable opponents at their own X/Y; no merged dummy sprite; (2) distinguishable red knights and green archer, including during sword tell; (3) report per-actor visible pixels per frame, longest absent-frame run and effective visual frequency.

**Negativ kontroll:** R3 same-Y each actor 4/12 frames=20 Hz; 2/3 completely absent; single-P1 NUSIZ copies with fixed X spacing do not count as independent.

**Bevis som KRÄVS senare:** 12 raw uncomposited actual frames after new authorized ROM, explicit actor masks; per-frame actor/weapon visibility tabulation against R3 reference.

### S2 — P1 order, spacing and HUD-zone boundary stress
**Prioritet:** P1; **vidare grind:** N5/N8. **Aktuell evidens:** UNPROVEN in replacement renderer.

**Testsyfte:** Do not let one handpicked X ordering, separation, or Y zone make a kernel look general.

**Fryst indata:** [{"enemy":[{"type":"knight1","x":120,"y":78},{"type":"knight2","x":40,"y":78},{"type":"archer","x":80,"y":78}],"coordinate_status":"synthetic permutation"},{"enemy":[{"type":"knight1","x":67,"y":78},{"type":"knight2","x":83,"y":78},{"type":"archer","x":101,"y":78}],"coordinate_status":"synthetic close-but-distinct; overlap semantics must be recorded"},{"enemy":[{"type":"knight1","x":40,"y":17},{"type":"knight2","x":80,"y":18},{"type":"archer","x":120,"y":19}],"coordinate_status":"synthetic near top HUD/arena transition"}].

**Testhändelser:** (1) reverse actor type order without swapping their identities; (2) VDEL/RESP1/HMOVE and color register crossover in one and multiple scanlines; (3) move actors one cell across any proposed graphics zone boundaries.

**Skall redovisas/bestå:** (1) three real position coordinates independent of fixed hardware copies; (2) no unintended P0 displacement when changing P1 HMOVE, no HUD leakage into arena; (3) document close-range physical overlap, priority and game logic, no fake actor separation.

**Negativ kontroll:** R3 partial overlap P0 occlusion: 128/136=94.1% pixels were masked on one test frame; three separated Y bands PASS does not imply any same-Y solution.

**Bevis som KRÄVS senare:** per-scanline actual GRP1/COLUP1/RESP1/HMOVE register time slots; X permutation and two-level moving-frame sequences.

### S3 — P0+knight visual overlap with live weapon telegraph
**Prioritet:** INTERACTION; **vidare grind:** N5/N8/N9. **Aktuell evidens:** Full-scene UNPROVEN; test may expose required visual choice.

**Testsyfte:** Distinguish actor presence in RAM from a readable dangerous object when P1 overlaps large P0.

**Fryst indata:** [{"troll":{"x":104,"y":80,"level":3},"enemy":[{"type":"knight1","x":105,"y":80,"phase":"telegraph"},{"type":"knight2","x":124,"y":80,"phase":"chase"},{"type":"archer","x":147,"y":80,"phase":"flee"}],"coordinate_status":"synthetic stress, informed by measured R3 P0 occlusion, not a legal spawn prescription"}].

**Testhändelser:** (1) hold at least ~24 NTSC frames of knight windup; then sword active and recovery; (2) reverse display priority if proposed, but never silently change collision effect; (3) P0 moving within active halo while weapon telegraphs.

**Skall redovisas/bestå:** (1) knight action and sword warning must be reportably readable despite overlaps; (2) P0 and all enemies retain frozen source identity; projectile/halo logic not inferred from color; (3) physical overlap does not itself inflict sword damage.

**Negativ kontroll:** R3 partial case 94.1% of one knight's red pixels occluded.

**Bevis som KRÄVS senare:** 24 raw frames plus per-actor bbox/mask/visible-pixel accounting; 4:3 video inspection; strike direction locked at telegraph start.

### S4 — PF gold halo vs contrasting solids, R3 source mask row 98
**Prioritet:** PF_COLOR; **vidare grind:** N4/N7/N8. **Aktuell evidens:** SOURCE-ONLY FAIL for tested naive methods; N4 unstarted.

**Testsyfte:** Ask whether time-varying PF masks and COLUPF events can draw two visibly different spatial functions in same frame and physical scanline.

**Fryst indata:** [{"halo":{"x":80,"level":3},"source_mask_row":98,"geometry_source":"R3 halo L1/L2/R0/R1/R2 source masks, PF-REP1B"},{"halo":{"x":84,"level":3},"source_mask_row":98,"geometry_source":"R3 mask second exact case"}].

**Testhändelser:** (1) gold ring ON with independently solid contrasting obstacles on same physical scanline; (2) test left PF and right asymmetry; isolate each source mask before composite; (3) preloaded X=gold/Y=solid STX/STY hypothesis with original R3 X/Y liveness conflict.

**Skall redovisas/bestå:** (1) report exact PF0/1/2 and COLUPF event completion before each 4-color-clock PF cell's beam deadline; (2) for distinct destination cells requiring different colors, both colors appear same 60Hz frame; (3) at mathematically identical requested pixel, output one documented visual priority, never claim two colors simultaneously.

**Negativ kontroll:** PF-REP1 simple one-write/two-line cannot represent source masks; PF-REP1B naive 5-cycle events fail 56/60 among 416 critical mixed rows; toy 3 cycles not full solution; R3 golden solids or gold/blue alternating 30/30 whole frames disallowed as pass.

**Bevis som KRÄVS senare:** source mask enumeration per X,Y and color transition times with CPU instruction/liveness table; later if authorized: actual Stella raw RGB and direct debugger cycle timing.

### S5 — Halo X56/X104 edge, reverse and unequal PF halves
**Prioritet:** PF_COLOR; **vidare grind:** N4/N7/N8. **Aktuell evidens:** SOURCE masks known, new scheduler UNPROVEN.

**Testsyfte:** Catch clipping, wrong right-PF2, shifted ring centre and orphan scene pixels from a centered demonstration.

**Fryst indata:** [{"halo":{"x":56,"level":3},"test":"leftmost original R3 diagnostic position"},{"halo":{"x":104,"level":3},"test":"rightmost original R3 diagnostic position"}].

**Testhändelser:** (1) X56->60->...->104 and direction reverse; (2) same gold/contrasting solids at original scene Y bands; (3) P0 remains at its visual center and original 4x L3 horizontal footprint.

**Skall redovisas/bestå:** (1) all R3-required source mask columns represented or explicit exact pixel-level failure; (2) asymmetric right PF2 updates before beam crossing; (3) no ghost columns, no unrelated P0 HMOVE shift, no inaccurate 2-clock recentering claim.

**Negativ kontroll:** R3 right-PF2 source-required cells and measured approx 2-clock visual center displacement.

**Bevis som KRÄVS senare:** left/right 13-X original mask diff, per-row PF0/1/2 write schedule; raw screenshot bounding box vs source pixel cells.

### S6 — Simultaneous arrow, persistent orb, HUD and resource-owner conflict
**Prioritet:** OWNERSHIP; **vidare grind:** N3/N6/N8. **Aktuell evidens:** No completed single-ROM coexistence proof.

**Testsyfte:** Prevent single-object microROM successes from hiding that all seven TIA graphical generators and four color owners are already contested.

**Fryst indata:** [{"troll":{"x":80,"y":88,"level":3},"enemy":[{"type":"knight1","x":32,"y":80},{"type":"knight2","x":101,"y":80},{"type":"archer","x":147,"y":80}],"projectile":{"x":92,"y":98,"active":true},"orb":{"x":116,"y":112,"available":true},"halo":{"x":80,"active":true},"hud":{"score":true,"lives":true},"coordinate_status":"synthetic worst-resource overlap, not a canon map"}].

**Testhändelser:** (1) arrow visible while halo active and orb not yet taken; (2) arrows move fixed after shot; show arrow destroyed by halo or solid when appropriate; (3) enemy colors remain red/red/green independent of any missile allocation.

**Skall redovisas/bestå:** (1) P0/GRP0 dedicated to player, P1/GRP1 enemy scheduling must not be silently borrowed for permanent orb; (2) no implicit M0/M1/BL independent color: M0 shares COLUP0, M1 shares COLUP1, BL shares COLUPF; (3) HUD score and lives readable, but R3 HUD placeholder not credited as gameplay; (4) owner ledger shows exact byte/visible frame/register-color-domain for every object.

**Negativ kontroll:** simple Ball-as-independent-gold over blue PF or M1-as-independent-blue arrow when P1 red/green; one object silently omitted in full-scene PASS.

**Bevis som KRÄVS senare:** per-object physical owner assignment by scanline and frame; liveness/register table; both frame-visibility and active projectile/orb state (when real ROM is separately authorized).

### S7 — Sword timing, arrow direction and physical collision through obstacles
**Prioritet:** GAMEPLAY; **vidare grind:** N3/N9/N10. **Aktuell evidens:** Design-canon ONLY; no real integrated gameplay ROM.

**Testsyfte:** Freeze damage and timing semantics separately from PF pixels.

**Fryst indata:** [{"world":"forest","frame_window":24,"scenario":"sword telegraph","timing_status":"~0.4 s at nominal NTSC 60 Hz, approximate"},{"world":"night","scenario":"one arrow flight, bounce/no-homing forbidden"}].

**Testhändelser:** (1) knight holds direction at windup start and stops for ~0.4s before sword active; (2) arrow aims at player position at FIRE instant, then never homes; (3) halo penetrates solid, kills arrow and enemy when in range, body/arrow/sword do not penetrate solids.

**Skall redovisas/bestå:** (1) no damage on body contact, windup or recovery; damage only active sword frame; (2) knight recovery ~1s before next cue, windup direction immutable; (3) at most 1 flying arrow and interval from last FIRE: forest ~3s, mountain ~2.5s, dream ~2s, night ~1.5s; (4) player can move/attack during active ~0.5s halo and ~1s invulnerability.

**Negativ kontroll:** TIA PF draw collision latch treated as gameplay truth when halo overlaps wall; aim point taken at windup instead of firing; telegraph invisible 2/3 frames.

**Bevis som KRÄVS senare:** state event log, exact nominal frame conversions flagged as approximate; visual 24-frame sword warning sequence and per-object swept collision tests later.

### S8 — Four world contrast and night readability, not new palette canon
**Prioritet:** VISUAL; **vidare grind:** N3/N8/N10. **Aktuell evidens:** Not aesthetically/physically approved globally (#15 open).

**Testsyfte:** Screen readability for approved sprite, green archer, gold active halo, contrasting solids and strike cue must survive all four environments.

**Fryst indata:** [{"world":"forest","stage_ids":[1,2]},{"world":"mountain","stage_ids":[3,4]},{"world":"dream","stage_ids":[5,6]},{"world":"night","stage_ids":[7,8]}].

**Testhändelser:** (1) same R3-problematic same-Y scene in each world palette candidate; (2) 12 and 24 consecutive 4:3 native original-Stella captures under movement; (3) night lowest expected luminance, include orb and active sword.

**Skall redovisas/bestå:** (1) maintain neutral light gray troll, green archer and gold ring identity; (2) all active hazards readable even at night, no overly disruptive constant flicker; (3) separate candidate diagnostic palette from user's approved final visual art.

**Negativ kontroll:** still screenshot looks acceptable but 20Hz/30Hz movement hides sword cue; archer green rendered using red knight color at wrong Y/scanline.

**Bevis som KRÄVS senare:** source palette references and RGB/visibility metrics, human-view evaluation when requested; negative control video comparing R3 20Hz/30Hz.

### S9 — Full L3 mobility, safe orb growth and one-room future gameplay stress
**Prioritet:** PHYSICS; **vidare grind:** N3/N9/N10. **Aktuell evidens:** COL1 isolated PASS; eight future maps source-only.

**Testsyfte:** Preserve L3 free space and gameplay state while exercising worst renderer; no false claim that eight draft maps are canonical.

**Fryst indata:** [{"arena":"COL1 single synthetic four-solid","source":"N1/N2 frozen ROM"},{"arena":"eight source-only draft maps F01/F02/M03/M04/D05/D06/N07/N08","source":"K0 and source drafts, not production"}].

**Testhändelser:** (1) diagonal slides at both corner negatives, all four solid contact directions; (2) L3 continuous free movement >=90 frames as an existing diagnostic target; (3) blocked growth x12,y64 at L2 and allowed x80,y88 synthetic positions, not official orb spawn; (4) reserve knight spawn after ~2s when one slot opens, only two active at once.

**Skall redovisas/bestå:** (1) 4-neighbor L3 accessible arena and safe orb sites for levels 1->2 and 2->3; (2) no player teleport, clipping, invisible width downgrade or sticky mandatory channels; (3) deaths don't respawn killed enemies/orb in SAME visit, new visit resets and saves persistent level/lives/score; (4) 8 maps only future design proposal; never declare them playable/canonical from K0.

**Negativ kontroll:** K0 660 four-clock endpoint-only false corner shortcuts and 39348/768864 overly sticky swept-step differences; spawn too close to player or orb cannot grow to full L3.

**Bevis som KRÄVS senare:** COL1 original Stella evidence and independent N2 model for diagnostic only; future code per-orb-center growth oracle and continuous movement tests for all real 8 maps.

## 7. Acceptansmatris och STOP

| Kontrolltyp | Vad kan PASS:a efter N3? | Vad får inte PASS:a ännu? |
|---|---|---|
| **N3 kontraktets formalia** | 10 scen-ID S0–S9, spårbara canon-länkar, bevarade negativa kontroller, färg-/registerägare explicit och deterministiska syntetiska indata | Inget påstående om fungerande source-mask eller ny ROM |
| **N4 research PF** | Ett källräknat event-/liveness-schemat som täcker S4,S5+S6 PF/BL konflikter med absolut deadline och riktig mask | Ingen enkel Hugg/delta/3-cykel-store får räknas som färg-PASS utan hela live-registerbanan |
| **N5 research P1** | S1,S2,S3 med tre verkligt separata X/Y, samplingsplan för varje av 12/24 frames, 0.4s windup | Enkelt R3 20Hz same-Y, NUSIZ-kopior eller borttagen green archer får inte bli GO |
| **N6 full resource GO till MICROTEST** | Komplett preliminärt per-rad TIA write-/RAM byte-live-/CPU-timer-/palette schema för alla S0–S9, även unresolved objections öppet märkta | Ingen integrations-ROM får startas direkt från N3 eller enskild source-PASS |
| **N7 fysisk mikro-ROM** | Endast dess uttryckligen avgränsade egna FYSIKALISKA S4/S5 eller S1/S2-kriterier och SHA/frames | Inte full original-TIA engine PASS |
| **N8 integrated scene** | Samma fysisk ROM kör S0–S8 inkl same-Y, COLUPF, HUD/projectile/orb, worst frame timing, rimlig synlighet | Inte full spelbarhet utan logisk gameplay |
| **N9–N10** | Verkligt spelbar L3-arena och efterföljande oberoende Verification | Aldrig automatiskt åtta kanoniska banor eller PAL/extern console PASS |

**STOP/FAIL om** en nödvändig TIA-write passerar sin beamdeadline; krav färg och mask bestäms av samma fysiska pixel men alternativet saknar explicit prioritet; P1-enemy ersätts med en identisk hårdvarukopia; archer försvinner från testet; figurart eller L3-body ändras; R3 hela 30Hz/20Hz flicker presenteras som ny lösning utan verklig skillnad; 128B RIOT/stack överskrids; en bild saknas utan att loggas; eller source/resultat inte kan reproduceras.

**Ingen ny global 60Hz-per-aktor-regel har beslutats.** Eftersom användaren begär låg störande flimmernivå jämför vi objektens 12/24 bildrutor med R3:s 20Hz negativa kontroll, dokumenterar längsta osynliga gap, andel visad svärdsförvarning och människobedömd rörelseläsbarhet innan eventuell visuell kompromiss läggs fram för användaren. **Det är inte legitimt att påstå att en stillbild bevisar en acceptabel attackvarning.**

**Särskild oavgjord fråga:** om samma PF 4-colorclock cell är både guldhalo och sten måste skärmen visa en prioritet (guld ovanpå sten, sten ovanpå guld eller tekniskt bevisad annan komposit). Det faktiska spelobjektets FYSIK blir ändå magi-genom-sten + stone-blocks-body/projectiles. Detta kontrakt VÄLJER INTE ny estetisk prioritet; ska eskaleras om olika aktiva kandidater behöver det.

## 8. Nästa tekniska handoff – INGEN ny ROM-order

**Till RESEARCH II för N4 (source-only):**
1. Extrahera exakt R3 PF mask-data för X80/X84, **källmaskrad 98**, uttryckligen översatt till riktig fysisk rasterrad, samt X56/104 och syntetisk S6. Returnera en CSV rad/event: physical row, beam color clock, PF bitmap request, COLUPF value, instruction opcode, start/end CPU cycle, X/Y/A register live, pagecross, color-owner, pass/fail, mask mismatch och minimal negativ reproduktion.
2. Varje 3-cykel STX/STY COLUPF-förslag måste visa varifrån X/Y-värden kommer och vad som händer med R3:s X=rowdown/Y=PF index. Utvärdera 5-cykel-FAIL-klass explicit, inte glömma.
3. Ingen allmän 2-line/3-stream-konklusion från dokumenterad historisk kernel. Returnera EN komplett minimum-schemakandidat ELLER ett tydligt NEGATIVT källbevis; metadata/hashes.

**Till RESEARCH II för N5 (source-only, kan gå parallellt):**
1. På S1,S2,S3 jämför GRP1/RESP1/HMOVE/NUSIZ/VDEL-scheman med fritt permuterade X, 3 olika originalfiendebitmappar och green archer på samma Y; 12/24 frame visible/weapon states.
2. Separera Venetian för **P1 fiender** från redan misslyckad naiv Venetian för **PF ring och scenery**. Valfri 1/2/3-line-leveladaptation får inte stjäla P0 U1-LEG1 original source-rader.
3. Returnera full owner-/deadline-/mask- och 128B-RAM-kostnad i stället för bara screenshots; inga nya ROMs, inget verktygs-Kernel-PASS utan verklig fysisk Stella.

**N3 formellt slut:** scenkatalog+resursägarbok är godkända av MAIN III **endast som testkontrakt/source-only research input**. N4 och N5 är nu **förberedda**, inte implementerade. P01-COL1 PR #27 fortsatt draft; R3 full renderer NO-GO; PF #25 och oberoende #1/#15/#19/#23/#24 öppna. ROM DEVELOPMENT/GRAPHICS/VERIFICATION får ingen ny arbetsorder genom denna dokumentation.

## 9. Källspårning
- Primär design: [beslut 01–60 och senare uttryckliga user updates](DESIGN_DECISIONS_01-60_2026-11-16.md), [visuell riktning](SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [U1-LEG1 källbitmappar](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json).
- Original hardware: [Stella Programmer's Guide (1979)](https://www.atariage.com/2600/programming/2600_101/docs/stella.html), especially 76 cycles/scanline, P0+M0/P1+M1/PF+BL/BK color owners and PF 4-clock cells.
- [R3 complete real-DASM/Stella negative report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md) and [R3 source](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm).
- [PF-REP1C resource/priority research](MAIN_II_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_SOURCE_AUDIT_2026-11-17.md), [RESEARCH II current report](https://drive.google.com/file/d/1MtA0edh0hCOa-OoIBDNITml7k18FYvJD/view).
- [COL1 draft PR #27](https://github.com/Odourman/the-skraun/pull/27), [N2 6507/RAM/stack calculated audit](MAIN_III_P01_COL1_N2_WORST_CASE_CPU_RIOT_STACK_AUDIT_2026-11-17.md), [N3 ten-step parent plan](MAIN_III_DEEP_ARCHITECTURE_REVIEW_REVISED_TEN_GATE_PLAN_2026-11-17.md).
