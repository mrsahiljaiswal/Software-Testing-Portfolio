"""Vehicle Traffic Violation and Fine Management System.

The module records vehicles, licences, challans, payments, and disputes.
It applies the course requirements baseline exactly. It does not call a
payment gateway or an external transport-department service.
"""

from __future__ import annotations

from datetime import date

from fine import (
    apply_repeat_and_surcharge,
    clearance_contribution,
    compute_base,
    compute_payable,
    dispute_deadline,
    due_date_for,
)
from models import (
    ALLOWED_TRANSITIONS,
    PRIOR_STATUSES,
    REQUIRED_LICENCE,
    UNPAID_STATUSES,
    Challan,
    ChallanStatus,
    Licence,
    LicenceClass,
    LicenceStatus,
    Owner,
    TrafficError,
    Vehicle,
    VehicleCategory,
    ViolationType,
    Zone,
)

CLEARANCE_LIMIT = 5000
REPEAT_WINDOW_DAYS = 180


class TrafficSystem:
    def __init__(self) -> None:
        self.owners: dict[str, Owner] = {}
        self.vehicles: dict[str, Vehicle] = {}
        self.licences: dict[str, Licence] = {}
        self.challans: dict[str, Challan] = {}
        self._next_id = 1

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_owner(self, owner_id: str, name: str) -> Owner:
        owner_id = self._required_text(owner_id, "Owner id")
        name = self._required_text(name, "Owner name")
        if owner_id in self.owners:
            raise TrafficError("Duplicate owner id")
        owner = Owner(owner_id=owner_id, name=name)
        self.owners[owner_id] = owner
        return owner

    def register_vehicle(self, registration_number: str, owner_id: str,
                         category: VehicleCategory, as_of: date) -> Vehicle:
        reg = self._normalise_registration(registration_number)
        owner_id = self._required_text(owner_id, "Owner id")
        as_of = self._as_date(as_of, "Registration date")
        if not isinstance(category, VehicleCategory):
            raise TrafficError("Unknown vehicle category")
        if owner_id not in self.owners:
            raise TrafficError("Owner does not exist")
        if reg in self.vehicles:
            raise TrafficError("Duplicate registration number")

        # Recompute from the challans on this date. Exactly 5000 does not block.
        self._update_clearance(owner_id, as_of)
        if self.owners[owner_id].clearance_blocked:
            raise TrafficError("Clearance blocked: unpaid total is above 5000")

        vehicle = Vehicle(registration_number=reg, owner_id=owner_id, category=category)
        self.vehicles[reg] = vehicle
        return vehicle

    def register_licence(self, owner_id: str, licence_class: LicenceClass,
                         expiry_date: date, status: LicenceStatus) -> Licence:
        owner_id = self._required_text(owner_id, "Owner id")
        expiry_date = self._as_date(expiry_date, "Licence expiry date")
        if owner_id not in self.owners:
            raise TrafficError("Owner does not exist")
        if not isinstance(licence_class, LicenceClass):
            raise TrafficError("Unknown licence class")
        if not isinstance(status, LicenceStatus):
            raise TrafficError("Unknown licence status")
        licence = Licence(
            owner_id=owner_id,
            licence_class=licence_class,
            expiry_date=expiry_date,
            status=status,
        )
        self.licences[owner_id] = licence
        return licence

    # ------------------------------------------------------------------
    # Challans
    # ------------------------------------------------------------------

    def create_draft(self, registration_number: str, violation: ViolationType,
                     offence_date: date, zone: Zone | None = None,
                     recorded_speed: int | None = None) -> Challan:
        """Store a draft. Category, speed, duplicate, and fine checks run on submit."""
        reg = self._normalise_registration(registration_number)
        offence_date = self._as_date(offence_date, "Offence date")
        self._require_violation(violation, zone)
        if reg not in self.vehicles:
            raise TrafficError("Vehicle is not registered")
        vehicle = self.vehicles[reg]
        challan = Challan(
            challan_id=self._new_id(),
            vehicle_reg=reg,
            owner_id=vehicle.owner_id,
            violation=violation,
            offence_date=offence_date,
            zone=zone,
            recorded_speed=recorded_speed,
            status=ChallanStatus.DRAFT,
        )
        self.challans[challan.challan_id] = challan
        return challan

    def submit(self, challan_id: str) -> Challan:
        challan = self._get(challan_id)
        self._require_transition(challan, ChallanStatus.ISSUED)
        self._apply_issue_fields(challan)
        self._update_clearance(challan.owner_id, challan.offence_date)
        return challan

    def issue_challan(self, registration_number: str, violation: ViolationType,
                      offence_date: date, zone: Zone | None = None,
                      recorded_speed: int | None = None) -> Challan:
        """Validate and store an Issued challan. A rejected attempt is not stored."""
        reg = self._normalise_registration(registration_number)
        offence_date = self._as_date(offence_date, "Offence date")
        self._require_violation(violation, zone)
        if reg not in self.vehicles:
            raise TrafficError("Vehicle is not registered")
        vehicle = self.vehicles[reg]
        fields = self._compute_fields(
            reg, vehicle, violation, offence_date, zone, recorded_speed, exclude_id=None,
        )
        challan = Challan(
            challan_id=self._new_id(),
            vehicle_reg=reg,
            owner_id=vehicle.owner_id,
            violation=violation,
            offence_date=offence_date,
            zone=zone,
            recorded_speed=recorded_speed,
            status=ChallanStatus.ISSUED,
            **fields,
        )
        self.challans[challan.challan_id] = challan
        self._update_clearance(challan.owner_id, offence_date)
        return challan

    def dispute(self, challan_id: str, dispute_date: date) -> Challan:
        challan = self._get(challan_id)
        dispute_date = self._as_date(dispute_date, "Dispute date")
        self._require_transition(challan, ChallanStatus.DISPUTED)
        last = dispute_deadline(challan.offence_date)
        if dispute_date < challan.offence_date or dispute_date > last:
            raise TrafficError("Dispute is outside the 15-day window")
        challan.status = ChallanStatus.DISPUTED
        challan.dispute_date = dispute_date
        return challan

    def review_dispute(self, challan_id: str, decision: str) -> Challan:
        challan = self._get(challan_id)
        if decision == "Dismissed":
            target = ChallanStatus.DISMISSED
        elif decision == "Upheld":
            target = ChallanStatus.UPHELD
        else:
            raise TrafficError("Decision must be Dismissed or Upheld")
        self._require_transition(challan, target)
        challan.status = target
        self._update_clearance(challan.owner_id, challan.offence_date)
        return challan

    def mark_overdue(self, challan_id: str, as_of: date) -> Challan:
        challan = self._get(challan_id)
        as_of = self._as_date(as_of, "Current date")
        self._require_transition(challan, ChallanStatus.OVERDUE)
        if as_of <= challan.due_date:
            raise TrafficError("Challan is not overdue")
        challan.status = ChallanStatus.OVERDUE
        self._update_clearance(challan.owner_id, as_of)
        return challan

    def mark_all_overdue(self, as_of: date) -> list[Challan]:
        as_of = self._as_date(as_of, "Current date")
        marked = []
        for challan_id in list(self.challans):
            challan = self.challans[challan_id]
            if challan.status == ChallanStatus.ISSUED and as_of > challan.due_date:
                marked.append(self.mark_overdue(challan_id, as_of))
        return marked

    def pay(self, challan_id: str, payment_date: date, amount: int) -> Challan:
        challan = self._get(challan_id)
        payment_date = self._as_date(payment_date, "Payment date")
        self._require_transition(challan, ChallanStatus.PAID)
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise TrafficError("Amount tendered must be a whole number of rupees")
        expected = self.payable_amount(challan_id, payment_date)
        if amount != expected:
            raise TrafficError(
                f"Amount tendered {amount} does not equal payable {expected}"
            )
        challan.status = ChallanStatus.PAID
        challan.payment_date = payment_date
        challan.amount_paid = amount
        # Paying a fine does not change licence status.
        self._update_clearance(challan.owner_id, payment_date)
        return challan

    def payable_amount(self, challan_id: str, payment_date: date) -> int:
        challan = self._get(challan_id)
        payment_date = self._as_date(payment_date, "Payment date")
        if challan.calculated_fine is None:
            raise TrafficError("Challan has no calculated fine")
        return compute_payable(
            challan.calculated_fine,
            challan.violation,
            challan.suspension_recommended,
            challan.offence_date,
            challan.status,
            payment_date,
        )

    # ------------------------------------------------------------------
    # Clearance and reports
    # ------------------------------------------------------------------

    def unpaid_total(self, owner_id: str, as_of: date) -> int:
        owner_id = self._required_text(owner_id, "Owner id")
        as_of = self._as_date(as_of, "As-of date")
        if owner_id not in self.owners:
            raise TrafficError("Owner does not exist")
        total = 0
        for challan in self.challans.values():
            if challan.owner_id != owner_id or challan.status not in UNPAID_STATUSES:
                continue
            total += clearance_contribution(
                challan.calculated_fine,
                challan.violation,
                challan.suspension_recommended,
                challan.offence_date,
                challan.status,
                as_of,
            )
        return total

    def refresh_clearance(self, owner_id: str, as_of: date) -> Owner:
        self._update_clearance(owner_id, as_of)
        return self.owners[owner_id]

    def report_pending(self, as_of: date) -> list[Challan]:
        """Issued, Overdue, and Upheld challans. Paid and Dismissed are omitted."""
        self._as_date(as_of, "Report date")
        return [
            c for c in self.challans.values()
            if c.status in UNPAID_STATUSES
        ]

    def report_overdue(self, as_of: date) -> list[Challan]:
        """Challans whose status is Overdue. The scan sets that status."""
        self._as_date(as_of, "Report date")
        return [c for c in self.challans.values() if c.status == ChallanStatus.OVERDUE]

    def report_repeat_offenders(self, as_of: date) -> list[str]:
        """Owners with two non-dismissed, non-draft challans of the same type
        whose offence dates are at most 180 days apart.
        """
        self._as_date(as_of, "Report date")
        by_owner: dict[str, list[Challan]] = {}
        for challan in self.challans.values():
            if challan.status not in PRIOR_STATUSES:
                continue
            by_owner.setdefault(challan.owner_id, []).append(challan)
        found = [owner_id for owner_id, items in by_owner.items() if _repeat_pair(items)]
        return sorted(found)

    def report_clearance_blocked(self, as_of: date) -> list[str]:
        as_of = self._as_date(as_of, "Report date")
        for owner_id in list(self.owners):
            self._update_clearance(owner_id, as_of)
        return sorted(
            owner.owner_id for owner in self.owners.values() if owner.clearance_blocked
        )

    # ------------------------------------------------------------------
    # Internal rules
    # ------------------------------------------------------------------

    def _apply_issue_fields(self, challan: Challan) -> None:
        vehicle = self.vehicles[challan.vehicle_reg]
        fields = self._compute_fields(
            challan.vehicle_reg,
            vehicle,
            challan.violation,
            challan.offence_date,
            challan.zone,
            challan.recorded_speed,
            exclude_id=challan.challan_id,
        )
        challan.base_fine = fields["base_fine"]
        challan.calculated_fine = fields["calculated_fine"]
        challan.repeat_applied = fields["repeat_applied"]
        challan.suspension_recommended = fields["suspension_recommended"]
        challan.licence_invalid = fields["licence_invalid"]
        challan.due_date = fields["due_date"]
        challan.status = ChallanStatus.ISSUED

    def _compute_fields(self, reg: str, vehicle: Vehicle, violation: ViolationType,
                        offence_date: date, zone: Zone | None,
                        recorded_speed: int | None, exclude_id: str | None) -> dict:
        base, speed_or_drunk_flag = compute_base(
            violation, vehicle.category, zone, recorded_speed,
        )
        if self._is_duplicate(reg, violation, offence_date, exclude_id):
            raise TrafficError(
                "Duplicate challan for the same vehicle, violation, and offence date"
            )
        priors = self._prior_challans(vehicle.owner_id, offence_date, exclude_id)
        repeat = any(prior.violation == violation for prior in priors)
        fine = apply_repeat_and_surcharge(base, repeat, vehicle.category)
        suspension = speed_or_drunk_flag or len(priors) >= 2
        return {
            "base_fine": base,
            "calculated_fine": fine,
            "repeat_applied": repeat,
            "suspension_recommended": suspension,
            "licence_invalid": not self._licence_valid(
                vehicle.owner_id, vehicle.category, offence_date,
            ),
            "due_date": due_date_for(offence_date),
        }

    def _is_duplicate(self, reg: str, violation: ViolationType, offence_date: date,
                      exclude_id: str | None) -> bool:
        for challan in self.challans.values():
            if exclude_id and challan.challan_id == exclude_id:
                continue
            if (
                challan.vehicle_reg == reg
                and challan.violation == violation
                and challan.offence_date == offence_date
            ):
                return True
        return False

    def _prior_challans(self, owner_id: str, offence_date: date,
                        exclude_id: str | None) -> list[Challan]:
        found = []
        for challan in self.challans.values():
            if exclude_id and challan.challan_id == exclude_id:
                continue
            if challan.owner_id != owner_id or challan.status not in PRIOR_STATUSES:
                continue
            if challan.offence_date >= offence_date:
                continue
            if (offence_date - challan.offence_date).days <= REPEAT_WINDOW_DAYS:
                found.append(challan)
        return found

    def _licence_valid(self, owner_id: str, category: VehicleCategory,
                       offence_date: date) -> bool:
        licence = self.licences.get(owner_id)
        if licence is None:
            return False
        if licence.status != LicenceStatus.ACTIVE:
            return False
        if licence.expiry_date < offence_date:
            return False
        if licence.licence_class != REQUIRED_LICENCE[category]:
            return False
        return True

    def _update_clearance(self, owner_id: str, as_of: date) -> None:
        total = self.unpaid_total(owner_id, as_of)
        owner = self.owners[owner_id]
        owner.unpaid_total = total
        # Strictly above 5000. An unpaid total of exactly 5000 does not block.
        owner.clearance_blocked = total > CLEARANCE_LIMIT

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
    def _required_text(value: str, label: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise TrafficError(f"{label} is required")
        return value.strip()

    @staticmethod
    def _normalise_registration(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise TrafficError("Registration number is required")
        return value.strip().upper()

    @staticmethod
    def _as_date(value: date, label: str) -> date:
        # Reject datetime subclasses; only a calendar date is accepted.
        if type(value) is not date:
            raise TrafficError(f"{label} must be a calendar date")
        return value

    @staticmethod
    def _require_violation(violation: ViolationType, zone: Zone | None) -> None:
        if not isinstance(violation, ViolationType):
            raise TrafficError("Unknown violation type")
        if zone is not None and not isinstance(zone, Zone):
            raise TrafficError("Unknown speed zone")


def _repeat_pair(challans: list[Challan]) -> bool:
    by_type: dict[ViolationType, list[date]] = {}
    for challan in challans:
        by_type.setdefault(challan.violation, []).append(challan.offence_date)
    for dates in by_type.values():
        dates.sort()
        for later_index, later in enumerate(dates):
            for earlier in dates[:later_index]:
                if (later - earlier).days <= REPEAT_WINDOW_DAYS:
                    return True
    return False
