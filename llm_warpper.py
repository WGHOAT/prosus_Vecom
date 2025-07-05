import os
from dotenv import load_dotenv
from langchain.schema import (AIMessage, HumanMessage, SystemMessage,ChatResult,ChatGeneration)
from langchain.chat_models.base import BaseChatModel
from typing import List, Any
from groq import Groq
from langchain_core.output_parsers import JsonOutputParser

load_dotenv(dotenv_path="/home/ajay/Documents/sleeping_dog_don/prosus_vecom/app/.env")
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))  # Add this line for debugging


parser = JsonOutputParser(pydantic_object={

    
})

class chatgroq(BaseChatModel):
    client: Any = None
    model: str = "llama3-8b-8192"
    temperature: float = 0.7

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    @property
    def _llm_type(self) -> str:
        return "chat-groq"

    def _convert_message(self, message):
        if isinstance(message, HumanMessage):
            return {"role": "user", "content": message.content}
        elif isinstance(message, AIMessage):
            return {"role": "assistant", "content": message.content}
        elif isinstance(message, SystemMessage):
            return {"role": "system", "content": message.content}
        else:
            raise ValueError(f"Unsupported message type: {type(message)}")

    def _convert_back(self, content: str) -> AIMessage:
        return AIMessage(content=content)

    def _generate(self, messages: List, **kwargs: Any):
        payload = {
            "model": self.model,
            "messages": [self._convert_message(m) for m in messages],
            "temperature": self.temperature,
        }
        res = self.client.chat.completions.create(**payload)
        ai_message = self._convert_back(res.choices[0].message.content)
        chat_generation = ChatGeneration(message=ai_message)
        return ChatResult(generations=[chat_generation])