# Boundary Value Analysis

## What to say

Boundary value analysis tests the edges, because an off-by-one error shows up there.

The speed limit is 60. The ₹500 band runs from 61 to 80. The ₹2000 band starts at 81. So the four speed values are 60, 61, 80, and 81. The limit is the same for every vehicle, so a Car is enough for these four.

The due date is the challan date plus 15 days. For a challan on 1 June 2026, the due date is 16 June 2026. We pay on 16 June and on 17 June. The late fee is a flat ₹200, so we also check it on a ₹1000 fine, and we check that one rupee less than the late amount is rejected.

## Boundaries

| Edge | Value | Result | Case |
| --- | --- | --- | --- |
| Speed still within the limit | 60 | Reject | TC-BVA-01 |
| First speed in the ₹500 band | 61 | Fine ₹500 | TC-BVA-02 |
| Last speed in the ₹500 band | 80 | Fine ₹500 | TC-BVA-03 |
| First speed in the ₹2000 band | 81 | Fine ₹2000 | TC-BVA-04 |
| Last on-time day | 16 June 2026 (the due date) | Pay the fine | TC-BVA-05 |
| First late day | 17 June 2026 | Pay the fine + ₹200 | TC-BVA-06 |
| Late fee on another fine | ₹1000 + ₹200 = ₹1200 | Pay ₹1200 | TC-BVA-07 |
| One rupee short of the late amount | ₹2199 instead of ₹2200 | Reject | TC-BVA-08 |

## Test cases

Challan date is 1 June 2026. The vehicle is registered first.

| ID | Requirement | Input | Expected result |
| --- | --- | --- | --- |
| TC-BVA-01 | REQ-FINE-03 | Car, Overspeeding, speed 60 | Rejected. No challan is stored. Failed on Build B1 (DEF-01). Passes on Build B2. |
| TC-BVA-02 | REQ-FINE-03 | Car, Overspeeding, speed 61 | Issued. Fine ₹500. |
| TC-BVA-03 | REQ-FINE-03 | Car, Overspeeding, speed 80 | Issued. Fine ₹500. |
| TC-BVA-04 | REQ-FINE-03 | Car, Overspeeding, speed 81 | Issued. Fine ₹2000. |
| TC-BVA-05 | REQ-PAY-01 | Car, Signal jump, fine ₹500. Pay ₹500 on 16 June 2026. | Due date is 16 June 2026. Status becomes Paid. Amount paid ₹500. |
| TC-BVA-06 | REQ-PAY-02 | Car, Signal jump, fine ₹500. On 17 June, tender ₹500, then tender ₹700. | ₹500 is rejected and the status stays Issued. ₹700 is accepted. Status becomes Paid. Failed on Build B1 (DEF-03). Passes on Build B2. |
| TC-BVA-07 | REQ-PAY-02 | Two-wheeler, No helmet, fine ₹1000. Pay ₹1200 on 17 June 2026. | Paid. The amount above the fine is ₹200. Failed on Build B1 (DEF-03). Passes on Build B2. |
| TC-BVA-08 | REQ-PAY-03 | Car, Overspeeding, speed 81, fine ₹2000. Pay ₹2199 on 17 June 2026. | Rejected. Status stays Issued. Nothing is recorded as paid. |

8 cases: TC-BVA-01 to TC-BVA-08.
