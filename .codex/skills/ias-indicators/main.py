from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))

from src.epidemio_common.api_client import search_datasets, utc_now_iso
from src.epidemio_common.cache import save_api_query

INDICATOR_QUERIES = {
    "grippe": {
        "label": "syndrome grippal",
        "query": "indicateur avancé sanitaire syndrome grippal",
        "interpretation": (
            "Cet indicateur peut aider à repérer une dynamique liée aux syndromes grippaux, "
            "mais il doit être comparé à d'autres sources officielles."
        ),
    },
    "gastro": {
        "label": "gastro-entérite",
        "query": "indicateur avancé sanitaire gastro-entérite",
        "interpretation": (
            "Cet indicateur peut aider à repérer une dynamique liée aux gastro-entérites, "
            "mais il doit être interprété avec prudence."
        ),
    },
}


def build_response(indicator: str) -> dict:
    config = INDICATOR_QUERIES[indicator]
    query = config["query"]

    api_result = search_datasets(query=query, page_size=5)
    status = api_result.get("status", "error")
    results = api_result.get("results", [])
    best_result = results[0] if results else {}

    response = {
        "status": status if results else "ok_no_results",
        "indicator": config["label"],
        "query": query,
        "generated_at": utc_now_iso(),
        "source_api": api_result.get("source_api"),
        "sources": ["data.gouv.fr"],
        "dataset_title": best_result.get("title"),
        "dataset_page": best_result.get("page"),
        "organization": best_result.get("organization"),
        "last_update": best_result.get("last_update"),
        "resources": best_result.get("resources", []),
        "resources_count": best_result.get("resources_count", 0),
        "relevance_score": best_result.get("relevance_score"),
        "all_results": results,
        "interpretation": config["interpretation"],
        "operational_summary": (
            "Cet indicateur peut être utilisé comme signal de surveillance en situation d'urgence, "
            "mais il doit être interprété avec prudence et comparé à d'autres sources officielles."
        ),
        "limits": [
            "Ce résultat indique des sources de données potentielles, pas une conclusion sanitaire.",
            "Les données doivent être vérifiées auprès du producteur officiel.",
            "Un indicateur isolé ne suffit pas à caractériser une situation épidémiologique.",
            "La zone géographique et la période doivent être précisées pour une analyse fiable.",
            "Ce projet ne fournit aucun diagnostic médical individuel.",
        ],
    }

    if api_result.get("status") == "error":
        response["status"] = "error"
        response["message"] = api_result.get("message")

    response["cache_saved"] = save_api_query(
        skill="ias-indicators",
        query=query,
        status=response["status"],
        result=response,
    )

    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Search datasets related to advanced sanitary indicators.")
    parser.add_argument(
        "--indicator",
        required=True,
        choices=sorted(INDICATOR_QUERIES.keys()),
        help="Indicator to search: grippe or gastro",
    )
    args = parser.parse_args()

    print(json.dumps(build_response(args.indicator), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
