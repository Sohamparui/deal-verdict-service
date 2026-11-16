# AI Deal Verdict Microservice

A production-grade FastAPI microservice that compares e-commerce product offers across multiple retailers and generates structured, AI-powered buying verdicts using Google Gemini.

---

## Features

- **Deterministic Offer Filtering**: Filters out-of-stock items and deterministically pinpoints the best available offer by price.
- **Structured AI Generation**: Uses Google GenAI SDK with JSON schema constraints (`response_schema=AIDealVerdict`) to guarantee strictly typed outputs without brittle prompt parsing.
- **Model Fallback Resilience**: Implements sequential fallback across Gemini models (`gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.5-flash`) for high availability.
- **Asynchronous & Latency Tracked**: Fully asynchronous execution path with end-to-end request latency captured in milliseconds.
- **Comprehensive Test Suite**: Automated unit tests with `pytest` and FastAPI's `TestClient`, covering edge cases, validation errors, and mocked external AI calls.
- **Interactive Documentation**: Built-in OpenAPI Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **AI / LLM**: [Google GenAI SDK](https://github.com/google-gemini/google-genai)
- **Testing**: [pytest](https://docs.pytest.org/) & [httpx](https://www.python-httpx.org/)

---

## Project Structure

```text
fast_api/
├── main.py              # FastAPI microservice endpoints and Gemini integration
├── schemas.py           # Pydantic data schemas for requests and responses
├── test_main.py         # Automated unit and integration tests
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

### 2. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from the example template:

```bash
cp .env.example .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

## Running the Application

Start the local development server:

```bash
uvicorn main:app --reload
```

- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/health`

---

## Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

Tests cover:
- Health check endpoint verification
- Deterministic cheapest price selection among in-stock offers
- Out-of-stock error handling (`400 Bad Request`)
- Payload schema validation (`422 Unprocessable Entity`)
- Mocked AI model response parsing and latency recording

---

## API Reference

### Health Check

- **URL**: `/health`
- **Method**: `GET`
- **Response**: `{"status": "ok", "service": "deal-analysis-service"}`

---

### Analyze Deal

- **URL**: `/api/v1/analyze-deal`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body

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

#### Response Body (`200 OK`)

```json
{
  "product": "Apple iPhone 15 (128 GB)",
  "cheapest_store": "Flipkart",
  "lowest_price_inr": 66999.0,
  "ai_verdict": {
    "buy_score": 8,
    "headline": "Solid Deal on Base Flagship with Good Flipkart Pricing",
    "pros": [
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
