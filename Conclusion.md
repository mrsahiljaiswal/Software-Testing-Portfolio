# Conclusion

This portfolio tests a small traffic-challan system. An officer records a challan, the system calculates one fine, and the owner pays it. The inputs are the vehicle type, the violation, the speed when the violation is overspeeding, and the payment date.

The rules are short enough to say in a viva. Signal jump is ₹500. No helmet is ₹1000 for a Two-wheeler and is rejected for a Car. Overspeeding uses a limit of 60 km/h for every vehicle: 60 or below is rejected, 61 to 80 is ₹500, and 81 or above is ₹2000. The due date is the challan date plus 15 days. Payment on or before that date is the fine. Payment after that date is the fine plus ₹200. A short payment is rejected. A challan moves only from Issued to Paid, from Issued to Overdue, or from Overdue to Paid.

The design has 28 manual cases: 8 equivalence partitions, 8 boundary values, 6 decision-table cases, and 6 state-transition cases. Cycle 1, on 17–18 November 2026, had 21 Pass and 7 Fail. Those seven failures were three defects: speed 60 was fined, a Car was accepted for no helmet, and a late payment did not add ₹200. The fixes were made on 19 November 2026. The retest on 20 November 2026 passed, so the final manual result is 28 Pass and 0 Fail.

The Python `unittest` suite has 30 tests and passes on the code in this repository. Three of those tests are the regression checks for DEF-01, DEF-02, and DEF-03. Two more check the only registration rule: the vehicle number is required, stored in uppercase, and unique. No extra packages are installed.

The test item is this local Python module. It is not a live police system and it does not take a card payment. The manual cases and the unit tests both use the rules in the test plan. All three defects are Closed, and the portfolio is ready to demonstrate.
