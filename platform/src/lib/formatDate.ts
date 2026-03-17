/**
 * Format an ISO date string for display.
 */
export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return 'N/A';
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

/**
 * Format a date as relative time (e.g., "3 months remaining", "expired 1 year ago").
 */
export function formatRelativeDate(dateStr: string | null | undefined): string {
  if (!dateStr) return 'Unknown';
  try {
    const target = new Date(dateStr);
    if (isNaN(target.getTime())) return dateStr;
    const now = new Date();
    const diffMs = target.getTime() - now.getTime();
    const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays > 365) {
      const years = Math.floor(diffDays / 365);
      return `${years} year${years > 1 ? 's' : ''} remaining`;
    }
    if (diffDays > 30) {
      const months = Math.floor(diffDays / 30);
      return `${months} month${months > 1 ? 's' : ''} remaining`;
    }
    if (diffDays > 0) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''} remaining`;
    }
    if (diffDays > -30) {
      const days = Math.abs(diffDays);
      return `expired ${days} day${days > 1 ? 's' : ''} ago`;
    }
    if (diffDays > -365) {
      const months = Math.floor(Math.abs(diffDays) / 30);
      return `expired ${months} month${months > 1 ? 's' : ''} ago`;
    }
    const years = Math.floor(Math.abs(diffDays) / 365);
    return `expired ${years} year${years > 1 ? 's' : ''} ago`;
  } catch {
    return 'Unknown';
  }
}
