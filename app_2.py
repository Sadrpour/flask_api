from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = '1234'
api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth end point is created

items = []

class Item(Resource):
    @jwt_required()

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True, help="this field has to be passed")
    parser.add_argument(
        'name', type=str, required=False, help="this field does not to be passed")


    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return item if item else {'Error': "Item not found! 404"}


    def post(self, name):
        # request_data = request.get_json()
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'Warning': 'the item already exists'}
        request_data = Item.parser.parse_args()
        item = {'name': request_data['name'], 'price': request_data['price']}
        items.append(item)
        return item


    def put(self, name):
        # request_data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        request_data = Item.parser.parse_args()
        if item:
            item.update(request_data) # this will update the fields by values you passed by request !
            return item
        else:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
            return {"message": "requested item added"}


    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "item deleted"}


class Items(Resource):
    def get(self):
        return items


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')


app.run(port=5000, debug=True)
