from flask import Flask, request, jsonify

from faker import Faker
from faker.generator import random

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here.
    return 'Hello World!'


incomes = [
    { 'amount': 0 },
    { 'amount': 1 }
]

@app.route('/numero')
def get_numero():
    return jsonify(incomes[(random.randint(0, 1))])


@app.route('/estado')
def get_estado():
    return '', 200

if __name__ == '__main__':
    app.run()
