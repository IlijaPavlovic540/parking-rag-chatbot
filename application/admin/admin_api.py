from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from application.admin.admin_storage import (
    get_pending_requests,
    get_request_by_id,
    approve_request,
    reject_request,
)

from application.admin.admin_chain import (
    build_admin_review_message,
    parse_admin_reply,
)

app = FastAPI(title = "Admin Agent API")

class AdminReplyRequest(BaseModel):
    admin_reply:str


@app.get("/admin/pending")
def list_pending_requests():
    rows = get_pending_requests()

    out = []
    for row in rows:
        request_id,first_name,last_name,car_plate,start_dt,end_dt,status,created_at = row

        out.append({
            "request_id":request_id,
            "first_name":first_name,
            "last_name":last_name,
            "car_plate":car_plate,
            "start_dt":str(start_dt),
            "end_dt":str(end_dt),
            "status":status,
            "created_at":str(created_at)
        })
    return {"pending_requests": out}

@app.get("/admin/pending/{request_id}/review")
def get_admin_review(reqeust_id:int):
    row = get_request_by_id(reqeust_id)
    if not row:
        raise HTTPException(status_code=404, detail="Request not found")
    
    compact_row = (
        row[0], # request id
        row[1], # first name
        row[2], # last name
        row[3], # car plate
        row[4], # start date
        row[5], # end date
        row[6], # status
        row[8], # created at
    )

    message = build_admin_review_message(compact_row)

    return {
        "request_id" : reqeust_id,
        "review_message" : message,
    }

@app.post("/admin/pending/{request_id}/decision")
def submit_admin_decision(request_id: int,body: AdminReplyRequest):
    row = get_request_by_id(request_id)
    if not row:
        raise HTTPException ( status_code= 404, detail="request not found")
    decision = parse_admin_reply(body.admin_reply)
    print(decision.decision)
    if decision.decision == "APPROVED":
        updated = approve_request ( request_id, decision.comment)
        if updated == 0:
            raise HTTPException ( status_code = 400, detail="Request was not updated")
        return{
            "request_id": request_id,
            "status": "APPROVED",
            "comment": decision.comment,
        }
    
    if decision.decision == "REJECT":
        updated = reject_request(request_id, decision.comment)
        if updated == 0:
            raise HTTPException(status_code=404, detail="Request was not updated")
        return{
            "request_id": request_id,
            "status":"REJECTED",
            "comment":decision.comment,
        }
    return{
        "request_id": request_id,
        "status":"UNCHANGED",
        "message": "Could not determine approve/reject from administrator reply.",
    }
@app.get("/admin/request/{request_id}")
def get_request_status ( request_id: int):
    row = get_request_by_id(request_id)
    if not row:
        raise HTTPException(status_code=404,detail="request not found")
    
    return{
        "request_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "car_plate": row[3],
        "start_dt": str(row[4]),
        "end_dt": str(row[5]),
        "status": row[6],
        "admin_comment": row[7],
        "created_at": str(row[8]),
        "decision_at": str(row[9]) if row[9] else None,
    }