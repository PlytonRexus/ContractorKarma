import { getRtiApplications } from '@/lib/data';
import { formatDate } from '@/lib/formatDate';

export const metadata = {
  title: 'RTI Library - Contractor Karma',
  description: 'Archive of all RTI applications filed for road infrastructure data. Track filing status and responses.',
};

const statusColors: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-700',
  filed: 'bg-blue-100 text-blue-700',
  responseReceived: 'bg-green-100 text-green-700',
  appeal: 'bg-yellow-100 text-yellow-700',
  awaitingResponse: 'bg-blue-100 text-blue-700',
};

const statusLabels: Record<string, string> = {
  draft: 'Draft',
  filed: 'Filed',
  responseReceived: 'Response Received',
  appeal: 'Under Appeal',
  awaitingResponse: 'Awaiting Response',
};

export default function RtiLibraryPage() {
  const applications = getRtiApplications();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">RTI Library</h1>
      <p className="text-sm text-muted-foreground mb-6">
        All Right to Information applications filed for road infrastructure
        data. Each response contributes to the platform&apos;s dataset.
      </p>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Total Applications</p>
          <p className="text-2xl font-bold">{applications.length}</p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Responses Received</p>
          <p className="text-2xl font-bold text-green-600">
            {
              applications.filter((a: any) => a.status === 'responseReceived')
                .length
            }
          </p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Awaiting Response</p>
          <p className="text-2xl font-bold text-blue-600">
            {applications.filter((a: any) =>
              a.status === 'filed' || a.status === 'awaitingResponse'
            ).length}
          </p>
        </div>
        <div className="border rounded-lg p-4">
          <p className="text-xs text-muted-foreground">Under Appeal</p>
          <p className="text-2xl font-bold text-yellow-600">
            {applications.filter((a: any) => a.status === 'appeal').length}
          </p>
        </div>
      </div>

      {/* Applications List */}
      <div className="space-y-3">
        {applications.map((app: any) => (
          <div
            key={String(app.rtiId)}
            className="border rounded-lg px-4 py-4"
          >
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <div>
                <p className="text-sm font-medium">
                  {String(app.subject || app.description || 'RTI Application')}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  RTI ID: {String(app.rtiId)}
                  {app.authority && ` | Authority: ${String(app.authority)}`}
                </p>
              </div>
              <span
                className={`text-xs px-2 py-1 rounded ${
                  statusColors[String(app.status)] || 'bg-gray-100 text-gray-700'
                }`}
              >
                {statusLabels[String(app.status)] || String(app.status)}
              </span>
            </div>
            <div className="flex gap-4 mt-2 text-xs text-muted-foreground">
              {(app.filedDate || app.filingDate) && (
                <span>Filed: {formatDate(String(app.filedDate || app.filingDate))}</span>
              )}
              {app.responseDate && (
                <span>Response: {formatDate(String(app.responseDate))}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
