
from flasgger import Swagger

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "specs": [
                {
                    "endpoint": 'cars',
                    "route": '/cars',
                    "spec": '/swagger/cars.yaml'
                },
                {
                    "endpoint": 'add car',
                    "route": '/add-cars',
                    "spec": '/swagger/add_car.yaml'
                },
                {
                    "endpoint": 'delete car',
                    "route": '/delete-car/<int:car_id>',
                    "spec": '/swagger/delete_car.yaml'
                },
                {
                    "endpoint": 'get specific car',
                    "route": '/car/<int:car_id>',
                    "spec": '/swagger/specific_car.yaml'

                },
                {
                    "endpoint": 'update status on car',
                    "route": '/update-status/<int:car_id>',
                    "spec": '/swagger/update_status.yaml'
                },
                {
                    "endpoint": 'list of rented cars',
                    "route": '/rented-cars',
                    "spec": '/swagger/rented_cars.yaml'
                },
                {
                    "endpoint": 'total price of rented cars',
                    "route": '/totalprice',
                    "spec": '/swagger/totalprice.yaml'
                },
                {
                    "endpoint": 'filter on car brand',
                    "route": '/brand-filter/<car_brand>',
                    "spec": '/swagger/filter_car_brand.yaml'
                },
                {
                    "endpoint": 'filter on car engine type',
                    "route": '/engine-filter/<engine_type>',
                    "spec": '/swagger/filter_car_engine.yaml'
                },
                {
                    "endpoint": 'filter on car color',
                    "route": '/color-filter/<color>',
                    "spec": '/swagger/filter_car_color.yaml'
                },
                {
                    "endpoint": 'filter on price of car',
                    "route": '/price_filter/<int:min_price>/<int:max_price>',
                    "spec": '/swagger/filter_car_price.yaml'
                },

            ],
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

template = {
    "info": {
        "title": "Cars microservice",
        "description": "Cars microservice that handles cars",
        "version": "1.0.0",
        "contact": {
            "name": "KEA",
            "url": "https://kea.dk"
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
        }
    }
}

def init_swagger(app):
    """Initialize Swagger with the given Flask app"""
    return Swagger(app, config=swagger_config, template=template)