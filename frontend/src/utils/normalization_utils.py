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


def normalize_cart_data(data_dict):
    result = {
        "price": data_dict["price"],
        "products": [],
    }
    for product in data_dict["order_products"]:
        product_data= {
            "item_id": product["id"],
            "model_name": product["product_size"]["product"]["model_color"]["model"]["name"],
            "model_id": product["product_size"]["product"]["model_color"]["model"]["id"],
            "variation_name": product["product_size"]["product"]["model_color"]["name"],
            "variation_id": product["product_size"]["product"]["model_color"]["id"],
            "size": product["product_size"]["size"]["ru"],
            "product_size_id": product["product_size"]["id"],
            "amount": product["quantity"],
            "price": product["price"],
        }
        result["products"].append(product_data)
    return result

example = {
    "id": 3,
    "client_id": 6,
    "approved_at": None,
    "status_id": 0,
    "price": 48960,
    "order_products": [
        {
            "id": 15,
            "price": 12990,
            "quantity": 1,
            "product_size": {
                "id": 1,
                "quantity": 999,
                "size": {"id": 1, "ru": "38", "cm": "24.0"},
                "product": {
                    "id": 1,
                    "price": 12990,
                    "model_color": {
                        "id": 1,
                        "name": "Чёрный мрак",
                        "model": {
                            "id": 1,
                            "name": "Nike Air Doom",
                            "description": "Лёгкие и удобные кеды, идеально подходящие для повседневной носки и прогулок по городу.",
                            "sex_id": 0,
                            "category": {"id": 1, "name": "Кеды"},
                        },
                        "color": {
                            "id": 1,
                            "name": "чёрный, белый",
                            "base_colors": [
                                {"id": 1, "name": "чёрный", "hex": "000000"},
                                {"id": 2, "name": "белый", "hex": "ffffff"},
                            ],
                        },
                    },
                },
            },
        },
        {
            "id": 17,
            "price": 9990,
            "quantity": 1,
            "product_size": {
                "id": 10,
                "quantity": 999,
                "size": {"id": 2, "ru": "39", "cm": "24.5"},
                "product": {
                    "id": 2,
                    "price": 9990,
                    "model_color": {
                        "id": 2,
                        "name": "Красный мрак",
                        "model": {
                            "id": 2,
                            "name": "Abibas Ultraboost",
                            "description": "Эти кроссовки обеспечивают надёжную поддержку и амортизацию, идеально подойдут для активного отдыха.",
                            "sex_id": 2,
                            "category": {"id": 2, "name": "Кроссовки"},
                        },
                        "color": {
                            "id": 2,
                            "name": "красный, чёрный",
                            "base_colors": [
                                {"id": 1, "name": "чёрный", "hex": "000000"},
                                {"id": 3, "name": "красный", "hex": "ef233c"},
                            ],
                        },
                    },
                },
            },
        },
        {
            "id": 19,
            "price": 12990,
            "quantity": 1,
            "product_size": {
                "id": 1,
                "quantity": 999,
                "size": {"id": 1, "ru": "38", "cm": "24.0"},
                "product": {
                    "id": 1,
                    "price": 12990,
                    "model_color": {
                        "id": 1,
                        "name": "Чёрный мрак",
                        "model": {
                            "id": 1,
                            "name": "Nike Air Doom",
                            "description": "Лёгкие и удобные кеды, идеально подходящие для повседневной носки и прогулок по городу.",
                            "sex_id": 0,
                            "category": {"id": 1, "name": "Кеды"},
                        },
                        "color": {
                            "id": 1,
                            "name": "чёрный, белый",
                            "base_colors": [
                                {"id": 1, "name": "чёрный", "hex": "000000"},
                                {"id": 2, "name": "белый", "hex": "ffffff"},
                            ],
                        },
                    },
                },
            },
        },
        {
            "id": 20,
            "price": 12990,
            "quantity": 1,
            "product_size": {
                "id": 1,
                "quantity": 999,
                "size": {"id": 1, "ru": "38", "cm": "24.0"},
                "product": {
                    "id": 1,
                    "price": 12990,
                    "model_color": {
                        "id": 1,
                        "name": "Чёрный мрак",
                        "model": {
                            "id": 1,
                            "name": "Nike Air Doom",
                            "description": "Лёгкие и удобные кеды, идеально подходящие для повседневной носки и прогулок по городу.",
                            "sex_id": 0,
                            "category": {"id": 1, "name": "Кеды"},
                        },
                        "color": {
                            "id": 1,
                            "name": "чёрный, белый",
                            "base_colors": [
                                {"id": 1, "name": "чёрный", "hex": "000000"},
                                {"id": 2, "name": "белый", "hex": "ffffff"},
                            ],
                        },
                    },
                },
            },
        },
    ],
}
