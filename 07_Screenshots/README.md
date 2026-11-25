# Screenshots and visual evidence

This folder is where screenshots would be placed during the faculty demonstration. This environment did not capture GUI screenshots, and none have been invented. Terminal evidence is stored as text.

## What to capture in the demo

Take real screenshots on the demonstration machine and drop them in this folder if the faculty asks for images. Suggested shots, in viva order:

1. The repository root on GitHub, after the student has created the remote, showing `README.md` and the numbered folders.
2. The PowerShell window after the unittest command, showing `Ran 92 tests` and `OK`.
3. `04_Defect_Reports/Defect_Log.md` with DEF-01 to DEF-05 all Closed.
4. The challan state diagram in `Diagrams.md`, rendered in a Markdown preview.

Until those shots are taken, use the files already here:

| File | What it is |
| --- | --- |
| `test_execution_console.txt` | Copy of the real unittest output from 24 November 2026 |
| `Diagrams.md` | Mermaid diagrams for the modules, the challan state machine, fine calculation, and the test process |

The same console text is stored at `05_Test_Automation/test_run_output.txt`. Do not replace either file with a typed summary. If the suite is run again, save the new output over both files so they stay identical.

## Command used for the saved run

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

Python 3.12.6. Result: 92 tests, 0 failures.
