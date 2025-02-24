# Daily CSS Battle

Chaque jour, publie sur ton channel slack le CSS Battle du jour !

Pour en savoir + : https://cssbattle.dev/

Ce dépôt contient un projet Python conçu pour être exécuté en tant que fonction AWS Lambda. Le projet utilise notamment Selenium, Requests, BeautifulSoup et python-dotenv. Il est également accompagné d'un Dockerfile pour faciliter le déploiement via un conteneur.

## Prérequis

- **Python >3.10** – Pour exécuter le code en local.
- **pip** – Pour installer les dépendances Python.
- (Optionnel) **Virtualenv** – Pour isoler les dépendances du projet.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/thomasperrein/daily-css-battle.git
cd daily-css-battle
```

### 2. Créer et activer un environnement virtuel (optionnel mais recommandé)

- Sous Linux/Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Sous Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer les bibliothèques python

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp -n .env.example .env
```

Puis ajouter votre lien de webhook Slack dans le fichier d'environnement. Pour plus d'informations : https://api.slack.com/messaging/webhooks

### 5. Lancer le script en local

```bash
python main.py
```
