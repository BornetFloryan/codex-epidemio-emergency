from __future__ import annotations

import unicodedata
from datetime import datetime, timezone
from typing import Any

import requests

DATA_GOUV_BASE_URL = "https://www.data.gouv.fr/api/1"
GEO_API_BASE_URL = "https://geo.api.gouv.fr"
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def remove_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_text(text: str) -> str:
    return remove_accents(text).lower().strip()


def build_error_response(source_api: str, query: str, message: str) -> dict[str, Any]:
    return {
        "status": "error",
        "query": query,
        "generated_at": utc_now_iso(),
        "source_api": source_api,
        "message": message,
        "results": [],
        "limits": [
            "La requête API n'a pas pu être exploitée.",
            "Vérifier la connexion internet ou réessayer plus tard.",
            "Ne pas tirer de conclusion sanitaire à partir d'une absence de résultat.",
            "Ce projet ne fournit aucun diagnostic médical individuel.",
        ],
    }


def parse_dataset_result(dataset: dict[str, Any]) -> dict[str, Any]:
    organization = dataset.get("organization") or {}
    resources = dataset.get("resources") or []

    page = dataset.get("page") or dataset.get("url") or dataset.get("uri")
    if not page and dataset.get("slug"):
        page = f"https://www.data.gouv.fr/fr/datasets/{dataset['slug']}/"

    parsed_resources = []
    for resource in resources[:10]:
        parsed_resources.append(
            {
                "title": resource.get("title") or resource.get("name") or "Ressource sans titre",
                "url": resource.get("url"),
                "format": resource.get("format"),
                "last_modified": resource.get("last_modified") or resource.get("modified"),
            }
        )

    return {
        "title": dataset.get("title") or "Jeu de données sans titre",
        "page": page,
        "organization": organization.get("name") if isinstance(organization, dict) else None,
        "description": dataset.get("description") or "",
        "last_update": dataset.get("last_update") or dataset.get("last_modified") or dataset.get("modified"),
        "resources_count": len(resources),
        "resources": parsed_resources,
    }


def score_health_dataset(result: dict[str, Any], query: str = "") -> dict[str, Any]:
    text = normalize_text(
        " ".join(
            [
                str(result.get("title") or ""),
                str(result.get("organization") or ""),
                str(result.get("description") or ""),
                query,
            ]
        )
    )

    score = 0
    reasons = []

    weighted_keywords = [
        ("syndrome grippal", 6),
        ("indicateur avance sanitaire", 6),
        ("gastro enterite", 6),
        ("incidence", 5),
        ("sante publique france", 4),
        ("sentinelles", 4),
        ("geodes", 4),
        ("epidemiologie", 3),
        ("surveillance", 3),
        ("grippe", 3),
        ("gastro", 3),
        ("vaccination", 1),
    ]

    for keyword, weight in weighted_keywords:
        if keyword in text:
            score += weight
            reasons.append(keyword)

    return {
        **result,
        "relevance_score": score,
        "relevance_reason": ", ".join(reasons) if reasons else "Pertinence faible ou non détectée automatiquement.",
    }


def search_datasets(query: str, page_size: int = 5, timeout: int = 10) -> dict[str, Any]:
    query = query.strip()

    if not query:
        return build_error_response(DATA_GOUV_BASE_URL, query, "La requête ne peut pas être vide.")

    try:
        response = requests.get(
            f"{DATA_GOUV_BASE_URL}/datasets/",
            params={"q": query, "page_size": page_size},
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return build_error_response(DATA_GOUV_BASE_URL, query, f"Erreur réseau ou API : {exc}")
    except ValueError as exc:
        return build_error_response(DATA_GOUV_BASE_URL, query, f"Réponse JSON invalide : {exc}")

    datasets = payload.get("data", [])
    parsed_results = [parse_dataset_result(dataset) for dataset in datasets]
    scored_results = [score_health_dataset(result, query) for result in parsed_results]
    scored_results.sort(key=lambda item: item.get("relevance_score", 0), reverse=True)

    return {
        "status": "ok",
        "query": query,
        "generated_at": utc_now_iso(),
        "source_api": DATA_GOUV_BASE_URL,
        "results": scored_results,
        "total": payload.get("total"),
        "limits": [
            "Les résultats proviennent de l'API publique data.gouv.fr.",
            "La présence d'un jeu de données ne garantit pas qu'il soit récent ou directement exploitable.",
            "Les données doivent être vérifiées auprès du producteur officiel.",
            "Ce projet ne fournit aucun diagnostic médical individuel.",
        ],
    }


def parse_commune_result(commune: dict[str, Any]) -> dict[str, Any]:
    centre = commune.get("centre") or {}
    coordinates = centre.get("coordinates") or [None, None]

    longitude = coordinates[0] if len(coordinates) > 0 else None
    latitude = coordinates[1] if len(coordinates) > 1 else None

    departement = commune.get("departement") or {}
    region = commune.get("region") or {}

    return {
        "name": commune.get("nom"),
        "code_insee": commune.get("code"),
        "postal_codes": commune.get("codesPostaux") or [],
        "population": commune.get("population"),
        "department_code": departement.get("code"),
        "department_name": departement.get("nom"),
        "region_code": region.get("code"),
        "region_name": region.get("nom"),
        "latitude": latitude,
        "longitude": longitude,
    }


def search_communes(query: str, limit: int = 5, timeout: int = 10) -> dict[str, Any]:
    query = query.strip()

    if not query:
        return build_error_response(GEO_API_BASE_URL, query, "La commune ou le code postal ne peut pas être vide.")

    params = {
        "fields": "nom,code,codesPostaux,centre,departement,region,population",
        "boost": "population",
        "limit": limit,
    }

    if query.isdigit():
        params["codePostal"] = query
    else:
        params["nom"] = query

    try:
        response = requests.get(
            f"{GEO_API_BASE_URL}/communes",
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return build_error_response(GEO_API_BASE_URL, query, f"Erreur réseau ou API : {exc}")
    except ValueError as exc:
        return build_error_response(GEO_API_BASE_URL, query, f"Réponse JSON invalide : {exc}")

    results = [parse_commune_result(commune) for commune in payload]

    return {
        "status": "ok",
        "query": query,
        "generated_at": utc_now_iso(),
        "source_api": GEO_API_BASE_URL,
        "results": results,
        "limits": [
            "Les informations proviennent de geo.api.gouv.fr.",
            "Les coordonnées sont approximatives et liées au centre de la commune.",
            "Ce skill ne remplace pas une analyse terrain.",
        ],
    }


def get_current_weather(latitude: float, longitude: float, timeout: int = 10) -> dict[str, Any]:
    try:
        response = requests.get(
            f"{OPEN_METEO_BASE_URL}/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
                "timezone": "Europe/Paris",
            },
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return build_error_response(OPEN_METEO_BASE_URL, f"{latitude},{longitude}", f"Erreur réseau ou API : {exc}")
    except ValueError as exc:
        return build_error_response(OPEN_METEO_BASE_URL, f"{latitude},{longitude}", f"Réponse JSON invalide : {exc}")

    return {
        "status": "ok",
        "query": f"{latitude},{longitude}",
        "generated_at": utc_now_iso(),
        "source_api": OPEN_METEO_BASE_URL,
        "current": payload.get("current") or {},
        "units": payload.get("current_units") or {},
        "limits": [
            "Les données météo proviennent d'Open-Meteo.",
            "Ce skill fournit un contexte météo, pas une vigilance officielle.",
            "Pour une alerte officielle, vérifier les autorités compétentes.",
        ],
    }