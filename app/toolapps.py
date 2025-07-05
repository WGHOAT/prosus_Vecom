import json
from langchain.tools import tool


def load_profile():
    with open("user_profile.json",'r') as f:
        return json.load(f)
    
def save_profile(profile):
    with open("user_profile.json",'w') as f:
        json.dump(profile ,f, indent= 5)

@tool
def find_restaurant(input: str):
    """Find up to 3 restaurants based on veg preference, spice level, and budget."""
    try:
        data = json.loads(input)
        assert isinstance(data, dict), "Parsed input is not a dict"
        veg = data.get("veg", True)
        spice_level = data.get("spice_level", "medium")
        max_price = data.get("max_price", 200)
    except Exception as e:
        raise ValueError(f"❌ Invalid input for tool: {input} | Error: {str(e)}")
    
    data = json.loads(input)
    veg = data.get("veg", True)
    spice_level = data.get("spice_level", "medium")
    max_price = data.get("max_price", 200)

    print("TOOL: find_restaurant called!")
    with open("restaurant.json", "r") as f:
        restaurants = json.load(f)

    found_res = []
    for res in restaurants:
        if veg and not res["veg"]:
            continue
        if spice_level and res["spice_level"] != spice_level:
            continue
        if res["price"] > max_price:
            continue
        found_res.append(res)

    return found_res[:3]

@tool
def food_order(input: str):
    """Places an order for a specific dish and quantity."""
    data = json.loads(input)
    dish = data.get("dish", "")
    quantity = data.get("quantity", 1)
    if not dish:
        return "Dish not specified in input."
    return f"Your order for {quantity} of '{dish}' has been placed successfully"

@tool
def update_profile(input: str):
    """Updates the user's profile with their latest order."""
    data = json.loads(input)
    order = data.get("order", {})
    if not order:
        return "Missing 'order' data in input."

    with open("user_profile.json", 'r') as f:
        profile = json.load(f)

    profile.setdefault("past_order", []).append(order.get("dish", ""))
    profile["vegan"] = order.get("vegan", False)
    profile["spice_level"] = order.get("spice_level", "medium")

    with open("user_profile.json", 'w') as f:
        json.dump(profile, f, indent=5)

    return profile