import { bbmpContacts, rtiGuidance } from '@/lib/bbmpContacts';

interface BbmpContactCardProps {
  showRtiInfo?: boolean;
}

export function BbmpContactCard({ showRtiInfo = true }: BbmpContactCardProps) {
  return (
    <div className="border rounded-lg p-4">
      <h3 className="text-sm font-semibold mb-3">BBMP Contact Information</h3>
      <div className="space-y-3">
        {bbmpContacts.map((contact) => (
          <div key={contact.name} className="border-b last:border-b-0 pb-2 last:pb-0">
            <p className="text-sm font-medium">{contact.name}</p>
            <p className="text-xs text-muted-foreground mt-0.5">
              {contact.description}
            </p>
            <div className="flex flex-wrap gap-3 mt-1">
              {contact.phone && (
                <a
                  href={`tel:${contact.phone}`}
                  className="text-xs text-blue-600 hover:underline"
                >
                  {contact.phone}
                </a>
              )}
              {contact.email && (
                <a
                  href={`mailto:${contact.email}`}
                  className="text-xs text-blue-600 hover:underline"
                >
                  {contact.email}
                </a>
              )}
              {contact.url && (
                <a
                  href={contact.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-600 hover:underline"
                >
                  Visit Portal
                </a>
              )}
            </div>
          </div>
        ))}
      </div>

      {showRtiInfo && (
        <div className="mt-4 pt-3 border-t">
          <h4 className="text-xs font-semibold mb-2">RTI Filing Information</h4>
          <div className="space-y-1 text-xs text-muted-foreground">
            <p>
              <span className="font-medium">Fee:</span> {rtiGuidance.fee}
            </p>
            <p>
              <span className="font-medium">Response deadline:</span>{' '}
              {rtiGuidance.timeLimits.responseDeadline}
            </p>
            <p>
              <span className="font-medium">First appeal:</span>{' '}
              {rtiGuidance.timeLimits.firstAppeal}
            </p>
            <a
              href={rtiGuidance.portalUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-1 text-blue-600 hover:underline"
            >
              File RTI Online
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
