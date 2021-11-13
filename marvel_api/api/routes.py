from flask import Blueprint, request, jsonify
from marvel_api.helpers import token_required
from marvel_api.models import db, User, Hero, hero_schema, heroes_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}

# CRUD operations

# Create
# trying to use datetime
@api.route('/heroes', methods = ['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    # date_created = datetime.utcnow
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    hero = Hero(name,description,comics_appeared_in,super_power, user_token) #removed <date_created,> from before user_token.

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

# Retrive all
@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token # maybe I should choose a different name than "owner".
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)

# Retrive one hero endpoint
@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid token required'}), 401

# UPDATE
@api.route('/heroes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_hero(current_user_token,id):
    hero = Hero.query.get(id)

    # hold alt to click at beginning of each line and add hero.

    hero.name = request.json['name'] 
    hero.description = request.json['description']
    hero.comics_appeared_in = request.json['comics_appeared_in']
    hero.super_power = request.json['super_power']
    hero.date_created = request.json['date_created']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

# DELETE
@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)