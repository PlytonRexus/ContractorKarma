import { getAllContractors } from '@/lib/data';
import { ContractorCard } from '@/components/contractor/ContractorCard';

export const metadata = {
  title: 'Contractors - Contractor Karma',
  description: 'Contractor performance rankings based on RTI data. Track on-time completion rates and DLP compliance.',
};

export default function ContractorsPage() {
  const contractors = getAllContractors();
  const sorted = [...contractors].sort(
    (a, b) => b.stats.performanceScore - a.stats.performanceScore
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">Contractor Rankings</h1>
      <p className="text-sm text-muted-foreground mb-6">
        Performance grades based on on-time completion (40%), DLP compliance
        (40%), and cost efficiency (20%).
      </p>
      <div className="space-y-3">
        {sorted.map((contractor, index) => (
          <div key={contractor.contractorId} className="flex gap-3 items-start">
            <span className="text-lg font-bold text-muted-foreground w-8 text-right mt-3">
              {index + 1}
            </span>
            <div className="flex-1">
              <ContractorCard contractor={contractor} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
