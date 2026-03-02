# Booking / Reservation Process (How it works)

## What you can reserve
- A parking space for a specific time window (start → end).
- Reservations are subject to availability.

## Required information
To create a reservation request, the chatbot will collect:
1) **First name**
2) **Last name**
3) **Car plate number**
4) **Reservation start date/time**
5) **Reservation end date/time**

## Steps
1. You tell the chatbot you want to reserve (e.g., “Reserve tomorrow 10:00–12:00”).
2. The chatbot asks for any missing details.
3. The system validates the request:
   - start time is before end time
   - plate format is acceptable
   - capacity/availability check (if enabled)
4. You receive a **summary** and confirm.
5. The request is stored as a **draft/pending** reservation (Stage 1).
   - In later stages, an administrator can approve/deny (human-in-the-loop).

## What you receive
- A confirmation message containing:
  - reservation period
  - car plate (may be partially masked for privacy)
  - reservation request ID (if implemented)
