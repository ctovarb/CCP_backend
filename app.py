import random
from functools import wraps

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, verify_jwt_in_request, get_jwt

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'jwt.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change on production


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    usuario = Column(String, unique=True)
    password = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'usuario', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

db.create_all()


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


users = []
usuario = "admin"
password = "admin"

users.append(User(usuario=usuario,
                     password=password))

usuario = "user"
password = "user"
users.append(User(usuario=usuario,
                     password=password))

for user in users:
    user_exists = User.query.filter_by(usuario=usuario, password=password).first()

    if user_exists is None:
        db.session.add(user)
        db.session.commit()


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        usuario = request.json['usuario']
        password = request.json['password']
    else:
        usuario = request.form['usuario']
        password = request.form['password']

    test = User.query.filter_by(usuario=usuario, password=password).first()
    if test:
        if usuario == "admin":
            access_token = create_access_token(identity=usuario, additional_claims={"is_administrator": True})
        else:
            access_token = create_access_token(identity=usuario, additional_claims={"is_administrator": False})
        return jsonify(message='Login Successful', access_token=access_token)
    else:
        return jsonify('Bad user or Password'), 401


numeros = [
    {'amount': 0},
    {'amount': 1}
]


@app.route('/numero')
@jwt_required()
def get_numero():
    if round(random.random(), 1) < 0.7:
        return jsonify(numeros[1])

    return jsonify(numeros[0])


@app.route('/estado')
@admin_required()
def get_estado():
    if round(random.random(), 1) < 0.7:
        return '', 200
    return '', 500


if __name__ == '__main__':
    app.run()
