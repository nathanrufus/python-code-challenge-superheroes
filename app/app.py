#!/usr/bin/env python3

from flask import Flask, jsonify, request
#from flask_migrate import Migrate

from models import db, Hero, Power, Hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#migrate = Migrate(app, db)



@app.route('/')
def home():
    return "Welcome to the Hero API"


# GET /heroes


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [{
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name
    } for hero in heroes]
    return jsonify(heroes_list)

# GET /heroes/:id


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [{
            "id": hero_power.power.id,
            "name": hero_power.power.name,
            "description": hero_power.power.description
        } for hero_power in hero.hero_powers]
    }

    return jsonify(hero_data),200

# GET /powers


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [{
        "id": power.id,
        "name": power.name,
        "description": power.description
    } for power in powers]
    return jsonify(powers_list),200

# GET /powers/:id


@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data),200

# PATCH /powers/:id


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.form
    if 'description' not in data or len(data['description']) < 20:
        return jsonify({"errors": ["Validation errors"]}), 400

    power.description = data['description']
    db.session.commit()

    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data),201

# POST /hero_powers


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.form
    if 'strength' not in data or data['strength'] not in ['Strong', 'Weak', 'Average'] \
            or 'power_id' not in data or 'hero_id' not in data:
        return jsonify({"errors": ["Validation errors"]}), 400

    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if hero is None or power is None:
        return jsonify({"errors": ["Validation errors"]}), 400

    hero_power = Hero_powers(hero=hero, power=power, strength=data['strength'])
    db.session.add(hero_power)
    db.session.commit()

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [{
            "id": power.id,
            "name": power.name,
            "description": power.description
        } for power in hero.powers]
    }
    return jsonify(hero_data)


if __name__ == "__main__":
    app.run(port=5555)