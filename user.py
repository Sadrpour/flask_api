import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password


    @classmethod
    def find_by_username(cls, username):  #without decorator cls = self
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


    @classmethod
    def find_by_id(cls, _id):  #without decorator cls = self
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str, required=True, help="this field has to be passed")
    parser.add_argument(
        'password', type=str, required=True, help="this field has to be passed")

    @classmethod
    def post(cls):
        request_data = cls.parser.parse_args()
        if User.find_by_username(request_data['username']): # note user is not an instance of User class, it is like np.rand(), you call a method from a class and pass values to it
            return {"message": "user already exist"}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (request_data['username'], request_data['password']))

        connection.commit()  #saving to disc
        connection.close()

        return {"message": "user created successfully"}



