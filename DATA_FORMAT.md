# Data Format Reference

All data is stored as JSON files in `platform/data/`. This document describes the schema for each file type.

## Directory Structure

```
data/
  meta.json
  cities/{cityId}/
    city.json
    zones/{zoneId}/
      zone.json
      wards/{wardId}/
        ward.json
        roads.json
        works.json
        dlp.json
        officials.json
  contractors/
    index.json
    {contractorId}.json
  officials/index.json
  geo/bengaluru-wards.geojson
  search/index.json
  rti/applications.json
  red-flags/flags.json
  stats/
    summary.json
    ward-rankings.json
    contractor-rankings.json
```

## Road Object (in `roads.json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| roadId | string | yes | Unique ID: `{city}-{zone}-{ward}-{seq}` |
| roadName | string | yes | Primary display name |
| aliases | string[] | yes | Alternative names |
| roadClass | enum | yes | `ward`, `arterial`, `subArterial`, `orrService` |
| surfaceType | enum | yes | `asphalt`, `concrete`, `whiteTopping`, `gravel`, `unknown` |
| lengthKm | number/null | no | Length in kilometers |
| widthM | number/null | no | Width in meters |
| osmWayId | number/null | no | OpenStreetMap way ID |
| currentDlpStatus | enum | yes | `active`, `expired`, `expiringSoon`, `unknown` |
| currentDlpEnd | string/null | no | ISO date of current DLP end |
| currentContractor | string/null | no | Name of current/latest contractor |
| totalWorksCount | number | yes | Number of works on this road |
| totalSpending | number | yes | Total amount spent (INR) |
| lastUpdated | string | yes | ISO date of last data update |

## Work Object (in `works.json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| jobCode | string | yes | Unique code: `{ward}-{year}-{serial}` |
| roadId | string | yes | FK to road |
| description | string | yes | Official work description |
| workType | enum | yes | `asphalting`, `concreting`, `whiteTopping`, etc. |
| contractorId | string | yes | FK to contractor |
| contractorName | string | yes | Contractor legal name |
| woNumber | string/null | no | Work Order number |
| woDate | string/null | no | Work Order date (ISO) |
| sanctionedCost | number/null | no | Approved cost (INR) |
| actualPaid | number/null | no | Amount paid (INR) |
| dlpStartDate | string/null | no | DLP start date (ISO) |
| dlpEndDate | string/null | no | DLP end date (ISO) |
| dlpDurationYears | number/null | no | DLP duration in years |
| dlpStatus | enum | yes | `active`, `expired`, `expiringSoon`, `unknown` |
| certifyingOfficials | array | yes | Officials who certified the work |
| redFlags | string[] | yes | Detected anomalies |
| dataSource | object | yes | `{ rtiId, responseDate }` |

## Contractor Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| contractorId | string | yes | Unique ID: `ctr-{seq}` |
| legalName | string | yes | Full legal name |
| registrationNumber | string/null | no | BBMP registration number |
| registrationClass | enum | yes | `Class I` through `Class IV`, or `unknown` |
| stats.totalWorks | number | yes | Total works count |
| stats.totalSanctionedValue | number | yes | Total value of works |
| stats.worksCompletedOnTime | number | yes | On-time completions |
| stats.worksDelayed | number | yes | Delayed works |
| stats.dlpViolations | number | yes | DLP violation count |
| stats.performanceGrade | enum | yes | `A`, `B`, `C`, `D`, `F` |
| stats.performanceScore | number | yes | 0.0 to 1.0 |

## DLP Status Values

| Status | Condition | UI Color |
|--------|-----------|----------|
| `active` | DLP end date > 6 months from now | Green |
| `expiringSoon` | DLP end date within 6 months | Yellow |
| `expired` | DLP end date has passed | Red |
| `unknown` | No DLP date available | Gray |

## ID Conventions

- Road IDs: `blr-mhd-150-001` (city-zone-ward-sequence)
- Job codes: `150-23-000042` (ward-year-serial)
- Contractor IDs: `ctr-001`
- Official IDs: `off-001`
- Red flag IDs: `rf-001`
