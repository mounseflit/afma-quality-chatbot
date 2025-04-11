import streamlit as st
import time
from openai import OpenAI

# Initialisation du client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = "asst_hIbemseWgHUIE32dCFmLEykX"

# UI settings
st.set_page_config(page_title="AFMA Chatbot", layout="centered")
st.title("🤖 Assistant Procédural Qualité AFMA")
st.caption("Développé par AI Crafters pour vous orienter dans les procédures internes")

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ d'entrée utilisateur
if prompt := st.chat_input("Posez-moi votre question sur une procédure AFMA..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Création du thread et ajout du message utilisateur
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)

    # Lancement de l'assistant avec create_and_poll
    with st.spinner("L’assistant réfléchit à la meilleure procédure..."):
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Récupération de la réponse
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = None
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            assistant_response = msg.content[0].text.value
            break

    if assistant_response:
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    else:
        st.warning("❗ Une erreur est survenue, je n’ai pas pu récupérer la réponse.")
