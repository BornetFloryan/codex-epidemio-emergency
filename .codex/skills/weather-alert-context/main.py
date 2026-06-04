from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))

from src.epidemio_common.api_client import (
    GEO_API_BASE_URL,
    OPEN_METEO_BASE_URL,
    get_current_weather,
    search_communes,
    utc_now_iso,
)
from src.epidemio_common.cache import save_api_query


def interpret_weather(current: dict) -> list[str]:
    signals = []

    precipitation = current.get("precipitation")
    wind_speed = current.get("wind_speed_10m")
    temperature = current.get("temperature_2m")

    if isinstance(precipitation, (int, float)) and precipitation > 0:
        signals.append("Precipitations en cours a prendre en compte pour les deplacements et interventions.")

    if isinstance(wind_speed, (int, float)) and wind_speed >= 50:
        signals.append("Vent significatif pouvant compliquer les operations exterieures.")
    elif isinstance(wind_speed, (int, float)) and wind_speed >= 30:
        signals.append("Vent modere a surveiller selon le contexte local.")

    if isinstance(temperature, (int, float)) and temperature >= 30:
        signals.append("Temperature elevee pouvant augmenter la vulnerabilite de certains publics.")
    elif isinstance(temperature, (int, float)) and temperature <= 0:
        signals.append("Temperature basse pouvant compliquer la prise en charge et les deplacements.")

    if not signals:
        signals.append("Aucun signal meteorologique fort detecte dans les donnees actuelles disponibles.")

    return signals


def build_response(query: str) -> dict:
    query = query.strip()
    geo_result = search_communes(query=query, limit=1)
    communes = geo_result.get("results", [])

    response = {
        "status": "ok_no_results",
        "query": query,
        "generated_at": utc_now_iso(),
        "source_api": {
            "geo": geo_result.get("source_api") or GEO_API_BASE_URL,
            "weather": OPEN_METEO_BASE_URL,
        },
        "matched_commune": communes[0] if communes else None,
        "weather": None,
        "operational_signals": [],
        "limits": [
            "Les donnees meteo proviennent d'Open-Meteo.",
            "Ce skill donne un contexte meteo local, pas une vigilance officielle.",
            "Pour une alerte officielle, verifier Meteo-France et les autorites competentes.",
            "Ce projet ne fournit aucun diagnostic medical individuel.",
        ],
        "sources": [
            "geo.api.gouv.fr",
            "Open-Meteo",
        ],
    }

    if geo_result.get("status") == "error":
        response["status"] = "error"
        response["message"] = geo_result.get("message")
    elif not communes:
        response["message"] = "Aucune commune trouvee pour cette requete."
    else:
        commune = communes[0]
        latitude = commune.get("latitude")
        longitude = commune.get("longitude")

        if latitude is None or longitude is None:
            response["status"] = "error"
            response["message"] = "La commune trouvee ne contient pas de coordonnees exploitables."
        else:
            weather_result = get_current_weather(latitude=latitude, longitude=longitude)
            response["weather"] = {
                "status": weather_result.get("status"),
                "current": weather_result.get("current"),
                "units": weather_result.get("units"),
            }

            if weather_result.get("status") == "error":
                response["status"] = "error"
                response["message"] = weather_result.get("message")
            else:
                current = weather_result.get("current") or {}
                response["status"] = "ok"
                response["operational_signals"] = interpret_weather(current)

    response["cache_saved"] = save_api_query(
        skill="weather-alert-context",
        query=query,
        status=response["status"],
        result=response,
    )

    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Return local weather context for a French commune.")
    parser.add_argument("place", nargs="*", help="Commune name or postal code")
    args = parser.parse_args()

    query = " ".join(args.place).strip()
    print(json.dumps(build_response(query), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
