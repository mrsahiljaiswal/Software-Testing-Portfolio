"""Automated unit tests for the traffic violation and fine rules.

Run from the workspace root:

    python -m unittest 05_Test_Automation\\traffic_system\\test_traffic.py -v
"""

from __future__ import annotations

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fine import percent_half_up
from models import (
    LicenceClass,
    LicenceStatus,
    TrafficError,
    VehicleCategory,
    ViolationType,
    Zone,
)
from system import TrafficSystem


OFFENCE = date(2026, 6, 1)


class TrafficCase(unittest.TestCase):
    def setUp(self) -> None:
        self.system = TrafficSystem()
        self.system.register_owner("OWN1", "Owner A")

    def add_vehicle(self, reg: str, category: VehicleCategory, owner: str = "OWN1",
                    as_of: date = date(2026, 1, 1), licence: bool = True,
                    expiry: date = date(2028, 1, 1),
                    lic_status: LicenceStatus = LicenceStatus.ACTIVE,
                    lic_class: LicenceClass | None = None) -> str:
        self.system.register_vehicle(reg, owner, category, as_of)
        if licence:
            self.system.register_licence(
                owner,
                lic_class or _class_for(category),
                expiry,
                lic_status,
            )
        return reg

    def issue(self, reg: str, violation: ViolationType, offence: date = OFFENCE,
              zone: Zone | None = None, speed: int | None = None):
        return self.system.issue_challan(reg, violation, offence, zone, speed)


class TestRegistrationAndLicence(TrafficCase):
    def test_TC_EP_01_registration_stored_uppercase(self):
        vehicle = self.system.register_vehicle(
            "  mh02cd4567  ", "OWN1", VehicleCategory.PRIVATE_CAR, date(2026, 1, 1),
        )
        self.assertEqual(vehicle.registration_number, "MH02CD4567")
        self.assertEqual(vehicle.owner_id, "OWN1")
        self.assertEqual(vehicle.category, VehicleCategory.PRIVATE_CAR)

    def test_TC_EP_02_empty_registration_rejected(self):
        with self.assertRaises(TrafficError):
            self.system.register_vehicle("   ", "OWN1", VehicleCategory.PRIVATE_CAR, date(2026, 1, 1))
        self.assertEqual(self.system.vehicles, {})

    def test_TC_EP_03_duplicate_registration_rejected(self):
        self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR, licence=False)
        with self.assertRaises(TrafficError):
            self.system.register_vehicle(
                "mh01ab1001", "OWN1", VehicleCategory.TWO_WHEELER, date(2026, 1, 2),
            )
        self.assertEqual(len(self.system.vehicles), 1)

    def test_TC_EP_04_unknown_owner_rejected(self):
        with self.assertRaises(TrafficError):
            self.system.register_vehicle(
                "MH01AB1001", "NOBODY", VehicleCategory.PRIVATE_CAR, date(2026, 1, 1),
            )
        self.assertEqual(self.system.vehicles, {})

    def test_TC_EP_05_licence_valid_on_expiry_date(self):
        reg = self.add_vehicle(
            "MH01AB1001", VehicleCategory.PRIVATE_CAR, expiry=OFFENCE,
        )
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertFalse(challan.licence_invalid)
        self.assertEqual(challan.calculated_fine, 1000)
        self.assertEqual(challan.status.value, "Issued")

    def test_TC_EP_06_expired_licence_flags_without_extra_fine(self):
        reg = self.add_vehicle(
            "MH01AB1001", VehicleCategory.PRIVATE_CAR,
            expiry=OFFENCE - timedelta(days=1),
        )
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertTrue(challan.licence_invalid)
        self.assertEqual(challan.calculated_fine, 1000)
        self.assertEqual(challan.status.value, "Issued")

    def test_TC_EP_07_suspended_licence_stays_suspended_after_payment(self):
        reg = self.add_vehicle(
            "MH01AB1001", VehicleCategory.PRIVATE_CAR,
            lic_status=LicenceStatus.SUSPENDED,
        )
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertTrue(challan.licence_invalid)
        self.assertEqual(challan.calculated_fine, 1000)
        self.assertFalse(challan.suspension_recommended)
        paid = self.system.pay(challan.challan_id, OFFENCE + timedelta(days=3), 900)
        self.assertEqual(paid.status.value, "Paid")
        self.assertEqual(paid.amount_paid, 900)
        self.assertEqual(self.system.licences["OWN1"].status, LicenceStatus.SUSPENDED)

    def test_TC_EP_08_wrong_licence_class_flags_challan(self):
        reg = self.add_vehicle(
            "MH01AB1001", VehicleCategory.PRIVATE_CAR, lic_class=LicenceClass.HGV,
        )
        challan = self.issue(reg, ViolationType.MOBILE_USE)
        self.assertTrue(challan.licence_invalid)
        self.assertEqual(challan.calculated_fine, 1500)
        self.assertEqual(challan.status.value, "Issued")

    def test_extra_missing_licence_is_invalid_flag(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR, licence=False)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertTrue(challan.licence_invalid)
        self.assertEqual(challan.calculated_fine, 1000)

    def test_extra_status_expired_is_invalid_even_with_future_expiry(self):
        reg = self.add_vehicle(
            "MH01AB1001", VehicleCategory.PRIVATE_CAR,
            expiry=date(2028, 1, 1), lic_status=LicenceStatus.EXPIRED,
        )
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertTrue(challan.licence_invalid)

    def test_extra_duplicate_owner_rejected(self):
        with self.assertRaises(TrafficError):
            self.system.register_owner("OWN1", "Owner A again")


class TestFineAndCategory(TrafficCase):
    def test_TC_EP_09_private_first_signal_jump(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertEqual(challan.calculated_fine, 1000)
        self.assertEqual(challan.base_fine, 1000)
        self.assertFalse(challan.repeat_applied)
        self.assertFalse(challan.suspension_recommended)
        self.assertEqual(challan.due_date, OFFENCE + timedelta(days=30))

    def test_TC_EP_10_helmet_on_two_wheeler(self):
        reg = self.add_vehicle("MH01TW1001", VehicleCategory.TWO_WHEELER)
        challan = self.issue(reg, ViolationType.NO_HELMET)
        self.assertEqual(challan.calculated_fine, 500)
        self.assertEqual(challan.status.value, "Issued")

    def test_TC_EP_11_helmet_on_private_car_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.NO_HELMET)
        self.assertEqual(self.system.challans, {})

    def test_TC_EP_12_seatbelt_on_two_wheeler_rejected(self):
        reg = self.add_vehicle("MH01TW1001", VehicleCategory.TWO_WHEELER)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.NO_SEATBELT)
        self.assertEqual(self.system.challans, {})

    def test_TC_EP_13_speed_below_limit_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.CITY, speed=40)
        self.assertEqual(self.system.challans, {})

    def test_TC_EP_14_drunk_driving_recommends_suspension(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.DRUNK_DRIVING)
        self.assertEqual(challan.calculated_fine, 10000)
        self.assertTrue(challan.suspension_recommended)
        self.assertFalse(challan.licence_invalid)
        self.assertEqual(self.system.licences["OWN1"].status, LicenceStatus.ACTIVE)

    def test_TC_EP_15_commercial_first_signal_jump(self):
        reg = self.add_vehicle("MH01CO1001", VehicleCategory.COMMERCIAL)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertEqual(challan.base_fine, 1000)
        self.assertFalse(challan.repeat_applied)
        self.assertEqual(challan.calculated_fine, 1500)

    def test_TC_EP_16_commercial_repeat_signal_jump(self):
        reg = self.add_vehicle("MH01CO1001", VehicleCategory.COMMERCIAL)
        first = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        second = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE + timedelta(days=30))
        self.assertEqual(first.calculated_fine, 1500)
        self.assertTrue(second.repeat_applied)
        self.assertEqual(second.calculated_fine, 3000)
        self.assertFalse(second.suspension_recommended)

    def test_TC_EP_20_third_challan_recommends_suspension_without_repeat(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        first = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        second = self.issue(reg, ViolationType.MOBILE_USE, OFFENCE + timedelta(days=10))
        third = self.issue(reg, ViolationType.WRONG_PARKING, OFFENCE + timedelta(days=20))
        self.assertEqual(first.calculated_fine, 1000)
        self.assertFalse(first.suspension_recommended)
        self.assertEqual(second.calculated_fine, 1500)
        self.assertFalse(second.suspension_recommended)
        self.assertEqual(third.calculated_fine, 500)
        self.assertFalse(third.repeat_applied)
        self.assertTrue(third.suspension_recommended)

    def test_extra_seatbelt_on_heavy_is_allowed(self):
        reg = self.add_vehicle("MH01HV1001", VehicleCategory.HEAVY)
        challan = self.issue(reg, ViolationType.NO_SEATBELT)
        self.assertEqual(challan.calculated_fine, 1500)

    def test_extra_blocked_owner_can_still_receive_a_challan(self):
        self._build_unpaid_5001()
        self.system.refresh_clearance("OWN1", date(2026, 6, 1))
        self.assertTrue(self.system.owners["OWN1"].clearance_blocked)
        extra = self.issue("MH12PR1001", ViolationType.WRONG_PARKING, date(2026, 6, 2))
        self.assertEqual(extra.status.value, "Issued")

    def _build_unpaid_5001(self):
        """Three same-day challans whose 1-day-late payables sum to 5001."""
        self.add_vehicle("MH12PR1001", VehicleCategory.PRIVATE_CAR)
        self.add_vehicle("MH12CO1001", VehicleCategory.COMMERCIAL)
        self.add_vehicle("MH12HV1001", VehicleCategory.HEAVY)
        offence = date(2026, 5, 1)
        self.issue("MH12CO1001", ViolationType.MOBILE_USE, offence)
        self.issue("MH12PR1001", ViolationType.SIGNAL_JUMP, offence)
        self.issue("MH12HV1001", ViolationType.OVERSPEEDING, offence, Zone.CITY, 60)
        return offence


class TestReports(TrafficCase):
    def test_TC_EP_17_pending_report_omits_paid(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        issued = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        paid = self.issue(reg, ViolationType.WRONG_PARKING, OFFENCE + timedelta(days=1))
        # Offence date is inside the 7-day window, so 500 becomes 450.
        self.system.pay(paid.challan_id, OFFENCE + timedelta(days=1), 450)
        pending = self.system.report_pending(OFFENCE + timedelta(days=1))
        ids = {c.challan_id for c in pending}
        self.assertEqual(ids, {issued.challan_id})

    def test_TC_EP_18_overdue_report_lists_only_overdue_status(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        old = self.issue(reg, ViolationType.SIGNAL_JUMP, date(2026, 4, 1))
        current = self.issue(reg, ViolationType.MOBILE_USE, OFFENCE)
        self.system.mark_all_overdue(date(2026, 5, 2))
        overdue = self.system.report_overdue(date(2026, 5, 2))
        self.assertEqual([c.challan_id for c in overdue], [old.challan_id])
        self.assertEqual(current.status.value, "Issued")
        self.assertEqual(old.status.value, "Overdue")

    def test_TC_EP_19_repeat_offender_report(self):
        self.system.register_owner("OWN2", "Owner B")
        self.system.register_owner("OWN3", "Owner C")
        car_a = self.add_vehicle("MH01AA1001", VehicleCategory.PRIVATE_CAR)
        car_b = self.add_vehicle("MH01BB1001", VehicleCategory.PRIVATE_CAR, owner="OWN2")
        car_c = self.add_vehicle("MH01CC1001", VehicleCategory.PRIVATE_CAR, owner="OWN3")
        self.issue(car_a, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.issue(car_a, ViolationType.SIGNAL_JUMP, OFFENCE + timedelta(days=10))
        first_b = self.issue(car_b, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.system.dispute(first_b.challan_id, OFFENCE)
        self.system.review_dispute(first_b.challan_id, "Dismissed")
        self.issue(car_b, ViolationType.SIGNAL_JUMP, OFFENCE + timedelta(days=10))
        self.issue(car_c, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.issue(car_c, ViolationType.MOBILE_USE, OFFENCE + timedelta(days=10))
        report = self.system.report_repeat_offenders(OFFENCE + timedelta(days=10))
        self.assertEqual(report, ["OWN1"])


class TestSpeedAndRepeatBoundaries(TrafficCase):
    def _speed(self, category, zone, speed, reg="MH01AB1001"):
        self.add_vehicle(reg, category)
        return self.issue(reg, ViolationType.OVERSPEEDING, zone=zone, speed=speed)

    def test_TC_BVA_01_overspeed_10(self):
        challan = self._speed(VehicleCategory.PRIVATE_CAR, Zone.CITY, 60)
        self.assertEqual(challan.calculated_fine, 500)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_02_overspeed_11(self):
        challan = self._speed(VehicleCategory.PRIVATE_CAR, Zone.CITY, 61)
        self.assertEqual(challan.calculated_fine, 1500)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_03_overspeed_20(self):
        challan = self._speed(VehicleCategory.PRIVATE_CAR, Zone.HIGHWAY, 100)
        self.assertEqual(challan.calculated_fine, 1500)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_04_overspeed_21(self):
        challan = self._speed(VehicleCategory.PRIVATE_CAR, Zone.HIGHWAY, 101)
        self.assertEqual(challan.calculated_fine, 3000)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_05_overspeed_40(self):
        challan = self._speed(VehicleCategory.PRIVATE_CAR, Zone.EXPRESSWAY, 140)
        self.assertEqual(challan.calculated_fine, 3000)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_06_overspeed_41_two_wheeler(self):
        challan = self._speed(VehicleCategory.TWO_WHEELER, Zone.EXPRESSWAY, 141, "MH01TW1001")
        self.assertEqual(challan.calculated_fine, 5000)
        self.assertTrue(challan.suspension_recommended)

    def test_TC_BVA_07_school_speed_equal_to_limit_rejected(self):
        self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        with self.assertRaises(TrafficError):
            self.issue("MH01AB1001", ViolationType.OVERSPEEDING, zone=Zone.SCHOOL, speed=25)
        self.assertEqual(self.system.challans, {})

    def test_TC_BVA_08_school_speed_one_over_limit(self):
        challan = self._speed(VehicleCategory.PRIVATE_CAR, Zone.SCHOOL, 26)
        self.assertEqual(challan.calculated_fine, 500)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_09_heavy_overspeed_10_with_surcharge(self):
        challan = self._speed(VehicleCategory.HEAVY, Zone.CITY, 60, "MH01HV1001")
        self.assertEqual(challan.base_fine, 500)
        self.assertEqual(challan.calculated_fine, 750)
        self.assertFalse(challan.suspension_recommended)

    def test_TC_BVA_10_repeat_on_day_180(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        prior = OFFENCE - timedelta(days=180)
        self.issue(reg, ViolationType.SIGNAL_JUMP, prior)
        second = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertTrue(second.repeat_applied)
        self.assertEqual(second.calculated_fine, 2000)

    def test_TC_BVA_11_no_repeat_on_day_181(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        prior = OFFENCE - timedelta(days=181)
        self.issue(reg, ViolationType.SIGNAL_JUMP, prior)
        second = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertFalse(second.repeat_applied)
        self.assertEqual(second.calculated_fine, 1000)

    def test_extra_dismissed_prior_does_not_repeat(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        first = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE - timedelta(days=10))
        self.system.dispute(first.challan_id, OFFENCE - timedelta(days=10))
        self.system.review_dispute(first.challan_id, "Dismissed")
        second = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertFalse(second.repeat_applied)
        self.assertEqual(second.calculated_fine, 1000)

    def test_extra_draft_does_not_count_as_repeat(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        self.system.create_draft(reg, ViolationType.SIGNAL_JUMP, OFFENCE - timedelta(days=5))
        issued = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertFalse(issued.repeat_applied)
        self.assertEqual(issued.calculated_fine, 1000)

    def test_extra_paid_prior_still_counts_as_repeat(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        first = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE - timedelta(days=10))
        self.system.pay(first.challan_id, OFFENCE - timedelta(days=9), 900)
        second = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertTrue(second.repeat_applied)
        self.assertEqual(second.calculated_fine, 2000)

    def test_extra_disputed_prior_counts_as_repeat(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        first = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE - timedelta(days=4))
        self.system.dispute(first.challan_id, OFFENCE - timedelta(days=4))
        second = self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertTrue(second.repeat_applied)
        self.assertEqual(second.calculated_fine, 2000)

    def test_extra_duplicate_overspeed_ignores_zone(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.CITY, speed=70)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.HIGHWAY, speed=120)
        self.assertEqual(len(self.system.challans), 1)

    def test_extra_negative_speed_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.CITY, speed=-1)


class TestDisputeAndPaymentBoundaries(TrafficCase):
    def _signal(self, offence: date = OFFENCE):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        return self.issue(reg, ViolationType.SIGNAL_JUMP, offence)

    def test_TC_BVA_12_dispute_on_day_15(self):
        challan = self._signal()
        updated = self.system.dispute(challan.challan_id, OFFENCE + timedelta(days=15))
        self.assertEqual(updated.status.value, "Disputed")

    def test_TC_BVA_13_dispute_on_day_16_rejected(self):
        challan = self._signal()
        with self.assertRaises(TrafficError):
            self.system.dispute(challan.challan_id, OFFENCE + timedelta(days=16))
        self.assertEqual(self.system.challans[challan.challan_id].status.value, "Issued")

    def test_TC_BVA_14_early_payment_on_day_7(self):
        challan = self._signal()
        pay_on = OFFENCE + timedelta(days=7)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 900)
        paid = self.system.pay(challan.challan_id, pay_on, 900)
        self.assertEqual(paid.status.value, "Paid")
        self.assertEqual(paid.amount_paid, 900)

    def test_TC_BVA_15_payment_on_day_8_has_no_discount(self):
        challan = self._signal()
        pay_on = OFFENCE + timedelta(days=8)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1000)
        paid = self.system.pay(challan.challan_id, pay_on, 1000)
        self.assertEqual(paid.amount_paid, 1000)

    def test_TC_BVA_16_payment_on_due_date(self):
        challan = self._signal()
        pay_on = OFFENCE + timedelta(days=30)
        self.assertEqual(pay_on, challan.due_date)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1000)
        self.system.pay(challan.challan_id, pay_on, 1000)

    def test_TC_BVA_17_one_day_late(self):
        challan = self._signal()
        pay_on = challan.due_date + timedelta(days=1)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1250)
        paid = self.system.pay(challan.challan_id, pay_on, 1250)
        self.assertEqual(paid.status.value, "Paid")

    def test_TC_BVA_18_thirty_days_late(self):
        challan = self._signal()
        pay_on = challan.due_date + timedelta(days=30)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1250)

    def test_TC_BVA_19_thirty_one_days_late(self):
        challan = self._signal()
        pay_on = challan.due_date + timedelta(days=31)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1500)

    def test_TC_BVA_20_sixty_days_late(self):
        challan = self._signal()
        pay_on = challan.due_date + timedelta(days=60)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1500)

    def test_TC_BVA_21_sixty_one_days_late_capped_at_double(self):
        challan = self._signal()
        pay_on = challan.due_date + timedelta(days=61)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 2000)
        paid = self.system.pay(challan.challan_id, pay_on, 2000)
        self.assertEqual(paid.amount_paid, 2000)
        self.assertLessEqual(paid.amount_paid, challan.calculated_fine * 2)

    def test_TC_BVA_22_unpaid_5000_does_not_block(self):
        reg = self.add_vehicle("MH01AA0001", VehicleCategory.PRIVATE_CAR)
        offence = date(2026, 4, 1)
        insurance = self.issue(reg, ViolationType.NO_INSURANCE, offence)
        speeding = self.issue(
            reg, ViolationType.OVERSPEEDING, offence, Zone.EXPRESSWAY, 140,
        )
        self.assertEqual(insurance.calculated_fine, 2000)
        self.assertEqual(speeding.calculated_fine, 3000)
        self.assertFalse(insurance.suspension_recommended)
        self.assertFalse(speeding.suspension_recommended)
        self.assertEqual(self.system.unpaid_total("OWN1", offence), 5000)
        second = self.system.register_vehicle(
            "MH01AA0002", "OWN1", VehicleCategory.PRIVATE_CAR, offence,
        )
        self.assertEqual(second.registration_number, "MH01AA0002")
        self.assertFalse(self.system.owners["OWN1"].clearance_blocked)
        self.assertEqual(self.system.owners["OWN1"].unpaid_total, 5000)
        self.assertEqual(self.system.report_clearance_blocked(offence), [])

    def test_TC_BVA_23_unpaid_5001_blocks_registration(self):
        self.add_vehicle("MH12PR1001", VehicleCategory.PRIVATE_CAR)
        self.add_vehicle("MH12CO1001", VehicleCategory.COMMERCIAL)
        self.add_vehicle("MH12HV1001", VehicleCategory.HEAVY)
        offence = date(2026, 5, 1)
        mobile = self.issue("MH12CO1001", ViolationType.MOBILE_USE, offence)
        signal = self.issue("MH12PR1001", ViolationType.SIGNAL_JUMP, offence)
        heavy = self.issue(
            "MH12HV1001", ViolationType.OVERSPEEDING, offence, Zone.CITY, 60,
        )
        self.assertEqual(mobile.calculated_fine, 2250)
        self.assertEqual(signal.calculated_fine, 1000)
        self.assertEqual(heavy.calculated_fine, 750)
        as_of = date(2026, 6, 1)
        self.assertEqual(self.system.payable_amount(mobile.challan_id, as_of), 2813)
        self.assertEqual(self.system.payable_amount(signal.challan_id, as_of), 1250)
        self.assertEqual(self.system.payable_amount(heavy.challan_id, as_of), 938)
        self.system.mark_all_overdue(as_of)
        self.assertEqual(self.system.unpaid_total("OWN1", as_of), 5001)
        with self.assertRaises(TrafficError):
            self.system.register_vehicle(
                "MH12PR1002", "OWN1", VehicleCategory.PRIVATE_CAR, as_of,
            )
        self.assertTrue(self.system.owners["OWN1"].clearance_blocked)
        self.assertEqual(self.system.report_clearance_blocked(as_of), ["OWN1"])
        self.assertNotIn("MH12PR1002", self.system.vehicles)

    def test_TC_BVA_24_late_penalty_rounds_half_up(self):
        reg = self.add_vehicle("MH01HV1001", VehicleCategory.HEAVY)
        challan = self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.CITY, speed=60)
        self.assertEqual(challan.calculated_fine, 750)
        self.assertEqual(percent_half_up(750, 25), 188)
        pay_on = challan.due_date + timedelta(days=1)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 938)

    def test_extra_clearance_unblocks_when_total_falls_to_5000_or_below(self):
        self.add_vehicle("MH12PR1001", VehicleCategory.PRIVATE_CAR)
        self.add_vehicle("MH12CO1001", VehicleCategory.COMMERCIAL)
        self.add_vehicle("MH12HV1001", VehicleCategory.HEAVY)
        offence = date(2026, 5, 1)
        mobile = self.issue("MH12CO1001", ViolationType.MOBILE_USE, offence)
        signal = self.issue("MH12PR1001", ViolationType.SIGNAL_JUMP, offence)
        self.issue("MH12HV1001", ViolationType.OVERSPEEDING, offence, Zone.CITY, 60)
        as_of = date(2026, 6, 1)
        self.system.mark_all_overdue(as_of)
        self.assertEqual(self.system.unpaid_total("OWN1", as_of), 5001)
        self.system.pay(signal.challan_id, as_of, 1250)
        self.assertEqual(self.system.unpaid_total("OWN1", as_of), 3751)
        vehicle = self.system.register_vehicle(
            "MH12PR1002", "OWN1", VehicleCategory.TWO_WHEELER, as_of,
        )
        self.assertEqual(vehicle.registration_number, "MH12PR1002")
        self.assertFalse(self.system.owners["OWN1"].clearance_blocked)
        self.assertEqual(mobile.status.value, "Overdue")

    def test_extra_percent_half_up_ties_round_away_from_zero(self):
        self.assertEqual(percent_half_up(750, 25), 188)
        self.assertEqual(percent_half_up(2250, 25), 563)
        self.assertEqual(percent_half_up(1000, 10), 100)
        self.assertEqual(percent_half_up(1, 50), 1)
        self.assertEqual(percent_half_up(1, 49), 0)


class TestDecisionTables(TrafficCase):
    def test_TC_DT_01_valid_challan_with_valid_licence(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertEqual(challan.status.value, "Issued")
        self.assertEqual(challan.calculated_fine, 1000)
        self.assertFalse(challan.licence_invalid)

    def test_TC_DT_02_category_mismatch_rejects_helmet_on_commercial(self):
        reg = self.add_vehicle("MH01CO1001", VehicleCategory.COMMERCIAL)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.NO_HELMET)
        self.assertEqual(self.system.challans, {})

    def test_TC_DT_03_speed_equal_to_city_limit_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.CITY, speed=50)
        self.assertEqual(self.system.challans, {})

    def test_TC_DT_04_duplicate_same_vehicle_type_and_date(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        self.issue(reg, ViolationType.SIGNAL_JUMP)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.assertEqual(len(self.system.challans), 1)

    def test_TC_DT_05_unregistered_vehicle_rejected(self):
        with self.assertRaises(TrafficError):
            self.issue("MH99ZZ9999", ViolationType.SIGNAL_JUMP)
        self.assertEqual(self.system.challans, {})

    def test_TC_DT_06_invalid_licence_still_records_mobile_use(self):
        reg = self.add_vehicle(
            "MH01AB1001", VehicleCategory.PRIVATE_CAR,
            expiry=OFFENCE - timedelta(days=1),
        )
        challan = self.issue(reg, ViolationType.MOBILE_USE)
        self.assertEqual(challan.status.value, "Issued")
        self.assertEqual(challan.calculated_fine, 1500)
        self.assertTrue(challan.licence_invalid)

    def test_TC_DT_07_early_discount_when_all_conditions_hold(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        pay_on = OFFENCE + timedelta(days=3)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 900)
        paid = self.system.pay(challan.challan_id, pay_on, 900)
        self.assertEqual(paid.status.value, "Paid")

    def test_TC_DT_08_drunk_driving_has_no_early_discount(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.DRUNK_DRIVING)
        pay_on = OFFENCE + timedelta(days=1)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 10000)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, pay_on, 9000)
        self.assertEqual(challan.status.value, "Issued")
        paid = self.system.pay(challan.challan_id, pay_on, 10000)
        self.assertEqual(paid.amount_paid, 10000)
        self.assertEqual(self.system.licences["OWN1"].status, LicenceStatus.ACTIVE)

    def test_TC_DT_09_suspension_recommendation_blocks_early_discount(self):
        reg = self.add_vehicle("MH01TW1001", VehicleCategory.TWO_WHEELER)
        challan = self.issue(reg, ViolationType.OVERSPEEDING, zone=Zone.EXPRESSWAY, speed=141)
        pay_on = OFFENCE + timedelta(days=2)
        self.assertTrue(challan.suspension_recommended)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 5000)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, pay_on, 4500)
        self.assertEqual(challan.status.value, "Issued")

    def test_TC_DT_10_full_fine_inside_due_date_after_early_window(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        pay_on = OFFENCE + timedelta(days=20)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1000)
        self.system.pay(challan.challan_id, pay_on, 1000)
        self.assertEqual(challan.status.value, "Paid")

    def test_TC_DT_11_twenty_five_percent_late_penalty(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        pay_on = challan.due_date + timedelta(days=10)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1250)
        self.system.pay(challan.challan_id, pay_on, 1250)

    def test_TC_DT_12_fifty_percent_late_penalty(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        pay_on = challan.due_date + timedelta(days=45)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1500)
        self.system.pay(challan.challan_id, pay_on, 1500)

    def test_TC_DT_13_hundred_percent_late_penalty_hits_cap(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        pay_on = challan.due_date + timedelta(days=90)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 2000)
        self.system.pay(challan.challan_id, pay_on, 2000)

    def test_TC_DT_14_disputed_challan_cannot_be_paid(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, OFFENCE + timedelta(days=1), 900)
        self.assertEqual(challan.status.value, "Disputed")

    def test_TC_DT_15_partial_amount_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, OFFENCE + timedelta(days=3), 899)
        self.assertEqual(challan.status.value, "Issued")
        self.assertIsNone(challan.amount_paid)

    def test_TC_DT_16_upheld_challan_has_no_early_discount(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE + timedelta(days=1))
        self.system.review_dispute(challan.challan_id, "Upheld")
        pay_on = OFFENCE + timedelta(days=4)
        self.assertEqual(self.system.payable_amount(challan.challan_id, pay_on), 1000)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, pay_on, 900)
        paid = self.system.pay(challan.challan_id, pay_on, 1000)
        self.assertEqual(paid.status.value, "Paid")


class TestStateTransitions(TrafficCase):
    def _draft(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        return self.system.create_draft(reg, ViolationType.SIGNAL_JUMP, OFFENCE)

    def test_TC_ST_01_draft_to_issued(self):
        draft = self._draft()
        self.assertEqual(draft.status.value, "Draft")
        issued = self.system.submit(draft.challan_id)
        self.assertEqual(issued.status.value, "Issued")
        self.assertEqual(issued.calculated_fine, 1000)
        self.assertEqual(issued.due_date, OFFENCE + timedelta(days=30))

    def test_TC_ST_02_issued_to_paid(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        paid = self.system.pay(challan.challan_id, OFFENCE + timedelta(days=8), 1000)
        self.assertEqual(paid.status.value, "Paid")

    def test_TC_ST_03_issued_to_disputed_on_offence_date(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        disputed = self.system.dispute(challan.challan_id, OFFENCE)
        self.assertEqual(disputed.status.value, "Disputed")
        self.assertEqual(disputed.calculated_fine, 1000)

    def test_TC_ST_04_issued_to_overdue_after_due_date(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        marked = self.system.mark_overdue(challan.challan_id, challan.due_date + timedelta(days=1))
        self.assertEqual(marked.status.value, "Overdue")

    def test_TC_ST_05_overdue_to_paid(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        late = challan.due_date + timedelta(days=1)
        self.system.mark_overdue(challan.challan_id, late)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, late, 1000)
        self.assertEqual(challan.status.value, "Overdue")
        paid = self.system.pay(challan.challan_id, late, 1250)
        self.assertEqual(paid.status.value, "Paid")
        self.assertEqual(paid.amount_paid, 1250)

    def test_TC_ST_06_disputed_to_dismissed(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE)
        closed = self.system.review_dispute(challan.challan_id, "Dismissed")
        self.assertEqual(closed.status.value, "Dismissed")
        self.assertEqual(self.system.unpaid_total("OWN1", OFFENCE), 0)

    def test_TC_ST_07_disputed_to_upheld(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE + timedelta(days=2))
        closed = self.system.review_dispute(challan.challan_id, "Upheld")
        self.assertEqual(closed.status.value, "Upheld")
        self.assertEqual(self.system.unpaid_total("OWN1", OFFENCE), 1000)

    def test_TC_ST_08_upheld_to_paid(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE)
        self.system.review_dispute(challan.challan_id, "Upheld")
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, OFFENCE + timedelta(days=4), 900)
        paid = self.system.pay(challan.challan_id, OFFENCE + timedelta(days=4), 1000)
        self.assertEqual(paid.status.value, "Paid")

    def test_TC_ST_09_paid_is_terminal(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.pay(challan.challan_id, OFFENCE + timedelta(days=8), 1000)
        with self.assertRaises(TrafficError):
            self.system.dispute(challan.challan_id, OFFENCE + timedelta(days=9))
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, OFFENCE + timedelta(days=9), 1000)
        self.assertEqual(challan.status.value, "Paid")

    def test_TC_ST_10_dismissed_is_terminal(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE)
        self.system.review_dispute(challan.challan_id, "Dismissed")
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, OFFENCE + timedelta(days=2), 1000)
        self.assertEqual(challan.status.value, "Dismissed")

    def test_TC_ST_11_draft_to_paid_rejected(self):
        draft = self._draft()
        with self.assertRaises(TrafficError):
            self.system.pay(draft.challan_id, OFFENCE, 1000)
        self.assertEqual(draft.status.value, "Draft")

    def test_TC_ST_12_draft_to_disputed_rejected(self):
        draft = self._draft()
        with self.assertRaises(TrafficError):
            self.system.dispute(draft.challan_id, OFFENCE)
        self.assertEqual(draft.status.value, "Draft")

    def test_TC_ST_13_draft_to_overdue_rejected(self):
        draft = self._draft()
        with self.assertRaises(TrafficError):
            self.system.mark_overdue(draft.challan_id, OFFENCE + timedelta(days=40))
        self.assertEqual(draft.status.value, "Draft")

    def test_TC_ST_14_issued_to_dismissed_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        with self.assertRaises(TrafficError):
            self.system.review_dispute(challan.challan_id, "Dismissed")
        self.assertEqual(challan.status.value, "Issued")

    def test_TC_ST_15_overdue_to_disputed_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.mark_overdue(challan.challan_id, challan.due_date + timedelta(days=1))
        with self.assertRaises(TrafficError):
            self.system.dispute(challan.challan_id, challan.due_date + timedelta(days=1))
        self.assertEqual(challan.status.value, "Overdue")

    def test_TC_ST_16_disputed_to_paid_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        self.system.dispute(challan.challan_id, OFFENCE + timedelta(days=1))
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, OFFENCE + timedelta(days=2), 900)
        self.assertEqual(challan.status.value, "Disputed")

    def test_TC_ST_17_overdue_on_due_date_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        with self.assertRaises(TrafficError):
            self.system.mark_overdue(challan.challan_id, challan.due_date)
        self.assertEqual(challan.status.value, "Issued")

    def test_extra_dispute_before_offence_date_rejected(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        challan = self.issue(reg, ViolationType.SIGNAL_JUMP)
        with self.assertRaises(TrafficError):
            self.system.dispute(challan.challan_id, OFFENCE - timedelta(days=1))
        self.assertEqual(challan.status.value, "Issued")

    def test_extra_draft_blocks_second_challan_same_day(self):
        reg = self.add_vehicle("MH01AB1001", VehicleCategory.PRIVATE_CAR)
        self.system.create_draft(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        with self.assertRaises(TrafficError):
            self.issue(reg, ViolationType.SIGNAL_JUMP, OFFENCE)
        self.assertEqual(len(self.system.challans), 1)


def _class_for(category: VehicleCategory) -> LicenceClass:
    return {
        VehicleCategory.TWO_WHEELER: LicenceClass.TW,
        VehicleCategory.PRIVATE_CAR: LicenceClass.LMV,
        VehicleCategory.COMMERCIAL: LicenceClass.COM,
        VehicleCategory.HEAVY: LicenceClass.HGV,
    }[category]


if __name__ == "__main__":
    unittest.main()
