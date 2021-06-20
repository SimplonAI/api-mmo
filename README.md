# App Agence Immobilière - Estimation de prix
[![Build Status](https://travis-ci.com/SimplonAI/api-mmo.svg?token=54ssNXAp4tdWQ5mk1zsT&branch=main)](https://travis-ci.com/SimplonAI/api-mmo)

Notre application se base sur le dataset Housing California de 1990.

# Prérequis
* Python 3.9
* PostgreSQL
ou
* Docker
    * Suivre seulement l'étape Docker

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
pip install -r requirements.txt
```

# Configuration
Ouvrir le fichier `exemple_config.json` et remplacer les valeurs par défaut par celle de votre environnement. Copier ensuite ce fichier dans un dossier instance et le renommer config.json.
```shell
mkdir instance
cp exemple_config.json instance/config.json
```
Ensuite exécuter les commandes de configuration pour la BDD:
```shell
flask db upgrade
flask insert-db
```

# Créer un utilisateur
Afin d'utiliser l'app, vous allez devoir vous connecter avec un utilisateur. Pour le créer :
```shell
flask create-db
```

# Exécution
Pour lancer l'app, vous devrez taper la commande :
```shell
flask run
```

# Docker
Si vous voulez vous éviter toutes les instructions précédentes, il est conseillé d'utiliser Docker.
1. Il faut configurer les variables environnements de Postgres dans un fichier .env à placer à la racine de l'application (renommer le fichier `.env.exemple` en `.env` suffit amplement) :
```shell
cp .env.exemple .env
```
2. Construire et exécuter l'image docker :
```shell
docker-compose up -d
```
