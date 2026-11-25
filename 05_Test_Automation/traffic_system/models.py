"""Types for the Vehicle Traffic Violation and Fine Management System.

A traffic officer records a challan. The system calculates one fine.
The owner pays that fine.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class TrafficError(Exception):
    """Raised when a rule rejects the operation."""


class VehicleType(Enum):
    TWO_WHEELER = "Two-wheeler"
    CAR = "Car"


class Violation(Enum):
    SIGNAL_JUMP = "Signal jump"
    NO_HELMET = "No helmet"
    OVERSPEEDING = "Overspeeding"


class ChallanStatus(Enum):
    ISSUED = "Issued"
    PAID = "Paid"
    OVERDUE = "Overdue"


# The only allowed moves. Every other pair is rejected.
ALLOWED_TRANSITIONS = {
    (ChallanStatus.ISSUED, ChallanStatus.PAID),
    (ChallanStatus.ISSUED, ChallanStatus.OVERDUE),
    (ChallanStatus.OVERDUE, ChallanStatus.PAID),
}


@dataclass
class Vehicle:
    registration_number: str
    vehicle_type: VehicleType


@dataclass
class Challan:
    challan_id: str
    vehicle_reg: str
    vehicle_type: VehicleType
    violation: Violation
    challan_date: date
    status: ChallanStatus
    fine: int
    due_date: date
    speed: int | None = None
    payment_date: date | None = None
    amount_paid: int | None = None
