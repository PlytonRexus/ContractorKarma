import { notFound } from 'next/navigation';
import dynamic from 'next/dynamic';
import {
  getAllWards,
  getWardInfo,
  getRoadsForWard,
  getDlpForWard,
  getWorksForWard,
  getOfficialsForWard,
  getRedFlags,
  getWardGeoFeature,
  getWardCenter,
} from '@/lib/data';
import { RoadCard } from '@/components/road/RoadCard';
import { StatCard } from '@/components/common/StatCard';
import { InfoTooltip } from '@/components/common/InfoTooltip';
import { WhatThisMeans } from '@/components/common/WhatThisMeans';
import { CivicActions } from '@/components/common/CivicActions';
import { BbmpContactCard } from '@/components/common/BbmpContactCard';
import { formatCurrency } from '@/lib/formatCurrency';

const RoadMap = dynamic(
  () => import('@/components/map/RoadMap').then((m) => ({ default: m.RoadMap })),
  { ssr: false, loading: () => <div className="w-full h-96 bg-muted animate-pulse rounded-lg" /> }
);

interface WardPageProps {
  params: { city: string; zone: string; ward: string };
}

export async function generateStaticParams() {
  const wards = getAllWards();
  return wards.map(({ cityId, zoneId, wardId }) => ({
    city: cityId,
    zone: zoneId,
    ward: wardId,
  }));
}

export async function generateMetadata({ params }: WardPageProps) {
  const ward = getWardInfo(params.city, params.zone, params.ward);
  if (!ward) return { title: 'Ward Not Found - Contractor Karma' };
  return {
    title: `${ward.wardName} - Contractor Karma`,
    description: `Road infrastructure data for ${ward.wardName} (Ward ${ward.wardNumber}). DLP warranty status, contractor details, and spending analysis.`,
  };
}

export default function WardPage({ params }: WardPageProps) {
  const ward = getWardInfo(params.city, params.zone, params.ward);
  if (!ward) return notFound();

  const roads = getRoadsForWard(params.city, params.zone, params.ward);
  const dlp = getDlpForWard(params.city, params.zone, params.ward);
  const works = getWorksForWard(params.city, params.zone, params.ward);
  const officials = getOfficialsForWard(params.city, params.zone, params.ward);
  const allFlags = getRedFlags();
  const wardFlags = allFlags.filter((f) =>
    f.roadId?.includes(`-${ward.wardNumber}-`)
  );

  const totalSpending = works.reduce(
    (sum, w) => sum + (w.actualPaid || w.sanctionedCost || 0),
    0
  );

  const wardGeo = getWardGeoFeature(ward.wardNumber);
  const wardCenter = getWardCenter(ward.wardNumber);

  // Build road markers for the map
  const roadMarkers = roads
    .filter((r) => r.lat != null && r.lng != null)
    .map((r) => ({
      roadId: r.roadId,
      roadName: r.roadName,
      lat: r.lat as number,
      lng: r.lng as number,
      dlpStatus: r.currentDlpStatus,
      dlpEnd: r.currentDlpEnd,
    }));

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold">{ward.wardName}</h1>
        <p className="text-sm text-muted-foreground">
          Ward {ward.wardNumber} | {params.zone} zone
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard title="Total Roads" value={roads.length} />
        <StatCard
          title={<InfoTooltip glossaryKey="dlp">Under Warranty</InfoTooltip>}
          value={dlp?.summary?.active ?? 0}
        />
        <StatCard title="Total Spending" value={formatCurrency(totalSpending)} />
        <StatCard title="Red Flags" value={wardFlags.length} />
      </div>

      {/* Map */}
      {roadMarkers.length > 0 && wardCenter && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">Ward Map</h2>
          <RoadMap
            center={wardCenter}
            zoom={14}
            roads={roadMarkers}
            wardBoundary={wardGeo?.geometry}
          />
          <div className="flex gap-4 mt-2 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-green-600" /> Under Warranty
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-yellow-600" /> Expiring Soon
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-red-600" /> Expired
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-gray-400" /> Unknown
            </span>
          </div>
        </div>
      )}

      {/* DLP Summary */}
      {dlp && dlp.summary && (
        <div className="border rounded-lg p-4 mb-8">
          <h2 className="font-semibold mb-3">Warranty Overview</h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-green-600">
                {dlp.summary.active}
              </p>
              <p className="text-xs text-muted-foreground">Active</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-yellow-600">
                {dlp.summary.expiringSoon}
              </p>
              <p className="text-xs text-muted-foreground">Expiring Soon</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-red-600">
                {dlp.summary.expired}
              </p>
              <p className="text-xs text-muted-foreground">Expired</p>
            </div>
          </div>
        </div>
      )}

      {/* Roads List */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-3">
          Roads ({roads.length})
        </h2>
        <div className="space-y-2">
          {roads.map((road) => (
            <RoadCard key={road.roadId} road={road} cityId={params.city} />
          ))}
        </div>
      </div>

      {/* Red Flags */}
      {wardFlags.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">Red Flags</h2>
          <div className="space-y-2">
            {wardFlags.map((flag) => (
              <div
                key={flag.flagId}
                className="border rounded-lg px-4 py-3 border-l-4 border-l-red-400"
              >
                <p className="text-sm font-medium">{flag.description}</p>
                <p className="text-xs text-muted-foreground mt-1">
                  {flag.roadName} | {flag.severity} severity
                </p>
                <WhatThisMeans flagType={flag.type} />
              </div>
            ))}
          </div>
          <div className="mt-3">
            <CivicActions
              wardName={ward.wardName}
              wardNumber={String(ward.wardNumber)}
            />
          </div>
        </div>
      )}

      {/* Officials */}
      {officials.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-3">Current Officials</h2>
          <div className="space-y-2">
            {officials.map((official) => (
              <div
                key={official.officialId}
                className="border rounded-lg px-4 py-3"
              >
                <p className="text-sm font-medium">{official.designation}</p>
                {official.currentHolder && (
                  <div className="text-xs text-muted-foreground mt-0.5">
                    <span>{official.currentHolder.name}</span>
                    {official.currentHolder.officialPhone && (
                      <span>
                        {' | '}
                        <a href={`tel:${official.currentHolder.officialPhone}`} className="text-blue-600 hover:underline">
                          {official.currentHolder.officialPhone}
                        </a>
                      </span>
                    )}
                    {official.currentHolder.officialEmail && (
                      <span>
                        {' | '}
                        <a href={`mailto:${official.currentHolder.officialEmail}`} className="text-blue-600 hover:underline">
                          {official.currentHolder.officialEmail}
                        </a>
                      </span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* BBMP Contact Card */}
      <BbmpContactCard />
    </div>
  );
}
