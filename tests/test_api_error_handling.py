import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from main import app


client = TestClient(app)


def test_endpoint_returns_503_for_runtime_error(monkeypatch):
    async def fake_weather_chatter(*args, **kwargs):
        raise RuntimeError("OPENWEATHER_API_KEY is not configured")

    monkeypatch.setattr("main.WeatherChat.weather_chatter", fake_weather_chatter)

    response = client.get(
        "/api/prompt",
        params={
            "user_prompt": "What is the weather like?",
            "lat": 40.7128,
            "lon": -74.0060,
            "current_location": "New York",
        },
    )

    assert response.status_code == 503
    assert "OPENWEATHER_API_KEY" in response.json()["detail"]
