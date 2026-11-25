"""Automated tests for the simple challan rules.

Run from the portfolio folder:

    python -m unittest 05_Test_Automation\\traffic_system\\test_traffic.py -v
"""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from models import ChallanStatus, TrafficError, VehicleType, Violation
from system import TrafficSystem

# One challan date is used throughout, so the due date is easy to remember.
# 1 June 2026 + 15 days = 16 June 2026. The next day is 17 June 2026.
CHALLAN = date(2026, 6, 1)
DUE = date(2026, 6, 16)
DAY_AFTER = date(2026, 6, 17)


class TrafficCase(unittest.TestCase):
    def setUp(self) -> None:
        self.system = TrafficSystem()

    def register(self, number: str, vehicle_type: VehicleType) -> None:
        self.system.register_vehicle(number, vehicle_type)


class TestEquivalence(TrafficCase):
    """Eight classes: vehicle x violation, and the three speed classes."""

    def test_TC_EP_01_two_wheeler_signal_jump(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        challan = self.system.issue_challan("KA01TW0001", Violation.SIGNAL_JUMP, CHALLAN)
        self.assertEqual(challan.status, ChallanStatus.ISSUED)
        self.assertEqual(challan.fine, 500)
        self.assertEqual(challan.due_date, DUE)

    def test_TC_EP_02_car_signal_jump(self):
        self.register("KA01CA0001", VehicleType.CAR)
        challan = self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)
        self.assertEqual(challan.fine, 500)
        self.assertEqual(challan.status, ChallanStatus.ISSUED)

    def test_TC_EP_03_two_wheeler_no_helmet(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        challan = self.system.issue_challan("KA01TW0001", Violation.NO_HELMET, CHALLAN)
        self.assertEqual(challan.fine, 1000)
        self.assertEqual(challan.status, ChallanStatus.ISSUED)

    def test_TC_EP_04_DEF_02_car_no_helmet_rejected(self):
        self.register("KA01CA0001", VehicleType.CAR)
        with self.assertRaises(TrafficError):
            self.system.issue_challan("KA01CA0001", Violation.NO_HELMET, CHALLAN)
        self.assertEqual(self.system.challans, {})

    def test_TC_EP_05_speed_within_limit_rejected(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        with self.assertRaises(TrafficError):
            self.system.issue_challan(
                "KA01TW0001", Violation.OVERSPEEDING, CHALLAN, speed=40,
            )
        self.assertEqual(self.system.challans, {})

    def test_TC_EP_06_speed_slightly_over(self):
        self.register("KA01CA0001", VehicleType.CAR)
        challan = self.system.issue_challan(
            "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=70,
        )
        self.assertEqual(challan.fine, 500)
        self.assertEqual(challan.speed, 70)

    def test_TC_EP_07_speed_well_over(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        challan = self.system.issue_challan(
            "KA01TW0001", Violation.OVERSPEEDING, CHALLAN, speed=100,
        )
        self.assertEqual(challan.fine, 2000)

    def test_TC_EP_08_car_speed_within_limit_rejected(self):
        self.register("KA01CA0001", VehicleType.CAR)
        with self.assertRaises(TrafficError):
            self.system.issue_challan(
                "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=50,
            )
        self.assertEqual(self.system.challans, {})


class TestBoundary(TrafficCase):
    """Speed 60, 61, 80, 81, and the due-date / late-fee edges."""

    def _car(self) -> None:
        self.register("KA01CA0001", VehicleType.CAR)

    def test_TC_BVA_01_DEF_01_speed_60_rejected(self):
        self._car()
        with self.assertRaises(TrafficError):
            self.system.issue_challan(
                "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=60,
            )
        self.assertEqual(self.system.challans, {})

    def test_TC_BVA_02_speed_61_fine_500(self):
        self._car()
        challan = self.system.issue_challan(
            "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=61,
        )
        self.assertEqual(challan.fine, 500)

    def test_TC_BVA_03_speed_80_fine_500(self):
        self._car()
        challan = self.system.issue_challan(
            "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=80,
        )
        self.assertEqual(challan.fine, 500)

    def test_TC_BVA_04_speed_81_fine_2000(self):
        self._car()
        challan = self.system.issue_challan(
            "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=81,
        )
        self.assertEqual(challan.fine, 2000)

    def test_TC_BVA_05_pay_on_due_date(self):
        self._car()
        challan = self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)
        self.assertEqual(challan.due_date, DUE)
        paid = self.system.pay(challan.challan_id, DUE, 500)
        self.assertEqual(paid.status, ChallanStatus.PAID)
        self.assertEqual(paid.amount_paid, 500)

    def test_TC_BVA_06_DEF_03_day_after_due_adds_200(self):
        self._car()
        challan = self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)
        self.assertEqual(self.system.payable(challan.challan_id, DAY_AFTER), 700)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, DAY_AFTER, 500)
        self.assertEqual(challan.status, ChallanStatus.ISSUED)
        paid = self.system.pay(challan.challan_id, DAY_AFTER, 700)
        self.assertEqual(paid.status, ChallanStatus.PAID)
        self.assertEqual(paid.amount_paid, 700)

    def test_TC_BVA_07_late_fee_is_200_on_helmet_fine(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        challan = self.system.issue_challan("KA01TW0001", Violation.NO_HELMET, CHALLAN)
        paid = self.system.pay(challan.challan_id, DAY_AFTER, 1200)
        self.assertEqual(paid.amount_paid, 1200)
        self.assertEqual(paid.amount_paid - challan.fine, 200)

    def test_TC_BVA_08_one_rupee_short_of_late_amount_rejected(self):
        self._car()
        challan = self.system.issue_challan(
            "KA01CA0001", Violation.OVERSPEEDING, CHALLAN, speed=81,
        )
        self.assertEqual(challan.fine, 2000)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, DAY_AFTER, 2199)
        self.assertEqual(challan.status, ChallanStatus.ISSUED)
        self.assertIsNone(challan.amount_paid)


class TestDecisionTable(TrafficCase):
    """Table A accepts or rejects a challan. Table B is the amount due."""

    def test_TC_DT_01_rule_a1_signal_jump_accepted(self):
        self.register("KA01CA0001", VehicleType.CAR)
        challan = self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)
        self.assertEqual(challan.fine, 500)

    def test_TC_DT_02_rule_a2_helmet_two_wheeler_accepted(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        challan = self.system.issue_challan("KA01TW0001", Violation.NO_HELMET, CHALLAN)
        self.assertEqual(challan.fine, 1000)

    def test_TC_DT_03_rule_a3_helmet_car_rejected(self):
        self.register("KA01CA0001", VehicleType.CAR)
        with self.assertRaises(TrafficError):
            self.system.issue_challan("KA01CA0001", Violation.NO_HELMET, CHALLAN)
        self.assertEqual(self.system.challans, {})

    def test_TC_DT_04_rule_a4_speed_at_or_below_60_rejected(self):
        self.register("KA01TW0001", VehicleType.TWO_WHEELER)
        with self.assertRaises(TrafficError):
            self.system.issue_challan(
                "KA01TW0001", Violation.OVERSPEEDING, CHALLAN, speed=50,
            )
        self.assertEqual(self.system.challans, {})

    def test_TC_DT_05_rule_b1_on_time_amount_is_the_fine(self):
        self.register("KA01CA0001", VehicleType.CAR)
        challan = self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)
        paid = self.system.pay(challan.challan_id, date(2026, 6, 10), 500)
        self.assertEqual(paid.status, ChallanStatus.PAID)
        self.assertEqual(paid.amount_paid, 500)

    def test_TC_DT_06_rule_b2_late_amount_is_fine_plus_200(self):
        self.register("KA01CA0001", VehicleType.CAR)
        challan = self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)
        paid = self.system.pay(challan.challan_id, date(2026, 6, 20), 700)
        self.assertEqual(paid.status, ChallanStatus.PAID)
        self.assertEqual(paid.amount_paid, 700)


class TestState(TrafficCase):
    """Three valid moves and three rejected moves."""

    def _issued_signal(self):
        self.register("KA01CA0001", VehicleType.CAR)
        return self.system.issue_challan("KA01CA0001", Violation.SIGNAL_JUMP, CHALLAN)

    def test_TC_ST_01_issued_to_paid_on_time(self):
        challan = self._issued_signal()
        paid = self.system.pay(challan.challan_id, date(2026, 6, 10), 500)
        self.assertEqual(paid.status, ChallanStatus.PAID)

    def test_TC_ST_02_issued_to_overdue_after_due_date(self):
        challan = self._issued_signal()
        with self.assertRaises(TrafficError):
            self.system.mark_overdue(challan.challan_id, DUE)
        self.assertEqual(challan.status, ChallanStatus.ISSUED)
        overdue = self.system.mark_overdue(challan.challan_id, DAY_AFTER)
        self.assertEqual(overdue.status, ChallanStatus.OVERDUE)

    def test_TC_ST_03_overdue_to_paid_late_amount(self):
        challan = self._issued_signal()
        self.system.mark_overdue(challan.challan_id, DAY_AFTER)
        paid = self.system.pay(challan.challan_id, date(2026, 6, 20), 700)
        self.assertEqual(paid.status, ChallanStatus.PAID)
        self.assertEqual(paid.amount_paid, 700)

    def test_TC_ST_04_paid_cannot_be_paid_again(self):
        challan = self._issued_signal()
        self.system.pay(challan.challan_id, DUE, 500)
        with self.assertRaises(TrafficError):
            self.system.pay(challan.challan_id, DAY_AFTER, 700)
        self.assertEqual(challan.status, ChallanStatus.PAID)
        self.assertEqual(challan.amount_paid, 500)

    def test_TC_ST_05_overdue_cannot_return_to_issued(self):
        challan = self._issued_signal()
        self.system.mark_overdue(challan.challan_id, DAY_AFTER)
        with self.assertRaises(TrafficError):
            self.system.reopen(challan.challan_id)
        self.assertEqual(challan.status, ChallanStatus.OVERDUE)

    def test_TC_ST_06_paid_cannot_become_overdue(self):
        challan = self._issued_signal()
        self.system.pay(challan.challan_id, DUE, 500)
        with self.assertRaises(TrafficError):
            self.system.mark_overdue(challan.challan_id, DAY_AFTER)
        self.assertEqual(challan.status, ChallanStatus.PAID)


class TestRegistration(TrafficCase):
    """The only registration rule: a number is required, uppercase, and unique."""

    def test_registration_required_and_stored_uppercase(self):
        with self.assertRaises(TrafficError):
            self.system.register_vehicle("   ", VehicleType.CAR)
        self.assertEqual(self.system.vehicles, {})
        vehicle = self.system.register_vehicle("  ka02ab0099  ", VehicleType.CAR)
        self.assertEqual(vehicle.registration_number, "KA02AB0099")
        self.assertEqual(vehicle.vehicle_type, VehicleType.CAR)

    def test_duplicate_registration_rejected(self):
        self.system.register_vehicle("KA05MH2211", VehicleType.CAR)
        with self.assertRaises(TrafficError):
            self.system.register_vehicle("ka05mh2211", VehicleType.TWO_WHEELER)
        self.assertEqual(len(self.system.vehicles), 1)
        self.assertEqual(
            self.system.vehicles["KA05MH2211"].vehicle_type, VehicleType.CAR,
        )


if __name__ == "__main__":
    unittest.main()
