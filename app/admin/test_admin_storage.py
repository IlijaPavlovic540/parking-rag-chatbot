from app.admin.admin_storage import(
    create_reservation_request,
    get_pending_requests,
    approve_request,
    get_request_by_id,
)


def main():
    request_id = create_reservation_request(
        first_name="Ilija",
        last_name="Pavlovic",
        car_plate="BG 123 AB",
        start_dt="2026-02-28 10:00:00",
        end_dt="2026-02-28 12:00:00",
    )
    print("Created request_id:", request_id)

    pending = get_pending_requests()
    print("Pendging requests:")
    for row in pending:
        print(row)

    updated = approve_request(request_id, "Approved by admin test")
    print("Updated rows:", updated)

    row = get_request_by_id(request_id)
    print("FInal row:", row)

if __name__ == "__main__":
    main()