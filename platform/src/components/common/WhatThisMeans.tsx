import { glossary, redFlagGlossaryKey } from '@/lib/glossary';

interface WhatThisMeansProps {
  flagType: string;
}

export function WhatThisMeans({ flagType }: WhatThisMeansProps) {
  const glossaryKey = redFlagGlossaryKey[flagType] || flagType;
  const entry = glossary[glossaryKey];
  if (!entry) return null;

  return (
    <div className="mt-2 rounded-md bg-blue-50 border border-blue-200 px-3 py-2">
      <p className="text-xs font-semibold text-blue-800 mb-0.5">
        What this means for you
      </p>
      <p className="text-xs text-blue-700">{entry.whatItMeans}</p>
    </div>
  );
}
