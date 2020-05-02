# Full Stack Deliver Me API 

## Getting Started

## API URL:

<https://deliverme1.herokuapp.com/materials>

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/DeliverMe` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

## Running the server

From within the `DeliverMe` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## API Reference

Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, <http://127.0.0.1:5000/,> which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

Premissions and Roles:
delivery_secretary role: materials (read), orders (read, add).
delivery_accountant role: materials (read, search, add, update), orders (read).
delivery_manager role: materials (read, search, add, update, delete) , orders (read, add, update , delete).

All requests require header authorization bearer key to access.

Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:
    400: Authentication error
    401: Unauthorized
    403: Access denied
    404: Resource Not Found
    405: Method not allowed
    500: Internal server error

## Access Token

You can use this URL to get Access Token(But this token will not contain any premissions):
<https://andalussoft.au.auth0.com/authorize?audience=deliver_me_api&scope=SCOPE&response_type=token&client_id=DC7ttqnyCgiuriyr3JGrENOu9NCnRFzp&redirect_uri=http://localhost:5000/&state=STATE>

## Endpoints

Get /materials
        General:
            Get all the materials
        Response:
            {
            "materials": [
                {
                "description": "desc1",
                "id": 1,
                "name": "mat1"
                },
                {
                "description": null,
                "id": 2,
                "name": "mat2"
                },
                {
                "description": "new material desc",
                "id": 3,
                "name": "new material "
                }
            ],
            "materials_count": 3,
            "success": true
            }

POST /materials
        General:
            Search for a material by passing the material's name or a portion of the material's name  in the request body, the searech is case insensitive.
        Request Body (type: 'application/json'):
            {
                "search":"mat1"
            }
        Response:
            {
            "materials": [
                {
                "description": "desc1",
                "id": 1,
                "name": "mat1"
                }
            ],
            "materials_count": 1,
            "success": true
            }

POST /materials
        General:
            Add a new material
        Reequest Body (type: 'application/json'):
            {
            "material_name":"new material " ,
            "material_description":"new material desc"
            }
        Response:
            {
            "inserted_material_id": 3,
            "success": true
            }

PATCH /materials/<material_id>
        General:
            Update material by passing it's id in the request
        Reequest Body (type: 'application/json'):
            {
            "material_name":"new material update " ,
            "material_description":"new material desc update"
            }
        Response:
            {
            "success": true,
            "updated_material": {
                "description": "new material desc update",
                "id": 1,
                "name": "new material update "
            }

DELETE /materials/<material_id>
        General:
            delete the material by passing it's id in the request
        Response:
            {
            "deleted_material_id": 3,
            "success": true
            }

Get /orders
        General:
            Get all orders
        Response:
            {
            "orders": [
                {
                "order_details": [
                    {
                    "description": "new material desc update",
                    "id": 1,
                    "name": "new material update "
                    },
                    {
                    "description": "new material desc update",
                    "id": 1,
                    "name": "new material update "
                    }
                ],
                "order_id": 11,
                "order_notes": "note1342ddd"
                },
                {
                "order_details": [
                    {
                    "description": "new material desc update",
                    "id": 1,
                    "name": "new material update "
                    },
                    {
                    "description": "new material desc update",
                    "id": 1,
                    "name": "new material update "
                    }
                ],
                "order_id": 12,
                "order_notes": "note1342ddd"
                },
                {
                "order_details": [
                    {
                    "description": null,
                    "id": 2,
                    "name": "mat2"
                    },
                    {
                    "description": null,
                    "id": 2,
                    "name": "mat2"
                    }
                ],
                "order_id": 13,
                "order_notes": "note modified"
                }
            ],
            "success": true
            }

Get /orders/<order_id>
        General:
            Get order details for specified order id by passing the order id in the request
        Response:
            {
            "order_details": [
                {
                "description": "new material desc update",
                "id": 1,
                "name": "new material update "
                },
                {
                "description": "new material desc update",
                "id": 1,
                "name": "new material update "
                }
            ],
            "success": true
            }

POST /orders
        General:
           Insert a new order
        Reequest Body (type: 'application/json'):
            {
            "order_notes":"note modified" ,
            "details":[
                {
                    "material_id":2 ,
                    "quantity":20 ,
                    "price":15
                }
            ,
                {
                    "material_id":1 ,
                    "quantity":40 ,
                    "price":30
                }
            ]
            }
        Response:
            {
            "inserted_order": {
                "order_details": [
                {
                    "description": null,
                    "id": 2,
                    "name": "mat2"
                },
                {
                    "description": "new material desc update",
                    "id": 1,
                    "name": "new material update "
                }
                ],
                "order_id": 15,
                "order_notes": "note modified"
            },
            "success": true
            }
DELETE /orders/<order_id>
        General:
            Delete specified order by passing it's id in the request
        Response:
            {
            "deleted_order_id": 15,
            "success": true
            }

PATCH /orders/<order_id>
        General:
           Update the specified order by passing it's id in the request 
        Sample:
            {
                "order_notes":"note modified" , 
                "details":[
                    {
                        "material_id":1 , 
                        "quantity":40 , 
                        "price":30
                    }
                ]
            }
        Response:
            {
            "modified_order": {
                "order_details": [
                {
                    "description": "new material desc update",
                    "id": 1,
                    "name": "new material update "
                }
                ],
                "order_id": 14,
                "order_notes": "note modified"
            },
            "success": true
            }

## Unit Tests

You can run the unit tests by navigating to the '/DeliverMe' directory and execute the command:

```bash
pytest test_app.py
```
