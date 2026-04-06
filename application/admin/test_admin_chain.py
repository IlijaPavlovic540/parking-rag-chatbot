from application.admin.admin_chain import build_admin_review_message, parse_admin_reply

def main ():
    sample_row = (
        1,
        "Ilija",
        "Pavlovic",
        "BG 123 AB",
        "2026-02-28 10:00:00",
        "2026-02-28 12:00:00",
        "PENDING",
        "2026-02-20 09:30:00"
    )
    review = build_admin_review_message(sample_row)
    print("==== REVIEW MESSAGE ====")
    print(review)


    print("\n === DECISION PARS ===")
    d1 = parse_admin_reply("approve this request")
    print(d1)

    d2 = parse_admin_reply("reject this reservation, invalig timing")
    print(d2)

if __name__ == "__main__":
    main()