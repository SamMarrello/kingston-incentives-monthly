# Data File Schema

This document describes the structure of `data/incentives.json`.

## Top-Level Structure

```json
{
  "version": "string",
  "last_updated": "YYYY-MM-DD",
  "federal": [...],
  "provincial": [...],
  "local": {
    "Kingston": [...],
    "Belleville": [...],
    "Brockville": [...],
    "Cornwall": [...],
    "Peterborough": [...]
  }
}
```

## Federal/Provincial Program Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Short program name |
| full_name | string | Yes | Complete program name |
| url | string | Yes | Official program URL |
| type | string | Yes | Grant/Loan/Tax Credit/etc |
| description | string | Yes | Program description |
| eligibility | string | Yes | Who qualifies |
| amount | string | Yes | Funding amount |
| status | string | Yes | Active/Closed/Paused |
| administered_by | string | Yes | Administering organization |

## Local Program Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Program name |
| type | string | Yes | Grant/Loan/Tax Relief/etc |
| description | string | Yes | Program description |
| eligibility | string | Yes | Who qualifies |
| contact | string | Yes | Contact organization |

## Incentive Types

Valid values for the `type` field:

- `Grant` - Non-repayable funding
- `Loan` - Low-interest or forgivable loans
- `Tax Credit` - Tax incentives
- `Tax Relief` - Property or other tax reductions
- `Fee Waiver` - Waived municipal fees
- `Fee Reduction` - Reduced municipal fees
- `Zoning Incentive` - Density/height bonuses
- `Process` - Fast-track permitting, etc
