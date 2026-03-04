from app.dialog.reservation_flow import ReservationDraft, missing_fields, validate


def test_missing_fields_order():
    d = ReservationDraft()
    assert missing_fields(d) ==["first_name","last_name","car_plate","start_dt","end_dt"]

def test_validate_end_before_start():
    d = ReservationDraft(
        first_name="A",
        last_name="B",
        car_plate="BG 123 AB",
        start_dt="2026-02-28T12:00",
        end_dt="2026-02-28T10:00",
    )
    assert validate(d) == "End time must be after start time."

def test_validate_plate_format_rejects_garbage():
    d = ReservationDraft(
         first_name="A",
        last_name="B",
        car_plate="!!!",
        start_dt="2026-02-28T10:00",
        end_dt="2026-02-28T12:00",
    )
    assert "plate" in (validate(d) or "").lower()