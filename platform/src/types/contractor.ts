export type PerformanceGrade = 'A' | 'B' | 'C' | 'D' | 'F';

export type RegistrationClass = 'Class I' | 'Class II' | 'Class III' | 'Class IV' | 'unknown';

export interface ContractorStats {
  totalWorks: number;
  totalSanctionedValue: number;
  worksCompletedOnTime: number;
  worksDelayed: number;
  dlpViolations: number;
  avgCostPerKm: number | null;
  wardsActive: string[];
  performanceGrade: PerformanceGrade;
  performanceScore: number;
}

export interface Contractor {
  contractorId: string;
  legalName: string;
  registrationNumber: string | null;
  registrationClass: RegistrationClass;
  address: string | null;
  stats: ContractorStats;
  phone: string | null;
  email: string | null;
  blacklisted: boolean;
  works: string[];
}
