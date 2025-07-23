import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


def generate_sql_from_prompt(prompt: str) -> str:
    full_prompt = (
    "You are an expert SQL query generator. Your task is to generate only the raw SQL query as plain text. "
    "Do not include any explanations, markdown formatting, or comments—return only the SQL query string. "
    "The SQL must be compatible with SQLite. "
    "The database contains the following tables:\n"
    "- ad_sales(date, item_id, ad_sales, impressions, clicks, ad_spend)\n"
    "- total_sales(date, item_id, total_sales, total_units_ordered)\n"
    "- eligibility(eligibility_datetime_utc, item_id, eligibility, message)\n"
    f"User request: {prompt}"
)
#     full_prompt = (
#     "You are an expert SQLite SQL query generator. "
#     "You must only generate valid SQL queries based strictly on the following three tables:\n"
#     "- ad_sales(date, item_id, ad_sales, impressions, clicks, ad_spend)\n"
#     "- total_sales(date, item_id, total_sales, total_units_ordered)\n"
#     "- eligibility(eligibility_datetime_utc, item_id, eligibility, message)\n"
#     "Do NOT discuss or reference any other tables, fields, schemas, or topics outside of these. "
#     "If the user prompt requests anything unrelated to these tables, respond with: "
#     "\"Invalid request. Only queries involving ad_sales, total_sales, or eligibility tables are supported.\"\n"
#     "Return only a raw SQLite-compatible SQL query. Do NOT include explanations, markdown, or formatting. "
#     "Stay strictly within the schema boundaries and do not hallucinate missing tables or columns."
# )
    
    response = model.generate_content(full_prompt)
    raw_sql = response.text.strip()

    # Clean leading 'sql' or markdown
    if raw_sql.lower().startswith("sql"):
        raw_sql = raw_sql[3:].strip()

    # Remove any triple backticks or code blocks
    raw_sql = raw_sql.strip("`").strip()

    return raw_sql



def generate_message_from_result(prompt: str, result: list[dict]) -> str:
    system_prompt = (
        "You are a helpful assistant. Given a user question and result from a database, generate a user-friendly summary."
    )
    user_input = f"Question: {prompt}\nResult: {result}"
    response = model.generate_content(user_input + " " +system_prompt)
    return response.text.strip()


def prompt_intent(prompt: str):
    chart_type_prompt = f"""
        You are a data assistant.

        The database contains the following tables:
        - ad_sales(date, item_id, ad_sales, impressions, clicks, ad_spend)
        - total_sales(date, item_id, total_sales, total_units_ordered)
        - eligibility(eligibility_datetime_utc, item_id, eligibility, message)
        "You are an expert SQL query generator. Your task is to generate only the raw SQL query as plain text. "
    "Do not include any explanations, markdown formatting, or comments—return only the SQL query string. "    
        Given the following user prompt, respond with ONLY a valid JSON object in this format:
        {{
        "type": "text" or "chart",
        "chart": "bar", "line", "pie", or "none",
        "x_axis": "column_name" or null,
        "y_axis": "column_name" or null
        "query": "raw SQL query"     
    }}

        DO NOT include any text, explanation, markdown, or formatting.
        Return only raw JSON, without any explanation, code block, or formatting.

        Prompt: {prompt}
        """

    response = model.generate_content(chart_type_prompt)
    return response.text  # Normalize to lowercase for consistency

ALLOWED_TABLES = {
    "ad_sales": {"date", "item_id", "ad_sales", "impressions", "clicks", "ad_spend"},
    "total_sales": {"date", "item_id", "total_sales", "total_units_ordered"},
    "eligibility": {"eligibility_datetime_utc", "item_id", "eligibility", "message"}
}

def check_bounds(prompt: str) -> bool:
    """
    Check whether the prompt only refers to allowed tables and columns.
    Returns True if the prompt is within bounds, False otherwise.
    """
    normalized = prompt.lower()

    # Combine all allowed table and column names into a set
    allowed_keywords = set(ALLOWED_TABLES.keys())
    for columns in ALLOWED_TABLES.values():
        allowed_keywords.update(col.lower() for col in columns)

    # Extract potential words that could be table or column references
    tokens = set(re.findall(r"\b[a-zA-Z_]+\b", normalized))

    # Allow basic SQL keywords to avoid false positives
    sql_keywords = {
        'select', 'from', 'where', 'and', 'or', 'join', 'on', 'group', 'by', 'order',
        'asc', 'desc', 'limit', 'inner', 'left', 'right', 'outer', 'as', 'having',
        'sum', 'count', 'avg', 'min', 'max', 'distinct'
    }

    # If any token looks like a table/column but is not allowed, reject the prompt
    for token in tokens:
        if token not in allowed_keywords and token not in sql_keywords and not token.isdigit():
            return False

    return True
    
    

if __name__ == "__main__":
    print(prompt_intent("Which product had the highest CPC (Cost Per Click)?"))