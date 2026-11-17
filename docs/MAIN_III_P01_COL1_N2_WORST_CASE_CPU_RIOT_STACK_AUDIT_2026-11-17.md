# THE SKRAUN – MAIN III N2: konservativ tids-, RAM- och stackgranskning

Datum: 2026-11-17. Klassning: MAIN:s oberoende käll- och artefaktgranskning, EJ oberoende Verification eller uppmätt Stella-instruktionstrace.

## Reproducerbara original

- Originalgren: `experiment/p01-col1-single-arena-collision-20261117`, fryst PR #27 commit `90f89441b41a2e82408581b81d3743b1423e5cdb`.
- Actual original 4096-byte ROM: SHA-256 `f36217f9ae96a1e927795ca639b9d6b6cca68ad3e8e4f296afadcdb52d6a6ad2`.
- `.asm` exakt GitHub blob `13deb852340d70ae7aca80a1a1f7e98579ccfeb9` för fryst branch.
- 35-filars original GitHub Actions/Drive-evidens-ZIP: SHA256 `a409c36aaaa651096cd686ad93238b50d47d276fe34ad7d7931f6064089b9487`. Hämtad på nytt från Google Drive, 35/35 CRC PASS.
- Senaste 19 Stella-skärmbilder/132 hjälpfiler i separat 138-file ZIP: 678660 bytes, SHA256 `e49d5187a977c9c580ff46c16d50089424c79cebe5500458a06ac221d96331f4`; samtliga ZIP CRC PASS. Kontroll har gjorts i tidigare MAIN N1; 19 images har visuella bboxes med förväntat rörelsemönster. Detta är verkliga Stella GUI-skärmbilder från ROM DEVELOPMENTs original Action, inte nya lokala Stella-körningar.

## Utförda nya analyser

1. `candidate_full_byte_audit.py` på **kompilerad 6502-ROM via utvecklarens existerande CPU-subsetinterpreter**: exakt 3 × 256 × 256 = **196608** möjliga TryX/TryY för level1–3, inklusive 0x00/0xFF som gränsfall. Högsta beräknade rutinlängd inklusive RTS: L1 **277** cykler vid x125 y162; L2 **261** vid x121 y64; L3 **261** vid x113 y70. Detta är en modell med direkt kodexekvering, **inte mätt verklig 6507/Stella**.
2. `frame_profile.py`: **798** kompilatormodell-bildrutefall, tre levels, joystick åtta riktningar, faser 0–2, SELECT och kombinationer, extrempositioner och hörn. Modellen höll **262×76 = 19912** cykler/frame i samtliga fall. Upp till fyra `CandidateValid`-anrop förekommer. Högsta observerade arbete från TIM64T till första `BlankWait` var **1512** cykler, annan exekverad icke-kollisionskod upp till 633; högsta beräknade synliga linjearbete efter WSYNC **60** cykler och max **4** 6502 retur-stackbytes. **Detta är sampling, ej ett worst-case bevis.**
3. `static_cfg_bound_pure.py`: en **oberoende opkodsbaserad konservativ kontrollflödesöverskattning på exakta maskinkodsbytes**, inte på developer-emulatorns val av testkoordinater. Samtliga villkorliga grenar ges **4 cykler** även vid ej-tagen väg, alla ABS,X/(indirect),Y sidkorsningar ges värsta cykelkostnad, båda `STA WSYNC` tilldelas upp till **76 extra väntcykler**, `P0Loop` tilldelas högst **18** upprepningar för godtyckligt unsigned 8-bit RenderX och `RectLoop` högst **4** iterationer från RectIndex 0,4,8,12, varje iteration konservativt 77 instruktionscykler plus return8. Detta ger 

   - `CandidateValid` **<=382 cykler**, inklusive RTS, oberoende av CPU-subsetinterpreter.
   - `DetectDiagonal` <=47; `MoveX` inkl 1 Candidate <=464; `MoveY` inkl 2 Candidates <=868; `DebugLevel` inkl 1 Candidate <=460; `UpdateScale` <=57; `UpdateGait` <=63; `PositionP0` inkl WSYNC max <=211.
   - **Komplett högsta VBLANK-kodtid** från *omedelbart efter* den riktiga `STA TIM64T` vid `$F043` till inträde i `BlankWait` vid `$F092`: **<=2372 CPU-cykler**.
   - Timer laddas med `#43` i `TIM64T` med 64-cykel-intervall: **43 × 64 = 2752 cykler**. **Konservativ beräknad säkerhetsmarginal minst 380 cykler** för *denna isolerade P0-only COL1-ROM* fram till normala väntloopen.
   - Detta är en **övergräns med avsiktligt tillåtna omöjliga branch-kombinationer**, inte en faktisk realtidsprofil. Den hanterar kodens fyra möjliga collision calls i samma teoretiska värstafall och bygger inte på antagandet att bara tre förekommer.
4. **Synlig scanline**: faktiska kodrader `$F0A5..$F0CF` skriver första `GRP0` direkt efter WSYNC, väljer PF-data och förladdar nästa P0-rad. ABS,X `PFCode` vid `$F2F8` kan ha pagecross +1, men `PF0Choices/PF1Choices` (index 0..2), `MapSmall/Medium/Large` och `Gfx`-tabellerna kan inte pagecross vid giltiga index. Värsta kontrollflöde i faktisk listning **60 CPU-cykler efter WSYNC + 3 WSYNC-cykler = 63/76**; **minst 13 cyklers teoretisk slack** i just COL1-diagnostikens P0/PF-arbetsrader. Verkliga Stella-bilder kontrollerar pixelresultatet och känt `_scanEnd #261` (0-index); detta är **inte uppmätt fysisk instruktionslogg**.
5. **RIOT och stack**: RAM-variablerna `$80..$9B` inkl är **28 bytes**. Källans djupaste JSR-kedja är Frame -> MoveX/MoveY/DebugLevel -> CandidateValid, alltså två return-adresser, **4 hardware stack bytes** i speglade `$1FC..$1FF`/RIOT `$FC..$FF`, utan konflikt med variabler upp till `$9B`; då återstår **96/128 byte** utanför reserverad variabel-/returstack i detta avgränsade test. Inga extra faktiska P1/halo/pil/orb/HUD/AI-variabler ingår.

## Beslut och begränsningar

**N2 beräknad worst-case developer gate: PASS för exakt isolerad COL1-källa och ROM**. Det finns ett statiskt beräknat worst-path marginbevis med avsiktlig överskattning, kompletterat av 798 scenarioframe i 6502-CPU-modellen och tidigare 19 genuina Stella GUI-cases. Den ursprungliga arbetsordern medger att cykler **mäts ELLER beräknas med tydlig beteckning**.

**FORTFARANDE EJ VISAT:** genuin Stella-maskinläsbar worst-path CPU-instruktionstrace och verkligt 6507-stacked runtime-profil, manuell riktig Atari-konsoljoystick/SELECT, real kontinuerlig 262-raders under alla möjliga framtida AI-vägar, tre fienders same-Y, tvåfärgad halo+scene, åtta kanoniska banor eller oberoende Verification. Arkivets Stella `saveSes` 0B ger ingen sådan instruktionsprofil; detta ska inte felrapporteras som ett spelkodsfel eller som att alla runtime-bevis saknas.

**PROJEKTSTATUS:** #24 hålls tills MAIN uttryckligen tar ett acceptans/Verification-beslut; PR #27 fortsatt DRAFT/UNMERGED. #1 äldre P01-verifiering, #15 visuell, #19 annan ART1-bugg, #23 åtta banor, #25 PF-research öppna. Ingen ROM/gameplay/grafik/mapper/renderer-ändring har gjorts av MAIN. En kontroll av verktygsversion, verklig Stella/per-instruction spårning och skarp hardwareprofil är relevant för **separat** Verification, inte automatiskt krav på att stoppa all research.

## Så reproduceras analyserna

Originalfilerna ligger i detta ZIP under `build/col1/`, `experiments/` och `tests/`. Python 3 utan extra tredjepartsbibliotek. Kör från paketets rot:

```sh
python candidate_full_byte_audit.py
python frame_profile.py
python static_cfg_bound_pure.py
```

Original ROM/hash och skripten kontrolleras med manifestet `SHA256SUMS.txt`. Detta är revisionsunderlag för MAIN/Verification, inte en ny spel-ROM.
