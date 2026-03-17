/**
 * Generate static JSON files in public/api/ that are loaded client-side.
 * These are data files that cannot be imported at build time by client components.
 * Run this as part of the build: tsx src/scripts/generateApiData.ts
 */
import fs from 'fs';
import path from 'path';
import { getAllRoads, getSearchIndex, getAllWards, getDlpForWard } from '../lib/data';

const PUBLIC_API_DIR = path.join(process.cwd(), 'public', 'api');

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

ensureDir(PUBLIC_API_DIR);
generateSearchIndex();
generateDlpAll();
console.log('API data generation complete.');
