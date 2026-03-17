import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Contractor Karma - Civic Road Infrastructure Transparency',
  description:
    'Track road warranty status, contractor performance, and public spending using RTI data. Built for Bengaluru citizens.',
  openGraph: {
    title: 'Contractor Karma - Civic Road Infrastructure Transparency',
    description:
      'Track road warranty status, contractor performance, and public spending using RTI data.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <header className="border-b bg-white sticky top-0 z-50">
            <div className="container mx-auto px-4 h-14 flex items-center justify-between">
              <a href="/" className="font-bold text-lg">
                Contractor Karma
              </a>
              <nav className="hidden md:flex items-center gap-6 text-sm">
                <a href="/dlp/" className="hover:text-primary">
                  DLP Tracker
                </a>
                <a href="/red-flags/" className="hover:text-primary">
                  Red Flags
                </a>
                <a href="/data/" className="hover:text-primary">
                  Data
                </a>
                <a href="/rti-library/" className="hover:text-primary">
                  RTI Library
                </a>
                <a href="/about/" className="hover:text-primary">
                  About
                </a>
              </nav>
            </div>
          </header>
          <main className="flex-1">{children}</main>
          <footer className="border-t py-6 text-center text-sm text-muted-foreground">
            <div className="container mx-auto px-4">
              <p>
                Data sourced from official RTI responses under RTI Act, 2005.
                Presented as-is.{' '}
                <a href="/about/" className="underline">
                  Methodology
                </a>
              </p>
              <p className="mt-1">
                Open source on{' '}
                <a
                  href="https://github.com"
                  className="underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  GitHub
                </a>
                . Code: MIT. Data: ODbL.
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
