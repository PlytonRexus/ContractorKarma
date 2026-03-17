import { DlpStatus } from '@/types/road';

export interface DlpResult {
  status: DlpStatus;
  label: string;
  color: string;
  daysRemaining: number | null;
}

const EXPIRING_SOON_THRESHOLD_DAYS = 180; // 6 months

/**
 * Calculate DLP (Defect Liability Period) status for a given end date.
 * Returns status, display label, CSS color class, and days remaining.
 */
export function calculateDlpStatus(
  dlpEndDate: string | null | undefined,
  referenceDate?: Date
): DlpResult {
  if (!dlpEndDate) {
    return {
      status: 'unknown',
      label: 'Unknown',
      color: 'bg-dlp-unknown',
      daysRemaining: null,
    };
  }

  const endDate = new Date(dlpEndDate);
  if (isNaN(endDate.getTime())) {
    return {
      status: 'unknown',
      label: 'Invalid date',
      color: 'bg-dlp-unknown',
      daysRemaining: null,
    };
  }

  const now = referenceDate || new Date();
  const diffMs = endDate.getTime() - now.getTime();
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays < 0) {
    return {
      status: 'expired',
      label: 'Warranty Expired',
      color: 'bg-dlp-expired',
      daysRemaining: diffDays,
    };
  }

  if (diffDays <= EXPIRING_SOON_THRESHOLD_DAYS) {
    return {
      status: 'expiringSoon',
      label: 'Expiring Soon',
      color: 'bg-dlp-expiringSoon',
      daysRemaining: diffDays,
    };
  }

  return {
    status: 'active',
    label: 'Under Warranty',
    color: 'bg-dlp-active',
    daysRemaining: diffDays,
  };
}

/**
 * Get the expected DLP duration (in years) based on surface type.
 */
export function getExpectedDlpYears(surfaceType: string): number {
  switch (surfaceType) {
    case 'asphalt':
      return 3;
    case 'concrete':
      return 5;
    case 'whiteTopping':
      return 10;
    default:
      return 3;
  }
}
