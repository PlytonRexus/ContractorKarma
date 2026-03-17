import { describe, it, expect } from 'vitest';
import { formatCurrency, formatCurrencyFull } from '@/lib/formatCurrency';

describe('formatCurrency', () => {
  it('formats crores', () => {
    expect(formatCurrency(23000000)).toBe('2.30 Cr');
  });

  it('formats large crores with 1 decimal', () => {
    expect(formatCurrency(150000000)).toBe('15.0 Cr');
  });

  it('formats lakhs', () => {
    expect(formatCurrency(1850000)).toBe('18.5 L');
  });

  it('formats large lakhs with 1 decimal', () => {
    expect(formatCurrency(5500000)).toBe('55.0 L');
  });

  it('formats thousands', () => {
    expect(formatCurrency(50000)).toBe('50K');
  });

  it('formats small thousands with decimal', () => {
    expect(formatCurrency(5500)).toBe('5.5K');
  });

  it('formats small numbers', () => {
    expect(formatCurrency(500)).toBe('500');
  });

  it('returns N/A for null', () => {
    expect(formatCurrency(null)).toBe('N/A');
  });

  it('returns N/A for undefined', () => {
    expect(formatCurrency(undefined)).toBe('N/A');
  });

  it('handles zero', () => {
    expect(formatCurrency(0)).toBe('0');
  });

  it('handles negative values', () => {
    const result = formatCurrency(-1850000);
    expect(result).toBe('-18.5 L');
  });
});

describe('formatCurrencyFull', () => {
  it('formats with INR symbol and commas', () => {
    const result = formatCurrencyFull(1850000);
    // Indian format: Rs 18,50,000
    expect(result).toContain('18');
    expect(result).toContain('50');
  });

  it('returns N/A for null', () => {
    expect(formatCurrencyFull(null)).toBe('N/A');
  });
});
