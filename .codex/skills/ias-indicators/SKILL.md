# AGENTS.md

## Nature du projet

Ce dépôt contient une adaptation Codex du projet de skills demandé dans le cours.

Le thème choisi est la veille épidémiologique en situation d’urgence.

## Objectif opérationnel

Aider un agent à répondre rapidement à des questions comme :

- Quelle est la situation épidémiologique actuelle ?
- Quels signaux sanitaires faut-il surveiller ?
- Quelle est la tendance grippe ou gastro-entérite ?
- Peut-on produire une courte note de situation pour une cellule de crise ?

## Architecture

- `.codex/skills/` contient les skills Codex, conformément au support de cours.
- Chaque skill possède un `SKILL.md`.
- Chaque script Python est testable seul en terminal.
- Les fichiers `references/` contiennent les détails longs : sources, limites, formats et exemples.
- Le projet repose sur des skills et des scripts CLI Python.
- Le projet ne repose pas sur un serveur MCP.

## Contraintes

- Ne pas fournir de diagnostic médical individuel.
- Toujours indiquer les limites des données.
- Toujours mentionner la source utilisée.
- Produire une réponse courte, claire et utile en situation tendue.
- Garder les `SKILL.md` courts.
- Mettre les détails longs dans `references/`.
- Tester les scripts Python seuls avant de les utiliser avec Codex.

## Commandes utiles

```bash
python .codex/skills/ias-indicators/main.py --indicator grippe
python .codex/skills/public-health-search/main.py "grippe santé publique"
python .codex/skills/trend-analysis/main.py --sample
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
python -m pytest
```

## Expected output

Return:

- trend;
- last value;
- previous value;
- delta;
- interpretation;
- limits.

Do not overinterpret the result.
