# LGDA-CMCI V2.1
**Logiciel de Gestion du Disciple au sein de l'Assemblée – CMCI**

Application web Django multi-assemblée et multi-utilisateur.

---

## Installation locale (développement)

```bash
# 1. Cloner / décompresser le projet
cd lgda_cmci

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env : renseigner SECRET_KEY au minimum

# 5. Créer la base de données
python manage.py migrate

# 6. Créer le Super Administrateur par défaut
python manage.py init_super_admin

# 7. Lancer le serveur
python manage.py runserver
```

Accéder à : http://127.0.0.1:8000

**Identifiants par défaut du Super Administrateur N°1 :**
- Login : `LGDA-CMCI`
- Mot de passe : `Administrateur` *(changement obligatoire à la première connexion)*

---

## Déploiement cloud (VPS / Heroku)

### Variables d'environnement requises

```
SECRET_KEY=<clé longue et aléatoire>
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=postgres://user:password@host:5432/lgda_cmci
```

### Procédure sur VPS (Ubuntu)

```bash
# Installer les dépendances système
sudo apt update && sudo apt install python3-pip python3-venv postgresql nginx -y

# Base de données PostgreSQL
sudo -u postgres createdb lgda_cmci
sudo -u postgres createuser lgda_user --pwprompt

# Application
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py init_super_admin

# Serveur de production avec Gunicorn
gunicorn lgda_cmci.wsgi:application --bind 0.0.0.0:8000
```

---

## Structure du projet

```
lgda_cmci/
├── accounts/          Utilisateurs & authentification (4 rôles)
├── core/              Pays, Ville, Zone, Sous-centre, Assemblée
├── disciples/         Fiche Disciple, amis, familles, assiduité
├── evangelisation/    Évangéliste, Planning d'évangélisation
├── rapports/          Listes & rapports exportables (PDF/Excel/Word)
├── templates/         Templates HTML Bootstrap 5
└── lgda_cmci/         Configuration Django
```

---

## Rôles et habilitations

| Rôle | Login par défaut | Lecture | Écriture |
|------|-----------------|---------|----------|
| **Super Administrateur** (max 5) | `LGDA-CMCI` | Tous les modules | Pays, Ville, Zone, Sous-centre, Assemblée, Évangéliste |
| **Dirigeant** | `Dirigeant` | Son assemblée & rapports | Aucune |
| **Gestionnaire** | Nom assemblée (ex: `ChezLesASSOHOU`) | Son assemblée & rapports | Disciple, Planning, Assiduité |
| **Évangéliste** | `Evangeliste` | Tous les modules & rapports | Aucune |

---

## Fonctionnalités clés

- **Matricule automatique** : A001, A002… pour les disciples ; A, B, C… pour les assemblées
- **Détection de conflits** : alerte si un évangéliste a déjà un RDV au même créneau
- **Changement de mot de passe obligatoire** à la première connexion
- **Rapports exportables** en PDF, Excel et Word avec filtres temps/périmètre
- **Interface responsive** Bootstrap 5 avec sidebar de navigation par rôle
