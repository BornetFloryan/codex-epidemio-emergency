# AGENTS.md

## Nature du projet

Ce depot contient une adaptation Codex du projet de skills demande dans le cours.

Le theme choisi est la veille epidemiologique en situation d'urgence.

## Objectif

Fournir un ensemble coherent de skills permettant a Codex d'aider a la decision en situation tendue, notamment pour :

- rechercher des sources de donnees sanitaires ;
- analyser des indicateurs epidemiologiques ;
- qualifier une tendance ;
- produire une courte note de situation ;
- contextualiser une zone geographique ;
- contextualiser une situation meteorologique locale.

## Architecture

- `.codex/skills/` contient les skills Codex conformement au support de cours.
- Chaque skill contient un `SKILL.md`.
- Chaque skill peut appeler un script Python `main.py`.
- Les scripts Python sont testables seuls en terminal.
- Les fichiers `references/` contiennent les details longs pour eviter de surcharger les `SKILL.md`.
- `src/epidemio_common/` contient le code commun pour l'API et le cache SQLite.
- `data/epidemio_cache.sqlite` est cree automatiquement pour stocker les resultats des appels API.
- Le projet ne doit pas utiliser de serveur MCP.

## Regles de developpement

- Ne pas creer d'application web.
- Ne pas creer de serveur MCP.
- Ne pas fournir de diagnostic medical individuel.
- Toujours preciser les limites des donnees.
- Toujours mentionner les sources utilisees.
- Les scripts doivent retourner du JSON propre.
- Les erreurs reseau doivent etre gerees sans stacktrace brute.
- Les tests ne doivent pas dependre d'internet.

## Commandes utiles

```bash
python -m pytest

python .codex/skills/health-dataset-search/main.py "grippe sante publique"
python .codex/skills/ias-indicators/main.py --indicator grippe
python .codex/skills/ias-indicators/main.py --indicator gastro
python .codex/skills/trend-analysis/main.py --sample
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
python .codex/skills/geo-zone-context/main.py "Besancon"
python .codex/skills/weather-alert-context/main.py "Besancon"
```
