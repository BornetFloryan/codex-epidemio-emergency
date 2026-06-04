import argparse
import json
from datetime import datetime


def build_report(text: str) -> dict:
    attention_level = "modéré" if any(
        word in text.lower()
        for word in ["hausse", "augmentation", "alerte", "urgence", "signal"]
    ) else "à qualifier"

    return {
        "status": "ok",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "title": "Note de situation épidémiologique",
        "operational_summary": text if text else "Aucune information détaillée fournie.",
        "attention_level": attention_level,
        "signals_to_monitor": [
            "Évolution des indicateurs sur plusieurs semaines.",
            "Différences régionales ou départementales.",
            "Cohérence entre plusieurs sources publiques.",
            "Présence éventuelle d'alertes officielles.",
        ],
        "recommended_actions": [
            "Vérifier les sources officielles.",
            "Comparer avec les semaines précédentes.",
            "Préciser la zone géographique, la période et l'indicateur.",
        ],
        "limits": [
            "Cette note est une synthèse d'aide à la décision.",
            "Elle ne remplace pas une expertise sanitaire officielle.",
            "Elle ne fournit pas de diagnostic médical individuel.",
        ],
        "sources": [
            "Sources publiques à vérifier : Santé publique France, Sentinelles, data.gouv.fr.",
        ],
        "medical_caution": "En cas de risque sanitaire réel, se référer aux autorités compétentes et aux sources officielles.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="*", help="Informations à synthétiser")
    args = parser.parse_args()

    text = " ".join(args.text)
    print(json.dumps(build_report(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
