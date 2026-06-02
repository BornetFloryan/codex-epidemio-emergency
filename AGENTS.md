# AGENTS.md

## Nature du projet

Ce dépôt contient une adaptation Codex du projet de skills demandé dans le cours.

Le thème choisi est la veille épidémiologique en situation d’urgence.

## Objectif

Fournir un ensemble cohérent de skills permettant à Codex d’aider à la décision en situation tendue, notamment pour :

- rechercher des sources de données sanitaires ;
- analyser des indicateurs épidémiologiques ;
- qualifier une tendance ;
- produire une courte note de situation.

## Architecture

- `.codex/skills/` contient les skills Codex conformément au support de cours.
- Chaque skill contient un `SKILL.md`.
- Chaque skill peut appeler un script Python `main.py`.
- Les scripts Python sont testables seuls en terminal.
- Les fichiers `references/` contiennent les détails longs pour éviter de surcharger les `SKILL.md`.
- `src/epidemio_common/` contient le code commun pour l’API et le cache SQLite.
- `data/epidemio_cache.sqlite` est créé automatiquement pour stocker les résultats des appels API.
- Le projet ne doit pas utiliser de serveur MCP.

## Règles de développement

- Ne pas créer d’application web.
- Ne pas créer de serveur MCP.
- Ne pas fournir de diagnostic médical individuel.
- Toujours préciser les limites des données.
- Toujours mentionner les sources utilisées.
- Les scripts doivent retourner du JSON propre.
- Les erreurs réseau doivent être gérées sans stacktrace brute.
- Les tests ne doivent pas dépendre d’internet.

## Commandes utiles

```bash
python -m pytest

python .codex/skills/health-dataset-search/main.py "grippe santé publique"
python .codex/skills/ias-indicators/main.py --indicator grippe
python .codex/skills/ias-indicators/main.py --indicator gastro
python .codex/skills/trend-analysis/main.py --sample
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
python .codex/skills/geo-zone-context/main.py "Besançon"
python .codex/skills/weather-alert-context/main.py "Besançon"
```
