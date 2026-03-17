import { describe, it, expect } from 'vitest';
import { calculateCostPerKm, median, analyzeCostPerKm } from '@/lib/costPerKm';

describe('calculateCostPerKm', () => {
  it('calculates correctly for normal values', () => {
    expect(calculateCostPerKm(1800000, 0.45)).toBe(4000000);
  });

  it('returns null when cost is null', () => {
    expect(calculateCostPerKm(null, 0.5)).toBeNull();
  });

  it('returns null when length is null', () => {
    expect(calculateCostPerKm(1800000, null)).toBeNull();
  });

  it('returns null when length is zero', () => {
    expect(calculateCostPerKm(1800000, 0)).toBeNull();
  });

  it('returns null when length is negative', () => {
    expect(calculateCostPerKm(1800000, -0.5)).toBeNull();
  });

  it('rounds to nearest integer', () => {
    const result = calculateCostPerKm(1000000, 0.3);
    expect(result).toBe(3333333);
  });
});

describe('median', () => {
  it('returns null for empty array', () => {
    expect(median([])).toBeNull();
  });

  it('returns the single value for array of one', () => {
    expect(median([5])).toBe(5);
  });

  it('returns middle value for odd-length array', () => {
    expect(median([1, 3, 5])).toBe(3);
  });

  it('returns average of middle values for even-length array', () => {
    expect(median([1, 2, 3, 4])).toBe(2.5);
  });

  it('handles unsorted input', () => {
    expect(median([5, 1, 3])).toBe(3);
  });
});

describe('analyzeCostPerKm', () => {
  const allCosts = [3000000, 3500000, 4000000, 4500000, 5000000];

  it('identifies non-outlier', () => {
    const result = analyzeCostPerKm(4000000, allCosts);
    expect(result.isOutlier).toBe(false);
    expect(result.costPerKm).toBe(4000000);
    expect(result.medianCostPerKm).toBe(4000000);
  });

  it('identifies outlier above 2x median', () => {
    const result = analyzeCostPerKm(9000000, allCosts);
    expect(result.isOutlier).toBe(true);
    expect(result.deviationRatio).toBeGreaterThan(2);
  });

  it('does not flag value at exactly 2x as outlier', () => {
    const result = analyzeCostPerKm(8000000, allCosts);
    expect(result.isOutlier).toBe(false);
    expect(result.deviationRatio).toBe(2);
  });
});
