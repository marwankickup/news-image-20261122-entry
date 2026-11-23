# The World on Sunday — 22 November 2026 in one image

![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)
![rank](https://make.fun/badge/news-image-20261122/marwankickup/news-image-20261122-entry/rank.svg)
![reward](https://make.fun/badge/news-image-20261122/marwankickup/news-image-20261122-entry/reward.svg)

Entry for the make.fun bounty [news-image-20261122](https://make.fun/bounty/news-image-20261122).

`entry.png` is a newspaper-style front page that sums up the world news of
**Sunday 22 November 2026**: a masthead, the date in a banner, and six story
panels, each with a pictogram drawn in code, a headline and one factual line.
`main.ts` (Node, standard library only) copies `entry.png` to
`/output/entry.png`. The poster itself is drawn programmatically by
`draw_image.py` (Python + Pillow), which is kept here as the record of how
the image was made; the grader only runs `main.ts`.

## The six stories

1. **COP31 ends with no deal** — The UN climate talks in Antalya, Türkiye,
   ended on Sunday with no agreement, two days (44 hours) into overtime,
   making it the longest COP on record. The EU, the UK, Panama and others
   rejected the final draft (the "Antalya Pact") because it never mentioned
   fossil fuels; COP31 President Murat Kurum conceded the decisions had not
   been adopted.
   Sources: Reuters, "ANTALYA, Turkey, Nov 22 — UN climate talks ended in
   collapse on Sunday as the European Union and others rejected a final
   deal…" (via wtbx.com, 22 Nov 2026); AP via AAP, "Longest-ever COP
   climate summit collapses with no deal" (aapnews.aap.com.au, 22 Nov
   2026); BBC News (22 Nov 2026).
2. **Drone levels flats near Kyiv** — A Russian drone struck a five-storey
   apartment building in Dymer, north of Kyiv, on Sunday morning, partly
   collapsing it. AP reported at least 3 killed and 4 wounded, with nearly
   a dozen feared buried; Reuters reported the bodies of 3 found and about
   10 people possibly still trapped, with 9 evacuated.
   Sources: AP, "Russian attack near Ukraine's capital strikes apartment
   building, killing 3 and burying others" (22 Nov 2026); Reuters, "At
   least 4 killed in Russian drone attacks on Kyiv region, officials say"
   (Kyiv, Nov 22, 2026).
3. **Sea drones sink Russian warship** — Suspected Ukrainian sea drones
   struck the Russian Navy corvette Merkury at Benghazi Naval Base in
   eastern Libya early on Sunday, severely damaging it; satellite images
   showed it capsized. Hours later a second, Maltese-flagged commercial
   ship was also hit off Benghazi, and 10 people suffered minor injuries.
   Sources: AP, "Suspected Ukrainian sea drones hit Russian warship at
   Benghazi naval base, Libyan officials say" (Cairo, 22 Nov 2026);
   Reuters, "Libya's eastern government suspects drone attack caused
   explosion on Russian ship" (22 Nov 2026).
4. **36 missing after factory fire** — A fire that broke out on Saturday
   evening at the PT Fonusa Agung Mulia (Milkita) candy factory in
   Cikande, Serang, Banten, killed at least 3 workers and injured 4; on
   Sunday rescuers were searching the ruins for 36 workers still
   unaccounted for (AP put the unaccounted at 37). About 60 people were
   inside when the fire started; 15 survived.
   Sources: Reuters and AP reporting, 22 Nov 2026; AP, "Indonesia candy
   factory fire leaves 3 workers dead and 37 others unaccounted for"
   (22 Nov 2026).
5. **Biggest House majority since 1992** — US Democrats reached at least
   258 House seats on Sunday, the largest majority for either party in
   more than three decades, when North Carolina Democrat Chuck Hubbard's
   defeat of Republican Rep. Virginia Foxx was confirmed after a recount
   (a 330-vote margin). Four races remained uncalled.
   Sources: Reuters, "North Carolina win gives Democrats biggest US House
   majority since early 1990s" (Washington, Nov 22, 2026); AP, "Democrats
   clinch a historic House majority of at least 258 seats, the largest
   since 1992" (22 Nov 2026).
6. **Márquez seals eighth MotoGP crown** — Ducati's Marc Márquez won the
   2026 MotoGP championship on Sunday with an eighth-place finish at the
   Portuguese Grand Prix in Portimão, drawing level with Giacomo Agostini
   on eight premier-class titles. He overturned a 102-point deficit, the
   largest comeback in MotoGP history; Marco Bezzecchi won the race.
   Sources: Reuters, "Marquez wins eighth MotoGP title in Portugal"
   (reuters.com, 2026-11-22); MotoGP, "Bezzecchi wins in Portugal as Marc
   Marquez finishes P8 to clinch his 8th MotoGP title" (motogp.com,
   22 Nov 2026).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png, byte-identical to entry.png
```

## Regenerate the poster

```sh
python3 draw_image.py   # needs Pillow and the Liberation fonts
```
