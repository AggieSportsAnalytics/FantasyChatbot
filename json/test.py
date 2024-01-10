import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.json_loader import JSONLoader
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv('.env')

json_path = 'fantasy.json'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

loader = JSONLoader(
    file_path=json_path,
    jq_schema='.[]',
    text_content=False)

data = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectors = FAISS.from_documents(data, embeddings)


chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0.0, model_name='gpt-4',
                   openai_api_key=OPENAI_API_KEY),
    retriever=vectors.as_retriever())


def conversational_chat(query):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))

    return result["answer"]


if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = [""]

if 'past' not in st.session_state:
    st.session_state['past'] = [""]

response_container = st.container()
container = st.container()


with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("Query:", placeholder="Talk about your data here (:", key='input')
        submit_button = st.form_submit_button(label='Send')
        user_query = "You are an expert sport analyst who specializes in Fantasy Football! Give a final answer without any precautions to this user question: " + user_input



    if submit_button and user_input:
        output = conversational_chat(user_input)

        st.session_state['past'].append(user_query)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
