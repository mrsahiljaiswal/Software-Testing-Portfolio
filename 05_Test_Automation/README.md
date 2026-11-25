# Test Automation

This folder is the automated check for the challan rules. The tests call the Python module directly. They use `unittest` from the standard library. No `pip install` is required.

## What the 30 tests cover

| Group | Tests |
| --- | ---: |
| Equivalence cases TC-EP-01 to TC-EP-08 | 8 |
| Boundary cases TC-BVA-01 to TC-BVA-08 | 8 |
| Decision-table cases TC-DT-01 to TC-DT-06 | 6 |
| State cases TC-ST-01 to TC-ST-06 | 6 |
| Registration (required, uppercase, unique) | 2 |
| **Total** | **30** |

Three of the case tests are also the defect regressions:

| Defect | Test |
| --- | --- |
| DEF-01 | `test_TC_BVA_01_DEF_01_speed_60_rejected` |
| DEF-02 | `test_TC_EP_04_DEF_02_car_no_helmet_rejected` |
| DEF-03 | `test_TC_BVA_06_DEF_03_day_after_due_adds_200` |

The saved run is 30 passed and 0 failed. The text is `test_run_output.txt`. The same text is in `07_Screenshots/test_execution_console.txt`.

## Layout

| File | Purpose |
| --- | --- |
| `traffic_system/models.py` | Vehicle, challan, and the three states |
| `traffic_system/fine.py` | The fine and the amount due |
| `traffic_system/system.py` | Register, issue, mark overdue, and pay |
| `traffic_system/test_traffic.py` | The 30 unittest methods |
| `Automation_Mapping.md` | Method name to manual case |
| `test_run_output.txt` | The real console output |

## How to run

Open PowerShell in the portfolio folder:

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

A passing run ends with `Ran 30 tests in …` and `OK`. Python 3.12.6 was used for the saved file.
