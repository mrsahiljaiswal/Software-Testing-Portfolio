# Decision Tables — VTFMS

## Technique

A decision table lists the conditions that change the outcome and gives one rule to each combination the team will test. Each test case below cites the rule it exercises. The baseline is `01_Test_Plan/Test_Plan.md`.

“—” means the condition is irrelevant because an earlier condition already rejects the action.

## Table A — Recording a challan

| Condition | R1 | R2 | R3 | R4 | R5 | R6 |
| --- | --- | --- | --- | --- | --- | --- |
| C1. Vehicle is registered | Y | Y | Y | Y | N | Y |
| C2. Violation is permitted for the category | Y | N | Y | Y | — | Y |
| C3. Speed is above the limit, or the violation is not overspeeding | Y | — | N | Y | — | Y |
| C4. No challan already exists for the same vehicle, type, and date | Y | — | — | N | — | Y |
| C5. Licence is valid for the class on the offence date | Y | — | — | — | — | N |
| Record the challan | Yes | No | No | No | No | Yes |
| `licence_invalid` | false | — | — | — | — | true |

R2 covers a category mismatch such as no helmet on a commercial vehicle. R3 covers speed at or below the limit. R6 shows that an invalid licence does not cancel the offence.

## Table B — Payment

| Condition | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1. Status is Issued, Overdue, or Upheld | Issued | Issued | Issued | Issued | Issued | Issued | Issued | No | Issued | Upheld |
| C2. Payment date ≤ offence + 7 | Y | Y | Y | N | N | N | N | — | Y | Y |
| C3. Drunk driving | N | Y | N | N | N | N | N | — | N | N |
| C4. `suspension_recommended` | N | Y | Y | N | N | N | N | — | N | N |
| C5. Payment date ≤ due date | Y | Y | Y | Y | N | N | N | — | Y | Y |
| Days late | — | — | — | — | 1–30 | 31–60 | 61+ | — | — | — |
| C7. Amount equals the computed payable | Y | Y | Y | Y | Y | Y | Y | — | N | Y |
| Discount 10% | Yes | No | No | No | No | No | No | No | — | No |
| Penalty | 0 | 0 | 0 | 0 | 25% | 50% | 100% | — | — | 0 |
| Result | Pay | Pay | Pay | Pay | Pay | Pay | Pay, cap 2× | Reject | Reject | Pay full fine |

## Test cases

The standard precondition, unless the case says otherwise, is owner OWN1, a registered vehicle, a valid matching licence, and offence date 1 June 2026.

| ID | Requirement | Preconditions | Input | Steps | Expected result | Technique | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-DT-01 | REQ-CH-01, REQ-LIC-01 | Rule R1. Private car MH01AB1001, valid LMV licence | Signal jump | 1. Issue the challan. | Status Issued. Fine 1000. `licence_invalid` false. | Decision table R1 | High |
| TC-DT-02 | REQ-CH-01 | Rule R2. Commercial vehicle, valid COM licence | No helmet | 1. Issue the challan. | Rejected. Nothing is stored. Build B1 accepted it (DEF-03). Build B2 rejects it. | Decision table R2 | High |
| TC-DT-03 | REQ-CH-02 | Rule R3. Private car | City, speed 50 | 1. Issue overspeeding. | Rejected. Speed equal to the limit is not an offence. Nothing is stored. | Decision table R3 | High |
| TC-DT-04 | REQ-CH-03 | Rule R4. Private car. A signal jump for 1 Jun 2026 is already Issued | A second signal jump on 1 Jun 2026 | 1. Issue the second challan. | Rejected. Only one challan is stored. | Decision table R4 | High |
| TC-DT-05 | REQ-REG-03 | Rule R5. Vehicle MH99ZZ9999 is not registered | Signal jump | 1. Issue the challan. | Rejected. Nothing is stored. | Decision table R5 | High |
| TC-DT-06 | REQ-LIC-02, REQ-FINE-01 | Rule R6. Private car. LMV licence expired on 31 May 2026 | Mobile use | 1. Issue the challan. | Status Issued. Fine 1500. `licence_invalid` true. | Decision table R6 | High |
| TC-DT-07 | REQ-PAY-01 | Rule P1. Issued private signal jump, fine 1000, suspension false | Pay on 4 Jun 2026, amount 900 | 1. Read the payable amount. 2. Pay 900. | Discount applies. Payable 900. Status Paid. | Decision table P1 | High |
| TC-DT-08 | REQ-PAY-01, REQ-FINE-05 | Rule P2. Issued drunk-driving challan, fine 10000, suspension true | Pay on 2 Jun 2026. First tender 9000, then tender 10000 | 1. Read the payable amount. 2. Tender 9000. 3. Tender 10000. | Payable is 10000. 9000 is rejected and the status stays Issued. 10000 is accepted and the status becomes Paid. The licence stays Active. Build B1 accepted 9000 (DEF-05). Build B2 rejects it. | Decision table P2 | High |
| TC-DT-09 | REQ-PAY-01, REQ-FINE-05 | Rule P3. Two-wheeler, expressway speed 141, fine 5000, suspension true | Pay on 3 Jun 2026, amount 4500 | 1. Confirm the flag. 2. Read the payable amount. 3. Tender 4500. | Payable is 5000. The discounted amount is rejected. Status stays Issued. | Decision table P3 | High |
| TC-DT-10 | REQ-PAY-02 | Rule P4. Issued private signal jump, fine 1000 | Pay on 21 Jun 2026, amount 1000 | 1. Pay 1000. | No discount and no penalty. Status Paid. | Decision table P4 | High |
| TC-DT-11 | REQ-PAY-03 | Rule P5. Issued private signal jump, due 1 Jul 2026 | Pay on 11 Jul 2026 (10 days late), amount 1250 | 1. Read the payable amount. 2. Pay 1250. | Penalty 250. Payable 1250. Status Paid. | Decision table P5 | High |
| TC-DT-12 | REQ-PAY-03 | Rule P6. Issued private signal jump, due 1 Jul 2026 | Pay on 15 Aug 2026 (45 days late), amount 1500 | 1. Read the payable amount. 2. Pay 1500. | Penalty 50%. Payable 1500. Status Paid. | Decision table P6 | High |
| TC-DT-13 | REQ-PAY-03 | Rule P7. Issued private signal jump, due 1 Jul 2026 | Pay on 29 Sep 2026 (90 days late), amount 2000 | 1. Read the payable amount. 2. Pay 2000. | Penalty 100% reaches the cap. Payable 2000. Status Paid. | Decision table P7 | High |
| TC-DT-14 | REQ-PAY-05, REQ-DIS-02 | Rule P8. Signal jump disputed on 1 Jun 2026 | Pay on 2 Jun 2026, amount 900 | 1. Dispute. 2. Attempt payment. | Payment is rejected. Status stays Disputed. | Decision table P8 | High |
| TC-DT-15 | REQ-PAY-04 | Rule P9. Issued private signal jump. Correct payable on 4 Jun 2026 is 900 | Tender 899 | 1. Attempt payment. | Rejected. Status stays Issued. Amount paid stays empty. | Decision table P9 | High |
| TC-DT-16 | REQ-PAY-06 | Rule P10. Signal jump disputed on 2 Jun 2026 and reviewed Upheld | Pay on 5 Jun 2026. First tender 900, then tender 1000 | 1. Dispute and uphold. 2. Tender 900. 3. Tender 1000. | Early discount is not available. 900 is rejected. 1000 is accepted. Status becomes Paid. | Decision table P10 | High |
