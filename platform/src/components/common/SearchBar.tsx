'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { searchEntries } from '@/lib/search';
import { SearchEntry } from '@/lib/data';

interface SearchBarProps {
  placeholder?: string;
  className?: string;
}

export function SearchBar({
  placeholder = 'Search roads, contractors, or job codes...',
  className = '',
}: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchEntry[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [searchIndex, setSearchIndex] = useState<SearchEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loadIndex = async () => {
      try {
        setLoading(true);
        const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';
        const res = await fetch(`${basePath}/api/search-index.json`);
        if (res.ok) {
          const data = await res.json();
          setSearchIndex(data);
        }
      } catch {
        // Search index not available
      } finally {
        setLoading(false);
      }
    };
    loadIndex();
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = useCallback(
    (value: string) => {
      setQuery(value);
      if (value.trim().length < 2) {
        setResults([]);
        setIsOpen(false);
        return;
      }
      const matches = searchEntries(searchIndex, value, 10);
      setResults(matches);
      setIsOpen(matches.length > 0);
    },
    [searchIndex]
  );

  const typeIcons: Record<string, string> = {
    road: 'R',
    contractor: 'C',
    work: 'W',
  };

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      <input
        type="text"
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        onFocus={() => results.length > 0 && setIsOpen(true)}
        placeholder={placeholder}
        className="w-full px-4 py-3 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        aria-label="Search"
      />
      {loading && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
          Loading...
        </div>
      )}

      {isOpen && results.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg max-h-80 overflow-y-auto z-50">
          {results.map((result) => (
            <a
              key={`${result.type}-${result.id}`}
              href={result.url}
              className="flex items-center gap-3 px-4 py-3 hover:bg-accent border-b last:border-b-0"
            >
              <span className="w-6 h-6 rounded bg-secondary text-xs font-medium flex items-center justify-center">
                {typeIcons[result.type] || '?'}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{result.title}</p>
                <p className="text-xs text-muted-foreground truncate">
                  {result.subtitle}
                </p>
              </div>
            </a>
          ))}
        </div>
      )}

      {isOpen && query.trim().length >= 2 && results.length === 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg p-4 z-50">
          <p className="text-sm text-muted-foreground">
            No results found for &quot;{query}&quot;
          </p>
        </div>
      )}
    </div>
  );
}
