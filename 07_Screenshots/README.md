# Screenshots and visual evidence

This folder holds the diagrams and the saved test console. No PNG screenshots were created for this portfolio. Do not add a picture that was not taken on the demonstration machine.

## Files here

| File | What it is |
| --- | --- |
| `test_execution_console.txt` | The real unittest console. It ends with `Ran 30 tests` and `OK`. |
| `Diagrams.md` | Three Mermaid diagrams: modules, challan states, and fine rules |

The same console text is stored at `05_Test_Automation/test_run_output.txt`. If the suite is run again, save the new output over both files so they stay identical.

## Command

```powershell
Set-Location C:\Users\sahil\OneDrive\Desktop\software-testing
python -m unittest "05_Test_Automation\traffic_system\test_traffic.py" -v
```

Python 3.12.6. Result in the saved file: 30 tests, 0 failures.

## Optional shots during the demo

Take these on the demonstration machine only if the faculty asks for images:

1. The portfolio folder, showing `README.md` and the numbered folders.
2. The PowerShell window after the command above, showing `Ran 30 tests` and `OK`.
3. `04_Defect_Reports/Defect_Log.md`, with DEF-01, DEF-02, and DEF-03 Closed.
4. The state diagram in `Diagrams.md`.
