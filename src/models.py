from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

class User(db.Model):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    # password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<User %r - %s>' % (self.username, self.email)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
            # do not serialize the password, its a security breach
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

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
    id = db.Column(db.Integer, primary_key=True)
    planetName = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.planetName

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planetName,
        }

    @classmethod
    def get_by_id(cls, id):
        planet = cls.query.get(id)
        return planet

    @classmethod
    def get_all(cls):
        planet = cls.query.all()
        return planet

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def delete(self):
        planet = Planet.query.get(self.id)
        db.session.delete(planet)
        db.session.commit()
        return self

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charName = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.charName

    def serialize(self):
        return {
            "id": self.id,
            "charName": self.charName,
        }

    @classmethod
    def get_by_id(cls, id):
        data = cls.query.get(id)
        return data

    @classmethod
    def get_all(cls):
        data = cls.query.all()
        return data

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def delete(self):
        character = Character.query.get(self.id)
        db.session.delete(character)
        db.session.commit()
        return self

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, ForeignKey('User.id'))
    fav_planet = db.Column(db.Integer, ForeignKey('Planet.id'))
    fav_char = db.Column(db.Integer, ForeignKey('Character.id'))
    user_R = db.relationship(User)
    fav_planet_R = db.relationship(Planet)
    fav_char_R = db.relationship(Character)
    
    # def __repr__(self):
    #     return '<Favorite %r>' % self.fav_planet, self.fav_char

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "user": self.user,
    #         "fav_planet": self.fav_planet,
    #         "fav_char": self.fav_char,
    #     }

    # def create(self):
    #     db.session.add(self)
    #     db.session.commit()
    #     return self

    # @classmethod
    # def delete(self):
    #     favorite = Favorite.query.get(self.id)
    #     db.session.delete(favorite)
    #     db.session.commit()
    #     return self

    # @classmethod
    # def get_user(cls, user):
    #     data = cls.query.filter_by(user=user)
    #     return data

    # @classmethod
    # def get_by_fav_planet(cls, id):
    #     data = cls.query.filter_by(fav_planet=id)
    #     return data

    # @classmethod
    # def get_by_id(cls, id):
    #     data = cls.query.filter_by(id=id)
    #     return data