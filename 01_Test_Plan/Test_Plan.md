# Test Plan — Vehicle Traffic Violation and Fine Management System

| Item | Detail |
| --- | --- |
| Document ID | TP-VTFMS-01 |
| Application | Vehicle Traffic Violation and Fine Management System (VTFMS) |
| Version | 1.0 (requirements baseline locked for this portfolio) |
| Student | [Your Name], [Your Roll Number] |
| Class / Semester | [Your Class and Semester] |
| College / Department | [Your College and Department] |
| Team | [Member 1] (Test Lead), [Member 2] (Test Designer), [Member 3] (Test Executor) |
| Planning window | 3 November 2026 – 7 November 2026 |
| Related execution window | 17 November 2026 – 21 November 2026 |

## 1. Introduction

This plan describes how the team tests VTFMS, a college case study of a traffic-police challan system. The system registers owners and vehicles, checks a driving licence, records a violation, calculates a fine, takes an exact payment, reviews a dispute, and produces four operational reports.

The test item is the Python module in `05_Test_Automation/traffic_system/`. Manual cases were executed against this requirements baseline and against that module. The module is not connected to a live police database or a payment gateway.

### 1.1 Objectives

- Confirm that every rule in the baseline below is either tested or explicitly out of scope.
- Design 77 manual cases using four techniques, with no duplicate test identifiers.
- Record execution results, including the first-cycle failures and the retest after the fixes.
- Keep automated tests aligned with the corrected rules so the five fixed defects cannot return unnoticed.

## 2. Scope

### 2.1 In scope

1. Vehicle and owner registration
2. Driving licence check
3. Violation and challan recording
4. Fine calculation
5. Fine payment
6. Dispute handling
7. Reports: pending fines, overdue challans, repeat offenders, clearance block
8. Challan state transitions, including invalid transitions

### 2.2 Out of scope

- Payment-gateway, bank, and receipt-printer integration
- Camera devices, ANPR, and SMS or mobile-app screens
- Court prosecution after a dispute decision
- Changing a licence to Suspended because `suspension_recommended` is true (the flag is recorded; the licence status is not changed automatically)
- Insurance-company notification
- Multi-user locking and performance load
- A deployed college or city production system

## 3. Application overview

An officer registers an owner, then a vehicle, and may record one licence for that owner. A challan may be saved as Draft and then submitted, or issued in one step. On a valid submit the challan becomes Issued, the fine is stored, and the due date is the offence date plus 30 calendar days. The owner may pay the exact payable amount, or dispute the challan inside a 15-day window. A reviewer dismisses or upholds the dispute. A system job marks an unpaid Issued challan Overdue when the current date is after the due date.

### 3.1 Worked examples the tests must match

| Situation | Calculated fine | Notes |
| --- | --- | --- |
| Private car, first signal jump | 1000 | No surcharge |
| Private car, second signal jump within 180 days | 2000 | Repeat ×2, no surcharge |
| Commercial, first signal jump | 1500 | 1000 + 50% |
| Commercial, repeat signal jump | 3000 | 2000 + 50% |
| Heavy, first overspeed of 10 km/h | 750 | Base 500 + 50% |
| Two-wheeler, overspeed of 41 km/h | 5000 | `suspension_recommended = true` |
| School zone, speed 25 | Rejected | Not an offence |
| School zone, speed 26, private car | 500 | Overspeed 1 |
| City, speed 60, private car | 500 | Overspeed 10 |
| City, speed 61, private car | 1500 | Overspeed 11 |
| Highway, speed 100, private car | 1500 | Overspeed 20 |
| Highway, speed 101, private car | 3000 | Overspeed 21 |
| Expressway, speed 140, private car | 3000 | Overspeed 40 |
| Expressway, speed 141, two-wheeler | 5000 | Overspeed 41, suspension recommended |

## 4. Requirements baseline

This section is the baseline used by every test case, defect report, and automated assertion. Identifiers are stable.

### 4.1 Registration

| ID | Rule |
| --- | --- |
| REQ-REG-01 | An owner id and name are required. A duplicate owner id is rejected. |
| REQ-REG-02 | A vehicle registration number is required, unique, and stored in uppercase after trimming spaces. `mh01ab1234` and `MH01AB1234` are the same number. |
| REQ-REG-03 | The owner must already exist. |
| REQ-REG-04 | The owner unpaid total is the sum of amounts for challans in Issued, Overdue, or Upheld. On or before the due date the contribution is the calculated fine, with no early discount. After the due date the contribution is the late-penalty payable. If that total is greater than 5000, `clearance_blocked` is true and a new vehicle for that owner is rejected. Exactly 5000 does not block. The flag is recalculated; it becomes false when the total is 5000 or less. A blocked owner can still receive a challan. |

### 4.2 Driving licence

Licence classes: Two-wheeler → TW, Private car → LMV, Commercial → COM, Heavy → HGV.

| ID | Rule |
| --- | --- |
| REQ-LIC-01 | A licence is valid on the offence date only when its status is Active, its expiry date is on or after the offence date, and its class matches the vehicle. |
| REQ-LIC-02 | An expired date, a status other than Active, a wrong class, or no licence on file sets `licence_invalid = true`. The violation is still recorded. No separate no-documents fine is added. |
| REQ-LIC-03 | A Suspended licence stays Suspended after the fine is paid. Payment does not change licence status. `suspension_recommended` does not itself suspend the licence. |

### 4.3 Challan recording

| ID | Rule |
| --- | --- |
| REQ-CH-01 | No helmet is allowed only for a Two-wheeler and is rejected otherwise. No seatbelt is rejected for a Two-wheeler and allowed for Private car, Commercial, and Heavy. Signal jump, mobile use, wrong parking, no insurance, drunk driving, and overspeeding follow the fine rules below. |
| REQ-CH-02 | Overspeeding requires a zone and a recorded speed. If recorded speed is less than or equal to the zone limit, the challan is rejected. Limits: City 50, Highway 80, Expressway 100, School zone 25. Overspeed = recorded speed − zone limit. |
| REQ-CH-03 | A second challan for the same vehicle, same violation type, and same offence date is rejected. Overspeeding on the same vehicle and date is one violation regardless of zone. Draft and Dismissed rows also block that duplicate. |
| REQ-CH-04 | The issue date is the offence date. The due date is the offence date plus 30 calendar days. |

### 4.4 Fine calculation

Base fines: Signal jump 1000 (any vehicle); No helmet 500 (Two-wheeler only); No seatbelt 1000 (not a Two-wheeler); Mobile use 1500; Wrong parking 500; No insurance 2000; Drunk driving 10000.

Overspeed bands, inclusive:

| Overspeed (km/h) | Base fine | Speed suspension |
| --- | ---: | --- |
| 1 to 10 | 500 | No |
| 11 to 20 | 1500 | No |
| 21 to 40 | 3000 | No |
| 41 or more | 5000 | Yes |

| ID | Rule |
| --- | --- |
| REQ-FINE-01 | Flat base fines are the amounts above. |
| REQ-FINE-02 | Speed bands use the inclusive limits in the table. 10, 20, and 40 stay in the lower band. 11, 21, and 41 enter the next band. |
| REQ-FINE-03 | If the same owner has at least one non-dismissed, non-draft challan of the same violation type with an offence date in the 180 days before this offence date, multiply the base fine by 2 before surcharge. Day 180 counts. Day 181 does not. The same calendar day is not “before”. Dismissed and Draft challans do not count. Paid, Disputed, Upheld, Issued, and Overdue challans do count. |
| REQ-FINE-04 | After the repeat multiplier, Commercial and Heavy add 50% of that amount. Two-wheeler and Private car add nothing. This result is the calculated fine. Percentage results use half-up rounding. |
| REQ-FINE-05 | `suspension_recommended` is true when overspeed is 41 or more, or the violation is drunk driving, or the owner already has at least 2 non-dismissed, non-draft challans in the 180 days before the offence date (this challan is the third or later). The new challan is not counted in its own prior total. |

Repeat doubling is an integer multiply. Only percentage steps (surcharge, early discount, late penalty) are rounded. Half-up example: 25% of 750 is 187.5, which rounds to 188.

### 4.5 Payment

| ID | Rule |
| --- | --- |
| REQ-PAY-01 | If the payment date is on or before the offence date + 7 days, the violation is not drunk driving, `suspension_recommended` is false, and the status is still Issued, the payable amount is the calculated fine minus a 10% discount. |
| REQ-PAY-02 | If the payment date is after day 7 and on or before the due date, the payable amount is the calculated fine. |
| REQ-PAY-03 | If the payment date is after the due date, days late = payment date − due date. 1 to 30 days late: penalty 25%. 31 to 60: penalty 50%. 61 or more: penalty 100%. Payable = calculated fine + penalty, and never more than 2 × calculated fine. The day after the due date is 1 day late. The due date itself is not late. |
| REQ-PAY-04 | The amount tendered must equal the payable amount exactly. A partial payment is rejected and the status does not change. |
| REQ-PAY-05 | Paid and Dismissed challans cannot be paid again. Draft and Disputed challans cannot be paid. Issued, Overdue, and Upheld can be paid when the amount is exact. |
| REQ-PAY-06 | An Upheld challan does not receive the early discount, even inside 7 days. The dispute removed it. After the due date, an Upheld challan uses the late-penalty payable. |

### 4.6 Dispute and state

| ID | Rule |
| --- | --- |
| REQ-DIS-01 | A dispute is accepted only from Issued, on any date from the offence date through the offence date + 15 days, inclusive. Day 15 is accepted. Day 16 is rejected and the status stays Issued. A date before the offence date is rejected. |
| REQ-DIS-02 | A Disputed challan is reviewed to Dismissed or Upheld. It cannot be paid while Disputed. |
| REQ-ST-01 | Allowed transitions: Draft → Issued; Issued → Paid; Issued → Disputed; Issued → Overdue; Overdue → Paid; Disputed → Dismissed; Disputed → Upheld; Upheld → Paid. Rejected transitions include anything out of Paid or Dismissed; Draft → Paid, Draft → Disputed, Draft → Overdue; Issued → Dismissed; Overdue → Disputed; Disputed → Paid. Issued → Overdue is rejected when the current date is on or before the due date. |

### 4.7 Reports

| ID | Rule |
| --- | --- |
| REQ-REP-01 | Pending fines lists Issued, Overdue, and Upheld challans and omits Paid and Dismissed. Overdue challans lists status Overdue only (the scan sets that status). Repeat offenders lists an owner who has two non-dismissed, non-draft challans of the same type at most 180 days apart. Clearance block lists owners whose recomputed unpaid total is greater than 5000. |

## 5. Features to be tested and not tested

| Feature | Tested | Representative cases |
| --- | --- | --- |
| Owner and vehicle registration | Yes | TC-EP-01 to TC-EP-04, TC-BVA-22, TC-BVA-23 |
| Licence validity flag | Yes | TC-EP-05 to TC-EP-08, TC-DT-06 |
| Category constraints | Yes | TC-EP-10 to TC-EP-12, TC-DT-02 |
| Speed bands and zone limits | Yes | TC-BVA-01 to TC-BVA-09, TC-EP-13, TC-DT-03 |
| Repeat multiplier and window | Yes | TC-EP-16, TC-BVA-10, TC-BVA-11 |
| Surcharge and half-up rounding | Yes | TC-EP-15, TC-BVA-09, TC-BVA-24 |
| Suspension recommendation | Yes | TC-EP-14, TC-EP-20, TC-BVA-06 |
| Early, on-time, and late payment | Yes | TC-BVA-14 to TC-BVA-21, TC-DT-07 to TC-DT-16 |
| Dispute window and review | Yes | TC-BVA-12, TC-BVA-13, TC-ST-03, TC-ST-06, TC-ST-07 |
| State machine, including invalid moves | Yes | TC-ST-01 to TC-ST-17 |
| Four reports | Yes | TC-EP-17 to TC-EP-19, TC-BVA-22, TC-BVA-23 |
| Payment gateway, cameras, court, automatic RTO suspension | No | Out of scope, section 2.2 |

## 6. Test approach

Manual cases are designed from this baseline and executed on the Python module.

| Technique | Cases | What it is responsible for |
| --- | --- | --- |
| Equivalence partitioning | 20 | One representative from each class: registration, licence, category, fine class, reports |
| Boundary value analysis | 24 | Values on and just across each numeric boundary |
| Decision tables | 16 | Combinations for recording a challan and for computing a payment |
| State transition | 17 | Every allowed transition and the required invalid transitions |

Automation is the additional activity. `unittest` reruns the manual rules and 15 extra regression checks (92 tests). It does not replace the written cases.

Builds used in the log:

- **Build B1** — module snapshot on 17 November 2026, before the five fixes.
- **Build B2** — corrected module from 19 November 2026. The code in this repository is Build B2.

## 7. Entry and exit criteria

### 7.1 Entry

- This baseline is agreed and the module can be imported with Python 3.
- Test-case identifiers are unique and expected results quote this baseline.
- The environment in section 9 is available.

### 7.2 Exit

- All 77 manual cases have a final status. Critical defects found in cycle 1 are Closed.
- The automated suite passes on Build B2.
- The traceability matrix links each requirement to at least one test.
- The summary report states residual risk and a demonstration recommendation.

The portfolio meets the exit criteria: 77/77 manual Pass after retest, 92/92 automated Pass, and `DEF-01` to `DEF-05` Closed.

## 8. Test environment

| Item | Value |
| --- | --- |
| Operating system | Windows 10/11 (win32 10.0.26200), PowerShell |
| Python | 3.12.6 (tags/v3.12.6:a4a2d2b, Sep 6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] |
| Java | OpenJDK 17.0.18 is installed |
| Maven / JUnit | Not available, and dependencies were not downloaded |
| Automation | Python `unittest` (standard library) |
| Documents | Markdown in this repository |
| Manual execution | Against this baseline and the local module, not a deployed traffic system |

Command:

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

## 9. Roles

| Role | Placeholder | Responsibility |
| --- | --- | --- |
| Test Lead | [Member 1] | Baseline, plan, exit review |
| Test Designer | [Member 2] | Partitions, boundaries, decision tables, state model, automation mapping |
| Test Executor | [Member 3] | Execution log, defect reports, retest, unittest run |

One student may fill more than one role. Replace the placeholders with the real team.

## 10. Schedule

| Week | Dates | Work | Output |
| --- | --- | --- | --- |
| 1 | 3–7 Nov 2026 | Understand VTFMS and freeze this baseline | Test plan |
| 2 | 10–14 Nov 2026 | Design 77 cases and the unittest suite | `02_Test_Case_Design/`, automation draft |
| 3 | 17–19 Nov 2026 | Cycle 1 execution, defect logging, fixes on 19 Nov | Execution log, DEF-01 to DEF-05, Build B2 |
| 4 | 20–21 Nov 2026 | Retest the 8 failed cases; write the summary | Final Pass, summary report |
| Confirmation | 24 Nov 2026 | Rerun the automated suite on the submitted snapshot | `test_run_output.txt` |

## 11. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Fine rules interact (repeat, surcharge, suspension, clearance) and an example looks inconsistent | Worked examples in section 3.1 are calculated in the cases. Same-day challans do not count as priors. |
| Off-by-one on inclusive bands or day counts | Boundaries are separate cases: 10/11, 20/21, 40/41, day 7/8, day 15/16, day 180/181, 5000/5001. |
| A percentage is rounded the wrong way at .5 | TC-BVA-24 expects 25% of 750 to become 188. The implementation uses integer half-up, not binary floating point. |
| Manual expected results drift from the code | Traceability and the unittest names (`test_TC_EP_01_` and so on) point at the same rule. |
| The case study is mistaken for a live police deployment | Scope section 2.2 and the conclusion state the limitation. |

## 12. Deliverables

| Folder | Deliverable |
| --- | --- |
| `01_Test_Plan/` | This test plan |
| `02_Test_Case_Design/` | Four technique files and `Test_Case_Index.md` |
| `03_Test_Execution/` | Execution log and execution summary |
| `04_Defect_Reports/` | Defect log and DEF-01 to DEF-05 |
| `05_Test_Automation/` | Module, 92 unittest methods, mapping, real console output |
| `06_Test_Reports/` | Summary report and traceability matrix |
| `07_Screenshots/` | Demo notes, Mermaid diagrams, console copy |

## 13. Suspension and resumption

Suspend testing if the baseline changes, if Python cannot import the module, or if a defect blocks more than half of the remaining cases. Resume when the baseline is updated in this plan, the module imports, and the blocked cases are retested. No suspension occurred in the 17–21 November 2026 window. The eight cycle-1 failures were localised and retested on 20 November 2026.

## 14. Approvals

| Role | Name | Signature | Date |
| --- | --- | --- | --- |
| Test Lead | [Member 1] | | |
| Test Designer | [Member 2] | | |
| Test Executor | [Member 3] | | |
| Faculty | | | |
