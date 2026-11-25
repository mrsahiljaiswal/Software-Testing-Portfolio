# DEF-02 — No-helmet challan accepted for a Car

| Item | Detail |
| --- | --- |
| ID | DEF-02 |
| Title | No-helmet challan was accepted for a Car |
| Module | Challan recording |
| Requirement | REQ-FINE-02 |
| Severity | Major |
| Priority | High |
| Status | Closed |
| Found | 17 November 2026, Build B1, TC-EP-04 |
| Also failed | TC-DT-03 on 18 November 2026 |
| Fixed | 19 November 2026, Build B2 |
| Retest | 20 November 2026, TC-EP-04 and TC-DT-03, Pass |
| Regression | `test_TC_EP_04_DEF_02_car_no_helmet_rejected` |

## What happened

No helmet is ₹1000 for a Two-wheeler only. A Car must be rejected and nothing stored. On Build B1, a Car with No helmet was accepted and a challan was stored.

## Steps

1. Register a Car.
2. Record No helmet on 1 June 2026.

| | Result |
| --- | --- |
| Expected | Rejected. No challan stored. |
| Actual on B1 | Challan stored. |
| Actual on B2 | Rejected. No challan stored. |

The same steps on a Two-wheeler still produce an Issued challan of ₹1000 (TC-EP-03 and TC-DT-02). Those two passed on Build B1.

## Fix

`calculate_fine` rejects No helmet unless the vehicle is a Two-wheeler. The repository code already contains this fix.

## Retest

TC-EP-04 and TC-DT-03 passed on 20 November 2026.
