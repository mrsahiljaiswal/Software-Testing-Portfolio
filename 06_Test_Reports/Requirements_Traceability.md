# Requirements Traceability — VTFMS

Each requirement is taken from section 4 of `01_Test_Plan/Test_Plan.md`. The result column is the final manual result on Build B2 (20 November 2026) and the automated result on 24 November 2026. Both are Pass for every row.

Additional automated methods that have no manual ID are listed in `05_Test_Automation/Automation_Mapping.md`. They do not change the manual count of 77.

| Requirement | Rule in short | Manual cases | Automated methods | Result |
| --- | --- | --- | --- | --- |
| REQ-REG-01 | Owner id is unique and named | TC-EP-01 | `test_TC_EP_01_registration_stored_uppercase`, `test_extra_duplicate_owner_rejected` | Pass |
| REQ-REG-02 | Registration number unique, non-empty, uppercase | TC-EP-01, TC-EP-02, TC-EP-03 | `test_TC_EP_01_registration_stored_uppercase`, `test_TC_EP_02_empty_registration_rejected`, `test_TC_EP_03_duplicate_registration_rejected` | Pass |
| REQ-REG-03 | Owner must exist | TC-EP-04, TC-DT-05 | `test_TC_EP_04_unknown_owner_rejected`, `test_TC_DT_05_unregistered_vehicle_rejected` | Pass |
| REQ-REG-04 | Block only when unpaid total is above 5000 | TC-BVA-22, TC-BVA-23 | `test_TC_BVA_22_unpaid_5000_does_not_block`, `test_TC_BVA_23_unpaid_5001_blocks_registration`, `test_extra_clearance_unblocks_when_total_falls_to_5000_or_below`, `test_extra_blocked_owner_can_still_receive_a_challan` | Pass |
| REQ-LIC-01 | Valid only if Active, unexpired, and the right class | TC-EP-05, TC-EP-06, TC-EP-08 | `test_TC_EP_05_licence_valid_on_expiry_date`, `test_TC_EP_06_expired_licence_flags_without_extra_fine`, `test_extra_status_expired_is_invalid_even_with_future_expiry` | Pass |
| REQ-LIC-02 | Invalid licence is a flag, not an extra fine, and the offence remains | TC-EP-06, TC-EP-07, TC-EP-08, TC-DT-06 | `test_TC_EP_06_expired_licence_flags_without_extra_fine`, `test_TC_EP_07_suspended_licence_stays_suspended_after_payment`, `test_TC_EP_08_wrong_licence_class_flags_challan`, `test_TC_DT_06_invalid_licence_still_records_mobile_use`, `test_extra_missing_licence_is_invalid_flag` | Pass |
| REQ-LIC-03 | A Suspended licence stays Suspended after payment | TC-EP-07 | `test_TC_EP_07_suspended_licence_stays_suspended_after_payment` | Pass |
| REQ-CH-01 | Helmet and seatbelt category rules | TC-EP-10, TC-EP-11, TC-EP-12, TC-DT-02 | `test_TC_EP_10_helmet_on_two_wheeler`, `test_TC_EP_11_helmet_on_private_car_rejected`, `test_TC_EP_12_seatbelt_on_two_wheeler_rejected`, `test_TC_DT_02_category_mismatch_rejects_helmet_on_commercial`, `test_extra_seatbelt_on_heavy_is_allowed` | Pass |
| REQ-CH-02 | Speed at or below the zone limit is not an offence | TC-EP-13, TC-BVA-07, TC-DT-03 | `test_TC_EP_13_speed_below_limit_rejected`, `test_TC_BVA_07_school_speed_equal_to_limit_rejected`, `test_TC_DT_03_speed_equal_to_city_limit_rejected`, `test_extra_negative_speed_rejected` | Pass |
| REQ-CH-03 | Duplicate vehicle, type, and date, including overspeed across zones | TC-DT-04 | `test_TC_DT_04_duplicate_same_vehicle_type_and_date`, `test_extra_duplicate_overspeed_ignores_zone`, `test_extra_draft_blocks_second_challan_same_day` | Pass |
| REQ-CH-04 | Due date is the offence date plus 30 days | TC-EP-09, TC-ST-01 | `test_TC_EP_09_private_first_signal_jump`, `test_TC_ST_01_draft_to_issued` | Pass |
| REQ-FINE-01 | Flat base fines | TC-EP-09, TC-EP-10, TC-EP-14, TC-EP-15, TC-DT-06 | `test_TC_EP_09_private_first_signal_jump`, `test_TC_EP_10_helmet_on_two_wheeler`, `test_TC_EP_14_drunk_driving_recommends_suspension`, `test_TC_EP_15_commercial_first_signal_jump` | Pass |
| REQ-FINE-02 | Inclusive speed bands 10/11, 20/21, 40/41 | TC-BVA-01 to TC-BVA-08 | `test_TC_BVA_01_overspeed_10` through `test_TC_BVA_08_school_speed_one_over_limit` | Pass |
| REQ-FINE-03 | Repeat ×2 inside 180 days; dismissed and draft do not count | TC-EP-16, TC-EP-19, TC-BVA-10, TC-BVA-11 | `test_TC_EP_16_commercial_repeat_signal_jump`, `test_TC_BVA_10_repeat_on_day_180`, `test_TC_BVA_11_no_repeat_on_day_181`, `test_extra_dismissed_prior_does_not_repeat`, `test_extra_draft_does_not_count_as_repeat`, `test_extra_paid_prior_still_counts_as_repeat`, `test_extra_disputed_prior_counts_as_repeat` | Pass |
| REQ-FINE-04 | 50% surcharge after repeat; half-up rounding | TC-EP-15, TC-EP-16, TC-BVA-09, TC-BVA-24 | `test_TC_EP_15_commercial_first_signal_jump`, `test_TC_EP_16_commercial_repeat_signal_jump`, `test_TC_BVA_09_heavy_overspeed_10_with_surcharge`, `test_TC_BVA_24_late_penalty_rounds_half_up`, `test_extra_percent_half_up_ties_round_away_from_zero` | Pass |
| REQ-FINE-05 | Suspension recommended for overspeed ≥ 41, drunk driving, or two priors | TC-EP-14, TC-EP-20, TC-BVA-06, TC-DT-09 | `test_TC_EP_14_drunk_driving_recommends_suspension`, `test_TC_EP_20_third_challan_recommends_suspension_without_repeat`, `test_TC_BVA_06_overspeed_41_two_wheeler`, `test_TC_DT_09_suspension_recommendation_blocks_early_discount` | Pass |
| REQ-PAY-01 | 10% discount inside 7 days, except drunk driving and suspension | TC-EP-07, TC-BVA-14, TC-DT-07, TC-DT-08, TC-DT-09 | `test_TC_BVA_14_early_payment_on_day_7`, `test_TC_DT_07_early_discount_when_all_conditions_hold`, `test_TC_DT_08_drunk_driving_has_no_early_discount`, `test_TC_DT_09_suspension_recommendation_blocks_early_discount` | Pass |
| REQ-PAY-02 | Full fine after day 7 and on or before the due date | TC-BVA-15, TC-BVA-16, TC-DT-10, TC-ST-02 | `test_TC_BVA_15_payment_on_day_8_has_no_discount`, `test_TC_BVA_16_payment_on_due_date`, `test_TC_DT_10_full_fine_inside_due_date_after_early_window`, `test_TC_ST_02_issued_to_paid` | Pass |
| REQ-PAY-03 | Late penalties 25%, 50%, 100%, capped at 2× | TC-BVA-17 to TC-BVA-21, TC-BVA-24, TC-DT-11, TC-DT-12, TC-DT-13, TC-ST-05 | `test_TC_BVA_17_one_day_late`, `test_TC_BVA_18_thirty_days_late`, `test_TC_BVA_19_thirty_one_days_late`, `test_TC_BVA_20_sixty_days_late`, `test_TC_BVA_21_sixty_one_days_late_capped_at_double`, `test_TC_BVA_24_late_penalty_rounds_half_up`, `test_TC_DT_11_twenty_five_percent_late_penalty`, `test_TC_DT_12_fifty_percent_late_penalty`, `test_TC_DT_13_hundred_percent_late_penalty_hits_cap`, `test_TC_ST_05_overdue_to_paid` | Pass |
| REQ-PAY-04 | Amount tendered must match exactly | TC-DT-15, TC-ST-05 | `test_TC_DT_15_partial_amount_rejected`, `test_TC_ST_05_overdue_to_paid` | Pass |
| REQ-PAY-05 | Paid, Dismissed, Draft, and Disputed cannot be paid | TC-DT-14, TC-ST-09, TC-ST-10, TC-ST-11, TC-ST-16 | `test_TC_DT_14_disputed_challan_cannot_be_paid`, `test_TC_ST_09_paid_is_terminal`, `test_TC_ST_10_dismissed_is_terminal`, `test_TC_ST_11_draft_to_paid_rejected`, `test_TC_ST_16_disputed_to_paid_rejected` | Pass |
| REQ-PAY-06 | Upheld challans have no early discount | TC-DT-16, TC-ST-08 | `test_TC_DT_16_upheld_challan_has_no_early_discount`, `test_TC_ST_08_upheld_to_paid` | Pass |
| REQ-DIS-01 | Dispute window is offence date through day 15 | TC-BVA-12, TC-BVA-13, TC-ST-03 | `test_TC_BVA_12_dispute_on_day_15`, `test_TC_BVA_13_dispute_on_day_16_rejected`, `test_TC_ST_03_issued_to_disputed_on_offence_date`, `test_extra_dispute_before_offence_date_rejected` | Pass |
| REQ-DIS-02 | Review ends in Dismissed or Upheld | TC-ST-06, TC-ST-07 | `test_TC_ST_06_disputed_to_dismissed`, `test_TC_ST_07_disputed_to_upheld` | Pass |
| REQ-ST-01 | Only the allowed transitions succeed | TC-ST-01 to TC-ST-17 | `test_TC_ST_01_draft_to_issued` through `test_TC_ST_17_overdue_on_due_date_rejected` | Pass |
| REQ-REP-01 | Pending, overdue, repeat offenders, clearance block | TC-EP-17, TC-EP-18, TC-EP-19, TC-BVA-22, TC-BVA-23 | `test_TC_EP_17_pending_report_omits_paid`, `test_TC_EP_18_overdue_report_lists_only_overdue_status`, `test_TC_EP_19_repeat_offender_report`, `test_TC_BVA_22_unpaid_5000_does_not_block`, `test_TC_BVA_23_unpaid_5001_blocks_registration` | Pass |

## Coverage check

| Check | Result |
| --- | --- |
| Requirements in the baseline | 26 |
| Requirements with at least one manual case | 26 |
| Requirements with at least one automated method | 26 |
| Manual cases in the index | 77 |
| Manual cases with a final result of Pass | 77 |
| Automated methods | 92 |
| Automated methods with result Pass | 92 |
| Open defects | 0 |
