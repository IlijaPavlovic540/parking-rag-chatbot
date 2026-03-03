import uuid
 
from app.core.guardrails import policy_check, redact_pii
from app.dialog.reservation_flow import ReservationDraft, missing_fields, validate, next_questions
from app.rag.rag_service import rag_answer
 
START_RES_WORDS = {"reserve", "reservation", "book", "booking", "start reservation"}
CANCEL_WORDS = {"cancel", "stop", "back", "exit reservation"}
 
def is_start_reservation(text: str) -> bool:
    t = text.strip().lower()
    return t in START_RES_WORDS or any(w in t for w in ["i want to reserve", "book a spot", "make a reservation"])
 
def is_cancel(text: str) -> bool:
    t = text.strip().lower()
    return t in CANCEL_WORDS
 
def main():
    session_id = str(uuid.uuid4())[:8]
    mode = "info"  # "info" or "reservation"
    draft = ReservationDraft()
 
    print("Parking Chatbot")
    print(f"Session: {session_id}")
    print("Commands: 'reserve' to book, 'cancel' to exit booking, 'exit' to quit.\n")
 
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            break
 
        # Guardrails on user input
        decision = policy_check(user)
        if not decision.allowed:
            print("Bot:", decision.reason)
            continue
 
        # Cancel reservation mode
        if mode == "reservation" and is_cancel(user):
            mode = "info"
            draft = ReservationDraft()
            print("Bot: Okay — booking cancelled. You can ask me parking questions.")
            continue
 
        # Start reservation mode (explicit)
        if mode == "info" and is_start_reservation(user):
            mode = "reservation"
            draft = ReservationDraft()
            print("Bot: Sure — let’s make a reservation.")
            print("Bot:", next_questions(missing_fields(draft)))
            continue
 
        # Reservation mode
        if mode == "reservation":
            miss = missing_fields(draft)
            if not miss:
                # Shouldn't happen often, but just in case
                mode = "info"
                print("Bot: Booking draft already complete. Type 'reserve' to start a new one.")
                continue
 
            field = miss[0]
            if field == "first_name": draft.first_name = user
            elif field == "last_name": draft.last_name = user
            elif field == "car_plate": draft.car_plate = user
            elif field == "start_dt": draft.start_dt = user
            elif field == "end_dt": draft.end_dt = user
 
            err = validate(draft)
            if err:
                print("Bot:", err)
                continue
 
            miss = missing_fields(draft)
            if miss:
                print("Bot:", next_questions(miss))
                continue
 
            summary = (
                f"Reservation draft collected:\n"
                f"- Name: {draft.first_name} {draft.last_name}\n"
                f"- Plate: {draft.car_plate}\n"
                f"- Start: {draft.start_dt}\n"
                f"- End: {draft.end_dt}\n"
                f"(Stage 1 stores draft only; admin approval is Stage 2.)"
            )
            print("Bot:", redact_pii(summary))
 
            # Finish reservation mode
            mode = "info"
            draft = ReservationDraft()
            print("Bot: You can ask more questions, or type 'reserve' to book again.")
            continue
 
        # Info mode (RAG)
        answer, citations = rag_answer(user, k=5)
        answer = redact_pii(answer)
 
        print("Bot:", answer)
        if citations:
            print("Citations:", ", ".join(citations))
        print()
 
if __name__ == "__main__":
    main()