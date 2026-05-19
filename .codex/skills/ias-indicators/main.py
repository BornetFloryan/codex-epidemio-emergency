#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


DATASETS = {
    "grippe": {
        "indicator": "syndrome grippal",
        "dataset_title": "Indicateur avancé sanitaire - syndrome grippal",
        "source": "data.gouv.fr / indicateurs sanitaires publics",
        "interpretation": "Indicateur utile pour surveiller une possible dynamique grippale.",
    },
    "gastro": {
        "indicator": "gastro-entérite",
        "dataset_title": "Indicateur avancé sanitaire - gastro-entérite",
        "source": "data.gouv.fr / indicateurs sanitaires publics",
        "interpretation": "Indicateur utile pour surveiller une possible dynamique de gastro-entérite.",
    },
}


def build_response(indicator: str) -> dict:
    selected = DATASETS.get(indicator)

    if selected is None:
        return {
            "status": "error",
            "message": "Indicateur non reconnu. Utiliser --indicator grippe ou --indicator gastro.",
            "allowed_values": list(DATASETS.keys()),
        }

    return {
        "status": "ok",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "indicator": selected["indicator"],
        "dataset_title": selected["dataset_title"],
        "source": selected["source"],
        "interpretation": selected["interpretation"],
        "operational_summary": (
            "Cet indicateur peut être utilisé comme signal de surveillance en situation d'urgence, "
            "mais il doit être interprété avec prudence et comparé à d'autres sources officielles."
        ),
        "limits": [
            "Ce script ne fournit pas de diagnostic médical.",
            "Les données doivent être vérifiées auprès de la source officielle.",
            "Un indicateur isolé ne suffit pas à caractériser une situation épidémiologique.",
            "La zone géographique et la période doivent être précisées pour une analyse fiable.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--indicator",
        required=True,
        choices=["grippe", "gastro"],
        help="Indicateur à analyser : grippe ou gastro",
    )
    args = parser.parse_args()

    print(json.dumps(build_response(args.indicator), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()