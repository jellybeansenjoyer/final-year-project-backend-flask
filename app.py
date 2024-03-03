from flask import Flask,jsonify,request
from pymongo import MongoClient
from bson import ObjectId
from flask import jsonify

app = Flask(__name__)
client = MongoClient('mongodb+srv://kashyap:kashyap@raghav.jvmxdco.mongodb.net/')
db = client['test']
collection_user_details = db['user_details']
collection_user_reviews = db['reviews']

user_details_schema = {
    "_id": {"type": "string", "auto": True},
    "title": {"type": "string"},
    "price": {"type": "string"},
    "picture": {"type": "string"},
    "technical-details": { #list of objects to technical details
        "type": "list",
        "schema": {
            "type":"dict",
            "schema":{
            "property": {"type": "string", "required": False},
            "value": {"type": "string", "required": True},
        }
        }
    },
    "details": {"type": "list", "schema": {"type": "string"}}, #list of strings of description
    "similar_products": {"type": "list", "schema": {"type": "string"}}, #list of id of similar products which are user_details itself
    "reviews": {"type": "string"} #reference to reviews table
}


# Schema for reviews collection
reviews= {
    "_id": {"type": "string", "auto": True},
    "type": "list",
    "schema": {
        "type": "dict",
        "schema": {
            "title": {"type": "string", "required": True},
            "images": {"type": "list", "required": False},
            "review": {"type": "string"},
            "rating": {"type": "number"}
        }
    }
}

@app.route('/user_details', methods=['POST'])
def create_user_details():
    data = request.json
    if validate_user_details_schema(data):
        collection_user_details.insert_one(data)
        return jsonify({'message': 'User details created successfully'}), 201
    else:
        return jsonify({'error': 'Invalid user details schema'}), 400
    
def find_user_details_by_id(user_details_id, collection_user_details):
    try:
        # Convert the user_details_id string to ObjectId
        user_details_id = ObjectId(user_details_id)
        # Find the document by _id
        user_details = collection_user_details.find_one({'_id': user_details_id})
        if user_details:
            # Convert ObjectId to string
            user_details['_id'] = str(user_details['_id'])
            return user_details
        else:
            return None  # Document not found
    except Exception as e:
        print("Error:", e)
        return None  # Return None in case of any error
    
@app.route('/user_details/<id>', methods=['GET'])
def get_user_details(id):
    # Call the find_user_details_by_id function
    user_details = find_user_details_by_id(id, collection_user_details)
    
    if user_details:
        return jsonify(user_details), 200
    else:
        return jsonify({'error': 'User details not found'}), 400
    
@app.route('/', methods=['GET'])
def get_hello():
        return jsonify("hello"), 200

# Other CRUD routes...

def validate_user_details_schema(data):
    if 'title' not in data:
        print("Missing 'title' field")
        return False
    
    if 'price' not in data:
        print("Missing 'price' field")
        return False
    
    if 'picture' not in data:
        print("Missing 'picture' field")
        return False
    
    if 'technical-details' in data:
        if not isinstance(data['technical-details'], list):
            print("'technical-details' must be a list")
            return False
            
        for detail in data['technical-details']:
            if not isinstance(detail, dict):
                print("Invalid element in 'technical-details':", detail)
                return False
            if 'property' not in detail:
                print("Missing 'property' in 'technical-details' detail:", detail)
                return False
            if 'value' not in detail:
                print("Missing 'value' in 'technical-details' detail:", detail)

    if 'details' in data:
        if not isinstance(data['details'], list):
            print("'details' must be a list")
            return False
        if not all(isinstance(detail, str) for detail in data['details']):
            print("Invalid value in 'details'")
            return False

    if 'similar_products' in data:
        if not isinstance(data['similar_products'], list):
            print("'similar_products' must be a list")
            return False
        if not all(isinstance(product_id, str) for product_id in data['similar_products']):
            print("Invalid value in 'similar_products'")
            return False

    if 'reviews' in data:
        if not isinstance(data['reviews'], str):
            print("'reviews' must be a string")
            return False

    return True

if __name__ == '__main__':
    app.run(debug=True)