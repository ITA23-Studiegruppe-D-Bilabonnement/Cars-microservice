from flask import Flask, jsonify, request
import requests
import sqlite3
import os 
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity 
from dotenv import load_dotenv
from flasgger import swag_from 


# Load environment variables 
load_dotenv()

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
DB_PATH = os.getenv('SQLITE_DB_PATH')
PORT = int(os.getenv('PORT', 5000))
jwt = JWTManager(app)


# Database creation
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS cars 
                    (
                    car_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    car_brand TEXT NOT NULL, 
                    car_model TEXT NOT NULL, 
                    is_rented BOOLEAN, 
                    price INTEGER, 
                    color TEXT NOT NULL, 
                    engine_type TEXT NOT NULL, 
                    mileage INTEGER 
                    )""")
    conn.commit()

# Initialize the database when the app starts
init_db()
    
# Homepoint 
@app.route("/")
def homepoint():
    return jsonify({
        "SERVICE": "CARS MICROSERVICE",
        "AVAILABLE ENDPOINTS": [
            {
                "PATH": "/cars",
                "METHOD": "GET",
                "DESCRIPTION": "Returns a list of all cars"
            },
            {
                "PATH": "/add-car",
                "METHOD": "POST",
                "DESCRIPTION": "Registers new car in the database",
                "BODY": {
                    "car_brand": "STRING",
                    "car_model": "STRING",
                    "price": "INTEGER",
                    "color": "STRING",
                    "engine_type": "STRING",
                    "mileage": "STRING"
                }
            },
            {
                "PATH": "/delete-car/car_id",
                "METHOD": "DELETE",
                "DESCRIPTION": "Deletes ID-specific car from the database",
                "PARAMETER": "car_id"
            },
            {
                "PATH": "/brand-filter/car_brand",
                "METHOD": "GET",
                "DESCRIPTION": "Filters list of cars from car brand",
                "PARAMETER": "car_brand"
            },
            {
                "PATH": "/engine-filter/engine_type",
                "METHOD": "GET",
                "DESCRIPTION": "Filters list of cars from engine type",
                "PARAMETER": "engine_type"
            },
            {
                "PATH": "/color-filter/color",
                "METHOD": "GET",
                "DESCRIPTION": "Filters list of cars from car color",
                "PARAMETER": "color"
            },
            {
                "PATH": "/price-filter/min_price/max_price",
                "METHOD": "GET",
                "DESCRIPTION": "Filters list of cars from minimum price to maximum price",
                "PARAMETER": "min_price & max_price",
            } 
        ]
    })

# View all cars
@app.route("/cars", methods=['GET'])
def show_all_cars():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # This allows rows to be accessed as dictionaries
        c = conn.cursor()
        c.execute("SELECT * FROM cars")
        cars = [dict(row) for row in c.fetchall()]
    conn.close
    return jsonify(cars), 200 

#Add a car to the database
@app.route("/add-car", methods=['POST'])
def add_car():
    data = request.get_json()

    # Check that all data has been inserted
    required_fields = ["car_brand", "car_model", "price", "color", "engine_type", "mileage"]
    for field in required_fields: 
        if field not in data: 
            return jsonify({"error": f"'{field}' is required"}), 400
        
    # Extract fields from the request
    car_brand = data["car_brand"]
    car_model = data["car_model"]
    is_rented = data.get("is_rented", 0)  # Default to 0 (False)
    price = data["price"]
    color = data["color"]
    engine_type = data["engine_type"]
    mileage = data["mileage"]
 
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO cars (
                    car_brand, 
                    car_model, 
                    is_rented, 
                    price, 
                    color, 
                    engine_type, 
                    mileage
                    ) VALUES (?,?,?,?,?,?,?) ''', (car_brand, car_model, is_rented, price, color, engine_type, mileage))
            
        conn.commit()
        return jsonify({
            "message": "Car added successfully"
            }), 200
#Måske noget error handling?? Spørg rassermus!
        

# Delete car from database 
@app.route("/delete-car/<int:car_id>", methods=['DELETE'])
def delete_car(car_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM cars WHERE car_id = ?", (car_id,))

        #Check to see if the database was affected
        if cur.rowcount == 0:
            return jsonify({
                "Error": "Couldnt find car"
            }), 400
        
        return jsonify({
            "message": f"Car with ID: {car_id} succesfully deleted"
            }), 200
        

# FILTER 

#Filter on car brand
@app.route("/brand-filter/<car_brand>", methods=['GET'])
def brand_filter(car_brand):
    with sqlite3.connect(DB_PATH) as conn:
        
        #Access rows as dictionaries
        conn.row_factory = sqlite3.Row 

        cur = conn.cursor()
        cur.execute("SELECT * FROM cars WHERE car_brand = ?", (car_brand,))
        rows = cur.fetchall()

    #Convert rows to a list of dictionaries
    cars = [dict(row) for row in rows]

    #Return the filtered cars
    return jsonify(cars), 200

#Filter on engine type
@app.route("/engine-filter/<engine_type>", methods=['GET'])
def engine_filter(engine_type):
    with sqlite3.connect(DB_PATH) as conn:

        #Access rows as dictionaries
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("SELECT * FROM cars WHERE engine_type = ?", (engine_type,))
        rows = cur.fetchall()

    #Convert rows to a list of dictionaries
    cars = [dict(row) for row in rows]

    return jsonify(cars), 200

#Filter on color 
@app.route("/color-filter/<color>", methods=['GET'])
def color_filter(color):
    with sqlite3.connect(DB_PATH) as conn:
    
        #Access rows as dictionaries
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("SELECT * FROM cars WHERE color = ?", (color,))
        rows = cur.fetchall()

    #Convert rows to a list of dictionaries
    cars = [dict(row) for row in rows]

    return jsonify(cars), 200

# Filter on price 
@app.route("/price-filter/<int:min_price>/<int:max_price>", methods=['GET'])
def price_filter(min_price, max_price):
    with sqlite3.connect(DB_PATH) as conn:

        #Access rows as dictionaries
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("SELECT * FROM cars WHERE price BETWEEN ? AND ?", (min_price, max_price))
        rows = cur.fetchall()

    #Convert rows to a list of dictionaries
    cars = [dict(row) for row in rows]

    return jsonify(cars), 200
    
 
app.run(debug=True)
