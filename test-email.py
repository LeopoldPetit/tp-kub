#!/usr/bin/env python3
"""
Script de test pour envoyer un email à Mailpit
Exécuter : python3 test-email.py
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
SMTP_HOST = 'localhost'  # ou 'mailpit-mailpit' depuis un pod dans le cluster
SMTP_PORT = 1025

# Créer l'email
msg = MIMEMultipart('alternative')
msg['Subject'] = "Email de test depuis Python 🚀"
msg['From'] = "test@example.com"
msg['To'] = "destinataire@example.com"

# Contenu HTML
html = """
<html>
  <body>
    <h1>Bienvenue dans Mailpit !</h1>
    <p>Cet email a été envoyé depuis un script Python de test.</p>
    <p>Mailpit a capturé cet email avec succès ! 🎉</p>
  </body>
</html>
"""

# Ajouter le contenu
part = MIMEText(html, 'html')
msg.attach(part)

# Envoyer l'email
print(f"📧 Envoi de l'email à {SMTP_HOST}:{SMTP_PORT}...")
try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)
    print("✅ Email envoyé avec succès !")
    print(f"🌐 Consultez http://localhost:8025 pour voir l'email")
except Exception as e:
    print(f"❌ Erreur : {e}")
