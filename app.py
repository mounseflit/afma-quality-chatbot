import streamlit as st
import time
from openai import OpenAI

# Initialisation du client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = "asst_hIbemseWgHUIE32dCFmLEykX"

# UI settings
st.set_page_config(page_title="AFMA Chatbot", layout="centered")

# Style personnalisé
st.markdown("""
    <style>
    .user-bubble {
        background-color: #dcf8c6;
        padding: 10px 15px;
        border-radius: 10px;
        max-width: 80%;
        margin-left: auto;
        margin-bottom: 10px;
    }
    .assistant-bubble {
        background-color: #f1f0f0;
        padding: 10px 15px;
        border-radius: 10px;
        max-width: 80%;
        margin-right: auto;
        margin-bottom: 10px;
    }
    .message-container {
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

# Titre et intro
st.title("🤖 Assistant Procédural Qualité AFMA")
st.caption("Développé par AI Crafters pour vous orienter dans les procédures internes")

with st.expander("ℹ️ À propos de cet assistant"):
    st.markdown("""
    Cet assistant virtuel vous aide à :
    - Identifier les procédures qualité adaptées à votre situation réelle.
    - Accéder aux bons documents internes AFMA.
    - Comprendre les rôles impliqués dans chaque processus.

    💡 Il se base uniquement sur les documents internes AFMA.
    """)

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.markdown(f'<div class="message-container"><div class="user-bubble">{content}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message-container"><div class="assistant-bubble">{content}</div></div>', unsafe_allow_html=True)

# Champ d'entrée utilisateur
if prompt := st.chat_input("Posez-moi votre question sur une procédure AFMA..."):
    # Affichage message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="message-container"><div class="user-bubble">{prompt}</div></div>', unsafe_allow_html=True)

    # Création du thread + message
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)

    # Lancement de l'assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    with st.spinner("L’assistant réfléchit à la meilleure procédure..."):
        while True:
            run_check = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_check.status == "completed":
                break
            time.sleep(1)

    # Récupérer les messages et trouver la dernière réponse de l’assistant
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = None
    for msg in reversed(messages.data):  # On lit à l’envers pour trouver la dernière réponse assistant
        if msg.role == "assistant":
            assistant_response = msg.content[0].text.value
            break

    if assistant_response:
        st.markdown(f'<div class="message-container"><div class="assistant-bubble">{assistant_response}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        st.warning("❗ Une erreur est survenue, je n’ai pas pu récupérer la réponse.")
