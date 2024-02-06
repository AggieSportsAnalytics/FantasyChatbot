from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from dotenv import load_dotenv

load_dotenv('.env')

agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-4-0613"),
    "testerdataa.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

agent.run("Should I trade Patrick Mahomes for Dak Prescott?")