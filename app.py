from flask import Flask, request, jsonify

from faker import Faker
from faker.generator import random

app = Flask(__name__)

numeros = [
    { 'amount': 0 },
    { 'amount': 1 }
]

@app.route('/numero')
def get_numero():
    return jsonify(numeros[(random.randint(0, 1))])


if __name__ == '__main__':
    app.run()
