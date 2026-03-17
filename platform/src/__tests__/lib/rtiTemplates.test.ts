import { describe, it, expect } from 'vitest';
import { generateRtiTemplate } from '@/lib/rtiTemplates';
import type { RtiTemplateContext } from '@/lib/rtiTemplates';

describe('generateRtiTemplate', () => {
  const baseContext: RtiTemplateContext = {
    roadName: 'Haralur Road',
    roadId: 'blr-mhd-150-007',
    contractorName: 'M/s Metro Roads & Bridges',
    wardName: 'Bellandur',
    wardNumber: '150',
    jobCode: '150-22-000003',
    sanctionedCost: '12000000',
    actualPaid: '14400000',
  };

  it('generates a default template when no flagType specified', () => {
    const template = generateRtiTemplate({ roadName: 'Test Road' });
    expect(template.subject).toContain('Test Road');
    expect(template.body).toContain('Right to Information Act');
    expect(template.body).toContain('[YOUR NAME]');
    expect(template.authority).toBeTruthy();
    expect(template.tips.length).toBeGreaterThan(0);
  });

  it('generates a costOutlier template', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'costOutlier',
    });
    expect(template.subject).toContain('cost breakdown');
    expect(template.body).toContain('rate analysis');
    expect(template.body).toContain('tender document');
    expect(template.body).toContain('Haralur Road');
    expect(template.body).toContain('M/s Metro Roads');
  });

  it('generates a repeatFailure template', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'repeatFailure',
    });
    expect(template.subject).toContain('quality inspection');
    expect(template.body).toContain('resurfaced');
    expect(template.body).toContain('DLP');
  });

  it('generates a dlpSpending template', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'dlpSpending',
      dlpEndDate: '2028-06-15',
    });
    expect(template.subject).toContain('DLP');
    expect(template.body).toContain('warranty period');
    expect(template.body).toContain('2028-06-15');
  });

  it('generates a costOverrun template', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'costOverrun',
    });
    expect(template.subject).toContain('cost overrun');
    expect(template.body).toContain('sanctioned cost');
    expect(template.body).toContain('revised estimate');
  });

  it('generates a severeDelay template', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'severeDelay',
    });
    expect(template.subject).toContain('delay');
    expect(template.body).toContain('penalty');
    expect(template.body).toContain('extension of time');
  });

  it('generates a contractorDominance template', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'contractorDominance',
    });
    expect(template.subject).toContain('tender');
    expect(template.body).toContain('disproportionately');
    expect(template.body).toContain('bidding contractors');
  });

  it('includes placeholder fields in all templates', () => {
    const flagTypes = [
      'costOutlier',
      'repeatFailure',
      'dlpSpending',
      'costOverrun',
      'severeDelay',
      'contractorDominance',
      undefined,
    ];
    for (const flagType of flagTypes) {
      const template = generateRtiTemplate({ ...baseContext, flagType });
      expect(template.body).toContain('[YOUR NAME]');
      expect(template.body).toContain('[YOUR ADDRESS]');
      expect(template.body).toContain('[DATE]');
    }
  });

  it('formats rupees amounts correctly', () => {
    const template = generateRtiTemplate({
      ...baseContext,
      flagType: 'costOverrun',
      sanctionedCost: '12000000',
      actualPaid: '14400000',
    });
    expect(template.body).toContain('Rs.');
  });

  it('handles missing context gracefully', () => {
    const template = generateRtiTemplate({});
    expect(template.subject).toBeTruthy();
    expect(template.body).toBeTruthy();
    expect(template.body).toContain('[ROAD NAME]');
  });
});
