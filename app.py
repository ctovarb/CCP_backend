from flask import Flask, request, jsonify

from faker import Faker
from faker.generator import random

app = Flask(__name__)

numeros = [
    {'amount': 0},
    {'amount': 1}
]


@app.route('/numero')
def get_numero():
    if round(random.random(), 1) < 0.7:
        return jsonify(numeros[1])

    return jsonify(numeros[0])


@app.route('/estado')
def get_estado():
    if round(random.random(), 1) < 0.7:
        return '', 200
    return '', 500


if __name__ == '__main__':
    app.run()
