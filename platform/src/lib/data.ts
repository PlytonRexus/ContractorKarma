import fs from 'fs';
import path from 'path';
import {
  Road,
  Work,
  Contractor,
  Official,
  RedFlag,
  CityInfo,
  ZoneInfo,
  WardInfo,
  WardDlpSummary,
  PlatformMeta,
  PlatformStats,
  WardRanking,
  ContractorRanking,
  RtiApplication,
} from '@/types';

const DATA_DIR = path.join(process.cwd(), 'data');

function readJson<T>(filePath: string): T | null {
  try {
    const fullPath = path.join(DATA_DIR, filePath);
    const content = fs.readFileSync(fullPath, 'utf-8');
    return JSON.parse(content) as T;
  } catch {
    return null;
  }
}

// Platform-level data

export function getMeta(): PlatformMeta | null {
  return readJson<PlatformMeta>('meta.json');
}

export interface SeedStats {
  generatedAt: string;
  totalCities: number;
  totalZones: number;
  totalWards: number;
  totalRoads: number;
  totalWorks: number;
  totalContractors: number;
  totalOfficials: number;
  financials: {
    totalSanctionedCost: number;
    totalActualPaid: number;
    avgCostPerWork: number;
  };
  dlp: {
    active: number;
    expiringSoon: number;
    expired: number;
  };
  performance: {
    worksDelayed: number;
    delayPercentage: number;
    redFlagsTotal: number;
  };
}

export function getStats(): SeedStats | null {
  return readJson<SeedStats>('stats/summary.json');
}

export function getWardRankings(): WardRanking[] {
  return readJson<WardRanking[]>('stats/ward-rankings.json') || [];
}

export function getContractorRankings(): ContractorRanking[] {
  return readJson<ContractorRanking[]>('stats/contractor-rankings.json') || [];
}

// City/Zone/Ward data

export function getCityInfo(cityId: string): CityInfo | null {
  return readJson<CityInfo>(`cities/${cityId}/city.json`);
}

export function getZoneInfo(cityId: string, zoneId: string): ZoneInfo | null {
  return readJson<ZoneInfo>(`cities/${cityId}/zones/${zoneId}/zone.json`);
}

export function getWardInfo(
  cityId: string,
  zoneId: string,
  wardId: string
): WardInfo | null {
  return readJson<WardInfo>(
    `cities/${cityId}/zones/${zoneId}/wards/${wardId}/ward.json`
  );
}

export function getRoadsForWard(
  cityId: string,
  zoneId: string,
  wardId: string
): Road[] {
  return (
    readJson<Road[]>(
      `cities/${cityId}/zones/${zoneId}/wards/${wardId}/roads.json`
    ) || []
  );
}

export function getWorksForWard(
  cityId: string,
  zoneId: string,
  wardId: string
): Work[] {
  return (
    readJson<Work[]>(
      `cities/${cityId}/zones/${zoneId}/wards/${wardId}/works.json`
    ) || []
  );
}

export interface DlpData {
  wardSlug: string;
  generatedAt: string;
  summary: {
    totalWorks: number;
    active: number;
    expiringSoon: number;
    expired: number;
    unknown: number;
  };
  items: DlpItem[];
}

export interface DlpItem {
  jobCode: string;
  roadId: string;
  roadName: string;
  contractorId: string;
  contractorName: string;
  dlpStartDate: string;
  dlpEndDate: string;
  dlpDurationYears: number;
  dlpStatus: string;
}

export function getDlpForWard(
  cityId: string,
  zoneId: string,
  wardId: string
): DlpData | null {
  return readJson<DlpData>(
    `cities/${cityId}/zones/${zoneId}/wards/${wardId}/dlp.json`
  );
}

export function getOfficialsForWard(
  cityId: string,
  zoneId: string,
  wardId: string
): Official[] {
  return (
    readJson<Official[]>(
      `cities/${cityId}/zones/${zoneId}/wards/${wardId}/officials.json`
    ) || []
  );
}

// Contractor data

export function getAllContractors(): Contractor[] {
  return readJson<Contractor[]>('contractors/index.json') || [];
}

export function getContractor(contractorId: string): Contractor | null {
  return readJson<Contractor>(`contractors/${contractorId}.json`);
}

// Officials

export function getAllOfficials(): Official[] {
  return readJson<Official[]>('officials/index.json') || [];
}

// Red flags

export function getRedFlags(): RedFlag[] {
  const raw = readJson<{ flags?: RedFlag[] } | RedFlag[]>('red-flags/flags.json');
  if (!raw) return [];
  if (Array.isArray(raw)) return raw;
  if (raw.flags && Array.isArray(raw.flags)) return raw.flags;
  return [];
}

// RTI applications

export function getRtiApplications(): RtiApplication[] {
  const raw = readJson<{ applications?: RtiApplication[] } | RtiApplication[]>('rti/applications.json');
  if (!raw) return [];
  if (Array.isArray(raw)) return raw;
  if (raw.applications && Array.isArray(raw.applications)) return raw.applications;
  return [];
}

// Aggregate helpers

export function getAllRoads(): Road[] {
  const roads: Road[] = [];
  const citiesDir = path.join(DATA_DIR, 'cities');
  if (!fs.existsSync(citiesDir)) return roads;

  for (const city of fs.readdirSync(citiesDir)) {
    const zonesDir = path.join(citiesDir, city, 'zones');
    if (!fs.existsSync(zonesDir)) continue;

    for (const zone of fs.readdirSync(zonesDir)) {
      const wardsDir = path.join(zonesDir, zone, 'wards');
      if (!fs.existsSync(wardsDir)) continue;

      for (const ward of fs.readdirSync(wardsDir)) {
        const wardRoads = getRoadsForWard(city, zone, ward);
        roads.push(...wardRoads);
      }
    }
  }
  return roads;
}

export function getAllWards(): { cityId: string; zoneId: string; wardId: string; ward: WardInfo }[] {
  const wards: { cityId: string; zoneId: string; wardId: string; ward: WardInfo }[] = [];
  const citiesDir = path.join(DATA_DIR, 'cities');
  if (!fs.existsSync(citiesDir)) return wards;

  for (const city of fs.readdirSync(citiesDir)) {
    const zonesDir = path.join(citiesDir, city, 'zones');
    if (!fs.existsSync(zonesDir)) continue;

    for (const zone of fs.readdirSync(zonesDir)) {
      const wardsDir = path.join(zonesDir, zone, 'wards');
      if (!fs.existsSync(wardsDir)) continue;

      for (const wardDir of fs.readdirSync(wardsDir)) {
        const ward = getWardInfo(city, zone, wardDir);
        if (ward) {
          wards.push({ cityId: city, zoneId: zone, wardId: wardDir, ward });
        }
      }
    }
  }
  return wards;
}

export function getRoadById(roadId: string): Road | null {
  const allRoads = getAllRoads();
  return allRoads.find((r) => r.roadId === roadId) || null;
}

export function getWorksForRoad(roadId: string): Work[] {
  // Parse the roadId to find the ward
  // Format: blr-mhd-150-001 -> city=bengaluru, zone prefix=mhd
  const allWards = getAllWards();
  for (const { cityId, zoneId, wardId } of allWards) {
    const works = getWorksForWard(cityId, zoneId, wardId);
    const roadWorks = works.filter((w) => w.roadId === roadId);
    if (roadWorks.length > 0) return roadWorks;
  }
  return [];
}

// GeoJSON helpers

export interface GeoFeature {
  type: string;
  properties: {
    wardNumber: number;
    wardName: string;
    wardSlug: string;
    zone: string;
  };
  geometry: {
    type: string;
    coordinates: number[][][];
  };
}

export interface GeoFeatureCollection {
  type: string;
  features: GeoFeature[];
}

export function getWardGeoFeatures(): GeoFeature[] {
  const raw = readJson<GeoFeatureCollection>('geo/bengaluru-wards.geojson');
  if (!raw || !raw.features) return [];
  return raw.features;
}

export function getWardGeoFeature(wardNumber: number): GeoFeature | null {
  const features = getWardGeoFeatures();
  return features.find((f) => f.properties.wardNumber === wardNumber) || null;
}

export function getWardCenter(wardNumber: number): [number, number] | null {
  const feature = getWardGeoFeature(wardNumber);
  if (!feature || !feature.geometry || !feature.geometry.coordinates) return null;
  const coords = feature.geometry.coordinates[0];
  if (!coords || coords.length === 0) return null;
  // Compute centroid from polygon coordinates (excluding closing point)
  const ring = coords.slice(0, -1);
  const sumLng = ring.reduce((s, c) => s + c[0], 0);
  const sumLat = ring.reduce((s, c) => s + c[1], 0);
  return [sumLat / ring.length, sumLng / ring.length];
}

// Search index
export interface SearchEntry {
  type: 'road' | 'contractor' | 'work';
  id: string;
  title: string;
  subtitle: string;
  url: string;
}

export function getSearchIndex(): SearchEntry[] {
  const raw = readJson<{ entries?: SearchEntry[] } | SearchEntry[]>('search/index.json');
  if (!raw) return [];
  // Handle both wrapped { entries: [...] } and plain array formats
  if (Array.isArray(raw)) return raw;
  if (raw.entries && Array.isArray(raw.entries)) return raw.entries;
  return [];
}
