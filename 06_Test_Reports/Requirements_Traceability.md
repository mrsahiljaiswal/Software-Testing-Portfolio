# Requirements Traceability

Every requirement in the test plan is linked to at least one test. The final result of every manual case is Pass.

| Requirement | Rule | Tests |
| --- | --- | --- |
| REQ-REG-01 | Vehicle number required, stored uppercase, and unique | `test_registration_required_and_stored_uppercase`, `test_duplicate_registration_rejected` |
| REQ-FINE-01 | Signal jump is ₹500 for either vehicle | TC-EP-01, TC-EP-02, TC-DT-01 |
| REQ-FINE-02 | No helmet is ₹1000 for a Two-wheeler and is rejected for a Car | TC-EP-03, TC-EP-04, TC-DT-02, TC-DT-03, TC-BVA-07 |
| REQ-FINE-03 | Limit 60. Reject 60 or below. ₹500 from 61 to 80. ₹2000 from 81. | TC-EP-05, TC-EP-06, TC-EP-07, TC-EP-08, TC-BVA-01, TC-BVA-02, TC-BVA-03, TC-BVA-04, TC-DT-04 |
| REQ-PAY-01 | Due date is challan date + 15 days. On time, pay the fine. | TC-EP-01, TC-BVA-05, TC-DT-05, TC-ST-01 |
| REQ-PAY-02 | After the due date, pay the fine + ₹200 | TC-BVA-06, TC-BVA-07, TC-DT-06, TC-ST-03 |
| REQ-PAY-03 | A short payment is rejected. A paid challan cannot be paid again. | TC-BVA-08, TC-ST-04 |
| REQ-ST-01 | Issued → Paid, Issued → Overdue, Overdue → Paid. Other moves rejected. | TC-ST-01, TC-ST-02, TC-ST-03, TC-ST-04, TC-ST-05, TC-ST-06 |

## Manual cases, each listed once as its main requirement

| Case | Main requirement | Automated method |
| --- | --- | --- |
| TC-EP-01 | REQ-FINE-01 | `test_TC_EP_01_two_wheeler_signal_jump` |
| TC-EP-02 | REQ-FINE-01 | `test_TC_EP_02_car_signal_jump` |
| TC-EP-03 | REQ-FINE-02 | `test_TC_EP_03_two_wheeler_no_helmet` |
| TC-EP-04 | REQ-FINE-02 | `test_TC_EP_04_DEF_02_car_no_helmet_rejected` |
| TC-EP-05 | REQ-FINE-03 | `test_TC_EP_05_speed_within_limit_rejected` |
| TC-EP-06 | REQ-FINE-03 | `test_TC_EP_06_speed_slightly_over` |
| TC-EP-07 | REQ-FINE-03 | `test_TC_EP_07_speed_well_over` |
| TC-EP-08 | REQ-FINE-03 | `test_TC_EP_08_car_speed_within_limit_rejected` |
| TC-BVA-01 | REQ-FINE-03 | `test_TC_BVA_01_DEF_01_speed_60_rejected` |
| TC-BVA-02 | REQ-FINE-03 | `test_TC_BVA_02_speed_61_fine_500` |
| TC-BVA-03 | REQ-FINE-03 | `test_TC_BVA_03_speed_80_fine_500` |
| TC-BVA-04 | REQ-FINE-03 | `test_TC_BVA_04_speed_81_fine_2000` |
| TC-BVA-05 | REQ-PAY-01 | `test_TC_BVA_05_pay_on_due_date` |
| TC-BVA-06 | REQ-PAY-02 | `test_TC_BVA_06_DEF_03_day_after_due_adds_200` |
| TC-BVA-07 | REQ-PAY-02 | `test_TC_BVA_07_late_fee_is_200_on_helmet_fine` |
| TC-BVA-08 | REQ-PAY-03 | `test_TC_BVA_08_one_rupee_short_of_late_amount_rejected` |
| TC-DT-01 | REQ-FINE-01 | `test_TC_DT_01_rule_a1_signal_jump_accepted` |
| TC-DT-02 | REQ-FINE-02 | `test_TC_DT_02_rule_a2_helmet_two_wheeler_accepted` |
| TC-DT-03 | REQ-FINE-02 | `test_TC_DT_03_rule_a3_helmet_car_rejected` |
| TC-DT-04 | REQ-FINE-03 | `test_TC_DT_04_rule_a4_speed_at_or_below_60_rejected` |
| TC-DT-05 | REQ-PAY-01 | `test_TC_DT_05_rule_b1_on_time_amount_is_the_fine` |
| TC-DT-06 | REQ-PAY-02 | `test_TC_DT_06_rule_b2_late_amount_is_fine_plus_200` |
| TC-ST-01 | REQ-ST-01 | `test_TC_ST_01_issued_to_paid_on_time` |
| TC-ST-02 | REQ-ST-01 | `test_TC_ST_02_issued_to_overdue_after_due_date` |
| TC-ST-03 | REQ-ST-01 | `test_TC_ST_03_overdue_to_paid_late_amount` |
| TC-ST-04 | REQ-ST-01 | `test_TC_ST_04_paid_cannot_be_paid_again` |
| TC-ST-05 | REQ-ST-01 | `test_TC_ST_05_overdue_cannot_return_to_issued` |
| TC-ST-06 | REQ-ST-01 | `test_TC_ST_06_paid_cannot_become_overdue` |

That is 8 + 8 + 6 + 6 = 28 manual cases, plus the two REQ-REG-01 methods, which is the 30 automated tests.

## Defects

| Defect | Requirement | Discovering case | Status |
| --- | --- | --- | --- |
| DEF-01 | REQ-FINE-03 | TC-BVA-01 | Closed |
| DEF-02 | REQ-FINE-02 | TC-EP-04 | Closed |
| DEF-03 | REQ-PAY-02 | TC-BVA-06 | Closed |
