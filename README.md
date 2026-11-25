# Software Testing Portfolio

**Application:** Vehicle Traffic Violation and Fine Management System

A traffic officer records a challan. The system calculates one fine. The owner pays it.

| Item | Detail |
| --- | --- |
| Student | [Your Name] |
| Roll number | [Your Roll Number] |
| Class and semester | [Your Class and Semester] |
| College and department | [Your College and Department] |
| Team | [Member 1], [Member 2], [Member 3] |
| Subject | Software Testing |

Replace the placeholders before submission.

## Four inputs

1. Vehicle type: Two-wheeler or Car
2. Violation: Signal jump, No helmet, or Overspeeding
3. Speed (km/h): used only for Overspeeding
4. Payment date, compared with the due date

## Fines

| Situation | Fine |
| --- | --- |
| Signal jump, either vehicle | ₹500 |
| No helmet, Two-wheeler only | ₹1000 |
| No helmet on a Car | Challan rejected |
| Overspeeding, speed 60 or below | Challan rejected. Not an offence. |
| Overspeeding, speed 61 to 80 | ₹500 |
| Overspeeding, speed 81 or above | ₹2000 |

The speed limit is 60 km/h for every vehicle.

## Payment and states

The due date is the challan date plus 15 days.

- Paid on or before the due date: the fine exactly
- Paid after the due date: the fine + ₹200 late fee, exactly
- A smaller amount is rejected
- A paid challan cannot be paid again

A challan has three states:

- Issued → Paid, when the exact on-time or late amount is paid
- Issued → Overdue, when it is still unpaid after the due date
- Overdue → Paid, when the exact late amount is paid

Every other move is rejected, including Paid → anything and Overdue → Issued.

Registration is one rule: a vehicle number is required, stored in uppercase, and unique.

## How to run the tests

From PowerShell, in this folder:

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

Python 3.12.6. The tests use the standard library only. No `pip install`. A passing run ends with `Ran 30 tests` and `OK`. The saved output is `05_Test_Automation/test_run_output.txt` and `07_Screenshots/test_execution_console.txt`.

## Counts

| Item | Count |
| --- | --- |
| Equivalence partitioning | 8 (`TC-EP-01` to `TC-EP-08`) |
| Boundary value analysis | 8 (`TC-BVA-01` to `TC-BVA-08`) |
| Decision tables | 6 (`TC-DT-01` to `TC-DT-06`) |
| State transition | 6 (`TC-ST-01` to `TC-ST-06`) |
| **Manual test cases** | **28** |
| Cycle 1 (17–18 Nov 2026) | 21 Pass, 7 Fail |
| Final manual result (20 Nov 2026) | 28 Pass, 0 Fail |
| Automated tests | 30 Pass, 0 Fail |
| Defects | `DEF-01`, `DEF-02`, `DEF-03`, all Closed |

The 30 automated tests are the 28 manual cases plus two registration checks. Three of those case tests are the regressions for DEF-01, DEF-02, and DEF-03. Testing window: 3 November 2026 – 21 November 2026.

## Folders

| Path | Purpose |
| --- | --- |
| `README.md` | This page, the mark map, and the viva points |
| `Conclusion.md` | What was tested and the result |
| `01_Test_Plan/` | Test plan and the rules |
| `02_Test_Case_Design/` | The 28 manual cases |
| `03_Test_Execution/` | Execution log and summary |
| `04_Defect_Reports/` | Defect log and DEF-01 to DEF-03 |
| `05_Test_Automation/` | Python module, 30 unit tests, and the real test run |
| `06_Test_Reports/` | Summary report and traceability |
| `07_Screenshots/` | Diagrams and the console log |

## Assessment map (20 marks)

| Component | Marks | Where to show it |
| --- | ---: | --- |
| GitHub repository creation and organization | 2 | This folder layout. The student creates the GitHub remote. |
| Test plan and application understanding | 3 | `01_Test_Plan/Test_Plan.md` |
| Test case design using testing techniques, automation/tool | 5 | `02_Test_Case_Design/` and `05_Test_Automation/` |
| Test execution and defect identification | 4 | `03_Test_Execution/` and `04_Defect_Reports/` |
| Documentation and README | 1 | This file, `06_Test_Reports/`, and `07_Screenshots/` |
| Demonstration and viva | 5 | Live with faculty. Speaking points are below. |
| **Total** | **20** | |

## Explain this in the viva

1. An officer records a challan with four inputs: vehicle type, violation, speed only when the violation is overspeeding, and the payment date.
2. The fines are fixed. Signal jump is ₹500. No helmet is ₹1000 for a Two-wheeler, and a Car is rejected. Overspeeding uses one limit, 60 km/h: 60 or below is rejected, 61 to 80 is ₹500, and 81 or above is ₹2000.
3. The due date is 15 days after the challan date. On time, the owner pays the fine. After the due date, the owner pays the fine plus ₹200. A short payment is rejected, and a paid challan stays paid.
4. We wrote 28 manual cases: 8 equivalence, 8 boundary, 6 decision-table, and 6 state-transition. Cycle 1 found three defects. All three are closed, and the final result is 28 Pass.
5. The automated check is one command, shown above. It runs 30 Python unit tests, all passing, including one regression test for each closed defect.
