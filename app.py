import streamlit as st
import time
from openai import OpenAI

# Initialisation du client avec la clé API depuis les secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ID de l'assistant AFMA
ASSISTANT_ID = "asst_hIbemseWgHUIE32dCFmLEykX"

# Initialisation de l'historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Interface utilisateur
st.set_page_config(page_title="AFMA Chatbot", layout="centered")
st.title("🤖 Assistant Procédural Qualité AFMA")
st.caption("Développé par AI Crafters")

# Bloc d'explication
with st.expander("ℹ️ En savoir plus sur le fonctionnement du chatbot"):
    st.markdown("""
    ### 🔍 Que fait cet assistant ?
    Cet assistant est un **expert virtuel** des procédures qualité d'AFMA. Il vous aide à :
    
    - Comprendre les procédures à suivre selon votre cas concret.
    - Identifier les documents internes pertinents.
    - Connaître les rôles et responsabilités associés.
    - Vous orienter dans la bonne section du bon document qualité AFMA.
    
    ### 🛡️ Limitations :
    - Il **ne sort pas du cadre** des procédures officielles d’AFMA.
    - Si votre demande est vague, il vous demandera poliment des précisions.
    - Il **n’invente jamais** de procédures. Il cite uniquement les documents AFMA.
    
    ### 📑 Méthodologie :
    1. Compréhension du contexte de votre situation.
    2. Identification de la procédure AFMA correspondante.
    3. Recommandation claire avec référence du document et section exacte.
    4. Explication des rôles et étapes à suivre.
    
    Pour toute utilisation, décrivez le plus précisément possible votre situation réelle.
    """)

# Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ d'entrée utilisateur
if prompt := st.chat_input("Comment puis-je vous assister concernant les procédures qualité d'AFMA aujourd’hui ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Création d’un thread et ajout du message utilisateur
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)

    # Lancement de l'assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Attente jusqu’à la fin du traitement
    with st.spinner("L’assistant analyse votre situation..."):
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

    # Récupération de la réponse
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
