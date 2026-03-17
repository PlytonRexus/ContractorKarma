export const metadata = {
  title: 'About - Contractor Karma',
  description: 'How Contractor Karma works: methodology, data sources, DLP calculation, and how to contribute.',
};

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <h1 className="text-2xl font-bold mb-6">About Contractor Karma</h1>

      <div className="prose prose-sm max-w-none space-y-6">
        <section>
          <h2 className="text-lg font-semibold mb-2">What is this?</h2>
          <p className="text-sm text-muted-foreground">
            Contractor Karma is a civic transparency platform that transforms raw RTI
            (Right to Information) disclosures into structured, queryable
            intelligence about road infrastructure. It enables citizens to check
            warranty status, identify underperforming contractors, and trace
            public spending to specific officials.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">How does it work?</h2>
          <p className="text-sm text-muted-foreground">
            We file RTI applications to municipal bodies requesting structured
            data about road works: job codes, contractor names, costs,
            completion dates, and warranty periods. The responses are processed
            through a data pipeline that normalizes, validates, and generates
            the JSON files that power this site.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">
            Defect Liability Period (DLP)
          </h2>
          <p className="text-sm text-muted-foreground mb-2">
            The DLP is the warranty period after road construction. During this
            period, the contractor is liable for any defects and must repair
            them at their own cost:
          </p>
          <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
            <li>
              <strong>Asphalt roads:</strong> 3 years
            </li>
            <li>
              <strong>Concrete roads:</strong> 5 years
            </li>
            <li>
              <strong>White-topped roads:</strong> 10 years
            </li>
          </ul>
          <p className="text-sm text-muted-foreground mt-2">
            If a road develops potholes or other defects during the DLP, the
            municipality should not spend public money on repairs. Instead, the
            contractor must fix it for free.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">Performance Grading</h2>
          <p className="text-sm text-muted-foreground mb-2">
            Contractors are graded A through F based on a composite score:
          </p>
          <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
            <li>On-time completion rate: 40% weight</li>
            <li>DLP compliance (no violations): 40% weight</li>
            <li>Cost efficiency (cost-per-km vs median): 20% weight</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">Red Flags</h2>
          <p className="text-sm text-muted-foreground mb-2">
            The platform automatically detects anomalies:
          </p>
          <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
            <li>Road resurfaced within 2 years of previous work</li>
            <li>Public money spent on road under DLP</li>
            <li>Cost-per-km more than 2x the median for same work type</li>
            <li>
              Same contractor wins more than 50% of works in one ward
            </li>
            <li>Completion more than 6 months past deadline</li>
            <li>Actual paid exceeds 1.2x sanctioned cost</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">Data Sources</h2>
          <p className="text-sm text-muted-foreground">
            Every data point on this platform is traceable to a specific RTI
            application and response. RTI IDs are included in every work record.
            The raw RTI responses are archived in the open-source repository.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">Technology</h2>
          <p className="text-sm text-muted-foreground">
            Contractor Karma is a fully static site with zero server costs. It is built
            with Next.js (static export), deployed on GitHub Pages, with data
            served via jsDelivr CDN. The data pipeline is written in Python.
            The entire codebase and data are open source.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">Contributing</h2>
          <p className="text-sm text-muted-foreground">
            This project is open source. You can contribute by:
          </p>
          <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
            <li>Filing RTI applications for your ward or city</li>
            <li>Submitting data corrections via GitHub Issues</li>
            <li>Contributing code improvements via Pull Requests</li>
            <li>Sharing the platform with your community</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-2">Legal</h2>
          <p className="text-sm text-muted-foreground">
            All data is sourced from official RTI responses under the Right to
            Information Act, 2005. Data is presented as-is from government
            records. This platform is a conduit, not an originator of data.
            Code is licensed under MIT. Data is licensed under Open Database
            License (ODbL).
          </p>
        </section>
      </div>
    </div>
  );
}
