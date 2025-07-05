from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/ajay/Documents/sleeping_dog_don/prosus_vecom/app/.env")

# LLM initialization
llm = ChatGroq(model="llama3-8b-8192", temperature=0.3)

# JSON structure we want from the LLM
parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "action": {"type": "string"},  # e.g., "find_restaurant"
        "params": {"type": "object"}   # dict for tool parameters
    },
    "required": ["action", "params"]
})

# Prompt the LLM with clear instruction
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a structured API interface to a food ordering assistant.

Return JSON **only** in this format:

{{
  "action": "find_restaurant" | "food_order" | "update_profile",
  "params": {{
    "veg": true,
    "spice_level": "high",
    "max_price": 200
  }}
}}

✱ If the user is asking for food preferences (like "spicy", "veg", "under 200"), the action should be "find_restaurant".
✱ If the user is placing an actual order ("order", "get me", "I want 2 of..."), then use "food_order".
✱ Only use "update_profile" when the user is asking to save or change their preferences or history.

Do NOT guess.
Do NOT hallucinate action names.
Do NOT output anything outside the required JSON.
"""),
    ("user", "{input}")
])



# Final LangChain chain
parser_chain = prompt | llm | parser