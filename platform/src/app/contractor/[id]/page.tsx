import { notFound } from 'next/navigation';
import {
  getAllContractors,
  getContractor,
  getAllRoads,
} from '@/lib/data';
import { PerformanceGrade } from '@/components/contractor/PerformanceGrade';
import { formatCurrency } from '@/lib/formatCurrency';

interface ContractorPageProps {
  params: { id: string };
}

export async function generateStaticParams() {
  const contractors = getAllContractors();
  return contractors.map((c) => ({ id: c.contractorId }));
}

export async function generateMetadata({ params }: ContractorPageProps) {
  const contractor = getContractor(params.id);
  if (!contractor) return { title: 'Contractor Not Found - Contractor Karma' };
  return {
    title: `${contractor.legalName} - Contractor Karma`,
    description: `Performance grade ${contractor.stats.performanceGrade}. ${contractor.stats.totalWorks} works worth ${formatCurrency(contractor.stats.totalSanctionedValue)}.`,
  };
}

export default function ContractorPage({ params }: ContractorPageProps) {
  const contractor = getContractor(params.id);
  if (!contractor) return notFound();

  const stats = contractor.stats;
  const allRoads = getAllRoads();
  const contractorRoads = allRoads.filter(
    (r) => r.currentContractor === contractor.legalName
  );

  const onTimeRate =
    stats.totalWorks > 0
      ? Math.round((stats.worksCompletedOnTime / stats.totalWorks) * 100)
      : 0;

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-6 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold">{contractor.legalName}</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {contractor.registrationClass !== 'unknown'
              ? contractor.registrationClass
              : 'Registration class N/A'}
            {contractor.registrationNumber &&
              ` | Reg: ${contractor.registrationNumber}`}
          </p>
          {contractor.blacklisted && (
            <span className="inline-block mt-1 px-2 py-0.5 bg-red-100 text-red-700 text-xs rounded">
              BLACKLISTED
            </span>
          )}
        </div>
        <PerformanceGrade grade={stats.performanceGrade} size="lg" />
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Total Works</p>
          <p className="text-2xl font-bold">{stats.totalWorks}</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Total Value</p>
          <p className="text-2xl font-bold">
            {formatCurrency(stats.totalSanctionedValue)}
          </p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">On-Time Completion</p>
          <p className="text-2xl font-bold">{onTimeRate}%</p>
          <p className="text-xs text-muted-foreground">
            {stats.worksCompletedOnTime} of {stats.totalWorks}
          </p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">DLP Violations</p>
          <p className="text-2xl font-bold">{stats.dlpViolations}</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Works Delayed</p>
          <p className="text-2xl font-bold">{stats.worksDelayed}</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Avg Cost/km</p>
          <p className="text-2xl font-bold">
            {formatCurrency(stats.avgCostPerKm)}
          </p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Wards Active</p>
          <p className="text-2xl font-bold">{stats.wardsActive.length}</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Performance Score</p>
          <p className="text-2xl font-bold">
            {(stats.performanceScore * 100).toFixed(0)}%
          </p>
        </div>
      </div>

      {/* Roads by this contractor */}
      <div>
        <h2 className="text-lg font-semibold mb-3">
          Roads ({contractorRoads.length})
        </h2>
        <div className="space-y-2">
          {contractorRoads.map((road) => (
            <a
              key={road.roadId}
              href={`/road/bengaluru/${road.roadId}/`}
              className="block border rounded-lg px-4 py-3 hover:bg-accent transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">{road.roadName}</span>
                <span className="text-xs text-muted-foreground">
                  {formatCurrency(road.totalSpending)}
                </span>
              </div>
            </a>
          ))}
          {contractorRoads.length === 0 && (
            <p className="text-sm text-muted-foreground">
              No roads currently assigned to this contractor.
            </p>
          )}
        </div>
      </div>

      {/* Address */}
      {contractor.address && (
        <div className="mt-8">
          <h2 className="text-lg font-semibold mb-2">Registered Address</h2>
          <p className="text-sm text-muted-foreground">{contractor.address}</p>
        </div>
      )}
    </div>
  );
}
