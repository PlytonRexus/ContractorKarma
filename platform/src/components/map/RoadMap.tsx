'use client';

import { useEffect, useRef, useState } from 'react';
import type { DlpStatus } from '@/types/road';

interface RoadMarker {
  roadId: string;
  roadName: string;
  lat: number;
  lng: number;
  dlpStatus: DlpStatus;
  dlpEnd?: string | null;
}

interface WardBoundary {
  type: string;
  coordinates: number[][][];
}

interface RoadMapProps {
  center?: [number, number];
  zoom?: number;
  className?: string;
  roads?: RoadMarker[];
  wardBoundary?: WardBoundary;
  highlightRoadId?: string;
}

const dlpColors: Record<DlpStatus, string> = {
  active: '#16a34a',
  expiringSoon: '#ca8a04',
  expired: '#dc2626',
  unknown: '#9ca3af',
};

export function RoadMap({
  center = [12.9352, 77.6446],
  zoom = 14,
  className = 'w-full h-96',
  roads = [],
  wardBoundary,
  highlightRoadId,
}: RoadMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    let cancelled = false;

    (async () => {
      const L = (await import('leaflet')).default;

      // Load Leaflet CSS via link element to avoid TS module resolution issues
      if (!document.querySelector('link[href*="leaflet"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(link);
      }

      if (cancelled || !containerRef.current) return;

      const map = L.map(containerRef.current).setView(center, zoom);
      mapRef.current = map;

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
      }).addTo(map);

      // Ward boundary polygon
      if (wardBoundary) {
        // GeoJSON uses [lng, lat] but Leaflet uses [lat, lng]
        const latLngs = wardBoundary.coordinates[0].map(
          (coord: number[]) => [coord[1], coord[0]] as [number, number]
        );
        L.polygon(latLngs, {
          color: '#4f46e5',
          weight: 2,
          fillOpacity: 0.05,
          dashArray: '5, 5',
        }).addTo(map);
      }

      // Road markers
      for (const road of roads) {
        const color = dlpColors[road.dlpStatus] || dlpColors.unknown;
        const isHighlighted = road.roadId === highlightRoadId;

        const circle = L.circleMarker([road.lat, road.lng], {
          radius: isHighlighted ? 10 : 7,
          fillColor: color,
          color: isHighlighted ? '#1e1b4b' : color,
          weight: isHighlighted ? 3 : 1.5,
          opacity: 1,
          fillOpacity: 0.8,
        }).addTo(map);

        const statusLabel =
          road.dlpStatus === 'active'
            ? 'Under Warranty'
            : road.dlpStatus === 'expiringSoon'
            ? 'Warranty Expiring Soon'
            : road.dlpStatus === 'expired'
            ? 'Warranty Expired'
            : 'Status Unknown';

        circle.bindPopup(
          `<strong>${road.roadName}</strong><br/><span style="color:${color}">${statusLabel}</span>${
            road.dlpEnd ? `<br/>DLP ends: ${road.dlpEnd}` : ''
          }`
        );
      }

      setLoaded(true);
    })();

    return () => {
      cancelled = true;
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [center, zoom, roads, wardBoundary, highlightRoadId]);

  return (
    <div className={`${className} rounded-lg overflow-hidden border relative`}>
      <div ref={containerRef} className="w-full h-full" />
      {!loaded && (
        <div className="absolute inset-0 bg-muted animate-pulse flex items-center justify-center">
          <p className="text-sm text-muted-foreground">Loading map...</p>
        </div>
      )}
    </div>
  );
}
