# GROUP 18
# GOSEN Hospital Internal Management System

A command-line Python application that simulates the internal operations of a hospital named **GOSEN**. The system allows administrators, nurses, doctors, and surgeons to manage staff, admit and discharge patients, process billing, and log all hospital activity — all from a unified terminal interface.

---

## How to Run the Project

**Requirements:**
- Python 3.10 or higher
- No external libraries required — only the Python standard library is used

**Steps:**

1. Clone or download the repository to your machine.
2. Navigate to the project folder in your terminal.
3. Run the main file:

```bash
python main.py
```

4. Use the numbered menu to navigate between wings. The admin panel requires the access code `1234`.

---

## Features

- **Administrator Panel** — protected by an access code; allows registering and removing staff, viewing the current hospital balance, listing all employees with their calculated pay, and reading the full activity log.
- **Medical Staff Wing** — nurses can check their shift schedule; GP doctors can consult assigned patients, write prescriptions, and either discharge or escalate patients to surgery; surgeons can operate on critical cases and record outcomes.
- **Reception & Nurse Discharge** — nurses can admit new patients (assigning them to a room and a doctor), and process billing and discharge for patients who have been treated.
- **Patient Queue and Room Management** — the system enforces a maximum queue size and tracks available rooms automatically.
- **Automatic File Generation** — on discharge, the system generates a personalised invoice file and a prescription file for each patient.
- **Activity Logging** — every admission and discharge is timestamped and written to `hospital_log.txt`.
- **Polymorphic Pay Calculation** — each staff type (Nurse, Doctor, Surgeon) has its own pay logic, all accessible through the same `calculate_pay()` method.

---

## Technologies Used

- **Python 3.10+**
- `datetime` — for timestamping admissions, discharges, and log entries
- `os` — for checking whether the log file exists before reading
- `typing` — for type annotations (`List`, `Dict`, `Tuple`, `Any`)

No third-party packages are required.

---

## Project Structure

```
├── main.py        # Entry point; contains the main loop, all navigation logic, and core data structures
├── models.py      # All class definitions: HospitalStaff, Nurse, Doctor, Surgeon, Patient
├── config.py      # System-wide constants: hospital name, severe case keywords, max queue size
├── utils.py       # Utility functions: activity logging, log reading, discharge document generation
├── admin.py       # Administrator panel logic (staff management, balance, logs)
├── doctor.py      # Doctor and nurse workspace logic (diagnosis, prescription, referral)
└── surgeon.py     # Surgeon workspace logic (operating room, case outcomes)
```

**Generated at runtime (not included in the repo):**
- `hospital_log.txt` — cumulative log of all admissions and discharges
- `invoice_<PatientName>.txt` — billing invoice generated on patient discharge
- `prescription_<PatientName>.txt` — medical prescription generated on patient discharge

---

## OOP Structure

| Class | Inherits From | Description | Key Methods |
|---|---|---|---|
| `HospitalStaff` | — | Base class for all hospital employees. Holds common attributes: `staff_id`, `name`, `base_salary`. | `calculate_pay()` |
| `Nurse` | `HospitalStaff` | Represents a nurse. Adds `shift_days` and a flat shift allowance to the base salary. | `calculate_pay()` |
| `Doctor` | `HospitalStaff` | Represents a GP doctor. Adds `consultation_fee` and a per-consultation bonus to pay. | `calculate_pay()` |
| `Surgeon` | `Doctor` | Represents a surgeon. Extends Doctor with an `operation_fee` and a per-operation bonus on top of the doctor's pay. | `calculate_pay()` |
| `Patient` | — | Tracks all data related to a patient: ID, name, age, temperature, symptoms, status, prescription, and admission date. | *(data class — attributes only)* |

**OOP Principles demonstrated:**

- **Encapsulation** — each class manages its own attributes privately; pay logic is contained within each class's own `calculate_pay()` method.
- **Abstraction** — the rest of the program calls `calculate_pay()` without needing to know how each staff type computes its salary.
- **Inheritance** — `Nurse` and `Doctor` inherit from `HospitalStaff`; `Surgeon` inherits from `Doctor`, forming a two-level hierarchy.
- **Polymorphism** — `calculate_pay()` is defined differently in each class; the admin panel calls the same method on any staff object and receives the correct result for that type.

---

## Acknowledgements

- Python official documentation: [https://docs.python.org](https://docs.python.org)
- PEP 8 Style Guide: [https://pep8.org](https://pep8.org)
- Course materials and examples provided by Lecturer Kweyakie Afi Blebo — Burkina Institute of Technology

---
## Group Members

## Group Members & Work Distribution

| Full Name | File Managed | Primary Contribution & Module Logic | GitHub Profile |
| :--- | :--- | :--- | :--- |
| **Zongo Tinwindé Samuel** | `main.py`, `config.py` | Core Orchestrator, System Loop, and Global Application Constants | [GitHub Profile](https://github.com/Sam-hub-blip) |
| **Zongo Osias** | `models.py` | OOP Architecture, Base Entity Templates, and Inheritance Hierarchies | [GitHub Profile](https://github.com/ozias6378-coder) |
| **Zongo Aurelie** | `utils.py` | File I/O Persistence, System Event Logging, and Document Generation | [GitHub Profile](https://github.com/zongoaurelie) |
| **Zongo Aude Ariane** | `admin.py` | Administrative Space Control, Security Access Gate, and HR/Accounting | [GitHub Profile](https://github.com/aude-code) |
| **Zongo Floriane** | `doctor.py` | General Clinical Medicine Wing, Patient Checkups, and Triage Logic | [GitHub Profile](https://github.com/zongofloriane706-max) |
| **Zongo Ibrahim** | `surgeon.py` | Emergency Surgical Block, Operating Room Workflow, and Post-Op Tracking | [GitHub Profile](https://github.com/ibrahim-c7) |
*This project was built as part of the Programming I with Python group assignment — BIT, May 2026.*
