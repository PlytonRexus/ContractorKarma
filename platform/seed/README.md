# Seed Data Generator

Generates realistic mock data for the Contractor Karma platform during development.

## What it generates

The script creates JSON data files in `platform/data/` covering:

### Geography
- **1 city**: Bengaluru
- **2 zones**: Mahadevapura, South
- **3 wards**: Bellandur (150), Jayanagar (168), BTM Layout (176)

### Roads
- **25 roads** in Bellandur ward (Mahadevapura zone) -- the primary ward with full coverage
- **5 roads** in Jayanagar ward (South zone)
- **5 roads** in BTM Layout ward (South zone)
- Road names are realistic Bengaluru localities (Green Glen Layout, Kaikondrahalli, Kasavanahalli, Haralur, Sarjapur Road, etc.)

### Works
- **~60 works** in Bellandur (some roads have 2-3 works showing history)
- **~6 works** in Jayanagar
- **~6 works** in BTM Layout
- Work types: asphalting, concretePaving, whitetopping, potholeFilling, resurfacing, drainRepair, footpathConstruction

### Contractors
- **8 contractors** with aggregated statistics
- Performance grades range from A (best) to D/F (worst)
- M/s Nandi Infrastructure (ctr-004) is the best performer (grade A)
- M/s ABC Infra Pvt Ltd (ctr-002) is the worst performer (grade D)

### Officials
- **15 officials** across wards with designations: JE, AE, AEE, EE, SE
- Certifying teams assigned to each work (recording officer, check measurement, superintending)

### DLP (Defect Liability Period)
- 3 years for asphalt roads
- 5 years for concrete roads
- 10 years for white-topping
- Statuses: active (green), expiringSoon (yellow, within 6 months), expired (red), unknown

### Red Flags (pre-computed anomalies)
At least 6 flags including:
1. **repeatFailure** -- Road resurfaced within 18 months (Kaikondrahalli Main Road)
2. **costOutlier** -- Sanctioned cost 80%+ above zone average (Haralur Road)
3. **delayedCompletion** -- Work completed 6+ months late (Sarjapur Road white-topping)
4. **missingFields** -- Incomplete data in work record (Devarabisanahalli)
5. **singleBid** -- Tender received only one bid
6. **poorContractorPerformance** -- Contractor with grade D and multiple violations

### Realistic Scenarios
- Roads with multiple works showing maintenance history
- Some works delayed by 2-12 months past stipulated completion
- Cost outliers (1.6x-1.8x zone average)
- Missing data fields (simulating incomplete RTI responses)
- Single-bid tenders
- Repeat road failures (same road resurfaced within 18 months)

### Other data files
- **RTI applications** -- 5 sample RTI filings with status tracking
- **Search index** -- All roads, works, and contractors indexed for search
- **GeoJSON** -- Simplified ward boundary polygons (approximate rectangles)
- **Stats** -- Summary statistics, ward rankings, contractor rankings

## Usage

```bash
cd platform
python3 seed/generate_seed.py
```

The script uses `random.seed(42)` for reproducibility. Running it multiple times produces identical output.

## Date assumptions

- Today's date is hardcoded to 2026-03-17 for DLP status calculations.
- Work dates span 2018-2025.
- DLP periods extend into 2026-2035 depending on surface type.

## Cost ranges

- Ward roads (asphalt): Rs 10-50 lakhs
- Collector roads (asphalt/concrete): Rs 50 lakhs - 2 crore
- Arterial roads (asphalt): Rs 1-5 crore
- White-topping: Rs 1-10 crore per km

## Output directory structure

```
data/
  meta.json
  cities/bengaluru/
    city.json
    zones/mahadevapura/
      zone.json
      wards/150-bellandur/
        ward.json, roads.json, works.json, dlp.json, officials.json
    zones/south/
      zone.json
      wards/168-jayanagar/
        ward.json, roads.json, works.json, dlp.json, officials.json
      wards/176-btm-layout/
        ward.json, roads.json, works.json, dlp.json, officials.json
  contractors/
    index.json, ctr-001.json .. ctr-008.json
  officials/
    index.json
  red-flags/
    flags.json
  stats/
    summary.json, ward-rankings.json, contractor-rankings.json
  search/
    index.json
  rti/
    applications.json
  geo/
    bengaluru-wards.geojson
```
