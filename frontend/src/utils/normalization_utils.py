from .formatting_utils import format_colors_amount, format_price


def normalize_catalog_products(products_list):
    models = dict()
    for product in products_list:
        id = product["model_color"]["model"]["id"]
        if id not in models:
            models[id] = {
                "id": id,
                "name": product["model_color"]["model"]["name"],
                "category": product["model_color"]["model"]["category"]["name"],
                "colors": set(),
                "min_price": product["price"],
                "max_price": product["price"],
            }
        models[id]["colors"].add(product["model_color"]["id"])
        models[id]["min_price"] = min(models[id]["min_price"], product["price"])
        models[id]["max_price"] = max(models[id]["max_price"], product["price"])
    for model in models.values():
        model["colors_str"] = format_colors_amount(len(model["colors"]))
        model["price_str"] = format_price(model["min_price"], model["max_price"])

    return models


def normalize_item_page_data(variations_list):
    model = {
        "id": variations_list[0]["model_color"]["model"]["id"],
        "name": variations_list[0]["model_color"]["model"]["name"],
        "category": variations_list[0]["model_color"]["model"]["category"]["name"],
        "description": variations_list[0]["model_color"]["model"]["description"],
        "variations": dict(),
    }
    for variation in variations_list:
        id = variation["id"]
        if id not in model["variations"]:
            model["variations"][id] = {
                "id": id,
                "name": variation["model_color"]["name"],
                "price": format_price(variation["price"], variation["price"]),
                "colors": [],
                "sizes": [],
            }
        for color in variation["model_color"]["color"]["base_colors"]:
            model["variations"][id]["colors"].append(color["hex"])
        for size in variation["product_size"]:
            model["variations"][id]["sizes"].append(
                {"product_id": size["id"], "value": size["size"]["ru"]}
            )
        model["variations"][id]["sizes"] = sorted(
            model["variations"][id]["sizes"], key=lambda d: float(d["value"])
        )
    return model
