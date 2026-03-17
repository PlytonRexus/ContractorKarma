# Architecture

## Overview

RTI Road is a fully static civic transparency platform. There is no server, no database, and no hosting costs. Data flows from RTI responses through a Python pipeline into JSON files, which Next.js reads at build time to generate static HTML pages deployed on GitHub Pages.

## Architecture Diagram

```
[RTI Responses: Excel/CSV/PDF]
        |
        v
[Python Pipeline]  -- runs locally or in CI
   pipeline/ingest.py
   pipeline/rebuild.py
        |
        v
[data/ directory]  -- JSON files (the "database")
        |
        v
[Next.js Static Export]  -- reads data/ at build time
        |
        v
[GitHub Pages]  -- serves static HTML/CSS/JS
        |
[jsDelivr CDN]  -- serves large data files (GeoJSON, search index)
```

## Directory Structure

```
rti_road/
  platform/
    src/app/          -- Next.js pages (static generation)
    src/components/   -- React components
    src/lib/          -- Utility functions, data layer
    src/types/        -- TypeScript type definitions
    src/__tests__/    -- Frontend tests (Vitest)
    data/             -- JSON data files
    pipeline/         -- Python data ingestion
    seed/             -- Seed data generator
    public/           -- Static assets
```

## Data Flow

1. RTI response arrives (Excel/CSV/scanned PDF)
2. Run `python pipeline/ingest.py --input response.xlsx --city bengaluru --zone mahadevapura --ward 150-bellandur`
3. Pipeline parses, normalizes, validates, and generates JSON files in `data/`
4. Run `python pipeline/rebuild.py` to regenerate aggregates (stats, rankings, search index, red flags)
5. Commit and push to GitHub
6. GitHub Actions runs `npm run build`, which generates static HTML
7. Static site deployed to GitHub Pages

## Key Design Decisions

### Why Static?
RTI data is batch-oriented (arrives in lumps when responses come back). It changes rarely (maybe monthly). Static sites are the fastest, cheapest, and most reliable way to serve read-heavy, rarely-changing data.

### Why JSON Files Instead of a Database?
- Zero hosting cost
- Git tracks all data changes with full history
- Anyone can fork and verify the data
- No migration scripts needed
- Build-time data loading means fast page renders

### Why Next.js Static Export?
- Generates one HTML file per road/contractor/ward for SEO
- React components for interactive features (search, maps)
- TypeScript for type safety
- `output: 'export'` produces plain HTML that works on any static host

### Build-Time vs Runtime Data
- **Build-time** (baked into HTML): Road lists, DLP badges, contractor names, ward summaries
- **Runtime** (fetched on demand): Search index, full map GeoJSON, detailed contractor data

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Static site generator | Next.js 14 (static export) |
| UI | shadcn/ui + Tailwind CSS |
| Charts | Recharts |
| Search | Client-side substring matching (upgradable to FlexSearch) |
| Data pipeline | Python (pandas, openpyxl, thefuzz) |
| Testing | Vitest (frontend), pytest (pipeline) |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |
| CDN | jsDelivr (for large data files) |
