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
import pandas as pd
from langchain.chains import SimpleSequentialChain


# Load environment variables
load_dotenv('.env')

# Setup
json_path = 'fantasy.json'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Loading and preparing data
loader = JSONLoader(file_path=json_path, jq_schema='.[]', text_content=False)
data = loader.load()

injury_loader = CSVLoader(file_path='data/injuryreports.csv', encoding="utf-8")
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

ss_chain: SimpleSequentialChain = SimpleSequentialChain(
    chains=[chain, injury_chain],
    verbose=True
)

# Function to handle conversation
def conversational_chat(query):
    injury_query = f'{query}. What is the current situation towards this/these player(s) regarding injuries?' 
    report = injury_chain({"question": injury_query, "chat_history": st.session_state['history']})

    result = ss_chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))

    injury_query = f'{query}. What is the current situation towards this/these player(s) regarding injuries?' 
    report = injury_chain({"question": injury_query, "chat_history": st.session_state['history']})
    print(report['answer']) 
    # st.session_state['history'].append((injury_query, report["answer"]))

    return result["answer"]
 
# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Streamlit layout
st.title("Fantasy Football Analyst Chatbot 🏈")
st.markdown("Ask me anything about fantasy football!")

# Initialize containers
response_container = st.container()
container = st.container()

# Displaying chat history
with response_container:
    for i in range(len(st.session_state['history'])):
        if i % 2 != 0:
            user_msg, bot_reply = st.session_state['history'][i]
            message(user_msg, is_user=True, avatar_style="big-smile", key=str(i) + '_user')
            message(bot_reply, key=str(i), avatar_style="thumbs")

# User input section
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("Your question:", placeholder="What should I know about player X?", key='input')
        submit_button = st.form_submit_button(label='Ask the Analyst')

        # Prefix to set the persona of the chatbot
        user_query = "You are an expert sport analyst specializing in Fantasy Football! " + user_input

    if submit_button and user_input:
        output = conversational_chat(user_query)
        # Update the chat history and refresh the page to show the latest message at the top
        st.session_state['history'].append((user_input, output))
        st.experimental_rerun()