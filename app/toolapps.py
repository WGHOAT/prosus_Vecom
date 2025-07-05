import json
from langchain.tools import tool


def load_profile():
    with open("user_profile.json",'r') as f:
        return json.load(f)
    
def save_profile(profile):
    with open("user_profile.json",'w') as f:
        json.dump(profile ,f, indent= 5)

import json

def find_restaurant(input: dict):
    with open("/home/ajay/Documents/sleeping_dog_don/prosus_vecom/app/restaurant.json", "r") as f:
        restaurants = json.load(f)

    veg = input.get("veg", True)
    spice_level = input.get("spice_level", "medium")
    max_price = input.get("max_price", 200)

    found = []
    for res in restaurants:
        if veg and not res["veg"]:
            continue
        if res["spice_level"] != spice_level:
            continue
        if res["price"] > max_price:
            continue
        found.append(res)
    return found[:3]

def food_order(input: dict):
    return f"Order placed for {input.get('quantity', 1)} x {input.get('dish', 'unknown')}."

def update_profile(input: dict):
    # dummy update 
    return f"Profile updated with order: {input}"