'use client';

import { Suspense, useState, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import { generateRtiTemplate } from '@/lib/rtiTemplates';
import type { RtiTemplateContext } from '@/lib/rtiTemplates';

function RtiGeneratorContent() {
  const searchParams = useSearchParams();

  const context: RtiTemplateContext = {
    roadName: searchParams.get('roadName') || undefined,
    roadId: searchParams.get('roadId') || undefined,
    contractorName: searchParams.get('contractorName') || undefined,
    flagType: searchParams.get('flagType') || undefined,
    jobCode: searchParams.get('jobCode') || undefined,
    wardName: searchParams.get('wardName') || undefined,
    wardNumber: searchParams.get('wardNumber') || undefined,
    sanctionedCost: searchParams.get('sanctionedCost') || undefined,
    actualPaid: searchParams.get('actualPaid') || undefined,
    dlpEndDate: searchParams.get('dlpEndDate') || undefined,
  };

  const template = generateRtiTemplate(context);
  const [body, setBody] = useState(template.body);
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(body);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback: select the textarea
      const textarea = document.querySelector('textarea');
      if (textarea) {
        textarea.select();
      }
    }
  }, [body]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">RTI Application Generator</h1>
      <p className="text-sm text-muted-foreground mb-6">
        This generates a pre-filled RTI application based on the road work data.
        Replace the placeholder fields marked in [BRACKETS] with your details before filing.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main letter */}
        <div className="lg:col-span-2">
          <div className="border rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold">
                Subject: {template.subject}
              </h2>
              <button
                onClick={handleCopy}
                className="px-3 py-1.5 text-xs border rounded-lg hover:bg-accent transition-colors"
              >
                {copied ? 'Copied!' : 'Copy to Clipboard'}
              </button>
            </div>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full min-h-[500px] p-3 text-sm font-mono border rounded-lg bg-muted/30 resize-y"
              spellCheck={false}
            />
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            You can edit the letter above. Replace all [BRACKETED] placeholders with your actual information.
          </p>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Filing info */}
          <div className="border rounded-lg p-4">
            <h3 className="text-sm font-semibold mb-2">How to File</h3>
            <div className="space-y-2 text-xs text-muted-foreground">
              <p>
                <span className="font-medium text-foreground">Online:</span>{' '}
                File at{' '}
                <a
                  href="https://rtionline.gov.in/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  rtionline.gov.in
                </a>
              </p>
              <p>
                <span className="font-medium text-foreground">By Post:</span>{' '}
                Send to {template.authority} with Rs. 10 fee (postal order / DD / court fee stamp).
              </p>
              <p>
                <span className="font-medium text-foreground">Fee:</span>{' '}
                Rs. 10 for State Government bodies.
              </p>
            </div>
          </div>

          {/* Tips */}
          <div className="border rounded-lg p-4">
            <h3 className="text-sm font-semibold mb-2">Tips</h3>
            <ul className="space-y-1.5">
              {template.tips.map((tip, i) => (
                <li key={i} className="text-xs text-muted-foreground flex gap-1.5">
                  <span className="text-muted-foreground/60 shrink-0">{i + 1}.</span>
                  <span>{tip}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Context info */}
          {(context.roadName || context.contractorName || context.flagType) && (
            <div className="border rounded-lg p-4">
              <h3 className="text-sm font-semibold mb-2">Context</h3>
              <div className="space-y-1 text-xs text-muted-foreground">
                {context.roadName && <p><span className="font-medium">Road:</span> {context.roadName}</p>}
                {context.contractorName && <p><span className="font-medium">Contractor:</span> {context.contractorName}</p>}
                {context.flagType && <p><span className="font-medium">Issue type:</span> {context.flagType}</p>}
                {context.wardName && <p><span className="font-medium">Ward:</span> {context.wardName}</p>}
                {context.jobCode && <p><span className="font-medium">Job code:</span> {context.jobCode}</p>}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function RtiGeneratorPage() {
  return (
    <Suspense
      fallback={
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-2xl font-bold mb-2">RTI Application Generator</h1>
          <div className="animate-pulse bg-muted h-96 rounded-lg" />
        </div>
      }
    >
      <RtiGeneratorContent />
    </Suspense>
  );
}
