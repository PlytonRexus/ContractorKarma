export type WorkType =
  | 'asphalting'
  | 'concreting'
  | 'whiteTopping'
  | 'potholeFilling'
  | 'drainRemodeling'
  | 'footpathWork'
  | 'other';

export type FundingSource =
  | 'wardDevelopment'
  | 'pCodeGrant'
  | 'mayorGrant'
  | 'majorRoads'
  | 'tenderSure'
  | 'stateFund'
  | 'centralFund'
  | 'other';

export type DlpWorkStatus = 'active' | 'expired' | 'expiringSoon' | 'unknown';

export type RedFlagType =
  | 'delayed'
  | 'costOverrun'
  | 'repeatFailure'
  | 'dlpSpending'
  | 'costOutlier'
  | 'contractorDominance';

export interface CertifyingOfficial {
  name: string;
  designation: string;
  role: 'recordingOfficer' | 'checkMeasurement' | 'superintending';
}

export interface DataSource {
  rtiId: string;
  responseDate: string | null;
}

export interface Work {
  jobCode: string;
  roadId: string;
  description: string;
  workType: WorkType;
  contractorId: string;
  contractorName: string;
  woNumber: string | null;
  woDate: string | null;
  sanctionedCost: number | null;
  actualPaid: number | null;
  tenderNumber: string | null;
  bidCount: number | null;
  commencementDate: string | null;
  stipulatedCompletionDate: string | null;
  actualCompletionDate: string | null;
  fundingSource: FundingSource;
  dlpStartDate: string | null;
  dlpEndDate: string | null;
  dlpDurationYears: number | null;
  dlpStatus: DlpWorkStatus;
  certifyingOfficials: CertifyingOfficial[];
  performanceGuarantee: number | null;
  costPerKm: number | null;
  redFlags: RedFlagType[];
  dataSource: DataSource;
}
