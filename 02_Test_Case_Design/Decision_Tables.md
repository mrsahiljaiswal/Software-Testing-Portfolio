# Decision Tables

## What to say

A decision table is a small grid: conditions on top, the action at the bottom. Each column is one rule, and each rule has one test case.

We use two tables.

Table A answers: do we accept this challan? Table B answers: how much is due? Overspeeding above 60 km/h is accepted, and the amount for that speed is already in the equivalence and boundary cases, so Table A only keeps the reject rule for speed.

The challan date in every case is 1 June 2026. The due date is 16 June 2026. The vehicle is registered first.

## Table A — Accept or reject a challan

| | Rule A1 | Rule A2 | Rule A3 | Rule A4 |
| --- | --- | --- | --- | --- |
| Vehicle | Two-wheeler or Car | Two-wheeler | Car | Two-wheeler or Car |
| Violation | Signal jump | No helmet | No helmet | Overspeeding |
| Speed | — | — | — | 60 or below |
| Action | Accept, fine ₹500 | Accept, fine ₹1000 | Reject | Reject |
| Case | TC-DT-01 | TC-DT-02 | TC-DT-03 | TC-DT-04 |

## Table B — Amount due

| | Rule B1 | Rule B2 |
| --- | --- | --- |
| Payment date | On or before the due date | After the due date |
| Amount tendered | The fine | The fine + ₹200 |
| Action | Status becomes Paid | Status becomes Paid |
| Case | TC-DT-05 | TC-DT-06 |

Any other amount is rejected. That check is TC-BVA-08. A second payment is TC-ST-04.

## Test cases

| ID | Rule | Requirement | Input | Expected result |
| --- | --- | --- | --- | --- |
| TC-DT-01 | A1 | REQ-FINE-01 | Car, Signal jump | Issued. Fine ₹500. |
| TC-DT-02 | A2 | REQ-FINE-02 | Two-wheeler, No helmet | Issued. Fine ₹1000. |
| TC-DT-03 | A3 | REQ-FINE-02 | Car, No helmet | Rejected. No challan is stored. Failed on Build B1 (DEF-02). Passes on Build B2. |
| TC-DT-04 | A4 | REQ-FINE-03 | Two-wheeler, Overspeeding, speed 50 | Rejected. Speed 50 is inside "60 or below". The edge at 60 is TC-BVA-01. |
| TC-DT-05 | B1 | REQ-PAY-01 | Car, Signal jump, fine ₹500. Pay ₹500 on 10 June 2026. | Paid. Amount paid ₹500. 10 June is before the due date. |
| TC-DT-06 | B2 | REQ-PAY-02 | Car, Signal jump, fine ₹500. Pay ₹700 on 20 June 2026. | Paid. Amount paid ₹700. The late fee is still ₹200 on a later day. Failed on Build B1 (DEF-03). Passes on Build B2. |

6 cases: TC-DT-01 to TC-DT-06. Each case traces to one rule.
