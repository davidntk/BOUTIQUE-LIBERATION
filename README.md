# BOUTIQUE LIBERATION

Application de boutique développée avec Python, Flask, MySQL, HTML, CSS et JavaScript.

## 1. Préparer Windows et VS Code

Installer :
- Python 3.11 ou 3.12 (cocher « Add Python to PATH » pendant l'installation).
- Visual Studio Code.
- XAMPP pour MySQL.

Ouvrir le dossier du projet dans VS Code, puis ouvrir un terminal PowerShell.

## 2. Créer l'environnement Python

Depuis le dossier principal du projet :

```powershell
py -3.12 -m venv .venv
`.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloque l'activation, utiliser cette commande dans le terminal courant, puis réessayer :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
`.venv\Scripts\Activate.ps1
```

Si Python 3.12 n'est pas installé, remplacer `py -3.12` par `py`.

## 3. Préparer MySQL avec XAMPP

1. Ouvrir XAMPP et démarrer **MySQL**.
2. Cliquer sur **Admin** à côté de MySQL pour ouvrir phpMyAdmin.
3. Ouvrir l'onglet **Importer**.
4. Sélectionner `database/schema_mysql.sql`.
5. Lancer l'importation. La base `boutique_liberation` et ses tables seront créées.

Apache n'est pas nécessaire pour exécuter Flask ; il peut seulement être utilisé pour accéder à phpMyAdmin selon votre installation XAMPP.

## 4. Configurer les variables locales

Copier `.env.example` et nommer la copie `.env` à la racine du projet. Adapter les paramètres MySQL si nécessaire.

Valeurs habituelles de XAMPP :
- MYSQL_HOST=127.0.0.1
- MYSQL_PORT=3306
- MYSQL_USER=root
- MYSQL_PASSWORD= (vide par défaut sur une installation XAMPP standard)
- MYSQL_DATABASE=boutique_liberation

Définir aussi une longue valeur secrète personnelle pour `SECRET_KEY`. Ne jamais publier le fichier `.env` ni ses secrets sur GitHub. Le fichier est ignoré par Git.

## 5. Lancer le site en local

Avec l'environnement virtuel activé :

```powershell
python app.py
```

Ouvrir : http://127.0.0.1:5001

Au premier lancement local, le code initialise les tables de données et ajoute les produits de démonstration si le catalogue est vide. Les deux modèles concernés sont configurés ainsi :
- **Sport Runner** : paire blanche.
- **Sneakers Urban** : paire bleu marine, modèle différent.

Les images sont référencées dans `app.py` par nom de produit, aussi bien pour l'initialisation locale que pour l'affichage du catalogue.

## 6. Déploiement sur Render

Dans les paramètres du service Render :

**Build Command**
```bash
pip install -r requirements.txt
```

**Start Command**
```bash
gunicorn app:app
```

Ajouter dans **Environment** les variables suivantes avec les valeurs de votre hébergeur MySQL :
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `SECRET_KEY` (valeur longue, aléatoire et privée)

Ne mettez pas les identifiants de la base de production dans le dépôt GitHub. La base MySQL de Render doit être créée et accessible depuis le service web.

**Important :** l'initialisation `init_db()` est lancée par `python app.py` en local, mais pas par la commande Gunicorn. Pour cette raison, les images des deux modèles sont également appliquées au moment de l'affichage du catalogue. Le schéma SQL doit être importé dans la base de production et les produits doivent déjà exister.

## 7. Dépannage rapide

- `ModuleNotFoundError` : vérifier que `.venv` est activé puis exécuter `pip install -r requirements.txt`.
- Erreur de connexion MySQL : vérifier que MySQL est démarré et contrôler les variables dans `.env`.
- Port MySQL différent : modifier `MYSQL_PORT`.
- Images non actualisées dans le navigateur : faire **Ctrl + F5** après le redéploiement.
- Les données locales et celles de Render sont deux bases différentes : une modification sur l'une ne modifie pas automatiquement l'autre.

## Sécurité

L'accès administrateur de cette version est actuellement sans authentification par mot de passe. Ne pas utiliser cette configuration pour une boutique publique avec des données réelles avant d'avoir rétabli une authentification sécurisée.
