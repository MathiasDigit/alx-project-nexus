#!/bin/bash
echo "🚀 Lancement du déploiement..."

# Appliquer les migrations
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Charger les données existantes (si fixtures)
if [ -f fixtures.json ]; then
    python manage.py loaddata fixtures.json
fi

echo "✅ Déploiement terminé."
