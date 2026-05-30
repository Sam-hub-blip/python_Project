from models import Surgeon


def manage_surgeon_space(staff_directory, patient_registry):
    id_surg = input("\nEnter Surgeon ID: ").upper()
    if id_surg in staff_directory and isinstance(
        staff_directory[id_surg], Surgeon
    ):
        surg = staff_directory[id_surg]
        critical_patients = [
            pid
            for pid, p in patient_registry.items()
            if p["status"] == "Severe Case - Waiting for Surgery"
        ]
        if not critical_patients:
            print("No critical cases in the ER right now.")
            return
        print("\n=== EMERGENCY OR BLOCK ===")
        for pid in critical_patients:
            last_sympt = patient_registry[pid]["symptoms"][-1]
            print(f"- [{pid}] {patient_registry[pid]['name']} | {last_sympt}")

        target_id = input("\nEnter Patient ID to operate: ").upper()
        if target_id in critical_patients:
            print(f"Operation started for {patient_registry[target_id]['name']}...")
            patient_registry[target_id]["prescription"] = input(
                "Post-op treatment plan: "
            )
            patient_registry[target_id]["doctor_id"] = id_surg
            patient_registry[target_id]["practitioner"] = surg.name
            surg.operations_done += 1
            surg.consultations_done += 1

            print("\nOUTCOME: 1.Success 2.Failure 3.Transfer")
            outcome = input("Select choice: ").strip()
            if outcome == "1":
                patient_registry[target_id]["status"] = (
                    "Operated - Ready for Billing"
                )
                print("Operation successful. Patient stabilized.")
            elif outcome == "2":
                patient_registry[target_id]["status"] = (
                    "Failure - Case Closed"
                )
                print("Operation failed. Medical file closed.")
            elif outcome == "3":
                patient_registry[target_id]["status"] = "Transferred"
                print("Patient transferred to another facility.")
        else:
            print("Incorrect Patient ID.")
    else:
        print("[ERROR] Invalid Surgeon ID.")