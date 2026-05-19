#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


def analyze(values: list[float]) -> dict:
    if len(values) < 2:
        return {
            "status": "error",
            "message": "Au moins deux valeurs sont nécessaires pour analyser une tendance.",
        }

    previous_value = values[-2]
    last_value = values[-1]
    delta = last_value - previous_value

    if abs(delta) < 0.00001:
        trend = "stable"
        interpretation = "La dernière valeur est équivalente à la précédente."
    elif delta > 0:
        trend = "increasing"
        interpretation = "La dernière valeur est supérieure à la précédente."
    else:
        trend = "decreasing"
        interpretation = "La dernière valeur est inférieure à la précédente."

    return {
        "status": "ok",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "values": values,
        "previous_value": previous_value,
        "last_value": last_value,
        "delta": delta,
        "trend": trend,
        "interpretation": interpretation,
        "limits": [
            "Cette analyse compare uniquement les deux dernières valeurs.",
            "Une tendance fiable nécessite plusieurs points, une période claire et une méthode statistique adaptée.",
            "Ce résultat ne constitue pas une conclusion épidémiologique officielle.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="Utiliser une série d'exemple")
    parser.add_argument("--values", nargs="*", type=float, help="Valeurs numériques à analyser")
    args = parser.parse_args()

    if args.sample:
        values = [12, 15, 18, 22]
    elif args.values:
        values = args.values
    else:
        values = []

    print(json.dumps(analyze(values), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()