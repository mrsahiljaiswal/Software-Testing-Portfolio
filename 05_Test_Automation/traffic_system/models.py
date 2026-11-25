"""Domain types for the Vehicle Traffic Violation and Fine Management System."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class TrafficError(Exception):
    """Raised when a traffic-system rule rejects an operation."""


class VehicleCategory(Enum):
    TWO_WHEELER = "Two-wheeler"
    PRIVATE_CAR = "Private car"
    COMMERCIAL = "Commercial"
    HEAVY = "Heavy"


class LicenceClass(Enum):
    TW = "TW"
    LMV = "LMV"
    COM = "COM"
    HGV = "HGV"


class LicenceStatus(Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    SUSPENDED = "Suspended"


class ViolationType(Enum):
    SIGNAL_JUMP = "Signal jump"
    NO_HELMET = "No helmet"
    NO_SEATBELT = "No seatbelt"
    MOBILE_USE = "Mobile use"
    WRONG_PARKING = "Wrong parking"
    NO_INSURANCE = "No insurance"
    DRUNK_DRIVING = "Drunk driving"
    OVERSPEEDING = "Overspeeding"


class Zone(Enum):
    CITY = "City"
    HIGHWAY = "Highway"
    EXPRESSWAY = "Expressway"
    SCHOOL = "School zone"


class ChallanStatus(Enum):
    DRAFT = "Draft"
    ISSUED = "Issued"
    PAID = "Paid"
    DISPUTED = "Disputed"
    OVERDUE = "Overdue"
    DISMISSED = "Dismissed"
    UPHELD = "Upheld"


# Licence class required for each vehicle category.
REQUIRED_LICENCE = {
    VehicleCategory.TWO_WHEELER: LicenceClass.TW,
    VehicleCategory.PRIVATE_CAR: LicenceClass.LMV,
    VehicleCategory.COMMERCIAL: LicenceClass.COM,
    VehicleCategory.HEAVY: LicenceClass.HGV,
}

ZONE_LIMITS = {
    Zone.CITY: 50,
    Zone.HIGHWAY: 80,
    Zone.EXPRESSWAY: 100,
    Zone.SCHOOL: 25,
}

# Statuses that are still "live" for repeat, suspension history, and duplicates
# are handled separately. Draft and Dismissed never count as prior offences.
PRIOR_STATUSES = {
    ChallanStatus.ISSUED,
    ChallanStatus.PAID,
    ChallanStatus.DISPUTED,
    ChallanStatus.OVERDUE,
    ChallanStatus.UPHELD,
}

UNPAID_STATUSES = {
    ChallanStatus.ISSUED,
    ChallanStatus.OVERDUE,
    ChallanStatus.UPHELD,
}

PAYABLE_STATUSES = {
    ChallanStatus.ISSUED,
    ChallanStatus.OVERDUE,
    ChallanStatus.UPHELD,
}

ALLOWED_TRANSITIONS = {
    (ChallanStatus.DRAFT, ChallanStatus.ISSUED),
    (ChallanStatus.ISSUED, ChallanStatus.PAID),
    (ChallanStatus.ISSUED, ChallanStatus.DISPUTED),
    (ChallanStatus.ISSUED, ChallanStatus.OVERDUE),
    (ChallanStatus.OVERDUE, ChallanStatus.PAID),
    (ChallanStatus.DISPUTED, ChallanStatus.DISMISSED),
    (ChallanStatus.DISPUTED, ChallanStatus.UPHELD),
    (ChallanStatus.UPHELD, ChallanStatus.PAID),
}


@dataclass
class Owner:
    owner_id: str
    name: str
    clearance_blocked: bool = False
    unpaid_total: int = 0


@dataclass
class Vehicle:
    registration_number: str
    owner_id: str
    category: VehicleCategory


@dataclass
class Licence:
    owner_id: str
    licence_class: LicenceClass
    expiry_date: date
    status: LicenceStatus


@dataclass
class Challan:
    challan_id: str
    vehicle_reg: str
    owner_id: str
    violation: ViolationType
    offence_date: date
    zone: Zone | None = None
    recorded_speed: int | None = None
    status: ChallanStatus = ChallanStatus.DRAFT
    base_fine: int | None = None
    calculated_fine: int | None = None
    repeat_applied: bool = False
    suspension_recommended: bool = False
    licence_invalid: bool = False
    due_date: date | None = None
    dispute_date: date | None = None
    payment_date: date | None = None
    amount_paid: int | None = None
