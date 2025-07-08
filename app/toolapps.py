import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_profile():
    with open(BASE_DIR / "user_profile.json",'r') as f:
        return json.load(f)
    
def save_profile(profile):
    with open(BASE_DIR / "user_profile.json",'w') as f:
        json.dump(profile ,f, indent= 5)

def find_restaurant(input: dict):
    with open(BASE_DIR / "restaurant.json", "r") as f:
        restaurants = json.load(f)

    veg = input.get("veg") 
    spice_level = input.get("spice_level", "medium")
    max_price = input.get("max_price", 200)
    

    found = []
    for res in restaurants:
        if veg is not None:
            if veg and not res["veg"]:
                continue
            if not veg and res["veg"]:
                continue

        res_spice = res.get("spice_level", "").lower()
        input_spice = spice_level.lower()

        if input_spice == "high" and res_spice not in ["high", "medium"]:
            continue
        if input_spice == "medium" and res_spice != "medium":
            continue
        if input_spice == "low" and res_spice != "low":
            continue

        if res["price"] > max_price:
            continue

        found.append(res)

    return found[:3]

def food_order(input: dict):
    profile = load_profile()[0]
    order = {"dish": input.get('dish', 'unknown'), "quantity": input.get("quantity", 1)}
    if "past_orders" not in profile:
        profile["past_orders"] = []
    profile["past_orders"].append(order)
    save_profile([profile])
    return order

def update_profile(input: dict):
    profile = load_profile()[0]
    
    # Update profile with new preferences
    if "veg" in input:
        profile["veg"] = input["veg"]
    if "spice_level" in input:
        profile["preferred_spice"] = input["spice_level"]
    if "max_price" in input:
        profile["budget"] = input["max_price"]
    
    save_profile([profile])
    return f"Profile updated successfully: {profile}"

def get_past_orders(_input: dict):
    profile = load_profile()[0]
    return profile.get("past_orders", [])