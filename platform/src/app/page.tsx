import Link from 'next/link';
import { getStats, getRedFlags, getAllWards } from '@/lib/data';
import { formatCurrency } from '@/lib/formatCurrency';
import { StatCard } from '@/components/common/StatCard';
import { SearchBar } from '@/components/common/SearchBar';

export default function HomePage() {
  const stats = getStats();
  const redFlags = getRedFlags().slice(0, 5);
  const wards = getAllWards();

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <div className="text-center max-w-2xl mx-auto mb-8">
        <h1 className="text-3xl font-bold mb-2">Contractor Karma</h1>
        <p className="text-muted-foreground mb-6">
          Track road warranty status, contractor performance, and public
          spending -- powered by RTI data from Bengaluru.
        </p>
        <SearchBar className="max-w-lg mx-auto" />
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <StatCard
            title="Roads Tracked"
            value={stats.totalRoads}
            subtitle={`across ${stats.totalWards} wards`}
          />
          <StatCard
            title="Under Warranty"
            value={stats.dlp.active}
            subtitle={`${stats.dlp.expiringSoon} expiring soon`}
          />
          <StatCard
            title="Public Spending Tracked"
            value={formatCurrency(stats.financials.totalSanctionedCost)}
            subtitle={`${stats.totalContractors} contractors`}
          />
        </div>
      )}

      {/* Quick Browse */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div>
          <h2 className="text-lg font-semibold mb-3">Browse by Ward</h2>
          <div className="space-y-2">
            {wards.map(({ cityId, zoneId, wardId, ward }) => (
              <Link
                key={wardId}
                href={`/ward/${cityId}/${zoneId}/${wardId}/`}
                className="block border rounded-lg px-4 py-3 hover:bg-accent transition-colors"
              >
                <span className="font-medium text-sm">{ward.wardName}</span>
                <span className="text-xs text-muted-foreground ml-2">
                  Ward {ward.wardNumber}
                </span>
              </Link>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-3">Recent Red Flags</h2>
          {redFlags.length > 0 ? (
            <div className="space-y-2">
              {redFlags.map((flag) => (
                <div
                  key={flag.flagId}
                  className="border rounded-lg px-4 py-3 border-l-4 border-l-red-400"
                >
                  <p className="text-sm font-medium">{flag.description}</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {flag.roadName && `${flag.roadName} | `}
                    {flag.severity} severity
                  </p>
                </div>
              ))}
              <Link
                href="/red-flags/"
                className="text-sm text-primary hover:underline"
              >
                View all red flags
              </Link>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No red flags detected yet.
            </p>
          )}
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Link
          href="/dlp/"
          className="border rounded-lg p-4 text-center hover:bg-accent transition-colors"
        >
          <p className="font-medium text-sm">DLP Tracker</p>
          <p className="text-xs text-muted-foreground mt-1">
            Warranty status lookup
          </p>
        </Link>
        <Link
          href="/contractor/"
          className="border rounded-lg p-4 text-center hover:bg-accent transition-colors"
        >
          <p className="font-medium text-sm">Contractors</p>
          <p className="text-xs text-muted-foreground mt-1">
            Performance rankings
          </p>
        </Link>
        <Link
          href="/data/"
          className="border rounded-lg p-4 text-center hover:bg-accent transition-colors"
        >
          <p className="font-medium text-sm">Data Explorer</p>
          <p className="text-xs text-muted-foreground mt-1">
            Browse and download
          </p>
        </Link>
        <Link
          href="/rti-library/"
          className="border rounded-lg p-4 text-center hover:bg-accent transition-colors"
        >
          <p className="font-medium text-sm">RTI Library</p>
          <p className="text-xs text-muted-foreground mt-1">
            Applications filed
          </p>
        </Link>
      </div>
    </div>
  );
}
