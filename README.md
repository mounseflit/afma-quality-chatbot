# 🤖 Assistant Procédural Qualité AFMA

Développé par **AI Crafters**, cet assistant virtuel permet aux collaborateurs d'AFMA d’obtenir des recommandations précises sur les **procédures qualité** internes à l’entreprise. Il s’appuie sur l'API d'OpenAI et les bibliothèques Streamlit pour offrir une interface conviviale et conversationnelle.

---

## 🎯 Objectif

Aider les utilisateurs à :
- Identifier les procédures qualité adaptées à leur situation.
- Trouver les documents officiels et les sections exactes des manuels internes d’AFMA.
- Comprendre les rôles et responsabilités liés à chaque procédure.
- Obtenir des réponses rigoureuses, professionnelles et bienveillantes.

---

## 🧰 Fonctionnalités

- 💬 Interface de chat interactive en français via Streamlit.
- 📚 Référencement automatique des procédures internes.
- 🧠 Compréhension contextuelle des cas d’usage terrain.
- 🕵️‍♂️ Demande de précisions si la requête est vague ou ambiguë.
- 📎 Références directes aux documents officiels d'AFMA (avec section).

---

## ⚠️ Limitations

- Ne couvre que les procédures incluses dans la bibliothèque interne AFMA.
- Ne peut pas fournir d'informations en dehors du périmètre des documents qualité.
- Ne remplace pas un contrôle humain ou un responsable qualité.

---

## 🚀 Lancer l'application localement

### 1. Cloner le projet

```bash
git clone https://votre-repo.git
cd afma-quality-chatbot
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Ajouter votre clé OpenAI

Créez un fichier `.streamlit/secrets.toml` :

```toml
OPENAI_API_KEY = "votre_clé_api_openai"
```

### 4. Lancer l’application

```bash
streamlit run afma_chatbot.py
```

---

## 📁 Structure

```
afma-quality-chatbot/
│
├── afma_chatbot.py            # Application principale Streamlit
├── requirements.txt           # Dépendances Python
└── .streamlit/
    └── secrets.toml           # Clé API OpenAI
```

---

---

## 📦 Fichier `requirements.txt`

```txt
openai>=1.3.7
streamlit>=1.32.0
```

---


## 🧑‍💼 Contact & Crédits

Ce projet a été développé par **AI Crafters** pour le compte d'**AFMA** dans le cadre de l'amélioration continue de la qualité et de la conformité documentaire.

---




