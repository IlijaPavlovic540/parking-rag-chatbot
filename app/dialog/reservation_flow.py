from dataclasses import dataclass, asdict
from datetime import datetime
import re
from typing import Optional

PLATE_RE = re.compile(r"^[A-Z0-9 -]{4,12}$",re.IGNORECASE)

@dataclass
class ReservationDraft:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    car_plate: Optional[str] = None
    start_dt: Optional[str] = None #ISO string for simplicity
    end_dt: Optional[str] = None


def missing_fields(d:ReservationDraft)->list[str]:
    miss = []
    if not d.first_name: miss.append("first_name")
    if not d.last_name:miss.append("last_name")
    if not d.car_plate:miss.append("car_plate")
    if not d.start_dt:miss.append("start_dt")
    if not d.end_dt:miss.append("end_dt")
    return miss

def validate(d:ReservationDraft) -> Optional[str]:
    if d.car_plate and not PLATE_RE.match(d.car_plate.strip()):
        return "Car plate format looks invalid. Please enter something like 'BG 123 AB' ."
    if d.start_dt and d.end_dt:
        try:
            s = datetime.fromisoformat (d.start_dt)
            e = datetime.fromisoformat (d.end_dt)
        except ValueError:
            return "please provide date/time in ISO format like 2026-02-28T10:00."
        if e <= s:
            return "End time must be after start time."
    return None

def next_questions(missing: list [str])-> str:
    m = missing [0]
    if m == "fist_name": return "Sure - what's your first name?"
    if m == "last_name": return "And your last name?"
    if m == "car_plate": return "What is your car plate number?"
    if m == "start_dt": return "Reservation start date/time (ISO), e.g. 2026-02-28T10:00?"
    if m == "end_dt": return "Reservation end date/time (ISO), e/g/ 2026-02-28T12:00?"
    return "Please provide the missing reservation infromation."