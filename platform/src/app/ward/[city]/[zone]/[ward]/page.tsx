import { notFound } from 'next/navigation';
import {
  getAllWards,
  getWardInfo,
  getRoadsForWard,
  getDlpForWard,
  getWorksForWard,
  getOfficialsForWard,
  getRedFlags,
} from '@/lib/data';
import { RoadCard } from '@/components/road/RoadCard';
import { StatCard } from '@/components/common/StatCard';
import { formatCurrency } from '@/lib/formatCurrency';

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
          title="Under Warranty"
          value={dlp?.summary?.active ?? 0}
        />
        <StatCard title="Total Spending" value={formatCurrency(totalSpending)} />
        <StatCard title="Red Flags" value={wardFlags.length} />
      </div>

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
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Officials */}
      {officials.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-3">Current Officials</h2>
          <div className="space-y-2">
            {officials.map((official) => (
              <div
                key={official.officialId}
                className="border rounded-lg px-4 py-3"
              >
                <p className="text-sm font-medium">{official.designation}</p>
                {official.currentHolder && (
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {official.currentHolder.name}
                    {official.currentHolder.officialPhone &&
                      ` | ${official.currentHolder.officialPhone}`}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
