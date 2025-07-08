from fastapi import FastAPI
from pydantic import BaseModel
from app.chain_parser import parser_chain
from app.toolapps import find_restaurant, food_order, update_profile, get_past_orders
import json
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message : str

class ToolCall(BaseModel):
    action: str
    params: dict
    result: Union[dict, list, str]
    response: str

class ErrorResponse(BaseModel):
    error: str
    response: str

@app.get("/")
def read_root():
    return {"it works man"}

# Tool map
tool_map = {
    "find_restaurant": find_restaurant,
    "food_order": food_order,
    "update_profile": update_profile,
    "get_past_orders": get_past_orders
}

from app.utils import normalize_params

@app.post("/user-chat", response_model=Union[ToolCall, ErrorResponse])
def user_chat(user_input: UserInput):
    try:
        parsed = parser_chain.invoke({"input": user_input.message})
        print("🤖 LLM returned:\n", json.dumps(parsed, indent=2))

        action = parsed.get("action")
        raw_params = parsed.get("params", {})
        params = normalize_params(raw_params)  # 👈 normalization step here
        response_msg = parsed.get("response", "Here’s what I found for you!")

        if action not in tool_map:
            return ErrorResponse(
                error=f"Unknown action: {action}",
                response="Sorry, I didn’t understand what you want me to do."
            )

        result = tool_map[action](params)

        return ToolCall(
            action=action,
            params=params,
            result=result,
            response=response_msg
        )

    except Exception as e:
        return ErrorResponse(
            error=str(e),
            response="Oops! Something went wrong processing your request."
        )


"""
Dude allow port eg i set up the fastapi port as 8000 so do

sudo ufw allow 8000 

and also for react app 

and for react app run it like this 

npx expo start


install expo app and then scan the qr




"""



