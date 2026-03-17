/**
 * Validate all JSON data files against expected schemas.
 * Run: npm run validate-data
 */
import fs from 'fs';
import path from 'path';

const DATA_DIR = path.join(process.cwd(), 'data');
let errors = 0;
let warnings = 0;

function readJson(filePath: string): unknown {
  const content = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(content);
}

function error(msg: string) {
  console.error(`  ERROR: ${msg}`);
  errors++;
}

function warn(msg: string) {
  console.warn(`  WARN: ${msg}`);
  warnings++;
}

function validateRoads(filePath: string) {
  const roads = readJson(filePath) as Record<string, unknown>[];
  const ids = new Set<string>();

  for (const road of roads) {
    if (!road.roadId) error(`Road missing roadId in ${filePath}`);
    if (!road.roadName) error(`Road missing roadName in ${filePath}`);
    if (typeof road.roadId === 'string') {
      if (ids.has(road.roadId)) error(`Duplicate roadId: ${road.roadId}`);
      ids.add(road.roadId);
    }
    if (!road.roadClass) warn(`Road ${road.roadId} missing roadClass`);
  }
  console.log(`  ${filePath}: ${roads.length} roads, ${ids.size} unique IDs`);
}

function validateWorks(filePath: string) {
  const works = readJson(filePath) as Record<string, unknown>[];
  const jobCodes = new Set<string>();

  for (const work of works) {
    if (!work.jobCode) error(`Work missing jobCode in ${filePath}`);
    if (!work.roadId) error(`Work missing roadId in ${filePath}`);
    if (typeof work.jobCode === 'string') {
      if (jobCodes.has(work.jobCode)) error(`Duplicate jobCode: ${work.jobCode}`);
      jobCodes.add(work.jobCode);
    }
  }
  console.log(`  ${filePath}: ${works.length} works, ${jobCodes.size} unique job codes`);
}

function validateContractors(filePath: string) {
  const contractors = readJson(filePath) as Record<string, unknown>[];
  for (const c of contractors) {
    if (!c.contractorId) error(`Contractor missing contractorId`);
    if (!c.legalName) error(`Contractor missing legalName`);
    const stats = c.stats as Record<string, unknown> | undefined;
    if (!stats) error(`Contractor ${c.contractorId} missing stats`);
  }
  console.log(`  ${filePath}: ${contractors.length} contractors`);
}

function walkWards() {
  const citiesDir = path.join(DATA_DIR, 'cities');
  if (!fs.existsSync(citiesDir)) {
    error('No cities/ directory found');
    return;
  }

  for (const city of fs.readdirSync(citiesDir)) {
    const cityJson = path.join(citiesDir, city, 'city.json');
    if (!fs.existsSync(cityJson)) {
      error(`Missing city.json for ${city}`);
      continue;
    }
    console.log(`\nCity: ${city}`);

    const zonesDir = path.join(citiesDir, city, 'zones');
    if (!fs.existsSync(zonesDir)) continue;

    for (const zone of fs.readdirSync(zonesDir)) {
      const zoneJson = path.join(zonesDir, zone, 'zone.json');
      if (!fs.existsSync(zoneJson)) {
        warn(`Missing zone.json for ${zone}`);
      }

      const wardsDir = path.join(zonesDir, zone, 'wards');
      if (!fs.existsSync(wardsDir)) continue;

      for (const ward of fs.readdirSync(wardsDir)) {
        console.log(`  Ward: ${ward}`);
        const wardDir = path.join(wardsDir, ward);

        const wardJson = path.join(wardDir, 'ward.json');
        if (!fs.existsSync(wardJson)) error(`Missing ward.json for ${ward}`);

        const roadsJson = path.join(wardDir, 'roads.json');
        if (fs.existsSync(roadsJson)) validateRoads(roadsJson);
        else warn(`Missing roads.json for ${ward}`);

        const worksJson = path.join(wardDir, 'works.json');
        if (fs.existsSync(worksJson)) validateWorks(worksJson);
        else warn(`Missing works.json for ${ward}`);
      }
    }
  }
}

function validateTopLevel() {
  // meta.json
  const metaPath = path.join(DATA_DIR, 'meta.json');
  if (fs.existsSync(metaPath)) {
    console.log('meta.json: OK');
  } else {
    error('Missing meta.json');
  }

  // contractors/index.json
  const contractorsPath = path.join(DATA_DIR, 'contractors', 'index.json');
  if (fs.existsSync(contractorsPath)) {
    validateContractors(contractorsPath);
  } else {
    error('Missing contractors/index.json');
  }

  // red-flags/flags.json
  const flagsPath = path.join(DATA_DIR, 'red-flags', 'flags.json');
  if (fs.existsSync(flagsPath)) {
    const flags = readJson(flagsPath) as unknown[];
    console.log(`red-flags/flags.json: ${flags.length} flags`);
  } else {
    warn('Missing red-flags/flags.json');
  }

  // stats/summary.json
  const statsPath = path.join(DATA_DIR, 'stats', 'summary.json');
  if (fs.existsSync(statsPath)) {
    console.log('stats/summary.json: OK');
  } else {
    warn('Missing stats/summary.json');
  }

  // search/index.json
  const searchPath = path.join(DATA_DIR, 'search', 'index.json');
  if (fs.existsSync(searchPath)) {
    const entries = readJson(searchPath) as unknown[];
    console.log(`search/index.json: ${entries.length} entries`);
  } else {
    warn('Missing search/index.json');
  }
}

console.log('=== Contractor Karma Data Validation ===\n');
validateTopLevel();
walkWards();

console.log(`\n=== Results ===`);
console.log(`Errors: ${errors}`);
console.log(`Warnings: ${warnings}`);

if (errors > 0) {
  process.exit(1);
}
