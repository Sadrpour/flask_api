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

        request_data = self.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occured inserting"}

        return item

    def put(self, name):
        item = Item.find_item_by_name(name)
        request_data = self.parser.parse_args()
        updated_item = {'name': name, 'price': request_data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
                updated_item.update({"message": "inserted item"})
                return updated_item
            except Exception as e:
                return {"message": "Failed to insert due to {}".format(e)}
        else:
            try:
                Item.update(updated_item)
                updated_item.update({"message": "updated item"})
                return updated_item
            except Exception as e:
                return {"message": "Failed to update due to {}".format(e)}

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


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        return {"result": items}

        connection.commit()
        connection.close()
