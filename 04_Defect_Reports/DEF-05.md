# DEF-05 — Early-payment discount given for drunk driving

| Field | Value |
| --- | --- |
| ID | DEF-05 |
| Title | Early-payment discount given for drunk driving |
| Module | Payment |
| Severity | Major |
| Priority | High |
| Build found | B1, 17 November 2026 |
| Detected in | TC-DT-08 |
| Status | Closed |
| Fixed in | Build B2, 19 November 2026 |
| Retest | 20 November 2026, Pass |

## Description

A 10% early discount applies only when the payment is on or before day 7, the status is still Issued, the violation is not drunk driving, and `suspension_recommended` is false. Drunk driving always recommends suspension and is also excluded by name. Build B1 still subtracted 10% and accepted 9000 on a 10000 fine.

## Steps

1. Issue drunk driving for a private car on 1 June 2026. Confirm the calculated fine is 10000 and `suspension_recommended` is true.
2. On 2 June 2026 tender 9000.
3. Tender 10000.

## Expected

The payable amount is 10000. The tender of 9000 is rejected and the status stays Issued. The tender of 10000 is accepted and the status becomes Paid. The licence status is unchanged.

## Actual (Build B1)

The tender of 9000 was accepted and the status became Paid.

## Fix

`compute_payable` grants the discount only when the status is Issued, the violation is not drunk driving, and `suspension_recommended` is false. An Upheld challan is also excluded, which is REQ-PAY-06 and was already behaving correctly; this defect is the drunk-driving hole in the Issued path.

## Retest result

TC-DT-08 passed on Build B2. 9000 was rejected and 10000 was accepted. A normal signal jump inside 7 days (TC-DT-07) still receives the discount, so the fix did not remove a valid discount. Regression method: `test_TC_DT_08_drunk_driving_has_no_early_discount`.
