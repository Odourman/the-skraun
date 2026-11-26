# The Skraun · ROM DEVELOPMENT VI

**2026-11-26 · PLAYABLE_CHECKPOINT · DEVELOPER_OBSERVED**

ROM för Stella och avsedd RetroN 77-kompatibilitet. Standard F6, 16 384 byte, NTSC, 262 rasterrader i de uppmätta körningarna. Spela med joysticken och håll FIRE för upprepade haloattacker.

- ROM SHA-256 `3d2e57cbe873dcabf44a325a75cf7859d8959da86823cb51c2b9e42cc7e12c94`
- Spelbas [PR #63](https://github.com/Odourman/the-skraun/pull/63), `e013e26b902f231e91dcfbb72153682b5634fa1b`
- Arbetsorder [FULLGAME-1](https://github.com/Odourman/the-skraun/issues/50)
- [Kodändringar på ROM DEVELOPMENT VI-grenen](https://github.com/Odourman/the-skraun/compare/experiment/fullgame1-romdev-v-health3-20261126...experiment/fullgame1-romdev-vi-stability-20261126)

## Ändring

HUD-rutinen i bank 1 delar varje packad BCD-byte en gång och slår upp de färdiga PF1- och PF2-bitarna rad för rad. Tabellen kontrollerades uttömmande mot den gamla fonten för alla 100 sifferpar på vardera av fem rader för båda registren. Den tidigare HUD-temporären på `$95` behövs inte längre. DASM producerade identiska byte i bank 0, 2 och 3. PF1-motiven har SHA-256 `4c52651d7eca55e8e5c5158d33c90bec6bbd4f85e1732e65cf94321cd2b5334d`.

PR #63:s `stage2_L3` är ett L1-fall på bana 1 med aktiv halo och pil. Stella visar 264 rader vid det arkiverade slutprovet samt en 310-radersruta i det omgivande provet. Registerspår placerar fördröjningen före VBLANK-avslag. Kandidaten kör om exakt samma knappsekvens till 262 rader. Den ursprungliga mätpunkten hade spelets interna bildräknare `$79`, medan samma emulatorkommando med stabil raster når `$7A`. Ett kompletterande prov stannar på `$79` och matchar hela PR #63:s RIOT-dump utom den slopade HUD-temporären `$95`. Även denna bildruta har 262 rader.

## Stella 6.7.1

| Prov | Resultat |
| --- | --- |
| 17 arkiverade joysticksekvenser | 17/17 slutvärden på 262 rader. Samtliga 17 speltillstånd matchar den frysta basens prov, inklusive jämförelsen vid motsvarande interna bildräknare i problemfallet. |
| Problemsekvensen `stage2_L3` | 634 loggade bildrutor i följd med 262 rader efter initiering. |
| Hela pendelloopen | 4 401 loggade bildrutor med 262 rader. Joystickkommandon, åtta banor, båda vändlägena, slut på bana 1, L3, sju liv och 8 400 poäng. |
| Riktade bildrutor | 120 konsekutiva naturliga bildrutor och 24 med en syntetisk L3-fixtur med halo, pil och flera fiender. Alla 144 hade 262 rader. |
| Orben i skog | Stella-PNG bekräftar två av/två på i samtliga tre prov, normalt, halo, och halo med pil. Orben är grön normalt och guld under aktiv halo. |

Spårsummorna kommer från VSYNC-skrivningar, förankrade mot `_scanEnd` vid slutpunkter och punktvisa bildsteg. Uppstartens ofullständiga intervall är separat. Speltilstånd lästes ur RIOT-dumpar. Arkivet innehåller de faktiska Stella-sessionerna, indata och inspelade PNG-filer. Timingvinsten ger den befintliga renderern marginal att visa fler valfria halosegment i vissa bildrutor.
 Videon visar 600 konsekutiva Stella-bildrutor från den sparade joysticksekvensen och är utan ljud.

## Kvar före releasekandidat

Halon behöver fortfarande en mer sammanhängande kontur och fiendernas varnings- och attackläsbarhet behöver mätas vid överlappning. Fullständiga per-rad/deadline- och stackprov, fler kollisions- och spelscenarier, ljudgranskning och fysisk Atari 2600/RetroN 77 återstår.

## Bygg och spela upp proven

Från arkivets rot, med Linux x86-64, Python 3 och medföljande DASM och Stella:

```sh
sha256sum -c SHA256SUMS.txt
chmod +x base/05_BUILD_TOOLS/dasm base/05_BUILD_TOOLS/stella
export PATH="$PWD/base/05_BUILD_TOOLS:$PATH"
python candidate/experiments/game/build.py
```

För att köra de arkiverade joysticksekvenserna från kommandoraden behöver SDL2:s offscreen-drivrutin samt en C-kompilator. Hjälpprogrammet skickar text till Stellas debugger. Spel- och rastervärden kommer från Stella.

```sh
cc -Wall -Wextra -shared -fPIC raster/sdl_input.c -o raster/sdl_input.so -ldl
python raster/run_regression.py reprise \
  "$PWD/candidate/build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin"
```
