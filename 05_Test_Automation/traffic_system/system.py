"""Vehicle Traffic Violation and Fine Management System.

An officer registers a vehicle and records a challan. The system stores
one fine. The owner pays that fine exactly, or the fine plus 200 rupees
when the payment is after the due date.
"""

from __future__ import annotations

from datetime import date

from fine import amount_due, calculate_fine, due_date_for
from models import (
    ALLOWED_TRANSITIONS,
    Challan,
    ChallanStatus,
    TrafficError,
    Vehicle,
    VehicleType,
    Violation,
)


class TrafficSystem:
    def __init__(self) -> None:
        self.vehicles: dict[str, Vehicle] = {}
        self.challans: dict[str, Challan] = {}
        self._next_id = 1

    def register_vehicle(self, registration_number: str,
                         vehicle_type: VehicleType) -> Vehicle:
        """Store a vehicle. The number is required, uppercase, and unique."""
        reg = self._registration(registration_number)
        if not isinstance(vehicle_type, VehicleType):
            raise TrafficError("Unknown vehicle type")
        if reg in self.vehicles:
            raise TrafficError("Duplicate registration number")
        vehicle = Vehicle(registration_number=reg, vehicle_type=vehicle_type)
        self.vehicles[reg] = vehicle
        return vehicle

    def issue_challan(self, registration_number: str, violation: Violation,
                      challan_date: date, speed: int | None = None) -> Challan:
        """Validate and store an Issued challan. A rejected attempt is not stored."""
        reg = self._registration(registration_number)
        challan_date = self._as_date(challan_date, "Challan date")
        if reg not in self.vehicles:
            raise TrafficError("Vehicle is not registered")
        vehicle = self.vehicles[reg]
        fine = calculate_fine(vehicle.vehicle_type, violation, speed)
        challan = Challan(
            challan_id=self._new_id(),
            vehicle_reg=reg,
            vehicle_type=vehicle.vehicle_type,
            violation=violation,
            challan_date=challan_date,
            status=ChallanStatus.ISSUED,
            fine=fine,
            due_date=due_date_for(challan_date),
            speed=speed if violation == Violation.OVERSPEEDING else None,
        )
        self.challans[challan.challan_id] = challan
        return challan

    def mark_overdue(self, challan_id: str, as_of: date) -> Challan:
        """Issued becomes Overdue only when the date is after the due date."""
        challan = self._get(challan_id)
        as_of = self._as_date(as_of, "Current date")
        self._require_transition(challan, ChallanStatus.OVERDUE)
        if as_of <= challan.due_date:
            raise TrafficError("Challan is not overdue")
        challan.status = ChallanStatus.OVERDUE
        return challan

    def pay(self, challan_id: str, payment_date: date, amount: int) -> Challan:
        """Pay the exact amount due. A short payment does not change the status."""
        challan = self._get(challan_id)
        payment_date = self._as_date(payment_date, "Payment date")
        self._require_transition(challan, ChallanStatus.PAID)
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise TrafficError("Amount must be a whole number of rupees")
        expected = self.payable(challan_id, payment_date)
        if amount != expected:
            raise TrafficError(
                f"Amount tendered {amount} does not equal payable {expected}"
            )
        challan.status = ChallanStatus.PAID
        challan.payment_date = payment_date
        challan.amount_paid = amount
        return challan

    def payable(self, challan_id: str, payment_date: date) -> int:
        challan = self._get(challan_id)
        payment_date = self._as_date(payment_date, "Payment date")
        if challan.status == ChallanStatus.PAID:
            raise TrafficError("A paid challan cannot be paid again")
        if challan.status == ChallanStatus.OVERDUE and payment_date <= challan.due_date:
            raise TrafficError("An overdue challan is paid after the due date")
        return amount_due(challan.fine, challan.due_date, payment_date)

    def reopen(self, challan_id: str) -> Challan:
        """Rejected. A challan cannot return to Issued."""
        challan = self._get(challan_id)
        self._require_transition(challan, ChallanStatus.ISSUED)
        return challan

    def _require_transition(self, challan: Challan, target: ChallanStatus) -> None:
        if (challan.status, target) not in ALLOWED_TRANSITIONS:
            raise TrafficError(
                f"Invalid transition {challan.status.value} -> {target.value}"
            )

    def _get(self, challan_id: str) -> Challan:
        challan = self.challans.get(challan_id)
        if challan is None:
            raise TrafficError("Challan does not exist")
        return challan

    def _new_id(self) -> str:
        challan_id = f"CH-{self._next_id:03d}"
        self._next_id += 1
        return challan_id

    @staticmethod
    def _registration(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise TrafficError("Registration number is required")
        return value.strip().upper()

    @staticmethod
    def _as_date(value: date, label: str) -> date:
        if type(value) is not date:
            raise TrafficError(f"{label} must be a calendar date")
        return value
