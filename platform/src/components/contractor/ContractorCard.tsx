import { Contractor } from '@/types/contractor';
import { formatCurrency } from '@/lib/formatCurrency';
import { PerformanceGrade } from './PerformanceGrade';

interface ContractorCardProps {
  contractor: Contractor;
}

export function ContractorCard({ contractor }: ContractorCardProps) {
  const stats = contractor.stats;

  return (
    <a
      href={`/contractor/${contractor.contractorId}/`}
      className="block border rounded-lg p-4 hover:bg-accent transition-colors"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-sm">{contractor.legalName}</h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            {contractor.registrationClass !== 'unknown'
              ? contractor.registrationClass
              : 'Registration N/A'}
            {contractor.blacklisted && (
              <span className="text-red-600 ml-2">BLACKLISTED</span>
            )}
          </p>
        </div>
        <PerformanceGrade grade={stats.performanceGrade} />
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3 text-xs">
        <div>
          <span className="text-muted-foreground">Total Works</span>
          <p className="font-medium">{stats.totalWorks}</p>
        </div>
        <div>
          <span className="text-muted-foreground">Total Value</span>
          <p className="font-medium">{formatCurrency(stats.totalSanctionedValue)}</p>
        </div>
        <div>
          <span className="text-muted-foreground">On-Time</span>
          <p className="font-medium">
            {stats.totalWorks > 0
              ? Math.round((stats.worksCompletedOnTime / stats.totalWorks) * 100)
              : 0}
            %
          </p>
        </div>
        <div>
          <span className="text-muted-foreground">DLP Violations</span>
          <p className="font-medium">{stats.dlpViolations}</p>
        </div>
      </div>
    </a>
  );
}
