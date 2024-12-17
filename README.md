# Cars Microservice

This Flask-based microservice provides an API for managing car data, including viewing, filtering, adding, and deleting cars in a database.

---

## File structure
```
project/
├── app.py                   
├── swagger/                 
│   ├── add_car.yaml          
│   ├── cars.yaml           
│   ├── specific_car.yaml
│   ├── delete_car.yaml
│   ├── rented_cars.yaml
│   ├── update_status.yaml
│   ├── totalprice.yaml
│   ├── filter_car_brand.yaml
│   ├── filter_car_color.yaml
│   ├── filter_car_engine.yaml
│   ├── filter_car_price.yaml  
│   └── swagger_config.py      
├── .dockerignore            
├── .env                     
├── .github/                 
│   └── workflows/           
│       └── main_Cars-microservice.yml 
├── .gitignore               
├── Dockerfile               
├── README.md                
├── requirements.txt
```

## Endpoints

| HTTP Method | Action                        | Example Endpoint                        | Notes                                         |
|-------------|-------------------------------|-----------------------------------------|----------------------------------------------|
| `GET`       | Get all cars                  | `/cars`                                 | Retrives a list of all the cars              |
| `POST`      | Add a new car                 | `/add-car`                              | Registers a new car in the database.         |
| `DELETE`    | Delete a car                  | `/delete-car/<car_id>`                  | Deletes a car by its unique ID.              |
| `GET`       | Get car details by ID         | `/car/<int:car_id>`                     | Retrieves details of a car by its ID.        |
| `PUT`       | Update car rental status      | `/update-status/<int:car_id>`           | Toggles the `is_rented` status of a car.     |
| `GET`       | List all rented cars          | `/rented-cars`                          | Retrieves a list of cars currently rented.   |
| `GET`       | Get total price of rented cars| `/totalprice`                           | Calculates and returns the total rental price.|
| `GET`       | Filter cars by brand          | `/brand-filter/<car_brand>`             | Retrieves cars matching a specific brand.    |
| `GET`       | Filter cars by engine type    | `/engine-filter/<engine_type>`          | Retrieves cars with a specific engine type.  |
| `GET`       | Filter cars by color          | `/color-filter/<color>`                 | Retrieves cars matching a specific color.    |
| `GET`       | Filter cars by price range    | `/price-filter/<min_price>/<max_price>` | Retrieves cars within a specific price range.|



### **Homepoint**

- **URL**: `/`
- **Method**: GET
- **Description**: Displays service information and available endpoints.
- **Response**:
    - `200 OK`: Returns a JSON object with service details and endpoints.

---

### **View All Cars**

- **URL**: `/cars`
- **Method**: GET
- **Description**: Retrieves a list of all cars in the database.
- **Response**:
    - `200 OK`: Returns a list of all cars in JSON format.

---

### **Add a New Car**

- **URL**: `/add-car`
- **Method**: POST
- **Description**: Registers a new car in the database.
- **Request Body**:
```json
{
    "car_brand": "STRING",
    "car_model": "STRING",
    "price": "INTEGER",
    "color": "STRING",
    "engine_type": "STRING",
    "mileage": "INTEGER"
}
```
---

### **Delete a Car**

- **URL**: `/delete-car/<car_id>`
- **Method**: DELETE
- **Description**: Deletes a car from the database by its unique ID.
- **Response**:
    - `200 OK`: Car successfully deleted.
    - `400 Bad Request`: Car with the specified ID was not found.

---

### **Get car by ID**

- **URL**: `/car/<int:car_id>`
- **Method**: GET
- **Description**: Shows details of a car from the database by its unique ID.
- **Response**: 
    - `200 OK`: Returns car details.
    - `400 Bad Request`: Car with the specified ID was not found. 

---

### **Update Car Status**

- **URL**: `/update-status/<int:car_id>`
- **Method**: PUT
- **Description**: Toggles the rental status (`is_rented`) of a specific car by its unique ID.
- **Response**:
    - `200 OK`: Car rental status successfully updated.
    - `500 Internal Server Error`: An error occurred while updating the car status.

---

### **Get List of Rented Cars**

- **URL**: `/rented-cars`
- **Method**: GET
- **Description**: Retrieves a list of all cars currently rented.
- **Response**:
    - `200 OK`: Returns a list of rented cars in JSON format.
    - `404 Not Found`: No cars are currently rented.
    - `500 Internal Server Error`: An error occurred while retrieving the rented cars.

---

### **Get Total Price of Rented Cars**

- **URL**: `/totalprice`
- **Method**: GET
- **Description**: Calculates and returns the total price of all currently rented cars.
- **Response**:
    - `200 OK`: Returns the total price of rented cars in JSON format.
    - `500 Internal Server Error`: An error occurred while calculating the total price.
    
---

### **Filter Cars by Brand**

- **URL**: `/brand-filter/<car_brand>`
- **Method**: GET
- **Description**: Retrieves cars filtered by their brand.
- **Response**:
    - `200 OK`: Returns a list of cars that match the specified brand.

---

### **Filter Cars by Engine Type**

- **URL**: `/engine-filter/<engine_type>`
- **Method**: GET
- **Description**: Retrieves a list of cars filtered by their engine type.
- **Response**:
    - `200 OK`: Returns a list of cars that match the specified engine type.

---

### **Filter Cars by Color**

- **URL**: `/color-filter/<color>`
- **Method**: GET
- **Description**: Retrieves a list of cars filtered by their color.
- **Response**:
    - `200 OK`: Returns a list of cars that match the specified color.

---

### **Filter Cars by Price Range**

- **URL**: `/price-filter/<min_price>/<max_price>`
- **Method**: GET
- **Description**: Retrieves a list of cars within a specified price range.
- **Response**:
    - `200 OK`: Returns a list of cars that fall within the specified price range.
  
 ## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET_KEY` | Yes | - | Secret key for JWT token generation |
| `PORT` | No | 5000 | Port to run the service on |
| `SQLITE_DB_PATH` | Yes | - | Path to SQLite database file |


## Database

The service uses SQLite for persistent user storage. The database schema is as follows:

| Column      | Type      | Constraints          |
|-------------|-----------|----------------------|
| `car_id`        | INTEGER   | PRIMARY KEY AUTOINCREMENT |
| `car_brand`     | TEXT      | NOT NULL      |
| `car_model`| TEXT      | NOT NULL             |
| `is_rented` | BOOLEAN      |              |
| `price`  | INTEGER      |              |
| `color`     | TEXT      | NOT NULL      |
| `engine_type`     | TEXT      | NOT NULL      |
| `milage`     | INTEGER      |      |


