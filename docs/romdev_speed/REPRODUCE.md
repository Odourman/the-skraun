# Reproducera D (Linux x86-64)
Kör från paketets rot. Python3/numpy/Pillow/ffmpeg, gcc, native DASM och Stella 6.7.1 samt SDL krävs. Binärverktygen är medföljande tidigare arkiverade byggverktyg; använd systeminstallation om bibliotek saknas. Stella7 Libretro-kärna och dess licens i raster/retro.
```sh
export PATH="$PWD/base/05_BUILD_TOOLS:$PATH"
python experiments/fullgame1_arrow_halo_20261125/build.py
sha256sum build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin
cc -shared -fPIC raster/sdl_production.c -o raster/sdl_production.so -ldl
python run_ranger.py speedD.bin D 0 1 2 3 4
python trace_ranger_all.py speedD.bin 'D-*'
python raster/seamless_fixtures.py speedD.bin evidence/edgeD
python raster/seamless_pixels_D.py speedD.bin evidence/pixelsD
python raster/seamless_pixels_return_D.py speedD.bin evidence/returnPixelsD
python raster/speed_measure.py speedD.bin evidence/speedD
python raster/seamless_extra_D.py speedD.bin evidence/extraD
python raster/ranger_los_fixtures.py speedD.bin evidence/losD
python raster/ranger_fire_hud.py
python raster/retro_capture.py raster/retro/stella_libretro.so speedD.bin evidence/D-tactical-0/route.script 9000 evidence/videoD
for i in 0 1 2 3; do python raster/retro_capture_edge.py raster/retro/stella_libretro.so speedD.bin evidence/video_edge$i/route.script 420 evidence/video_edge$i evidence/video_edge$i/fixture.json; done
```
Kant-/hastighets-/LOS-fixturer initierar RIOT uttryckligen och kör sedan riktig emulator. Pixelproven fryser ett valt initialtillstånd inför enskilda bildrutor; de är inte naturlig gameplay. Spelserierna styr bara joystick via RAM-läsande strategi; inga RAM-injektioner. Native replay på samma input, separat emulator, inte garanti för identiskt varje frame. Versionfältet PR69_C5 i ärvda native result.json är en historisk fast sträng i testskriptet, inte ROM-identitet; identifiera via katalog, ROM-hash och logg. D native PC-baserad skadeorsak från aktuella DASM-listningar. Absoluta paths i bevarade loggar kommer från körmiljön; nya skript skapar aktuella paths.
