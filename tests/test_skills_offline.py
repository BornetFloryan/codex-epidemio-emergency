from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


trend = load_module("trend_analysis_main", ".codex/skills/trend-analysis/main.py")
crisis = load_module("crisis_report_main", ".codex/skills/crisis-report/main.py")
health = load_module("health_dataset_search_main", ".codex/skills/health-dataset-search/main.py")
geo = load_module("geo_zone_context_main", ".codex/skills/geo-zone-context/main.py")
weather = load_module("weather_alert_context_main", ".codex/skills/weather-alert-context/main.py")


def test_trend_analysis_increasing():
    result = trend.analyze([12, 15, 18, 22])

    assert result["status"] == "ok"
    assert result["trend"] == "increasing"
    assert result["delta"] == 4
    assert result["limits"]


def test_trend_analysis_requires_two_values():
    result = trend.analyze([12])

    assert result["status"] == "error"
    assert "message" in result


def test_crisis_report_flags_rising_signal():
    result = crisis.build_report("Hausse des syndromes grippaux en France")

    assert result["status"] == "ok"
    assert result["attention_level"] == "modéré"
    assert result["sources"]
    assert any("diagnostic" in limit.lower() for limit in result["limits"])


def test_health_query_variants_cover_flu():
    variants = health.build_query_variants("grippe sante publique")

    assert "syndrome grippal" in variants
    assert "Sentinelles grippe" in variants


def test_geo_context_success_without_network(monkeypatch):
    def fake_search_communes(query: str, limit: int = 5):
        return {
            "status": "ok",
            "query": query,
            "source_api": "fake-geo",
            "results": [
                {
                    "name": "Besançon",
                    "code_insee": "25056",
                    "postal_codes": ["25000"],
                    "population": 120000,
                    "department_code": "25",
                    "department_name": "Doubs",
                    "region_name": "Bourgogne-Franche-Comté",
                    "latitude": 47.24,
                    "longitude": 6.02,
                }
            ],
            "limits": ["fake limit"],
        }

    monkeypatch.setattr(geo, "search_communes", fake_search_communes)
    monkeypatch.setattr(geo, "save_api_query", lambda **kwargs: True)

    result = geo.build_response("Besancon")

    assert result["status"] == "ok"
    assert result["best_match"]["code_insee"] == "25056"
    assert result["cache_saved"] is True


def test_weather_context_success_without_network(monkeypatch):
    def fake_search_communes(query: str, limit: int = 1):
        return {
            "status": "ok",
            "source_api": "fake-geo",
            "results": [
                {
                    "name": "Besançon",
                    "latitude": 47.24,
                    "longitude": 6.02,
                }
            ],
        }

    def fake_weather(latitude: float, longitude: float):
        return {
            "status": "ok",
            "current": {
                "temperature_2m": 31,
                "relative_humidity_2m": 40,
                "precipitation": 0,
                "wind_speed_10m": 12,
            },
            "units": {"temperature_2m": "°C"},
        }

    monkeypatch.setattr(weather, "search_communes", fake_search_communes)
    monkeypatch.setattr(weather, "get_current_weather", fake_weather)
    monkeypatch.setattr(weather, "save_api_query", lambda **kwargs: True)

    result = weather.build_response("Besancon")

    assert result["status"] == "ok"
    assert result["weather"]["current"]["temperature_2m"] == 31
    assert any("Temperature elevee" in signal for signal in result["operational_signals"])
