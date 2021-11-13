from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager #originally two lines of from flask_login imports.
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin): # added UserMixin for day_3 branch
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default ='')
    email = db.Column(db.String(150), nullable = False)
    user_name = db.Column(db.String, nullable = True)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)

    def __init__(self,first_name,last_name,email,user_name,id='',password='',token='',g_auth_verify=False): # the order here mattered for the signup page.
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_name = user_name
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.user_name} has been added to the database!'

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key = True) # change Integer to String if you run into problems.
    # the Hero id is supposed to be an integer according to the prompt... 
    # Switch out for string if it gives errors.
    # I'm not sure it will work with the def set_id we were shown in class.
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Integer, nullable = True)
    super_power = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,comics_appeared_in,super_power,user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token

    def __repr__(self):
        return f'The following Hero has been added: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe()) # may need to check on this line.

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','comics_appeared_in','super_power'] # may need to check on this line.

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many = True)