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


example = [
    {
        "id": 10,
        "price": 3490,
        "model_color_id": 10,
        "size_grid": [
            {"id": 56, "quantity": 999, "size": {"id": 8, "ru": "46", "cm": "28.0"}},
            {"id": 57, "quantity": 999, "size": {"id": 7, "ru": "45", "cm": "27.5"}},
            {"id": 58, "quantity": 999, "size": {"id": 5, "ru": "42", "cm": "26.5"}},
            {"id": 59, "quantity": 999, "size": {"id": 3, "ru": "40.5", "cm": "25.5"}},
            {"id": 60, "quantity": 999, "size": {"id": 2, "ru": "40", "cm": "25.0"}},
            {"id": 61, "quantity": 999, "size": {"id": 1, "ru": "39", "cm": "24.5"}},
        ],
        "model_color": {
            "id": 10,
            "name": "Медный блеск",
            "model": {
                "id": 10,
                "name": "Asics Gel-Kayano",
                "description": "Подходит для любителей бега и спортивных тренировок, с инновационной технологией амортизации и отличным сцеплением.",
                "sex_id": 2,
                "category": {"id": 3, "name": "Для бега"},
            },
            "color": {
                "id": 7,
                "name": "чёрный, жёлтый",
                "base_colors": [
                    {"id": 0, "name": "чёрный", "hex": "000000"},
                    {"id": 4, "name": "жёлтый", "hex": "ffff00"},
                ],
            },
        },
    },
    {
        "id": 13,
        "price": 3990,
        "model_color_id": 13,
        "size_grid": [
            {"id": 74, "quantity": 999, "size": {"id": 0, "ru": "38", "cm": "24.0"}},
            {"id": 75, "quantity": 999, "size": {"id": 2, "ru": "40", "cm": "25.0"}},
            {"id": 76, "quantity": 999, "size": {"id": 3, "ru": "40.5", "cm": "25.5"}},
            {"id": 77, "quantity": 999, "size": {"id": 5, "ru": "42", "cm": "26.5"}},
            {"id": 78, "quantity": 999, "size": {"id": 7, "ru": "45", "cm": "27.5"}},
            {"id": 79, "quantity": 999, "size": {"id": 8, "ru": "46", "cm": "28.0"}},
        ],
        "model_color": {
            "id": 13,
            "name": "Океанский бриз",
            "model": {
                "id": 10,
                "name": "Asics Gel-Kayano",
                "description": "Подходит для любителей бега и спортивных тренировок, с инновационной технологией амортизации и отличным сцеплением.",
                "sex_id": 2,
                "category": {"id": 3, "name": "Для бега"},
            },
            "color": {
                "id": 8,
                "name": "белый, синий",
                "base_colors": [
                    {"id": 1, "name": "белый", "hex": "ffffff"},
                    {"id": 5, "name": "синий", "hex": "0000ff"},
                ],
            },
        },
    },
    {
        "id": 14,
        "price": 4490,
        "model_color_id": 14,
        "size_grid": [
            {"id": 80, "quantity": 999, "size": {"id": 1, "ru": "39", "cm": "24.5"}},
            {"id": 81, "quantity": 999, "size": {"id": 3, "ru": "40.5", "cm": "25.5"}},
            {"id": 82, "quantity": 999, "size": {"id": 5, "ru": "42", "cm": "26.5"}},
            {"id": 83, "quantity": 999, "size": {"id": 7, "ru": "45", "cm": "27.5"}},
        ],
        "model_color": {
            "id": 14,
            "name": "Алый рассвет",
            "model": {
                "id": 10,
                "name": "Asics Gel-Kayano",
                "description": "Подходит для любителей бега и спортивных тренировок, с инновационной технологией амортизации и отличным сцеплением.",
                "sex_id": 2,
                "category": {"id": 3, "name": "Для бега"},
            },
            "color": {
                "id": 10,
                "name": "красный, белый",
                "base_colors": [
                    {"id": 1, "name": "белый", "hex": "ffffff"},
                    {"id": 2, "name": "красный", "hex": "ff3333"},
                ],
            },
        },
    },
    {
        "id": 15,
        "price": 4990,
        "model_color_id": 15,
        "size_grid": [
            {"id": 84, "quantity": 999, "size": {"id": 2, "ru": "40", "cm": "25.0"}},
            {"id": 85, "quantity": 999, "size": {"id": 4, "ru": "41", "cm": "26.0"}},
            {"id": 86, "quantity": 999, "size": {"id": 5, "ru": "42", "cm": "26.5"}},
            {"id": 87, "quantity": 999, "size": {"id": 6, "ru": "41", "cm": "25.5"}},
            {"id": 88, "quantity": 999, "size": {"id": 8, "ru": "46", "cm": "28.0"}},
        ],
        "model_color": {
            "id": 15,
            "name": "Голубая лагуна",
            "model": {
                "id": 10,
                "name": "Asics Gel-Kayano",
                "description": "Подходит для любителей бега и спортивных тренировок, с инновационной технологией амортизации и отличным сцеплением.",
                "sex_id": 2,
                "category": {"id": 3, "name": "Для бега"},
            },
            "color": {
                "id": 3,
                "name": "синий, белый",
                "base_colors": [
                    {"id": 1, "name": "белый", "hex": "ffffff"},
                    {"id": 5, "name": "синий", "hex": "0000ff"},
                ],
            },
        },
    },
]


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
        for size in variation["size_grid"]:
            model["variations"][id]["sizes"].append(
                {"product_id": size["id"], "value": size["size"]["ru"]}
            )
    return model
