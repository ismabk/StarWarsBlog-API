import os
from flask import Flask, request, jsonify, url_for, render_template, redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, FavoritePlanet, FavoriteCharacter
from sqlalchemy import exc
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.route('/')
def sitemap():
    return generate_sitemap(app)

#--------------------LOGIN -----------------

@app.route("/login", methods=["POST"])
def create_token():
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(name=name, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad name or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token,"user_name": user.name ,"user_id": user.id })


#-------------- USERS -----------------
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

#--------SIGNUP-----------
@app.route('/signup', methods=['POST'])
def signup():

    name, email, password = request.json.get(
        'name', None
    ), request.json.get(
        'email', None
    ), request.json.get(
        'password', None
    )

    if not (name and email and password):
        return jsonify({
            'message': "Data not provided"
        }), 400

    myUser = User(name=name, email=email, password=password)

    try:
        user = myUser.create()
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'User created', 'access_token':access_token}), 201
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

#----------- PLANETS -------------------
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets= Planet.get_all()

    if not planets:
        return jsonify({
            "message": "Planet doesnt exist"
        }), 500

    return jsonify([
         planet.serialize()
         for planet in planets
        ]), 200


@app.route('/planets', methods=['POST'])
def create_planet():

    name = request.json.get(
        'name', None
    )

    if not name:
        return jsonify({
            'message': "Data not provided"
        }), 400

    myPlanet = Planet(name=name)

    try:
        planet = myPlanet.create()
        return jsonify({'message': 'Planet created'}), 201
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_id(id):
    planetsID = Planet.query.get(id)

    if planetsID: return jsonify(planetsID.serialize()), 200

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet_id(id):
    planet = Planet.query.get(id)
    
    try:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message': 'Planet deleted'}), 201
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

#----------- CHARACTERS ----------------
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


@app.route('/people', methods=['POST'])
def create_people():

    name = request.json.get(
        'name', None
    )

    if not name:
        return jsonify({
            'message': "Data not provided"
        }), 400

    myCharacter = Character(name=name)

    try:
        character = myCharacter.create()
        return jsonify({'message': 'Character created'}), 201
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

@app.route('/people/<int:id>', methods=["GET"])
def get_person_id(id):
    personID = Character.query.get(id)

    if personID: return jsonify(personID.serialize()), 200

#------------- FAVORITES -----------------------

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_user_fav():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    favorite_planets= user.favorite_planets
    favorite_characters=user.favorite_characters

    if not favorite_planets and favorite_characters:
        return jsonify({
            "message": "There arent favorites"
        }), 500

    return jsonify([
        faves.serialize() 
        for faves in favorite_characters
        ],[
        favs.serialize()
        for favs in favorite_planets]), 200
    
@app.route('/favorite/planets', methods=['GET'])
def get_all_fav_planets():
    favPlanets= FavoritePlanet.get_all()

    if not favPlanets:
        return jsonify({
            "message": "There arent favorite planets"
        }), 500

    return jsonify([
         favplanet.serialize()
         for favplanet in favPlanets
        ]), 200


@app.route("/favorite/planets/<int:id>", methods=["POST"])
@jwt_required()
def favorite_planet(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    planet = Planet.query.get(id)
    myfavPlanet=FavoritePlanet(user=user.id, planet=planet.id)

    try:
        favoritePlanet = myfavPlanet.create()
        return jsonify({"id": user.id,"planet-favorite":planet.name, "name": user.name }), 200
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

@app.route("/favorite/people/<int:id>", methods=["POST"])
@jwt_required()
def favorite_people(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = Character.query.get(id)
    myfavCharacter=FavoriteCharacter(user=user.id, character=character.id)

    try:
        favoriteCharacter = myfavCharacter.create()
        return jsonify({"id": user.id,"character-favorite":character.name, "name": user.name }), 200
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

@app.route("/favorite/planets/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_planet(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    favorite_planet= FavoritePlanet.query.filter_by(user=user.id, planet=id)
    try:
        db.session.delete(favorite_planet[0])
        db.session.commit()
        return jsonify({'message': 'Planet favorite deleted'}), 201
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})

@app.route("/favorite/people/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_people(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    favorite_character= FavoriteCharacter.query.filter_by(user=user.id, character=id)
    try:
        db.session.delete(favorite_character[0])
        db.session.commit()
        return jsonify({'message': 'Character favorite deleted'}), 201
    except exc.IntegrityError:
        return jsonify({'message': 'Data provided is not valid'})


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)