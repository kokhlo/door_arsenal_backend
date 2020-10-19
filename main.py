import json
import copy
import datetime
import unittest
import settings
import logger
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from mongoengine.context_managers import query_counter
from mongoengine.errors import ValidationError
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

db = SQLAlchemy(app)
api = Api(app)
api.prefix = '/api/v2'
CORS(app)
door_logger = logger.logger

ORDERS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

MEASUREMENTS = {
    'uuid16-1': {
        'name': 'Илья',
        'phone': '+79621671488',
        'email': 'test@mail.ru',
        'type': 'doors',
        'cart': {},
        'address': 'Тула, Матросова-Комбайновая',
        'ip': '255.255.255.254',
        'geo_from_ip': 'Tula region',
        'registration_date': 'Sun 27 Sep 2020 19:19:22 MSK',
    },
    'uuid16-2': {
        'name': 'Илья',
        'phone': 'build an API',
        'email': 'build an API',
        'type': 'buildings',
        'cart': {},
        'address': 'build an API',
        'ip': 'build an API',
        'geo_from_ip': 'build an API',
        'registration_date': 'Sun 27 Sep 2020 19:19:23 MSK',
    },
    'uuid16-3': {
        'name': 'Илья',
        'phone': 'build an API',
        'email': 'build an API',
        'type': 'doors',
        'cart': {},
        'address': 'build an API',
        'ip': 'build an API',
        'geo_from_ip': 'build an API',
        'registration_date': 'Sun 27 Sep 2020 19:19:24 MSK',
    },
}

GOODS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

BUYINGS = {
    'uuid16-1': {
        'name': 'Google Adwords',
        'qty': '1',
        'category': 'advertisment',
        'price': '50000',
        'date': 'Sun 27 Sep 2020 14:24:01 MSK'
    },
    'uuid16-2': {
        'name': 'Workers',
        'qty': '3',
        'category': 'employees',
        'price': '7500',
        'date': 'Sun 27 Sep 2020 14:24:01 MSK'
    },
    'uuid16-3': {
        'name': 'Repair a PS4',
        'qty': '1',
        'category': 'repairments',
        'price': '359',
        'date': 'Sun 27 Sep 2020 14:24:01 MSK'
    }
}

USERS = {
    'uuid16-1': {
        'name': 'Пётр Иванов',
        'phone': '+7(960)5051883',
        'email': 'test@gmail.com',
        'address': 'Тула, Красина, 15/2',
        'ip': '14.88.359.282',
        'geo_for_ip': 'Tula region',
        'role': 'buyer',
        'active': 'active',
        'registration_date': 'Sun 27 Sep 2020 14:24:01 MSK'
    },
    'uuid16-2': {
        'name': 'Пётр Иванов',
        'phone': '+7(960)5051883',
        'email': 'test@gmail.com',
        'address': 'Тула, Красина, 15/2',
        'ip': '14.88.359.282',
        'geo_for_ip': 'Tula region',
        'role': 'buyer',
        'active': 'active',
        'registration_date': 'Sun 27 Sep 2020 14:24:01 MSK'
    },
    'uuid16-3': {
        'name': 'Пётр Иванов',
        'phone': '+7(960)5051883',
        'email': 'test@gmail.com',
        'address': 'Тула, Красина, 15/2',
        'ip': '14.88.359.282',
        'geo_for_ip': 'Tula region',
        'role': 'buyer',
        'active': 'active',
        'registration_date': 'Sun 27 Sep 2020 14:24:01 MSK'
    }
}

def abort_if_order_doesnt_exist(order_id):
    if order_id not in ORDERS:
        abort(404, message="Order #{} doesn't exist".format(order_id))

def abort_if_measurement_doesnt_exist(measurement_id):
    if measurement_id not in MEASUREMENTS:
        abort(404, message="Measurement {} doesn't exist".format(measurement_id))

def abort_if_good_doesnt_exist(good_id):
    if good_id not in GOODS:
        abort(404, message="good {} doesn't exist".format(good_id))

def abort_if_buying_doesnt_exist(buying_id):
    if buying_id not in BUYINGS:
        abort(404, message="Buying {} doesn't exist".format(buying_id))

def abort_if_user_doesnt_exist(user_id):
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

# Orders
#   show a single order item and lets you delete them
class Orders(Resource):
    # Read
    def get(self, order_id):
        abort_if_order_doesnt_exist(order_id)
        return ORDERS[order_id]
    # Delete
    def delete(self, order_id):
        abort_if_order_doesnt_exist(order_id)
        del ORDERS[order_id]
        return '', 204
    # (PATCH) Update
    def put(self, order_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ORDERS[order_id] = task
        return task, 201
    # Create
    def post(self, order_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ORDERS[order_id] = task
        return task, 201


# Measurements
#   shows a list of all todos, and lets you POST to add new tasks
class Measurements(Resource):
    # Read
    def get(self):
        return MEASUREMENTS
    # Create
    def post(self):
        args = parser.parse_args()
        measurement_id = 'todo%d' % (len(MEASUREMENTS) + 1)
        MEASUREMENTS[measurement_id] = {'task': args['task']}
        return MEASUREMENTS[measurement_id], 201
    # Delete
    def delete(self, measurement_id):
        abort_if_order_doesnt_exist(measurement_id)
        del MEASUREMENTS[measurement_id]
        return '', 204
    # (PATCH) Update
    def put(self, measurement_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ORDERS[order_id] = task
        return task, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(Orders, '/orders/<string:order_id>')
api.add_resource(Measurements, '/measurements/<string:measurement_id>')
api.add_resource(Goods, '/goods/<string:good_id>')
api.add_resource(Buyings, '/buyings/<string:buying_id>')
api.add_resource(Users, '/users/<string:user_id>')


door_logger.info('init, stage 0, successfully')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5555', debug=True)