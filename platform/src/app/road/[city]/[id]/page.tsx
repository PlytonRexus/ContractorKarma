import { notFound } from 'next/navigation';
import { getAllRoads, getRoadById, getWorksForRoad } from '@/lib/data';
import { DlpBadge } from '@/components/road/DlpBadge';
import { WorkTimeline } from '@/components/road/WorkTimeline';
import { ShareButton } from '@/components/common/ShareButton';
import { formatCurrency } from '@/lib/formatCurrency';

interface RoadPageProps {
  params: { city: string; id: string };
}

export async function generateStaticParams() {
  const roads = getAllRoads();
  return roads.map((road) => {
    // Extract city from roadId pattern: blr-mhd-150-001 -> bengaluru
    const cityPrefix = road.roadId.split('-')[0];
    const cityMap: Record<string, string> = { blr: 'bengaluru' };
    const city = cityMap[cityPrefix] || cityPrefix;
    return { city, id: road.roadId };
  });
}

export async function generateMetadata({ params }: RoadPageProps) {
  const road = getRoadById(params.id);
  if (!road) return { title: 'Road Not Found - Contractor Karma' };
  return {
    title: `${road.roadName} - Contractor Karma`,
    description: `DLP warranty status, contractor details, and work history for ${road.roadName}. Total spending: ${formatCurrency(road.totalSpending)}.`,
  };
}

export default function RoadPage({ params }: RoadPageProps) {
  const road = getRoadById(params.id);
  if (!road) return notFound();

  const works = getWorksForRoad(road.roadId);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 className="text-2xl font-bold">{road.roadName}</h1>
            <p className="text-sm text-muted-foreground mt-1">
              {road.roadClass === 'ward' ? 'Ward Road' : 'Arterial Road'}
              {road.lengthKm != null && ` | ${road.lengthKm} km`}
              {road.widthM != null && ` | ${road.widthM}m wide`}
              {road.surfaceType !== 'unknown' && ` | ${road.surfaceType}`}
            </p>
            {road.aliases.length > 0 && (
              <p className="text-xs text-muted-foreground mt-0.5">
                Also known as: {road.aliases.join(', ')}
              </p>
            )}
          </div>
          <DlpBadge
            dlpEndDate={road.currentDlpEnd}
            contractorName={road.currentContractor}
            showDetails
          />
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-lg p-3">
          <p className="text-xs text-muted-foreground">Total Works</p>
          <p className="text-lg font-bold">{road.totalWorksCount}</p>
        </div>
        <div className="border rounded-lg p-3">
          <p className="text-xs text-muted-foreground">Total Spending</p>
          <p className="text-lg font-bold">
            {formatCurrency(road.totalSpending)}
          </p>
        </div>
        <div className="border rounded-lg p-3">
          <p className="text-xs text-muted-foreground">Current Contractor</p>
          <p className="text-sm font-medium">
            {road.currentContractor || 'N/A'}
          </p>
        </div>
        <div className="border rounded-lg p-3">
          <p className="text-xs text-muted-foreground">Surface Type</p>
          <p className="text-sm font-medium capitalize">{road.surfaceType}</p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-3 mb-8">
        <ShareButton
          roadName={road.roadName}
          dlpStatus={road.currentDlpStatus}
          contractorName={road.currentContractor}
          dlpEndDate={road.currentDlpEnd}
        />
      </div>

      {/* Work Timeline */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Work History</h2>
        <WorkTimeline works={works} />
      </div>
    </div>
  );
}
