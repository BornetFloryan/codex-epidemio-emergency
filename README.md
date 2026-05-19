# Codex Epidemio Emergency Skills

## Objectif

Ce projet propose un ensemble de **skills Codex** destinés à aider à la **veille épidémiologique en situation d’urgence**.

L’objectif est de fournir des capacités activables à la demande pour :

- rechercher des sources de données sanitaires ;
- analyser des indicateurs épidémiologiques ;
- qualifier une tendance ;
- produire une note de situation synthétique ;
- aider à la décision dans un contexte de crise sanitaire.

Le projet repose sur :

- des **skills** ;
- des scripts **Python CLI testables seuls** ;
- une architecture légère ;
- aucun serveur MCP ;
- aucune application web.

---

# Architecture du projet

```text
codex-epidemio-emergency/
│
├── AGENTS.md
├── README.md
├── requirements.txt
│
├── .codex/
│   └── skills/
│       ├── ias-indicators/
│       │   ├── SKILL.md
│       │   ├── main.py
│       │   └── references/
│       │       └── sources.md
│       │
│       ├── public-health-search/
│       │   ├── SKILL.md
│       │   ├── main.py
│       │   └── references/
│       │       └── api.md
│       │
│       ├── trend-analysis/
│       │   ├── SKILL.md
│       │   ├── main.py
│       │   └── references/
│       │       └── method.md
│       │
│       └── crisis-report/
│           ├── SKILL.md
│           ├── main.py
│           └── references/
│               └── format.md
│
└── tests/
    ├── test_ias_indicators.py
    ├── test_trend_analysis.py
    └── test_crisis_report.py
```

---

# Adaptation à Codex

Le projet suit donc cette structure :

```text
.codex/skills/
```

---

# Installation

## 1. Installer Node.js

Télécharger Node.js :

https://nodejs.org

Vérifier l’installation :

```bash
node -v
npm -v
```

---

## 2. Installer Codex CLI

```bash
npm install -g @openai/codex
```

Vérifier :

```bash
codex --version
```

---

## 3. Connexion Codex

```bash
codex login
```

---

## 4. Cloner le dépôt

```bash
git clone https://github.com/VOTRE-USER/codex-epidemio-emergency.git
cd codex-epidemio-emergency
```

---

## 5. Créer l’environnement Python

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 6. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

---

# Lancer Codex

Depuis la racine du projet :

```bash
codex
```

---

# Skills disponibles

## 1. `ias-indicators`

Analyse ou prépare l’analyse d’indicateurs épidémiologiques publics.

### Test direct du script

```bash
python .codex/skills/ias-indicators/main.py --indicator grippe
```

```bash
python .codex/skills/ias-indicators/main.py --indicator gastro
```

---

## 2. `public-health-search`

Recherche ou présente des sources publiques utiles à la veille sanitaire.

### Test direct du script

```bash
python .codex/skills/public-health-search/main.py "grippe santé publique"
```

---

## 3. `trend-analysis`

Analyse une série temporelle simple afin de détecter :

- hausse ;
- baisse ;
- stabilité.

### Test direct du script

```bash
python .codex/skills/trend-analysis/main.py --sample
```

```bash
python .codex/skills/trend-analysis/main.py --values 12 15 18 22
```

---

## 4. `crisis-report`

Produit une courte note de situation pour une cellule de crise.

### Test direct du script

```bash
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
```

---

# Tests

Lancer tous les tests :

```bash
python -m pytest
```

---

# Déclenchement des skills

Les skills sont activés :

- soit explicitement ;
- soit automatiquement via leur `description`.

Les descriptions contiennent :

- des formulations naturelles ;
- des mots-clés métier ;
- des termes français et anglais ;
- des exemples de requêtes utilisateur.

---

# Contraintes et limites

## Important

Ce projet :

- ne fournit **aucun diagnostic médical** ;
- ne remplace pas une expertise sanitaire officielle ;
- ne doit pas être utilisé seul pour prendre une décision médicale ;
- sert uniquement d’aide à l’organisation et à la synthèse.

Les données doivent toujours être :

- vérifiées ;
- contextualisées ;
- croisées avec des sources officielles.
