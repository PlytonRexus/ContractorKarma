export type RedFlagSeverity = 'high' | 'medium' | 'low';

export type RedFlagCategory =
  | 'repeatFailure'
  | 'dlpSpending'
  | 'costOutlier'
  | 'contractorDominance'
  | 'severeDelay'
  | 'costOverrun';

export interface RedFlag {
  flagId: string;
  type: RedFlagCategory;
  severity: RedFlagSeverity;
  description: string;
  roadId: string | null;
  roadName: string | null;
  contractorId: string | null;
  contractorName: string | null;
  details: Record<string, string | number | null>;
}
