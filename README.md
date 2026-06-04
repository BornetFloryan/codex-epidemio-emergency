# Codex Epidemio Emergency

Ce depot contient une adaptation Codex d'un projet de skills pour l'aide a la decision en situation d'urgence sanitaire.

Le theme choisi est la veille epidemiologique : recherche de sources publiques, lecture d'indicateurs sanitaires, qualification rapide d'une tendance et production d'une courte note de situation.

## Objectif

Le projet fournit un ensemble coherent de skills que Codex peut activer selon la demande de l'utilisateur pour :

- rechercher des jeux de donnees sanitaires publics ;
- identifier des sources utiles pour la grippe, la gastro-enterite et la veille epidemiologique ;
- analyser une petite serie temporelle ;
- qualifier une tendance simple : hausse, baisse ou stabilite ;
- produire une synthese operationnelle courte pour une situation sanitaire.

Le projet ne fournit pas de diagnostic medical individuel. Les resultats sont des aides a la veille et doivent toujours etre verifies avec les sources officielles.

## Architecture

```text
.
|-- .codex/
|   `-- skills/
|       |-- crisis-report/
|       |-- geo-zone-context/
|       |-- health-dataset-search/
|       |-- ias-indicators/
|       |-- trend-analysis/
|       `-- weather-alert-context/
|-- data/
|   `-- epidemio_cache.sqlite
|-- src/
|   `-- epidemio_common/
|       |-- api_client.py
|       `-- cache.py
|-- AGENTS.md
|-- README.md
`-- requirements.txt
```

Chaque skill contient :

- un `SKILL.md` court, utilise par Codex pour savoir quand activer le skill ;
- un script Python `main.py`, executable seul en terminal ;
- eventuellement un dossier `references/` pour stocker les details longs sans surcharger le contexte.

Le code commun se trouve dans `src/epidemio_common/`. Il contient notamment le client API et la gestion du cache SQLite.

## Skills disponibles

### `health-dataset-search`

Recherche des jeux de donnees de sante publique via l'API data.gouv.fr.

Exemples d'usage :

```bash
python .codex/skills/health-dataset-search/main.py "grippe sante publique"
python .codex/skills/health-dataset-search/main.py "gastro-enterite surveillance"
```

Sortie attendue : JSON contenant la requete, les variantes utilisees, les jeux de donnees trouves, les organisations, les ressources disponibles, les limites et le statut du cache.

### `ias-indicators`

Recherche des sources liees aux indicateurs avances sanitaires pour deux indicateurs :

- `grippe` ;
- `gastro`.

Exemples d'usage :

```bash
python .codex/skills/ias-indicators/main.py --indicator grippe
python .codex/skills/ias-indicators/main.py --indicator gastro
```

Sortie attendue : JSON contenant l'indicateur, la source API, le jeu de donnees le plus pertinent, les ressources, une interpretation prudente et les limites.

### `trend-analysis`

Analyse une courte serie numerique et qualifie la tendance entre les deux dernieres valeurs.

Exemples d'usage :

```bash
python .codex/skills/trend-analysis/main.py --sample
python .codex/skills/trend-analysis/main.py --values 12 15 18 22
```

Sortie attendue : JSON contenant la derniere valeur, la valeur precedente, l'ecart, la tendance et les limites.

### `crisis-report`

Produit une courte note de situation epidemiologique a partir d'un texte fourni.

Exemple d'usage :

```bash
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
```

Sortie attendue : JSON contenant un resume operationnel, un niveau d'attention, des signaux a surveiller, des actions recommandees, les limites et les sources a verifier.

### `geo-zone-context`

Recherche le contexte geographique d'une commune francaise a partir d'un nom de ville ou d'un code postal.

Exemple d'usage :

```bash
python .codex/skills/geo-zone-context/main.py "Besancon"
```

Sortie attendue : JSON contenant la commune la plus probable, le code INSEE, les codes postaux, le departement, la region, la population, les coordonnees approximatives, les limites et les sources.

### `weather-alert-context`

Fournit un contexte meteo local pour une commune francaise, apres resolution de la commune avec l'API geo.api.gouv.fr.

Exemple d'usage :

```bash
python .codex/skills/weather-alert-context/main.py "Besancon"
```

Sortie attendue : JSON contenant la commune retenue, les coordonnees utilisees, les donnees meteo actuelles disponibles, les signaux operationnels, les limites et les sources.

Ce skill donne un contexte meteo, mais ne remplace pas une vigilance officielle Meteo-France.

## Installation

Creer puis activer un environnement Python :

```bash
python -m venv .venv
```

Sous Windows PowerShell :

```bash
.\.venv\Scripts\Activate.ps1
```

Installer les dependances :

```bash
python -m pip install -r requirements.txt
```

Les skills peuvent ensuite etre appeles directement avec les commandes indiquees plus haut ou etre sollicites naturellement dans une conversation Codex.

## Verification manuelle

Le projet se verifie par des commandes terminal simples, sans serveur et sans framework de test supplementaire :

```bash
python .codex/skills/health-dataset-search/main.py "grippe sante publique"
python .codex/skills/ias-indicators/main.py --indicator grippe
python .codex/skills/ias-indicators/main.py --indicator gastro
python .codex/skills/trend-analysis/main.py --sample
python .codex/skills/trend-analysis/main.py --values 12 15 18 22
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
python .codex/skills/geo-zone-context/main.py "Besancon"
python .codex/skills/weather-alert-context/main.py "Besancon"
```

Pour chaque sortie, verifier que le JSON contient au minimum un `status`, des `limits`, des `sources` ou une `source_api`, et aucune conclusion medicale individuelle.

Exemples de demandes naturelles dans Codex :

- "Trouve des sources de donnees publiques sur la grippe."
- "Analyse cette serie epidemiologique : 12, 15, 18, 22."
- "Fais une courte note de situation : hausse des syndromes grippaux en France."
- "Donne le contexte geographique de Besancon."
- "Donne le contexte meteo operationnel pour Besancon."

## Conformite au support `ProjetsSkills.pdf`

Le projet suit le cadrage du support :

- pas de serveur MCP, pas de framework web et pas de port a exposer ;
- un decoupage en six skills operationnels, chacun centre sur une capacite mobilisable en situation d'urgence ;
- chaque skill contient un `SKILL.md` court, un script CLI Python `main.py` testable seul et, si necessaire, des details dans `references/` ;
- les descriptions utilisent des formulations de declenchement et des mots-cles metier pour faciliter l'auto-routage ;
- les `allowed-tools` sont restreints au script Python propre a chaque skill et a la lecture des fichiers utiles ;
- les contenus longs, exemples, sources et methodes sont externalises hors des `SKILL.md` ;
- les scripts sont verifies manuellement par commandes terminal et par demandes naturelles dans Codex.

Estimation de l'empreinte tokens, calculee approximativement par `caracteres / 4` :

| Skill | Idle, nom + description | Actif, `SKILL.md` |
|---|---:|---:|
| `crisis-report` | ~64 tokens | ~203 tokens |
| `geo-zone-context` | ~60 tokens | ~212 tokens |
| `health-dataset-search` | ~73 tokens | ~218 tokens |
| `ias-indicators` | ~60 tokens | ~231 tokens |
| `trend-analysis` | ~58 tokens | ~209 tokens |
| `weather-alert-context` | ~60 tokens | ~228 tokens |

Ces valeurs restent faibles car les scripts, references et donnees ne sont charges qu'a la demande.

## Cache

Les appels API peuvent etre enregistres dans :

```text
data/epidemio_cache.sqlite
```

Ce cache permet de conserver les resultats utiles et de mieux gerer les cas ou l'API ou le reseau ne repond pas.

## Sources utilisees

Les principales sources prevues ou utilisees sont :

- data.gouv.fr : recherche de jeux de donnees publics ;
- Sante publique France : source officielle a consulter pour la surveillance sanitaire ;
- Reseau Sentinelles : source de reference pour certains indicateurs epidemiologiques ;
- Geodes Sante publique France : portail de donnees sanitaires ;
- geo.api.gouv.fr : contexte geographique des communes francaises ;
- Open-Meteo : contexte meteorologique local ;
- documentation des producteurs de donnees mentionnes dans les resultats.

Les scripts qui interrogent data.gouv.fr utilisent l'endpoint :

```text
GET https://www.data.gouv.fr/api/1/datasets/?q=<requete>&page_size=5
```

## Limites

- Les resultats dependent de l'indexation et de la disponibilite de data.gouv.fr.
- Une absence de resultat ne signifie pas une absence de risque sanitaire.
- Un indicateur isole ne suffit pas a qualifier une situation epidemiologique.
- Les donnees doivent etre croisees avec la periode, la zone geographique, la methode de collecte et les sources officielles.
- Les erreurs reseau sont gerees dans les scripts sans afficher de stacktrace brute.
- Le projet ne remplace pas l'expertise des autorites sanitaires.

## Etat actuel

Le depot contient actuellement six skills fonctionnels :

- `health-dataset-search` ;
- `ias-indicators` ;
- `trend-analysis` ;
- `crisis-report` ;
- `geo-zone-context` ;
- `weather-alert-context`.

## Regles de developpement

- Ne pas creer d'application web.
- Ne pas creer de serveur MCP.
- Garder les `SKILL.md` courts et placer les details longs dans `references/`.
- Les scripts doivent retourner du JSON propre.
- Toujours mentionner les sources et les limites des donnees.
- Ne jamais fournir de diagnostic medical individuel.
