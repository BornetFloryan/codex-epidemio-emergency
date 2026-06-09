# Codex Epidemio Emergency - Version LangChain

Cette branche contient la variante **LangChain** du projet de veille epidemiologique en situation d'urgence.

Elle conserve les six skills Codex du projet original et ajoute un agent LangChain capable de choisir et d'enchainer automatiquement ces capacites selon la demande de l'utilisateur.

> La branche `main` contient volontairement la version sans LangChain. Cette branche `codex/langchain-agent` doit rester separee et ne pas etre fusionnee dans `main`.

## Objectif

Fournir un assistant de veille epidemiologique capable de :

- rechercher des sources et jeux de donnees sanitaires publics ;
- consulter des indicateurs lies a la grippe et a la gastro-enterite ;
- analyser une tendance numerique ;
- contextualiser une commune et sa situation meteorologique ;
- produire une courte note de situation ;
- rechercher des informations dans la documentation locale ou un PDF ;
- orchestrer automatiquement plusieurs outils avec un LLM.

Le projet ne fournit aucun diagnostic medical individuel. Les resultats doivent toujours etre verifies avec les sources officielles et accompagnes de leurs limites.

## Architecture

```text
.
|-- .codex/
|   `-- skills/                     # Six skills Codex utilisables seuls
|-- src/
|   |-- epidemio_common/            # Client API et cache SQLite
|   `-- langchain_epidemio/
|       |-- agent.py                # Agent create_agent, memoire et streaming
|       |-- backends.py             # Selection Mistral ou Ollama
|       |-- cli.py                  # Interface en ligne de commande
|       |-- models.py               # Schemas Pydantic
|       |-- rag.py                  # RAG Markdown et PDF
|       |-- structured.py           # Chaine de sortie structuree
|       `-- tools.py                # Skills exposes comme outils LangChain
|-- tests/
|   `-- test_langchain_offline.py
|-- .env.example
|-- LANGCHAIN.md
`-- requirements.txt
```

## Fonctionnement

```text
Question utilisateur
        |
        v
Agent LangChain
        |
        v
Choix et enchainement des outils
        |
        +-- recherche de donnees sanitaires
        +-- indicateurs IAS
        +-- analyse de tendance
        +-- contexte geographique
        +-- contexte meteorologique
        +-- note de crise
        `-- recherche RAG dans la documentation
        |
        v
Reponse operationnelle avec sources et limites
```

L'agent utilise `create_agent` et dispose :

- d'un message systeme imposant les regles sanitaires du projet ;
- d'une limite de recursion pour eviter les boucles ;
- d'une memoire multi-tour basee sur un `thread_id` ;
- d'un mode streaming pour afficher sa trajectoire ;
- d'un RAG optionnel sur les fichiers Markdown ou PDF ;
- d'une sortie structuree validee par Pydantic.

## Skills exposes comme outils

| Outil LangChain | Skill reutilise | Role |
|---|---|---|
| `rechercher_donnees_sanitaires` | `health-dataset-search` | Recherche sur data.gouv.fr |
| `consulter_indicateur_ias` | `ias-indicators` | Sources grippe ou gastro |
| `analyser_tendance` | `trend-analysis` | Qualification hausse, baisse ou stabilite |
| `contexte_geographique` | `geo-zone-context` | Informations sur une commune francaise |
| `contexte_meteorologique` | `weather-alert-context` | Contexte meteo local |
| `produire_note_de_crise` | `crisis-report` | Synthese operationnelle courte |

Les scripts des skills restent executables directement, sans passer par LangChain.

## Installation

Creer et activer un environnement Python :

```bash
python -m venv .venv
```

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les dependances :

```bash
python -m pip install -r requirements.txt
```

## Configuration du LLM

Creer un fichier `.env` a partir de `.env.example`.

### Mistral cloud

```text
LLM_BACKEND=mistral
MISTRAL_API_KEY=votre_cle
MISTRAL_MODEL=mistral-small-latest
MISTRAL_EMBED_MODEL=mistral-embed
```

### Ollama local

Installer les modeles :

```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text
```

Configurer `.env` :

```text
LLM_BACKEND=ollama
OLLAMA_MODEL=qwen3:4b
OLLAMA_EMBED_MODEL=nomic-embed-text
```

Le meme backend d'embeddings doit etre utilise pour indexer et interroger le RAG.

## Utilisation

### Question simple avec choix automatique des outils

```bash
python -m src.langchain_epidemio.cli "Analyse la tendance 12, 15, 18, 22"
```

### Conversation avec memoire

```bash
python -m src.langchain_epidemio.cli --interactive --thread-id cellule-1
```

### Affichage de la trajectoire de l'agent

```bash
python -m src.langchain_epidemio.cli --stream "Donne le contexte meteo de Besancon"
```

### RAG sur la documentation du projet

```bash
python -m src.langchain_epidemio.cli --rag "Quelles sont les limites de l'analyse de tendance ?"
```

### RAG sur un PDF

```bash
python -m src.langchain_epidemio.cli --rag-pdf AgentsLangchain.pdf "Qu'est-ce qu'un agent ?"
```

### Sortie structuree Pydantic

```bash
python -m src.langchain_epidemio.cli --structured "Hausse des syndromes grippaux en France"
```

## RAG

Le RAG local suit le pipeline presente dans le cours :

```text
Documents -> decoupage en chunks -> embeddings -> InMemoryVectorStore -> recherche
```

Sans option particuliere, il peut indexer :

- `README.md` et `AGENTS.md` ;
- les `SKILL.md` ;
- les fichiers Markdown des dossiers `references/`.

L'option `--rag-pdf` utilise `PyPDFLoader` pour indexer un ou plusieurs PDF.

## Tests

Les tests LangChain restent independants d'internet :

```bash
python -m pytest tests/test_langchain_offline.py
```

Ils verifient notamment :

- l'utilisation des skills comme outils LangChain ;
- la validation des sorties Pydantic ;
- le decoupage et les metadonnees du RAG ;
- le chargement d'un PDF ;
- la construction du graphe de l'agent sans appel reseau.

Un appel reel de l'agent necessite cependant une cle Mistral valide ou un serveur Ollama actif.

## Sources et limites

Sources principales utilisees ou recommandees :

- data.gouv.fr ;
- Sante publique France ;
- Reseau Sentinelles ;
- Geodes ;
- geo.api.gouv.fr ;
- Open-Meteo.

Limites obligatoires :

- un indicateur isole ne suffit pas a caracteriser une situation epidemiologique ;
- une absence de resultat ne signifie pas une absence de risque ;
- les informations doivent etre croisees avec la periode, la zone et la methode de collecte ;
- le RAG ne garantit pas que les passages retrouves soient suffisants ou a jour ;
- l'agent ne remplace pas l'expertise des autorites sanitaires ;
- aucun diagnostic medical individuel ne doit etre produit.

## Separation des branches

- `main` : version originale basee uniquement sur les skills Codex ;
- `codex/langchain-agent` : version etendue avec agent LangChain, memoire, streaming, sorties structurees et RAG.

Cette separation permet de comparer clairement l'approche skills seule avec l'orchestration LangChain.
