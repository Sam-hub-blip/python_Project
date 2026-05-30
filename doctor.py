from models import Nurse, Doctor, Surgeon


def manage_doctor_space(staff_directory, patient_registry):
    profile_choice = input("\n1.Nurse 2.Doctor 3.Surgeon: ").strip()

    if profile_choice == "1":
        id_nurse = input("Enter Nurse ID: ").upper()
        if id_nurse in staff_directory and isinstance(
            staff_directory[id_nurse], Nurse
        ):
            nurse = staff_directory[id_nurse]
            shifts = ", ".join(nurse.shift_days)
            print(f"Hello {nurse.name}. Your shifts: {shifts}")
        else:
            print("[ERROR] Nurse not found.")

    elif profile_choice == "2":
        id_doc = input("\nEnter Doctor ID: ").upper()
        is_valid_doc = (
            id_doc in staff_directory
            and isinstance(staff_directory[id_doc], Doctor)
            and not isinstance(staff_directory[id_doc], Surgeon)
        )
        if is_valid_doc:
            doc = staff_directory[id_doc]
            doc_patients = [
                pid
                for pid, p in patient_registry.items()
                if p["doctor_id"] == id_doc
                and p["status"] == "Awaiting Diagnosis"
            ]
            if not doc_patients:
                print("No patients currently waiting for you.")
                return
            print(f"\nDr. {doc.name}, your assigned patients:")
            for pid in doc_patients:
                sympt = patient_registry[pid]["symptoms"][0]
                print(f"- [{pid}] {patient_registry[pid]['name']} ({sympt})")

            target_id = input("\nEnter Patient ID to check: ").upper()
            if target_id in doc_patients:
                specific_diagnosis = input("Diagnosis statement: ").lower()
                patient_registry[target_id]["symptoms"].append(
                    specific_diagnosis.capitalize()
                )

                print("\n--- DOCTOR'S DECISION ---")
                print("1. Treat & Discharge (Prescription & Invoice ready)")
                print("2. Escalate to Surgeon (Severe Case / Emergency)")
                decision = input("Your choice (1-2): ").strip()

                if decision == "1":
                    try:
                        presc_text = input("Enter prescription: ").strip()
                        patient_registry[target_id]["status"] = (
                            "Treated - Ready for Billing"
                        )
                        patient_registry[target_id]["prescription"] = presc_text
                        doc.consultations_done += 1
                        print("[SUCCESS] Patient file updated.")
                    except Exception:
                        print("[ERROR] Input processing failed.")
                elif decision == "2":
                    patient_registry[target_id]["status"] = (
                        "Severe Case - Waiting for Surgery"
                    )
                    patient_registry[target_id]["doctor_id"] = None
                    print("[INFO] Patient successfully referred to Surgeon.")
                else:
                    print("Invalid option selected.")
            else:
                print("Incorrect Patient ID.")
        else:
            print("[ERROR] Invalid Doctor ID.")