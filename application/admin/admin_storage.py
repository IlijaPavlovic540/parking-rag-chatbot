from application.db.db import get_connection
 
def create_reservation_request(first_name, last_name, car_plate, start_dt, end_dt):
    sql = """
        INSERT INTO reservation_requests (
            first_name,
            last_name,
            car_plate,
            start_dt,
            end_dt,
            status
        )
        VALUES (%s, %s, %s, %s, %s, 'PENDING')
        RETURNING request_id;
    """
 
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, car_plate, start_dt, end_dt))
                request_id = cur.fetchone()[0]
                return request_id
    finally:
        conn.close()
 
 
def get_pending_requests():
    sql = """
        SELECT
            request_id,
            first_name,
            last_name,
            car_plate,
            start_dt,
            end_dt,
            status,
            created_at
        FROM reservation_requests
        WHERE status = 'PENDING'
        ORDER BY created_at;
    """
 
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()
 
 
def approve_request(request_id, admin_comment=None):
    sql = """
        UPDATE reservation_requests
        SET
            status = 'APPROVED',
            admin_comment = %s,
            decision_at = CURRENT_TIMESTAMP
        WHERE request_id = %s
          AND status = 'PENDING';
    """
 
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (admin_comment, request_id))
                return cur.rowcount
    finally:
        conn.close()
 
 
def reject_request(request_id, admin_comment=None):
    sql = """
        UPDATE reservation_requests
        SET
            status = 'REJECTED',
            admin_comment = %s,
            decision_at = CURRENT_TIMESTAMP
        WHERE request_id = %s
          AND status = 'PENDING';
    """
 
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (admin_comment, request_id))
                return cur.rowcount
    finally:
        conn.close()
 
 
def get_request_by_id(request_id):
    sql = """
        SELECT
            request_id,
            first_name,
            last_name,
            car_plate,
            start_dt,
            end_dt,
            status,
            admin_comment,
            created_at,
            decision_at
        FROM reservation_requests
        WHERE request_id = %s;
    """
 
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (request_id,))
            row = cur.fetchone()
            return row
    finally:
        conn.close()