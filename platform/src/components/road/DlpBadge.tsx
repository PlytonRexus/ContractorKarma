'use client';

import { calculateDlpStatus } from '@/lib/dlpCalculator';
import { formatRelativeDate } from '@/lib/formatDate';
import { DlpStatus } from '@/types/road';

interface DlpBadgeProps {
  dlpEndDate: string | null;
  dlpStatus?: DlpStatus;
  contractorName?: string | null;
  showDetails?: boolean;
}

const statusConfig = {
  active: {
    bg: 'bg-green-100',
    text: 'text-green-800',
    border: 'border-green-300',
    dot: 'bg-green-500',
  },
  expired: {
    bg: 'bg-red-100',
    text: 'text-red-800',
    border: 'border-red-300',
    dot: 'bg-red-500',
  },
  expiringSoon: {
    bg: 'bg-yellow-100',
    text: 'text-yellow-800',
    border: 'border-yellow-300',
    dot: 'bg-yellow-500',
  },
  unknown: {
    bg: 'bg-gray-100',
    text: 'text-gray-600',
    border: 'border-gray-300',
    dot: 'bg-gray-400',
  },
};

export function DlpBadge({
  dlpEndDate,
  dlpStatus: overrideStatus,
  contractorName,
  showDetails = false,
}: DlpBadgeProps) {
  const result = calculateDlpStatus(dlpEndDate);
  const status = overrideStatus || result.status;
  const config = statusConfig[status];

  return (
    <div className={`inline-flex flex-col ${showDetails ? 'gap-1' : ''}`}>
      <span
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${config.bg} ${config.text} ${config.border}`}
      >
        <span className={`w-2 h-2 rounded-full ${config.dot}`} />
        {result.label}
      </span>
      {showDetails && dlpEndDate && status !== 'unknown' && (
        <span className="text-xs text-muted-foreground pl-1">
          {formatRelativeDate(dlpEndDate)}
          {contractorName && ` | ${contractorName}`}
        </span>
      )}
    </div>
  );
}
