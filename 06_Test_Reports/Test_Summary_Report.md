# Test Summary Report

| Item | Detail |
| --- | --- |
| Application | Vehicle Traffic Violation and Fine Management System |
| Test item | `05_Test_Automation/traffic_system/` |
| Window | 3 November 2026 – 21 November 2026 |
| Build reported | Build B2 (fixes of 19 November 2026) |
| Author | [Member 1] |

## What was tested

An officer records a challan. The system calculates one fine and the owner pays it. The four inputs are vehicle type, violation, speed for overspeeding, and the payment date. The rules are in `01_Test_Plan/Test_Plan.md`.

## Manual result

| Technique | Designed | Final Pass | Final Fail |
| --- | ---: | ---: | ---: |
| Equivalence partitioning | 8 | 8 | 0 |
| Boundary value analysis | 8 | 8 | 0 |
| Decision table | 6 | 6 | 0 |
| State transition | 6 | 6 | 0 |
| **Total** | **28** | **28** | **0** |

Cycle 1 on Build B1 was 21 Pass and 7 Fail. The 7 failures were retested on 20 November 2026 and passed.

## Defects

| ID | Closed? | Regression test |
| --- | --- | --- |
| DEF-01 Speed 60 was fined | Yes | `test_TC_BVA_01_DEF_01_speed_60_rejected` |
| DEF-02 No helmet accepted for a Car | Yes | `test_TC_EP_04_DEF_02_car_no_helmet_rejected` |
| DEF-03 Late fee of ₹200 was missing | Yes | `test_TC_BVA_06_DEF_03_day_after_due_adds_200` |

Open defects: 0.

## Automated result

30 tests, 0 failures. The console is `05_Test_Automation/test_run_output.txt`. It ends with `Ran 30 tests` and `OK`.

## Recommendation

The module matches the rules baseline. It is ready to demonstrate. The remaining limit is the test item itself: a local Python module, with no payment gateway and no live police database.
