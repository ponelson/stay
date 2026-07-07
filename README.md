# Luxury Hotel Atlas — Expanded Global Edition

Generated: 2026-07-06

## What changed

This expanded build adds the requested portfolios and tabs for:
Rosewood, Four Seasons, COMO, Auberge, Explora, Singita, Capella, &Beyond, EDITION, Antarctica Expedition Cruises, Hoshino Resorts, Rocco Forte, Zannier, The Chedi / GHM, Shangri-La Group, Jumeirah, and Taj / IHCL.

## Counts

Total embedded entries: **1,293**

Brand counts:

- Relais & Châteaux: 540
- Four Seasons: 165
- Shangri-La Group: 91
- Art Hotels: 75
- Taj / IHCL: 49
- Aman: 47
- Rosewood: 38
- Hoshino Resorts: 38
- EDITION: 31
- Belmond: 29
- &Beyond: 29
- Jumeirah: 28
- Auberge: 28
- COMO: 21
- Singita: 18
- Capella: 17
- Rocco Forte: 14
- Antarctica Expedition Cruises: 13
- Explora: 8
- The Chedi / GHM: 7
- Zannier: 7

## How to update

1. Open the HTML file in a browser.
2. Use **Update Tools → Export JSON** before major edits.
3. Run the updater starter:

```bash
python3 -m pip install requests beautifulsoup4 pandas lxml
python3 luxury_hotel_atlas_expanded_updater.py luxury_hotel_atlas_expanded_data.csv
```

4. Paste/import the refreshed JSON in the atlas.
5. Use **Geocode visible batch** after filtering to a brand or country.

## Data caveats

- This is an atlas and planning console, not a booking engine.
- Asterisks mark destinations with a routinely direct NYC-area gateway or nearest major nonstop gateway; seasonal schedules change.
- Relais & Châteaux mixes hotels, inns, lodges, restaurants, spas, cruises, and culinary members.
- Giant portfolios such as Shangri-La, Taj/IHCL, Hoshino, and Jumeirah change frequently; the updater exists so the file can be refreshed rather than fossilized.
- Some coordinates are city-level or country-level seeds until geocoded.
