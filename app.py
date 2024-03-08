from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://kashyap:kashyap@raghav.jvmxdco.mongodb.net/test'
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
