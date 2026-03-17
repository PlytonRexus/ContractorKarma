/**
 * Format a number as Indian currency (INR) with lakhs/crores notation.
 */
export function formatCurrency(amount: number | null | undefined): string {
  if (amount == null) return 'N/A';
  if (amount < 0) return `-${formatCurrency(-amount)}`;
  if (amount === 0) return '0';

  if (amount >= 10000000) {
    const crores = amount / 10000000;
    return `${crores.toFixed(crores >= 10 ? 1 : 2)} Cr`;
  }
  if (amount >= 100000) {
    const lakhs = amount / 100000;
    return `${lakhs.toFixed(lakhs >= 10 ? 1 : 2)} L`;
  }
  if (amount >= 1000) {
    const thousands = amount / 1000;
    return `${thousands.toFixed(thousands >= 10 ? 0 : 1)}K`;
  }
  return amount.toFixed(0);
}

/**
 * Format a number as full INR with commas (Indian numbering system).
 */
export function formatCurrencyFull(amount: number | null | undefined): string {
  if (amount == null) return 'N/A';
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
}
