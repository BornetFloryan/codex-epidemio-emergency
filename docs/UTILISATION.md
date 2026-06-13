# Installer et essayer le projet Skills

Ce guide permet de tester rapidement la branche `main` sous Linux ou Windows.
Toutes les commandes doivent etre lancees depuis la racine du depot.

## 1. Recuperer la bonne branche

```bash
git clone https://github.com/BornetFloryan/codex-epidemio-emergency.git
cd codex-epidemio-emergency
git switch main
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

## 4. Demonstration rapide

Ces commandes sont identiques sous Linux et Windows une fois l'environnement
active :

```bash
python .codex/skills/trend-analysis/main.py --values 12 15 18 22
python .codex/skills/crisis-report/main.py "Hausse des syndromes grippaux en France"
python .codex/skills/geo-zone-context/main.py "Besancon"
python .codex/skills/weather-alert-context/main.py "Besancon"
python .codex/skills/ias-indicators/main.py --indicator grippe
python .codex/skills/health-dataset-search/main.py "grippe sante publique"
```

Chaque commande doit retourner un JSON contenant un `status`, les sources
utilisees et les limites des donnees.

Les commandes geographiques, meteo et sanitaires utilisent internet. En cas de
reseau indisponible, elles doivent retourner un JSON d'erreur lisible sans
stacktrace brute.

## 5. Essayer naturellement dans Codex

Ouvrir Codex depuis la racine du depot, puis essayer :

```text
Trouve des sources publiques sur la grippe.
Analyse la tendance 12, 15, 18, 22.
Fais une note de situation sur une hausse des syndromes grippaux.
Donne le contexte geographique de Besancon.
Donne le contexte meteo operationnel de Besancon.
```

Codex doit selectionner le skill correspondant et restituer une reponse avec
les sources et limites.

## 6. Nettoyage facultatif

Les appels API creent localement `data/epidemio_cache.sqlite`. Ce fichier est
ignore par Git et peut etre supprime sans affecter le projet.
