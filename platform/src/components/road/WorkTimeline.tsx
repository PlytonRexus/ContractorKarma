import { Work } from '@/types/work';
import { formatCurrency } from '@/lib/formatCurrency';
import { formatDate } from '@/lib/formatDate';
import { DlpBadge } from './DlpBadge';

interface WorkTimelineProps {
  works: Work[];
}

export function WorkTimeline({ works }: WorkTimelineProps) {
  if (works.length === 0) {
    return (
      <p className="text-sm text-muted-foreground py-4">
        No works recorded for this road.
      </p>
    );
  }

  const sorted = [...works].sort((a, b) => {
    const dateA = a.actualCompletionDate || a.woDate || '';
    const dateB = b.actualCompletionDate || b.woDate || '';
    return dateB.localeCompare(dateA);
  });

  return (
    <div className="space-y-4">
      {sorted.map((work, index) => (
        <div
          key={work.jobCode}
          className="relative pl-6 pb-4 border-l-2 border-border last:border-l-0"
        >
          <div className="absolute -left-[5px] top-0 w-2 h-2 rounded-full bg-primary" />
          <div className="border rounded-lg p-4">
            <div className="flex items-start justify-between gap-2">
              <div>
                <h4 className="text-sm font-medium">{work.description}</h4>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Job Code: {work.jobCode}
                </p>
              </div>
              <DlpBadge dlpEndDate={work.dlpEndDate} />
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-2 mt-3 text-xs">
              <div>
                <span className="text-muted-foreground">Contractor</span>
                <p className="font-medium">{work.contractorName}</p>
              </div>
              <div>
                <span className="text-muted-foreground">Sanctioned Cost</span>
                <p className="font-medium">{formatCurrency(work.sanctionedCost)}</p>
              </div>
              <div>
                <span className="text-muted-foreground">Actual Paid</span>
                <p className="font-medium">{formatCurrency(work.actualPaid)}</p>
              </div>
              <div>
                <span className="text-muted-foreground">WO Date</span>
                <p>{formatDate(work.woDate)}</p>
              </div>
              <div>
                <span className="text-muted-foreground">Completed</span>
                <p>{formatDate(work.actualCompletionDate)}</p>
              </div>
              <div>
                <span className="text-muted-foreground">DLP Period</span>
                <p>
                  {formatDate(work.dlpStartDate)} - {formatDate(work.dlpEndDate)}
                </p>
              </div>
            </div>

            {work.certifyingOfficials.length > 0 && (
              <div className="mt-3 pt-3 border-t">
                <p className="text-xs text-muted-foreground mb-1">
                  Certifying Officials
                </p>
                <div className="flex flex-wrap gap-2">
                  {work.certifyingOfficials.map((official, i) => (
                    <span
                      key={i}
                      className="text-xs bg-secondary px-2 py-0.5 rounded"
                    >
                      {official.name} ({official.designation})
                    </span>
                  ))}
                </div>
              </div>
            )}

            {work.redFlags.length > 0 && (
              <div className="mt-2 flex gap-1">
                {work.redFlags.map((flag) => (
                  <span
                    key={flag}
                    className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded"
                  >
                    {flag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
