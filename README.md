# Cars Microservice

This Flask-based microservice provides an API for managing car data, including viewing, filtering, adding, and deleting cars in a database.

---

# File structure
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


