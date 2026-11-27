# Checkpoint C - julyyero

- Étudiante : Julie Yerolymos
- GitHub : julyyero
- Équipe : G01 - Tmahjeur
- Dépôt : `Alex-dmns/esilv-marketpulse-g01-tmhajeur`

## 1. Qu'est-ce que MarketPulse ?

Une application Python qui compare un instrument financier à son benchmark sur la même période.
Elle répond à la question : l'instrument fait-il mieux ou moins bien que le marché ?
Le même résultat (`build_market_snapshot()`) est affiché dans le terminal et dans un dashboard Dash.

## 2. Instrument et benchmark

| | |
|---|---|
| Instrument | AAPL - Apple Inc. |
| Benchmark | SP500 - S&P 500 |
| Période | 1 mois |
| Intervalle | journalier |

## 3. Provider utilisé

```text
Provider    : Bloomberg stage
Access mode : APPROVED_SAMPLE
Source      : data/sample/bloomberg_reference_sample.json
```

APPROVED_SAMPLE est l'échantillon fourni par l'enseignant.
Ce ne sont pas des données Bloomberg en direct, et ce n'est pas une preuve de connexion Bloomberg LIVE.

Deux autres sources restent disponibles, avec les mêmes calculs :

- `build_market_snapshot("yahoo")` : Yahoo Finance via `yfinance` (LIVE, besoin d'internet)
- `build_market_snapshot("csv")` : CSV local `data/sample/prices.csv` (LOCAL_SAMPLE, hors ligne)

## 4. Installation et lancement

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python src/main.py
python src/dashboard.py
```

Le dashboard s'ouvre sur <http://127.0.0.1:8050> (arrêt avec `Ctrl+C`).

Résultat attendu (APPROVED_SAMPLE) :

```text
Instrument return : 6.48%
Benchmark return  : 2.15%
AAPL vs SP500     : +4.33 percentage points
Base 100          : AAPL 100.00 -> 106.48 / SP500 100.00 -> 102.15
```

Le terminal et le dashboard lisent le même snapshot, donc ils affichent les mêmes valeurs.

## 5. Contraintes d'environnement

- Pas de terminal Bloomberg ni d'identifiant : le mode APPROVED_SAMPLE fonctionne hors ligne.
- Yahoo nécessite internet. `yfinance` est une bibliothèque communautaire, pas l'API officielle de Yahoo.
- Les commandes se lancent depuis la racine du dépôt (les chemins `data/sample/` sont relatifs).
- Sur macOS, utiliser `python3` si `python` n'est pas trouvé.

## 6. Preuves

Toutes mes preuves et mes rapports de TD sont dans `rendu_tp/YEROLYMOS_julie/`.

Le rapport de Checkpoint C contient :

- `python src/main.py` sur `main` mergé ;
- le dashboard complet (contexte, 3 indicateurs, graphique base 100) ;
- ma Pull Request #21, mergée dans `main` ;
- le lancement depuis un clone neuf (installation + exécution).

## 7. Reproductibilité

Test réalisé dans un dossier neuf (`marketpulse-repro`), sur macOS :

```bash
git clone https://github.com/Alex-dmns/esilv-marketpulse-g01-tmhajeur.git marketpulse-repro
cd marketpulse-repro
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

L'installation réussit et `python src/main.py` donne les mêmes valeurs que ci-dessus.
Sur macOS (Python Homebrew), un environnement virtuel `.venv` est nécessaire pour installer les dépendances.

## 8. Ma contribution (TD07-TD12)

| Commit / PR | Travail |
|---|---|
| `ecdc36d` (PR #11, mergée) | TD07 - analytics : alignement des dates, rendement, base 100, performance relative |
| `df7f9fa` | TD08 - provider Yahoo Finance |
| `25a18e6` | TD09 - mapping Bloomberg |
| `9176c6a` | TD10 - provider Bloomberg et `build_market_snapshot()` |
| `006ed99` (PR #21, mergée) | TD11 - dashboard limité à la présentation : il lit le snapshot, sans calcul ni appel provider |
| `0cc2b4d` (PR #21, mergée) | TD10 optionnel - choix du provider `csv / yahoo / bloomberg` avec un mode d'accès honnête |
| `aa3ee8b` (PR #21, mergée) | TD12 - suppression des fichiers temporaires (`main2.py`, labs en double) |
| PR #20 | TD12 - review et merge de la PR d'intégration finale d'Hadrien |
