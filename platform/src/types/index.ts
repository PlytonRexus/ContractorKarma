export * from './road';
export * from './work';
export * from './contractor';
export * from './dlp';
export * from './official';
export * from './redFlag';

export interface CityInfo {
  cityId: string;
  cityName: string;
  state: string;
  municipalBody: string;
  hierarchyLabels: {
    zone: string;
    ward: string;
  };
  rtiPortal: string | null;
  notes: string | null;
}

export interface ZoneInfo {
  zoneId: string;
  zoneName: string;
  cityId: string;
  wards: string[];
}

export interface WardInfo {
  wardId: string;
  wardName: string;
  wardNumber: number;
  zoneId: string;
  cityId: string;
}

export interface PlatformMeta {
  lastUpdated: string;
  totalRoads: number;
  totalKmTracked: number;
  totalSpending: number;
  citiesCovered: string[];
  version: string;
}

export interface PlatformStats {
  totalRoads: number;
  totalWorks: number;
  totalContractors: number;
  totalSpending: number;
  roadsUnderWarranty: number;
  kmUnderWarranty: number;
  warrantyExpired: number;
  warrantyExpiringSoon: number;
  redFlagsCount: number;
  wardsCovered: number;
  zonesCovered: number;
  lastUpdated: string;
}

export interface WardRanking {
  wardId: string;
  wardName: string;
  zoneId: string;
  totalRoads: number;
  totalSpending: number;
  warrantyRate: number;
  avgCostPerKm: number | null;
  redFlagsCount: number;
}

export interface ContractorRanking {
  contractorId: string;
  legalName: string;
  performanceScore: number;
  performanceGrade: string;
  totalWorks: number;
  totalValue: number;
  onTimeRate: number;
  dlpComplianceRate: number;
}

export interface RtiApplication {
  rtiId: string;
  filingDate: string | null;
  zone: string;
  ward: string | null;
  applicationType: string;
  status: 'draft' | 'filed' | 'responseReceived' | 'appeal';
  responseDate: string | null;
  description: string;
}
