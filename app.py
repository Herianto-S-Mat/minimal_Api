from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from api.routes.category_routes import category_ns
from api.routes.restaurant_routes import restaurant_ns


app = Flask(__name__)
CORS(app)
api = Api(
    app,
    version='1.0',
    title='Restaurant API',
    description='A simple API for restaurant data',
    prefix='/api' # Global prefix for all API routes
)

api.add_namespace(category_ns)
api.add_namespace(restaurant_ns)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify(message="Resource not found"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(message="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True)