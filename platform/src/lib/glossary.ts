export interface GlossaryEntry {
  term: string;
  shortExplanation: string;
  fullExplanation: string;
  whatItMeans: string;
}

export const glossary: Record<string, GlossaryEntry> = {
  dlp: {
    term: 'Defect Liability Period (DLP)',
    shortExplanation:
      'A warranty period after road work where the contractor must fix defects at their own cost.',
    fullExplanation:
      'After a road is built or resurfaced, the contractor is legally bound to maintain it for a set period -- 3 years for asphalt, 5 for concrete, 10 for white-topping. If potholes, cracks, or other defects appear during this period, the contractor must repair them at no cost to the public.',
    whatItMeans:
      'If your road has potholes and is still under warranty, the contractor is legally obligated to fix it for free. You can file a complaint with BBMP or an RTI to ask why repairs have not been done.',
  },
  gradeA: {
    term: 'Performance Grade A',
    shortExplanation:
      'Top-performing contractor with most works completed on time and minimal DLP violations.',
    fullExplanation:
      'Grade A is assigned to contractors scoring 85% or above on a composite metric that weighs on-time completion (50%), delay rate (30%), and DLP compliance (20%).',
    whatItMeans:
      'This contractor has a strong track record. Roads built by them are more likely to be completed on schedule and maintained properly during the warranty period.',
  },
  gradeB: {
    term: 'Performance Grade B',
    shortExplanation: 'Good performer with scores between 70-85%.',
    fullExplanation:
      'Grade B contractors score between 70% and 85%. They generally complete work on time but may have occasional delays or minor DLP issues.',
    whatItMeans:
      'A reasonably reliable contractor, though you may want to check if any of their roads in your area have had delays or warranty issues.',
  },
  gradeC: {
    term: 'Performance Grade C',
    shortExplanation: 'Average performer with scores between 55-70%.',
    fullExplanation:
      'Grade C indicates a contractor with noticeable delays or DLP compliance issues. Their composite score falls between 55% and 70%.',
    whatItMeans:
      'This contractor has a mixed record. Some of their works may have been delayed or had quality issues. Worth monitoring closely.',
  },
  gradeD: {
    term: 'Performance Grade D',
    shortExplanation:
      'Below-average performer with significant delays and DLP violations.',
    fullExplanation:
      'Grade D is assigned when the composite score falls between 40% and 55%. These contractors have multiple delayed works and/or DLP violations.',
    whatItMeans:
      'This contractor has a poor track record. If they are working on a road near you, pay extra attention to work quality and timelines. Consider filing an RTI to understand why they continue to receive contracts.',
  },
  gradeF: {
    term: 'Performance Grade F',
    shortExplanation:
      'Failing grade -- serious performance issues across multiple metrics.',
    fullExplanation:
      'Grade F means the contractor scores below 40%. This indicates systemic problems with delays, cost overruns, and DLP violations.',
    whatItMeans:
      'This contractor should arguably not be receiving new contracts. If you see them assigned to a road in your area, an RTI asking for their selection justification is warranted.',
  },
  costOutlier: {
    term: 'Cost Outlier',
    shortExplanation:
      'The cost of this work is significantly higher than the median for similar roads.',
    fullExplanation:
      'A cost outlier is flagged when a road work costs 40% or more above the zone median for the same road class and work type. This does not automatically mean corruption, but it warrants scrutiny -- the road may be wider, longer, or have genuine cost factors.',
    whatItMeans:
      'Public money may have been overspent on this road. You can file an RTI asking for the detailed cost breakdown, rate analysis, and tender documents to understand why the cost was higher than comparable roads.',
  },
  repeatFailure: {
    term: 'Repeat Failure',
    shortExplanation:
      'This road was resurfaced again within 2 years of the previous work.',
    fullExplanation:
      'A repeat failure is flagged when a road needs re-surfacing within 24 months of the previous work. This suggests the original work was of poor quality, or the DLP warranty was not enforced.',
    whatItMeans:
      'Your tax money was spent twice on the same road in a short period. The contractor who did the first work should have repaired it under warranty instead. You can ask via RTI why the DLP was not enforced and why fresh public funds were used.',
  },
  dlpSpending: {
    term: 'DLP Spending Violation',
    shortExplanation:
      'Public money was spent on repairs during the warranty period when the contractor should have paid.',
    fullExplanation:
      'When a road is under DLP warranty, any defect repairs are the contractor responsibility. If BBMP spends public money on repairs during this period, it means the warranty is not being enforced.',
    whatItMeans:
      'Your money was wasted. The contractor was supposed to fix this for free. File an RTI to ask why BBMP did not enforce the DLP warranty and whether the contractor was penalized.',
  },
  costOverrun: {
    term: 'Cost Overrun',
    shortExplanation:
      'The actual amount paid exceeded the originally sanctioned (approved) cost.',
    fullExplanation:
      'A cost overrun occurs when the final payment to the contractor exceeds the initially sanctioned budget. Small overruns (under 5%) can occur due to legitimate scope changes, but larger overruns need justification.',
    whatItMeans:
      'More money was spent than originally approved. You can file an RTI asking for the justification for the excess expenditure and whether proper approvals were obtained for the revised estimate.',
  },
  severeDelay: {
    term: 'Severe Delay',
    shortExplanation:
      'Work was completed more than 3 months past the stipulated deadline.',
    fullExplanation:
      'A severe delay is flagged when actual completion exceeds the stipulated date by more than 90 days. Contracts typically include penalty clauses for delays.',
    whatItMeans:
      'This road work took far longer than planned, causing extended inconvenience to residents. You can ask via RTI whether delay penalties were imposed on the contractor and what caused the delay.',
  },
  contractorDominance: {
    term: 'Contractor Dominance',
    shortExplanation:
      'One contractor holds a disproportionately large share of works in this area.',
    fullExplanation:
      'This flag is raised when a single contractor handles more than 40% of works in a ward. While not necessarily improper, concentrated allocation reduces competitive bidding benefits.',
    whatItMeans:
      'One contractor may have too much control over road works in your area. This could mean less competitive pricing. You can file an RTI asking for tender details, how many bidders participated, and selection criteria.',
  },
  sanctionedCost: {
    term: 'Sanctioned Cost',
    shortExplanation:
      'The officially approved budget for a road work before it begins.',
    fullExplanation:
      'Sanctioned cost is the amount approved by BBMP for a specific road work based on the estimate prepared by engineers. It sets the upper limit for contractor payment.',
    whatItMeans:
      'This is how much was approved to be spent. Compare it with the actual paid amount to see if the work stayed within budget.',
  },
  actualPaid: {
    term: 'Actual Paid',
    shortExplanation:
      'The final amount paid to the contractor after work completion.',
    fullExplanation:
      'Actual paid reflects the total payment made to the contractor, which may differ from the sanctioned cost due to quantity variations, additional works, or deductions.',
    whatItMeans:
      'This is how much of your tax money actually went to the contractor. If it is higher than the sanctioned cost, ask why through an RTI.',
  },
  performanceScore: {
    term: 'Performance Score',
    shortExplanation:
      'A composite score (0-100%) measuring contractor reliability.',
    fullExplanation:
      'Calculated as: 50% weight on on-time completion rate + 30% weight on absence of delays + 20% weight on DLP compliance. Higher is better.',
    whatItMeans:
      'A quick way to judge contractor reliability. Below 55% means the contractor has significant issues. Above 85% means they generally deliver quality work on time.',
  },
};

// Maps red flag types to glossary keys
export const redFlagGlossaryKey: Record<string, string> = {
  repeatFailure: 'repeatFailure',
  dlpSpending: 'dlpSpending',
  costOutlier: 'costOutlier',
  costOverrun: 'costOverrun',
  severeDelay: 'severeDelay',
  contractorDominance: 'contractorDominance',
  delayedCompletion: 'severeDelay',
  poorContractorPerformance: 'gradeD',
  missingFields: 'dlp',
  singleBid: 'contractorDominance',
};
