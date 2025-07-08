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
    
    if 'max_price' not in normalized or normalized['max_price'] is None:
        normalized['max_price'] = 200

    return normalized
