# Reproducera C7 (Linux x86_64)
Kör från paketets rot. Installera Python 3, numpy, Pillow och ffmpeg; använd de medföljande DASM/Stella-verktygen om miljön stöder deras bibliotek, annars motsvarande native DASM och Stella 6.7.1. Stella 7 Libretro-kärnan och dess licens finns i raster/retro. Kör:
```
export PATH="$PWD/base/05_BUILD_TOOLS:$PATH"
python experiments/fullgame1_arrow_halo_20261125/build.py
sha256sum build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin
cc -Wall -Wextra -shared -fPIC raster/sdl_production.c -o raster/sdl_production.so -ldl
python run_ranger.py build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin C7 0 1 2 3 4
python trace_ranger_all.py build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin 'C7-*'
python raster/ranger_final_fixtures.py build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin evidence/C7_fixtures
python raster/ranger_los_fixtures.py build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin evidence/C7_LOS
python raster/ranger_extra_fixtures.py build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin evidence/C7_extra
python raster/hard_checks.py build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin evidence/C7_legacy experiments/fullgame1_arrow_halo_20261125
python raster/ranger_fire_hud.py
python raster/retro_capture.py raster/retro/stella_libretro.so build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin evidence/C7-tactical-0/route.script 9000 evidence/VIDEO/C7_gameplay
```
Native replay använder SDL debugger input injection, inte modifierad ROM. Alla riktade RAM-initfixturer är uttryckligt syntetiska initialtillstånd. Den gamla `arrow_release` har 49 octagonavstånd, C7:s max 44; därför förväntad ändring, inte samma gammalt PASS. Native RESET-kommandot ej stöds, verklig libretro RESET används. `MEASUREMENTS.json` redovisar faktiska körningar, inte garanti för samtliga möjliga tillstånd. Bevisens absoluta sökvägar kan behöva ersättas vid flytt; skripten genererar egna aktuella sökvägar.
