"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import (db, User, Planet, Character, Favorite)
from sqlalchemy import exc

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ---------------------------- PEOPLE ---------------------------------------   

@app.route('/people', methods=['GET'])
def get_all_people():
    charNames= Character.get_all()

    if not charNames:
        return jsonify({
            "message": "People doesnt exist"
        }), 500

    return jsonify([
         charName.serialize()
         for charName in charNames
        ]), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_user(id):
    charNames= Character.get_by_id(id)

    if not charNames:
        return jsonify({
            "message": "People doesnt exist"
        }), 500

    return jsonify(
         charNames.serialize()
        ), 200

@app.route('/people', methods=['POST'])
def create_people():
    charName = request.json.get(
        "charName", None
    )

    if not(charName):
        return jsonify({
            "message": "Character not provided"
        }), 400

    myChar = Character(charName=charName)

    try:
        myChar.create()
        return jsonify({
            "message": "Character favorite created"
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Data provided not valid"
        }), 500


# -------------------------- PLANETS -----------------------------------


@app.route('/planet', methods=['GET'])
def get_all_planets():
    planetNames= Planet.get_all()

    if not planetNames:
        return jsonify({
            "message": "Planet doesnt exist"
        }), 500

    return jsonify([
         planetName.serialize()
         for planetName in planetNames
        ]), 200


@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    planetNames= Planet.get_by_id(id)

    if not planetNames:
        return jsonify({
            "message": "Planet doesnt exist"
        }), 500

    return jsonify(
        planetNames.serialize()
    ), 200


@app.route('/planet', methods=['POST'])
def create_planet():
    planetName = request.json.get(
        "planetName", None
    )

    if not(planetName):
        return jsonify({
            "message": "Planet not provided"
        }), 400

    myPlanet = Planet(planetName=planetName)

    try:
        myPlanet.create()
        return jsonify({
            "message": "Planet favorite created"
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Data provided not valid"
        }), 500

#----------------------------------- USERS ---------------------------

@app.route('/users', methods=['POST'])
def create_user():
    username, email = request.json.get(
        "username", None
    ), request.json.get(
        "email", None
    )

    if not(username and email):
        return jsonify({
            "message": "User not provided"
        }), 400

    myUser = User(username=username, email=email)

    try:
        myUser.create()
        return jsonify({
            "message": "User favorite created",
            "data": myUser.serialize()
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Data provided not valid"
        }), 500


@app.route('/users', methods=['GET'])
def get_all_users():
    user= User.get_all()

    if not user:
        return jsonify({
            "message": "Users doesnt exist"
        }), 500

    return jsonify([
         usere.serialize()
         for usere in user
        ]), 200



@app.route('/users/favorites', methods=['GET'])
def get_all_users_favorites():
    userFavorites= Favorite.get_all()
    users = Favorite.get_user(userFavorites.user)

    if not userFavorites:
        return jsonify({
            "message": "Favorites Users content doesnt exist"
        }), 500

    if not users:
        return jsonify({
            "message": " Users content doesnt exist"
        }), 500

    return jsonify({
         user.serialize()
         for user in users
        }), 200

#---------------------------- FAVORITES-------------------------------


@app.route('/favorite/planet/<int:id>', methods=['POST'])
def create_favorite_planet():
    planet = request.json.get(
        "planetName", None
    )

    if not(planet):
        return jsonify({
            "message": "Planet not provided"
        }), 400

    myPlanetFavorite = Planet(planet_name=planet_name)

    try:
        myPlanetFavorite.create()
        return jsonify({
            "message": "Planet favorite created",
            "data": myPlanetFavorite.serialize()
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Data provided not valid"
        }), 500

@app.route('/favorite/people/<int:id>', methods=['POST'])
def create_favorite_people():
    char = request.json.get(
        "charName", None
    )

    if not(char):
        return jsonify({
            "message": "Character not provided"
        }), 400

    myCharFavorite = char(charName=charName)

    try:
        myCharFavorite.create()
        return jsonify({
            "message": "Character favorite created"
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Data provided not valid"
        }), 500

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):

    deletePlanet = Planet.query.get(id)
    db.session.delete(deletePlanet)
    db.session.commit()

    try:
        return jsonify({
            "message": "Planet favorite deleted"
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Planet provided not valid"
        }), 500

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_people(id):

    deletePeople = Character.query.get(id)
    db.session.delete(deletePeople)
    db.session.commit()

    try:
        return jsonify({
            "message": "Character favorite deleted"
        }), 201

    except exc.IntegrityError:
        return jsonify({
            "message": "Character provided not valid"
        }), 500

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
