from typing import List, Dict, Any
from config import HOSPITAL_NAME, MAX_QUEUE_SIZE
from models import Nurse, Doctor, Surgeon, Patient
from utils import log_activity, generate_discharge_docs
from admin import manage_admin_space
from doctor import manage_doctor_space
from surgeon import manage_surgeon_space

if __name__ == "__main__":
    staff_directory: Dict[str, Any] = {}
    patient_registry: Dict[str, Dict[str, Any]] = {}
    available_rooms: List[int] = [101, 102, 103, 201, 202, 203]
    waiting_queue: List[Patient] = []

    hospital_balance: float = 0.0
    patient_counter: int = 0
    system_running: bool = True

    # Pre-populating system with startup data
    staff_directory["INF-01"] = Nurse(
        "INF-01", "Traore Lamine", 180000.0, ["Monday", "Tuesday"]
    )
    staff_directory["MED-01"] = Doctor(
        "MED-01", "Sanon Alizeta", 350000.0, ["Wednesday", "Thursday"], 10000.0
    )
    staff_directory["DOC-01"] = Surgeon(
        "DOC-01",
        "Ouedraogo Issa",
        550000.0,
        ["Friday", "Saturday"],
        15000.0,
        75000.0,
    )

    while system_running:
        print(f"\n{'='*50}")
        print(f"        INTERNAL MANAGEMENT SYSTEM: {HOSPITAL_NAME}")
        print(f"{'='*50}")
        print("1. [WING 1] - Administrator Panel")
        print("2. [WING 2] - Medical Staff Wing")
        print("3. [WING 3] - Reception & Nurse Discharge")
        print("4. Shut down system")

        selected_wing = input("Select navigation wing (1-4): ").strip()

        if selected_wing == "1":
            manage_admin_space(staff_directory, hospital_balance)

        elif selected_wing == "2":
            print("\nAccessing medical wing...")
            profile_type = input("1.Nurse/GP Doctor | 2.Surgeon (OR): ").strip()
            if profile_type == "1":
                manage_doctor_space(staff_directory, patient_registry)
            elif profile_type == "2":
                manage_surgeon_space(staff_directory, patient_registry)

        elif selected_wing == "3":
            choice_nurse = input("\n1.Admit Patient 2.Bill & Discharge: ").strip()
            if choice_nurse == "1":
                if len(waiting_queue) >= MAX_QUEUE_SIZE:
                    print("[ALERT] Queue full. Registration blocked.")
                    continue
                if not available_rooms:
                    print("[ALERT] No rooms left.")
                    continue

                doctors_list = [
                    k
                    for k, v in staff_directory.items()
                    if isinstance(v, Doctor) and not isinstance(v, Surgeon)
                ]
                print("\nAvailable GP Doctors: ", ", ".join(doctors_list))
                assigned_doc = input("Enter Doctor ID: ").upper()
                if assigned_doc not in doctors_list:
                    print("[ERROR] Invalid Doctor ID.")
                    continue

                active_patients = [
                    p
                    for p in patient_registry.values()
                    if p["doctor_id"] == assigned_doc
                    and "Ready for Billing" not in p["status"]
                ]
                if len(active_patients) >= 3:
                    print("[ALERT] This doctor has reached their 3-patient max.")
                    continue

                try:
                    patient_counter += 1
                    pat_id = f"PAT-{patient_counter:03d}"
                    pat_name = input("First & Last Name: ").strip()
                    pat_age = int(input("Age: "))
                    pat_temp = float(input("Temperature: "))
                    symptom = input("Primary Symptom: ").strip()
                except ValueError:
                    print("[ERROR] Invalid inputs. Admission aborted.")
                    continue

                allocated_room = available_rooms.pop(0)
                patient_registry[pat_id] = {
                    "name": pat_name,
                    "age": pat_age,
                    "room": allocated_room,
                    "status": "Awaiting Diagnosis",
                    "symptoms": [symptom],
                    "doctor_id": assigned_doc,
                    "practitioner": staff_directory[assigned_doc].name,
                    "prescription": "None.",
                }
                waiting_queue.append(
                    Patient(pat_id, pat_name, pat_age, pat_temp)
                )
                log_msg = f"ADMISSION: {pat_name} ({pat_id}) Room {allocated_room}"
                log_activity(log_msg)
                print(f"[SUCCESS] {pat_name} admitted to Room {allocated_room}.")

            elif choice_nurse == "2":
                billable_patients = [
                    pid
                    for pid, p in patient_registry.items()
                    if "Ready for Billing" in p["status"]
                ]
                if not billable_patients:
                    print("No patients ready for discharge.")
                    continue
                for pid in billable_patients:
                    print(f"- [{pid}] {patient_registry[pid]['name']}")
                id_to_discharge = input("\nEnter ID to bill: ").upper()
                if id_to_discharge in billable_patients:
                    pat_data = patient_registry[id_to_discharge]
                    practitioner = staff_directory[pat_data["doctor_id"]]
                    total = 30000.0 + practitioner.consultation_fee
                    if isinstance(practitioner, Surgeon):
                        total += practitioner.operation_fee

                    try:
                        if generate_discharge_docs(id_to_discharge, pat_data, total):
                            hospital_balance += total
                            available_rooms.append(pat_data["room"])
                            log_sort = (
                                f"DISCHARGE: {pat_data['name']} ({id_to_discharge}) "
                                f"Billed {total} FCFA"
                            )
                            log_activity(log_sort)
                            del patient_registry[id_to_discharge]
                            print("[SUCCESS] Patient successfully discharged.")
                    except Exception as e:
                        print(f"[ERROR] {e}")
                else:
                    print("Invalid Patient ID.")

        elif selected_wing == "4":
            print("\nShutting down hospital systems...")
            system_running = False
        else:
            print("[ERROR] Invalid selection.")

    print("Sahel Care System is offline. Execution terminated.")