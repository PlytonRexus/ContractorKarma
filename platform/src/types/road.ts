export type DlpStatus = 'active' | 'expired' | 'expiringSoon' | 'unknown';

export type RoadClass = 'ward' | 'arterial' | 'subArterial' | 'orrService';

export type SurfaceType = 'asphalt' | 'concrete' | 'whiteTopping' | 'gravel' | 'unknown';

export interface Road {
  roadId: string;
  roadName: string;
  aliases: string[];
  roadClass: RoadClass;
  surfaceType: SurfaceType;
  lengthKm: number | null;
  widthM: number | null;
  osmWayId: number | null;
  currentDlpStatus: DlpStatus;
  currentDlpEnd: string | null;
  currentContractor: string | null;
  totalWorksCount: number;
  totalSpending: number;
  lastUpdated: string;
}
