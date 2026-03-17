import { describe, it, expect } from 'vitest';
import { calculateDlpStatus, getExpectedDlpYears } from '@/lib/dlpCalculator';

describe('calculateDlpStatus', () => {
  const refDate = new Date('2026-03-17');

  it('returns active for future end date', () => {
    const result = calculateDlpStatus('2028-06-15', refDate);
    expect(result.status).toBe('active');
    expect(result.label).toBe('Under Warranty');
    expect(result.daysRemaining).toBeGreaterThan(180);
  });

  it('returns expired for past end date', () => {
    const result = calculateDlpStatus('2025-01-10', refDate);
    expect(result.status).toBe('expired');
    expect(result.label).toBe('Warranty Expired');
    expect(result.daysRemaining).toBeLessThan(0);
  });

  it('returns expiringSoon for date within 6 months', () => {
    const result = calculateDlpStatus('2026-07-01', refDate);
    expect(result.status).toBe('expiringSoon');
    expect(result.label).toBe('Expiring Soon');
    expect(result.daysRemaining).toBeGreaterThan(0);
    expect(result.daysRemaining).toBeLessThanOrEqual(180);
  });

  it('returns unknown when date is null', () => {
    const result = calculateDlpStatus(null);
    expect(result.status).toBe('unknown');
    expect(result.label).toBe('Unknown');
    expect(result.daysRemaining).toBeNull();
  });

  it('returns unknown when date is undefined', () => {
    const result = calculateDlpStatus(undefined);
    expect(result.status).toBe('unknown');
  });

  it('returns unknown for invalid date string', () => {
    const result = calculateDlpStatus('not-a-date');
    expect(result.status).toBe('unknown');
    expect(result.label).toBe('Invalid date');
  });

  it('returns active for date far in the future', () => {
    const result = calculateDlpStatus('2035-12-31', refDate);
    expect(result.status).toBe('active');
    expect(result.daysRemaining).toBeGreaterThan(365 * 9);
  });

  it('uses current date when no reference date provided', () => {
    // A date far in the future should always be active
    const result = calculateDlpStatus('2099-01-01');
    expect(result.status).toBe('active');
  });
});

describe('getExpectedDlpYears', () => {
  it('returns 3 for asphalt', () => {
    expect(getExpectedDlpYears('asphalt')).toBe(3);
  });

  it('returns 5 for concrete', () => {
    expect(getExpectedDlpYears('concrete')).toBe(5);
  });

  it('returns 10 for whiteTopping', () => {
    expect(getExpectedDlpYears('whiteTopping')).toBe(10);
  });

  it('returns 3 for unknown type', () => {
    expect(getExpectedDlpYears('gravel')).toBe(3);
  });
});
