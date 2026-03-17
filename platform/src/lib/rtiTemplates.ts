export interface RtiTemplateContext {
  roadName?: string;
  roadId?: string;
  contractorName?: string;
  flagType?: string;
  jobCode?: string;
  wardName?: string;
  wardNumber?: string;
  sanctionedCost?: string;
  actualPaid?: string;
  dlpEndDate?: string;
}

export interface RtiTemplate {
  subject: string;
  body: string;
  authority: string;
  tips: string[];
}

function formatRupees(amount: string | undefined): string {
  if (!amount) return '[AMOUNT]';
  const num = parseFloat(amount);
  if (isNaN(num)) return amount;
  if (num >= 10000000) return `Rs. ${(num / 10000000).toFixed(2)} Cr`;
  if (num >= 100000) return `Rs. ${(num / 100000).toFixed(2)} L`;
  return `Rs. ${num.toLocaleString('en-IN')}`;
}

const commonHeader = `To,
The Public Information Officer,
BBMP Head Office,
N.R. Square, Bengaluru - 560002

From,
[YOUR NAME]
[YOUR ADDRESS]
Phone: [YOUR PHONE NUMBER]

Date: [DATE]

Subject: `;

const commonFooter = `
I am willing to pay the prescribed fee for obtaining this information.

I request that the information be provided in hard copy / electronic format (as available).

Thanking you,
[YOUR NAME]
[YOUR ADDRESS]
[YOUR PHONE NUMBER]`;

const commonTips = [
  'Attach a Rs. 10 fee (postal order, demand draft, or court fee stamp) if filing by post.',
  'You can also file this online at rtionline.gov.in.',
  'BBMP must respond within 30 days under the RTI Act, 2005.',
  'If no response in 30 days, file a first appeal to the Appellate Authority (next senior officer).',
  'Keep a photocopy of your application and the postal/online receipt.',
  'If your first appeal also fails, you can approach the Karnataka Information Commission within 90 days.',
];

export function generateRtiTemplate(context: RtiTemplateContext): RtiTemplate {
  const road = context.roadName || '[ROAD NAME]';
  const contractor = context.contractorName || '[CONTRACTOR NAME]';
  const ward = context.wardName || '[WARD NAME]';
  const wardNum = context.wardNumber || '[WARD NUMBER]';
  const jobCode = context.jobCode || '[JOB CODE]';

  switch (context.flagType) {
    case 'costOutlier':
      return {
        subject: `Request for cost breakdown of road work on ${road}`,
        body:
          commonHeader +
          `Request for detailed cost breakdown and tender documents for road work on ${road}, Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information regarding road work on ${road} (Job Code: ${jobCode}):\n\n` +
          `1. Detailed item-wise cost breakdown (Schedule of Rates) for this work.\n` +
          `2. Copy of the estimate prepared by the engineer with rate analysis.\n` +
          `3. Copy of the tender document and all bids received.\n` +
          `4. Sanctioned cost: ${formatRupees(context.sanctionedCost)}. Please provide justification for this amount compared to similar works in the zone.\n` +
          `5. Copy of the Work Order issued to ${contractor}.\n` +
          `6. Details of any revised estimates and approvals obtained.\n` +
          `7. Measurement book entries for this work.\n\n` +
          `This information is sought because the cost of this work appears significantly higher than comparable road works in the area.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: [
          ...commonTips,
          'Compare the cost per km with similar roads in the same zone to build your case.',
          'If the response is inadequate, you can ask follow-up questions in a new RTI.',
        ],
      };

    case 'repeatFailure':
      return {
        subject: `Request for quality inspection reports for ${road}`,
        body:
          commonHeader +
          `Request for information on repeated road work on ${road}, Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information regarding ${road} (Job Code: ${jobCode}):\n\n` +
          `1. Why was this road resurfaced/repaired again within 2 years of the previous work?\n` +
          `2. Copy of quality inspection reports for the previous work on this road.\n` +
          `3. Was the Defect Liability Period (DLP) warranty enforced on the previous contractor (${contractor})? If not, why not?\n` +
          `4. Details of any penalties imposed on the contractor for defective work.\n` +
          `5. Copy of the complaint/inspection report that led to the decision to redo the work.\n` +
          `6. Who authorized fresh expenditure of public funds instead of enforcing the DLP warranty?\n` +
          `7. Total public money spent on both the previous and current work on this road.\n\n` +
          `The road appears to have been repaired twice in a short period, which raises questions about work quality and DLP enforcement.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: [
          ...commonTips,
          'Mention the specific dates of both works if you have them.',
          'Photos of current road condition can support your case if you file a complaint alongside.',
        ],
      };

    case 'dlpSpending':
      return {
        subject: `Request for DLP warranty enforcement details for ${road}`,
        body:
          commonHeader +
          `Request for information on public expenditure during DLP period for ${road}, Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information:\n\n` +
          `1. The DLP (Defect Liability Period) for road work on ${road} (Job Code: ${jobCode}) is valid until ${context.dlpEndDate || '[DLP END DATE]'}. Why was public money spent on repairs during this warranty period?\n` +
          `2. Was the contractor (${contractor}) notified about defects during the DLP period? If yes, provide copies of notices sent.\n` +
          `3. What action was taken against the contractor for failing to maintain the road during DLP?\n` +
          `4. Was the performance guarantee / security deposit of the contractor forfeited? If not, why?\n` +
          `5. Who authorized the expenditure of public funds for repairs that should have been done by the contractor under warranty?\n` +
          `6. Total amount of public money spent on repairs during the DLP period for this road.\n\n` +
          `The DLP warranty exists specifically to protect public money. Spending fresh public funds while the warranty is active is a misuse of taxpayer money.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: [
          ...commonTips,
          'The DLP end date is key evidence -- make sure to mention it clearly.',
          'Ask for the performance guarantee amount and whether it was encashed.',
        ],
      };

    case 'costOverrun':
      return {
        subject: `Request for justification of cost overrun on ${road}`,
        body:
          commonHeader +
          `Request for information on cost overrun for road work on ${road}, Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information regarding road work on ${road} (Job Code: ${jobCode}):\n\n` +
          `1. The sanctioned cost for this work was ${formatRupees(context.sanctionedCost)} but the actual amount paid was ${formatRupees(context.actualPaid)}. Please provide the detailed justification for this excess expenditure.\n` +
          `2. Copy of the revised estimate, if any, with approval from the competent authority.\n` +
          `3. Details of additional items or quantity variations that led to the cost increase.\n` +
          `4. Name and designation of the officer who approved the excess expenditure.\n` +
          `5. Was the excess within the permissible limits under KTPP Act / BBMP rules? If it exceeded limits, was higher authority approval obtained?\n\n` +
          `The actual payment exceeding the sanctioned cost requires justification and proper authorization.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: [
          ...commonTips,
          'Cost overruns beyond 10% typically require approval from a higher authority.',
          'Under KTPP Act rules, significant variations may require re-tendering.',
        ],
      };

    case 'severeDelay':
    case 'delayedCompletion':
      return {
        subject: `Request for delay details and penalty status for ${road}`,
        body:
          commonHeader +
          `Request for information on delayed road work on ${road}, Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information regarding road work on ${road} (Job Code: ${jobCode}):\n\n` +
          `1. What were the reasons for delay in completing this road work by ${contractor}?\n` +
          `2. Was a penalty imposed on the contractor for the delay as per contract terms? If yes, how much? If no, why not?\n` +
          `3. Copy of any extension of time granted and the reasons cited.\n` +
          `4. Was liquidated damages clause invoked? If not, why?\n` +
          `5. Details of any show-cause notices issued to the contractor.\n` +
          `6. Impact assessment: what was the estimated public inconvenience cost due to the delay?\n\n` +
          `Severe delays in road works cause significant inconvenience to residents and commuters.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: [
          ...commonTips,
          'Typical penalty clauses allow deduction of 1-2% of contract value per week of delay.',
          'If extension of time was granted without valid reasons, this is a red flag.',
        ],
      };

    case 'contractorDominance':
      return {
        subject: `Request for tender and selection details in Ward ${wardNum}`,
        body:
          commonHeader +
          `Request for contractor selection details for road works in Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information:\n\n` +
          `1. List of all road works awarded in Ward ${wardNum} (${ward}) from 2020 to present, with contractor names and values.\n` +
          `2. For each tender, the number of bids received and names of all bidding contractors.\n` +
          `3. Why has ${contractor} been awarded a disproportionately large number of works in this ward?\n` +
          `4. Tender evaluation criteria and scoring sheets for recent works.\n` +
          `5. Were any complaints received about the tender process? If yes, what action was taken?\n` +
          `6. Is there a policy to ensure equitable distribution of works among qualified contractors?\n\n` +
          `Concentration of works with a single contractor reduces competitive benefits and raises transparency concerns.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: [
          ...commonTips,
          'A healthy tender process should have at least 3 bidders.',
          'Check if the same contractor keeps winning across multiple wards -- that pattern is worth an RTI.',
        ],
      };

    default:
      return {
        subject: `Request for road work information - ${road}`,
        body:
          commonHeader +
          `Request for information regarding road work on ${road}, Ward ${wardNum} (${ward})\n\n` +
          `Dear Sir/Madam,\n\n` +
          `Under the Right to Information Act, 2005, I request the following information regarding road work on ${road}${jobCode !== '[JOB CODE]' ? ` (Job Code: ${jobCode})` : ''}:\n\n` +
          `1. Complete details of road works undertaken on this road from 2018 to present, including:\n` +
          `   a. Work description and type\n` +
          `   b. Contractor name and registration details\n` +
          `   c. Sanctioned cost and actual amount paid\n` +
          `   d. Work order date, stipulated completion date, and actual completion date\n` +
          `   e. DLP (warranty) start and end dates\n` +
          `2. Quality inspection reports for completed works.\n` +
          `3. Details of any complaints received about road quality.\n` +
          `4. Current DLP status and contractor responsible for maintenance.\n` +
          `5. Tender documents and number of bids received for each work.\n\n` +
          `This information is sought as a citizen interested in transparency of public road infrastructure spending.` +
          commonFooter,
        authority: 'Public Information Officer, BBMP',
        tips: commonTips,
      };
  }
}
