# Workflow LangGraph multi-agents

Le dossier `src/langchain_epidemio/` ajoute un workflow au-dessus des six skills
existants, avec un routage externe deterministe.

Fonctionnalites :

- cinq agents LangChain specialises : surveillance, tendance, territoire,
  documentation et synthese ;
- graphe `StateGraph` avec planification par regles et ordre d'execution fixe ;
- outils LangChain construits a partir des skills existants et limites au role
  de chaque agent ;
- backends Mistral cloud et Ollama local ;
- sorties structurees validees avec Pydantic ;
- memoire par `thread_id`, trace du workflow et streaming des etapes ;
- RAG sur la documentation locale et chargement de PDF avec `PyPDFLoader`.

Le routage externe est deterministe : le LLM ne choisit ni le prochain agent ni
l'ordre du workflow. Selon la demande, le graphe execute un sous-ensemble de :

```text
surveillance -> tendance -> territoire -> documentation -> synthese
```

La synthese est toujours executee en dernier. Les agents appellent les skills
existants comme outils et leurs resultats restent presents dans le JSON final.

Configurer les variables de `.env.example`, puis utiliser par exemple :

```bash
python -m src.langchain_epidemio.cli "Analyse la tendance 12, 15, 18, 22"
python -m src.langchain_epidemio.cli --interactive --thread-id cellule-1
python -m src.langchain_epidemio.cli --rag-pdf AgentsLangchain.pdf "Qu'est-ce qu'un agent ?"
python -m src.langchain_epidemio.cli --structured "Hausse des syndromes grippaux en France"
```

Chaque agent doit mentionner les sources et limites des donnees et ne fournit
aucun diagnostic medical individuel.
