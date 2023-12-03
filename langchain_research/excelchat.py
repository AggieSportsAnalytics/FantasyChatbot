from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv('.env')

loader = CSVLoader(file_path='testerdata.csv')    

# Create an index using the loaded documents
index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])

# Create a question-answering chain using the index
chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")

query = "Should I draft Nick Chubb or Kenneth Gainwell? Base this answer on Rushing"
response = chain({"question": query})
print(response['result'])