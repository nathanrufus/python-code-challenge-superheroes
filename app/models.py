from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(100))
    super_name =db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes=db.relationship('Hero_powers' ,backref='hero')

class Hero_powers(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength =db.Column(db.String(100))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def strength_validation(self, key, strength):  
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError(
                "Strength must be either Strong, Weak, or Average")
        return strength


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(100))
    description =db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    mypower=db.relationship('Hero_powers', backref='power')


    @validates('description')
    def description_validation(self, key, description):  
        if  description == "":
            raise ValueError('Power must have a description')
        if len(description) < 20:
            raise ValueError('Description must be more than 20 characters')

        return description


# add any models you may need. 