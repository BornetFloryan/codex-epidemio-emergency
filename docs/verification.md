# Verification de la branche LangChain

## Planification deterministe

```bash
python -c "from src.langchain_epidemio.workflow import plan_workflow; print(plan_workflow('Analyse la hausse 12, 15, 18 de la grippe avec la meteo de Besancon'))"
```

Resultat attendu :

```text
['surveillance', 'tendance', 'territoire', 'synthese']
```

Relancer plusieurs fois doit produire le meme plan.

## Tests hors reseau

```bash
python -m pytest tests/test_langchain_offline.py
```

Ils verifient notamment le plan, la construction du graphe, les outils, les
schemas Pydantic et le chargement documentaire.

## Execution du workflow

Avec Mistral ou Ollama configure :

```bash
python -m src.langchain_epidemio.cli --stream "Analyse la hausse 12, 15, 18 de la grippe avec la meteo de Besancon"
```

Verifier :

- le plan et la trace suivent le meme ordre ;
- la synthese est executee en dernier ;
- les sorties d'outils restent presentes ;
- les sources et limites sont mentionnees ;
- aucun diagnostic medical individuel n'est produit.

## RAG et sortie structuree

```bash
python -m src.langchain_epidemio.cli --rag-pdf AgentsLangchain.pdf "Qu'est-ce qu'un agent ?"
python -m src.langchain_epidemio.cli --structured "Hausse des syndromes grippaux en France"
```

Le premier appel doit restituer des passages avec leur source. Le second doit
respecter le schema `SituationAssessment`.
