# Defect Log — VTFMS

Defects were found while executing Build B1 on 17 and 18 November 2026. All five were fixed on 19 November 2026 in Build B2. The code in `05_Test_Automation/traffic_system/` is Build B2. The automated tests named below fail if a fix is undone.

| ID | Title | Module | Severity | Priority | Detected in | Status | Retest |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEF-01 | Speed band off-by-one: 11 km/h over charged the 1–10 fine | Fine calculation | Major | High | TC-BVA-02; also TC-BVA-04, TC-BVA-06 | Closed | 20 Nov 2026 Pass |
| DEF-02 | Clearance blocked at exactly 5000 | Registration | Major | High | TC-BVA-22 | Closed | 20 Nov 2026 Pass |
| DEF-03 | No-helmet challan accepted for a private car | Challan recording | Major | High | TC-EP-11; also TC-DT-02 | Closed | 20 Nov 2026 Pass |
| DEF-04 | Dispute accepted on day 16 | Dispute | Major | High | TC-BVA-13 | Closed | 20 Nov 2026 Pass |
| DEF-05 | Early-payment discount given for drunk driving | Payment | Major | High | TC-DT-08 | Closed | 20 Nov 2026 Pass |

| Status | Count |
| --- | ---: |
| Closed | 5 |
| Open | 0 |

Individual reports: `DEF-01.md`, `DEF-02.md`, `DEF-03.md`, `DEF-04.md`, `DEF-05.md`.
