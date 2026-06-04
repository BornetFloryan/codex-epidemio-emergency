from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))

from src.epidemio_common.api_client import remove_accents, search_datasets
from src.epidemio_common.cache import save_api_query


def build_query_variants(query: str) -> list[str]:
    query = query.strip()
    lowered = query.lower()
    variants = [query]

    without_accents = remove_accents(query)
    if without_accents != query:
        variants.append(without_accents)

    if "grippe" in lowered or "grippal" in lowered:
        variants.extend(
            [
                "indicateur avancé sanitaire syndrome grippal",
                "syndrome grippal",
                "incidence syndrome grippal",
                "Santé publique France grippe",
                "Sentinelles grippe",
                "vaccination grippe",
            ]
        )

    if "gastro" in lowered:
        variants.extend(
            [
                "indicateur avancé sanitaire gastro-entérite",
                "gastro-entérite",
                "gastro enterite",
                "incidence gastro-entérite",
                "Santé publique France gastro-entérite",
            ]
        )

    if "santé" in lowered or "sanitaire" in lowered or "epidem" in remove_accents(lowered):
        variants.extend(
            [
                "veille sanitaire",
                "surveillance épidémiologique",
                "indicateur sanitaire",
                "Santé publique France",
            ]
        )

    unique = []
    for variant in variants:
        if variant and variant not in unique:
            unique.append(variant)

    return unique


def merge_results(existing: list[dict], new_results: list[dict]) -> list[dict]:
    seen = {item.get("page") or item.get("title") for item in existing}
    merged = list(existing)

    for item in new_results:
        key = item.get("page") or item.get("title")
        if key and key not in seen:
            merged.append(item)
            seen.add(key)

    merged.sort(key=lambda item: item.get("relevance_score", 0), reverse=True)
    return merged


def build_response(query: str) -> dict:
    variants = build_query_variants(query)

    all_results = []
    attempts = []
    source_api = None
    generated_at = None
    final_status = "ok"
    final_message = None
    limits = []

    for variant in variants:
        api_result = search_datasets(query=variant, page_size=5)
        source_api = api_result.get("source_api", source_api)
        generated_at = api_result.get("generated_at", generated_at)
        limits = api_result.get("limits", limits)

        results = api_result.get("results", [])
        attempts.append(
            {
                "query": variant,
                "status": api_result.get("status"),
                "results_count": len(results),
                "message": api_result.get("message"),
            }
        )

        if api_result.get("status") == "error":
            final_status = "partial_error"
            final_message = api_result.get("message")
            continue

        all_results = merge_results(all_results, results)

    if not all_results and final_status != "partial_error":
        final_status = "ok_no_results"
        final_message = "Aucun jeu de données trouvé avec la requête et ses variantes."

    response = {
        "status": final_status,
        "query": query,
        "query_variants_used": variants,
        "attempts": attempts,
        "generated_at": generated_at,
        "source_api": source_api,
        "sources": ["data.gouv.fr"],
        "results_count": len(all_results),
        "results": all_results[:10],
        "message": final_message,
        "limits": limits
        or [
            "Les résultats doivent être vérifiés auprès des sources officielles.",
            "Ce projet ne fournit aucun diagnostic médical.",
        ],
    }

    response["cache_saved"] = save_api_query(
        skill="health-dataset-search",
        query=query,
        status=final_status,
        result=response,
    )

    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Search public health datasets through data.gouv.fr.")
    parser.add_argument("query", nargs="*", help="Dataset search query")
    args = parser.parse_args()

    query = " ".join(args.query).strip() or "santé publique épidémiologie"

    print(json.dumps(build_response(query), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
