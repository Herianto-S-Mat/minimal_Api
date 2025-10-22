from flask_restx import Namespace, Resource, fields
from api.service.category_service import get_categories

# Create a Namespace for categories
category_ns = Namespace('categories', description='Category related operations')

# Define a model for the category output (for Swagger documentation)
category_model = category_ns.model('Category', {
    'category_name': fields.String(required=True, description='The name of the category')
})

@category_ns.route('/')
class CategoryList(Resource):
    @category_ns.doc('list_categories')
    @category_ns.marshal_list_with(category_model) # Use marshal_list_with for a list of items
    def get(self):
        """List all categories"""
        categories_list = get_categories()
        # Flask-RESTX expects a list of dicts if using marshal_list_with
        # So, convert the list of strings to a list of dicts
        return [{'category_name': cat} for cat in categories_list]