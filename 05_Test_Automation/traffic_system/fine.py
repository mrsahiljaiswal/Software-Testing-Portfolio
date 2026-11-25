"""Fine amount and the amount due on a payment date.

Fines:
- Signal jump: 500 rupees for either vehicle.
- No helmet: 1000 rupees, and only for a Two-wheeler.
- Overspeeding: the limit is 60 km/h for every vehicle.
  Speed 60 or below is not an offence.
  Speed 61 to 80 is 500 rupees.
  Speed 81 or above is 2000 rupees.

The due date is the challan date plus 15 days.
On or before the due date the owner pays the fine.
After the due date the owner pays the fine plus 200 rupees.
"""

from __future__ import annotations

from datetime import date, timedelta

from models import TrafficError, VehicleType, Violation

SPEED_LIMIT = 60
LOWER_BAND_MAX = 80
LATE_FEE = 200
DUE_DAYS = 15


def calculate_fine(vehicle_type: VehicleType, violation: Violation,
                   speed: int | None = None) -> int:
    """Return the fine in rupees, or reject the challan."""
    if not isinstance(vehicle_type, VehicleType):
        raise TrafficError("Unknown vehicle type")
    if not isinstance(violation, Violation):
        raise TrafficError("Unknown violation")

    if violation == Violation.SIGNAL_JUMP:
        return 500

    if violation == Violation.NO_HELMET:
        if vehicle_type != VehicleType.TWO_WHEELER:
            raise TrafficError("No helmet applies to a two-wheeler only")
        return 1000

    if violation == Violation.OVERSPEEDING:
        return _overspeed_fine(speed)

    raise TrafficError("Unknown violation")


def _overspeed_fine(speed: int | None) -> int:
    if speed is None:
        raise TrafficError("Overspeeding requires a speed")
    # bool is a subclass of int, and it is not a speed.
    if isinstance(speed, bool) or not isinstance(speed, int):
        raise TrafficError("Speed must be a whole number of km/h")
    if speed < 0:
        raise TrafficError("Speed cannot be negative")
    # 60 is within the limit. The 500-rupee band starts at 61.
    if speed <= SPEED_LIMIT:
        raise TrafficError("Speed is not above 60 km/h")
    if speed <= LOWER_BAND_MAX:
        return 500
    return 2000


def due_date_for(challan_date: date) -> date:
    """Due date is 15 days after the challan date."""
    return challan_date + timedelta(days=DUE_DAYS)


def amount_due(fine: int, due_date: date, payment_date: date) -> int:
    """Payable rupees. After the due date, add a flat late fee of 200."""
    if payment_date <= due_date:
        return fine
    return fine + LATE_FEE
