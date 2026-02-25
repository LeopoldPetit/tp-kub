# 📝 Résumé du Projet WordPress - Atelier Kubernetes

## 🎯 Objectif

Déployer une application WordPress avec base de données MySQL sur Kubernetes en utilisant Helm, avec deux environnements distincts (dev et prod) ayant chacun leurs propres quotas et limites de ressources.

## ✅ Livrables réalisés

### 1. Chart Helm complet ✓
- **Localisation** : `wordpress-app/`
- **Templates** : 10 fichiers YAML pour déployer toutes les ressources
- **Valeurs paramétrables** : Image, ports, ressources, variables d'environnement

### 2. Configuration multi-environnements ✓
- **DEV** : `values-dev.yaml` - Ressources limitées pour le développement
- **PROD** : `values-prod.yaml` - Ressources étendues avec haute disponibilité

### 3. Base de données persistante ✓
- **MySQL 8.0** avec PersistentVolumeClaim
- **Stockage** : 2Gi (dev) / 10Gi (prod)
- **Secrets** : Credentials stockés de manière sécurisée

### 4. Quotas et limites ✓
- **ResourceQuota** par namespace
- **LimitRange** pour contrôle CPU/mémoire par pod
- **Isolation** : Namespace distinct par environnement

### 5. Documentation complète ✓
- **README.md** : Guide complet d'installation et d'utilisation
- **Architecture** : Diagrammes et tableaux de configuration
- **Commandes** : Helm install, upgrade, delete, tests

## 📊 Comparaison des environnements

| Ressource | DEV | PROD |
|-----------|-----|------|
| WordPress Replicas | 1 | 2 |
| WordPress CPU | 100m-200m | 200m-500m |
| WordPress Memory | 128Mi-256Mi | 256Mi-512Mi |
| MySQL Storage | 2Gi | 10Gi |
| Max Pods | 5 | 20 |
| Quota CPU Total | 500m-1 core | 2-4 cores |
| Quota Memory Total | 1Gi-2Gi | 4Gi-8Gi |

## 🚀 Commandes rapides

```bash
# Installation DEV
cd wordpress-app
helm install wordpress-dev . -f values-dev.yaml

# Installation PROD
helm install wordpress-prod . -f values-prod.yaml

# Vérification
kubectl get all -n wordpress-dev
kubectl get all -n wordpress-prod

# Accès WordPress DEV
kubectl port-forward -n wordpress-dev svc/wordpress-dev 8080:80

# Accès WordPress PROD
kubectl port-forward -n wordpress-prod svc/wordpress-prod 8081:80
```

## 📁 Structure du projet

```
tp-kub/
├── README.md                  # Documentation du projet Mailpit
├── PROJET-WORDPRESS.md        # Ce fichier - résumé du projet
├── mailpit/                   # Chart Helm Mailpit (exercice précédent)
└── wordpress-app/             # Chart Helm WordPress (projet principal)
    ├── Chart.yaml
    ├── values.yaml            # Valeurs par défaut
    ├── values-dev.yaml        # Configuration DEV
    ├── values-prod.yaml       # Configuration PROD
    ├── README.md              # Documentation WordPress
    └── templates/
        ├── namespace.yaml
        ├── resourcequota.yaml
        ├── limitrange.yaml
        ├── mysql-secret.yaml
        ├── mysql-pvc.yaml
        ├── mysql-deployment.yaml
        ├── mysql-service.yaml
        ├── wordpress-deployment.yaml
        ├── wordpress-service.yaml
        └── NOTES.txt
```

## 🎓 Compétences démontrées

✅ Création et structuration de charts Helm  
✅ Templating avec Go templates  
✅ Gestion multi-environnements  
✅ Configuration de ResourceQuota et LimitRange  
✅ Déploiement d'applications stateful (avec BDD)  
✅ Gestion des secrets Kubernetes  
✅ Stockage persistant avec PVC  
✅ Services et networking  
✅ Documentation technique  
✅ Bonnes pratiques DevOps  

## 📖 Documentation

- **README WordPress** : `wordpress-app/README.md`
- **Configuration DEV** : `wordpress-app/values-dev.yaml`
- **Configuration PROD** : `wordpress-app/values-prod.yaml`

## 🔗 Repository GitHub

À pousser sur : `https://github.com/LeopoldPetit/tp-kub`

```bash
git add wordpress-app/
git commit -m "feat: Ajout du chart Helm WordPress multi-environnements"
git push origin main
```
