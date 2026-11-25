# DEF-03 — No-helmet challan accepted for a private car

| Field | Value |
| --- | --- |
| ID | DEF-03 |
| Title | No-helmet challan accepted for a vehicle that is not a two-wheeler |
| Module | Challan recording |
| Severity | Major |
| Priority | High |
| Build found | B1, 17 November 2026 |
| Detected in | TC-EP-11. The same fault also failed TC-DT-02 |
| Status | Closed |
| Fixed in | Build B2, 19 November 2026 |
| Retest | 20 November 2026, Pass on both cases |

## Description

No helmet applies to a Two-wheeler only. Build B1 recorded it for a private car and for a commercial vehicle and stored a fine of 500.

## Steps

1. Register a private car with a valid LMV licence.
2. Issue a no-helmet challan on 1 June 2026.
3. Repeat with a commercial vehicle.

## Expected

Both attempts are rejected. No challan is stored.

## Actual (Build B1)

Each attempt stored an Issued challan with calculated fine 500.

## Fix

`compute_base` now raises an error when no helmet is used for any category other than Two-wheeler. A rejected `issue_challan` call does not leave a row behind. No seatbelt remains rejected for a Two-wheeler and allowed for other categories.

## Retest result

TC-EP-11 and TC-DT-02 passed on Build B2. A two-wheeler no-helmet challan (TC-EP-10) still calculates 500. Regression methods: `test_TC_EP_11_helmet_on_private_car_rejected` and `test_TC_DT_02_category_mismatch_rejects_helmet_on_commercial`.
