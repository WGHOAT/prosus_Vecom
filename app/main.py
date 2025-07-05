from fastapi import FastAPI
from pydantic import BaseModel
from app.chain_parser import parser_chain
from app.toolapps import find_restaurant, food_order, update_profile
app = FastAPI()

class userInput(BaseModel):
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

@app.post("/user-chat")
def user_chat(user_input: userInput):
    try:
        parsed = parser_chain.invoke({"input": user_input.message})
        action = parsed.get("action")
        params = parsed.get("params", {})
        print("🎯 LLM returned:", parsed)

        if action not in tool_map:
            return {"error": f"Unknown action: {action}"}
        if action == "food_order" and not params.get("dish"):
            return {
                "warning": "Model tried to order food without specifying dish. Likely misclassification.",
                "suggestion": "Try: 'find spicy veg food under 200'",
                "result": None
            }

        result = tool_map[action](params)
        return {
            "action": action,
            "params": params,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}
    

    

