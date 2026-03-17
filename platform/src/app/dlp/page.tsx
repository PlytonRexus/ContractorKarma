'use client';

import { useState, useEffect } from 'react';
import { DlpBadge } from '@/components/road/DlpBadge';
import { DlpLegend } from '@/components/map/DlpOverlay';
import type { DlpStatus } from '@/types/road';

interface DlpEntry {
  roadId: string;
  roadName: string;
  dlpStatus: DlpStatus;
  dlpEnd: string | null;
  contractor: string | null;
  contractorId: string | null;
  wardName?: string;
}

export default function DlpTrackerPage() {
  const [roads, setRoads] = useState<DlpEntry[]>([]);
  const [filter, setFilter] = useState<'all' | DlpStatus>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';
        const res = await fetch(`${basePath}/api/dlp-all.json`);
        if (res.ok) {
          const data = await res.json();
          setRoads(data);
        }
      } catch {
        // Data not available
      }
    };
    loadData();
  }, []);

  const filtered = roads
    .filter((r) => filter === 'all' || r.dlpStatus === filter)
    .filter(
      (r) =>
        !searchQuery ||
        r.roadName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (r.contractor &&
          r.contractor.toLowerCase().includes(searchQuery.toLowerCase()))
    );

  const counts = {
    all: roads.length,
    active: roads.filter((r) => r.dlpStatus === 'active').length,
    expiringSoon: roads.filter((r) => r.dlpStatus === 'expiringSoon').length,
    expired: roads.filter((r) => r.dlpStatus === 'expired').length,
    unknown: roads.filter((r) => r.dlpStatus === 'unknown').length,
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">DLP Warranty Tracker</h1>
      <p className="text-sm text-muted-foreground mb-4">
        Check which roads are under Defect Liability Period (warranty). If a
        road under warranty has defects, the contractor must repair it at their
        cost.
      </p>

      <DlpLegend className="mb-4" />

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {(
          [
            ['all', 'All'],
            ['active', 'Under Warranty'],
            ['expiringSoon', 'Expiring Soon'],
            ['expired', 'Expired'],
          ] as [string, string][]
        ).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setFilter(key as 'all' | DlpStatus)}
            className={`px-3 py-1.5 text-sm rounded-lg border ${
              filter === key
                ? 'bg-primary text-primary-foreground'
                : 'hover:bg-accent'
            }`}
          >
            {label} ({counts[key as keyof typeof counts]})
          </button>
        ))}
      </div>

      {/* Search */}
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Filter by road name or contractor..."
        className="w-full md:w-80 px-3 py-2 border rounded-lg text-sm mb-4"
      />

      {/* Results */}
      <div className="space-y-2">
        {filtered.map((road) => (
          <a
            key={road.roadId}
            href={`/road/bengaluru/${road.roadId}/`}
            className="flex items-center justify-between border rounded-lg px-4 py-3 hover:bg-accent transition-colors"
          >
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{road.roadName}</p>
              <p className="text-xs text-muted-foreground">
                {road.contractor || 'Contractor N/A'}
                {road.wardName && ` | ${road.wardName}`}
              </p>
            </div>
            <DlpBadge dlpEndDate={road.dlpEnd} showDetails />
          </a>
        ))}
        {filtered.length === 0 && (
          <p className="text-sm text-muted-foreground py-4">
            No roads found matching your criteria.
          </p>
        )}
      </div>
    </div>
  );
}
