from fastapi import FastAPI
from pydantic import BaseModel
from app.chain_parser import parser_chain 
from app.toolapps import find_restaurant, food_order, update_profile
import json
from fastapi.middleware.cors import CORSMiddleware

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
@app.get("/")
def read_root():
    return {"it works man"}

# Tool map
tool_map = {
    "find_restaurant": find_restaurant,
    "food_order": food_order,
    "update_profile": update_profile
}

def normalize_params(params: dict) -> dict:
    key_map = {
        "cuisine": "veg",
        "spiciness": "spice_level",
        "budget": "max_price"
    }

    spice_map = {
        "spicy": "high",
        "mild": "low",
        "medium": "medium",
        "hot": "high"
    }

    normalized = {}
    for k, v in params.items():
        new_key = key_map.get(k, k)

        # Handle veg
        if new_key == "veg" and isinstance(v, str):
            v = v.lower() in ["veg", "vegetarian", "yes"]

        # Normalize spice level
        if new_key == "spice_level" and isinstance(v, str):
            v = spice_map.get(v.lower(), v.lower())

        normalized[new_key] = v

    return normalized

@app.post("/user-chat")
def user_chat(user_input: UserInput):
    try:
        parsed = parser_chain.invoke({"input": user_input.message})
        print("🤖 LLM returned:\n", json.dumps(parsed, indent=2))

        action = parsed.get("action")
        raw_params = parsed.get("params", {})
        params = normalize_params(raw_params)  # 👈 normalization step here
        response_msg = parsed.get("response", "Here’s what I found for you!")

        if action not in tool_map:
            return {
                "error": f"Unknown action: {action}",
                "response": "Sorry, I didn’t understand what you want me to do."
            }

        result = tool_map[action](params)

        return {
            "action": action,
            "params": params,
            "result": result,
            "response": response_msg
        }

    except Exception as e:
        return {
            "error": str(e),
            "response": "Oops! Something went wrong processing your request."
        }


"""
Dude allow port eg i set up the fastapi port as 8000 so do

sudo ufw allow 8000 

and also for react app 

and for react app run it like this 

npx expo start


install expo app and then scan the qr




"""



