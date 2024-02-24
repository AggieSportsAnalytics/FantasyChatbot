import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variable
load_dotenv('.env')

# Setup
json_path = 'final_data.json'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Loading and preparing data
loader = JSONLoader(file_path=json_path, jq_schema='.[]', text_content=False)
data = loader.load()

injury_loader = CSVLoader(file_path='injuryreports.csv', encoding="utf-8")
injury_reports = injury_loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectors = FAISS.from_documents(data, embeddings)
injury_vectors = FAISS.from_documents(injury_reports, embeddings)

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY),
    retriever=vectors.as_retriever())

injury_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY),
    retriever=injury_vectors.as_retriever())

# Function to handle conversation
def conversational_chat(query):
    injury_query = f'{query}. What is the current situation towards this/these player(s) regarding injuries?' 
    injury_report = injury_chain({"question": injury_query, "chat_history": st.session_state['injury_history']})

    answer_query = f"{query}. Use the following as additional info to answer: {injury_report['answer']}"
    result = chain({"question": answer_query, "chat_history": st.session_state['history']})

    st.session_state['history'].append((query, result["answer"]))

    return result["answer"]

# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []
    st.session_state['injury_history'] = []

# Streamlit layout
logo_image = "asa.png"


st.set_page_config(page_title="HIKE", page_icon="asa.png", initial_sidebar_state="auto", menu_items=None)
st.image(logo_image, width=100, use_column_width=False)

st.title(f"Fantasy Football Analyst Chatbot 🏈")
st.markdown(
    """
    <style>
    h1 {
        color: #B4B7ED !important;
    }
    .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
    """,
    unsafe_allow_html=True
)

# Bio Section
st.write(
    "Hi! My name is HIKE, your AI Fantasy Sports coach. Ask me any questions regarding player info, trade advice, or draft recommendations. I'm always here to help!"
)

# Initialize containers
response_container = st.container()
container = st.container()

with response_container:
    # Insert a unique identifier
    unique_identifier = "response-container-unique"
    st.markdown(f'<div id="{unique_identifier}"></div>', unsafe_allow_html=True)

    for i in range(len(st.session_state['history'])):
        if i % 2 != 0:
            user_msg, bot_reply = st.session_state['history'][i]
            message(user_msg, is_user=True, avatar_style="big-smile", key=str(i) + '_user')
            message(bot_reply, key=str(i), avatar_style="thumbs")

# CSS scoped to the response_container
st.markdown(
    f"""
    <style>
    #{unique_identifier} p {{
        color: #000000 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# User input section
with container:

    st.markdown(
        """
        <style>
        ::placeholder{
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        /* CSS to set the text color of the input box to black */
        input[type="text"] {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("Your question:", placeholder="What should I know about player X?", key='input')
        submit_button = st.form_submit_button(label='Ask HIKE')

        # Prefix to set the persona of the chatbot
        user_query = "You are HIKE, an expert sport analyst specializing in Fantasy Football! Use the data provided to provide CONFIDENT advice (DO NOT hesitate about giving opinions)" + user_input

    if submit_button and user_input:
        output = conversational_chat(user_query)
        # Update the chat history and refresh the page to show the latest message at the top
        st.session_state['history'].append((user_input, output))
        st.experimental_rerun()
    