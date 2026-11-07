# Product Backlog — Gestion de stock d'une boutique de chaussures

## 1. Présentation du projet

Le projet consiste à développer une application informatique pour gérer le stock d'une boutique qui vend des chaussures pour hommes et femmes. L'application doit faciliter l'enregistrement des produits, le suivi des entrées et sorties, la gestion des ventes et la consultation des quantités disponibles.

## 2. Objectif général

Mettre en place une application qui améliore la gestion quotidienne du stock, limite les erreurs de suivi et aide le responsable à prendre des décisions de réapprovisionnement.

## 3. Product Backlog

| ID | Fonctionnalité / User Story | Description | Priorité |
|---|---|---|---|
| US01 | Authentification | En tant qu'utilisateur, je veux me connecter afin d'accéder à l'application de manière sécurisée. | Haute |
| US02 | Gestion des utilisateurs | En tant qu'administrateur, je veux ajouter, modifier et désactiver les comptes des utilisateurs. | Moyenne |
| US03 | Ajouter un produit | En tant que responsable, je veux enregistrer une nouvelle chaussure avec ses informations. | Haute |
| US04 | Modifier un produit | En tant que responsable, je veux modifier les informations d'une chaussure. | Haute |
| US05 | Supprimer un produit | En tant que responsable, je veux retirer du catalogue un produit qui n'est plus commercialisé. | Moyenne |
| US06 | Consulter les produits | En tant qu'utilisateur, je veux consulter la liste des chaussures enregistrées. | Haute |
| US07 | Gérer les catégories | En tant que responsable, je veux classer les chaussures par catégorie, notamment homme et femme. | Haute |
| US08 | Gérer les pointures | En tant que responsable, je veux enregistrer les pointures disponibles pour chaque modèle. | Haute |
| US09 | Enregistrer les entrées de stock | En tant que responsable, je veux enregistrer les nouvelles marchandises reçues. | Haute |
| US10 | Enregistrer les sorties de stock | En tant que responsable, je veux enregistrer les sorties de marchandises et leur motif. | Haute |
| US11 | Consulter le stock | En tant que responsable, je veux connaître la quantité disponible pour chaque modèle et chaque pointure. | Haute |
| US12 | Gérer les ventes | En tant que vendeur, je veux enregistrer les ventes effectuées. | Haute |
| US13 | Actualiser automatiquement le stock | En tant que responsable, je veux que le stock soit diminué automatiquement après chaque vente validée. | Haute |
| US14 | Gérer les fournisseurs | En tant que responsable, je veux enregistrer et consulter les informations des fournisseurs. | Moyenne |
| US15 | Alerte de stock faible | En tant que responsable, je veux être averti lorsqu'un produit atteint un seuil minimal. | Moyenne |
| US16 | Générer une facture | En tant que vendeur, je veux générer une facture après une vente. | Moyenne |
| US17 | Consulter les rapports | En tant que responsable, je veux consulter les rapports des ventes et de l'état du stock. | Moyenne |
| US18 | Rechercher un produit | En tant qu'utilisateur, je veux rechercher une chaussure par nom, catégorie, modèle ou pointure. | Haute |

## 4. Classement par priorité

### Priorité haute — fonctionnalités essentielles
- Authentification.
- Ajout, modification et consultation des produits.
- Gestion des catégories et des pointures.
- Enregistrement des entrées et sorties de stock.
- Consultation des quantités disponibles.
- Enregistrement des ventes.
- Mise à jour automatique du stock.
- Recherche de produits.

### Priorité moyenne — fonctionnalités importantes
- Gestion des utilisateurs.
- Suppression ou archivage des produits.
- Gestion des fournisseurs.
- Alertes de stock faible.
- Génération des factures.
- Consultation des rapports.

## 5. Proposition de découpage en Sprints

| Sprint | Travaux prévus |
|---|---|
| Sprint 1 | Analyse détaillée, conception de la base de données et authentification. |
| Sprint 2 | Gestion des produits, catégories, modèles et pointures. |
| Sprint 3 | Gestion des entrées, sorties et consultation du stock. |
| Sprint 4 | Gestion des ventes et actualisation automatique du stock. |
| Sprint 5 | Fournisseurs, alertes, factures, rapports, tests et déploiement. |

## 6. Résultat attendu

À la fin du projet, l'application devra permettre de gérer les chaussures pour hommes et femmes, de connaître les quantités disponibles par modèle et pointure, d'enregistrer les approvisionnements et les ventes, de suivre les mouvements du stock et d'identifier les produits à réapprovisionner.

## 7. Remarque

Ce Product Backlog est une première base de travail. Il pourra être ajusté et complété après validation des besoins réels de la boutique avec les utilisateurs.

## 8. Design - Boutique Liberation - Par Ingenieur Ova, Designer

### A. Ecran d'accueil / Catalogue Client
- Top Bar : Logo a gauche, Barre de recherche, Panier avec badge rouge
- Filtres : Tous, Homme, Femme, Sport, Cuir
- Grille Produits : Photo, Nom, Couleur, Prix en $, Badge Plus que 2 ou Epuise, Bouton Ajouter avec Pointure

### B. Panier et Commande
- Tableau : Modele, Pointure, Prix, Bouton Retirer
- Paiement : Nom, Numero de telephone, Airtel Money, Orange Money, M-Pesa, Paiement a la livraison
- Bouton : Valider le paiement

### C. Espace Administrateur - Dashboard
- KPI : Ventes du jour, Chiffre d'affaires, Benefice net, Total en stock
- Alerte rouge si stock inferieur ou egal a 2

### D. Gestion des Produits et Stocks
- Formulaire : Nom, Categorie, Prix d'achat, Prix de vente, Pointure, Quantite, Photo
- Tableau par pointure : Exemple T40 : 3, T41 : 0 barre si epuise




