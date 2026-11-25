# Defect Log

Three defects were found on Build B1 during 17–18 November 2026. All three were fixed on 19 November 2026 in Build B2. The code in `05_Test_Automation/traffic_system/` is Build B2. The named regression tests fail if a fix is undone.

| ID | Title | Module | Severity | Found in | Status | Retest |
| --- | --- | --- | --- | --- | --- | --- |
| DEF-01 | Speed 60 was fined | Fine | Major | TC-BVA-01 | Closed | 20 Nov 2026 Pass |
| DEF-02 | No-helmet challan accepted for a Car | Challan | Major | TC-EP-04; also TC-DT-03 | Closed | 20 Nov 2026 Pass |
| DEF-03 | Payment after the due date did not add ₹200 | Payment | Major | TC-BVA-06; also TC-BVA-07, TC-DT-06, TC-ST-03 | Closed | 20 Nov 2026 Pass |

| Status | Count |
| --- | ---: |
| Closed | 3 |
| Open | 0 |

Reports: `DEF-01.md`, `DEF-02.md`, `DEF-03.md`.
