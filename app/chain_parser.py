from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser  # 👈 key import
from dotenv import load_dotenv

load_dotenv()

# 1. Define base parser
base_parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "params": {"type": "object"},
        "response": {"type": "string"}
    },
    "required": ["action", "params", "response"]
})

# 2. Wrap it with OutputFixingParser
from langchain_core.runnables import RunnablePassthrough  # Add this import if not already present

parser = OutputFixingParser(parser=base_parser, retry_chain=RunnablePassthrough())

# 3. System prompt with aggressive instruction
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for a food ordering service.
Return ONLY a JSON object with the following format:

{{
  "action": "find_restaurant" | "food_order" | "update_profile",
  "params": {{ ... }},
  "response": "Friendly summary of what you did"
}}
Do not give the Counting of number of Restaurant you found just say these are the results i have found
No intro. No explanation. No comments. Just raw JSON, nothing else."""),
    ("user", "{input}")
])

# 4. Connect your chain
llm = ChatGroq(model="llama3-8b-8192", temperature=0.3)
parser_chain = prompt | llm | parser

