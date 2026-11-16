from itertools import product
from typing import Annotated
from pydantic import BaseModel, Field

class StoreOffer(BaseModel):
    store_name: Annotated[str,Field(min_length=3, examples=["Amazon India"])]
    price_inr: Annotated[float,Field(gt=0, examples=["54999.0"])]
    in_stock: bool = True
class ProductComareRequest(BaseModel):
    product_name: Annotated[str, Field(min_length=3, examples=["iphone 15"])]
    offers: Annotated[list[StoreOffer],Field(min_length=1)]

class AIDealVerdict(BaseModel):
    buy_score: Annotated[int, Field(ge=1, le=10,description="Score from 1 to 10")]
    headline: str
    pro: list[str]
    cons: list[str]

class FullAnalyzeResponse(BaseModel):
    product: str
    cheapest_store: str
    lowest_price: float
    ai_verdict: AIDealVerdict
    latency_ms: float