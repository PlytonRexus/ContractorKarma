import { Road } from '@/types/road';
import { DlpBadge } from './DlpBadge';
import { formatCurrency } from '@/lib/formatCurrency';

interface RoadCardProps {
  road: Road;
  cityId: string;
}

export function RoadCard({ road, cityId }: RoadCardProps) {
  return (
    <a
      href={`/road/${cityId}/${road.roadId}/`}
      className="block border rounded-lg p-4 hover:bg-accent transition-colors"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-sm truncate">{road.roadName}</h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            {road.roadClass === 'ward' ? 'Ward Road' : 'Arterial Road'}
            {road.lengthKm != null && ` | ${road.lengthKm} km`}
            {road.surfaceType !== 'unknown' && ` | ${road.surfaceType}`}
          </p>
        </div>
        <DlpBadge dlpEndDate={road.currentDlpEnd} />
      </div>
      <div className="mt-2 flex items-center gap-4 text-xs text-muted-foreground">
        {road.currentContractor && (
          <span>Contractor: {road.currentContractor}</span>
        )}
        <span>Total spent: {formatCurrency(road.totalSpending)}</span>
        <span>{road.totalWorksCount} work{road.totalWorksCount !== 1 ? 's' : ''}</span>
      </div>
    </a>
  );
}
