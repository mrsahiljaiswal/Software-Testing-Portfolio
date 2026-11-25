# Equivalence Partitioning — VTFMS

## Technique

Equivalence partitioning divides inputs into classes that the requirements treat the same way. One representative from a class is enough for that class. Values that sit on a numeric edge are left to boundary value analysis.

The baseline is `01_Test_Plan/Test_Plan.md`. Expected results below use that baseline and match Build B2.

## Partitions

| Condition | Valid class | Invalid or other class | Cases |
| --- | --- | --- | --- |
| Registration number | Non-empty, stored uppercase | Empty; duplicate ignoring case | TC-EP-01, TC-EP-02, TC-EP-03 |
| Owner | Owner exists | Owner id not registered | TC-EP-04 |
| Licence | Active, expiry on or after the offence date, matching class | Expiry before the offence date; status Suspended; wrong class | TC-EP-05 to TC-EP-08 |
| No helmet | Two-wheeler | Private car | TC-EP-10, TC-EP-11 |
| No seatbelt | Private car, Commercial, Heavy | Two-wheeler | TC-EP-12 |
| Recorded speed | Above the zone limit | Clearly below the zone limit | TC-EP-13 |
| Fine class | First private signal jump; drunk driving; first commercial signal; repeat commercial signal; third offence of a new type | — | TC-EP-09, TC-EP-14, TC-EP-15, TC-EP-16, TC-EP-20 |
| Reports | Pending includes Issued and omits Paid; overdue lists Overdue only; repeat report lists a same-type pair only | Paid, not-yet-overdue, dismissed-only, different-type pair | TC-EP-17, TC-EP-18, TC-EP-19 |

An invalid licence is not an invalid challan. The offence is still recorded and `licence_invalid` is true. No extra fine is added.

## Test cases

| ID | Requirement | Preconditions | Input | Steps | Expected result | Technique | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-EP-01 | REQ-REG-01, REQ-REG-02 | No owner OWN1 yet | Owner id OWN1, name Owner A; registration `  mh02cd4567  `; category Private car; date 1 Jan 2026 | 1. Register the owner. 2. Register the vehicle. | Owner OWN1 exists. Vehicle is stored as MH02CD4567, owner OWN1, category Private car. | EP | Medium |
| TC-EP-02 | REQ-REG-02 | Owner OWN1 exists | Registration number of spaces only; Private car; 1 Jan 2026 | 1. Register the vehicle. | Registration is rejected. No vehicle is stored. | EP | Medium |
| TC-EP-03 | REQ-REG-02 | MH01AB1001 is already registered to OWN1 | Registration `mh01ab1001`, category Two-wheeler, 2 Jan 2026 | 1. Register the second vehicle. | Registration is rejected as a duplicate. The original vehicle remains the only one. | EP | High |
| TC-EP-04 | REQ-REG-03 | Owner NOBODY does not exist | Registration MH01AB1001, owner NOBODY, Private car, 1 Jan 2026 | 1. Register the vehicle. | Registration is rejected. No vehicle is stored. | EP | High |
| TC-EP-05 | REQ-LIC-01 | OWN1, private car MH01AB1001, Active LMV licence expiring on 1 Jun 2026 | Signal jump on 1 Jun 2026 | 1. Issue the challan. | Status Issued. Calculated fine 1000. `licence_invalid` is false. | EP | High |
| TC-EP-06 | REQ-LIC-02 | Same vehicle. Active LMV licence expires on 31 May 2026 | Signal jump on 1 Jun 2026 | 1. Issue the challan. | Status Issued. Calculated fine stays 1000. `licence_invalid` is true. No documents fine is added. | EP | High |
| TC-EP-07 | REQ-LIC-03, REQ-PAY-01 | Same vehicle. LMV licence status Suspended, expiry 1 Jan 2028 | Signal jump on 1 Jun 2026. Pay on 4 Jun 2026 with 900 | 1. Issue the challan. 2. Pay 900. | Fine is 1000 and `licence_invalid` is true. `suspension_recommended` is false, so the early discount applies and 900 is accepted. Status becomes Paid. Licence status remains Suspended. | EP | High |
| TC-EP-08 | REQ-LIC-02 | Private car with an Active HGV licence expiring 1 Jan 2028 | Mobile use on 1 Jun 2026 | 1. Issue the challan. | Status Issued. Fine 1500. `licence_invalid` is true because the class does not match LMV. | EP | High |
| TC-EP-09 | REQ-FINE-01, REQ-CH-04 | Private car, valid LMV licence, no earlier challan | Signal jump on 1 Jun 2026 | 1. Issue the challan. | Base fine 1000, calculated fine 1000, repeat not applied, `suspension_recommended` false. Due date 1 Jul 2026. | EP | High |
| TC-EP-10 | REQ-CH-01, REQ-FINE-01 | Two-wheeler MH01TW1001, valid TW licence | No helmet on 1 Jun 2026 | 1. Issue the challan. | Status Issued. Calculated fine 500. | EP | High |
| TC-EP-11 | REQ-CH-01 | Private car, valid LMV licence | No helmet on 1 Jun 2026 | 1. Issue the challan. | Challan is rejected. Nothing is stored. This case failed on Build B1 (DEF-03) and passes on Build B2. | EP | High |
| TC-EP-12 | REQ-CH-01 | Two-wheeler, valid TW licence | No seatbelt on 1 Jun 2026 | 1. Issue the challan. | Challan is rejected. Nothing is stored. | EP | High |
| TC-EP-13 | REQ-CH-02 | Private car, valid licence | City zone, recorded speed 40 on 1 Jun 2026 | 1. Issue an overspeeding challan. | Rejected. Speed 40 is below the city limit of 50, so it is not an offence. Nothing is stored. | EP | High |
| TC-EP-14 | REQ-FINE-01, REQ-FINE-05 | Private car, valid Active LMV licence | Drunk driving on 1 Jun 2026 | 1. Issue the challan. | Calculated fine 10000. `suspension_recommended` is true. `licence_invalid` is false. The licence stays Active; the flag does not suspend it. | EP | High |
| TC-EP-15 | REQ-FINE-04 | Commercial vehicle MH01CO1001, valid COM licence, no earlier signal jump | Signal jump on 1 Jun 2026 | 1. Issue the challan. | Base 1000, repeat not applied, 50% surcharge, calculated fine 1500. | EP | High |
| TC-EP-16 | REQ-FINE-03, REQ-FINE-04 | Same commercial vehicle. A signal jump was issued on 1 Jun 2026 (fine 1500) | Signal jump on 1 Jul 2026 | 1. Issue the second challan. | Repeat applies. Base 1000 × 2 = 2000, plus 50% = 3000. `suspension_recommended` is false because there is only one prior challan. | EP | High |
| TC-EP-17 | REQ-REP-01 | Private car, valid licence | Signal jump on 1 Jun 2026. Wrong parking on 2 Jun 2026, paid the same day with 450 | 1. Issue both challans. 2. Pay the parking challan 450. 3. Open the pending report for 2 Jun 2026. | Wrong parking is 500, and the offence date is inside the 7-day window, so payable is 450. Pending report contains only the signal-jump challan. The paid challan is omitted. | EP | Medium |
| TC-EP-18 | REQ-REP-01, REQ-ST-01 | Private car, valid licence | Signal jump on 1 Apr 2026 (due 1 May 2026). Mobile use on 1 Jun 2026. Overdue scan on 2 May 2026 | 1. Issue both. 2. Run the overdue scan for 2 May 2026. 3. Open the overdue report. | The April challan is Overdue. The June challan stays Issued. The overdue report lists only the April challan. | EP | Medium |
| TC-EP-19 | REQ-REP-01, REQ-FINE-03 | Three owners, each with a private car and a valid licence | Owner A: signal jumps on 1 Jun and 11 Jun 2026. Owner B: signal jump on 1 Jun, disputed and dismissed, then another signal jump on 11 Jun. Owner C: signal jump on 1 Jun and mobile use on 11 Jun | 1. Record the challans and the dismissal. 2. Open the repeat-offender report. | Only Owner A is listed. Owner B has only one non-dismissed signal jump. Owner C’s two challans have different types. | EP | Medium |
| TC-EP-20 | REQ-FINE-05, REQ-FINE-03 | Private car, valid licence, no earlier challans | Signal jump on 1 Jun 2026; mobile use on 11 Jun 2026; wrong parking on 21 Jun 2026 | 1. Issue the three challans in date order. | First fine 1000, suspension false. Second fine 1500, suspension false (only one prior). Third fine 500, repeat not applied because the type is new, `suspension_recommended` true because two priors exist inside 180 days. | EP | High |
