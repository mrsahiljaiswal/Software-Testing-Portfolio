# Test Plan — Vehicle Traffic Violation and Fine Management System

| Item | Detail |
| --- | --- |
| Document ID | TP-VTFMS-01 |
| Application | Vehicle Traffic Violation and Fine Management System |
| Version | 1.0 |
| Student | [Your Name], [Your Roll Number] |
| Class / Semester | [Your Class and Semester] |
| College / Department | [Your College and Department] |
| Team | [Member 1] (Test Lead), [Member 2] (Test Designer), [Member 3] (Test Executor) |
| Testing window | 3 November 2026 – 21 November 2026 |

## 1. Introduction

An officer registers a vehicle and records a challan. The system calculates one fine. The owner pays that fine. This plan is the rules baseline for every test case, defect report, and automated test.

The item under test is the Python module in `05_Test_Automation/traffic_system/`. It does not call a payment gateway or a police database.

### 1.1 Example to remember

A Car jumps a signal on 1 June 2026.

- Fine: ₹500
- Due date: 16 June 2026 (15 days later)
- Pay on 16 June: ₹500
- Pay on 17 June: ₹700

A Two-wheeler at 80 km/h is fined ₹500. At 81 km/h the fine is ₹2000. At 60 km/h the challan is rejected. A Car with no helmet is rejected.

## 2. The four inputs

| Input | Allowed values |
| --- | --- |
| Vehicle type | Two-wheeler or Car |
| Violation | Signal jump, No helmet, or Overspeeding |
| Speed | Whole km/h. Used only for Overspeeding. |
| Payment date | Compared with the due date |

## 3. Rules baseline

### 3.1 Registration

| ID | Rule |
| --- | --- |
| REQ-REG-01 | A vehicle number is required. Blank text is rejected. The stored number is trimmed and written in uppercase. The same number cannot be registered twice. `ka01ab1234` and `KA01AB1234` are the same number. |

### 3.2 Fines

| ID | Rule |
| --- | --- |
| REQ-FINE-01 | Signal jump is ₹500 for a Two-wheeler and for a Car. |
| REQ-FINE-02 | No helmet is ₹1000, and only for a Two-wheeler. A Car is rejected and no challan is stored. |
| REQ-FINE-03 | Overspeeding has one limit, 60 km/h, for every vehicle. Speed 60 or below is not an offence and the challan is rejected. Speed 61 to 80 is ₹500. Speed 81 or above is ₹2000. |

A rejected challan is not stored.

### 3.3 Payment

| ID | Rule |
| --- | --- |
| REQ-PAY-01 | The due date is the challan date plus 15 days. On or before the due date, the payable amount is the fine. |
| REQ-PAY-02 | After the due date, the payable amount is the fine plus ₹200. The late fee is ₹200 on the first late day and on every later day. |
| REQ-PAY-03 | The amount paid must equal the payable amount. A smaller amount is rejected and the status does not change. A paid challan cannot be paid again. |

### 3.4 States

| ID | Rule |
| --- | --- |
| REQ-ST-01 | Allowed: Issued → Paid (exact on-time or late amount); Issued → Overdue (unpaid, and the date is after the due date); Overdue → Paid (exact late amount). Every other move is rejected, including Paid → anything and Overdue → Issued. Marking Overdue on the due date is rejected. The status stays Issued. |

## 4. Scope

In scope: vehicle registration, recording a challan, the fine, the payment, and the three states.

Out of scope: a payment gateway, cameras, a phone app, and a live police database. The module is a college case study.

## 5. Features to be tested

| Feature | Cases |
| --- | --- |
| Signal jump ₹500 | TC-EP-01, TC-EP-02, TC-DT-01 |
| No helmet | TC-EP-03, TC-EP-04, TC-DT-02, TC-DT-03, TC-BVA-07 |
| Speed classes and the 60 / 80 edges | TC-EP-05 to TC-EP-08, TC-BVA-01 to TC-BVA-04, TC-DT-04 |
| Due date and on-time payment | TC-BVA-05, TC-DT-05, TC-ST-01 |
| Late fee of ₹200 | TC-BVA-06, TC-BVA-07, TC-DT-06, TC-ST-03 |
| Short payment and a second payment | TC-BVA-08, TC-ST-04 |
| The three states, including rejected moves | TC-ST-01 to TC-ST-06 |
| Vehicle number | Two automated tests for REQ-REG-01 |

## 6. Test approach

| Technique | Cases | What it covers |
| --- | ---: | --- |
| Equivalence partitioning | 8 | Vehicle type × violation, plus speed within the limit, slightly over, and well over |
| Boundary value analysis | 8 | Speed 60, 61, 80, 81; payment on the due date and the day after; late fee ₹200 |
| Decision tables | 6 | Table A: accept or reject a challan. Table B: amount due, on time or late |
| State transition | 6 | 3 valid moves and 3 invalid moves |
| **Total** | **28** | |

Automation is extra. `unittest` runs 30 tests: the 28 manual cases, two registration checks, and the three defect regressions (those three sit inside the 28). It does not add manual cases.

Builds:

- **Build B1** — the module on 17 November 2026, before the three fixes.
- **Build B2** — the corrected module from 19 November 2026. The code in this repository is Build B2.

## 7. Entry and exit

Entry: these rules are agreed, and Python 3 can import the module.

Exit, all met by this portfolio:

- All 28 manual cases have a final result of Pass.
- DEF-01, DEF-02, and DEF-03 are Closed.
- The automated suite passes on Build B2 (30 tests, 0 failures).
- Every requirement in section 3 is linked to a test.

## 8. Environment

| Item | Value |
| --- | --- |
| Operating system | Windows 10/11, PowerShell |
| Python | 3.12.6 |
| Automation | Python `unittest` (standard library) |
| Documents | Markdown in this repository |

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

## 9. Roles

| Role | Name | Work |
| --- | --- | --- |
| Test Lead | [Member 1] | This plan and the exit review |
| Test Designer | [Member 2] | The 28 cases and the automation mapping |
| Test Executor | [Member 3] | The execution log, the defect reports, and the retest |

## 10. Schedule

| Dates | Work | Output |
| --- | --- | --- |
| 3–7 Nov 2026 | Freeze these rules | This test plan |
| 10–14 Nov 2026 | Design the 28 cases | `02_Test_Case_Design/` |
| 17–18 Nov 2026 | Cycle 1 on Build B1 | 21 Pass, 7 Fail |
| 19 Nov 2026 | Fix DEF-01, DEF-02, DEF-03 | Build B2 |
| 20–21 Nov 2026 | Retest the 7 failed cases | 28 Pass, summary report |

## 11. Risks

| Risk | What we did |
| --- | --- |
| Speed 60 is fined by mistake | TC-BVA-01 sits on 60. TC-BVA-02 sits on 61. |
| A Car is challaned for no helmet | TC-EP-04 and TC-DT-03 both reject it. |
| The late fee is missed, or it changes with the size of the fine | TC-BVA-06 expects ₹700. TC-BVA-07 expects ₹1200, which is ₹1000 + ₹200. |

## 12. Deliverables

| Folder | Deliverable |
| --- | --- |
| `01_Test_Plan/` | This plan |
| `02_Test_Case_Design/` | Four technique files and the index |
| `03_Test_Execution/` | Log and summary |
| `04_Defect_Reports/` | Defect log and DEF-01 to DEF-03 |
| `05_Test_Automation/` | Module, 30 unit tests, mapping, console output |
| `06_Test_Reports/` | Summary and traceability |
| `07_Screenshots/` | Diagrams and the console copy |

## 13. Approvals

| Role | Name | Date |
| --- | --- | --- |
| Test Lead | [Member 1] | |
| Test Designer | [Member 2] | |
| Test Executor | [Member 3] | |
| Faculty | | |
