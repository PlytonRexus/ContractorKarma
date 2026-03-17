import { getStats, getAllWards, getAllContractors } from '@/lib/data';

export const metadata = {
  title: 'Data Explorer - Contractor Karma',
  description: 'Browse and download raw RTI road infrastructure data in JSON and CSV formats.',
};

export default function DataPage() {
  const stats = getStats();
  const wards = getAllWards();
  const contractors = getAllContractors();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">Data Explorer</h1>
      <p className="text-sm text-muted-foreground mb-6">
        All data is sourced from official RTI responses under the RTI Act, 2005.
        Raw data files are available for download in JSON format.
      </p>

      {/* Data Summary */}
      <div className="border rounded-lg p-4 mb-8">
        <h2 className="font-semibold mb-2">Dataset Summary</h2>
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-muted-foreground">Total Roads</span>
              <p className="font-medium">{stats.totalRoads}</p>
            </div>
            <div>
              <span className="text-muted-foreground">Total Works</span>
              <p className="font-medium">{stats.totalWorks}</p>
            </div>
            <div>
              <span className="text-muted-foreground">Contractors</span>
              <p className="font-medium">{stats.totalContractors}</p>
            </div>
            <div>
              <span className="text-muted-foreground">Wards Covered</span>
              <p className="font-medium">{stats.totalWards}</p>
            </div>
          </div>
        )}
      </div>

      {/* Download Links */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-3">Download Data</h2>
        <div className="space-y-2">
          <h3 className="text-sm font-medium mt-4 mb-2">Ward Data</h3>
          {wards.map(({ cityId, zoneId, wardId, ward }) => (
            <div
              key={wardId}
              className="border rounded-lg px-4 py-3 flex items-center justify-between"
            >
              <div>
                <p className="text-sm font-medium">
                  {ward.wardName} (Ward {ward.wardNumber})
                </p>
                <p className="text-xs text-muted-foreground">
                  {zoneId} zone
                </p>
              </div>
              <div className="flex gap-2">
                <a
                  href={`/data/cities/${cityId}/zones/${zoneId}/wards/${wardId}/roads.json`}
                  className="text-xs px-2 py-1 border rounded hover:bg-accent"
                  download
                >
                  roads.json
                </a>
                <a
                  href={`/data/cities/${cityId}/zones/${zoneId}/wards/${wardId}/works.json`}
                  className="text-xs px-2 py-1 border rounded hover:bg-accent"
                  download
                >
                  works.json
                </a>
              </div>
            </div>
          ))}

          <h3 className="text-sm font-medium mt-4 mb-2">Contractors</h3>
          <div className="border rounded-lg px-4 py-3 flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">
                All Contractors ({contractors.length})
              </p>
              <p className="text-xs text-muted-foreground">
                Aggregated performance stats
              </p>
            </div>
            <a
              href="/data/contractors/index.json"
              className="text-xs px-2 py-1 border rounded hover:bg-accent"
              download
            >
              contractors.json
            </a>
          </div>

          <h3 className="text-sm font-medium mt-4 mb-2">Red Flags</h3>
          <div className="border rounded-lg px-4 py-3 flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">Anomaly Data</p>
              <p className="text-xs text-muted-foreground">
                Pre-computed red flags
              </p>
            </div>
            <a
              href="/data/red-flags/flags.json"
              className="text-xs px-2 py-1 border rounded hover:bg-accent"
              download
            >
              flags.json
            </a>
          </div>
        </div>
      </div>

      {/* License */}
      <div className="border rounded-lg p-4 bg-muted/50">
        <h2 className="font-semibold mb-2">Data License</h2>
        <p className="text-sm text-muted-foreground">
          Code is released under the MIT License. Data is released under the
          Open Database License (ODbL). You are free to share, modify, and use
          this data for any purpose with attribution.
        </p>
      </div>
    </div>
  );
}
