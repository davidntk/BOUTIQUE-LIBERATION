# BOUTIQUE LIBERATION

Application de gestion d'une boutique de chaussures développée avec **Python, Flask, MySQL, HTML, CSS et JavaScript**.

## Fonctionnalités
- Catalogue public et recherche de chaussures.
- Espace administrateur.
- Gestion des produits et des prix.
- Gestion du stock par pointure.
- Historique des entrées et sorties.
- Ventes, commandes et mise à jour automatique du stock.
- Factures imprimables et tableau de bord.

## Installation locale avec XAMPP et MySQL

### 1. Démarrer MySQL
1. Installer XAMPP.
2. Ouvrir le panneau de contrôle XAMPP.
3. Démarrer **MySQL** (Apache est facultatif pour Flask).
4. Ouvrir phpMyAdmin depuis le bouton Admin de MySQL.

### 2. Créer les tables
1. Dans phpMyAdmin, ouvrir l'onglet **Importer**.
2. Sélectionner le fichier `database/schema_mysql.sql` du projet.
3. Cliquer sur **Importer / Exécuter**.
4. Une base nommée `boutique_liberation` et toutes les tables seront créées.

### 3. Installer et démarrer Flask
Dans PowerShell, depuis le dossier du projet :

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Ouvrir ensuite **http://127.0.0.1:5001**.

Au premier démarrage, l'application crée automatiquement un compte de démonstration et quatre produits d'exemple si la table des produits est vide.

## Paramètres MySQL

Par défaut, l'application utilise les paramètres XAMPP habituels :
- Hôte : `127.0.0.1`
- Port : `3306`
- Utilisateur : `root`
- Mot de passe : vide
- Base : `boutique_liberation`

Si votre installation utilise d'autres paramètres, définissez les variables d'environnement avant de lancer Flask :

```powershell
$env:MYSQL_HOST="127.0.0.1"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="votre_mot_de_passe"
$env:MYSQL_DATABASE="boutique_liberation"
python app.py
```

Ne publiez jamais votre mot de passe MySQL sur GitHub.

## Connexion administrateur de démonstration
- Identifiant : `admin`
- Mot de passe : `admin123`

Changez ce mot de passe avant une utilisation réelle. Cette version utilise encore une authentification de démonstration simple.

## Sauvegarde
Dans phpMyAdmin, sélectionnez la base `boutique_liberation`, ouvrez **Exporter**, puis exportez-la en SQL. Les données MySQL restent sur votre ordinateur et ne sont pas enregistrées dans le dépôt GitHub.

## Structure de la base
Le script `database/schema_mysql.sql` crée les tables `users`, `products`, `stock`, `movements`, `sales`, `sale_items` et `suppliers`.
