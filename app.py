import streamlit as st
import openai
import time

# Clé API OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ID de l'Assistant
ASSISTANT_ID = "asst_hIbemseWgHUIE32dCFmLEykX"

# Historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Titre et Branding
st.title("🤖 Assistant Procédural Qualité AFMA")
st.caption("Développé par AI Crafters • Pour un accompagnement conforme et structuré")

# --- SECTION : Explication des fonctionnalités ---
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
    
    Pour toute utilisation, décrivez le plus précisément possible votre situation réelle. L’assistant vous guidera avec rigueur et bienveillance.
    """)

# Affichage de l'historique de conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Comment puis-je vous assister concernant les procédures qualité d'AFMA aujourd’hui ?"):
    # Affichage message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Création d’un thread avec l’assistant
    thread = openai.Thread.create()
    openai.Message.create(thread_id=thread.id, role="user", content=prompt)

    # Lancer le run avec l’assistant
    run = openai.Run.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Attente de la réponse complète
    while run.status != "completed":
        time.sleep(5)
        run = openai.Run.retrieve(thread_id=thread.id, run_id=run.id)

    # Récupération des messages de réponse
    messages = openai.Message.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    # Affichage réponse assistant
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
