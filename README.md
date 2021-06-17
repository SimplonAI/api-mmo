# App Agence Immobilière - Estimation de prix

Notre application se base sur le dataset Housing California de 1990.

# Prérequis
* Python 3.9
* PostgreSQL
ou
* Docker

# Installation
```shell
git clone https://github.com/SimplonAI/api-mmo
cd api-mmo
python -m venv venv
```
Sur Windows exécutez :
```shell
venv/Scripts/activate
```
ou sur Linux :
```shell
venv/bin/activate
```
Ensuite finir par :
```
pip install requirements.txt
flask init-db
```

# Configuration
Ouvrir le fichier `exemple_config.json` et remplacer les valeurs par défaut par celle de votre environnement. Copier ensuite ce fichier dans un dossier instance et le renommer config.json.
```shell
mkdir instance
cp exemple_config.json instance/config.json
```

# Exécution
Pour lancer l'app, vous devrez taper la commande :
```shell
flask run
```
