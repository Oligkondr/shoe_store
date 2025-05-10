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
        models[id]["colors"].add(product["model_color_id"])
        models[id]["min_price"] = min(models[id]["min_price"], product["price"])
        models[id]["max_price"] = max(models[id]["max_price"], product["price"])
    for model in models.values():
        model["colors_str"] = format_colors_amount(len(model["colors"]))
        model["price_str"] = format_price(model["min_price"], model["max_price"])

    return models