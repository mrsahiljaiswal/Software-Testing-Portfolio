# Automation Mapping

Each manual case has one unittest method. Two extra methods cover registration. The three regression methods are marked in the Defect column. There are 30 methods, matching `Ran 30 tests`.

| Method | Manual case | Requirement | Defect |
| --- | --- | --- | --- |
| `test_TC_EP_01_two_wheeler_signal_jump` | TC-EP-01 | REQ-FINE-01, REQ-PAY-01 | |
| `test_TC_EP_02_car_signal_jump` | TC-EP-02 | REQ-FINE-01 | |
| `test_TC_EP_03_two_wheeler_no_helmet` | TC-EP-03 | REQ-FINE-02 | |
| `test_TC_EP_04_DEF_02_car_no_helmet_rejected` | TC-EP-04 | REQ-FINE-02 | DEF-02 |
| `test_TC_EP_05_speed_within_limit_rejected` | TC-EP-05 | REQ-FINE-03 | |
| `test_TC_EP_06_speed_slightly_over` | TC-EP-06 | REQ-FINE-03 | |
| `test_TC_EP_07_speed_well_over` | TC-EP-07 | REQ-FINE-03 | |
| `test_TC_EP_08_car_speed_within_limit_rejected` | TC-EP-08 | REQ-FINE-03 | |
| `test_TC_BVA_01_DEF_01_speed_60_rejected` | TC-BVA-01 | REQ-FINE-03 | DEF-01 |
| `test_TC_BVA_02_speed_61_fine_500` | TC-BVA-02 | REQ-FINE-03 | |
| `test_TC_BVA_03_speed_80_fine_500` | TC-BVA-03 | REQ-FINE-03 | |
| `test_TC_BVA_04_speed_81_fine_2000` | TC-BVA-04 | REQ-FINE-03 | |
| `test_TC_BVA_05_pay_on_due_date` | TC-BVA-05 | REQ-PAY-01 | |
| `test_TC_BVA_06_DEF_03_day_after_due_adds_200` | TC-BVA-06 | REQ-PAY-02 | DEF-03 |
| `test_TC_BVA_07_late_fee_is_200_on_helmet_fine` | TC-BVA-07 | REQ-PAY-02 | |
| `test_TC_BVA_08_one_rupee_short_of_late_amount_rejected` | TC-BVA-08 | REQ-PAY-03 | |
| `test_TC_DT_01_rule_a1_signal_jump_accepted` | TC-DT-01, Rule A1 | REQ-FINE-01 | |
| `test_TC_DT_02_rule_a2_helmet_two_wheeler_accepted` | TC-DT-02, Rule A2 | REQ-FINE-02 | |
| `test_TC_DT_03_rule_a3_helmet_car_rejected` | TC-DT-03, Rule A3 | REQ-FINE-02 | |
| `test_TC_DT_04_rule_a4_speed_at_or_below_60_rejected` | TC-DT-04, Rule A4 | REQ-FINE-03 | |
| `test_TC_DT_05_rule_b1_on_time_amount_is_the_fine` | TC-DT-05, Rule B1 | REQ-PAY-01 | |
| `test_TC_DT_06_rule_b2_late_amount_is_fine_plus_200` | TC-DT-06, Rule B2 | REQ-PAY-02 | |
| `test_TC_ST_01_issued_to_paid_on_time` | TC-ST-01 | REQ-ST-01, REQ-PAY-01 | |
| `test_TC_ST_02_issued_to_overdue_after_due_date` | TC-ST-02 | REQ-ST-01 | |
| `test_TC_ST_03_overdue_to_paid_late_amount` | TC-ST-03 | REQ-ST-01, REQ-PAY-02 | |
| `test_TC_ST_04_paid_cannot_be_paid_again` | TC-ST-04 | REQ-ST-01, REQ-PAY-03 | |
| `test_TC_ST_05_overdue_cannot_return_to_issued` | TC-ST-05 | REQ-ST-01 | |
| `test_TC_ST_06_paid_cannot_become_overdue` | TC-ST-06 | REQ-ST-01 | |
| `test_registration_required_and_stored_uppercase` | — | REQ-REG-01 | |
| `test_duplicate_registration_rejected` | — | REQ-REG-01 | |

28 manual rows + 2 registration rows = 30. The Defect column names the three regression tests.
