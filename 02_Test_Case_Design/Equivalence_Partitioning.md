# Equivalence Partitioning

## What to say

Equivalence partitioning puts inputs that the system treats the same way into one class. We test one value from the class.

There are two vehicle types and three violations. Signal jump is ₹500 for both vehicles, so each vehicle is one class. No helmet is allowed for a Two-wheeler and rejected for a Car, so those are two classes. Overspeeding has three speed classes, and the limit is 60 km/h for every vehicle:

- Within the limit: speed 60 or below. The challan is rejected.
- Slightly over: speed 61 to 80. The fine is ₹500.
- Well over: speed 81 or above. The fine is ₹2000.

The numbers 60, 61, 80, and 81 are the edges of those classes. They are tested in the boundary file. Here, 40 and 50 stand for "within the limit", 70 stands for "slightly over", and 100 stands for "well over".

Every case uses challan date 1 June 2026. The vehicle is registered before the challan. A rejected challan is not stored.

## Partitions

| Class | Example | Result | Case |
| --- | --- | --- | --- |
| Two-wheeler, Signal jump | — | Accept, ₹500 | TC-EP-01 |
| Car, Signal jump | — | Accept, ₹500 | TC-EP-02 |
| Two-wheeler, No helmet | — | Accept, ₹1000 | TC-EP-03 |
| Car, No helmet | — | Reject | TC-EP-04 |
| Overspeeding, within the limit | 40 km/h, Two-wheeler | Reject | TC-EP-05 |
| Overspeeding, slightly over | 70 km/h, Car | Accept, ₹500 | TC-EP-06 |
| Overspeeding, well over | 100 km/h, Two-wheeler | Accept, ₹2000 | TC-EP-07 |
| Overspeeding, within the limit, other vehicle | 50 km/h, Car | Reject | TC-EP-08 |

## Test cases

| ID | Requirement | Input | Expected result |
| --- | --- | --- | --- |
| TC-EP-01 | REQ-FINE-01, REQ-PAY-01 | Two-wheeler, Signal jump, 1 June 2026 | Issued. Fine ₹500. Due date 16 June 2026. |
| TC-EP-02 | REQ-FINE-01 | Car, Signal jump, 1 June 2026 | Issued. Fine ₹500. |
| TC-EP-03 | REQ-FINE-02 | Two-wheeler, No helmet, 1 June 2026 | Issued. Fine ₹1000. |
| TC-EP-04 | REQ-FINE-02 | Car, No helmet, 1 June 2026 | Rejected. No challan is stored. Failed on Build B1 (DEF-02). Passes on Build B2. |
| TC-EP-05 | REQ-FINE-03 | Two-wheeler, Overspeeding, speed 40 | Rejected. No challan is stored. |
| TC-EP-06 | REQ-FINE-03 | Car, Overspeeding, speed 70 | Issued. Fine ₹500. |
| TC-EP-07 | REQ-FINE-03 | Two-wheeler, Overspeeding, speed 100 | Issued. Fine ₹2000. |
| TC-EP-08 | REQ-FINE-03 | Car, Overspeeding, speed 50 | Rejected. No challan is stored. |

8 cases: TC-EP-01 to TC-EP-08.
