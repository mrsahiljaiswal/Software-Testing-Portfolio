# Test Execution Log

Executor: [Member 3]. Cycle 1 used Build B1 on 17 and 18 November 2026. The seven failures were retested on Build B2 on 20 November 2026. The final column is the result after that retest. Every final result is Pass.

| ID | First run | Build | First result | Retest on 20 Nov 2026 | Final | Note |
| --- | --- | --- | --- | --- | --- | --- |
| TC-EP-01 | 17 Nov 2026 | B1 | Pass | — | Pass | Two-wheeler, signal jump, ₹500, due 16 June |
| TC-EP-02 | 17 Nov 2026 | B1 | Pass | — | Pass | Car, signal jump, ₹500 |
| TC-EP-03 | 17 Nov 2026 | B1 | Pass | — | Pass | Two-wheeler, no helmet, ₹1000 |
| TC-EP-04 | 17 Nov 2026 | B1 | Fail | Pass | Pass | DEF-02. Car, no helmet, was stored |
| TC-EP-05 | 17 Nov 2026 | B1 | Pass | — | Pass | Speed 40 rejected |
| TC-EP-06 | 17 Nov 2026 | B1 | Pass | — | Pass | Speed 70, fine ₹500 |
| TC-EP-07 | 17 Nov 2026 | B1 | Pass | — | Pass | Speed 100, fine ₹2000 |
| TC-EP-08 | 17 Nov 2026 | B1 | Pass | — | Pass | Car, speed 50, rejected |
| TC-BVA-01 | 17 Nov 2026 | B1 | Fail | Pass | Pass | DEF-01. Speed 60 was fined ₹500 |
| TC-BVA-02 | 17 Nov 2026 | B1 | Pass | — | Pass | Speed 61, fine ₹500 |
| TC-BVA-03 | 17 Nov 2026 | B1 | Pass | — | Pass | Speed 80, fine ₹500 |
| TC-BVA-04 | 17 Nov 2026 | B1 | Pass | — | Pass | Speed 81, fine ₹2000 |
| TC-BVA-05 | 18 Nov 2026 | B1 | Pass | — | Pass | Pay ₹500 on the due date |
| TC-BVA-06 | 18 Nov 2026 | B1 | Fail | Pass | Pass | DEF-03. 17 June still asked for ₹500 |
| TC-BVA-07 | 18 Nov 2026 | B1 | Fail | Pass | Pass | DEF-03. Helmet late amount stayed ₹1000. Expected ₹1200. |
| TC-BVA-08 | 18 Nov 2026 | B1 | Pass | — | Pass | ₹2199 rejected, status stayed Issued |
| TC-DT-01 | 18 Nov 2026 | B1 | Pass | — | Pass | Rule A1, signal jump accepted |
| TC-DT-02 | 18 Nov 2026 | B1 | Pass | — | Pass | Rule A2, helmet on a Two-wheeler |
| TC-DT-03 | 18 Nov 2026 | B1 | Fail | Pass | Pass | DEF-02. Rule A3, Car helmet was accepted |
| TC-DT-04 | 18 Nov 2026 | B1 | Pass | — | Pass | Rule A4, speed 50 rejected |
| TC-DT-05 | 18 Nov 2026 | B1 | Pass | — | Pass | Rule B1, ₹500 on 10 June |
| TC-DT-06 | 18 Nov 2026 | B1 | Fail | Pass | Pass | DEF-03. 20 June was not ₹700 |
| TC-ST-01 | 18 Nov 2026 | B1 | Pass | — | Pass | Issued → Paid, on time |
| TC-ST-02 | 18 Nov 2026 | B1 | Pass | — | Pass | Issued → Overdue on 17 June |
| TC-ST-03 | 18 Nov 2026 | B1 | Fail | Pass | Pass | DEF-03. Overdue → Paid did not accept ₹700 |
| TC-ST-04 | 18 Nov 2026 | B1 | Pass | — | Pass | Second payment rejected |
| TC-ST-05 | 18 Nov 2026 | B1 | Pass | — | Pass | Overdue → Issued rejected |
| TC-ST-06 | 18 Nov 2026 | B1 | Pass | — | Pass | Paid → Overdue rejected |

## Row check

| First run | Rows | Pass | Fail |
| --- | ---: | ---: | ---: |
| 17 Nov 2026 | 12 | 10 | 2 |
| 18 Nov 2026 | 16 | 11 | 5 |
| Cycle 1 total | 28 | 21 | 7 |
| Retest, 20 Nov 2026 | 7 | 7 | 0 |
| Final | 28 | 28 | 0 |

The seven cycle-1 failures are TC-EP-04, TC-BVA-01, TC-BVA-06, TC-BVA-07, TC-DT-03, TC-DT-06, and TC-ST-03. They map to DEF-01, DEF-02, and DEF-03.
