# Contributing to RTI Road

## Setup

### Prerequisites
- Node.js 20+
- Python 3.10+
- npm

### Local Development

```bash
# Clone the repo
git clone <repo-url>
cd rti_road

# Install frontend dependencies
cd platform
npm install

# Install pipeline dependencies
cd pipeline
pip install -r requirements.txt

# Generate seed data (if data/ is empty)
cd ..
python3 seed/generate_seed.py

# Start dev server
npm run dev
# Site available at http://localhost:3000
```

### Running Tests

```bash
# Frontend tests
cd platform && npm test

# Data validation
cd platform && npm run validate-data

# Pipeline tests
cd platform/pipeline && python -m pytest tests/ -v

# Full build (verifies everything works end-to-end)
cd platform && npm run build
```

## How to Contribute

### Adding Data for a New Ward

1. File RTI applications using templates in `rti_applications_*.md`
2. When response arrives, run the pipeline:
   ```bash
   python pipeline/ingest.py \
     --input "response.xlsx" \
     --city bengaluru \
     --zone mahadevapura \
     --ward 150-bellandur \
     --rti-id "KA-RTI-2026-XXX"
   ```
3. Run `python pipeline/rebuild.py` to update aggregates
4. Verify: `npm run validate-data && npm run build`
5. Submit a PR

### Reporting Data Errors

Use the "Data Correction" issue template on GitHub. Include:
- Which page shows the error
- What the correct value should be
- Your source (RTI response, official document, etc.)

### Code Contributions

- Follow existing code style (TypeScript, React, Tailwind)
- Add tests for new features
- Run `npm test && npm run build` before submitting
- Keep PRs focused on one change

## Code Style

- TypeScript with strict mode
- React functional components
- Tailwind CSS for styling
- camelCase for variables and functions
- PascalCase for components and types
- No emojis or non-ASCII characters in code comments

## Data Format

See `DATA_FORMAT.md` for the complete JSON schema reference.
