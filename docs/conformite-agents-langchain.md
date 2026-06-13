# Conformite au projet Agents LangChain

## Elements couverts

- plusieurs agents specialises avec responsabilites distinctes ;
- workflow explicite construit avec `StateGraph` ;
- partage d'un etat structure entre les noeuds ;
- routeur par regles et ordre fixe ;
- outils LangChain reutilisant les skills du projet initial ;
- outils limites selon le role de chaque agent ;
- memoire par `thread_id` et streaming des etapes ;
- RAG sur Markdown et PDF ;
- sortie structuree validee avec Pydantic ;
- selection centralisee du backend Mistral ou Ollama ;
- configuration des LLM avec `temperature=0` ;
- tests hors reseau du plan, du graphe, des outils, du RAG et des schemas.

## Securite et prudence

- les sources et limites doivent etre conservees dans les constats ;
- aucun diagnostic medical individuel ne doit etre produit ;
- la synthese ne remplace pas l'expertise des autorites sanitaires ;
- les donnees vivantes et les sorties LLM doivent etre relues.

## Separation des branches

- `main` : projet initial Skills ;
- `codex/langchain-agent` : extension Agents LangChain/LangGraph.
