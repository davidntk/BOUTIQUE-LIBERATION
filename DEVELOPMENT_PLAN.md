# Plan de développement — BOUTIQUE LIBERATION

> **Document de pilotage** — version 1.0  
> Référentiel : `PRODUCT_BACKLOG.md` et première interface de démonstration (`index.html`).  
> Branche de travail actuelle : `feature/boutique-liberation-app`.

## 1. Vision du produit

Construire une application web fiable pour gérer une boutique de chaussures pour hommes et femmes : catalogue, pointures, inventaire, approvisionnements, ventes, clients, fournisseurs, factures et rapports.

L'application doit être utilisable sur ordinateur, tablette et téléphone. Elle doit conserver des données centralisées et sécurisées, contrairement à la première maquette qui stocke les données dans le navigateur.

### Objectifs mesurables

- Connaître à tout moment le stock disponible par modèle et par pointure.
- Enregistrer une vente et mettre à jour le stock sans intervention manuelle.
- Retrouver rapidement un produit par son nom, sa catégorie ou sa pointure.
- Identifier les références à réapprovisionner.
- Consulter les ventes, le chiffre d'affaires et les marges sur une période.
- Protéger les informations grâce à des comptes et des droits d'accès.

## 2. État actuel et périmètre

La version initiale est une **maquette fonctionnelle front-end** dans `index.html`. Elle comprend un tableau de bord, un catalogue, un panier, une gestion simple des produits et pointures, des mouvements de stock, des ventes, des fournisseurs et un export CSV.

Les éléments suivants restent à construire avant une utilisation réelle :

- API serveur et base de données persistante.
- Authentification, rôles et permissions.
- Historique complet et traçabilité des mouvements.
- Factures imprimables et numérotation fiable.
- Paiements réellement intégrés et vérification des transactions.
- Sauvegardes, tests, sécurité et déploiement.
- Gestion des images produits et des commandes multi-utilisateurs.

Les données d'exemple de la maquette ne sont pas des données réelles de la boutique.

## 3. Utilisateurs et rôles

| Rôle | Autorisations principales |
|---|---|
| Administrateur | Accès complet, utilisateurs, paramètres, produits, stocks, ventes et rapports |
| Responsable de stock | Produits, pointures, fournisseurs, approvisionnements, inventaire et alertes |
| Vendeur | Catalogue, panier, création de vente, facture et consultation limitée de ses ventes |
| Client (si boutique en ligne activée) | Catalogue public, panier, commande et suivi de ses commandes |

Chaque opération sensible doit être enregistrée avec l'utilisateur, la date et l'heure.

## 4. Feuille de route par phases

Les durées sont des estimations pour un petit projet et peuvent être ajustées selon l'équipe et les choix techniques.

### Phase 0 — Cadrage et conception (3 à 5 jours)

- [ ] Valider les besoins avec le propriétaire et les vendeurs.
- [ ] Confirmer les rôles, les règles de vente, les devises et les moyens de paiement.
- [ ] Définir les règles de stock : réservation, annulation, retours, pertes et corrections.
- [ ] Dessiner les écrans principaux et les parcours utilisateur.
- [ ] Définir le modèle de données et les critères d'acceptation.
- [ ] Choisir la stack technique et l'environnement d'hébergement.

**Livrable :** spécifications validées, maquettes et schéma de base de données.

### Phase 1 — Fondations techniques et sécurité (1 semaine)

- [ ] Mettre en place le projet front-end et le serveur/API.
- [ ] Configurer la base de données et les migrations.
- [ ] Créer l'authentification : connexion, déconnexion et réinitialisation du mot de passe.
- [ ] Mettre en place les rôles et permissions.
- [ ] Ajouter validation des données, gestion des erreurs et journalisation.
- [ ] Configurer les environnements développement, test et production.

**Livrable :** application connectée à une base de données avec accès sécurisé.

### Phase 2 — Catalogue et gestion des produits (1 semaine)

Références : US03 à US08 et US18.

- [ ] Créer, consulter, modifier et archiver un produit.
- [ ] Gérer les catégories : Homme, Femme, Sport, Cuir (catégories configurables).
- [ ] Gérer les modèles, couleurs, marques et descriptions.
- [ ] Gérer les pointures et les quantités propres à chaque pointure.
- [ ] Ajouter et modifier les photos des produits.
- [ ] Rechercher et filtrer par nom, catégorie, modèle et pointure.
- [ ] Empêcher les doublons de références produits.

**Critères d'acceptation :** un produit peut avoir plusieurs pointures avec des quantités indépendantes ; une recherche retourne les bons résultats ; un produit déjà utilisé dans une vente est archivé plutôt que supprimé définitivement.

**Livrable :** catalogue administrable et consultable.

### Phase 3 — Inventaire et approvisionnements (1 semaine)

Références : US09 à US11 et US15.

- [ ] Enregistrer une réception de marchandises par fournisseur.
- [ ] Enregistrer les sorties : vente, perte, dommage, retour fournisseur ou correction.
- [ ] Afficher le stock par produit et par pointure.
- [ ] Conserver un historique non effaçable des mouvements.
- [ ] Définir un seuil d'alerte configurable.
- [ ] Prévenir les stocks négatifs.
- [ ] Prévoir un inventaire physique et un rapprochement avec le stock théorique.

**Critères d'acceptation :** toute entrée ou sortie crée un mouvement horodaté ; le stock est recalculé de façon cohérente ; une sortie supérieure au stock disponible est refusée.

**Livrable :** module de stock traçable.

### Phase 4 — Ventes, commandes et facturation (1 à 2 semaines)

Références : US12, US13 et US16.

- [ ] Créer un panier avec produit, pointure et quantité.
- [ ] Vérifier la disponibilité au moment de valider la vente.
- [ ] Enregistrer le client et ses coordonnées utiles.
- [ ] Appliquer les réductions selon les droits autorisés.
- [ ] Enregistrer le mode et le statut du paiement.
- [ ] Déduire le stock dans la même transaction que la vente.
- [ ] Générer une facture avec numéro unique, date, articles, quantités, prix et total.
- [ ] Gérer annulation et remboursement avec mouvements de stock correspondants.
- [ ] Empêcher qu'une double validation crée deux ventes.

**Critères d'acceptation :** une vente validée ne peut pas vendre une quantité indisponible ; une vente annulée suit une procédure traçable ; la facture correspond exactement à la vente enregistrée.

**Livrable :** parcours de vente complet avec facture.

### Phase 5 — Fournisseurs, rapports et tableau de bord (1 semaine)

Références : US14, US17 et indicateurs du backlog.

- [ ] Créer, modifier et consulter les fournisseurs.
- [ ] Relier les approvisionnements aux fournisseurs.
- [ ] Afficher les ventes par jour, semaine, mois et période personnalisée.
- [ ] Afficher chiffre d'affaires, coûts, marge brute et nombre de ventes.
- [ ] Afficher les produits les plus vendus et les stocks faibles.
- [ ] Exporter les rapports en CSV.
- [ ] Prévoir une impression ou un export PDF des factures et rapports.

**Livrable :** tableau de bord de gestion et rapports exploitables.

### Phase 6 — Boutique en ligne et paiements (1 à 2 semaines, après validation)

- [ ] Publier un catalogue public adapté au mobile.
- [ ] Permettre aux clients de créer un panier et une commande.
- [ ] Gérer les statuts : en attente, confirmée, préparée, livrée, annulée.
- [ ] Étudier l'intégration officielle d'Airtel Money, Orange Money et M-Pesa selon le pays, le compte marchand et les API disponibles.
- [ ] Vérifier les paiements côté serveur via notifications/webhooks signés.
- [ ] Ne jamais considérer une simple capture d'écran ou une déclaration du client comme preuve de paiement.
- [ ] Prévoir le paiement à la livraison si ce mode est retenu.

**Livrable :** boutique publique et paiements réels après homologation du prestataire.

### Phase 7 — Qualité, recette et mise en production (1 semaine)

- [ ] Tester les parcours principaux sur ordinateur et téléphone.
- [ ] Tester les permissions de chaque rôle.
- [ ] Tester les cas limites : stock nul, pointure indisponible, vente concurrente, annulation et remboursement.
- [ ] Vérifier les sauvegardes et tester une restauration.
- [ ] Corriger les problèmes de performance et d'accessibilité.
- [ ] Configurer HTTPS, domaine, secrets et variables d'environnement.
- [ ] Former les utilisateurs et rédiger un guide court.
- [ ] Déployer progressivement et surveiller les erreurs.

**Livrable :** version de production validée et guide utilisateur.

## 5. Architecture technique proposée

L'architecture définitive doit être confirmée avant la Phase 1. Pour une application web maintenable :

- **Interface :** React avec TypeScript (ou conserver une interface HTML/CSS/JS au tout début si le périmètre reste très réduit).
- **Serveur :** API REST avec Node.js/Express ou un framework backend maîtrisé par l'équipe.
- **Base de données :** PostgreSQL.
- **Authentification :** sessions sécurisées ou jetons courts avec renouvellement sécurisé ; mots de passe hachés côté serveur.
- **Images :** stockage objet ou service de fichiers, avec validation du type et de la taille.
- **Hébergement :** service web et base de données managés, HTTPS obligatoire.
- **Qualité :** GitHub, revues de code, tests automatisés et intégration continue.

Ne pas connecter directement le navigateur à la base de données avec des identifiants privilégiés. Les secrets et clés API doivent rester côté serveur.

## 6. Modèle de données initial

| Entité | Champs essentiels |
|---|---|
| users | id, nom, email, password_hash, role, actif |
| products | id, référence, nom, description, catégorie, marque, image, actif |
| product_variants | id, product_id, pointure, couleur, prix_achat, prix_vente |
| stock_movements | id, variant_id, type, quantité, motif, date, user_id |
| suppliers | id, nom, contact, téléphone, email |
| purchases | id, supplier_id, date, statut, total |
| purchase_items | id, purchase_id, variant_id, quantité, coût_unitaire |
| customers | id, nom, téléphone, email |
| sales | id, numéro, customer_id, user_id, date, statut, total |
| sale_items | id, sale_id, variant_id, quantité, prix_unitaire, coût_unitaire |
| payments | id, sale_id, méthode, montant, statut, référence_prestataire |
| audit_logs | id, user_id, action, entité, entité_id, date |

Les quantités doivent être stockées comme des nombres entiers par variante (pointure/couleur). Les écritures de vente et les mouvements de stock doivent être atomiques en base de données.

## 7. Tests et règles métier indispensables

- Un utilisateur non connecté ne peut pas accéder à l'administration.
- Un vendeur ne peut pas gérer les comptes ou modifier les paramètres sensibles.
- Une pointure ne peut pas avoir un stock négatif.
- Une vente validée décrémente exactement les variantes vendues.
- Une annulation ou un retour crée une trace et ajuste le stock selon la règle définie.
- Deux ventes simultanées ne peuvent pas consommer les mêmes dernières paires.
- Les totaux et marges sont calculés côté serveur.
- Les paiements sont confirmés côté serveur, jamais sur la seule réponse du navigateur.
- Les exports ne doivent contenir que les données accessibles au rôle connecté.

## 8. Ordre de priorité

| Priorité | Périmètre | Pourquoi |
|---|---|---|
| P0 — indispensable | Authentification, rôles, produits, pointures, stock, ventes | Faire fonctionner la gestion quotidienne en sécurité |
| P1 — important | Fournisseurs, alertes, factures, rapports | Améliorer le pilotage et la traçabilité |
| P2 — évolution | Boutique publique, paiement en ligne, notifications | Ouvrir la vente aux clients à distance |

## 9. Definition of Done — conditions de validation

Une fonctionnalité est considérée comme terminée uniquement si :

1. Le besoin et les critères d'acceptation sont satisfaits.
2. Les validations et messages d'erreur sont présents.
3. Les permissions sont vérifiées côté serveur.
4. Les tests pertinents passent.
5. L'interface fonctionne sur mobile et ordinateur.
6. La documentation est mise à jour.
7. Le code est relu et fusionné dans la branche principale après validation.

## 10. Suivi du projet

Mettre à jour les cases à cocher de ce document au fur et à mesure. Pour chaque tâche GitHub, créer une issue avec : objectif, user story, critères d'acceptation, priorité, estimation et dépendances.

### Jalons

- [ ] Jalon 1 : cadrage et conception validés.
- [ ] Jalon 2 : connexion, rôles et base de données opérationnels.
- [ ] Jalon 3 : catalogue et inventaire opérationnels.
- [ ] Jalon 4 : ventes et factures opérationnelles.
- [ ] Jalon 5 : fournisseurs, alertes et rapports validés.
- [ ] Jalon 6 : recette, sauvegarde et déploiement terminés.
- [ ] Jalon 7 : boutique publique et paiements intégrés (optionnel).

---

**Note :** ce plan complète le Product Backlog existant. Les délais sont indicatifs et doivent être recalés après validation des ressources, de la technologie et des contraintes réelles de la boutique.
