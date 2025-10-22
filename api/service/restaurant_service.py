import os
import json

def _load_restaurants():
    current_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(current_dir, '..', 'data', 'restaurant.json')

    if not os.path.exists(data_file_path):
        return []

    with open(data_file_path, 'r') as f:
        return json.load(f)

def get_all_restaurants(categories=[]):
    restaurants = _load_restaurants()

    for r in restaurants:
        r['url'] = f'/api/restaurants/{r["id"]}'

    if not categories:
        return restaurants

    lower_cats = [cat.lower() for cat in categories]
    filtered_restaurants = []

    for r in restaurants:
        # pastikan ada 'categories' dan bertipe list
        if "categories" not in r or not isinstance(r["categories"], list):
            continue

        # ubah ke lowercase untuk perbandingan
        rest_cats_lower = [c.lower() for c in r["categories"]]

        # cek apakah ada irisan
        if set(lower_cats) & set(rest_cats_lower):
            # urutkan kategori supaya yang cocok muncul di depan
            r["categories"] = sorted(
                r["categories"],
                key=lambda c: (c.lower() not in lower_cats)
            )
            filtered_restaurants.append(r)

    return filtered_restaurants
    

def get_restaurant_by_id(restaurant_id):
    restaurants = _load_restaurants()
    for restaurant in restaurants:
        if str(restaurant.get('id')) == str(restaurant_id):
            return restaurant
    return None
