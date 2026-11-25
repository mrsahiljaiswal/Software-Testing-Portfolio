# Boundary Value Analysis — VTFMS

## Technique

Boundary value analysis tests the values on each edge and the value just across it. Equivalence classes supply the middles; this file supplies the edges. All amounts are rupees. Day counts are calendar days.

The baseline is `01_Test_Plan/Test_Plan.md`. Unless a case names another date, the offence date is 1 June 2026 and the vehicle has a valid matching licence.

## Boundaries

| Boundary | On the edge | Just across the edge | Cases |
| --- | --- | --- | --- |
| Overspeed bands | 10, 20, 40 | 11, 21, 41 | TC-BVA-01 to TC-BVA-06 |
| Zone limit, school | Speed 25 (not an offence) | Speed 26 (overspeed 1) | TC-BVA-07, TC-BVA-08 |
| Heavy surcharge on the 10 km/h band | Overspeed 10, base 500, calculated 750 | — | TC-BVA-09 |
| Repeat window | Prior offence 180 days before | Prior offence 181 days before | TC-BVA-10, TC-BVA-11 |
| Dispute window | Offence + 15 days | Offence + 16 days | TC-BVA-12, TC-BVA-13 |
| Early payment | Offence + 7 days | Offence + 8 days | TC-BVA-14, TC-BVA-15 |
| Due date | Offence + 30 days (0 days late) | Due date + 1 (1 day late) | TC-BVA-16, TC-BVA-17 |
| Late 25% band | 30 days late | 31 days late | TC-BVA-18, TC-BVA-19 |
| Late 50% / 100% bands | 60 days late | 61 days late | TC-BVA-20, TC-BVA-21 |
| Clearance | Unpaid total 5000 | Unpaid total 5001 | TC-BVA-22, TC-BVA-23 |
| Half-up at .5 | 25% of 750 = 187.5 → 188 | — | TC-BVA-24 |

Speed references for a private car, unless noted:

| Zone | Limit | Speed | Overspeed | Band fine |
| --- | ---: | ---: | ---: | ---: |
| City | 50 | 60 | 10 | 500 |
| City | 50 | 61 | 11 | 1500 |
| Highway | 80 | 100 | 20 | 1500 |
| Highway | 80 | 101 | 21 | 3000 |
| Expressway | 100 | 140 | 40 | 3000 |
| Expressway | 100 | 141 | 41 | 5000 and suspension recommended |
| School zone | 25 | 25 | 0 | Rejected |
| School zone | 25 | 26 | 1 | 500 |

## Test cases

| ID | Requirement | Preconditions | Input | Steps | Expected result | Technique | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-BVA-01 | REQ-FINE-02 | Private car, no prior challan | City, speed 60, 1 Jun 2026 | 1. Issue overspeeding. | Calculated fine 500. `suspension_recommended` false. | BVA | High |
| TC-BVA-02 | REQ-FINE-02 | Private car, no prior challan | City, speed 61, 1 Jun 2026 | 1. Issue overspeeding. | Calculated fine 1500. `suspension_recommended` false. Build B1 returned 500 (DEF-01). Build B2 returns 1500. | BVA | High |
| TC-BVA-03 | REQ-FINE-02 | Private car, no prior challan | Highway, speed 100, 1 Jun 2026 | 1. Issue overspeeding. | Calculated fine 1500. `suspension_recommended` false. | BVA | High |
| TC-BVA-04 | REQ-FINE-02 | Private car, no prior challan | Highway, speed 101, 1 Jun 2026 | 1. Issue overspeeding. | Calculated fine 3000. `suspension_recommended` false. Build B1 returned 1500 (DEF-01). Build B2 returns 3000. | BVA | High |
| TC-BVA-05 | REQ-FINE-02 | Private car, no prior challan | Expressway, speed 140, 1 Jun 2026 | 1. Issue overspeeding. | Calculated fine 3000. `suspension_recommended` false. This edge stayed correct on Build B1 because overspeed 40 was still inside the faulty upper bound. | BVA | High |
| TC-BVA-06 | REQ-FINE-02, REQ-FINE-05 | Two-wheeler, no prior challan | Expressway, speed 141, 1 Jun 2026 | 1. Issue overspeeding. | Calculated fine 5000. No surcharge. `suspension_recommended` true. Build B1 returned 3000 and did not recommend suspension (DEF-01). Build B2 matches this result. | BVA | High |
| TC-BVA-07 | REQ-CH-02 | Private car | School zone, speed 25, 1 Jun 2026 | 1. Issue overspeeding. | Rejected. Nothing is stored. | BVA | High |
| TC-BVA-08 | REQ-FINE-02 | Private car | School zone, speed 26, 1 Jun 2026 | 1. Issue overspeeding. | Overspeed 1, band 1–10, calculated fine 500. `suspension_recommended` false. | BVA | High |
| TC-BVA-09 | REQ-FINE-04 | Heavy vehicle, no prior challan | City, speed 60, 1 Jun 2026 | 1. Issue overspeeding. | Base 500. Surcharge 250. Calculated fine 750. `suspension_recommended` false. | BVA | High |
| TC-BVA-10 | REQ-FINE-03 | Private car. Signal jump already issued on 3 Dec 2025 | Signal jump on 1 Jun 2026 | 1. Issue the second challan. | The prior date is 180 days before. Repeat applies. Calculated fine 2000. | BVA | High |
| TC-BVA-11 | REQ-FINE-03 | Private car. Signal jump already issued on 2 Dec 2025 | Signal jump on 1 Jun 2026 | 1. Issue the second challan. | The prior date is 181 days before. Repeat does not apply. Calculated fine 1000. | BVA | High |
| TC-BVA-12 | REQ-DIS-01 | Issued signal-jump challan, offence 1 Jun 2026, fine 1000 | Dispute date 16 Jun 2026 | 1. Dispute the challan. | Status becomes Disputed. Day 15 of the window is accepted. | BVA | High |
| TC-BVA-13 | REQ-DIS-01 | Issued signal-jump challan, offence 1 Jun 2026 | Dispute date 17 Jun 2026 | 1. Dispute the challan. | Rejected. Status stays Issued. Build B1 moved it to Disputed (DEF-04). Build B2 leaves it Issued. | BVA | High |
| TC-BVA-14 | REQ-PAY-01 | Issued private signal jump, fine 1000, suspension false, not drunk driving | Payment date 8 Jun 2026, amount 900 | 1. Read the payable amount. 2. Pay 900. | Payable is 900 (10% of 1000). Status becomes Paid. Amount paid is 900. | BVA | High |
| TC-BVA-15 | REQ-PAY-02 | Same challan shape, still Issued | Payment date 9 Jun 2026, amount 1000 | 1. Read the payable amount. 2. Pay 1000. | Day 8 has no discount. Payable is 1000. Status becomes Paid. | BVA | High |
| TC-BVA-16 | REQ-PAY-02 | Issued private signal jump, due 1 Jul 2026 | Payment date 1 Jul 2026, amount 1000 | 1. Confirm the due date. 2. Pay 1000. | The due date is not late. Payable is 1000. Status becomes Paid. | BVA | High |
| TC-BVA-17 | REQ-PAY-03 | Issued private signal jump, due 1 Jul 2026. Status is still Issued | Payment date 2 Jul 2026, amount 1250 | 1. Read the payable amount. 2. Pay 1250. | 1 day late, penalty 25% = 250, payable 1250. Status becomes Paid. | BVA | High |
| TC-BVA-18 | REQ-PAY-03 | Issued private signal jump, due 1 Jul 2026 | Payment date 31 Jul 2026 | 1. Read the payable amount. | 30 days late is still the 25% band. Payable is 1250. | BVA | High |
| TC-BVA-19 | REQ-PAY-03 | Issued private signal jump, due 1 Jul 2026 | Payment date 1 Aug 2026 | 1. Read the payable amount. | 31 days late is the 50% band. Payable is 1500. | BVA | High |
| TC-BVA-20 | REQ-PAY-03 | Issued private signal jump, due 1 Jul 2026 | Payment date 30 Aug 2026 | 1. Read the payable amount. | 60 days late is still the 50% band. Payable is 1500. | BVA | High |
| TC-BVA-21 | REQ-PAY-03 | Issued private signal jump, due 1 Jul 2026 | Payment date 31 Aug 2026, amount 2000 | 1. Read the payable amount. 2. Pay 2000. | 61 days late is a 100% penalty. Payable is 2000, which is the cap of 2 × 1000. Status becomes Paid. | BVA | High |
| TC-BVA-22 | REQ-REG-04, REQ-REP-01 | Private car MH01AA0001, valid licence, no earlier challans | On 1 Apr 2026: no insurance, and expressway speed 140. Then register MH01AA0002 on 1 Apr 2026 | 1. Issue both challans. 2. Read the unpaid total. 3. Register the second vehicle. 4. Open the clearance report. | Fines are 2000 and 3000. They share a date, so neither is a prior of the other, and suspension is false. Unpaid total is 5000. `clearance_blocked` is false. MH01AA0002 is stored. The clearance report is empty. Build B1 blocked this owner (DEF-02). Build B2 allows the vehicle. | BVA | High |
| TC-BVA-23 | REQ-REG-04, REQ-REP-01 | Three vehicles of OWN1, registered before the offences: MH12PR1001 Private car, MH12CO1001 Commercial, MH12HV1001 Heavy. Valid licences | All on 1 May 2026: commercial mobile use; private signal jump; heavy vehicle, city, speed 60. Clearance date 1 Jun 2026. Attempt to register MH12PR1002 | 1. Issue the three challans. 2. Mark them overdue on 1 Jun 2026. 3. Read each payable amount and the unpaid total. 4. Register MH12PR1002. 5. Open the clearance report. | Calculated fines 2250, 1000, and 750. Due date is 31 May 2026, so 1 Jun is 1 day late. Payables: 2250 + half-up(25% of 2250 = 562.5 → 563) = 2813; 1000 + 250 = 1250; 750 + half-up(187.5 → 188) = 938. Total 5001. Registration is rejected. `clearance_blocked` is true. The clearance report lists OWN1. MH12PR1002 is not stored. | BVA | High |
| TC-BVA-24 | REQ-FINE-04, REQ-PAY-03 | Heavy vehicle, no prior challan | City, speed 60, offence 1 Jun 2026. Payment date 2 Jul 2026 | 1. Issue the challan. 2. Read 25% of 750. 3. Read the payable amount. | Calculated fine 750. 25% rounds half-up from 187.5 to 188. Payable is 938. | BVA | High |
