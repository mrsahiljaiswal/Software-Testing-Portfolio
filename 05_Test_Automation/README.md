# Test Automation — VTFMS

This folder is the additional activity for the portfolio. The syllabus activity is often demonstrated with JUnit. This workstation has Python 3.12.6 and OpenJDK 17.0.18, but it does not have Maven and the assignment does not allow downloaded dependencies. The same activity is therefore implemented with `unittest` from the Python standard library. No `pip install` is required.

## What the suite is

The technique is automated unit testing. The tests call the VTFMS module directly. They encode equivalence classes, boundary values, decision-table rules, and valid and invalid state transitions. They also lock the five defects fixed in Build B2:

| Defect | Rule the test now protects |
| --- | --- |
| DEF-01 | Overspeed 11, 21, and 41 use the higher band, and 41 recommends suspension |
| DEF-02 | Unpaid total 5000 does not block; 5001 does |
| DEF-03 | No helmet is rejected unless the vehicle is a two-wheeler |
| DEF-04 | A dispute on day 16 is rejected |
| DEF-05 | Drunk driving does not receive the 10% early discount |

There are 92 tests: 77 correspond to the manual cases and 15 are extra regression checks. The mapping is `Automation_Mapping.md`. The last run, on 24 November 2026, was 92 passed and 0 failed.

## Layout

| File | Purpose |
| --- | --- |
| `traffic_system/models.py` | Owners, vehicles, licences, challans, and the allowed transitions |
| `traffic_system/fine.py` | Base fines, speed bands, surcharge, half-up rounding, and payable amount |
| `traffic_system/system.py` | Registration, issue, payment, dispute, clearance, and reports |
| `traffic_system/test_traffic.py` | The unittest module |
| `Automation_Mapping.md` | Method name to manual test-case ID |
| `test_run_output.txt` | The real console output from the run below |

## How to run

Open PowerShell in the portfolio folder (the folder that contains this `05_Test_Automation` directory):

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

A passing run ends with a line of the form `Ran 92 tests in …` followed by `OK`. The saved output in `test_run_output.txt` is that run, copied also to `07_Screenshots/test_execution_console.txt`.

The tests do not need a database, a network connection, or a payment gateway. They use fixed calendar dates so the results do not depend on the day the suite is started.
