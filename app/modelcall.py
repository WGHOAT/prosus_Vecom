import os
from dotenv import load_dotenv
import groq
from app.toolapps import find_restaurant, food_order, update_profile
from app.llm_warpper import chatgroq
from langchain.agents import initialize_agent, AgentType


tools = [find_restaurant, food_order, update_profile]

load_dotenv(dotenv_path="/home/ajay/Documents/sleeping_dog_don/prosus_vecom/app/.env")

llm = chatgroq(model="llama3-8b-8192",temperature=0.7)
from langchain.schema import SystemMessage

system_msg = SystemMessage(content="""
You are an AI agent that uses the following tools to respond to user queries. 
Always respond in this format:

Thought: <what you're thinking>
Action: <tool name>
Action Input: <JSON dict as string>

OR

Thought: <what you're thinking>
Final Answer: <the final response to user>
""")


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
    agent_kwargs={
        "system_message": system_msg
    },
    max_iterations=3,
    early_stopping_method="generate"
   
)

def call_model(message: str):
    print(f"\n🔥 Calling agent with message: {message}\n")
    return agent.invoke({"input": message})
