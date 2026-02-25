# Atelier Kubernetes - Chart Helm Mailpit

Ce repository contient un chart Helm pour déployer Mailpit, un serveur SMTP de test avec interface web, dans un cluster Kubernetes.

## 📧 Qu'est-ce que Mailpit ?

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
