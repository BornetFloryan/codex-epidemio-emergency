# Architecture du workflow

## Vue generale

```text
question
  -> planification par regles
  -> surveillance
  -> tendance
  -> territoire
  -> documentation
  -> synthese
  -> reponse JSON
```

Seuls les agents selectionnes sont executes. L'ordre est defini par
`AGENT_ORDER` et la synthese est toujours placee en dernier.

## Agents et outils

| Agent | Outils |
|---|---|
| `surveillance` | recherche de donnees, IAS |
| `tendance` | analyse de serie |
| `territoire` | contexte geographique, meteo |
| `documentation` | recherche RAG locale |
| `synthese` | note de crise |

Chaque outil reutilise la logique d'un skill Codex existant. Le workflow
conserve le plan, la trace, les constats et les sorties d'outils dans son etat.

## Fonctions complementaires

- memoire de conversation par `thread_id` ;
- streaming des mises a jour du graphe ;
- RAG Markdown et PDF ;
- sorties structurees validees par Pydantic ;
- backend Mistral cloud ou Ollama local.
