# Reproduktion
Linux x86-64, Python3 + numpy/Pillow, FFmpeg, CC. Kör från paketrot. Källkoden är assembler/experiments/fullgame1_arrow_halo_20261125. `sha256sum -c SHA256SUMS.txt` verifierar arkivfiler före ombyggnad. Bygg i ny kopia av paketet.
```bash
export PATH="$PWD/base:$PATH"
python3 assembler/experiments/fullgame1_arrow_halo_20261125/build.py
b=assembler/build/arrow_halo_romdev4
rom="$b/THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin"
cmp "$rom" THE_SKRAUN_AURA_REFINEMENT_F6_NTSC.bin
mkdir -p rerun
cc -shared -fPIC -O2 tools/sdl_input.c -o rerun/input.so -ldl
for script in aura_combat_cases aura_edges aura_hit_matrix aura_p1_slots aura_motion aura_comparison ghost_cases enemy_visual lifecycle; do
 python3 tools/$script.py core/stella_libretro.so "$rom" candidate rerun/$script
done
python3 tools/aura_live_capture.py core/stella_libretro.so "$rom" tactical 0 7200 rerun/live aura
python3 tools/aura_live_capture.py core/stella_libretro.so "$rom" naive 0 7200 rerun/naive aura
python3 tools/aura_native.py base/stella rerun/input.so "$b" evidence/R2/live/route.script rerun/native-live --mode natural
python3 tools/aura_native.py base/stella rerun/input.so "$b" evidence/R2/naive/route.script rerun/native-naive --mode natural
python3 tools/aura_tia.py base/stella rerun/input.so "$b" fixtures/combined.script rerun/tia --mode tia
python3 tools/aura_native.py base/stella rerun/input.so "$b" fixtures/stack.script rerun/stack --mode stack
mkdir -p analysis reference
cp "$b"/bank?.bin reference/
python3 tools/stack_static.py
```
Kör arena1..8.script `--mode beam`, combined/previous-264/riot-race `--mode short`, ghost med ghost_native.py (se källans CLI). Reproduktion av visuell audit: läs CLI i tools/video_audit.py; rå RIOT och video från samma inspelning. Fixturer har explicit RAM-injektion; naturlig policy läser enbart RIOT. De gamla videorna och B3/PR72/PR73 BIN-filerna i baseline är jämförelser, ej slut-ROM. `analysis/final_metrics.py` är den bevarade lokala analysscriptversionen med ursprungliga arbetsvägar; justera till paketets rot om den körs i ny miljö. Native logs inkluderar start/stop; räkning använder fulla synkroniserade frames efter startup, PC 3/f05b och scanline+3. Native CI-artifact är oförändrad kopia från Actions. `MAIN_HANDOFF.md` beskriver begränsningar.
