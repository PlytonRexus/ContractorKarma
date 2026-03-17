'use client';

import { useEffect, useRef, useState } from 'react';

interface RoadMapProps {
  center?: [number, number];
  zoom?: number;
  className?: string;
  geojsonUrl?: string;
}

/**
 * Lazy-loaded MapLibre map component.
 * Shows a placeholder until the map library is loaded.
 * In static export mode, the map is client-side only.
 */
export function RoadMap({
  center = [77.6446, 12.9352], // Bellandur, Bengaluru
  zoom = 13,
  className = 'w-full h-96',
  geojsonUrl,
}: RoadMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    // MapLibre GL JS will be integrated when GeoJSON data is available.
    // For now, show a placeholder with an OpenStreetMap embed.
    setLoaded(true);
  }, []);

  if (!loaded) {
    return (
      <div className={`${className} bg-muted animate-pulse rounded-lg flex items-center justify-center`}>
        <p className="text-sm text-muted-foreground">Loading map...</p>
      </div>
    );
  }

  return (
    <div className={`${className} rounded-lg overflow-hidden border`}>
      <iframe
        title="Road Map"
        width="100%"
        height="100%"
        style={{ border: 0 }}
        loading="lazy"
        src={`https://www.openstreetmap.org/export/embed.html?bbox=${center[0] - 0.02},${center[1] - 0.015},${center[0] + 0.02},${center[1] + 0.015}&layer=mapnik`}
      />
    </div>
  );
}
