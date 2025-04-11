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

    # Lancement de l'assistant avec streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Création du run avec streaming
        stream = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
            stream=True
        )

        for chunk in stream:
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "content"):
                content = chunk.delta.content
                full_response += content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
