# Atelier Kubernetes - Charts Helm

Ce repository contient deux projets de déploiement Kubernetes avec Helm :
1. **Mailpit** - Serveur SMTP de test (exercice d'introduction)
2. **WordPress** - Application complète avec MySQL et multi-environnements (projet principal)

---

## 🚀 DÉMARRAGE RAPIDE - WordPress Multi-environnements

### Installation et lancement complet en 4 étapes :

```bash
# 1. Cloner le repository
git clone https://github.com/LeopoldPetit/tp-kub.git
cd tp-kub/wordpress-app

# 2. Installer l'environnement DEV
helm install wordpress-dev . -f values-dev.yaml

# 3. Attendre que tout soit prêt (environ 1-2 minutes)
kubectl wait --for=condition=ready pod -l app=mysql -n wordpress-dev --timeout=120s
kubectl wait --for=condition=ready pod -l app=wordpress -n wordpress-dev --timeout=120s

# 4. Accéder à WordPress
kubectl port-forward -n wordpress-dev svc/wordpress-dev 8080:80
# Puis ouvrir http://localhost:8080
```

### Vérifier le déploiement :

```bash
# Voir toutes les ressources
kubectl get all -n wordpress-dev

# Voir les volumes persistants
kubectl get pvc -n wordpress-dev

# Voir les quotas et limites appliqués
kubectl describe resourcequota -n wordpress-dev
kubectl describe limitrange -n wordpress-dev

# Voir les logs
kubectl logs -l app=wordpress -n wordpress-dev
kubectl logs -l app=mysql -n wordpress-dev
```

### Installer aussi l'environnement PROD (optionnel) :

```bash
# Installation PROD (2 replicas WordPress, 10Gi MySQL, plus de ressources)
helm install wordpress-prod . -f values-prod.yaml

# Attendre que ce soit prêt
kubectl wait --for=condition=ready pod -l app=mysql -n wordpress-prod --timeout=120s
kubectl wait --for=condition=ready pod -l app=wordpress -n wordpress-prod --timeout=120s

# Accéder à WordPress PROD
kubectl port-forward -n wordpress-prod svc/wordpress-prod 8081:80
# Puis ouvrir http://localhost:8081
```

### Désinstaller :

```bash
# Désinstaller DEV
helm uninstall wordpress-dev
kubectl delete namespace wordpress-dev

# Désinstaller PROD
helm uninstall wordpress-prod
kubectl delete namespace wordpress-prod
```

---

## 📚 Documentation complète

- **WordPress** : Voir `wordpress-app/README.md` (documentation détaillée)
- **Mailpit** : Voir la section ci-dessous

---

## 📧 Projet Mailpit (exercice d'introduction)

Mailpit est un serveur SMTP de test avec interface web.

### Qu'est-ce que Mailpit ?

Mailpit est un outil de développement qui simule un serveur SMTP et fournit une interface Web pour lire les e-mails de test. Il permet de :

- **Capturer tous les emails** envoyés par vos applications en développement
- **Visualiser les emails** dans une interface web moderne
- **Tester l'envoi d'emails** sans risquer d'envoyer de vrais emails
- **Déboguer** le contenu HTML, les pièces jointes, etc.

## 🚀 Installation

### Prérequis

- Kubernetes cluster actif (Minikube, Docker Desktop, K3s, etc.)
- Helm 3.x installé
- kubectl configuré

### Déploiement

1. **Cloner le repository**
```bash
git clone https://github.com/LeopoldPetit/tp-kub.git
cd tp-kub
```

2. **Installer le chart Helm**
```bash
helm install mailpit ./mailpit
```

3. **Vérifier le déploiement**
```bash
kubectl get pods
kubectl get svc
kubectl get pvc
```

4. **Accéder à l'interface Web**
```bash
kubectl port-forward svc/mailpit-mailpit 8025:8025
```

Puis ouvrir : http://localhost:8025

## 📁 Structure du Chart

```
mailpit/
├── Chart.yaml                          # Métadonnées du chart
├── values.yaml                         # Valeurs par défaut
├── charts/                             # Dépendances (vide)
└── templates/
    ├── _helpers.tpl                    # Fonctions helper
    ├── NOTES.txt                       # Instructions post-installation
    ├── deployment.yaml                 # Déploiement Mailpit
    ├── service.yaml                    # Service (ports 8025 et 1025)
    ├── configmap.yaml                  # Configuration Mailpit
    └── persistentvolumeclaim.yaml      # Stockage persistant (1Gi)
```

## ⚙️ Configuration

### Valeurs par défaut (values.yaml)

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `image.repository` | Image Docker de Mailpit | `docker.io/axllent/mailpit` |
| `image.tag` | Tag de l'image | `latest` |
| `service.port` | Port HTTP (interface web) | `8025` |
| `service.smtp.port` | Port SMTP | `1025` |
| `persistence.enabled` | Activer le stockage persistant | `true` |
| `persistence.size` | Taille du volume | `1Gi` |
| `replicaCount` | Nombre de réplicas | `1` |

### Personnaliser les valeurs

Créez un fichier `my-values.yaml` :

```yaml
image:
  tag: "v1.10.0"

persistence:
  size: 2Gi

replicaCount: 1
```

Puis installez avec :

```bash
helm install mailpit ./mailpit -f my-values.yaml
```

## 📧 Utilisation

### Envoyer des emails de test

Configurez votre application pour envoyer des emails vers :

- **Hôte SMTP** : `mailpit-mailpit.default.svc.cluster.local` (depuis un pod)
- **Hôte SMTP** : `localhost` (avec port-forward)
- **Port SMTP** : `1025`
- **Authentification** : Aucune

### Exemple Python

```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Ceci est un email de test")
msg['Subject'] = "Test Mailpit"
msg['From'] = "test@example.com"
msg['To'] = "destinataire@example.com"

with smtplib.SMTP('localhost', 1025) as server:
    server.send_message(msg)
```

### Exemple avec curl

```bash
kubectl port-forward svc/mailpit-mailpit 1025:1025 &

curl --url 'smtp://localhost:1025' \
  --mail-from 'from@example.com' \
  --mail-rcpt 'to@example.com' \
  --upload-file - <<EOF
From: from@example.com
To: to@example.com
Subject: Test Email

Ceci est un email de test envoyé via curl!
EOF
```

## 🧪 Test du script Python

Un script de test est fourni dans `test-email.py` :

```bash
python3 test-email.py
```

Consultez ensuite http://localhost:8025 pour voir l'email.

## 🛠️ Commandes utiles

### Vérifier l'état

```bash
# Voir les pods
kubectl get pods -l app=mailpit

# Voir les logs
kubectl logs -l app=mailpit

# Décrire le pod
kubectl describe pod -l app=mailpit
```

### Mise à jour

```bash
# Modifier values.yaml puis :
helm upgrade mailpit ./mailpit

# Ou avec des valeurs spécifiques :
helm upgrade mailpit ./mailpit --set persistence.size=2Gi
```

### Désinstallation

```bash
helm uninstall mailpit

# Supprimer aussi le PVC (données)
kubectl delete pvc mailpit-mailpit
```

## 📚 Ressources Helm utilisées

Ce chart déploie les ressources Kubernetes suivantes :

- **Deployment** : Gère le pod Mailpit avec configuration des volumes et variables d'environnement
- **Service** : Expose les ports 8025 (HTTP) et 1025 (SMTP)
- **ConfigMap** : Configure les variables d'environnement de Mailpit
- **PersistentVolumeClaim** : Stocke les emails dans `/maildir` (1Gi par défaut)

## 🎓 Contexte pédagogique

Ce projet a été créé dans le cadre d'un atelier Kubernetes pour apprendre :

- ✅ La création de charts Helm
- ✅ L'utilisation des templates Go
- ✅ La gestion des variables avec `values.yaml`
- ✅ Le déploiement d'applications dans Kubernetes
- ✅ La gestion du stockage persistant
- ✅ Les services et l'exposition d'applications

## 📄 Licence

Ce projet est fourni à des fins éducatives.

## 👤 Auteur

Atelier créé par : Nizar MHADHBI (2025)

---

**Note** : Mailpit est un outil de développement. Ne l'utilisez pas en production pour envoyer de vrais emails !
