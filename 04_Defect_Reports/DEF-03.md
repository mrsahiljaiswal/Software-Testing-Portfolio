# DEF-03 — Late payment missed the ₹200 fee

| Item | Detail |
| --- | --- |
| ID | DEF-03 |
| Title | Payment after the due date did not add the ₹200 late fee |
| Module | Payment |
| Requirement | REQ-PAY-02 |
| Severity | Major |
| Priority | High |
| Status | Closed |
| Found | 18 November 2026, Build B1, TC-BVA-06 |
| Also failed | TC-BVA-07, TC-DT-06, TC-ST-03 |
| Fixed | 19 November 2026, Build B2 |
| Retest | 20 November 2026, all four cases, Pass |
| Regression | `test_TC_BVA_06_DEF_03_day_after_due_adds_200` |

## What happened

The due date is the challan date plus 15 days. After that date the owner pays the fine plus ₹200. On Build B1, a late payment was still the fine alone. A ₹500 signal jump due on 16 June 2026 was payable at ₹500 on 17 June 2026. The rule says ₹700.

## Steps

1. Register a Car and record Signal jump on 1 June 2026. Fine ₹500. Due date 16 June 2026.
2. On 17 June 2026, ask for the payable amount.
3. Tender ₹700.

| | Result |
| --- | --- |
| Expected | Payable ₹700. Payment of ₹700 is accepted. Payment of ₹500 is rejected. |
| Actual on B1 | Payable stayed ₹500. ₹700 was rejected. |
| Actual on B2 | Payable is ₹700. ₹500 is rejected. ₹700 is accepted and the status is Paid. |

The same fault failed three more cases: a ₹1000 helmet fine was not taken as ₹1200 (TC-BVA-07), a payment on 20 June was not ₹700 (TC-DT-06), and an Overdue challan could not be paid with ₹700 (TC-ST-03). On-time payment of ₹500 (TC-BVA-05) passed on Build B1.

## Fix

`amount_due` returns the fine on or before the due date, and the fine plus 200 after the due date. The fee stays ₹200 on later days. The repository code already contains this fix.

## Retest

TC-BVA-06, TC-BVA-07, TC-DT-06, and TC-ST-03 passed on 20 November 2026.
