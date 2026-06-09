# Agent LangChain epidemiologique

Le dossier `src/langchain_epidemio/` ajoute une couche LangChain au-dessus des six skills existants.

Fonctionnalites :

- outils LangChain construits a partir des skills existants ;
- agent `create_agent` avec consignes sanitaires et limite de recursion ;
- backends Mistral cloud et Ollama local ;
- sorties structurees validees avec Pydantic ;
- memoire multi-tour par `thread_id` et streaming ;
- RAG sur la documentation locale et chargement de PDF avec `PyPDFLoader`.

Configurer les variables de `.env.example`, puis utiliser par exemple :

```bash
python -m src.langchain_epidemio.cli "Analyse la tendance 12, 15, 18, 22"
python -m src.langchain_epidemio.cli --interactive --thread-id cellule-1
python -m src.langchain_epidemio.cli --rag-pdf AgentsLangchain.pdf "Qu'est-ce qu'un agent ?"
python -m src.langchain_epidemio.cli --structured "Hausse des syndromes grippaux en France"
```

L'agent doit toujours mentionner les sources et limites des donnees et ne fournit aucun diagnostic medical individuel.
