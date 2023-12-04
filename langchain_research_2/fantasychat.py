import tempfile
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv('.env')

# OpenAI API key
openai_key = "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"

# Function to load data from CSV file
def load_data_from_csv(file_path):
    loader = CSVLoader(file_path=file_path, encoding="utf-8")
    return loader.load()

# Setup the conversational chain
def setup_chain(data, openai_key):
    embeddings = OpenAIEmbeddings()
    vectors = FAISS.from_documents(data, embeddings)
    chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo', openai_api_key=openai_key),
                                                  retriever=vectors.as_retriever())
    return chain

# Function for handling conversational chat
def conversational_chat(query, history, chain):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def main():
    # Input CSV file path from the user
    csv_file_path = input("Enter the path to your CSV file: ")
    data = load_data_from_csv(csv_file_path)
    chain = setup_chain(data, openai_key)

    history = []
    print("Hello! Ask me anything about your data.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = conversational_chat(user_input, history, chain)
        print("Bot:", response)

if __name__ == "__main__":
    main()
