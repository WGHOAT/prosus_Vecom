import os
from dotenv import load_dotenv
import groq


load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not GROQ_API_KEY:
    raise ValueError("Where is the Key bro ?")

client = groq.Groq(api_key=GROQ_API_KEY)

def call_model(prompt : str,Model = "llama3-8b-8192"):
    chat_completion = client.chat.completions.create(
        messages = [
            {"role":"user","content":prompt}
        ],
        model = Model
    )
    return chat_completion.choices[0].message.content