# DEF-04 — Dispute accepted on day 16

| Field | Value |
| --- | --- |
| ID | DEF-04 |
| Title | Dispute accepted on day 16 |
| Module | Dispute |
| Severity | Major |
| Priority | High |
| Build found | B1, 18 November 2026 |
| Detected in | TC-BVA-13 |
| Status | Closed |
| Fixed in | Build B2, 19 November 2026 |
| Retest | 20 November 2026, Pass |

## Description

The dispute window is the offence date through the offence date plus 15 calendar days, inclusive. Day 16 must be rejected and the challan must stay Issued. Build B1 accepted day 16.

## Steps

1. Issue a private-car signal jump on 1 June 2026.
2. Dispute it on 17 June 2026, which is offence date + 16 days.

## Expected

The dispute is rejected. Status remains Issued.

## Actual (Build B1)

Status became Disputed.

## Fix

The guard is now `offence_date <= dispute_date <= offence_date + 15 days`. A date before the offence date is also rejected. The state transition Issued → Disputed is still allowed only when this guard passes. The check is `dispute` in `system.py`.

## Retest result

TC-BVA-13 passed on Build B2 and the status stayed Issued. Day 15 (TC-BVA-12, 16 June 2026) and the offence date (TC-ST-03) are still accepted. Regression method: `test_TC_BVA_13_dispute_on_day_16_rejected`.
