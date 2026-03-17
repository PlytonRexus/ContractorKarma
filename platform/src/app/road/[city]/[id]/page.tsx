import { notFound } from 'next/navigation';
import dynamic from 'next/dynamic';
import { getAllRoads, getRoadById, getWorksForRoad, getRedFlags } from '@/lib/data';
import { DlpBadge } from '@/components/road/DlpBadge';
import { WorkTimeline } from '@/components/road/WorkTimeline';
import { ShareButton } from '@/components/common/ShareButton';
import { InfoTooltip } from '@/components/common/InfoTooltip';
import { WhatThisMeans } from '@/components/common/WhatThisMeans';
import { CivicActions } from '@/components/common/CivicActions';
import { formatCurrency } from '@/lib/formatCurrency';

const RoadMap = dynamic(
  () => import('@/components/map/RoadMap').then((m) => ({ default: m.RoadMap })),
  { ssr: false, loading: () => <div className="w-full h-64 bg-muted animate-pulse rounded-lg" /> }
);

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
  const allFlags = getRedFlags();
  const roadFlags = allFlags.filter((f) => f.roadId === road.roadId);

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

      {/* Map */}
      {road.lat != null && road.lng != null && (
        <div className="mb-8">
          <RoadMap
            center={[road.lat, road.lng]}
            zoom={16}
            className="w-full h-64"
            roads={[{
              roadId: road.roadId,
              roadName: road.roadName,
              lat: road.lat,
              lng: road.lng,
              dlpStatus: road.currentDlpStatus,
              dlpEnd: road.currentDlpEnd,
            }]}
            highlightRoadId={road.roadId}
          />
        </div>
      )}

      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-lg p-3">
          <p className="text-xs text-muted-foreground">Total Works</p>
          <p className="text-lg font-bold">{road.totalWorksCount}</p>
        </div>
        <div className="border rounded-lg p-3">
          <p className="text-xs text-muted-foreground">
            <InfoTooltip glossaryKey="sanctionedCost">Total Spending</InfoTooltip>
          </p>
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

      {/* Red Flags for this road */}
      {roadFlags.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">Red Flags</h2>
          <div className="space-y-2">
            {roadFlags.map((flag) => (
              <div
                key={flag.flagId}
                className="border rounded-lg px-4 py-3 border-l-4 border-l-red-400"
              >
                <p className="text-sm font-medium">{flag.description}</p>
                <p className="text-xs text-muted-foreground mt-1">
                  {flag.severity} severity
                </p>
                <WhatThisMeans flagType={flag.type} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Civic Actions */}
      <div className="mb-8">
        <CivicActions
          roadName={road.roadName}
          roadId={road.roadId}
          contractorName={road.currentContractor || undefined}
          flagType={roadFlags[0]?.type}
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
