import { getRedFlags } from '@/lib/data';

export const metadata = {
  title: 'Red Flags - Contractor Karma',
  description: 'Pre-computed anomalies in road infrastructure data: repeat failures, cost outliers, DLP violations.',
};

const severityColors = {
  high: 'border-l-red-500 bg-red-50',
  medium: 'border-l-yellow-500 bg-yellow-50',
  low: 'border-l-blue-500 bg-blue-50',
};

const typeLabels: Record<string, string> = {
  repeatFailure: 'Repeat Failure',
  dlpSpending: 'DLP Spending',
  costOutlier: 'Cost Outlier',
  contractorDominance: 'Contractor Dominance',
  severeDelay: 'Severe Delay',
  costOverrun: 'Cost Overrun',
};

export default function RedFlagsPage() {
  const flags = getRedFlags();

  const byType: Record<string, typeof flags> = {};
  for (const flag of flags) {
    if (!byType[flag.type]) byType[flag.type] = [];
    byType[flag.type].push(flag);
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">Red Flags</h1>
      <p className="text-sm text-muted-foreground mb-6">
        Pre-computed anomalies detected in road infrastructure data. These are
        automatically flagged based on data patterns and thresholds.
      </p>

      {/* Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Total Flags</p>
          <p className="text-2xl font-bold">{flags.length}</p>
        </div>
        <div className="border rounded-lg p-4 border-l-4 border-l-red-500">
          <p className="text-xs text-muted-foreground">High Severity</p>
          <p className="text-2xl font-bold text-red-600">
            {flags.filter((f) => f.severity === 'high').length}
          </p>
        </div>
        <div className="border rounded-lg p-4 border-l-4 border-l-yellow-500">
          <p className="text-xs text-muted-foreground">Medium Severity</p>
          <p className="text-2xl font-bold text-yellow-600">
            {flags.filter((f) => f.severity === 'medium').length}
          </p>
        </div>
        <div className="border rounded-lg p-4 border-l-4 border-l-blue-500">
          <p className="text-xs text-muted-foreground">Low Severity</p>
          <p className="text-2xl font-bold text-blue-600">
            {flags.filter((f) => f.severity === 'low').length}
          </p>
        </div>
      </div>

      {/* Flags by type */}
      {Object.entries(byType).map(([type, typeFlags]) => (
        <div key={type} className="mb-8">
          <h2 className="text-lg font-semibold mb-3">
            {typeLabels[type] || type} ({typeFlags.length})
          </h2>
          <div className="space-y-2">
            {typeFlags.map((flag) => (
              <div
                key={flag.flagId}
                className={`border rounded-lg px-4 py-3 border-l-4 ${
                  severityColors[flag.severity]
                }`}
              >
                <p className="text-sm font-medium">{flag.description}</p>
                <div className="flex flex-wrap gap-3 mt-1.5 text-xs text-muted-foreground">
                  {flag.roadName && (
                    <a
                      href={`/road/bengaluru/${flag.roadId}/`}
                      className="hover:underline"
                    >
                      {flag.roadName}
                    </a>
                  )}
                  {flag.contractorName && (
                    <a
                      href={`/contractor/${flag.contractorId}/`}
                      className="hover:underline"
                    >
                      {flag.contractorName}
                    </a>
                  )}
                  <span>{flag.severity} severity</span>
                </div>
                {Object.keys(flag.details).length > 0 && (
                  <div className="mt-2 text-xs text-muted-foreground">
                    {Object.entries(flag.details).map(([k, v]) => (
                      <span key={k} className="mr-3">
                        {k}: {v ?? 'N/A'}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}

      {flags.length === 0 && (
        <p className="text-sm text-muted-foreground py-8">
          No anomalies detected. This will populate as more data is ingested.
        </p>
      )}
    </div>
  );
}
