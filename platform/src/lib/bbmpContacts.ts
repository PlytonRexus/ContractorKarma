export interface BbmpContact {
  name: string;
  type: 'portal' | 'phone' | 'office';
  description: string;
  phone?: string;
  email?: string;
  url?: string;
  address?: string;
}

export const bbmpContacts: BbmpContact[] = [
  {
    name: 'BBMP Sahaaya (Online Grievance Portal)',
    type: 'portal',
    description:
      'File complaints about potholes, road damage, or unfinished works online. Track status with your complaint ID.',
    url: 'https://bbmp.sahaaya.karnataka.gov.in/',
  },
  {
    name: 'BBMP Control Room',
    type: 'phone',
    description:
      'Call for urgent road-related complaints including dangerous potholes, open manholes, or flooding.',
    phone: '080-22660000',
  },
  {
    name: 'BBMP Commissioner Office',
    type: 'office',
    description:
      'For escalations when ward-level officials have not responded to your complaints.',
    phone: '080-22975803',
    email: 'commissioner@bbmp.gov.in',
    address: 'BBMP Head Office, N.R. Square, Bengaluru - 560002',
  },
];

export const rtiGuidance = {
  portalUrl: 'https://rtionline.gov.in/',
  fee: 'Rs. 10 (for State Government bodies under Karnataka RTI Rules)',
  authority:
    'Public Information Officer, BBMP Head Office, N.R. Square, Bengaluru - 560002',
  timeLimits: {
    responseDeadline: '30 days from receipt of application',
    firstAppeal: 'Within 30 days of response (or non-response)',
    secondAppeal:
      'Within 90 days to Karnataka Information Commission if first appeal fails',
  },
  tips: [
    'Keep a copy of your RTI application and the postal receipt or online acknowledgment.',
    'Be specific in your questions -- mention road names, job codes, and date ranges.',
    'If you do not get a response in 30 days, file a first appeal to the Appellate Authority.',
    'You can file RTI online at rtionline.gov.in or by post with a Rs. 10 fee.',
    'BBMP is obligated to provide information within 30 days under the RTI Act, 2005.',
  ],
};
