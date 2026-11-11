# Plan de développement — BOUTIQUE LIBERATION

> Document de planification établi à partir de `PRODUCT_BACKLOG.md` et des tickets GitHub existants.
> Branche de référence : `main` — Date : 11 novembre 2026.

## 1. Présentation du projet

BOUTIQUE LIBERATION est une application de gestion et de vente de chaussures pour hommes et femmes. Elle doit permettre de gérer le catalogue, les catégories, les pointures, les stocks, les ventes, les commandes et le suivi de l'activité de la boutique.

Le plan conserve le découpage en cinq sprints du Product Backlog. Il précise l'ordre de réalisation, les dépendances, les livrables et les critères de validation.

## 2. Objectifs

- Centraliser les informations sur les produits, les pointures et les quantités.
- Sécuriser l'accès à l'espace d'administration.
- Permettre aux clients de consulter le catalogue et de préparer une commande.
- Assurer la cohérence des stocks lors des mouvements et des ventes.
- Fournir au responsable des indicateurs fiables sur les ventes et les stocks.
- Tester et documenter l'application avant sa mise en service.

## 3. Périmètre fonctionnel

| Domaine | Fonctionnalités | User Stories |
|---|---|---|
| Accès | Authentification, gestion des utilisateurs | US01, US02 |
| Catalogue | Ajouter, modifier, archiver et consulter les produits ; catégories ; recherche | US03, US04, US05, US06, US07, US18 |
| Variantes | Gestion des pointures par modèle | US08 |
| Stock | Entrées, sorties, consultation et mise à jour des quantités | US09, US10, US11, US13 |
| Vente | Enregistrement des ventes | US12 |
| Approvisionnement | Fournisseurs et alertes de stock faible | US14, US15 |
| Documents et pilotage | Factures et rapports | US16, US17 |

## 4. Planification des sprints

### Sprint 1 — Fondations techniques et sécurité

**Objectif :** établir une base applicative stable et sécurisée.

Travaux :
1. Vérifier et documenter la structure frontend/backend.
2. Configurer l'environnement Flask et les dépendances.
3. Préparer les paramètres d'exécution et les variables d'environnement.
4. Concevoir et initialiser la base de données.
5. Définir les relations entre utilisateurs, produits, catégories, pointures, stocks, clients, commandes et lignes de commande.
6. Développer la connexion et la déconnexion de l'administrateur.
7. Protéger les routes d'administration et stocker les mots de passe sous forme hachée.
8. Rédiger les instructions d'installation et de lancement.

**User Stories :** US01. Préparation technique des autres stories.

**Tickets associés :** #1, #2, #7.

**Livrables :** application initialisée, schéma de base de données, authentification opérationnelle et documentation de démarrage.

**Critères de validation :**
- L'application démarre selon les instructions documentées.
- Les tables et relations nécessaires sont créées.
- Un utilisateur non authentifié ne peut pas accéder aux fonctions d'administration.
- Les mots de passe ne sont pas stockés en clair.

### Sprint 2 — Catalogue, produits et pointures

**Objectif :** rendre le catalogue consultable et administrable.

Travaux :
1. Développer l'accueil et l'en-tête du catalogue.
2. Afficher les produits depuis la base de données.
3. Ajouter les catégories Tous, Homme, Femme, Sport et Cuir.
4. Développer l'ajout et la modification d'un produit.
5. Gérer les photos, le nom, la couleur, la description et les prix d'achat et de vente.
6. Gérer les pointures et leur disponibilité par modèle.
7. Ajouter la recherche et les filtres.
8. Prévoir l'archivage des produits qui ne sont plus commercialisés.
9. Préparer la sélection d'une pointure disponible pour le panier.

**User Stories :** US03, US04, US05, US06, US07, US08, US18.

**Tickets associés :** #3, #10, avec préparation du #4.

**Livrables :** catalogue dynamique, interface d'administration des produits et gestion des pointures.

**Critères de validation :**
- Les produits affichés proviennent de la base de données.
- La recherche et les filtres retournent les résultats attendus.
- Les modifications sont enregistrées et visibles dans le catalogue.
- Une pointure indisponible est clairement signalée et ne peut pas être ajoutée au panier.

### Sprint 3 — Gestion et contrôle des stocks

**Objectif :** assurer le suivi fiable des quantités par produit et par pointure.

Travaux :
1. Créer l'enregistrement des entrées de marchandises.
2. Créer l'enregistrement des sorties avec leur motif.
3. Afficher le stock disponible pour chaque modèle et chaque pointure.
4. Permettre les corrections de stock autorisées.
5. Conserver un historique des mouvements.
6. Définir le seuil critique par défaut à deux unités.
7. Afficher les alertes pour les pointures dont le stock atteint ou passe sous le seuil.
8. Vérifier que les quantités ne deviennent pas négatives.

**User Stories :** US09, US10, US11, US15.

**Tickets associés :** #9, #11.

**Livrables :** module de stock, historique des mouvements et alertes de stock faible.

**Critères de validation :**
- Chaque mouvement est enregistré avec une date, une quantité et un motif/type.
- Le stock est consultable par produit et pointure.
- Une quantité négative est impossible.
- Les alertes disparaissent ou sont actualisées après réapprovisionnement.

### Sprint 4 — Panier, commandes et ventes

**Objectif :** permettre la préparation et l'enregistrement des commandes sans incohérence de stock.

Travaux :
1. Ajouter au panier un produit, une pointure et une quantité.
2. Afficher les lignes du panier et leurs prix.
3. Permettre de modifier les quantités ou retirer une ligne.
4. Recalculer les sous-totaux et le total après chaque modification.
5. Recueillir les coordonnées nécessaires du client.
6. Proposer Airtel Money, Orange Money, M-Pesa et le paiement à la livraison.
7. Créer une référence unique pour chaque commande.
8. Enregistrer les lignes de commande et le statut de règlement.
9. Définir les transitions de statut de commande et de paiement.
10. Décrémenter le stock de manière contrôlée lors de la confirmation effective de la vente.
11. Préparer la génération d'une facture.

**User Stories :** US12, US13 et parcours client du backlog.

**Tickets associés :** #4, #5, #6.

**Livrables :** panier, formulaire de commande, enregistrement des ventes et suivi du paiement.

**Critères de validation :**
- Le panier conserve le produit, la pointure et la quantité.
- Les montants sont recalculés correctement.
- Chaque commande possède une référence unique.
- Le choix d'un moyen de paiement ne vaut pas confirmation du paiement.
- Une commande ne peut pas dépasser le stock disponible.
- Le stock n'est décrémenté qu'une seule fois au moment métier défini comme vente confirmée.
- Les opérations de commande et de stock sont cohérentes même en cas d'erreur.

**Point d'attention paiement :** l'intégration réelle des opérateurs nécessite les accès et API officiels. Tant qu'ils ne sont pas configurés et testés, le système doit afficher un statut non confirmé et ne pas prétendre avoir encaissé le paiement.

### Sprint 5 — Administration, rapports, qualité et déploiement

**Objectif :** finaliser les outils de pilotage et vérifier l'application avant sa mise en service.

Travaux :
1. Développer le tableau de bord administrateur.
2. Afficher les ventes du jour et le chiffre d'affaires.
3. Calculer le bénéfice à partir des prix d'achat et de vente et des ventes confirmées.
4. Afficher le total du stock et les alertes critiques.
5. Ajouter la gestion des utilisateurs et des fournisseurs.
6. Générer les factures.
7. Produire les rapports de ventes et d'état du stock.
8. Tester les parcours catalogue, recherche, filtres, pointures et panier.
9. Tester commandes, statuts de paiement, mouvements et calculs de stock.
10. Tester les droits d'accès et les formulaires.
11. Corriger les anomalies et documenter les limites connues.
12. Vérifier le démarrage local et Docker, la persistance SQLite et le contrôle de santé.
13. Préparer la procédure de déploiement.

**User Stories :** US02, US14, US16, US17, ainsi que les critères transversaux de test et de livraison.

**Tickets associés :** #8, #12. Les tickets #13 et #14 concernent également l'infrastructure et l'interface ; leur état doit être vérifié avant de planifier leur intégration.

**Livrables :** tableau de bord, fournisseurs, factures, rapports, résultats de tests et documentation de déploiement.

**Critères de validation :**
- Les indicateurs proviennent des commandes et mouvements réellement enregistrés.
- Les calculs de chiffre d'affaires et de bénéfice sont documentés et vérifiables.
- Les scénarios essentiels sont exécutés et leurs résultats consignés.
- Les anomalies restantes sont listées.
- Le démarrage et la persistance des données sont vérifiés dans l'environnement cible.

## 5. Dépendances et ordre de réalisation

L'ordre suivant doit être respecté pour limiter les reprises :

1. Structure et configuration avant les modules métier.
2. Base de données avant les écrans connectés aux données.
3. Authentification et autorisations avant les fonctions d'administration.
4. Produits et pointures avant le stock par variante.
5. Stock fiable avant la validation des commandes et ventes.
6. Commandes et ventes enregistrées avant les indicateurs du tableau de bord et les rapports.
7. Tests fonctionnels avant la mise en service.

## 6. Priorisation

- **P0 — Indispensable :** authentification, base de données, catalogue, produits, catégories, pointures, stocks, ventes, mise à jour du stock et recherche.
- **P1 — Important :** gestion des utilisateurs, archivage, fournisseurs, alertes, factures et rapports.

Les fonctionnalités P1 peuvent être développées après stabilisation du parcours principal, sans compromettre la cohérence des données.

## 7. Stratégie de tests

| Domaine | Scénario de vérification | Résultat attendu |
|---|---|---|
| Authentification | Connexion valide et invalide | Accès autorisé ou refusé selon les identifiants |
| Catalogue | Recherche et filtres | Produits correspondants affichés |
| Pointures | Choisir une pointure épuisée | Ajout refusé |
| Panier | Modifier une quantité | Total recalculé |
| Stock | Enregistrer une entrée ou sortie | Quantité et historique actualisés |
| Commande | Commander plus que le stock | Validation refusée |
| Paiement | Sélectionner un opérateur sans confirmation | Paiement non marqué comme reçu |
| Vente | Confirmer une vente | Stock décrémenté une seule fois |
| Administration | Accéder sans session | Accès refusé |
| Déploiement | Redémarrer l'application | Données persistantes conservées |

Aucun test ne doit être déclaré réussi sans exécution réelle et résultat consigné.

## 8. Risques et mesures de prévention

| Risque | Mesure prévue |
|---|---|
| Stock incohérent entre commandes simultanées | Contrôles transactionnels et validation de disponibilité côté serveur |
| Décrémentation multiple du stock | Opération idempotente et statut de vente contrôlé |
| Paiement déclaré reçu sans preuve | Statuts distincts et confirmation via intégration officielle |
| Perte de données | Sauvegardes et vérification de la persistance |
| Accès non autorisé | Sessions sécurisées, contrôle des rôles et mots de passe hachés |
| Indicateurs financiers erronés | Calculs documentés à partir des ventes confirmées et des coûts enregistrés |

## 9. Suivi de l'avancement

Pour chaque User Story, le suivi doit utiliser les états suivants :

- **À faire :** aucun développement validé.
- **En cours :** développement commencé.
- **À tester :** développement terminé, validation en attente.
- **Terminé :** critères d'acceptation vérifiés.

Une story ne doit être marquée « Terminée » que lorsque son code est intégré, ses critères d'acceptation sont vérifiés et les tests correspondants sont documentés.

Les tickets GitHub existants doivent être reliés aux User Stories. Les stories sans ticket dédié doivent faire l'objet de tickets complémentaires si nécessaire.

## 10. Résultat final attendu

À la fin du projet, BOUTIQUE LIBERATION devra fournir une application permettant de consulter et gérer les chaussures, suivre les stocks par modèle et pointure, enregistrer les commandes et les ventes, contrôler les paiements, produire des factures et rapports, et aider le responsable à prendre des décisions de réapprovisionnement.

---

**Document de référence :** `PRODUCT_BACKLOG.md`  
**Repository :** [davidntk/BOUTIQUE-LIBERATION](https://github.com/davidntk/BOUTIQUE-LIBERATION)  
**Nature du document :** plan prévisionnel de développement. Il ne constitue pas une preuve que les fonctionnalités sont déjà implémentées ou testées.
