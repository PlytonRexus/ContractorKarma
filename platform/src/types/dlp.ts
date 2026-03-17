import { DlpStatus } from './road';

export interface DlpRoadEntry {
  roadId: string;
  roadName: string;
  dlpStatus: DlpStatus;
  dlpEnd: string | null;
  contractor: string | null;
  contractorId: string | null;
}

export interface WardDlpSummary {
  wardId: string;
  totalRoads: number;
  underWarranty: number;
  warrantyExpired: number;
  warrantyExpiringSoon: number;
  totalKmUnderWarranty: number;
  roads: DlpRoadEntry[];
}
