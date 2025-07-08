from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

class ToolOutput(BaseModel):
    action: str = Field(description="The action to perform: find_restaurant, food_order, update_profile, or get_past_orders.")
    params: dict = Field(default_factory=dict, description="Parameters for the action. Should be an empty object if no relevant parameters are found.")
    response: str = Field(description="A friendly summary of what you did.")

# 1. Define parser using Pydantic model
parser = JsonOutputParser(pydantic_object=ToolOutput)

# 2. System prompt with aggressive instruction
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for a food ordering service.
Return ONLY a JSON object with the following format, adhering to the ToolOutput schema:

{{
  "action": "find_restaurant" | "update_profile" | "get_past_orders",
  "params": {{
    "veg": Optional[bool],  // true if user wants vegetarian, false if non-vegetarian. Omit if not specified.
    "spice_level": Optional["low" | "medium" | "high"], // Omit if not specified.
    "max_price": Optional[float], // Omit if not specified.
    "dish": Optional[str], // Required for food_order action
    "quantity": Optional[int] // Required for food_order action
  }},
  "response": "Friendly summary of what you did"
}}

If no relevant parameters are found for 'params', return an empty JSON object for 'params'.
     do action "food_order only when user specify the word order"
No intro. No explanation. No comments. Just raw JSON, nothing else."""),
    ("user", "{input}")
])

# 3. Connect your chain
llm = ChatGroq(model="llama3-8b-8192", temperature=0.3)
parser_chain = prompt | llm | parser

