# Diagrams

Three diagrams for the viva. They describe the module in this repository.

## 1. Modules

The officer registers a vehicle, records a challan, and the owner pays one fine.

```mermaid
flowchart LR
    Registration --> Challan
    Challan --> Fine
    Fine --> Payment
```

## 2. Challan states

Issued can become Paid or Overdue. Overdue can become Paid. Paid stops.

```mermaid
stateDiagram-v2
    [*] --> Issued
    Issued --> Paid: exact amount
    Issued --> Overdue: after the due date
    Overdue --> Paid: fine plus 200
```

## 3. Fine rules

Signal jump is ₹500. No helmet is ₹1000 on a Two-wheeler and is rejected on a Car. Overspeeding uses 60 and 80.

```mermaid
flowchart TD
    start{Violation}
    start -->|Signal jump| fine500[Fine 500]
    start -->|No helmet, Two-wheeler| fine1000[Fine 1000]
    start -->|No helmet, Car| reject[Reject]
    start -->|Overspeeding| speed{Speed}
    speed -->|60 or below| reject
    speed -->|61 to 80| fine500b[Fine 500]
    speed -->|81 or above| fine2000[Fine 2000]
```
