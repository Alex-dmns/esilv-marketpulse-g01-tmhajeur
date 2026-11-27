# Checkpoint C - Alex-dmns

- Étudiant : Alexandre Damianos
- GitHub : Alex-dmns
- Équipe : G01 - Tmahjeur
- Dépôt : `Alex-dmns/esilv-marketpulse-g01-tmhajeur`

## 1. Qu'est-ce que MarketPulse ?

Une application Python qui compare un instrument financier à son benchmark sur la même période.
Elle répond à la question : l'instrument fait-il mieux ou moins bien que le marché ?
Le résultat est affiché dans le terminal et dans un dashboard Dash.

## 2. Quel est l'instrument ?

AAPL - Apple Inc.

## 3. Quel est le benchmark ?

SP500 - S&P 500

Période : 1 mois. Intervalle : journalier.

## 4. Quel provider ou mode est utilisé ?

```text
Provider    : Bloomberg stage
Access mode : APPROVED_SAMPLE
Source      : data/sample/bloomberg_reference_sample.json
```

APPROVED_SAMPLE est l'échantillon approuvé par l'enseignant.
Ce ne sont pas des données Bloomberg en direct, et ce n'est pas une preuve de connexion Bloomberg LIVE.

Yahoo Finance (`build_market_snapshot("yahoo")`) et le CSV local (`build_market_snapshot("csv")`) restent disponibles.

## 5. Comment installer les dépendances ?

```bash
git clone https://github.com/Alex-dmns/esilv-marketpulse-g01-tmhajeur.git
cd esilv-marketpulse-g01-tmhajeur
python -m pip install -r requirements.txt
```

Dépendances directes : `yfinance`, `dash`, `plotly`.

## 6. Comment lancer le terminal ?

```bash
python src/main.py
```

Résultat avec APPROVED_SAMPLE :

```text
Instrument return : 6.48%
Benchmark return  : 2.15%
AAPL vs SP500     : +4.33 percentage points
Base 100          : AAPL 100.00 -> 106.48 / SP500 100.00 -> 102.15
```

## 7. Comment lancer le dashboard ?

```bash
python src/dashboard.py
```

Puis ouvrir <http://127.0.0.1:8050>. Arrêter avec `Ctrl+C`.

Le dashboard affiche le provider, l'instrument, le benchmark, la période, l'intervalle, les trois indicateurs et le graphique base 100.
Il lit le même snapshot que le terminal (`build_market_snapshot()`), donc les valeurs sont identiques.

## 8. Quelles contraintes d'environnement ?

- Pas d'accès à un terminal Bloomberg : le mode APPROVED_SAMPLE fonctionne hors ligne, sans identifiant.
- Le chemin Yahoo nécessite internet. `yfinance` est une bibliothèque communautaire, pas l'API officielle de Yahoo.
- Les commandes se lancent depuis la racine du dépôt. Sous Windows : `python` (ou `py`) ; sous Linux / macOS : parfois `python3`.

## 9. Où sont les preuves ?

| Fichier | Contenu |
|---|---|
| `01_final_market_data.png` | `python src/main.py` sur `main` mergé |
| `02_dash_dashboard.png` | le dashboard complet |
| `03_final_pull_request.png` | ma Pull Request TD09-TD12 |
| `04_reproducible_run.png` | clone neuf + installation + lancement |

Rapports de TD : `rendu_tp/DAMIANOS_Alexandre/`.

## Reproductibilité

Test réalisé dans un environnement virtuel Python neuf :
`pip install -r requirements.txt` a réussi (dash 4.5.1, plotly 7.2.0, yfinance 1.8.0),
puis `python src/main.py` et `python src/dashboard.py` ont fonctionné avec les mêmes valeurs.

## Ma contribution (TD07-TD12)

| Commit | Travail |
|---|---|
| `395151c` | TD07 - analytics réutilisables (alignement, rendement, base 100, performance relative) |
| `d3a2160` | TD08 - provider Yahoo Finance |
| `54cc127`, `325434d` | TD09 - mapping Bloomberg |
| `5928e58` | TD10 - provider Bloomberg et `build_market_snapshot()` |
| `c1fc0eb` | TD11 - dashboard Dash |
| `b3db7d5` | TD12 - nettoyage, README, settings, correctifs de release |

Pull Request mergée : #12 (`Alexandre-Damianos` -> `main`, TD08 à TD11).
