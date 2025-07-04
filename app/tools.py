import json

def find_restaurant(veg ,spice_level,max_price):
    with open("restaurant.json","r") as f:
        restaurants = json.load(f)
    found_res = []
    for res in found_res:
        if veg and not res['veg']:
            continue
        if spice_level and res['spice_level'] != spice_level:
            continue
        if max_price >= res['price']:
            continue
        found_res.append(res)
    return found_res[:3]

def load_profile():
    with open("user_profile.json",'r') as f:
        return json.load(f)
    
def save_profile(profile):
    with open("user_profile.json",'w') as f:
        json.dump(profile ,f, indent= 5)

def updae_profile(order):
    profile = load_profile()
    profile['past_order'].append(['dish'])
    profile['vegan'] = order['vegan']
    profile['spice_level'] = order['spice_level']
    save_profile(profile)
    return profile

def food_order(dish):
    return f"Your order '{dish}' have been Placed successfully"    
