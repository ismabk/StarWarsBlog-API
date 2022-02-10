from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    favorite_planets = db.relationship("FavoritePlanet")
    favorite_characters = db.relationship("FavoriteCharacter")


    def __repr__(self):
        return '<User %r - %s>' % (self.name, self.email)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_id(cls, id):
        user = cls.query.get(id)
        return user

    @classmethod
    def get_all(cls):
        user = cls.query.all()
        return user

    @classmethod
    def delete(self):
        user = User.query.get(self.id)
        db.session.delete(user)
        db.session.commit()
        return self

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    faved_by = db.relationship("FavoritePlanet", backref="planet_faved")

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @classmethod
    def get_all(cls):
        planet = cls.query.all()
        return planet

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    faved_by = db.relationship("FavoriteCharacter")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @classmethod
    def get_all(cls):
        data = cls.query.all()
        return data

    def create(self):
        db.session.add(self)
        db.session.commit()
      

    @classmethod
    def delete(self):
        character = Character.query.get(self.id)
        db.session.delete(character)
        db.session.commit()
        return self 

class FavoritePlanet(db.Model):
    __tablename__ = 'favoritesPlanets'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    planet = db.Column(db.Integer, db.ForeignKey("planets.id"))

    def __repr__(self):
        return f"{User.query.get(self.user)} faved {Planet.query.get(self.planet)}"
            
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "planet": self.planet,
        }
        
    @classmethod
    def get_all(cls):
        data = cls.query.all()
        return data

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class FavoriteCharacter(db.Model):
    __tablename__ = 'favoritesCharacters'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    character = db.Column(db.Integer, db.ForeignKey("characters.id"))

    def __repr__(self):
        return f"{User.query.get(self.user)} faved {Character.query.get(self.fav_character)}"
            
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "character": self.character,
        }

    @classmethod
    def get_all(cls):
        data = cls.query.all()
        return data

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
