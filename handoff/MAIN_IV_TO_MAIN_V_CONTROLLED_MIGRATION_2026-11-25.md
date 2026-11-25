# THE SKRAUN – MAIN IV till MAIN V: kontrollerad migration, 2026-11-25



**Rollen MAIN IV överlämnar till en ny MAIN V-ledningschatt.** Detta är en dokumentations- och källöverlämning, **inte** en implementeringsorder, ny canon, godkänd releasekandidat, oberoende verifiering eller merge.



## Ett komplett, bytekontrollerat migrationspaket



- **Google Drive, projektets huvudmapp:** https://drive.google.com/drive/folders/1tSipzf7bucrqFOwHBEH61fKvyl0z7D1z

- **Ny komplett MAIN IV → MAIN V ZIP:** https://drive.google.com/file/d/14MNQon6nm4-k0YVj4KKaIfoGymKQpOVj/view

- Namn: THE_SKRAUN_MAIN_IV_TILL_MAIN_V_KOMPLETT_2026-11-25.zip; **11,882,318 bytes**, **40 filer**, ZIP CRC PASS och **39/39 SHA-256-manifestposter PASS**.

- **Exakt SHA-256 ZIP:** `08aa3297daf53ba30a107f26efa5903c8595f570ec36a94177e717d5e32daff0`.

- [Ny MAIN V-startprompt, exakt text i GitHub](MAIN_IV_TO_MAIN_V_EXACT_STARTPROMPT_2026-11-25.md); samma text separat i [Drive](https://drive.google.com/file/d/1KaCDFhs3N2gBwZLXhcgtft_bv4SethuK/view).

- ZIP-filerna `00_START_HAR.md` och `01_EXAKT_STARTPROMPT_MAIN_V.md` är för nya MAIN. De sex övriga MAIN-dokumenten beskriver live-status, källordning, arbetsgränser och nästa tekniska prioritet.

- Under `10_ROMDEV_IV_MIGRATIONSARKIV/` finns **samtliga 32 ursprungliga filer, oförändrade**, från ROM DEVELOPMENT IV:s tidigare migreringspaket på Drive https://drive.google.com/file/d/1oAPDlnYL5TF9eE_xZIK3b1sStCNNSRrW/view (12,279,203 bytes, SHA256 `02e8f4b0dee3b941a4c314199c0ce543eeaee6d2957245d0534a936759a8acde`). Dessa omfattar verkliga F6-banker, två frysta ROM:ar, samlade Stella-debuggerloggar, GitHub Actions artefakt, Project Sources 00-04 och tidigare tekniska 491-filsleverans.



## LIVE GitHub-proveniens vid migrationen



- `main`: `46d31504cccc5d17b521f7b9f01b7aded003de1a` (FULLGAME-1 ej mergad).

- [Issue #50 FULLGAME-1](https://github.com/Odourman/the-skraun/issues/50): OPEN. Helspelstillstånd inom max **16 KiB originalkompatibel F6**, motiverad F6SC möjligt. Inte automatisk main-merge, release eller separat Verification.

- [PR #51](https://github.com/Odourman/the-skraun/pull/51): OPEN/DRAFT, HEAD `8ab2840c99785b499c3499b89a23246fca026fa9`, tidigare best playable 16KiB ROM SHA256 `146c6541c673b10d2dc44304627b67ce9a5e3788e39d087d73251cfd3f50767c`.

- [PR #52](https://github.com/Odourman/the-skraun/pull/52): OPEN/DRAFT, HEAD `7528bb52105240642fd5e1d1edce18472b8d0ee5`, **NEGATIV** sparse-PF-försök, `arrow_first=263` i riktig Stella. Integrera inte utan ny korrigering.

- [PR #53](https://github.com/Odourman/the-skraun/pull/53): OPEN/DRAFT, HEAD `7a2f34e267a46bfcac909a5d96d6589f98f8ec67`; 16,384-byte adaptiv F6-ROM SHA256 `d2a0a1b57ac9c78b2af14f77800f7c1ecf99aaa43f60e8c4216974f18aed2a0e`; verklig [Actions #45530532678](https://github.com/Odourman/the-skraun/actions/runs/45530532678) SUCCESS, 17/17 **utvalda slutbildrutor** `_scanEnd=262`. Detta är sista frysta avgränsade developer-PASS, inte tre samtidiga fulla sprites eller releasegodkännande.

- **[PR #54 – NYAST](https://github.com/Odourman/the-skraun/pull/54)**: OPEN/DRAFT, branch `experiment/fullgame1-arrow-halo-romdev4-20261125`, HEAD `80acf144c7bd795bf6792ca478d28c542bbd2627`, 16KiB pil/halokod SHA256 `a9189404275d4c3e5f04c246033290384c64d0ffcc127ff73229522d9a81e8a3`. Senaste verkliga [DASM/Stella Actions #45602662669](https://github.com/Odourman/the-skraun/actions/runs/45602662669) **FAIL**: DASM/SHA SUCCESS, men `stage2_L3=263` i stället för 262; övriga 16 utvalda frames 262. Generell grön CI ersätter inte detta. Det finns ännu inget bevis för tydlig sammanhängande 360°-halo på alla tre levels.

- Tidigare lokal halo/pil-ROM `564ac02c7a748dfe7c77c96e4b1f22a9267876959470e4fa781cb8c0a8a94fa9` är **en annan binär** och dess egna korta positiva tester får aldrig användas som PASS för PR54:s `a918...`.

- PR54 senaste Actions har 120 sparade debuggerstates men **0/120 individuellt observerade** `_scanEnd` i den körningen. All-path 76-cykler/beam, RIOT stack high-water, full spelprogression och originalkonsol är inte verifierade.



## Bindande källor och roller



- Userbeslut > [beslutslogg 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [visuell riktning](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [fryst U1-LEG1-mask](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json) och giltig FULLGAME-1-överlämning > verklig GitHub-/DASM-/Stella-källa > MAIN-review > research/daterade Project Sources. Välj inte automatiskt nyast lättåtkomliga källa om en högre auktoritet motsäger den.

- Upprätt ljusgrå U1-LEG1, A/B mask på tre levels; 8 joystickriktningar och smidig L3, 2 riddare + världskamouflerad Ranger, tydlig svärdsvarning, verklig pil, X/Y-följande 360°-halo som passerar hinder, orb, 8 banor, HUD/ljud/poäng/liv och pendelprogression. Inga osynliga skador eller tysta kompromisser.

- MAIN V leder, granskar och utfärdar eventuella uppdrag. **ROM DEVELOPMENT IV** implementerar/testar redan auktoriserad pil-/halouppgift. RESEARCH rådgivande, GRAPHICS efter uppdrag, VERIFICATION separat efter uttrycklig order.

- Inga nya ROM-commits, ingen main-merge, ingen public release och ingen independent Verification är påbörjade av denna migration.



## Första tekniskt meningsfulla steg för MAIN V



Kontrollera PR #54:s senaste Actions och felscenen `stage2_L3=263`, jämför mot PR #53:s funktionella fallback och begär av ROM DEVELOPMENT IV en smal korrigering inom redan auktoriserat pil/halo-scope. Kräv samma frysta bygg-SHA i alla tester; 17 Stella-scener, 120 **verkligt individuellt mätta** frames, värsta L3 med 2 riddare+Ranger+M1+orb+aktiv halo+HUD, verkliga TIA-colorclock-deadlines och RAM/stackmätning, samt verkliga bilder av korrekt radiell halo och synlig pil. Låt inte MAIN själv ta över assemblerimplementationen och starta inga andra etapper bara p.g.a. migration.



**Beslut:** `MAIN_IV_TO_MAIN_V_HANDOFF_READY / LATEST_PR54_STAGE2_L3_FAIL / PR53_BOUNDED_BASELINE_PRESERVED / FULLGAME1_RELEASE_NOT_READY`.