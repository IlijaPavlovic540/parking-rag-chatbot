import os

from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

CHAT_MODEL = os.getenv("CHAT_MODE", "gpt-4o-mini")

class AdminDecision(BaseModel):
    decision : Literal["APPROVED","REJECT", "UNKNOWN"] = Field (
        description="Structured administrator decision"
    )
    comment: Optional[str] = Field (
        default=None,
        description="Optional short explanation from administrator reply"
    )

review_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an assistant helping a parking administrator review reservation requests."
     "Create a short, clear, professional summary for a human administrator."
     "Do not approve or reject automatically. "
     "Only summarize the request so the administraotr can decide."
     ),
     (
         "user",
         "Reservation request:\n"
         "Request ID: {request_id}\n"
         "Customer: {first_name} {last_name}\n"
         "Car plate: {car_plate}\n"
         "Start: {start_dt}\n"
         "End: {end_dt}\n"
         "Status: {status}\n"
         "Created at:{created_at}\n\n"
         "Write a concise review message for the administrator."
     ),
])

decision_parser = PydanticOutputParser(pydantic_object=AdminDecision)

decision_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You convert administrator replise into structured decisions.\n"
     "If the reply clearly means approved, return APPROVED.\n"
     "If the reply clearly means reject, refuse, deny, or decline, return REJECT\n"
     "If the meaning is unclear, return UNKNOWN.\n\n"
     "{format_instructions}"
     ),
     (
         "user",
         "Administrator reply:\n{admin_reply}"
     ),
])

def get_llm():
    return ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0
    )


def build_admin_review_message(row) -> str:
    """
    Expected row shape from get_pending_requests():
    (
    request_id,
    first_name,
    last_name,
    car_plate,
    start_dt,
    end_dt,
    status,
    created_at
    )
    """
    (
        request_id,
        first_name,
        last_name,
        car_plate,
        start_dt,
        end_dt,
        status,
        created_at,
    ) = row

    llm = get_llm()
    chain = review_prompt | llm

    result = chain.invoke({
    "request_id":request_id,
    "first_name":first_name,
    "last_name":last_name,
    "car_plate":car_plate,
    "start_dt":start_dt,
    "end_dt":end_dt,
    "status":status,
    "created_at":created_at
    })

    return result.content.strip()

def parse_admin_reply ( admin_reply:str ) ->AdminDecision:
    llm = get_llm()
    chain = decision_prompt | llm | decision_parser

    return chain.invoke({
        "admin_reply": admin_reply,
        "format_instructions": decision_parser.get_format_instructions()
    })