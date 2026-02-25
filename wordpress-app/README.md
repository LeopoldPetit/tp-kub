# 🚀 Déploiement WordPress avec Helm - Multi-environnements

Ce projet déploie une application WordPress complète avec base de données MySQL sur Kubernetes, en utilisant Helm pour gérer deux environnements distincts : **développement (dev)** et **production (prod)**.

## 📋 Table des matières

- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Structure du projet](#-structure-du-projet)
- [Configuration des environnements](#️-configuration-des-environnements)
- [Installation](#-installation)
- [Gestion des déploiements](#-gestion-des-déploiements)
- [Tests et vérification](#-tests-et-vérification)
- [Commandes utiles](#️-commandes-utiles)
- [Ressources Kubernetes](#-ressources-kubernetes)
- [Troubleshooting](#-troubleshooting)

---

## 🏗 Architecture

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                     Cluster Kubernetes                       │
│                                                              │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │   Namespace: dev     │    │   Namespace: prod    │      │
│  │                      │    │                      │      │
│  │  ┌────────────────┐  │    │  ┌────────────────┐  │      │
│  │  │  WordPress     │  │    │  │  WordPress     │  │      │
│  │  │  (1 replica)   │  │    │  │  (2 replicas)  │  │      │
│  │  └────────┬───────┘  │    │  └────────┬───────┘  │      │
│  │           │          │    │           │          │      │
│  │  ┌────────▼───────┐  │    │  ┌────────▼───────┐  │      │
│  │  │  MySQL         │  │    │  │  MySQL         │  │      │
│  │  │  (1 replica)   │  │    │  │  (1 replica)   │  │      │
│  │  │  PVC: 2Gi      │  │    │  │  PVC: 10Gi     │  │      │
│  │  └────────────────┘  │    │  └────────────────┘  │      │
│  │                      │    │                      │      │
│  │  ResourceQuota       │    │  ResourceQuota       │      │
│  │  LimitRange          │    │  LimitRange          │      │
│  └──────────────────────┘    └──────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Composants déployés

| Composant | Description |
|-----------|-------------|
| **WordPress** | Application web CMS (Content Management System) |
| **MySQL 8.0** | Base de données relationnelle avec stockage persistant |
| **Secret** | Stockage sécurisé des credentials MySQL |
| **PersistentVolumeClaim** | Volume persistant pour les données MySQL |
| **Services** | Exposition interne des applications |
| **ResourceQuota** | Limitation des ressources par namespace |
| **LimitRange** | Limites par défaut pour les pods |

---

## ✅ Prérequis

- **Kubernetes cluster** actif (Minikube, Docker Desktop, K3s, Kind, etc.)
- **Helm 3.x** installé
- **kubectl** configuré et connecté au cluster
- Au moins **4Gi de RAM** disponible sur le cluster
- **Stockage dynamique** configuré (ou provider de PV)

### Vérification des prérequis

```bash
# Vérifier Kubernetes
kubectl cluster-info
kubectl version --short

# Vérifier Helm
helm version --short

# Vérifier les nodes disponibles
kubectl get nodes

# Vérifier le storage class
kubectl get storageclass
```

---

## 📁 Structure du projet

```
wordpress-app/
├── Chart.yaml                          # Métadonnées du chart Helm
├── values-dev.yaml                     # Configuration environnement DEV
├── values-prod.yaml                    # Configuration environnement PROD
└── templates/
    ├── NOTES.txt                       # Instructions post-installation
    ├── _helpers.tpl                    # Fonctions helper
    ├── namespace.yaml                  # Création du namespace
    ├── resourcequota.yaml              # Quotas de ressources
    ├── limitrange.yaml                 # Limites par défaut
    ├── mysql-secret.yaml               # Secrets MySQL
    ├── mysql-pvc.yaml                  # Volume persistant MySQL
    ├── mysql-deployment.yaml           # Déploiement MySQL
    ├── mysql-service.yaml              # Service MySQL
    ├── wordpress-deployment.yaml       # Déploiement WordPress
    └── wordpress-service.yaml          # Service WordPress
```

---

## ⚙️ Configuration des environnements

### 📘 Environnement DEV

**Objectif** : Développement et tests avec ressources limitées

| Paramètre | Valeur |
|-----------|--------|
| **Namespace** | `wordpress-dev` |
| **WordPress replicas** | 1 |
| **WordPress CPU** | Request: 100m / Limit: 200m |
| **WordPress Memory** | Request: 128Mi / Limit: 256Mi |
| **MySQL CPU** | Request: 100m / Limit: 200m |
| **MySQL Memory** | Request: 256Mi / Limit: 512Mi |
| **MySQL Storage** | 2Gi |
| **ResourceQuota CPU** | Request: 500m / Limit: 1 core |
| **ResourceQuota Memory** | Request: 1Gi / Limit: 2Gi |
| **Max Pods** | 5 |

### 📗 Environnement PROD

**Objectif** : Production avec haute disponibilité et ressources étendues

| Paramètre | Valeur |
|-----------|--------|
| **Namespace** | `wordpress-prod` |
| **WordPress replicas** | 2 (haute disponibilité) |
| **WordPress CPU** | Request: 200m / Limit: 500m |
| **WordPress Memory** | Request: 256Mi / Limit: 512Mi |
| **MySQL CPU** | Request: 200m / Limit: 500m |
| **MySQL Memory** | Request: 512Mi / Limit: 1Gi |
| **MySQL Storage** | 10Gi |
| **ResourceQuota CPU** | Request: 2 cores / Limit: 4 cores |
| **ResourceQuota Memory** | Request: 4Gi / Limit: 8Gi |
| **Max Pods** | 20 |

### Personnalisation

Vous pouvez modifier les fichiers `values-dev.yaml` ou `values-prod.yaml` selon vos besoins :

```yaml
# Exemple : Augmenter les ressources
wordpress:
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "500m"
```

---

## 🚀 Installation

### Option 1 : Déploiement rapide

#### Environnement DEV

```bash
# Se placer dans le dossier du projet
cd wordpress-app

# Installer le chart pour l'environnement DEV
helm install wordpress-dev . -f values-dev.yaml

# Attendre que les pods soient prêts
kubectl wait --for=condition=ready pod -l app=mysql -n wordpress-dev --timeout=120s
kubectl wait --for=condition=ready pod -l app=wordpress -n wordpress-dev --timeout=120s
```

#### Environnement PROD

```bash
# Installer le chart pour l'environnement PROD
helm install wordpress-prod . -f values-prod.yaml

# Attendre que les pods soient prêts
kubectl wait --for=condition=ready pod -l app=mysql -n wordpress-prod --timeout=120s
kubectl wait --for=condition=ready pod -l app=wordpress -n wordpress-prod --timeout=120s
```

### Option 2 : Installation avec surcharge de valeurs

```bash
# Exemple : Modifier le nombre de replicas WordPress en prod
helm install wordpress-prod . -f values-prod.yaml \
  --set wordpress.replicaCount=3

# Exemple : Augmenter le stockage MySQL en dev
helm install wordpress-dev . -f values-dev.yaml \
  --set mysql.persistence.size=5Gi
```

---

## 🔄 Gestion des déploiements

### Mise à jour (Upgrade)

```bash
# Mettre à jour l'environnement DEV après modification des values
helm upgrade wordpress-dev . -f values-dev.yaml

# Mettre à jour avec des valeurs en ligne de commande
helm upgrade wordpress-prod . -f values-prod.yaml \
  --set wordpress.image.tag="6.5-apache"
```

### Rollback

```bash
# Voir l'historique des releases
helm history wordpress-dev -n wordpress-dev

# Revenir à la version précédente
helm rollback wordpress-dev -n wordpress-dev

# Revenir à une version spécifique (ex: revision 2)
helm rollback wordpress-dev 2 -n wordpress-dev
```

### Désinstallation

```bash
# Désinstaller WordPress DEV
helm uninstall wordpress-dev

# Désinstaller WordPress PROD
helm uninstall wordpress-prod

# Supprimer également les namespaces (et toutes les ressources)
kubectl delete namespace wordpress-dev
kubectl delete namespace wordpress-prod
```

**⚠️ Attention** : La suppression du namespace supprime également les PVC et donc les données !

---

## 🧪 Tests et vérification

### 1. Vérifier l'état des ressources

```bash
# Environnement DEV
kubectl get all -n wordpress-dev
kubectl get pvc -n wordpress-dev
kubectl get secret -n wordpress-dev

# Environnement PROD
kubectl get all -n wordpress-prod
kubectl get pvc -n wordpress-prod
kubectl get secret -n wordpress-prod
```

### 2. Consulter les quotas et limites

```bash
# ResourceQuota
kubectl describe resourcequota -n wordpress-dev
kubectl describe resourcequota -n wordpress-prod

# LimitRange
kubectl describe limitrange -n wordpress-dev
kubectl describe limitrange -n wordpress-prod
```

### 3. Vérifier les logs

```bash
# Logs MySQL
kubectl logs -l app=mysql -n wordpress-dev --tail=50
kubectl logs -l app=mysql -n wordpress-prod --tail=50

# Logs WordPress
kubectl logs -l app=wordpress -n wordpress-dev --tail=50
kubectl logs -l app=wordpress -n wordpress-prod --tail=50
```

### 4. Accéder à WordPress

#### Environnement DEV

```bash
# Port-forward sur le port 8080
kubectl port-forward -n wordpress-dev svc/wordpress-dev 8080:80

# Ouvrir dans le navigateur
open http://localhost:8080
```

#### Environnement PROD

```bash
# Port-forward sur le port 8081
kubectl port-forward -n wordpress-prod svc/wordpress-prod 8081:80

# Ouvrir dans le navigateur
open http://localhost:8081
```

### 5. Test de connexion MySQL

```bash
# Environnement DEV
kubectl exec -it -n wordpress-dev deployment/wordpress-mysql-dev -- \
  mysql -u wp_user_dev -pdev_password_123 -e "SHOW DATABASES;"

# Environnement PROD
kubectl exec -it -n wordpress-prod deployment/wordpress-mysql-prod -- \
  mysql -u wp_user_prod -pprod_secure_password_456 -e "SHOW DATABASES;"
```

---

## 🛠️ Commandes utiles

### Helm

```bash
# Lister toutes les releases Helm
helm list --all-namespaces

# Voir les valeurs utilisées pour un déploiement
helm get values wordpress-dev

# Voir le manifeste complet généré
helm get manifest wordpress-dev

# Tester le template sans installation
helm template wordpress-dev . -f values-dev.yaml

# Valider le chart
helm lint .
```

### Kubectl

```bash
# Événements dans un namespace
kubectl get events -n wordpress-dev --sort-by='.lastTimestamp'

# Décrire un pod
kubectl describe pod -l app=wordpress -n wordpress-dev

# Shell dans un pod WordPress
kubectl exec -it -n wordpress-dev deployment/wordpress-dev -- bash

# Copier des fichiers depuis/vers un pod
kubectl cp wordpress-dev/<pod-name>:/var/www/html/wp-config.php ./wp-config.php -n wordpress-dev

# Surveiller les pods en temps réel
kubectl get pods -n wordpress-dev --watch
```

### Monitoring des ressources

```bash
# Utilisation CPU/Mémoire par pod
kubectl top pods -n wordpress-dev
kubectl top pods -n wordpress-prod

# Utilisation par node
kubectl top nodes
```

---

## 📚 Ressources Kubernetes déployées

### Par environnement (DEV ou PROD)

| Type | Nom | Namespace | Description |
|------|-----|-----------|-------------|
| Namespace | `wordpress-{env}` | - | Isolation logique de l'environnement |
| ResourceQuota | `{env}-quota` | `wordpress-{env}` | Quotas CPU/mémoire/storage |
| LimitRange | `{env}-limitrange` | `wordpress-{env}` | Limites par défaut des containers |
| Secret | `mysql-secret` | `wordpress-{env}` | Credentials MySQL |
| PVC | `mysql-pvc` | `wordpress-{env}` | Stockage persistant MySQL |
| Deployment | `wordpress-mysql-{env}` | `wordpress-{env}` | MySQL 8.0 |
| Service | `wordpress-mysql-{env}` | `wordpress-{env}` | Service MySQL (port 3306) |
| Deployment | `wordpress-{env}` | `wordpress-{env}` | WordPress 6.4 |
| Service | `wordpress-{env}` | `wordpress-{env}` | Service WordPress (port 80) |

### Variables d'environnement WordPress

| Variable | Source | Description |
|----------|--------|-------------|
| `WORDPRESS_DB_HOST` | ConfigMap | Hôte MySQL |
| `WORDPRESS_DB_NAME` | Secret | Nom de la base de données |
| `WORDPRESS_DB_USER` | Secret | Utilisateur MySQL |
| `WORDPRESS_DB_PASSWORD` | Secret | Mot de passe MySQL |

---

## 🔧 Troubleshooting

### Les pods ne démarrent pas

```bash
# Vérifier les événements
kubectl get events -n wordpress-dev --sort-by='.lastTimestamp'

# Vérifier les logs
kubectl logs -l app=mysql -n wordpress-dev
kubectl logs -l app=wordpress -n wordpress-dev

# Vérifier les quotas
kubectl describe resourcequota -n wordpress-dev
```

### Erreur "Insufficient CPU/Memory"

```bash
# Augmenter les quotas dans values-{env}.yaml
# Ou réduire les ressources demandées par les pods
```

### MySQL ne démarre pas

```bash
# Vérifier le PVC
kubectl get pvc -n wordpress-dev
kubectl describe pvc mysql-pvc -n wordpress-dev

# Vérifier les secrets
kubectl get secret mysql-secret -n wordpress-dev -o yaml
```

### WordPress ne peut pas se connecter à MySQL

```bash
# Vérifier que MySQL est prêt
kubectl get pods -l app=mysql -n wordpress-dev

# Tester la connexion depuis le pod WordPress
kubectl exec -it -n wordpress-dev deployment/wordpress-dev -- \
  ping wordpress-mysql-dev
```

### Problème de stockage

```bash
# Vérifier les StorageClass disponibles
kubectl get storageclass

# Si pas de StorageClass par défaut, en définir un dans values.yaml
mysql:
  persistence:
    storageClass: "local-path"  # ou autre
```

---

## 📄 Licence

Ce projet est fourni à des fins éducatives dans le cadre d'un atelier Kubernetes.

## 👤 Auteurs

- **Projet réalisé par** : [Votre Nom]
- **Date** : Février 2025
- **Formation** : Atelier Kubernetes - Déploiement avec Helm

---

## 🎓 Objectifs pédagogiques atteints

✅ Création d'un chart Helm structuré et paramétrable  
✅ Gestion de deux environnements distincts (dev/prod)  
✅ Intégration d'une base de données persistante  
✅ Configuration de ResourceQuota et LimitRange  
✅ Utilisation de Secrets pour les données sensibles  
✅ Déploiement multi-composants (WordPress + MySQL)  
✅ Documentation complète et tests  

---

**Note** : Ce projet est conçu pour l'apprentissage. Pour une utilisation en production réelle, ajoutez :
- Ingress pour l'exposition externe
- TLS/SSL avec cert-manager
- Backup automatique des données
- Monitoring (Prometheus/Grafana)
- Autoscaling (HPA)
- Network Policies pour la sécurité
