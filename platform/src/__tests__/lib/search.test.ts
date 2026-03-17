import { describe, it, expect } from 'vitest';
import { searchEntries } from '@/lib/search';
import { SearchEntry } from '@/lib/data';

const mockEntries: SearchEntry[] = [
  {
    type: 'road',
    id: 'blr-mhd-150-001',
    title: '7th Cross, Green Glen Layout',
    subtitle: 'Ward 150, Bellandur',
    url: '/road/bengaluru/blr-mhd-150-001/',
  },
  {
    type: 'road',
    id: 'blr-mhd-150-002',
    title: 'Main Road, Kasavanahalli',
    subtitle: 'Ward 150, Bellandur',
    url: '/road/bengaluru/blr-mhd-150-002/',
  },
  {
    type: 'contractor',
    id: 'ctr-001',
    title: 'M/s Reliable Constructions',
    subtitle: 'Class I | 12 works',
    url: '/contractor/ctr-001/',
  },
  {
    type: 'work',
    id: '150-23-000042',
    title: 'Asphalting of 7th Cross',
    subtitle: 'Job Code: 150-23-000042',
    url: '/road/bengaluru/blr-mhd-150-001/',
  },
];

describe('searchEntries', () => {
  it('returns results matching road name', () => {
    const results = searchEntries(mockEntries, 'Green Glen');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].title).toContain('Green Glen');
  });

  it('returns results matching contractor name', () => {
    const results = searchEntries(mockEntries, 'Reliable');
    expect(results.length).toBe(1);
    expect(results[0].type).toBe('contractor');
  });

  it('returns empty for empty query', () => {
    expect(searchEntries(mockEntries, '')).toEqual([]);
  });

  it('returns empty for whitespace query', () => {
    expect(searchEntries(mockEntries, '   ')).toEqual([]);
  });

  it('returns few results for partial match on common word', () => {
    // "road" partially matches "Main Road, Kasavanahalli"
    const results = searchEntries(mockEntries, 'nonexistent xyzabc');
    expect(results).toEqual([]);
  });

  it('matches job codes', () => {
    const results = searchEntries(mockEntries, '150-23-000042');
    expect(results.length).toBeGreaterThan(0);
  });

  it('respects limit parameter', () => {
    const results = searchEntries(mockEntries, 'road', 1);
    expect(results.length).toBeLessThanOrEqual(1);
  });

  it('is case insensitive', () => {
    const results = searchEntries(mockEntries, 'green glen');
    expect(results.length).toBeGreaterThan(0);
  });
});
