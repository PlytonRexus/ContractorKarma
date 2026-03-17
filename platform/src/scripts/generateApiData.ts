/**
 * Generate static JSON files in public/api/ that are loaded client-side.
 * These are data files that cannot be imported at build time by client components.
 * Run this as part of the build: tsx src/scripts/generateApiData.ts
 */
import fs from 'fs';
import path from 'path';
import { getAllRoads, getSearchIndex, getAllWards, getDlpForWard } from '../lib/data';

const PUBLIC_API_DIR = path.join(process.cwd(), 'public', 'api');
const DATA_DIR = path.join(process.cwd(), 'data');
const PUBLIC_DATA_DIR = path.join(process.cwd(), 'public', 'data');

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function generateSearchIndex() {
  const entries = getSearchIndex();
  fs.writeFileSync(
    path.join(PUBLIC_API_DIR, 'search-index.json'),
    JSON.stringify(entries)
  );
  console.log(`Generated search-index.json (${entries.length} entries)`);
}

function generateDlpAll() {
  const wards = getAllWards();
  const allDlpEntries: unknown[] = [];

  for (const { cityId, zoneId, wardId, ward } of wards) {
    const dlp = getDlpForWard(cityId, zoneId, wardId);
    if (dlp && dlp.items) {
      for (const item of dlp.items) {
        allDlpEntries.push({
          roadId: item.roadId,
          roadName: item.roadName,
          dlpStatus: item.dlpStatus,
          dlpEnd: item.dlpEndDate,
          contractor: item.contractorName,
          contractorId: item.contractorId,
          wardName: ward.wardName,
        });
      }
    }
  }

  fs.writeFileSync(
    path.join(PUBLIC_API_DIR, 'dlp-all.json'),
    JSON.stringify(allDlpEntries)
  );
  console.log(`Generated dlp-all.json (${allDlpEntries.length} roads)`);
}

function copyFile(src: string, dest: string) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

function copyDownloadableData() {
  let count = 0;

  // Per-ward roads.json and works.json
  const wards = getAllWards();
  for (const { cityId, zoneId, wardId } of wards) {
    const wardDir = path.join('cities', cityId, 'zones', zoneId, 'wards', wardId);
    for (const file of ['roads.json', 'works.json']) {
      const src = path.join(DATA_DIR, wardDir, file);
      if (fs.existsSync(src)) {
        copyFile(src, path.join(PUBLIC_DATA_DIR, wardDir, file));
        count++;
      }
    }
  }

  // Contractors index
  const contractorsSrc = path.join(DATA_DIR, 'contractors', 'index.json');
  if (fs.existsSync(contractorsSrc)) {
    copyFile(contractorsSrc, path.join(PUBLIC_DATA_DIR, 'contractors', 'index.json'));
    count++;
  }

  // Red flags
  const flagsSrc = path.join(DATA_DIR, 'red-flags', 'flags.json');
  if (fs.existsSync(flagsSrc)) {
    copyFile(flagsSrc, path.join(PUBLIC_DATA_DIR, 'red-flags', 'flags.json'));
    count++;
  }

  console.log(`Copied ${count} downloadable data files to public/data/`);
}

ensureDir(PUBLIC_API_DIR);
generateSearchIndex();
generateDlpAll();
copyDownloadableData();
console.log('API data generation complete.');
