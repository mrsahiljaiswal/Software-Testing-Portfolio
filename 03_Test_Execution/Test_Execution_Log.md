# Test Execution Log — VTFMS

Manual cases were executed against the requirements baseline and the local Python module. Every case below is also covered by a method in `05_Test_Automation/traffic_system/test_traffic.py`. The automated run on 24 November 2026 is recorded separately and is not a substitute for this log.

| Item | Detail |
| --- | --- |
| Executor | [Member 3] |
| Cycle 1 | 17–18 November 2026 on Build B1 |
| Fixes | 19 November 2026, Build B2 |
| Retest | 20 November 2026 on Build B2, the eight failed cases only |
| Cases | 77 |
| Cycle 1 result | 69 Pass, 8 Fail |
| Final result | 77 Pass, 0 Fail |

Build B1 is the module before DEF-01 to DEF-05 were fixed. Build B2 is the module in this repository. State-transition cases passed on the first cycle. The failures were rule defects in the speed bands, the clearance comparison, the helmet category check, the dispute window, and the drunk-driving discount.

| ID | Executed | Actual result | Final status | Defect | Retest | Automated |
| --- | --- | --- | --- | --- | --- | --- |
| TC-EP-01 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-02 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-03 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-04 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-05 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-06 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-07 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-08 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-09 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-10 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-11 | 17 Nov 2026 | Cycle 1 on B1 stored a no-helmet challan for a private car. Cycle 2 on B2 rejected it and stored nothing. | Pass | DEF-03 | 20 Nov 2026 Pass | Yes |
| TC-EP-12 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-13 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-14 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-15 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-16 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-17 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-18 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-19 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-EP-20 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-01 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-02 | 18 Nov 2026 | Cycle 1 on B1 fined city speed 61 at 500. Cycle 2 on B2 fined it 1500 with suspension_recommended false. | Pass | DEF-01 | 20 Nov 2026 Pass | Yes |
| TC-BVA-03 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-04 | 18 Nov 2026 | Cycle 1 on B1 fined highway speed 101 at 1500. Cycle 2 on B2 fined it 3000 with suspension_recommended false. | Pass | DEF-01 | 20 Nov 2026 Pass | Yes |
| TC-BVA-05 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-06 | 18 Nov 2026 | Cycle 1 on B1 fined expressway speed 141 at 3000 and did not recommend suspension. Cycle 2 on B2 fined it 5000 and set suspension_recommended true. | Pass | DEF-01 | 20 Nov 2026 Pass | Yes |
| TC-BVA-07 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-08 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-09 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-10 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-11 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-12 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-13 | 18 Nov 2026 | Cycle 1 on B1 moved the challan to Disputed on 17 Jun 2026. Cycle 2 on B2 rejected the dispute and left the status Issued. | Pass | DEF-04 | 20 Nov 2026 Pass | Yes |
| TC-BVA-14 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-15 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-16 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-17 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-18 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-19 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-20 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-21 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-22 | 18 Nov 2026 | Cycle 1 on B1 set clearance_blocked true at unpaid total 5000 and rejected MH01AA0002. Cycle 2 on B2 left the flag false and stored the vehicle. | Pass | DEF-02 | 20 Nov 2026 Pass | Yes |
| TC-BVA-23 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-BVA-24 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-01 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-02 | 17 Nov 2026 | Cycle 1 on B1 stored a no-helmet challan for a commercial vehicle. Cycle 2 on B2 rejected it and stored nothing. | Pass | DEF-03 | 20 Nov 2026 Pass | Yes |
| TC-DT-03 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-04 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-05 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-06 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-07 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-08 | 17 Nov 2026 | Cycle 1 on B1 accepted 9000 for drunk driving on day 1. Cycle 2 on B2 rejected 9000, kept the status Issued, and accepted 10000. | Pass | DEF-05 | 20 Nov 2026 Pass | Yes |
| TC-DT-09 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-10 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-11 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-12 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-13 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-14 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-15 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-DT-16 | 17 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-01 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-02 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-03 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-04 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-05 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-06 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-07 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-08 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-09 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-10 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-11 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-12 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-13 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-14 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-15 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-16 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |
| TC-ST-17 | 18 Nov 2026 | Matched the expected result on Build B1. | Pass | — | Not required | Yes |

## Cycle 1 failures

| ID | Defect | What B1 did | What B2 does |
| --- | --- | --- | --- |
| TC-BVA-02 | DEF-01 | Fine 500 for 11 km/h over the city limit | Fine 1500 |
| TC-BVA-04 | DEF-01 | Fine 1500 for 21 km/h over the highway limit | Fine 3000 |
| TC-BVA-06 | DEF-01 | Fine 3000 and no suspension for 41 km/h over | Fine 5000 and suspension_recommended true |
| TC-BVA-22 | DEF-02 | Blocked a new vehicle when the unpaid total was 5000 | Allowed the vehicle and left clearance_blocked false |
| TC-EP-11 | DEF-03 | Accepted no helmet on a private car | Rejected the challan |
| TC-DT-02 | DEF-03 | Accepted no helmet on a commercial vehicle | Rejected the challan |
| TC-BVA-13 | DEF-04 | Accepted a dispute on day 16 | Rejected it; status stayed Issued |
| TC-DT-08 | DEF-05 | Accepted 9000 for drunk driving inside 7 days | Rejected 9000 and accepted 10000 |

No case was left Fail or Open. The eight retests on 20 November 2026 all passed, so the final column is Pass for every ID.
