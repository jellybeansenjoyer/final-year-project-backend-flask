from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson import ObjectId
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape(url):
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        # Wait for the product title element to be visible
        product_title_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "productTitle"))
        )
        
        # Extract the product title text
        product_title_text = product_title_element.text.strip()
        print("Title:", product_title_text)
        
        # Find the price element
        price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "a-price-whole"))
        )
        
        # Extract the price text
        price_text = price_element.text.strip()
        print("Price:", price_text)
        
        # Wait for the list of span elements to be present
        spans = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.a-unordered-list.a-vertical.a-spacing-mini span.a-list-item"))
        )
        
        # Extract the text from each span and store it in a list
        text_list = [span.text.strip() for span in spans]
        print("List of Texts inside Span elements:")
        print("Details:", text_list)
        
        # Get the HTML of the table
        table_html = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "productDetails_techSpec_section_1"))
        ).get_attribute("innerHTML")
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(table_html, "html.parser")
        
        # Find all rows in the table
        rows = soup.find_all("tr")
        
        # Create an empty dictionary to store name-value pairs
        data_dict = {}
        
        # Loop through each row
        for row in rows:
            # Find the header and data cells
            header_cell = row.find("th")
            data_cell = row.find("td")
            
            # Extract the text from header and data cells
            if header_cell and data_cell:
                header_text = header_cell.text.strip()
                data_text = data_cell.text.strip()
                
                # Add the name-value pair to the dictionary
                data_dict[header_text] = data_text
                
        # Print the dictionary
        print("Technical Specifications:")
        
        cleaned_data_dict = {}

        # Iterate through each key-value pair in the original dictionary
        for key, value in data_dict.items():
            # Remove special characters from the value
            cleaned_value = value.strip('\u200e')
            # Add the cleaned key-value pair to the new dictionary
            cleaned_data_dict[key] = cleaned_value

        # Print the cleaned dictionary
        print("Cleaned Technical Specifications:")
        print(cleaned_data_dict)

    except Exception as e:
        print("An error occurred:", e)
    try:
        # Wait for the product details table to be visible
        table_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "productDetails_detailBullets_sections1"))
        )
        
        # Get the HTML content of the table
        table_html = table_element.get_attribute('innerHTML')
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find_all('tr')
        
        # Create an empty dictionary to store the extracted data
        data_dict = {}
        
        # Loop through each row
        for row in rows:
            # Find the header and data cells
            header_cell = row.find('th')
            data_cell = row.find('td')
            
            # Extract the text from header and data cells
            if header_cell and data_cell:
                header_text = header_cell.text.strip()
                data_text = data_cell.text.strip()
                
                # Add the name-value pair to the dictionary
                data_dict[header_text] = data_text
        
        # Print the extracted data dictionary
        print("Technical_Details:")
        cleaned_data_dict.update(data_dict)
        print(cleaned_data_dict)
    except Exception as e:
        print("An error occurred:", e)
        

    try:
        # Wait for the div element to be visible
        div_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "wayfinding-breadcrumbs_feature_div"))
        )
        
        # Get the HTML content of the div
        div_html = div_element.get_attribute('innerHTML')
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(div_html, 'html.parser')
        
        # Find the ul element inside the div
        ul_element = soup.find('ul', class_='a-unordered-list')
        
        a_tag = ul_element.find('a')
        # Extract the text of the <a> tag
        if a_tag:
            a_tag_text = a_tag.text.strip()
            print("Category:", a_tag_text)
        else:
            print("No <a> tag found within the <ul> element.")

    except Exception as e:
        print("An error occurred:", e)    # Quit the driver
    try:
    # Wait for the image element to be visible
        image_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "landingImage"))
        )

        # Extract the image source URL
        image_url = image_element.get_attribute("src")
        print("Image URL:", image_url)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()
    return {
            "title": product_title_text,
            "price": price_text,
            "technical_details": cleaned_data_dict,
            "details": text_list,
            "category": a_tag_text,
            "url": url,
            "picture":image_url
        }


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = 'mongodb+srv://kashyap:kashyap@raghav.jvmxdco.mongodb.net/test2'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

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
    technical_details = fields.Dict()
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
    password = fields.String(required=True,load_only=True)
    emailid = fields.String(required=True)
    address = fields.String(required=True)
    phone_number = fields.String(required=True)
    description = fields.String(required=True)
    products = fields.List(fields.String())

# Routes
@app.route('/signUp', methods=['POST'])
def create_user():
    json_data = request.json
    try:
        validated_data = UserSchema().load(json_data)
        validated_data['password'] = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
        inserted_id = mongo.db.users.insert_one(validated_data).inserted_id
        return jsonify({'message': 'User created successfully', '_id': str(inserted_id)}), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400

@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    email = json_data.get('emailid', None)
    password = json_data.get('password', None)
    user = mongo.db.users.find_one({'emailid': email})
    if user and bcrypt.check_password_hash(user['password'], password):
        # Return user id upon successful login
        return jsonify({'user_id': str(user['_id']), 'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401
    
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
@app.route('/product_details', methods=['POST'])
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


# Flask route to create product details
@app.route('/product_details_scrape', methods=['POST'])
def create_product_details_scrape():
    user_id = request.args.get('_id')
    if user_id is None or user_id.strip() == '':
        url = request.json.get('url')  
        scraped_data = scrape(url)  
        try:
            validated_data = ProductDetailsSchema().load(scraped_data)
            inserted_id = mongo.db.product_details.insert_one(validated_data).inserted_id
            return jsonify({'message': 'Product details created successfully', '_id': str(inserted_id)}), 201
        except ValidationError as e:
            return jsonify({'error': 'Validation failed', 'messages': e.messages}), 400
    else:
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        url = request.json.get('url')  
        json_data = scrape(url)
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

from flask import jsonify

@app.route('/userProducts/<user_id>', methods=['GET'])
def get_user_products(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    product_ids = user.get('products', [])
    products = []
    for product_id in product_ids:
        product = mongo.db.product_details.find_one({'_id': ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])
            products.append(product)
    
    return jsonify(products), 200


# Additional route for testing the scrape function
@app.route('/scrape', methods=['GET'])
def scrape_test():
    try:
        scraped_data = scrape("https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B084JGJ8PF/ref=sr_1_4?keywords=bags&qid=1697885232&sr=8-4&th=1")
        return jsonify(scraped_data), 200
    except Exception as e:
        print("An error occurred during scraping:", e)
        return jsonify({'error': 'Scraping failed'}), 500
    
@app.route('/d',methods=['GET'])
def d():
    try:
        scrape("https://www.amazon.in/Wesley-Milestone-Waterproof-Backpack-Business/dp/B084JGJ8PF/ref=sr_1_4?keywords=bags&qid=1697885232&sr=8-4&th=1")
        return jsonify("success"), 200
    except:
        return 400
if __name__ == '__main__':
    app.run(debug=True)
