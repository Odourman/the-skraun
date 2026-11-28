# HEALTH IV → MAIN VI – final recovery
2026-11-28. HEALTH_OBSERVED / PASS_BOUNDED, not independent verification. EXPERIMENT_ONLY. No merge or product integration.

Protected PR78/B2 code 0fce7ccd6ab6d47703bf7233b7a7c928eb338704; Stack B code 4048807118bdc7abb1b1558efaa3a53bfbc7a295. Final code 87bdd835803d4e5aeab177a32ae08165bfbfbfaf, gateway checkpoint c423058e81405b9741f99489010b25ecca6d36dc. Selected final 16384-byte standard F6 NTSC ROM SHA-256 9ebb8f9ab78484badd72913585186108e93e35af4111b0a0931e01dd9ae429e2. Five code blob hashes verified against local builds.

- Alternate bank0/1 illegal startup opcode observed in native Stella, not a hardware crash. Compensated gateway passed all four selected startup banks; bank2/3 normal reset vectors unchanged. Console RESET tested title, active halo, directed pause, gameover.
- Late overscan INTIM underflow injection (scanline257, TIM1T 0/1/2/3) gateway raster 265/265/268/262 → final 262/262/262/262. Earlier bank2 F027 TIM1T=7 injection remains 250 lines. VBLANK race not modified. No general arbitrary timer corruption recovery claim.
- 7200/7200 framebuffer and audio frame hashes, 7544552 PCM int16 values, all 128 RAM bytes per frame identical to Stack B; B2 RAM differs only residual stack F3–F9. 98251/98251 selected native trap events match, 7199/7199 natural 262 intervals. Eight arena fixtures 443 normal intervals each, prior264 18/18, combined 28/28 twice. Combat396/396, orb219/219 +37 skip, ghost462/462. Fresh directed orb captures match; historical same-ROM HUD variation remains. No full bus or all-input proof.
- Modeled stack 14→12 bytes vs B2, all-vector model final 15798 states with no stopped branches. Address-specific native stack traps lowest reported poststartup 01F3→01F5, SP F2→F4; multiwrite caveat. No new persistent RAM or net CPU/ROM savings claimed. Ranger CPU trial rejected for 7 PCM frame mismatches. Gopher NOT_RUN DNS connection refused. No physical hardware/PAL. Full liveness/beam audit incomplete.

## Published files
All five were uploaded and raw downloaded; local SHA-256 matched, ZIP CRC and manifest checked again. Full report contains exact tests and limitations; RESTART.md in ZIP. Prior evidence preserved.
- [ROM](https://drive.google.com/file/d/14fICLg6Twh6NTNVTDgVjb6mFc-ojikpI/view)
- [Source ZIP](https://drive.google.com/file/d/1mqHqZ_XKD6xUfhvv1b1eheteV0pynjYl/view) SHA 0a558c195384197a946f5e9e5efb327e8270f66d45e05a1cf2e5746e45a506a2 (30 manifest entries)
- [Evidence ZIP](https://drive.google.com/file/d/1J6SGvDD3G4ApPUjZAJ-Vk46x2bJARYgn/view) SHA c44bae141a72e7e2d85c3bd98e22e978d65648f82a467359f109abc2bf8b5c4f (2499 entries)
- [Gameplay MP4](https://drive.google.com/file/d/1UXUWToYnA1iGiQOL4nrylfX2Dx0vhH4C/view) SHA 7a344e007108024c514227b3e340e01e06b3f5e8243dd5e4df95ee0935647265
- [Full MAIN_HANDOFF.md](https://drive.google.com/file/d/1OFHyOHPlB-YIQe0LuCpszQGXG-v2Y9Y0/view) SHA 7827beaf55d428a21e290d354e58f467406e40960f40c568349ab9f8f76ded3c

STOP. MAIN decides separate integration; no new scope started.