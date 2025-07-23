from fastapi import Body, FastAPI, Depends, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from routes.gemini_routes import run_query
from app.gemini_utils import generate_sql_from_prompt


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174","http://localhost:5173"],  # In prod, specify only React origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/eligibility")
def get_eligibility(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM eligibility")).mappings().all()
    return list(result)

@app.get("/ad_sales")
def get_ad_sales(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM ad_sales")).mappings().all()
    return list(result)

@app.get("/total_sales")
def get_total_sales(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM total_sales")).mappings().all()
    return list(result)



@app.post("/ask-gemini/")
async def ask_gemini_endpoint(prompt: str = Body(..., embed=True)):
    response = run_query(prompt)
    return {"response": response}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


