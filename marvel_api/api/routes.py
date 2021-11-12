from flask import Blueprint, request, jsonify
from marvel_api.helpers import token_required
from marvel_api.models import db, User, Hero, hero_schema, heroes_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}