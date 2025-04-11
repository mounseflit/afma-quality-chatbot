import streamlit as st
import time
import openai

# Configuration de la page
st.set_page_config(page_title="AFMA Chatbot", layout="centered")
st.title("🤖 Assistant Procédural Qualité AFMA")
st.caption("Développé par AI Crafters")

# Initialisation de l'historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ d'entrée utilisateur
if prompt := st.chat_input("Posez votre question sur les procédures qualité d'AFMA :"):
    # Affichage du message de l'utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Appel à l'API OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant expert des procédures qualité d'AFMA."},
                *st.session_state.messages,
            ],
            api_key=st.secrets["OPENAI_API_KEY"]
        )
        assistant_reply = response.choices[0].message["content"]

        # Affichage de la réponse de l'assistant
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
