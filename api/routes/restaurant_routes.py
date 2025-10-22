from flask_restx import Namespace, Resource, fields, reqparse
from api.service.restaurant_service import get_all_restaurants, get_restaurant_by_id

restaurant_ns = Namespace('restaurants', description='Restaurant related operations')

# Define models for documentation
review_model = restaurant_ns.model('Review', {
    'user_image': fields.String(description='URL of the user\'s image'),
    'user_name': fields.String(description='Name of the user'),
    'rating': fields.Float(description='Rating given by the user'),
    'text': fields.String(description='Review text')
})

restaurant_model = restaurant_ns.model('Restaurant', {
    'id': fields.String(required=True, description='The restaurant unique identifier'),
    'name': fields.String(required=True, description='The restaurant name'),
    'photos': fields.List(fields.String, description='List of photo URLs'),
    'categories': fields.List(fields.String, description='List of cuisine/category types'),
    'rating': fields.Float(description='Average rating of the restaurant'),
    'price_range': fields.String(description='Price range (e.g., $, $$, $$$)'),
    'is_open': fields.Boolean(description='Whether the restaurant is currently open'),
    'address': fields.String(description='Physical address of the restaurant'),
    'url': fields.String(description='URL to the restaurant detail page'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews for the restaurant')
})

# Parser for query parameters
restaurant_list_parser = reqparse.RequestParser()
restaurant_list_parser.add_argument('category', type=str, help='Filter restaurants by category', location='args', action='append')

@restaurant_ns.route('/')
class RestaurantList(Resource):
    @restaurant_ns.doc('list_restaurants')
    @restaurant_ns.expect(restaurant_list_parser)
    @restaurant_ns.marshal_list_with(restaurant_model)
    def get(self):
        """List all restaurants, optionally filtered by category"""
        args = restaurant_list_parser.parse_args()
        category = args.get('category')
        return get_all_restaurants(category)

@restaurant_ns.route('/<string:restaurant_id>')
@restaurant_ns.param('restaurant_id', 'The restaurant identifier')
class Restaurant(Resource):
    @restaurant_ns.doc('get_restaurant')
    @restaurant_ns.marshal_with(restaurant_model)
    def get(self, restaurant_id):
        """Fetch a single restaurant by its ID"""
        restaurant = get_restaurant_by_id(restaurant_id)
        if restaurant:
            return restaurant
        restaurant_ns.abort(404, message="Restaurant not found")