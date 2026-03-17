# RTI Filing Guide

How to file RTI applications for road infrastructure data in a new city or zone.

## Overview

The platform relies on RTI (Right to Information) Act, 2005 responses for its data. Filing effective RTI applications is critical. This guide covers how to adapt our templates for any Indian municipality.

## Step 1: Understand the Municipal Structure

Before filing, map out:
- **Municipal body name** (e.g., BBMP, PMC, GHMC)
- **Zone/ward structure** (how the city divides into zones and wards)
- **Road jurisdiction split**: Most cities separate ward roads (local) from arterial/major roads (central). You need separate RTI applications for each.
- **PIO (Public Information Officer)**: Identify the correct PIO for each jurisdiction.

## Step 2: Identify Key Data Fields

The platform needs these fields for each road work:

| Priority | Field | Why |
|----------|-------|-----|
| Critical | Job Code / Work Code | Primary key for the database |
| Critical | Name of Work | Links to physical road |
| Critical | Contractor Name | Accountability |
| Critical | DLP Start/End Dates | Warranty tracking |
| High | Work Order Number & Date | Audit trail |
| High | Sanctioned Cost | Budget tracking |
| High | Actual Amount Paid | Cost analysis |
| High | Actual Completion Date | Delay detection |
| Medium | Check Measurement Officers | Official accountability |
| Medium | Tender Number & Bid Count | Competition analysis |
| Low | Performance Guarantee Amount | Security deposit tracking |

## Step 3: Draft the RTI Application

Use our Bengaluru templates as a starting point:
- `APPLICATION_A_ready_to_file.md` -- Template for ward roads
- `APPLICATION_B_ready_to_file.md` -- Template for arterial/major roads

### Adaptation Checklist

- [ ] Replace "BBMP" with your municipal body name
- [ ] Replace zone name (e.g., "Mahadevapura" with your zone)
- [ ] Replace ward number and name
- [ ] Adjust financial year range (typically last 5-7 years)
- [ ] Update PIO designation and office
- [ ] Keep the request for "Excel/CSV" format -- this is key
- [ ] Keep the Section 4(1)(b) reference for digital format
- [ ] Stay within 3000 characters (portal limit)

## Step 4: File on the RTI Portal

1. Go to [rtionline.gov.in](https://rtionline.gov.in) (central) or your state portal
2. Select the correct Public Authority
3. Fill applicant details
4. Paste the RTI text (keep under 3000 chars)
5. Pay Rs 10 fee
6. Save the Registration Number

## Step 5: Handle Responses

### Ideal Response
An Excel/CSV file with all requested fields. Run it through the pipeline:
```bash
python pipeline/ingest.py --input response.xlsx --city <city> --zone <zone> --ward <ward> --rti-id <id>
```

### Common Problems

| Problem | Solution |
|---------|----------|
| "Data not available in digital format" | Cite Section 4(1)(b). File First Appeal. |
| "Information is voluminous" | Offer to pay for photocopying. Narrow the date range. |
| Response is a letter, not data | File First Appeal requesting structured data specifically. |
| Partial response (missing columns) | File follow-up RTI for missing fields. |
| Transferred to another department | Wait for transfer. File separately if delayed. |
| Scanned PDF of register | Use OCR (Tesseract) to extract data. |

### First Appeal

If response is unsatisfactory (incomplete, denied, or no response within 30 days):
1. File First Appeal to the Appellate Authority (usually one rank above PIO)
2. Cite specific shortcomings in the response
3. Deadline: within 30 days of receiving response (or 30 days after response deadline)

## Step 6: Process and Contribute

1. Run the data through the pipeline
2. Verify with `npm run validate-data`
3. Submit a Pull Request with the new data
4. Include the RTI registration number for provenance

## Tips

- **File in batches**: Start with the road inventory (Application A equivalent), then follow up with detailed financials and DLP data
- **Request Excel specifically**: The phrase "Excel/CSV via email" in the RTI text is deliberate
- **Photograph registers**: If the PIO shows physical registers, photograph them and OCR later
- **Track everything**: Keep a spreadsheet of all RTI applications, dates, registration numbers, and response status
