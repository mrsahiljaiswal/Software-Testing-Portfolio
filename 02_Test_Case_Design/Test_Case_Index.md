# Test Case Index

Master list of the 28 manual cases. The final result is the status after the 20 November 2026 retest on Build B2.

| ID | Technique | Module | Requirement | Final result |
| --- | --- | --- | --- | --- |
| TC-EP-01 | Equivalence partitioning | Fine | REQ-FINE-01, REQ-PAY-01 | Pass |
| TC-EP-02 | Equivalence partitioning | Fine | REQ-FINE-01 | Pass |
| TC-EP-03 | Equivalence partitioning | Fine | REQ-FINE-02 | Pass |
| TC-EP-04 | Equivalence partitioning | Challan | REQ-FINE-02 | Pass |
| TC-EP-05 | Equivalence partitioning | Challan | REQ-FINE-03 | Pass |
| TC-EP-06 | Equivalence partitioning | Fine | REQ-FINE-03 | Pass |
| TC-EP-07 | Equivalence partitioning | Fine | REQ-FINE-03 | Pass |
| TC-EP-08 | Equivalence partitioning | Challan | REQ-FINE-03 | Pass |
| TC-BVA-01 | Boundary value analysis | Fine | REQ-FINE-03 | Pass |
| TC-BVA-02 | Boundary value analysis | Fine | REQ-FINE-03 | Pass |
| TC-BVA-03 | Boundary value analysis | Fine | REQ-FINE-03 | Pass |
| TC-BVA-04 | Boundary value analysis | Fine | REQ-FINE-03 | Pass |
| TC-BVA-05 | Boundary value analysis | Payment | REQ-PAY-01 | Pass |
| TC-BVA-06 | Boundary value analysis | Payment | REQ-PAY-02 | Pass |
| TC-BVA-07 | Boundary value analysis | Payment | REQ-PAY-02 | Pass |
| TC-BVA-08 | Boundary value analysis | Payment | REQ-PAY-03 | Pass |
| TC-DT-01 | Decision table | Challan | REQ-FINE-01 | Pass |
| TC-DT-02 | Decision table | Challan | REQ-FINE-02 | Pass |
| TC-DT-03 | Decision table | Challan | REQ-FINE-02 | Pass |
| TC-DT-04 | Decision table | Challan | REQ-FINE-03 | Pass |
| TC-DT-05 | Decision table | Payment | REQ-PAY-01 | Pass |
| TC-DT-06 | Decision table | Payment | REQ-PAY-02 | Pass |
| TC-ST-01 | State transition | State | REQ-ST-01, REQ-PAY-01 | Pass |
| TC-ST-02 | State transition | State | REQ-ST-01 | Pass |
| TC-ST-03 | State transition | State | REQ-ST-01, REQ-PAY-02 | Pass |
| TC-ST-04 | State transition | State | REQ-ST-01, REQ-PAY-03 | Pass |
| TC-ST-05 | State transition | State | REQ-ST-01 | Pass |
| TC-ST-06 | State transition | State | REQ-ST-01 | Pass |

## Counts

| Technique | Cases | Final Pass |
| --- | ---: | ---: |
| Equivalence partitioning | 8 | 8 |
| Boundary value analysis | 8 | 8 |
| Decision table | 6 | 6 |
| State transition | 6 | 6 |
| Total | 28 | 28 |

All 28 cases are High priority.

## Module counts

| Module | Cases |
| --- | ---: |
| Challan | 7 |
| Fine | 9 |
| Payment | 6 |
| State | 6 |
| Total | 28 |

Challan: TC-EP-04, TC-EP-05, TC-EP-08, TC-DT-01, TC-DT-02, TC-DT-03, TC-DT-04.

Fine: TC-EP-01, TC-EP-02, TC-EP-03, TC-EP-06, TC-EP-07, TC-BVA-01, TC-BVA-02, TC-BVA-03, TC-BVA-04.

Payment: TC-BVA-05, TC-BVA-06, TC-BVA-07, TC-BVA-08, TC-DT-05, TC-DT-06.

State: TC-ST-01, TC-ST-02, TC-ST-03, TC-ST-04, TC-ST-05, TC-ST-06.

7 + 9 + 6 + 6 = 28.

Registration (REQ-REG-01) is checked by two automated tests. It is not one of these 28 technique cases.
