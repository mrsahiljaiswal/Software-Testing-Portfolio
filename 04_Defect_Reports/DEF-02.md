# DEF-02 — Clearance blocked at exactly 5000

| Field | Value |
| --- | --- |
| ID | DEF-02 |
| Title | Clearance blocked at an unpaid total of exactly 5000 |
| Module | Registration |
| Severity | Major |
| Priority | High |
| Build found | B1, 18 November 2026 |
| Detected in | TC-BVA-22 |
| Status | Closed |
| Fixed in | Build B2, 19 November 2026 |
| Retest | 20 November 2026, Pass |

## Description

A new vehicle is blocked only when the owner’s unpaid total is greater than 5000. Exactly 5000 must not block. Build B1 treated 5000 as blocked.

## Steps

1. Register owner OWN1 and private car MH01AA0001 with a valid licence.
2. On 1 April 2026 issue no insurance (fine 2000) and expressway speed 140 (fine 3000). The two challans share a date, so neither is a prior offence.
3. Read the unpaid total on 1 April 2026.
4. Register MH01AA0002 for OWN1 on that date.

## Expected

Unpaid total 5000. `clearance_blocked` is false. MH01AA0002 is stored. The clearance report is empty.

## Actual (Build B1)

`clearance_blocked` was set true and registration of MH01AA0002 was rejected.

## Fix

The comparison was changed from `total >= 5000` to `total > 5000`. The flag is recomputed from the challans, so it is cleared again when a later payment brings the total to 5000 or below. The check is `_update_clearance` in `system.py`.

## Retest result

TC-BVA-22 passed on Build B2: the second vehicle was stored and the flag stayed false. TC-BVA-23 still blocks at 5001. Regression methods: `test_TC_BVA_22_unpaid_5000_does_not_block` and `test_TC_BVA_23_unpaid_5001_blocks_registration`.
