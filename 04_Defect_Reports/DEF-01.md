# DEF-01 — Speed band off-by-one

| Field | Value |
| --- | --- |
| ID | DEF-01 |
| Title | Speed band off-by-one (11 km/h over charged the 1–10 fine) |
| Module | Fine calculation |
| Severity | Major |
| Priority | High |
| Build found | B1, 18 November 2026 |
| Detected in | TC-BVA-02. The same fault also failed TC-BVA-04 and TC-BVA-06 |
| Status | Closed |
| Fixed in | Build B2, 19 November 2026 |
| Retest | 20 November 2026, Pass on TC-BVA-02, TC-BVA-04, and TC-BVA-06 |

## Description

Overspeed bands must be inclusive at 10, 20, and 40. Build B1 used upper bounds of 11, 21, and 41, so the first kilometre of each next band was still charged the previous fine. Suspension for 41 km/h or more was therefore also missed.

## Steps

1. Register a private car with a valid licence and no earlier challan.
2. Issue overspeeding in the City zone at 61 km/h (limit 50, overspeed 11).
3. Repeat with a private car at highway speed 101 and a two-wheeler at expressway speed 141.

## Expected

| Overspeed | Fine | suspension_recommended |
| ---: | ---: | --- |
| 11 | 1500 | false |
| 21 | 3000 | false |
| 41 | 5000 | true |

Overspeed 10, 20, and 40 were already correct on B1 and are not part of this defect.

## Actual (Build B1)

| Overspeed | Fine returned | suspension_recommended |
| ---: | ---: | --- |
| 11 | 500 | false |
| 21 | 1500 | false |
| 41 | 3000 | false |

## Fix

The band conditions were changed to `overspeed <= 10`, `<= 20`, and `<= 40`. Overspeed of 41 or more returns 5000 and sets the speed-suspension flag. The current function is `compute_base` in `05_Test_Automation/traffic_system/fine.py`.

## Retest result

On Build B2, TC-BVA-02 returned 1500, TC-BVA-04 returned 3000, and TC-BVA-06 returned 5000 with `suspension_recommended` true. Regression methods: `test_TC_BVA_02_overspeed_11`, `test_TC_BVA_04_overspeed_21`, `test_TC_BVA_06_overspeed_41_two_wheeler`.
