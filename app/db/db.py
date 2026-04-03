import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST","localhost"),
        port=os.getenv("PG_PORT","5432"),
        dbname=os.getenv("PG_DB","parking"),
        user=os.getenv("PG_USER","parking_user"),
        password=os.getenv("PG_PASSWORD"),   
            
            
                )