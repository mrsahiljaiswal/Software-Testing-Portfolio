# Test Summary Report — VTFMS

| Item | Detail |
| --- | --- |
| Application | Vehicle Traffic Violation and Fine Management System |
| Report date | 21 November 2026 |
| Automation confirmation | 24 November 2026 |
| Build reported | B2, the module in `05_Test_Automation/traffic_system/` |
| Author | [Member 3], reviewed by [Member 1] |
| Audience | Faculty demonstration and viva |

## 1. Executive summary

Build B2 meets the requirements baseline for the seven in-scope modules. All 77 manual cases pass after retest. All 92 automated tests passed on 24 November 2026. Five defects found on Build B1 are Closed. The recommendation is that the module is ready for demonstration.

The test item is a local Python module. It is not a live traffic-police system.

## 2. Scope

In scope: registration, licence check, challan recording, fine calculation, payment, dispute handling, the four reports, and the challan state machine. Out of scope: payment gateways, cameras, court proceedings, and automatic updates to an external licence register. `suspension_recommended` is stored on the challan and does not change the licence status.

The baseline is section 4 of `01_Test_Plan/Test_Plan.md`.

## 3. Environment

| Item | Value |
| --- | --- |
| OS | Windows, PowerShell |
| Python | 3.12.6 (tags/v3.12.6:a4a2d2b, Sep 6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] |
| Automation | `unittest` from the standard library |
| Java / Maven | OpenJDK 17.0.18 is installed. Maven is not. JUnit was not used because that would have required a download. |
| Execution style | Manual cases against the baseline and the local module; automated cases in-process |

## 4. Results

| Set | Pass | Fail | Total | Pass % |
| --- | ---: | ---: | ---: | ---: |
| Manual, cycle 1 (17–18 Nov 2026) | 69 | 8 | 77 | 89.61% |
| Manual, final (20 Nov 2026) | 77 | 0 | 77 | 100% |
| Automated (24 Nov 2026) | 92 | 0 | 92 | 100% |

| Technique | Cases | Final Pass |
| --- | ---: | ---: |
| Equivalence partitioning | 20 | 20 |
| Boundary value analysis | 24 | 24 |
| Decision table | 16 | 16 |
| State transition | 17 | 17 |
| Total | 77 | 77 |

| Module | Cases | Final Pass |
| --- | ---: | ---: |
| Registration | 6 | 6 |
| Licence | 4 | 4 |
| Challan recording | 12 | 12 |
| Fine calculation | 15 | 15 |
| Payment | 23 | 23 |
| Dispute | 11 | 11 |
| Reports | 6 | 6 |
| Total | 77 | 77 |

Worked examples checked by these cases include a private first signal jump at 1000, a private repeat at 2000, a commercial first signal jump at 1500, a commercial repeat at 3000, a heavy overspeed of 10 at 750, and a two-wheeler overspeed of 41 at 5000 with suspension recommended.

## 5. Defect summary

| ID | Title | Final status |
| --- | --- | --- |
| DEF-01 | Speed band off-by-one at 11, 21, and 41 km/h over | Closed |
| DEF-02 | Clearance blocked at exactly 5000 | Closed |
| DEF-03 | No-helmet challan accepted for a non-two-wheeler | Closed |
| DEF-04 | Dispute accepted on day 16 | Closed |
| DEF-05 | Early discount given for drunk driving | Closed |

Open defects: 0. Deferred defects: 0.

## 6. Residual risk

- The module has no user interface. A future screen could send the wrong date or the wrong amount even though the module rejects it.
- Clearance and late penalties are correct for the rules, but they are not reconciled with a bank.
- `suspension_recommended` is advice on the challan. It does not suspend a licence at a transport office.
- Concurrent officers editing the same challan are out of scope.

None of these residual items is an open failure of a tested rule.

## 7. Recommendation

Ready for demonstration. Walk one case from each technique, one closed defect, and the unittest command in the README.

## 8. Traceability overview

Every requirement in the baseline maps to at least one manual case and at least one automated method, all Pass on Build B2. The full matrix is `Requirements_Traceability.md`.
