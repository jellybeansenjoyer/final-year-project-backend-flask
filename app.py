from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://kashyap:kashyap@raghav.jvmxdco.mongodb.net/test2'
mongo = PyMongo(app)

# Define schemas using Marshmallow
class TechnicalDetailSchema(Schema):
    property = fields.String(required=False)
    value = fields.String(required=True)

class ReviewSchema(Schema):
    _id = fields.String(dump_only=True)
    title = fields.String(required=True)
    images = fields.List(fields.String(), required=False)
    review = fields.String()
    rating = fields.Float()

class UserDetailsSchema(Schema):
    _id = fields.String(dump_only=True)
    title = fields.String(required=True)
    price = fields.String(required=True)
    picture = fields.String(required=True)
    technical_details = fields.List(fields.Nested(TechnicalDetailSchema))
    details = fields.List(fields.String())
    similar_products = fields.List(fields.String())
    reviews = fields.Nested(ReviewSchema, many=True)
    original_price = fields.String()
    average_price = fields.String()
    highest_price = fields.String()
    lowest_price = fields.String()
    sentimental_score = fields.String()
    category = fields.String()
    url = fields.String()

class UserSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    emailid = fields.String(required=True)
    address = fields.String(required=True)
    phone_number = fields.String(required=True)
    description = fields.String(required=True)
    products = fields.List(fields.String())

# Routes
@app.route('/users', methods=['POST'])
def create_user():
    json_data = request.json
    try:
        validated_data = UserSchema().load(json_data)
        inserted_id = mongo.db.users.insert_one(validated_data).inserted_id
        return jsonify({'message': 'User created successfully', '_id': str(inserted_id)}), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one_or_404({'_id': ObjectId(id)})
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    
    # Fetch details of each product from user_details collection
    product_details = []
    for product_id in user['products']:
        product = mongo.db.user_details.find_one_or_404({'_id': ObjectId(product_id)})
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
        product_details.append(product)
    
    # Replace product IDs with product details in the user document
    user['products'] = product_details
    
    return jsonify(user), 200
# Routes
@app.route('/user_details', methods=['POST'])
def create_user_details():
    json_data = request.json
    try:
        validated_data = UserDetailsSchema().load(json_data)
        inserted_id = mongo.db.user_details.insert_one(validated_data).inserted_id
        return jsonify({'message': 'User details created successfully', '_id': str(inserted_id)}), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

@app.route('/user_details/<id>', methods=['GET'])
def get_user_details(id):
    user_details = mongo.db.user_details.find_one_or_404({'_id': ObjectId(id)})
    user_details['_id'] = str(user_details['_id'])  # Convert ObjectId to string
    return jsonify(user_details), 200

@app.route('/reviews', methods=['POST'])
def create_review():
    json_data = request.json
    try:
        validated_data = ReviewSchema().load(json_data)
        inserted_id = mongo.db.reviews.insert_one(validated_data).inserted_id
        return jsonify({'message': 'Review created successfully', '_id': str(inserted_id)}), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

@app.route('/', methods=['GET'])
def get_hello():
    return jsonify("hello"), 200

if __name__ == '__main__':
    app.run(debug=True)
