from fastapi import APIRouter, HTTPException
from app.gemini_utils import generate_sql_from_prompt, generate_message_from_result,check_bounds,prompt_intent
from app.database import get_db
from sqlalchemy import text

from fastapi.responses import FileResponse, JSONResponse
import plotly.express as px
import uuid
import os
import json
import pandas as pd
import base64
import re

from sqlalchemy.orm import Session

router = APIRouter()

def extract_json_only(response_text):
    try:
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found")
        json_str = match.group(0)
        return json.loads(json_str)
    except Exception as e:
        print("Failed to parse JSON:", e)
        return None

@router.post("/query")
def run_query(prompt: str):
    try:
        print(f"Received prompt: {prompt}")
        chart_type_response = prompt_intent(prompt)
        print(f"Intent: {chart_type_response }")
        parsed_info = json.loads(chart_type_response)
        
        

        # Step 1: Generate SQL query from Gemini
        sql_query = parsed_info.get("query","")
        print(sql_query)

        # Step 2: Run SQL on DB using SQLAlchemy Session
        # if not check_bounds(prompt):
        #     raise HTTPException(status_code=400, detail="Invalid request. Only queries involving ad_sales, total_sales, or eligibility tables are supported.")
        
        
        db: Session = next(get_db())
        result_proxy = db.execute(text(sql_query))
        rows = result_proxy.fetchall()
        columns = result_proxy.keys()
        result = [dict(zip(columns, row)) for row in rows]
        
        print(f"SQL Result: {result}")

        # Step 3: Convert to natural language
        if parsed_info["type"] == "text":
            final_message = generate_message_from_result(prompt,result)
            print(f"Final message: {final_message}")
            return JSONResponse(content={"type": "text", "message": final_message})
        if parsed_info["type"] == "chart":
             # Generate Plotly chart
            df = pd.DataFrame(result)
            print(df)
            chart_img = None

            if parsed_info["chart"] == "bar":
                fig = px.bar(df, x=parsed_info["x_axis"], y=parsed_info["y_axis"])
            elif parsed_info["chart"] == "line":
                fig = px.line(df, x=parsed_info["x_axis"], y=parsed_info["y_axis"])
            elif parsed_info["chart"] == "pie":
                fig = px.pie(df, names=parsed_info["x_axis"], values=parsed_info["y_axis"])
            elif parsed_info["chart"] == "scatter":
                fig = px.scatter(df, x=parsed_info["x_axis"], y=parsed_info["y_axis"])
            else:
                return JSONResponse(content={"type": "text", "content": "Chart type not supported."})

            # Convert chart to base64
            img_bytes = fig.to_image(format="png")
            b64_image = base64.b64encode(img_bytes).decode("utf-8")
            fig.write_image(f"chart_{uuid.uuid4()}.png")  # Save to file for debugging
            print(f"Base64 Image: {b64_image[:30]}...")
            return JSONResponse(content={"type": "chart", "image": b64_image})
       

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
