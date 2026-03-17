import { SearchEntry } from './data';

/**
 * Client-side search using simple substring matching.
 * For MVP, this provides fast search without loading the full FlexSearch library.
 * Can be upgraded to FlexSearch later for fuzzy matching.
 */
export function searchEntries(
  entries: SearchEntry[],
  query: string,
  limit: number = 20
): SearchEntry[] {
  if (!query || query.trim().length === 0) return [];

  const normalizedQuery = query.toLowerCase().trim();
  const terms = normalizedQuery.split(/\s+/);

  const scored = entries
    .map((entry) => {
      const titleLower = entry.title.toLowerCase();
      const subtitleLower = entry.subtitle.toLowerCase();
      let score = 0;

      // Exact match in title
      if (titleLower === normalizedQuery) score += 100;
      // Title starts with query
      else if (titleLower.startsWith(normalizedQuery)) score += 80;
      // Title contains query
      else if (titleLower.includes(normalizedQuery)) score += 60;

      // All terms match somewhere
      const allTermsMatch = terms.every(
        (term) => titleLower.includes(term) || subtitleLower.includes(term)
      );
      if (allTermsMatch) score += 40;

      // Individual term matches in title
      for (const term of terms) {
        if (titleLower.includes(term)) score += 10;
        if (subtitleLower.includes(term)) score += 5;
      }

      // ID/jobCode exact match
      if (entry.id.toLowerCase() === normalizedQuery) score += 90;

      return { entry, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  return scored.map((item) => item.entry);
}
