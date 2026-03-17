export interface CostAnalysis {
  costPerKm: number;
  isOutlier: boolean;
  medianCostPerKm: number | null;
  deviationRatio: number | null;
}

/**
 * Calculate cost per km for a road work.
 */
export function calculateCostPerKm(
  cost: number | null | undefined,
  lengthKm: number | null | undefined
): number | null {
  if (cost == null || lengthKm == null || lengthKm <= 0) return null;
  return Math.round(cost / lengthKm);
}

/**
 * Calculate median of an array of numbers.
 */
export function median(values: number[]): number | null {
  if (values.length === 0) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 0) {
    return (sorted[mid - 1] + sorted[mid]) / 2;
  }
  return sorted[mid];
}

/**
 * Analyze cost per km relative to other works.
 * Flags as outlier if cost exceeds 2x the median.
 */
export function analyzeCostPerKm(
  costPerKm: number,
  allCostsPerKm: number[]
): CostAnalysis {
  const med = median(allCostsPerKm);
  const deviationRatio = med != null && med > 0 ? costPerKm / med : null;
  const isOutlier = deviationRatio != null && deviationRatio > 2;

  return {
    costPerKm,
    isOutlier,
    medianCostPerKm: med,
    deviationRatio,
  };
}
