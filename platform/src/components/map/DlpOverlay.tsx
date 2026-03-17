'use client';

import { DlpStatus } from '@/types/road';

interface DlpLegendProps {
  className?: string;
}

const legendItems: { status: DlpStatus; label: string; color: string }[] = [
  { status: 'active', label: 'Under Warranty', color: '#16a34a' },
  { status: 'expiringSoon', label: 'Expiring Soon', color: '#ca8a04' },
  { status: 'expired', label: 'Warranty Expired', color: '#dc2626' },
  { status: 'unknown', label: 'Data Unavailable', color: '#6b7280' },
];

export function DlpLegend({ className = '' }: DlpLegendProps) {
  return (
    <div className={`flex flex-wrap gap-3 ${className}`}>
      {legendItems.map((item) => (
        <div key={item.status} className="flex items-center gap-1.5 text-xs">
          <span
            className="w-3 h-3 rounded-sm"
            style={{ backgroundColor: item.color }}
          />
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}

/**
 * Returns the color for a DLP status, for use with map styling.
 */
export function getDlpColor(status: DlpStatus): string {
  switch (status) {
    case 'active':
      return '#16a34a';
    case 'expiringSoon':
      return '#ca8a04';
    case 'expired':
      return '#dc2626';
    default:
      return '#6b7280';
  }
}
