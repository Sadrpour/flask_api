from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
    {'name': 'my store',
     'items':
         [{'name': 'shoes',
           'price': 15.99}]
     }
]


@app.route('/')  # http://www.google.com/
def home():
    return ("hello world")


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store', methods=['GET'])  # you do not need methods since GET is default
def get_store():  # http//127.0.0.1:5000/store/some_name  will return the value with key some_name
    return jsonify({'stores': stores})


@app.route('/store/<string:name>', methods=['GET'])  # you do not need methods since GET is default
def get_store_name(name):  # http//127.0.0.1:5000/store/some_name  will return the value with key some_name
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'Error': "store not found"})


@app.route('/store/<string:name>/item', methods=['POST'])  # you do not need methods since GET is default
def create_item_in_store(name):  # http//127.0.0.1:5000/store/some_name  will return the value with key some_name
    request_data = request.get_json()
    print(request_data)
    for store in stores:
        if store['name'] == name:
            print(name)
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            print("i am here")
            store['items'].append(new_item)
            print("stored")
            return (jsonify(store))
    return (jsonify({"Error": "did not find the store"}))


@app.route('/store/<string:name>/item', methods=['GET'])  # you do not need methods since GET is default
def get_item_in_store(name):  # http//127.0.0.1:5000/store/some_name  will return the value with key some_name
    for store in stores:
        if store['name'] == name:
            return jsonify({"items": store["items"]})
        return jsonify({"Error": "store not found"})


app.run(port=5000)