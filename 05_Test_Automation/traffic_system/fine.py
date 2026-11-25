"""Fine, surcharge, and payable-amount rules.

Currency is rupees. A percentage is rounded half-up to the nearest rupee.
When the remainder is exactly one half, the value rounds away from zero.
Repeat doubling is an integer multiply and is not rounded.
"""

from __future__ import annotations

from datetime import date, timedelta

from models import (
    ChallanStatus,
    TrafficError,
    VehicleCategory,
    ViolationType,
    Zone,
    ZONE_LIMITS,
)


def percent_half_up(amount: int, percent: int) -> int:
    """Return `percent` percent of `amount`, rounded half-up to a rupee.

    Positive amounts only. A remainder of exactly 50 paise in 100 rounds up.
    """
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise TrafficError("Amount must be a whole number of rupees")
    if not isinstance(percent, int) or isinstance(percent, bool):
        raise TrafficError("Percent must be a whole number")
    if amount < 0 or percent < 0:
        raise TrafficError("Percentage applies to non-negative amounts only")
    quotient, remainder = divmod(amount * percent, 100)
    if remainder >= 50:
        return quotient + 1
    return quotient


def compute_base(violation: ViolationType, category: VehicleCategory,
                  zone: Zone | None, recorded_speed: int | None) -> tuple[int, bool]:
    """Return (base fine, speed-or-drunk suspension flag) before repeat and surcharge.

    The boolean is true for drunk driving and for overspeed of 41 km/h or more.
    Repeat history is applied by the caller.
    """
    if violation == ViolationType.NO_HELMET:
        if category != VehicleCategory.TWO_WHEELER:
            raise TrafficError("No helmet applies to two-wheelers only")
        return 500, False

    if violation == ViolationType.NO_SEATBELT:
        if category == VehicleCategory.TWO_WHEELER:
            raise TrafficError("No seatbelt does not apply to two-wheelers")
        return 1000, False

    flat = {
        ViolationType.SIGNAL_JUMP: 1000,
        ViolationType.MOBILE_USE: 1500,
        ViolationType.WRONG_PARKING: 500,
        ViolationType.NO_INSURANCE: 2000,
    }
    if violation in flat:
        return flat[violation], False

    if violation == ViolationType.DRUNK_DRIVING:
        return 10000, True

    if violation == ViolationType.OVERSPEEDING:
        return _overspeed_base(zone, recorded_speed)

    raise TrafficError("Unknown violation type")


def _overspeed_base(zone: Zone | None, recorded_speed: int | None) -> tuple[int, bool]:
    if zone is None or recorded_speed is None:
        raise TrafficError("Overspeeding requires a zone and a recorded speed")
    if zone not in ZONE_LIMITS:
        raise TrafficError("Unknown speed zone")
    if not isinstance(recorded_speed, int) or isinstance(recorded_speed, bool):
        raise TrafficError("Recorded speed must be a whole number of km/h")
    if recorded_speed < 0:
        raise TrafficError("Recorded speed cannot be negative")

    limit = ZONE_LIMITS[zone]
    # Speed at or below the zone limit is not an offence.
    if recorded_speed <= limit:
        raise TrafficError("Recorded speed is not above the zone limit")

    overspeed = recorded_speed - limit
    # Inclusive bands. 10, 20, and 40 stay in the lower band.
    # 11, 21, and 41 enter the next band. 41 and above also recommends suspension.
    if overspeed <= 10:
        return 500, False
    if overspeed <= 20:
        return 1500, False
    if overspeed <= 40:
        return 3000, False
    return 5000, True


def apply_repeat_and_surcharge(base: int, repeat: bool, category: VehicleCategory) -> int:
    """Apply the repeat multiplier, then the commercial/heavy surcharge."""
    amount = base * 2 if repeat else base
    if category in (VehicleCategory.COMMERCIAL, VehicleCategory.HEAVY):
        amount = amount + percent_half_up(amount, 50)
    return amount


def due_date_for(offence_date: date) -> date:
    return offence_date + timedelta(days=30)


def early_deadline(offence_date: date) -> date:
    return offence_date + timedelta(days=7)


def dispute_deadline(offence_date: date) -> date:
    return offence_date + timedelta(days=15)


def compute_payable(calculated_fine: int, violation: ViolationType,
                    suspension_recommended: bool, offence_date: date,
                    status: ChallanStatus, payment_date: date) -> int:
    """Payable rupees for a payment on `payment_date`.

    Early discount (10%) applies only when all of these are true:
    the payment date is on or before offence date + 7 days, the status is
    still Issued, the violation is not drunk driving, and suspension is not
    recommended. An upheld dispute removes the early discount. Late payment
    adds 25%, 50%, or 100%, and the payable amount never exceeds twice the
    calculated fine.
    """
    if payment_date <= early_deadline(offence_date):
        discount_allowed = (
            status == ChallanStatus.ISSUED
            and violation != ViolationType.DRUNK_DRIVING
            and not suspension_recommended
        )
        if discount_allowed:
            return calculated_fine - percent_half_up(calculated_fine, 10)
        return calculated_fine

    due = due_date_for(offence_date)
    if payment_date <= due:
        return calculated_fine

    days_late = (payment_date - due).days
    if days_late <= 30:
        percent = 25
    elif days_late <= 60:
        percent = 50
    else:
        percent = 100
    penalty = percent_half_up(calculated_fine, percent)
    return min(calculated_fine + penalty, calculated_fine * 2)


def clearance_contribution(calculated_fine: int, violation: ViolationType,
                           suspension_recommended: bool, offence_date: date,
                           status: ChallanStatus, as_of: date) -> int:
    """Amount this unpaid challan contributes on `as_of`.

    On or before the due date the contribution is the calculated fine
    (no early discount). After the due date it is the late-penalty payable.
    """
    if as_of <= due_date_for(offence_date):
        return calculated_fine
    return compute_payable(
        calculated_fine, violation, suspension_recommended,
        offence_date, status, as_of,
    )
