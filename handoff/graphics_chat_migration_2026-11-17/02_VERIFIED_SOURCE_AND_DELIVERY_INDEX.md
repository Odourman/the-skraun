# THE SKRAUN – GRAPHICS: källa och leveransregister för ny chatt

**Snapshot 2026-11-17.** Kontrollera alltid på nytt; länkar är källpekare, inte självständig godkännandeauktoritet.

## A. Bindande huvudkällor (MAIN + användare)

1. [Aktuell visuell riktning – senare U1-LEG1- och L1/L2/L3-beslut inskrivna](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md). Läs **HELA**, särskilt sista avsnitten om användargodkännande, riktningsomvändning och identisk grafikkälla på tre levels.
2. [Designbeslut 01–60 med senare korrektionsnotering](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md). Skilj ursprungligt 'fyrfotat'-ordval från senare överordnad direkt användarkorrigering att spritekroppen står upprätt.
3. [Öppen visuell gate #15 + MAIN II:s senaste kommentarer](https://github.com/Odourman/the-skraun/issues/15). Här dokumenteras explicit L1-acceptans, omvända display-R/L-etiketter och identisk source art för alla tre levels.
4. [Privat originalteckning, Drive endast](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view). Aldrig inklistrad eller ompublicerad i offentlig handoff.
5. [GRAPHICS U1-LEG1 bindande tidigare arbetsorder](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_GRAPHICS_U1_LEG1_CAPRINE_GAIT_SOURCE_ONLY_AUTHORIZED_2026-11-16.md) – historiskt avslutad order, INTE ny beställning.

## B. Senaste faktiska källbitmap och evidens

- **Gällande fryst U1-LEG1 A/B källbitmappar (maskdata i författarens ursprungliga, omvända namnsättning):** [GitHub `SOURCE_U1_LEG1.json` på fryst separat gren](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json).
- **Fryst U1-LEG1 SOURCE-art fullständig Drive-ZIP:** [THE_SKRAUN_U1_LEG1_CAPRINE_GAIT_2026-11-16.zip](https://drive.google.com/file/d/1hMP78tBR5NrBnaBXdvc3yub23xTJB8vv/view), **39 124 byte**, SHA-256 `bd0d303f9793e43f6945a51b2e85aa5b0adfd4e9f17b7912b67229651c49db5c`, **22 ZIP-filer, 21/21 manifestposter** enligt tidigare verifierad source-rapport.
- **U1-LEG1:s ursprungliga källbegränsning:** bevarad `U1-FIX1` y=0..8 i båda poser; endast getbensrader y=9..11 ändrades. Fryst LEG1 A y9–11 `00100110 / 00100011 / 01100000`; B y9–11 `01100100 / 11000100 / 00000110`. **Försök inte 'rätta' eller revidera dessa bitar utan separat order.**
- **Godkänd presentationskonvention, NY i MAIN:s beslut efter originalpaketet:** VISUELL RIGHT = LEG1-författarens gamla LEFT; VISUELL LEFT = LEG1-författarens gamla RIGHT. Detta är **ett användarbeslut utanför och senare än det frysta ZIP:ets ursprungliga etiketter**. Om namn motsäger, låt senaste explicita användarbeslut styra visningsnamnen, medan källdata förblir oförändrad.
- [#22 – LEG1 som avklarad SOURCE-leverans](https://github.com/Odourman/the-skraun/issues/22). Status **CLOSED completed**.

## C. Proveniens / äldre frysta experiment (INTE senaste design)

- [U1-FIX1 exakt bas i GitHub](https://github.com/Odourman/the-skraun/blob/graphics/u1-fix1-facing-headpixel-20261116/graphics/u1_fix1/U1_FIX1_BITMAPS.json) och [Drive ZIP](https://drive.google.com/file/d/1brrYlMseD8rmRaVRQ2CAvanVUkRjI_xs/view), ZIP SHA-256 `02ef45d636867a384dc88dabeac4338996e2f0f6b275b2d5e17dacaa6fea935a`. Historiskt en huvudpixel bort på x7,y3 plus liten arm-/fotkorrigering, nu LEG1:s överdelsbas.
- [U1/U2 ursprunglig P3 i GitHub](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json) och [Drive ZIP](https://drive.google.com/file/d/196UpbC1Kl400BcMj5zZ44Y48p7-WW7-W/view). Ursprungligt upprätt U1; före huvudpixelkorrigering och getben.
- [P3-F1 forskningsfrisläppta D1/D2 rapport](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_GRAPHICS_P3_F1_POST_RESEARCH_INDEPENDENT_REVIEW_AND_DISPOSITION_2026-11-16.md) och [Drive ZIP](https://drive.google.com/file/d/1GjHMHqYeQRVyRiqc9dTf264qo_OEQlsq/view). D1/D2 avvisades estetiskt vid L1; **#21 CLOSED**.
- P1/P2 horisontell fyrbent kropp är anatomiska **negativa kontroller**, inte designgrund för nya spriteförsök.

## D. Faktisk teknisk evidens (aldrig 'source-only' = Stella)

- [#19 – ART1 level-3 överfull första P0-rasterrad, OPEN](https://github.com/Odourman/the-skraun/issues/19).
- [#1 – P01 oberoende Stella/NTSC-grind, OPEN](https://github.com/Odourman/the-skraun/issues/1).
- [#15 – global visuell gate, OPEN](https://github.com/Odourman/the-skraun/issues/15).
- [R3 visuell riktning och 57-fall-orienteringsrättning, inte helscen-GO](https://github.com/Odourman/the-skraun/pull/16).

## E. Förvaring

- [Gemensamma GRAPHICS-artifakter i Google Drive](https://drive.google.com/drive/folders/1udBPud9jpVzvMevcgKL8duib94GyV_yJ).
- [GitHub-repository `Odourman/the-skraun`](https://github.com/Odourman/the-skraun).

**Publiceringsdisciplin:** Befintliga leveranser är frysta. Denna migrationsgren innehåller **bara markdown-underlag**, inget nytt godkännande, inga bitmapdataomskrivningar, ingen originalbild, ingen ROM, ingen merge till main.
