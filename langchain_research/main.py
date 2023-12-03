from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Part 1
load_dotenv('.env')

llm = OpenAI()
chat_model = ChatOpenAI()

# Initialize the chat with a system message
chat = ChatOpenAI(model_name="gpt-4", temperature=0.3)
messages = [
    SystemMessage(content="You are an expert sport analyst who specializes in Fantasy Football")
]

print("Welcome to the Basketball Expert Chatbot! Type 'exit' to end the conversation.")

while True:
    # Get user input
    user_input = input("You: ")
    
    # Check for exit command
    if user_input.lower() == 'exit':
        break

    # Add the user's message to the conversation
    messages.append(HumanMessage(content=user_input))

    # Get the response from the chat model
    response = chat(messages)

    # Print the response
    print("Chatbot:", response.content)

    # Add the AI's response to the conversation
    messages.append(AIMessage(content=response.content))
