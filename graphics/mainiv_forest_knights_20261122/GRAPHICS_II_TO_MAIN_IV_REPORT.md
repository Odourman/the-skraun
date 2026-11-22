# THE SKRAUN — GRAPHICS II → MAIN IV
## SOURCE_ONLY: skogsglänta och riddarsprites (2026-11-22)

**Uppdrag:** uttrycklig MAIN IV-grafikorder. **Status:** `SOURCE_ONLY` / ej estetiskt godkända. **Ingen ROM, ingen Stella, ingen ändring av canon eller main.**

## Läsning och proveniens
- Projektkällor 00–04 (snapshot 2026-11-21); aktuella primärkällor: [design 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [visuell riktning](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md).
- GAMEPLAY-1: [draft PR #41](https://github.com/Odourman/the-skraun/pull/41), granskad på HEAD `7f289a536c375bf760428274280179cfe15a6a62`. P1 är blå proxy, svärdsvarning är i nuvarande diagnostik färgbyte och skogsmiljö två provisoriska PF-layouter. Full 2 riddare + Ranger och halo-X/renderern är INTE färdig.
- Äldre GRAPHICS v0.3 `ENEMIES_V03.json` och `WORLDS_V03.json`: 8×12 riddare/ranger och 40-cell PF-skogsform, **tidigare ej godkända**, vägledande endast.
- Spelarkonst: [fryst U1-LEG1](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json) med visuell höger = ursprunglig LEFT. Oförändrade byte. Privat originalfoto ej inkluderat.

## A: tre skogsförslag
Tre koncept i `FOREST_PF_CANDIDATES.json`, var och en med 22 höjdsegment à **8 fysiska rasterrader**, 20 PF-bitar på vänster halva, speglad högerhalva, en PF-cell = fyra colour clocks. Källmask samt exakta PF0/PF1/PF2-trippelvärden lagras per band. Man behöver inte skriva om höger-halvans PF midscanline eftersom spegling används; detta **bevisar inte** att verklig kärna hinner med byte- och färgbytena.

| ID | Motiv | Minsta grafiska centrala PF-öppning¹ | Omritade PF-trippelmönster² |
| --- | --- | --- | --- |
| **A_Glanta** | Rund krona, ojämn krona, buskar längs kant | **88 cc** | 10 |
| B_Dungar | Dunggrupper upptill och små stubbar | 64 cc | 9 |
| C_Skogskant | Trädkant, stora och små träd, stubbar | 80 cc | 12 |

¹ Endast bredaste högsta PF-markering på vänster sida och dess spegel, **inte** säker kollisionspassage eller fri level3-navigation. ² Antal unika tripletter i 22 segment, inte mätt antal TIA-skrivningar eller cykler.

**REKOMMENDATION: A_Glanta.** Den kommunicerar glänta med tydliga kron-/stamformer och lämnar en stor öppen mitt. B känns mer skogstät men kräver extra kollisionsomsorg; C fungerar som alternativ skogskant. Ingen ändring av kanoniska kartor. **Ingen kostnadsfri marktextur** utöver PF-objekt antas; markerad buske är en PF-siluett, och framtida dekor måste prövas separat. Egen separat kollisionsmodell krävs: en PF-krona blir inte automatiskt en solid hitbox.

## B: tre riddarkandidater
Faktiska bitmasker `KNIGHT_P1_CANDIDATES.json`. Alla är **8×16**, varje bit motsvarar ett P1-färgur och varje källa har 16 topp-först-rader för tre lägen: neutral/jakt, svärdsförvarning, svärdshugg. Inga extra TIA-objekt har lagts till.

- **K1_VISIR (rekommenderas):** liten tydlig visirspalt, differentierad rustnings-/axelsilhuett, två åtskilda ben och upplyft svärd i yttersta P1-kolumnen under varning. Huggformen blir en högervriden klinga inom samma åtta kolumner.
- **K2_VINGHJALM:** spetsigare och tydligt rustad form, svärdsarbete på vänster sida; risk att de två topparna liknar Skrauns horn.
- **K3_TUNG_RUSTNING:** bredare axlar/visir och ben, men svärdet är svagast isolerat från kroppens silhuett.

Rekommenderat grundfärgprov är `COLUP1=$9E` (ljusblå i GAMEPLAY-1). Provets RGB-färger är illustrationsvärden, inte ett fastställt NTSC-palettpass. Alternativa P1-byten per rasterrad kan inte antas gratis.

**Canon oförändrad:** cirka 0,4s stillastående, upplyft svärd före hugg (24 NTSC-rutor), kort aktivt skadefönster med attackpose, ~1s vila. Endast svärdshugg skadar, aldrig kroppskontakt. Svärdets grafiska räckvidd är *inte* automatisk hitbox; MAIN/ROM måste separat testa om åttabitars silhuett räcker.

## Kostnad, TIA och integration — instruktion, EJ ROM-order
- `P0` = exakt U1-LEG1. `P1` = en knight/ranger 8-bitarsrad. Två riddare plus Ranger inom samma scanline är **fortfarande obevisat**; grafiken löser inte N6-C eller N7:s tre-fiende-timingfel.
- `PF0/PF1/PF2`: skogsformer kan källkodskompileras till symmetriska 20-bitars radmasker. Vertikal 8-radershållning minskar antalet unika skogsdata, men GAMEPLAY-1:s befintliga `Visible` skriver PF för sin halo och provhinder och får **inte** få nya sen-/extra-skrivningar utan riktig 76-cykel-/beamdeadlinetest.
- `COLUPF`: under halo testmodell B blir **hela PF guld**, även träd; träden får inte fortsätta vara gröna på egen hand utan oberoende färgobjekt. `M1`-svärd vore ett separat framtida alternativ, har P1-färg och är **inte** beslutat.
- Riktigt kommande ROM-test: jämför `GRP1` 16×8 maskpixlar i autentisk Stella och tre poser på rätt X/Y/varaktighet; kontrollera PF-byte/order/spegling, färgkontrast, original-NTSC **262 scanlines**, 76 CPU-cykler inklusive TIA beamdeadlines, RIOT 128B med stack samt kollisions-/level3-korridorer i faktiskt spel. Detta får endast ROM DEVELOPMENT III göra efter en separat MAIN IV-order.

## Leverans
- [Masker: riddare](KNIGHT_P1_CANDIDATES.json)
- [Masker: skog](FOREST_PF_CANDIDATES.json)
- [Palettkandidater](PALETTE_PROPOSALS.json)
- **Alla 3 skogsbilder, 3×3 riddarposer, native 8×16-maskbilder, sammansatta scener, byte-tabeller, exakt U1-referenssnapshot, reproduktionsskript och SHA-manifest:** [ZIP i denna gren](THE_SKRAUN_MAIN_IV_GRAPHICS_FOREST_KNIGHTS_SOURCE_ONLY_2026-11-22.zip); samma ZIP i [Google Drive](https://drive.google.com/file/d/1PLa3oBjsBmgENpc5PJFbX0kJ0kfhLi5u/view).

Fullständigt paket: **32 filer, 220336 bytes, SHA256 `c9054563d18dcad5a49f07af7978a3c81df722b688baed9e556ef12f7f40fba0`** lokalt kontrollerat ZIP CRC PASS. Bildgenereringskod använder Pillow-nearest-neighbour, inte Stella.

**STOP:** MAIN IV och användaren väljer design; ingen ROM-implementation, inga berg-/dröm-/nattgrafikuppdrag, ingen merge till main, ingen automatisk ny order.
