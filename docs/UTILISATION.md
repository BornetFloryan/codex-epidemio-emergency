# Installer et essayer le projet Agents LangChain

Ce guide permet de tester rapidement la branche `codex/langchain-agent` sous
Linux ou Windows. Toutes les commandes doivent etre lancees depuis la racine du
depot.

## 1. Recuperer la bonne branche

```bash
git clone https://github.com/BornetFloryan/codex-epidemio-emergency.git
cd codex-epidemio-emergency
git switch codex/langchain-agent
```

## 2. Installer sous Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Si le module `venv` manque sous Debian ou Ubuntu :

```bash
sudo apt install python3-venv
```

## 3. Installer sous Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloque l'activation :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Verifier sans LLM ni cle API

La suite suivante ne depend pas d'internet :

```bash
python -m pytest tests/test_langchain_offline.py
```

Resultat attendu :

```text
10 passed
```

Verifier directement que la planification est stable :

```bash
python -c "from src.langchain_epidemio.workflow import plan_workflow; print(plan_workflow('Analyse la hausse 12, 15, 18 de la grippe avec la meteo de Besancon'))"
```

Resultat attendu :

```text
['surveillance', 'tendance', 'territoire', 'synthese']
```

## 5. Configurer un LLM

Copier le fichier d'exemple :

Sous Linux :

```bash
cp .env.example .env
```

Sous Windows PowerShell :

```powershell
Copy-Item .env.example .env
```

### Option Mistral

Modifier `.env` :

```text
LLM_BACKEND=mistral
MISTRAL_API_KEY=votre_cle
MISTRAL_MODEL=mistral-small-latest
MISTRAL_EMBED_MODEL=mistral-embed
```

### Option Ollama local

Installer Ollama, puis :

```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text
```

Modifier `.env` :

```text
LLM_BACKEND=ollama
OLLAMA_MODEL=qwen3:4b
OLLAMA_EMBED_MODEL=nomic-embed-text
```

## 6. Demonstration du workflow

```bash
python -m src.langchain_epidemio.cli --stream "Analyse la hausse 12, 15, 18 de la grippe avec la meteo de Besancon"
```

La sortie doit montrer un plan, une trace des agents, les sorties d'outils et
une synthese finale. Le plan suit un ordre fixe et termine par `synthese`.

## 7. Demonstration des fonctions du cours

Conversation avec memoire :

```bash
python -m src.langchain_epidemio.cli --interactive --thread-id cellule-1
```

RAG sur le PDF du cours :

```bash
python -m src.langchain_epidemio.cli --rag-pdf AgentsLangchain.pdf "Qu'est-ce qu'un agent ?"
```

Sortie structuree Pydantic :

```bash
python -m src.langchain_epidemio.cli --structured "Hausse des syndromes grippaux en France"
```

## 8. Points a verifier

- la planification selectionne les agents attendus ;
- la trace suit l'ordre du plan ;
- `synthese` est toujours la derniere etape ;
- les sources et limites sont conservees ;
- aucun diagnostic medical individuel n'est produit.

Les formulations du LLM et les donnees d'API peuvent varier. Le routage externe
et l'ordre du graphe restent deterministes.
