# Reproduktion
Från paketrot (Linux x86_64; Python 3, NumPy, Pillow, ffmpeg, SDL2; verklig DASM/Stella ingår). `chmod +x pr76/base/{dasm,stella}`. `cd refit; PATH="$PWD/../pr76/base:$PATH" python experiments/fullgame1_arrow_halo_20261125/build.py; cd ..` Bygget har låst EXPECTED. Frysta byggträd i pr76/assembler och pr77; originalcheckpoint i pr77/build. Refit-generator tools/refit_signed_bounds.py är endast reproduktion av källtransform från geometry-fångster, inte nödvändig för bygget. Kör på kopia för att inte ändra den frysta källan.
```
core=pr76/core/stella_libretro.so
rom=refit/build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin
b=refit/build/arrow_halo_romdev4
python tools/combat_orb_fixtures.py "$core" "$rom" candidate evidence/recheck-contact
python tools/actual_pixel_overlap.py "$core" "$rom" candidate evidence/recheck-pixels
python tools/final_extra_fixtures.py "$core" "$rom" candidate evidence/recheck-extra
for t in ghost_cases aura_p1_slots lifecycle; do python tools/$t.py "$core" "$rom" candidate evidence/recheck-$t; done
python tools/aura_live_capture.py "$core" "$rom" naive 0 7200 evidence/recheck-gameplay aura
python tools/video_audit.py evidence/recheck-gameplay/gameplay.mp4 evidence/recheck-gameplay/riot.bin evidence/recheck-audit --version R2
cc -shared -fPIC tools/sdl_input.c -o evidence/input.so -ldl
python tools/aura_native.py pr76/base/stella evidence/input.so "$b" evidence/refit-naive/route.script evidence/recheck-native --mode natural
python tools/aura_native.py pr76/base/stella evidence/input.so "$b" pr76/fixtures/previous-264.script evidence/recheck-264
python tools/aura_native.py pr76/base/stella evidence/input.so "$b" evidence/combined-orb-safe.script evidence/recheck-combined
```
Fixturer använder initierad RIOT; speluppdatering/pixlar/ljud verklig emulator. Alla native-sessioner har rå stella.log och debugger.txt, använd WTrap[00] vid 3/f05b, frame≥2, scanline+3. Stack trap[01], SP i loggen, filtrera startup. Native stella.log innehåller verkliga traps, debugger.txt är kommandosession. Ursprungliga run_*.sh arkiverade med gamla absoluta sökvägar; använd kommandona ovan. Klipp: `python tools/final_clips.py` genererar fixturer, därefter `python tools/capture.py "$core" "$rom" evidence/clips/edge.script 84 evidence/recheck-edge evidence/clips/edge.json` (orb analogt). `sha256sum -c SHA256SUMS.txt` i paketrot verifierar exakt levererade bytes. Använd kopior för omprov.
