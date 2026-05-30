import os
from datetime import datetime
from typing import Dict, Any
from config import HOSPITAL_NAME


def log_activity(message: str) -> None:
    try:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        with open("hospital_log.txt", "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {message}\n")
    except IOError:
        print("[Error] Failed to write to the log file.")


def read_full_log() -> None:
    print("\n" + "=" * 16 + " HOSPITAL LOG HISTORY " + "=" * 16)
    if not os.path.exists("hospital_log.txt"):
        print("No log history available.")
        return
    try:
        with open("hospital_log.txt", "r", encoding="utf-8") as file:
            content = file.read()
            if content.strip():
                print(content)
            else:
                print("The log file is empty.")
    except IOError:
        print("[Error] Unable to read the log file.")
    print("=" * 54)


def generate_discharge_docs(
    patient_id: str, patient_info: Dict[str, Any], total_bill: float
) -> bool:
    clean_name = patient_info["name"].replace(" ", "_")
    current_date = datetime.now().strftime("%d/%m/%Y")
    try:
        with open(f"invoice_{clean_name}.txt", "w", encoding="utf-8") as f:
            f.write(
                f"{'='*50}\n"
                f"             DISCHARGE INVOICE - {HOSPITAL_NAME}\n"
                f"{'='*50}\n"
                f"Date: {current_date}\n"
                f"Patient ID: {patient_id} | Name: {patient_info['name']}\n"
                f"Occupied Room: {patient_info['room']}\n"
                f"Attending Practitioner: Dr. {patient_info['practitioner']}\n"
                f"{'-'*50}\n"
                f"TOTAL AMOUNT: {total_bill} FCFA\n"
                f"{'='*50}\n"
                f"Status: PAID / ACCOUNT SETTLED\n"
            )

        with open(f"prescription_{clean_name}.txt", "w", encoding="utf-8") as o:
            o.write(
                f"{'='*50}\n"
                f"            MEDICAL PRESCRIPTION - {HOSPITAL_NAME}\n"
                f"{'='*50}\n"
                f"Date: {current_date}\n"
                f"Patient: {patient_info['name']} ({patient_info['age']} yo)\n"
                f"Prescribed by: Dr. {patient_info['practitioner']}\n"
                f"{'-'*50}\n"
                f"PRESCRIPTION:\n"
                f"{patient_info['prescription']}\n"
                f"{'-'*50}\n"
                f"Signature and stamp of the medical wing.\n"
            )
        return True
    except IOError:
        return False