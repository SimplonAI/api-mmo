from flask_sqlalchemy import SQLAlchemy

# on initialise SQLAlchemy en dehors du fichier __init__.py afin d'éviter des problèmes de dépendances circulaires
db = SQLAlchemy()
