import os
import json

def _load_restaurants():
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, '..', 'data', 'restaurant.json')

    if not os.path.exists(data_file_path):
        return []

    with open(data_file_path, 'r') as f:
        return json.load(f)

def get_all_restaurants(category=None, page=1, per_page=10):
    restaurants = _load_restaurants()

    if category:
        filtered_restaurants = []
        for restaurant in restaurants:
            if 'categories' in restaurant and isinstance(restaurant['categories'], list):
                if any(cat.lower() == category.lower() for cat in restaurant['categories']):
                    filtered_restaurants.append(restaurant)
            restaurants = filtered_restaurants

    for restaurant in restaurants:
        if 'id' in restaurant:
            restaurant['url'] = f'/api/restaurants/{restaurant["id"]}'

    # Apply pagination
    total_items = len(restaurants)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_restaurants = restaurants[start_index:end_index]

    return {
        "total_items": total_items,
        "total_pages": (total_items + per_page - 1) // per_page,
        "current_page": page,
        "per_page": per_page,
        "restaurants": paginated_restaurants
    }
    

def get_restaurant_by_id(restaurant_id):
    restaurants = _load_restaurants()
    for restaurant in restaurants:
        if str(restaurant.get('id')) == str(restaurant_id):
            return restaurant
    return None
