from fastapi import FastAPI , requests
from app.modelcall import call_model
from app.toolapps import find_restaurant , load_profile, save_profile, update_profile, food_order
from pydantic import BaseModel

app = FastAPI()

class userInput(BaseModel):
    message : str
@app.get("/")
def read_root():
    return {"it works man"}

@app.post("/user-chat")
def user_chat(user_input: userInput):
    response = call_model(user_input.message)
    return {"response": response}