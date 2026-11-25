# Diagrams — VTFMS

These diagrams match the requirements baseline and the Python module. They are Mermaid source, not captured screenshots.

## 1. Module diagram

```mermaid
flowchart LR
    subgraph vtfms [Vehicle Traffic Violation and Fine Management System]
        reg[Vehicle and owner registration]
        lic[Driving licence check]
        rec[Violation and challan recording]
        fine[Fine calculation]
        pay[Fine payment]
        dis[Dispute handling]
        rep[Reports]
    end
    reg --> rec
    lic --> rec
    rec --> fine
    fine --> pay
    fine --> dis
    pay --> rep
    dis --> rep
    reg --> rep
```

Registration feeds challan recording. The licence check sets `licence_invalid` and does not block the offence. Fine calculation produces the calculated fine and `suspension_recommended`. Payment and disputes change challan state. Reports read registration clearance and the challan list.

## 2. Challan state machine

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Issued: Submit a valid challan
    Issued --> Paid: Exact payment
    Issued --> Disputed: Offence date through day 15
    Issued --> Overdue: Current date after due date
    Overdue --> Paid: Exact late payment
    Disputed --> Dismissed: Review accepts
    Disputed --> Upheld: Review rejects
    Upheld --> Paid: Exact payment, no early discount
    Paid --> [*]
    Dismissed --> [*]
```

Rejected moves, with no arrow above: anything leaving Paid or Dismissed; Draft to Paid, Disputed, or Overdue; Issued to Dismissed; Overdue to Disputed; Disputed to Paid. Issued to Overdue is also rejected on the due date itself.

## 3. Fine-calculation flow

```mermaid
flowchart TD
    startNode[Violation, vehicle, speed, offence date]
    cat{Category allows this violation?}
    speed{Overspeeding and speed above the zone limit?}
    reject[Reject the challan]
    base[Base fine from type or speed band]
    repeat{Same type in the previous 180 days?}
    doubled[Multiply base by 2]
    surcharge{Commercial or Heavy?}
    addHalf[Add 50 percent, half-up]
    suspend{Overspeed at least 41, drunk driving, or at least two priors?}
    done[Store calculated fine and suspension flag]
    startNode --> cat
    cat -->|No| reject
    cat -->|Yes| speed
    speed -->|No, and it is overspeeding| reject
    speed -->|Yes, or not overspeeding| base
    base --> repeat
    repeat -->|Yes| doubled
    repeat -->|No| surcharge
    doubled --> surcharge
    surcharge -->|Yes| addHalf
    surcharge -->|No| suspend
    addHalf --> suspend
    suspend --> done
```

The speed flag is set inside the base-fine step when overspeed is 41 or more, and drunk driving sets it as well. The final suspension flag is that value or a prior count of at least 2. A duplicate vehicle, type, and date is rejected before this flow stores a row.

## 4. Test process

```mermaid
flowchart LR
    plan[Test plan and baseline<br/>3 to 7 Nov 2026]
    design[77 cases and unittest<br/>10 to 14 Nov 2026]
    run1[Cycle 1 on Build B1<br/>17 to 18 Nov 2026]
    defects[DEF-01 to DEF-05<br/>fixed 19 Nov 2026]
    retest[Retest 8 cases<br/>20 Nov 2026]
    report[Summary report<br/>21 Nov 2026]
    confirm[92 automated tests<br/>24 Nov 2026]
    plan --> design --> run1 --> defects --> retest --> report --> confirm
```

Cycle 1 was 69 Pass and 8 Fail. The retest and the later automated run were both fully passing.
