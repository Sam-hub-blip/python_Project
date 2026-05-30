from models import Nurse, Doctor, Surgeon
from utils import read_full_log


def manage_admin_space(staff_directory, hospital_balance):
    code = input("\nEnter admin access code: ").strip()
    if code != "1234":
        print("[ERROR] Incorrect code.")
        return

    continue_admin = True
    while continue_admin:
        print("\n--- ADMINISTRATOR PANEL ---")
        print("1. Register Employee | 2. Remove Employee")
        print("3. Check Balance    | 4. Staff List")
        print("5. View Logs        | 6. Back")
        option_admin = input("Select option (1-6): ").strip()

        if option_admin == "1":
            try:
                staff_type = input("1.Nurse 2.Doctor 3.Surgeon: ").strip()
                staff_id = input("Staff ID: ").upper()
                if staff_id in staff_directory:
                    print("[ERROR] ID already exists.")
                    continue
                name = input("Full Name: ").strip()
                salary = float(input("Base Salary: "))
                days = input("Shift Days (comma separated): ").split(",")

                if staff_type == "1":
                    staff_directory[staff_id] = Nurse(
                        staff_id, name, salary, days
                    )
                elif staff_type == "2":
                    fee = float(input("Consultation fee: "))
                    staff_directory[staff_id] = Doctor(
                        staff_id, name, salary, days, fee
                    )
                elif staff_type == "3":
                    fee = float(input("Consultation fee: "))
                    op_fee = float(input("Operation fee: "))
                    staff_directory[staff_id] = Surgeon(
                        staff_id, name, salary, days, fee, op_fee
                    )
                else:
                    print("Invalid choice.")
                    continue
                print(f"[SUCCESS] {name} successfully registered.")
            except ValueError:
                print("[ERROR] Invalid numeric input.")

        elif option_admin == "2":
            id_to_remove = input("Enter ID to remove: ").upper()
            if id_to_remove in staff_directory:
                staff_directory.pop(id_to_remove)
                print("[SUCCESS] Employee removed.")
            else:
                print("[ERROR] Unknown ID.")

        elif option_admin == "3":
            print(f"\nCurrent Balance: {hospital_balance} FCFA")

        elif option_admin == "4":
            for k, emp in staff_directory.items():
                cls_name = type(emp).__name__
                pay = emp.calculate_pay()
                print(f"ID: {k} | {emp.name} | {cls_name} | Pay: {pay} FCFA")

        elif option_admin == "5":
            read_full_log()

        elif option_admin == "6":
            continue_admin = False