# DEF-01 — Speed 60 was fined

| Item | Detail |
| --- | --- |
| ID | DEF-01 |
| Title | Speed 60 was incorrectly fined |
| Module | Fine calculation |
| Requirement | REQ-FINE-03 |
| Severity | Major |
| Priority | High |
| Status | Closed |
| Found | 17 November 2026, Build B1, TC-BVA-01 |
| Fixed | 19 November 2026, Build B2 |
| Retest | 20 November 2026, TC-BVA-01, Pass |
| Regression | `test_TC_BVA_01_DEF_01_speed_60_rejected` |

## What happened

The limit is 60 km/h. Speed 60 is not an offence, so the challan must be rejected. On Build B1, a Car recorded at 60 km/h was stored as Issued with a fine of ₹500. The check used "below 60" where the rule says "60 or below".

## Steps

1. Register a Car.
2. Record Overspeeding on 1 June 2026 with speed 60.

| | Result |
| --- | --- |
| Expected | Rejected. No challan stored. |
| Actual on B1 | Issued. Fine ₹500. |
| Actual on B2 | Rejected. No challan stored. |

## Fix

`calculate_fine` rejects overspeeding when the speed is less than or equal to 60. The ₹500 band starts at 61 and ends at 80. Speed 81 is ₹2000. The repository code already contains this fix.

## Retest

TC-BVA-01 passed on 20 November 2026. TC-BVA-02 (speed 61, ₹500) had already passed on Build B1, so the fix did not move the next value into the reject class.
