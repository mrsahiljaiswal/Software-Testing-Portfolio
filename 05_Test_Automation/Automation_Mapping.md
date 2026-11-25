# Automation Mapping — VTFMS

Each automated method lives in `05_Test_Automation/traffic_system/test_traffic.py`.
There are 92 methods: 77 map to one manual case, and 15 are additional regression checks.
The additional checks are not extra manual cases. The manual total remains 77.

The five fixed defects are locked by these methods:

| Defect | Methods |
| --- | --- |
| DEF-01 | `test_TC_BVA_02_overspeed_11`, `test_TC_BVA_04_overspeed_21`, `test_TC_BVA_06_overspeed_41_two_wheeler` |
| DEF-02 | `test_TC_BVA_22_unpaid_5000_does_not_block` (paired with `test_TC_BVA_23_unpaid_5001_blocks_registration`) |
| DEF-03 | `test_TC_EP_11_helmet_on_private_car_rejected`, `test_TC_DT_02_category_mismatch_rejects_helmet_on_commercial` |
| DEF-04 | `test_TC_BVA_13_dispute_on_day_16_rejected` |
| DEF-05 | `test_TC_DT_08_drunk_driving_has_no_early_discount` |

## Manual cases

| Automated method | Manual case | Result |
| --- | --- | --- |
| `test_TC_EP_01_registration_stored_uppercase` | TC-EP-01 | Pass |
| `test_TC_EP_02_empty_registration_rejected` | TC-EP-02 | Pass |
| `test_TC_EP_03_duplicate_registration_rejected` | TC-EP-03 | Pass |
| `test_TC_EP_04_unknown_owner_rejected` | TC-EP-04 | Pass |
| `test_TC_EP_05_licence_valid_on_expiry_date` | TC-EP-05 | Pass |
| `test_TC_EP_06_expired_licence_flags_without_extra_fine` | TC-EP-06 | Pass |
| `test_TC_EP_07_suspended_licence_stays_suspended_after_payment` | TC-EP-07 | Pass |
| `test_TC_EP_08_wrong_licence_class_flags_challan` | TC-EP-08 | Pass |
| `test_TC_EP_09_private_first_signal_jump` | TC-EP-09 | Pass |
| `test_TC_EP_10_helmet_on_two_wheeler` | TC-EP-10 | Pass |
| `test_TC_EP_11_helmet_on_private_car_rejected` | TC-EP-11 | Pass |
| `test_TC_EP_12_seatbelt_on_two_wheeler_rejected` | TC-EP-12 | Pass |
| `test_TC_EP_13_speed_below_limit_rejected` | TC-EP-13 | Pass |
| `test_TC_EP_14_drunk_driving_recommends_suspension` | TC-EP-14 | Pass |
| `test_TC_EP_15_commercial_first_signal_jump` | TC-EP-15 | Pass |
| `test_TC_EP_16_commercial_repeat_signal_jump` | TC-EP-16 | Pass |
| `test_TC_EP_20_third_challan_recommends_suspension_without_repeat` | TC-EP-20 | Pass |
| `test_TC_EP_17_pending_report_omits_paid` | TC-EP-17 | Pass |
| `test_TC_EP_18_overdue_report_lists_only_overdue_status` | TC-EP-18 | Pass |
| `test_TC_EP_19_repeat_offender_report` | TC-EP-19 | Pass |
| `test_TC_BVA_01_overspeed_10` | TC-BVA-01 | Pass |
| `test_TC_BVA_02_overspeed_11` | TC-BVA-02 | Pass |
| `test_TC_BVA_03_overspeed_20` | TC-BVA-03 | Pass |
| `test_TC_BVA_04_overspeed_21` | TC-BVA-04 | Pass |
| `test_TC_BVA_05_overspeed_40` | TC-BVA-05 | Pass |
| `test_TC_BVA_06_overspeed_41_two_wheeler` | TC-BVA-06 | Pass |
| `test_TC_BVA_07_school_speed_equal_to_limit_rejected` | TC-BVA-07 | Pass |
| `test_TC_BVA_08_school_speed_one_over_limit` | TC-BVA-08 | Pass |
| `test_TC_BVA_09_heavy_overspeed_10_with_surcharge` | TC-BVA-09 | Pass |
| `test_TC_BVA_10_repeat_on_day_180` | TC-BVA-10 | Pass |
| `test_TC_BVA_11_no_repeat_on_day_181` | TC-BVA-11 | Pass |
| `test_TC_BVA_12_dispute_on_day_15` | TC-BVA-12 | Pass |
| `test_TC_BVA_13_dispute_on_day_16_rejected` | TC-BVA-13 | Pass |
| `test_TC_BVA_14_early_payment_on_day_7` | TC-BVA-14 | Pass |
| `test_TC_BVA_15_payment_on_day_8_has_no_discount` | TC-BVA-15 | Pass |
| `test_TC_BVA_16_payment_on_due_date` | TC-BVA-16 | Pass |
| `test_TC_BVA_17_one_day_late` | TC-BVA-17 | Pass |
| `test_TC_BVA_18_thirty_days_late` | TC-BVA-18 | Pass |
| `test_TC_BVA_19_thirty_one_days_late` | TC-BVA-19 | Pass |
| `test_TC_BVA_20_sixty_days_late` | TC-BVA-20 | Pass |
| `test_TC_BVA_21_sixty_one_days_late_capped_at_double` | TC-BVA-21 | Pass |
| `test_TC_BVA_22_unpaid_5000_does_not_block` | TC-BVA-22 | Pass |
| `test_TC_BVA_23_unpaid_5001_blocks_registration` | TC-BVA-23 | Pass |
| `test_TC_BVA_24_late_penalty_rounds_half_up` | TC-BVA-24 | Pass |
| `test_TC_DT_01_valid_challan_with_valid_licence` | TC-DT-01 | Pass |
| `test_TC_DT_02_category_mismatch_rejects_helmet_on_commercial` | TC-DT-02 | Pass |
| `test_TC_DT_03_speed_equal_to_city_limit_rejected` | TC-DT-03 | Pass |
| `test_TC_DT_04_duplicate_same_vehicle_type_and_date` | TC-DT-04 | Pass |
| `test_TC_DT_05_unregistered_vehicle_rejected` | TC-DT-05 | Pass |
| `test_TC_DT_06_invalid_licence_still_records_mobile_use` | TC-DT-06 | Pass |
| `test_TC_DT_07_early_discount_when_all_conditions_hold` | TC-DT-07 | Pass |
| `test_TC_DT_08_drunk_driving_has_no_early_discount` | TC-DT-08 | Pass |
| `test_TC_DT_09_suspension_recommendation_blocks_early_discount` | TC-DT-09 | Pass |
| `test_TC_DT_10_full_fine_inside_due_date_after_early_window` | TC-DT-10 | Pass |
| `test_TC_DT_11_twenty_five_percent_late_penalty` | TC-DT-11 | Pass |
| `test_TC_DT_12_fifty_percent_late_penalty` | TC-DT-12 | Pass |
| `test_TC_DT_13_hundred_percent_late_penalty_hits_cap` | TC-DT-13 | Pass |
| `test_TC_DT_14_disputed_challan_cannot_be_paid` | TC-DT-14 | Pass |
| `test_TC_DT_15_partial_amount_rejected` | TC-DT-15 | Pass |
| `test_TC_DT_16_upheld_challan_has_no_early_discount` | TC-DT-16 | Pass |
| `test_TC_ST_01_draft_to_issued` | TC-ST-01 | Pass |
| `test_TC_ST_02_issued_to_paid` | TC-ST-02 | Pass |
| `test_TC_ST_03_issued_to_disputed_on_offence_date` | TC-ST-03 | Pass |
| `test_TC_ST_04_issued_to_overdue_after_due_date` | TC-ST-04 | Pass |
| `test_TC_ST_05_overdue_to_paid` | TC-ST-05 | Pass |
| `test_TC_ST_06_disputed_to_dismissed` | TC-ST-06 | Pass |
| `test_TC_ST_07_disputed_to_upheld` | TC-ST-07 | Pass |
| `test_TC_ST_08_upheld_to_paid` | TC-ST-08 | Pass |
| `test_TC_ST_09_paid_is_terminal` | TC-ST-09 | Pass |
| `test_TC_ST_10_dismissed_is_terminal` | TC-ST-10 | Pass |
| `test_TC_ST_11_draft_to_paid_rejected` | TC-ST-11 | Pass |
| `test_TC_ST_12_draft_to_disputed_rejected` | TC-ST-12 | Pass |
| `test_TC_ST_13_draft_to_overdue_rejected` | TC-ST-13 | Pass |
| `test_TC_ST_14_issued_to_dismissed_rejected` | TC-ST-14 | Pass |
| `test_TC_ST_15_overdue_to_disputed_rejected` | TC-ST-15 | Pass |
| `test_TC_ST_16_disputed_to_paid_rejected` | TC-ST-16 | Pass |
| `test_TC_ST_17_overdue_on_due_date_rejected` | TC-ST-17 | Pass |

## Additional regression checks

| Automated method | Manual case | What it locks | Result |
| --- | --- | --- | --- |
| `test_extra_missing_licence_is_invalid_flag` | — | REQ-LIC-02. No licence on file sets licence_invalid and does not add a fine. | Pass |
| `test_extra_status_expired_is_invalid_even_with_future_expiry` | — | REQ-LIC-01. Status Expired is invalid even when the expiry date is in the future. | Pass |
| `test_extra_duplicate_owner_rejected` | — | REQ-REG-01. A second registration of the same owner id is rejected. | Pass |
| `test_extra_seatbelt_on_heavy_is_allowed` | — | REQ-CH-01. No seatbelt is allowed on a Heavy vehicle. Fine is 1000 plus 50% = 1500. | Pass |
| `test_extra_blocked_owner_can_still_receive_a_challan` | — | REQ-REG-04. Clearance block stops a new vehicle only. A challan can still be issued. | Pass |
| `test_extra_dismissed_prior_does_not_repeat` | — | REQ-FINE-03. A dismissed prior challan does not double the next fine. | Pass |
| `test_extra_draft_does_not_count_as_repeat` | — | REQ-FINE-03. A draft prior challan does not double the next fine. | Pass |
| `test_extra_paid_prior_still_counts_as_repeat` | — | REQ-FINE-03. A paid prior challan still counts as a repeat. | Pass |
| `test_extra_disputed_prior_counts_as_repeat` | — | REQ-FINE-03. A disputed prior challan still counts as a repeat. | Pass |
| `test_extra_duplicate_overspeed_ignores_zone` | — | REQ-CH-03. A second overspeeding challan on the same vehicle and date is rejected even in another zone. | Pass |
| `test_extra_negative_speed_rejected` | — | REQ-CH-02. A negative recorded speed is rejected. | Pass |
| `test_extra_clearance_unblocks_when_total_falls_to_5000_or_below` | — | REQ-REG-04. After a payment brings the unpaid total from 5001 to 3751, clearance_blocked becomes false. | Pass |
| `test_extra_percent_half_up_ties_round_away_from_zero` | — | REQ-FINE-04 and REQ-PAY-03. 25% of 750 is 188 and 25% of 2250 is 563. | Pass |
| `test_extra_dispute_before_offence_date_rejected` | — | REQ-DIS-01. A dispute dated before the offence date is rejected. | Pass |
| `test_extra_draft_blocks_second_challan_same_day` | — | REQ-CH-03. An unsubmitted draft blocks another challan for the same vehicle, type, and date. | Pass |

Mapped manual methods: 77. Additional methods: 15. Total: 92.
