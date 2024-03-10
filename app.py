from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson import ObjectId
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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

class ProductDetailsSchema(Schema):
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
    
    # Fetch details of each product from product_details collection
    product_details = []
    for product_id in user['products']:
        product = mongo.db.product_details.find_one_or_404({'_id': ObjectId(product_id)})
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
        product_details.append(product)
    
    # Replace product IDs with product details in the user document
    user['products'] = product_details
    
    return jsonify(user), 200
# Routes
@app.route('/product_details/', methods=['POST'])
def create_product_details():
    user_id = request.args.get('_id')
    if user_id is None or user_id.strip() == '':
        # If _id is null or blank, create a new entry in product_details
        json_data = request.json
        try:
            validated_data = ProductDetailsSchema().load(json_data)
            inserted_id = mongo.db.product_details.insert_one(validated_data).inserted_id
            return jsonify({'message': 'Product details created successfully', '_id': str(inserted_id)}), 201
        except ValidationError as e:
            return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400
    else:
        # If _id is valid, create a record in product_details and add the generated _id to userSchema's products list
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        
        json_data = request.json
        try:
            validated_data = ProductDetailsSchema().load(json_data)
            inserted_id = mongo.db.product_details.insert_one(validated_data).inserted_id
            product_id = str(inserted_id)
            print(product_id)
            # Update userSchema's products list with the new product id
            mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$push': {'products': product_id}})
            
            # Fetch the updated user data to ensure products list is up to date
            updated_user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            updated_user['_id'] = str(updated_user['_id'])  # Convert ObjectId to string
            
            return jsonify({'message': 'User details created successfully', '_id': product_id, 'user': updated_user}), 201
        except ValidationError as e:
            return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

@app.route('/product_details/<id>', methods=['GET'])
def get_product_details(id):
    product_details = mongo.db.product_details.find_one_or_404({'_id': ObjectId(id)})
    product_details['_id'] = str(product_details['_id'])  # Convert ObjectId to string
    return jsonify(product_details), 200

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

@app.route('/product_details', methods=['GET'])
def get_all_product_details():
    product_details = list(mongo.db.product_details.find({}))  # Retrieve all documents from product_details collection
    for user_detail in product_details:
        user_detail['_id'] = str(user_detail['_id'])  # Convert ObjectId to string for each document
    return jsonify(product_details), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(mongo.db.users.find({}))  # Retrieve all documents from product_details collection
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for each document
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)
