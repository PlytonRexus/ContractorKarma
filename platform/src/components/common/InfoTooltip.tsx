'use client';

import { useState, useCallback } from 'react';
import * as Tooltip from '@radix-ui/react-tooltip';
import { glossary } from '@/lib/glossary';

interface InfoTooltipProps {
  glossaryKey: string;
  children?: React.ReactNode;
}

export function InfoTooltip({ glossaryKey, children }: InfoTooltipProps) {
  const entry = glossary[glossaryKey];
  if (!entry) {
    return <>{children}</>;
  }

  const label = children || entry.term;

  return (
    <Tooltip.Provider delayDuration={200}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <span
            className="border-b border-dashed border-muted-foreground/50 cursor-help inline-flex items-center gap-0.5"
          >
            {label}
            <span className="text-[10px] text-muted-foreground align-super">[?]</span>
          </span>
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content
            className="z-50 max-w-xs rounded-lg border bg-popover px-3 py-2 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95"
            sideOffset={5}
          >
            <p className="font-medium text-xs mb-1">{entry.term}</p>
            <p className="text-xs text-muted-foreground">{entry.shortExplanation}</p>
            <Tooltip.Arrow className="fill-popover" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
}
