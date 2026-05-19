#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


SOURCES = [
    {
        "title": "Santé publique France - Géodes",
        "organization": "Santé publique France",
        "use": "Suivi d'indicateurs de santé publique et visualisation territoriale.",
        "keywords": ["santé publique", "géodes", "indicateurs", "épidémiologie"],
        "limits": "Les indicateurs doivent être interprétés dans leur contexte méthodologique.",
    },
    {
        "title": "Réseau Sentinelles",
        "organization": "Sorbonne Université / INSERM",
        "use": "Surveillance épidémiologique de syndromes comme la grippe ou la gastro-entérite.",
        "keywords": ["sentinelles", "grippe", "gastro", "surveillance"],
        "limits": "Les données peuvent être hebdomadaires et nécessitent une interprétation prudente.",
    },
    {
        "title": "data.gouv.fr - jeux de données santé",
        "organization": "Plateforme ouverte des données publiques françaises",
        "use": "Recherche de jeux de données publics liés à la santé ou à l'épidémiologie.",
        "keywords": ["data.gouv.fr", "open data", "santé", "dataset"],
        "limits": "La qualité, la fraîcheur et le format varient selon les producteurs.",
    },
]


def search_sources(query: str) -> dict:
    query_lower = query.lower()

    results = []
    for source in SOURCES:
        score = sum(1 for keyword in source["keywords"] if keyword in query_lower)
        if score > 0 or not query:
            results.append({**source, "score": score})

    results = sorted(results, key=lambda item: item["score"], reverse=True)

    return {
        "status": "ok",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "query": query,
        "results": results,
        "limits": [
            "Cette recherche est une aide à l'orientation vers des sources publiques.",
            "Il faut vérifier la fraîcheur et la méthode de production des données.",
            "Aucune conclusion sanitaire ne doit être tirée d'une source unique.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="*", help="Recherche de source santé publique")
    args = parser.parse_args()

    query = " ".join(args.query)
    print(json.dumps(search_sources(query), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()