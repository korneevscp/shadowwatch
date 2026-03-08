# 👁 ShadowWatch

> 🌐 **Notre site pour tout comprendre :** [ShadowWatch — Protège tes données personnelles](https://korneevscp.github.io/shadowwatch)

> Surveillance automatique de tes données personnelles sur le web et le darknet. Alerte par email. Dashboard local. 100% gratuit. Open-source.

![Python](https://img.shields.io/badge/Python-3.8+-00ff88?style=flat-square&logo=python&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-00cfff?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-c8d8e8?style=flat-square)
![Cost](https://img.shields.io/badge/Coût-100%25%20Gratuit-00ff88?style=flat-square)

---

## ✨ Fonctionnalités

- 🔍 **Surveillance multi-sources** — Google, Pastebin, BreachDirectory, Ahmia (index Tor)
- 📧 **Email systématique** — alerte à chaque scan, positif ou négatif
- 🌐 **Dashboard web local** — historique des scans sur `localhost:8080`
- ⏰ **Automatisation quotidienne** — tâche Windows en un clic via `installer.bat`
- 🔒 **100% local** — aucune donnée envoyée à un service tiers
- 💸 **Entièrement gratuit** — aucune API payante requise

---

## 📁 Structure du projet

```
shadowwatch/
├── monitor.py       # Script principal de surveillance
├── dashboard.py     # Serveur web local (localhost:8080)
├── installer.bat    # Installation tâche automatique Windows
├── index.html       # Page de présentation du projet
├── scan_history.json  # Généré automatiquement après le 1er scan
└── README.md
```

---

## ⚙️ Installation

### Prérequis

- Python 3.8 ou plus récent → [python.org](https://python.org/downloads)
- Un compte Gmail avec [App Password activé](https://myaccount.google.com/apppasswords)

### 1. Cloner le dépôt

```bash
git clone https://github.com/korneevscp/shadowwatch.git
cd shadowwatch
```

### 2. Installer les dépendances

```bash
pip install requests beautifulsoup4 googlesearch-python
# Sur Windows si pip n'est pas reconnu :
py -m pip install requests beautifulsoup4 googlesearch-python
```

### 3. Configurer `monitor.py`

Ouvre `monitor.py` et modifie les lignes suivantes :

```python
SMTP_USER  = "ton_email@gmail.com"      # Ton adresse Gmail (expéditeur)
SMTP_PASS  = "xxxx xxxx xxxx xxxx"      # App Password Google (16 caractères)
ALERT_TO   = "destination@email.fr"     # Email qui reçoit les alertes

KEYWORDS = [
    "Prénom Nom",                        # Ton nom complet
    "ton@email.fr",                      # Tes adresses email
    "+33612345678",                      # Tes numéros de téléphone
    "ton_pseudo",                        # Pseudos, ancienne adresse, etc.
]
```

### 4. Créer un App Password Gmail

1. Va sur [myaccount.google.com/security](https://myaccount.google.com/security)
2. Active la **Validation en 2 étapes**
3. Clique sur **Mots de passe des applications**
4. Crée un mot de passe pour "ShadowWatch"
5. Copie le code de 16 caractères dans `SMTP_PASS`

---

## 🚀 Utilisation

### Lancer un scan manuel

```bash
py monitor.py          # Windows
python3 monitor.py     # Mac / Linux
```

### Lancer le dashboard web

```bash
py dashboard.py
# Ouvre automatiquement http://localhost:8080
```

### Automatiser (Windows)

Fais un **clic droit** sur `installer.bat` → **Exécuter en tant qu'administrateur**

Le script installe une tâche Windows qui lance `monitor.py` chaque jour à 09h00.

### Automatiser (Mac / Linux)

```bash
crontab -e
# Ajouter cette ligne (scan tous les jours à 09h00) :
0 9 * * * /usr/bin/python3 /chemin/vers/shadowwatch/monitor.py
```

---

## 📧 Format des emails

| Situation | Sujet | Couleur |
|-----------|-------|---------|
| Données trouvées | `[ALERTE] ShadowWatch — X exposition(s)` | 🔴 Rouge |
| Aucune exposition | `[OK] ShadowWatch — Scan propre` | 🟢 Vert |

---

## 🌐 Sources surveillées

| Source | Type | Coût |
|--------|------|------|
| Google Search | Web de surface | Gratuit |
| BreachDirectory | Fuites de bases de données | Gratuit |
| Pastebin (via Google) | Pastes publics | Gratuit |
| Ahmia | Index réseau Tor | Gratuit |

---

## ⚠️ Limitations connues

- **Google 429** : Google peut bloquer les requêtes trop fréquentes. Le script attend 10 secondes entre chaque requête. Si le blocage persiste, attends 15-20 minutes avant de relancer.
- **Usage personnel uniquement** : Ce projet est conçu pour surveiller vos propres données. Surveiller les données d'autrui sans consentement est illégal (RGPD, Art. 226-1 du Code pénal).

---

## 📜 Licence

MIT License — libre d'utilisation, modification et distribution.

---

## 🤝 Contribuer

Les pull requests sont les bienvenues ! Pour les changements majeurs, ouvre d'abord une issue pour discuter de ce que tu souhaites modifier.

1. Fork le projet
2. Crée ta branche (`git checkout -b feature/nouvelle-source`)
3. Commit tes changements (`git commit -m 'Ajout source XYZ'`)
4. Push (`git push origin feature/nouvelle-source`)
5. Ouvre une Pull Request

---

## 🤖 Développé avec l'IA

Ce projet a été développé en partie avec l'aide de l'IA **Claude (Anthropic)**, faute de développeurs disponibles sur le projet. Le code, la logique et l'architecture ont été construits collaborativement entre l'auteur et l'IA.

---

<div align="center">
  <sub>Fait avec ❤️ pour protéger ta vie privée · <a href="https://github.com/korneevscp/shadowwatch">GitHub</a></sub>
</div>