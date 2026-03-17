# CLAUDE.md

## Project: RTI Road (Contractor Karma)

Civic transparency platform for road infrastructure data from RTI responses.
Fully static: Next.js 14 static export deployed to GitHub Pages, zero server costs.

## Quick Commands

```bash
cd platform && npm run dev          # dev server at localhost:3000
cd platform && npm run build        # full build (runs prebuild + static export)
cd platform && npm test             # 58 vitest tests
cd platform && npm run validate-data # JSON schema validation
cd platform && python3 -m pytest pipeline/tests/ -v  # 18 pipeline tests
cd platform && python3 seed/generate_seed.py          # regenerate seed data
```

## Project Structure

- `platform/`: all application code lives here
  - `src/app/`: Next.js pages (static routes)
  - `src/components/`: React UI components (shadcn/ui based)
  - `src/lib/`: Utilities and data layer (data.ts loads JSON files)
  - `src/types/`: TypeScript type definitions
  - `src/scripts/`: Build scripts (generateApiData.ts, validateData.ts)
  - `src/__tests__/`: Frontend tests (Vitest)
  - `data/`: JSON data files (the "database")
  - `pipeline/`: Python data ingestion pipeline (pandas, thefuzz)
  - `seed/`: Seed data generator (generate_seed.py)
- `drafts/`: RTI application templates and planning docs

## Tech Stack

- Next.js 14 (static export), TypeScript, Tailwind CSS, shadcn/ui
- Recharts for charts, Leaflet for maps, FlexSearch for client-side search
- Python with pandas and thefuzz for data pipeline
- Vitest (frontend), pytest (pipeline)

## Data Format

- Seed data wraps arrays in objects: `{ generatedAt, items/entries/flags/applications }`
- `data.ts` handles both wrapped and plain array formats
- DLP data uses `items` array (not `roads`), summary has `active/expired/expiringSoon`
- Stats uses nested `financials`, `dlp`, `performance` objects
- RTI apps use `filedDate` (not `filingDate`), `subject` (not `description`)

## Code Style

- TypeScript with strict mode
- camelCase for variables/functions, PascalCase for components/classes
- No snake_case
- No emojis, em-dashes, or non-ASCII characters in code comments
- No double hyphens in comments; use commas or colons instead
