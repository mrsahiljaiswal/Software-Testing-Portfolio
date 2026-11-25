# Software Testing Portfolio

**Application:** Vehicle Traffic Violation and Fine Management System (VTFMS)

| Item | Detail |
| --- | --- |
| Student Name | Sahil Jaiswal |
| USN | 1MS23IS109 |
| Semester | VII |
| Department | ISE |
| Subject | Software Testing |
| Team Members | Vishal D. Dhamu, Prince Khatri |

Replace every bracketed placeholder before submission. This repository does not invent a student name.

## Course objectives

By completing this portfolio, the team should be able to:

1. Describe the purpose of a test plan and relate it to a fixed requirements baseline.
2. Design test cases with equivalence partitioning, boundary value analysis, decision tables, and state-transition testing.
3. Keep requirement identifiers, test-case identifiers, and expected results consistent across the design, execution, and automation.
4. Execute tests, record actual results, and write defect reports that show the fault, the fix, and the retest.
5. Automate unit tests that lock the corrected business rules and can be rerun without extra installations.
6. Summarise coverage, defects, residual risk, and a demonstration recommendation for a viva.

## Project description

VTFMS is a traffic-police system for a college case study. An officer registers a vehicle owner and a vehicle, checks the driving licence, records a challan, calculates the fine, accepts an exact payment, and handles a dispute. Supervisors use reports for pending fines, overdue challans, repeat offenders, and clearance blocks.

The system under test is a small Python module in `05_Test_Automation/traffic_system/`. It implements the requirements baseline in `01_Test_Plan/Test_Plan.md`. It is not a live production traffic system and it does not call a payment gateway.

Currency is rupees. Where a percentage is applied, the amount is rounded half-up to the nearest rupee. A remainder of exactly half a rupee rounds away from zero.

## Application modules

1. Vehicle and owner registration
2. Driving licence check
3. Violation / challan recording
4. Fine calculation (type, speed band, repeat, vehicle surcharge)
5. Fine payment (early discount and late penalty)
6. Dispute handling
7. Reports (pending fines, overdue challans, repeat offenders, clearance block)

## Testing activities

| Activity | Where it is recorded |
| --- | --- |
| Test planning and application understanding | `01_Test_Plan/Test_Plan.md` |
| Test case design with four techniques | `02_Test_Case_Design/` |
| Manual test execution and summary | `03_Test_Execution/` |
| Defect identification, fix, and retest | `04_Defect_Reports/` |
| Automated unit testing (additional activity) | `05_Test_Automation/` |
| Summary report and traceability | `06_Test_Reports/` |
| Diagrams and terminal evidence | `07_Screenshots/` |

## Techniques used

- **Equivalence partitioning** — classes such as vehicle category, licence validity, violation applicability, and report membership.
- **Boundary value analysis** — speed bands at 10/11, 20/21, and 40/41; zone limits; the 180/181-day repeat window; dispute day 15/16; payment day 7/8; due day 30/31; late bands 30/31 and 60/61; unpaid total 5000/5001; half-up rounding.
- **Decision tables** — one table for challan recording and one table for payment.
- **State transition** — Draft, Issued, Paid, Disputed, Overdue, Dismissed, and Upheld, including invalid transitions.

## Manual and automated counts

These counts are the same in the execution summary, the defect log, and the test summary report.

| Item | Count |
| --- | --- |
| Equivalence partitioning cases | 20 (`TC-EP-01` to `TC-EP-20`) |
| Boundary value analysis cases | 24 (`TC-BVA-01` to `TC-BVA-24`) |
| Decision-table cases | 16 (`TC-DT-01` to `TC-DT-16`) |
| State-transition cases | 17 (`TC-ST-01` to `TC-ST-17`) |
| **Manual test cases** | **77** |
| Cycle 1 (17–18 Nov 2026) | 69 Pass, 8 Fail |
| Final manual result after retest (20 Nov 2026) | 77 Pass, 0 Fail (100%) |
| Automated unit tests (run 24 Nov 2026) | 92 Pass, 0 Fail |
| Defects | `DEF-01` to `DEF-05`, all Closed |

The 92 automated tests cover all 77 manual cases and 15 extra regression checks. The extra checks are listed in `05_Test_Automation/Automation_Mapping.md`. They are not additional manual cases.

## Repository structure

| Path | Purpose |
| --- | --- |
| `README.md` | Portfolio entry point, assessment map, and viva order |
| `Conclusion.md` | What was tested, what was proved, and what remains out of scope |
| `01_Test_Plan/` | IEEE-style test plan and the requirements baseline |
| `02_Test_Case_Design/` | Technique notes and the 77 manual test cases |
| `03_Test_Execution/` | Execution log and execution summary |
| `04_Defect_Reports/` | Defect log and the five formal defect reports |
| `05_Test_Automation/` | Python module, unittest suite, mapping, and the real test run |
| `06_Test_Reports/` | Test summary report and requirements traceability |
| `07_Screenshots/` | What to capture in the faculty demo, Mermaid diagrams, and the console log |

## How to run the automated tests

From PowerShell, in this folder:

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

No `pip install` is required. The suite uses the Python 3 standard library only. The workstation used for this portfolio has Python 3.12.6. Java 17 is installed, but Maven is not, and this assignment does not download dependencies, so the JUnit-style additional activity is implemented with `unittest`.

The saved run is `05_Test_Automation/test_run_output.txt`. The same text is copied to `07_Screenshots/test_execution_console.txt`.

## Assessment mapping

| Assessment component | Marks | Evidence in this repository |
| --- | --- | --- |
| GitHub repository creation and organization | 2 | This folder layout and `README.md`. The remote is created by the student; this workspace was not pushed. |
| Test plan and application understanding | 3 | `01_Test_Plan/Test_Plan.md` |
| Test case design using testing techniques, including the automation activity | 5 | `02_Test_Case_Design/` and `05_Test_Automation/` |
| Test execution and defect identification | 4 | `03_Test_Execution/` and `04_Defect_Reports/` |
| Documentation and README | 1 | This file, `06_Test_Reports/`, and `07_Screenshots/` |
| Demonstration and viva | 5 | Done live with faculty. The section below is the suggested order. |
| **Total** | **20** | |

## How to demonstrate

Open the files in this order during the viva:

1. This `README.md` — name the application, the seven modules, and the 77 / 92 counts.
2. `01_Test_Plan/Test_Plan.md` — show the requirements baseline, especially speed bands, the repeat multiplier, the surcharge, the payment windows, and `clearance_blocked`.
3. One case from each technique:
   - `TC-EP-11` — no-helmet challan rejected for a private car
   - `TC-BVA-02` — 11 km/h over the city limit is fined 1500, not 500
   - `TC-DT-08` — drunk driving paid inside 7 days is still 10000
   - `TC-ST-15` — an Overdue challan cannot be disputed
4. `04_Defect_Reports/DEF-01.md` — off-by-one speed band, found, fixed, and retested. Mention that `DEF-02` through `DEF-05` are Closed as well.
5. Run the PowerShell command above and compare it with `05_Test_Automation/test_run_output.txt` (92 tests, OK).
6. `06_Test_Reports/Requirements_Traceability.md` and `07_Screenshots/Diagrams.md` — trace one requirement to a test and walk the challan state machine.
