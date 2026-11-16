import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from main import app
from schemas import AIDealVerdict

client = TestClient(app)


def test_health_check():
    """Verify service health endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "deal-analysis-service"}


def test_all_offers_out_of_stock():
    """Verify endpoint rejects requests when all offers are out of stock."""
    payload = {
        "product_name": "Sony WH-1000XM5",
        "offers": [
            {"store_name": "Amazon India", "price_inr": 29990.0, "in_stock": False},
            {"store_name": "Flipkart", "price_inr": 28990.0, "in_stock": False},
        ],
    }
    response = client.post("/api/v1/analyze-deal", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "All stores are out of stock!"


def test_empty_offers_validation_error():
    """Verify Pydantic validation rejects empty offers list."""
    payload = {
        "product_name": "Sony WH-1000XM5",
        "offers": [],
    }
    response = client.post("/api/v1/analyze-deal", json=payload)
    assert response.status_code == 422


@patch("main.ai_client")
def test_successful_deal_analysis(mock_ai_client):
    """Verify deterministic cheapest calculation and AI verdict parsing."""
    mock_response = MagicMock()
    mock_response.text = '{"buy_score": 9, "headline": "Terrific price for flagship headphones", "pros": ["Lowest recorded price", "Great ANC"], "cons": ["No aptX", "Non-folding design"]}'

    mock_ai_client.aio.models.generate_content = AsyncMock(return_value=mock_response)

    payload = {
        "product_name": "Sony WH-1000XM5",
        "offers": [
            {"store_name": "Amazon India", "price_inr": 29990.0, "in_stock": True},
            {"store_name": "Flipkart", "price_inr": 26990.0, "in_stock": True},
            {"store_name": "Reliance Digital", "price_inr": 25990.0, "in_stock": False},
        ],
    }

    response = client.post("/api/v1/analyze-deal", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Verify deterministic logic picked Flipkart (cheapest in-stock, ignoring Reliance which was out of stock)
    assert data["product"] == "Sony WH-1000XM5"
    assert data["cheapest_store"] == "Flipkart"
    assert data["lowest_price_inr"] == 26990.0
    assert data["ai_verdict"]["buy_score"] == 9
    assert len(data["ai_verdict"]["pros"]) == 2
    assert "latency_ms" in data
