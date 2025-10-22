import os
import json

def get_categories():
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, '..', 'data', 'restaurant.json')

    if not os.path.exists(data_file_path):
        return []

    with open(data_file_path, 'r') as f:
        restaurants_data = json.load(f)

    categories = set()
    for restaurant in restaurants_data:
        if 'categories' in restaurant and isinstance(restaurant['categories'], list):
            for category in restaurant['categories']:
                categories.add(category)
    return sorted(list(categories))
