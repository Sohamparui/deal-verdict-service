# AI Deal Microservice

A production-ready FastAPI microservice that compares e-commerce product offers across multiple retailers and generates an AI-powered buying verdict using Google Gemini (`gemini-3.8-flash`).

---

## Features

- **Deterministic Offer Filtering**: Automatically filters out-of-stock listings and detects the lowest price offer.
- **AI-Powered Deal Analysis**: Uses Google Gemini to generate structured JSON deal verdicts, including a buying score (1–10), punchy headline, pros, and cons.
- **Strict Pydantic Schemas**: Validates incoming payloads and guarantees structured output schemas.
- **Async Execution & Latency Tracking**: End-to-end asynchronous requests with execution latency reported in milliseconds.
- **Interactive Documentation**: Built-in Swagger UI and ReDoc generated automatically by FastAPI.

---

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **LLM / AI**: [Google GenAI SDK](https://github.com/google-gemini/google-genai) (`gemini-3.8-flash`)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Configuration**: [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## Project Structure

```text
fast_api/
├── main.py              # FastAPI microservice endpoints and Gemini integration
├── schemas.py           # Pydantic data schemas for requests and responses
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore configuration
└── README.md            # Project documentation
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 2. Clone the Repository

```bash
git clone <your-github-repo-url>
cd fast_api
```

### 3. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory by copying `.env.example`:

```bash
cp .env.example .env
```

Open `.env` and enter your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

## Running the Application

Start the development server with hot-reload enabled:

```bash
uvicorn main:app --reload
```

The service will be accessible at:
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc Alternative Docs**: `http://127.0.0.1:8000/redoc`

---

## API Reference

### Analyze Deal

Compares available store offers and returns the lowest price alongside an AI buying recommendation.

- **URL**: `/api/v1/analyze-deal`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body Example

```json
{
  "product_name": "Apple iPhone 15 (128 GB)",
  "offers": [
    {
      "store_name": "Amazon India",
      "price_inr": 69999.0,
      "in_stock": true
    },
    {
      "store_name": "Flipkart",
      "price_inr": 66999.0,
      "in_stock": true
    },
    {
      "store_name": "Croma",
      "price_inr": 65999.0,
      "in_stock": false
    }
  ]
}
```

#### Response Example (`200 OK`)

```json
{
  "product": "Apple iPhone 15 (128 GB)",
  "cheapest_store": "Flipkart",
  "lowest_price_inr": 66999.0,
  "ai_verdict": {
    "buy_score": 8,
    "headline": "Solid Deal on Base Flagship with Good Flipkart Pricing",
    "pro": [
      "Cheapest currently in-stock option across analyzed stores",
      "Noticeable price cut below standard Indian retail MRP"
    ],
    "cons": [
      "128 GB internal storage may feel restrictive without cloud storage",
      "Better bank card promotions may appear during seasonal sales"
    ]
  },
  "latency_ms": 780.45
}
```

#### Error Responses

- **`400 Bad Request`**: When all submitted store offers are out of stock.
- **`502 Bad Gateway`**: When the Gemini API call fails or all fallback models are unreachable.
- **`422 Unprocessable Entity`**: Request validation error (e.g. empty offers list or missing fields).

---

## Pushing to GitHub

To push this repository to GitHub for the first time:

1. Create a new repository on [GitHub](https://github.com/new).
2. Run the following commands in the project directory:

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```
