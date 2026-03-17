import { SearchBar } from '@/components/common/SearchBar';

export const metadata = {
  title: 'Search - Contractor Karma',
  description: 'Search roads, contractors, and job codes in RTI road data.',
};

export default function SearchPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Search</h1>
      <SearchBar className="max-w-xl" />
      <p className="text-sm text-muted-foreground mt-4">
        Search by road name, contractor name, job code, or area name. Results
        appear as you type.
      </p>
    </div>
  );
}
