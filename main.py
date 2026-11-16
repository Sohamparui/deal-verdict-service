import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from schemas import AIDealVerdict, FullAnalyzeResponse, ProductComareRequest

load_dotenv()

app = FastAPI(title="Level 3: Production AI Deal Microservice")

ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

FALLBACK_MODELS = ["gemini-3.8-flash"]


@app.post("/api/v1/analyze-deal")
async def analyze_deal(payload: ProductComareRequest) -> FullAnalyzeResponse:
    start_time = time.perf_counter()

    # 1. Deterministic Python logic
    in_stock_offers = [o for o in payload.offers if o.in_stock]
    if not in_stock_offers:
        raise HTTPException(status_code=400, detail="All stores are out of stock!")

    best_offer = min(in_stock_offers, key=lambda x: x.price_inr)

    # 2. Build a clean prompt for Gemini
    prompt = (
        f"Analyze this deal for an Indian buyer.\n"
        f"Product: {payload.product_name}\n"
        f"Best Available Store: {best_offer.store_name} at ₹{best_offer.price_inr}\n"
        f"All In-Stock Offers: {[o.model_dump() for o in in_stock_offers]}\n"
        f"Give a realistic buy_score (1-10), a punchy headline, 2 pros, and 2 cons."
    )

    # 3. Call Gemini asynchronously with automatic model fallback
    response = None
    last_error = None

    for model_name in FALLBACK_MODELS:
        try:
            response = await ai_client.aio.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AIDealVerdict,
                    temperature=0.3,
                ),
            )
            break
        except Exception as e:
            last_error = e
            continue

    if response is None:
        raise HTTPException(
            status_code=502, detail=f"All AI models unavailable: {str(last_error)}"
        )

    # 4. Parse the guaranteed JSON back into our Pydantic object
    verdict = AIDealVerdict.model_validate_json(response.text)
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return FullAnalyzeResponse(
        product=payload.product_name,
        cheapest_store=best_offer.store_name,
        lowest_price_inr=best_offer.price_inr,
        ai_verdict=verdict,
        latency_ms=elapsed_ms,
    )