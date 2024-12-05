from flask import Flask, jsonify, request
import requests
import sqlite3
import os 
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity 
from dotenv import load_dotenv
from flasgger import swag_from 
from swagger.swagger_config import init_swagger


#Load environment variables 
load_dotenv()

app = Flask(__name__)

#JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
DB_PATH = os.getenv('SQLITE_DB_PATH')
PORT = int(os.getenv('PORT', 5000))
jwt = JWTManager(app)

#Initialize Swagger
init_swagger(app)

#Database creation
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

#View all cars
@app.route("/cars", methods=['GET'])
@swag_from("swagger/cars.yaml")
def show_all_cars():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row  #This allows rows to be accessed as dictionaries
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            cars = [dict(row) for row in c.fetchall()]
        conn.close
        return jsonify(cars), 200 
    except Exception as e: #Catch errors
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500

#Add a car to the database
@app.route("/add-car", methods=['POST'])
@swag_from("swagger/add_car.yaml")
def add_car():
    try:
        data = request.get_json()

        #Check that all data has been inserted
        required_fields = ["car_brand", "car_model", "price", "color", "engine_type", "mileage"]
        for field in required_fields: 
            if field not in data or not data[field]: 
                return jsonify({
                    "error": f"'{field}' is required"
                    }), 400
            
        #Extract fields from the request
        car_brand = data["car_brand"]
        car_model = data["car_model"]
        is_rented = data.get("is_rented", 0)  #Default to 0 (False)
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
        
    except Exception as e:  # Catch other possible errors
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500

# Delete car from database 
@app.route("/delete-car/<int:car_id>", methods=['DELETE'])
@swag_from("swagger/delete_car.yaml")
def delete_car(car_id):
    try:
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
        
    except Exception as e:  #General error
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500
    

#Get list of rented cars 
@app.route("/rented-cars", methods=['GET'])
@swag_from("swagger/rented_cars.yaml")
def rented_cars():
    try:
        with sqlite3.connect(DB_PATH) as conn: 

            #Access rows as dictionaries
            conn.row_factory = sqlite3.Row

            cur = conn.cursor()
            cur.execute("SELECT * FROM cars where is_rented = 1")
            rows = cur.fetchall()
        
        #Convert rows to a list of dictionaries
        cars = [dict(row) for row in rows]

        #Check if no cars are rented
        if not cars:
            return jsonify({
                "message": "No cars are rented"
            }), 404 
        
        #Return the list of rented cars
        return jsonify(cars), 200
    
    except Exception as e: 
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500
    

#Get total price of rented cars 
@app.route("/totalprice", methods=['GET'])
@swag_from("swagger/totalprice.yaml")
def totalprice():
    try:
        with sqlite3.connect(DB_PATH) as conn: 
            cur = conn.cursor()
            cur.execute("SELECT SUM(price) FROM cars WHERE is_rented = 1")
            total = cur.fetchone()[0]

            #Check if no cars are rented (Total is None)
            if total is None:
                total = 0 #Default to 0

        return jsonify({
        "message": f"Total price of rented cars: {total}"
    }), 200

    except Exception as e: 
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
        }), 500


# FILTER 

#Filter on car brand
@app.route("/brand-filter/<car_brand>", methods=['GET'])
@swag_from("swagger/filter_car_brand.yaml")
def brand_filter(car_brand):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            
            #Access rows as dictionaries
            conn.row_factory = sqlite3.Row 

            cur = conn.cursor()
            cur.execute("SELECT * FROM cars WHERE car_brand = ?", (car_brand,))
            rows = cur.fetchall()

        #Convert rows to a list of dictionaries
        cars = [dict(row) for row in rows]

        #Check if no cars match the filter
        if not cars:
            return jsonify({
                "message": f"No cars found for brand: '{car_brand}'"
                }), 404

        #Return the filtered cars
        return jsonify(cars), 200
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500

#Filter on engine type
@app.route("/engine-filter/<engine_type>", methods=['GET'])
@swag_from("swagger/filter_car_engine.yaml")
def engine_filter(engine_type):
    try: 
        with sqlite3.connect(DB_PATH) as conn:

            #Access rows as dictionaries
            conn.row_factory = sqlite3.Row

            cur = conn.cursor()
            cur.execute("SELECT * FROM cars WHERE engine_type = ?", (engine_type,))
            rows = cur.fetchall()

        #Convert rows to a list of dictionaries
        cars = [dict(row) for row in rows]

        #Check if no cars match the filter
        if not cars:
            return jsonify({
                "message": f"No cars found with engine: '{engine_type}'"
                }), 404
        
        #Return the filtered cars
        return jsonify(cars), 200
    
    except Exception as e: 
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500

#Filter on color 
@app.route("/color-filter/<color>", methods=['GET'])
@swag_from("swagger/filter_car_color.yaml")
def color_filter(color):
    try: 
        with sqlite3.connect(DB_PATH) as conn:
        
            #Access rows as dictionaries
            conn.row_factory = sqlite3.Row

            cur = conn.cursor()
            cur.execute("SELECT * FROM cars WHERE color = ?", (color,))
            rows = cur.fetchall()

        #Convert rows to a list of dictionaries
        cars = [dict(row) for row in rows]

        #Check if no cars match the filter
        if not cars: 
            return jsonify({
                "message": f"No cars found with the color: '{color}'"
                }), 404 
        
        #Return the filtered cars
        return jsonify(cars), 200
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500

#Filter on price 
@app.route("/price-filter/<int:min_price>/<int:max_price>", methods=['GET'])
@swag_from("swagger/filter_car_price.yaml")
def price_filter(min_price, max_price):
    try: 
        with sqlite3.connect(DB_PATH) as conn:

            #Access rows as dictionaries
            conn.row_factory = sqlite3.Row

            cur = conn.cursor()
            cur.execute("SELECT * FROM cars WHERE price BETWEEN ? AND ?", (min_price, max_price))
            rows = cur.fetchall()

        #Convert rows to a list of dictionaries
        cars = [dict(row) for row in rows]

        #Check if no cars match the filter
        if not cars: 
            return jsonify({
                "message": f"No cars found within price range: '{min_price}' and '{max_price}'"
            }), 404
        
        #Return the filtered cars
        return jsonify(cars), 200
    
    except Exception as e:
        return jsonify({
            "error": "OOPS! Something went wrong :(", "details": str(e)
            }), 500



if __name__ == "__main__":    
    app.run(debug=True)
