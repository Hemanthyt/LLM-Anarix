from fastapi import APIRouter, HTTPException
from app.gemini_utils import generate_sql_from_prompt, generate_message_from_result,check_bounds
from app.database import get_db
from sqlalchemy import text

from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/query")
def run_query(prompt: str):
    try:
        print(f"Received prompt: {prompt}")

        # Step 1: Generate SQL query from Gemini
        sql_query = generate_sql_from_prompt(prompt)
        print(sql_query)

        # Step 2: Run SQL on DB using SQLAlchemy Session
        # if not check_bounds(prompt):
        #     raise HTTPException(status_code=400, detail="Invalid request. Only queries involving ad_sales, total_sales, or eligibility tables are supported.")
        db: Session = next(get_db())
        result_proxy = db.execute(text(sql_query))
        rows = result_proxy.fetchall()
        columns = result_proxy.keys()
        result = [dict(zip(columns, row)) for row in rows]

        # Step 3: Convert to natural language
        formatted_data = f"Prompt: {prompt}\nData: {result}"
        final_message = generate_message_from_result(prompt,result)

        return {
            "message": final_message
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
