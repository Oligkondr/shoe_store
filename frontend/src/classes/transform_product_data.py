api_data = [
  {
    "model_color_id": 1,
    "quantity": 5000,
    "created_at": "2025-05-03T09:24:38.461000+00:00",
    "size_id": 1,
    "price": 5490,
    "id": 1,
    "updated_at": "2025-05-03T09:24:39.278000+00:00",
    "model_color": {
      "name": "bloody black",
      "id": 1,
      "updated_at": "2025-05-03T09:21:26.522000+00:00",
      "model_id": 1,
      "color_id": 1,
      "created_at": "2025-05-03T09:21:24.919000+00:00",
      "model": {
        "name": "super_sneaker",
        "category_id": 1,
        "created_at": "2025-05-03T09:17:49.297000+00:00",
        "description": "best shoes",
        "sex_id": 2,
        "id": 1,
        "updated_at": "2025-05-03T09:17:50.654000+00:00",
        "category": {
          "name": "sneakers",
          "updated_at": "2025-05-03T09:15:40.093000+00:00",
          "id": 1,
          "created_at": "2025-05-03T09:15:38.225000+00:00"
        }
      },
      "color": {
        "created_at": "2025-05-03T09:14:25.981000+00:00",
        "id": 1,
        "name": "black, white, red",
        "updated_at": "2025-05-03T09:14:27.501000+00:00",
        "base_colors": [
          {
            "id": 1,
            "hex": "000000",
            "updated_at": "2025-05-03T09:12:30.148000+00:00",
            "created_at": "2025-05-03T09:12:28.622000+00:00",
            "name": "black"
          },
          {
            "id": 2,
            "hex": "ffffff",
            "updated_at": "2025-05-03T09:12:48.892000+00:00",
            "created_at": "2025-05-03T09:12:46.043000+00:00",
            "name": "white"
          },
          {
            "id": 3,
            "hex": "ff3333",
            "updated_at": "2025-05-03T09:23:13.681000+00:00",
            "created_at": "2025-05-03T09:23:12.290000+00:00",
            "name": "red"
          }
        ]
      }
    },
    "size": {
      "cm": "28",
      "id": 1,
      "updated_at": "2025-05-03T09:11:37.359000+00:00",
      "created_at": "2025-05-03T09:11:35.912000+00:00",
      "ru": "43"
    }
  }
]

def transform_product_data(api_data):
    result = {
        "id": "",
        "model_names": "",
        "color_counts": "",
        "categories": "",
        "prices": "",
        "images": ""
    }

    for item in api_data:
        result["id"] = str(item["id"])
        result["model_names"] = item["model_color"]["model"]["name"]
        result["color_counts"] = str(len(item["model_color"]["color"]["base_colors"]))
        result["categories"] = item["model_color"]["model"]["category"]["name"]
        result["prices"] = str(item["price"])
        result["images"] = "placeholder.png "  # заглушка

    return result

transformed_data = transform_product_data(api_data)
print(transformed_data)
