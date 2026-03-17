import { describe, it, expect } from 'vitest';
import { glossary, redFlagGlossaryKey } from '@/lib/glossary';

describe('glossary', () => {
  it('has entries for all key terms', () => {
    const expectedKeys = [
      'dlp',
      'costOutlier',
      'repeatFailure',
      'dlpSpending',
      'costOverrun',
      'severeDelay',
      'contractorDominance',
      'sanctionedCost',
      'actualPaid',
      'performanceScore',
    ];
    for (const key of expectedKeys) {
      expect(glossary[key]).toBeDefined();
      expect(glossary[key].term).toBeTruthy();
      expect(glossary[key].shortExplanation).toBeTruthy();
      expect(glossary[key].fullExplanation).toBeTruthy();
      expect(glossary[key].whatItMeans).toBeTruthy();
    }
  });

  it('has grade entries', () => {
    expect(glossary['gradeA']).toBeDefined();
    expect(glossary['gradeD']).toBeDefined();
    expect(glossary['gradeF']).toBeDefined();
  });

  it('maps red flag types to glossary keys', () => {
    expect(redFlagGlossaryKey['repeatFailure']).toBe('repeatFailure');
    expect(redFlagGlossaryKey['costOutlier']).toBe('costOutlier');
    expect(redFlagGlossaryKey['dlpSpending']).toBe('dlpSpending');
    expect(redFlagGlossaryKey['severeDelay']).toBe('severeDelay');
    expect(redFlagGlossaryKey['delayedCompletion']).toBe('severeDelay');
  });

  it('all glossary entries have non-empty fields', () => {
    for (const [key, entry] of Object.entries(glossary)) {
      expect(entry.term.length).toBeGreaterThan(0);
      expect(entry.shortExplanation.length).toBeGreaterThan(10);
      expect(entry.whatItMeans.length).toBeGreaterThan(10);
    }
  });
});
