from datetime import datetime
from typing import List


class HospitalStaff:
    """Base class for all hospital employees."""

    def __init__(self, staff_id: str, name: str, base_salary: float):
        self.staff_id = staff_id
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self) -> float:
        return self.base_salary


class Nurse(HospitalStaff):
    """Class representing a nurse with shift allowances."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        base_salary: float,
        shift_days: List[str],
    ):
        super().__init__(staff_id, name, base_salary)
        self.shift_days = shift_days

    def calculate_pay(self) -> float:
        return self.base_salary + 20000.0


class Doctor(HospitalStaff):
    """Class representing a general practitioner doctor."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        base_salary: float,
        shift_days: List[str],
        consultation_fee: float,
    ):
        super().__init__(staff_id, name, base_salary)
        self.shift_days = shift_days
        self.consultation_fee = consultation_fee
        self.consultations_done = 0

    def calculate_pay(self) -> float:
        bonus = self.consultations_done * 5000.0
        return self.base_salary + bonus


class Surgeon(Doctor):
    """Class representing a specialized surgeon."""

    def __init__(
        self,
        staff_id: str,
        name: str,
        base_salary: float,
        shift_days: List[str],
        consultation_fee: float,
        operation_fee: float,
    ):
        super().__init__(
            staff_id, name, base_salary, shift_days, consultation_fee
        )
        self.operation_fee = operation_fee
        self.operations_done = 0

    def calculate_pay(self) -> float:
        doctor_salary = super().calculate_pay()
        bonus_op = self.operations_done * 15000.0
        return doctor_salary + bonus_op


class Patient:
    """Class dedicated to tracking patient medical data."""

    def __init__(self, patient_id: str, name: str, age: int, temperature: float):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.temperature = temperature
        self.symptoms: List[str] = []
        self.status: str = "Awaiting Diagnosis"
        self.prescription: str = "None."
        self.assigned_practitioner_name: str = ""
        self.admission_date = datetime.now().strftime("%d/%m/%Y %H:%M")