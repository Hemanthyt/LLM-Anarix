# 📊 Gemini-AI Chart & Text Generation App

![Gemini AI Chart Generator](https://drive.google.com/uc?export=view\&id=179Y3R6Psa2Ql8zPpQeyupDT5tyVfRh0d)

## 🌟 Project Overview

This project leverages Google’s Gemini API to interpret user queries and generate dynamic content in two forms:

* 📄 **Textual Explanations** (natural language responses)
* 📈 **Visual Charts** (bar/scatter plots using Plotly)

It is a full-stack application combining FastAPI (Python) for the backend and React.js for the frontend.

---

## 🚀 Features

* Accepts user input prompts
* Detects if response type is `text` or `chart`
* If `chart`: parses JSON chart instructions, generates Plotly image, and returns it as Base64
* If `text`: returns structured, readable AI-generated content
* Displays chart or animated word-by-word paragraph

---

## ⚙️ Tech Stack

### 🖥️ Frontend

* React.js (Vite)
* Axios for API calls
* TailwindCSS (optional)

### 🧠 Backend

* FastAPI
* OpenAI / Gemini API integration
* Plotly for chart generation
* Kaleido for saving images

---

## 📬 API Endpoints

### `POST /ask-gemini/`

* **Request**: `{ "prompt": "Show me total sales by date as bar chart" }`
* **Response (text)**:

  ```json
  {
    "type": "text",
    "content": "Here's a breakdown of total sales over the past year..."
  }
  ```
* **Response (chart)**:

  ```json
  {
    "type": "chart",
    "image": "<base64-encoded-png>"
  }
  ```

---

## 🧠 How It Works

1. User enters prompt in frontend
2. Frontend sends it to FastAPI via Axios
3. Backend sends prompt to Gemini API and gets response
4. If response contains JSON chart description:

   * Parses `type`, `chart`, `x_axis`, `y_axis`
   * Uses Plotly to create chart
   * Converts it into Base64 PNG using Kaleido
5. Returns Base64 string to frontend
6. Frontend shows chart using:

   ```js
   const imageUrl = `data:image/png;base64,${base64string}`
   ```
7. If text response: animates it word-by-word with delay

---

## 🖼️ Image Handling

* Base64 image sent from backend:

  ```json
  { "type": "chart", "image": "iVBOR..." }
  ```
* Frontend usage:

  ```js
  setChartUrl(`data:image/png;base64,${data.image}`);
  ```

---

## 📁 Folder Structure

```
llm-anarix/
├── backend/
│   ├── main.py            # FastAPI backend
│   ├── requirements.txt   # Python dependencies
│   └── .venv/             # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main UI logic
│   │   ├── components/    # Custom UI components
│   │   └── utils/         # Delay animation, API utils
│   ├── public/
│   └── package.json
```

---

## 🛠️ Setup Instructions

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔚 Final Notes

* Ensure Plotly ≥ 6.1.1 and Kaleido = 0.2.1
* Use `data:image/png;base64,...` format in frontend for rendering image
* Customize chart types by adding `line`, `pie`, etc. support in backend

---

Feel free to fork, clone, or contribute. ✨
