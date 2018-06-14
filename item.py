from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True, help="this field has to be passed")
    parser.add_argument(
        'name', type=str, required=False, help="this field does not to be passed")


    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,))
        item = result.fetchone()
        connection.close()

        if item:
            return {"name": item[0], "price": item[1]}


    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()


    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()



    @jwt_required()  # i think this generates endpoint items/auth
    def get(self, name):  # name is passed by /endpoint/name automagically
        item = Item.find_item_by_name(name)
        if item:
            return item
        return {"message": "did not find the item"}


    def post(self, name):
        # request_data = request.get_json()
        item = Item.find_item_by_name(name)

        if item:
            return {'Warning': 'the item already exists'}

        request_data = cls.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}

        try:
            cls.insert(item)
        except:
            return {"message" : "An error occured inserting"}

        return item


    def put(self, name):
        item = Item.find_item_by_name(name)
        request_data = cls.parser.parse_args()
        udpated_item = {'name': name, 'price': request_data['price']}
        if item is None:
            try:
                cls.insert(udpated_item)
                return udpated_item.update({"message": "inserted item"})
            except:
                return {"message": "Failed to insert"}
        else:
            try:
                cls.udpate(udpated_item)
                return udpated_item.update({"message": "updated item"})
            except:
                return {"message": "Failed to update"}


    def delete(self, name):
        item = Item.find_item_by_name(name)
        if not item:
            return {"Message": "item does not exist"}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"Message": "{} removed".format(name)}


        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {"message": "item deleted"}


class Items(Resource):
    def get(self):
        return items
