import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import *
from auth import AuthError,requires_auth


def create_app(test=False):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')

    # Set up database
    if not test:
        setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.route('/', methods=['GET']
              )(lambda: jsonify({'message': 'Welcome to sample Render backend!'}))

    @app.after_request
    def after_request(response):
        """Use the after_request decorator to set Access-Control-Allow"""
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/healthy', methods=['GET'])
    def get_healthy(payload=None):
        return jsonify({
            'success': True
        }), 200
    
    @app.route('/drinks', methods=['GET'])
    @requires_auth(permission='get:drinks')
    def get_drinks(payload=None):
        """Get all drinks.

        Returns:
            dict: A dictionary with success status and drinks list.
        """
        drinks_row_list = [drink.short() for drink in Drinking.query.all()]

        return jsonify({
            'success': True,
            'drinks': drinks_row_list
        }), 200

    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth(permission='get:drinks-detail')
    def get_drinks_detail(payload=None):
        """Get all drinks detail.
        """
        drinks_row_list = [drink.long() for drink in Drinking.query.all()]

        return jsonify({
            'success': True,
            'drinks': drinks_row_list
        }), 200

    @app.route('/drinks/<int:id>', methods=['GET'])
    @requires_auth(permission='get:drinks-detail')
    def get_drink(payload, id):
        drink_row = Drinking.query.filter(Drinking.id == id).one_or_none()
        if not drink_row:
            abort(code=404)
        return jsonify({
            'success': True,
            'drinks': [drink_row.long()]
        }), 200

    @app.route('/drinks', methods=['POST'])
    @requires_auth(permission='post:drinks')
    def post_drink(payload=None):
        """Create a new drink.
        """
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        if not title and not recipe:
            abort(code=403)
        drink = Drinking(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    @app.route('/drinks/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:drinks')
    def patch_drink(payload, id):
        drink_row = Drinking.query.filter(Drinking.id == id).one_or_none()
        if not drink_row:
            abort(code=404)
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        if not title and not recipe:
            abort(code=400)
        drink_row.title = title
        drink_row.recipe = json.dumps(recipe)
        drink_row.update()
        return jsonify({
            'success': True,
            'drinks': [drink_row.long()]
        }), 200

    @app.route('/drinks/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:drinks')
    def delete_drink(payload, id):
        drink_row = Drinking.query.filter(Drinking.id == id).one_or_none()
        if not drink_row:
            abort(code=404)
        drink_row.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200

    @app.route('/ingredients', methods=['GET'])
    @requires_auth(permission='get:ingredients')
    def get_ingredients(payload=None):
        """Get all ingredients.

        Returns:
            dict: A dictionary with success status and ingredients list.
        """
        metals_row_list = [ingredient.format()
                                for ingredient in Metals.query.all()]
        return jsonify({
            'success': True,
            'ingredients': metals_row_list
        }), 200

    @app.route('/ingredients', methods=['POST'])
    @requires_auth(permission='post:ingredients')
    def post_ingredient(payload=None):
        """Create a new ingredient.

        Args:
            payload (dict): Payload from Auth0.

        Returns:
            dict: A dictionary with success status and ingredient.
        """
        body = request.get_json()
        name = body.get('name', None)
        density = body.get('density', None)
        if not name:
            abort(code=403)
        ingredient = Metals(name=name, density=density)
        ingredient.insert()
        return jsonify({
            'success': True,
            'ingredients': ingredient.format()
        }), 200

    @app.route('/ingredients/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:ingredients')
    def patch_ingredient(payload, id):
        """Update an ingredient.

        Args:
            payload (dict): Payload from Auth0.
            id (int): Ingredient ID.

        Returns:
            dict: A dictionary with success status and ingredient.

        Raises:
            AuthError 404: If the ingredient is not found.
            AuthError 400: If name is not provided.
        """
        ingredient_row = Metals.query.filter(
            Metals.id == id).one_or_none()
        if not ingredient_row:
            abort(code=404)
        body = request.get_json()
        name = body.get('name', None)
        if not name:
            abort(code=400)
        ingredient_row.name = name
        ingredient_row.update()
        return jsonify({
            'success': True,
            'ingredients': ingredient_row.format()
        }), 200

    @app.route('/ingredients/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:ingredients')
    def delete_ingredient(payload, id):
        """Delete an ingredient.

        Args:
            payload (dict): Payload from Auth0.
            id (int): Ingredient ID.

        Returns:
            dict: A dictionary with success status and deleted ingredient ID.
        """
        ingredient_row = Metals.query.filter(
            Metals.id == id).one_or_none()
        if not ingredient_row:
            abort(code=404)
        ingredient_row.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()
with app.app_context():
    db_reset()


if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0")