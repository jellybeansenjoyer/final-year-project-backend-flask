from flask import Flask,jsonify,request
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)
client = MongoClient('mongodb+srv://kashyap:kashyap@raghav.jvmxdco.mongodb.net/')
db = client['test']
collection_user_details = db['user_details']
collection_details = db['details']
collection_reviews = db['reviews']
# Schema for user_details collection
# Schema for user_details collection
user_details_schema = {
    "_id": {"type": "string", "auto": True},
    "title": {"type": "string"},
    "price": {"type": "string"},
    "picture": {"type": "string"},
    "technical-details": {
        "type": "dict",
        "schema": {
            "details_id": {"type": "string", "required": False}
        }
    },
    "details": {"type": "list", "schema": {"type": "string"}},
    "similar_products": {"type": "list", "schema": {"type": "string"}},
    "reviews": {"type": "list", "schema": {"type": "string"}}
}

# Schema for details collection
details_schema = {
    "_id": {"type": "string", "auto": True},
    "properties": {"type": "dict", "schema": {"type": "string"}}
}

# Schema for reviews collection
reviews_schema = {
    "_id": {"type": "string", "auto": True},
    "images": {"type": "list", "schema": {"type": "string"}},
    "review": {"type": "string"},
    "rating": {"type": "number"}
}

@app.route('/user_details', methods=['POST'])
def create_user_details():
    data = request.json
    if validate_user_details_schema(data):
        collection_user_details.insert_one(data)
        return jsonify({'message': 'User details created successfully'}), 201
    else:
        return jsonify({'error': 'Invalid user details schema'}), 400
from flask import jsonify
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
        if 'details_id' not in data['technical-details']:
            print("Missing 'details_id' in 'technical-details'")
            return False

    if 'details' in data:
        if not all(isinstance(detail, str) for detail in data['details']):
            print("Invalid value in 'details'")
            return False

    if 'similar_products' in data:
        if not all(isinstance(product_id, str) for product_id in data['similar_products']):
            print("Invalid value in 'similar_products'")
            return False

    if 'reviews' in data:
        if not all(isinstance(review_id, str) for review_id in data['reviews']):
            print("Invalid value in 'reviews'")
            return False

    return True


if __name__ == '__main__':
    app.run(debug=True)