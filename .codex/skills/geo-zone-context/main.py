#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))

from src.epidemio_common.api_client import GEO_API_BASE_URL, search_communes, utc_now_iso
from src.epidemio_common.cache import save_api_query


def build_response(query: str) -> dict:
    query = query.strip()
    api_result = search_communes(query=query, limit=5)
    results = api_result.get("results", [])
    best = results[0] if results else {}

    response = {
        "status": api_result.get("status", "error") if results else "ok_no_results",
        "query": query,
        "generated_at": utc_now_iso(),
        "source_api": api_result.get("source_api") or GEO_API_BASE_URL,
        "best_match": best or None,
        "all_results": results,
        "operational_summary": None,
        "limits": api_result.get("limits")
        or [
            "Les informations geographiques doivent etre verifiees avec les sources officielles.",
            "Les coordonnees correspondent au centre approximatif de la commune.",
            "Ce skill ne remplace pas une analyse terrain.",
        ],
        "sources": [
            "geo.api.gouv.fr",
        ],
    }

    if api_result.get("status") == "error":
        response["status"] = "error"
        response["message"] = api_result.get("message")
    elif best:
        response["operational_summary"] = (
            f"{best.get('name')} est situee dans le departement "
            f"{best.get('department_name')} ({best.get('department_code')}), "
            f"region {best.get('region_name')}. Population indiquee : "
            f"{best.get('population')} habitants."
        )
    else:
        response["message"] = "Aucune commune trouvee pour cette requete."

    response["cache_saved"] = save_api_query(
        skill="geo-zone-context",
        query=query,
        status=response["status"],
        result=response,
    )

    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Return geographic context for a French commune.")
    parser.add_argument("place", nargs="*", help="Commune name or postal code")
    args = parser.parse_args()

    query = " ".join(args.place).strip()
    print(json.dumps(build_response(query), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
