# RTI Road: Civic Road Infrastructure Transparency Platform

## The Problem

Road infrastructure data in Indian cities -- who built a road, how much was spent, whether the warranty is still active -- exists inside government registers but is effectively inaccessible to the public. When a road develops potholes within its warranty period (called the Defect Liability Period or DLP), citizens don't know that the contractor is legally obligated to fix it for free. Instead, the municipality quietly spends public money on repairs that contractors should be paying for. There is no way to look up which contractor built a specific road, what their track record looks like across the city, or which officials certified the work.

The Right to Information Act (2005) gives citizens the legal right to extract this data from government offices. RTI applications have already been drafted and are ready to file for two zones in Bengaluru -- Bellandur (Mahadevapura Zone) and BBMP South Zone. But raw RTI responses (Excel spreadsheets, scanned register pages, bureaucratic tables) are useless without a system to structure, cross-reference, and present them.

## What RTI Road Does

RTI Road transforms raw RTI disclosures into structured, queryable intelligence. A resident can search for their road by name, see whether it's under warranty (green/yellow/red badge), find the contractor responsible, and generate a WhatsApp message to share with their apartment group. A journalist can query aggregate contractor performance data and export CSV files. An RTI activist can identify which wards still lack data and file targeted applications.

The platform answers four questions:

1. **Is my road under warranty?** -- DLP status lookup with color-coded badges and expiry countdown.
2. **Who built this road and how much did it cost?** -- Full work history with job codes, costs, and certifying officials.
3. **How does this contractor perform?** -- Composite performance grades (A-F) based on on-time completion, DLP compliance, and cost efficiency.
4. **Where are the anomalies?** -- Automated red flags for repeat failures, cost outliers, warranty-period spending, and contractor dominance.

## Architecture: Zero Server, Zero Cost

The key constraint is no hosting budget. The entire platform runs as a static site deployed on GitHub Pages, with data served from the git repository itself. This works because RTI data is inherently batch-oriented -- it arrives in lumps when responses come back, not as a real-time stream. Data changes maybe once a month. A static site with pre-processed JSON files is the ideal architecture for this access pattern.

The data pipeline is a Python CLI tool that processes RTI responses (Excel/CSV files) through parsing, normalization (fuzzy-matching contractor names, canonicalizing road names, parsing Indian currency notation like "18.5 Lakhs"), validation (sanity checks on dates and costs, deduplication), and generation (structured JSON files for roads, works, contractors, DLP status, red flags, search index, and aggregate statistics).

Next.js reads these JSON files at build time and generates one static HTML page per road, per contractor, and per ward. Client-side features (search, DLP tracker filters) load pre-built JSON indexes on demand.

```
[RTI Responses: Excel/CSV/PDF]
        |
        v
[Python Pipeline]  -- parses, normalizes, validates, generates JSON
        |
        v
[data/ directory]  -- JSON files serving as the "database"
        |
        v
[Next.js Static Export]  -- generates one HTML page per road/contractor/ward
        |
        v
[GitHub Pages]  -- serves the static site at zero cost
```

The stack: Next.js 14 (static export), TypeScript, Tailwind CSS, Python with pandas and thefuzz, Vitest and pytest for testing, GitHub Actions for CI/CD.

## Data Model

The data is organized hierarchically: city > zone > ward > road > work > contractor/official. Each work record carries a job code (the primary key in BBMP's internal system, formatted as ward-year-serial like `150-23-000042`), links to a road and contractor, includes cost and timeline data, DLP dates, certifying officials, and automatically detected red flags.

Contractors get aggregate performance scores computed from on-time completion rate (40% weight), DLP compliance (40%), and cost efficiency relative to median (20%), producing letter grades A through F.

Red flags are pre-computed anomalies:

- **Repeat failure** -- road resurfaced within 2 years of previous work
- **DLP spending** -- public money spent on a road still under warranty
- **Cost outlier** -- cost-per-km exceeding 2x the ward median
- **Contractor dominance** -- a single contractor winning more than 50% of works in one ward
- **Severe delay** -- completion more than 6 months past deadline
- **Cost overrun** -- actual amount paid exceeding 1.2x the sanctioned cost

## DLP (Defect Liability Period)

The DLP is the warranty period after road construction. During this period, the contractor is liable for any defects and must repair them at their own cost:

- **Asphalt roads:** 3 years
- **Concrete roads:** 5 years
- **White-topped roads:** 10 years

If a road develops potholes or other defects during the DLP, the municipality should not spend public money on repairs. The contractor must fix it for free. This is the single most actionable piece of information the platform surfaces.

## Current State

The platform is fully functional with realistic seed data: 35 roads, 72 works, 8 contractors across 3 wards in Bengaluru (Bellandur, Jayanagar, BTM Layout). The seed data includes all the scenarios needed for development -- active warranties, expired warranties, expiring-soon warnings, high-performing and low-performing contractors, cost outliers, repeat failures, and incomplete data fields simulating partial RTI responses.

76 tests pass across the frontend and pipeline. The static build produces 56 HTML pages with a first-load JS size under 90KB per page.

## Broader Vision

Roads are the pilot domain, but the data architecture (city > zone > ward > asset > work > contractor > official) is domain-agnostic. The same schema shape applies to water supply pipelines, drainage construction, street lighting installations, solid waste management contracts, and public buildings. Each is a class of civic infrastructure where work orders, contractor performance, and warranty periods can be extracted through RTI and structured for public accountability.

The growth path: Bellandur MVP with real RTI data when responses arrive, then expand to remaining BBMP zones using the same RTI templates, then pilot a second city. The static architecture comfortably handles 50,000+ roads before any scaling concerns arise. Community contributions happen through pull requests -- anyone can fork the repo, add data for their ward, and submit it back.

## Repository Structure

```
rti_road/
  OVERVIEW.md                    -- this file
  ARCHITECTURE.md                -- technical architecture details
  CONTRIBUTING.md                -- how to contribute
  DATA_FORMAT.md                 -- JSON schema reference
  RTI_FILING_GUIDE.md            -- how to file RTIs for a new city
  framework.md                   -- domain strategy and initial schema
  APPLICATION_A_ready_to_file.md -- RTI template for ward roads
  APPLICATION_B_ready_to_file.md -- RTI template for arterial roads

  platform/
    src/app/          -- Next.js pages
    src/components/   -- React UI components
    src/lib/          -- Utilities and data layer
    src/types/        -- TypeScript type definitions
    src/__tests__/    -- Frontend tests (Vitest)
    data/             -- JSON data files (the "database")
    pipeline/         -- Python data ingestion pipeline
    seed/             -- Seed data generator

  .github/
    workflows/        -- CI/CD (deploy, test)
    ISSUE_TEMPLATE/   -- Templates for data corrections, new cities, defect reports
```

## Getting Started

```bash
cd platform
npm install
npm run dev        # start dev server at localhost:3000
npm test           # run 58 frontend tests
npm run build      # generate static site in out/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup instructions.
