import Link from 'next/link';
import { bbmpContacts } from '@/lib/bbmpContacts';

interface CivicActionsProps {
  roadName?: string;
  roadId?: string;
  contractorName?: string;
  flagType?: string;
  wardName?: string;
  wardNumber?: string;
}

export function CivicActions({
  roadName,
  roadId,
  contractorName,
  flagType,
  wardName,
  wardNumber,
}: CivicActionsProps) {
  const rtiParams = new URLSearchParams();
  if (roadName) rtiParams.set('roadName', roadName);
  if (roadId) rtiParams.set('roadId', roadId);
  if (contractorName) rtiParams.set('contractorName', contractorName);
  if (flagType) rtiParams.set('flagType', flagType);
  if (wardName) rtiParams.set('wardName', wardName);
  if (wardNumber) rtiParams.set('wardNumber', wardNumber);

  const rtiUrl = `/rti-library/generate/?${rtiParams.toString()}`;
  const sahaaya = bbmpContacts.find((c) => c.type === 'portal');
  const controlRoom = bbmpContacts.find((c) => c.type === 'phone');

  return (
    <div className="border rounded-lg p-4">
      <h3 className="text-sm font-semibold mb-3">What You Can Do</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <Link
          href={rtiUrl}
          className="flex flex-col border rounded-lg p-3 hover:bg-accent transition-colors"
        >
          <span className="text-sm font-medium">File an RTI</span>
          <span className="text-xs text-muted-foreground mt-0.5">
            Generate a pre-filled RTI application to get official information about this issue.
          </span>
        </Link>

        {sahaaya && sahaaya.url && (
          <a
            href={sahaaya.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex flex-col border rounded-lg p-3 hover:bg-accent transition-colors"
          >
            <span className="text-sm font-medium">Complain to BBMP</span>
            <span className="text-xs text-muted-foreground mt-0.5">
              File a complaint on the BBMP Sahaaya grievance portal.
            </span>
          </a>
        )}

        {controlRoom && controlRoom.phone && (
          <a
            href={`tel:${controlRoom.phone}`}
            className="flex flex-col border rounded-lg p-3 hover:bg-accent transition-colors"
          >
            <span className="text-sm font-medium">Call BBMP Control Room</span>
            <span className="text-xs text-muted-foreground mt-0.5">
              {controlRoom.phone} -- for urgent road safety issues.
            </span>
          </a>
        )}

        <div className="flex flex-col border rounded-lg p-3">
          <span className="text-sm font-medium">Share with Community</span>
          <span className="text-xs text-muted-foreground mt-0.5">
            Share this finding with your RWA, local media, or civic forums to build awareness.
          </span>
        </div>
      </div>
    </div>
  );
}
