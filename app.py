from flask import Flask, jsonify, request, abort
from models import setup_db
from models import materials, orders, ErrorModel, orders_details
from auth import requires_auth
import sys

app = Flask(__name__)
setup_db(app)

'''
MATERIALS: Get All Materials Method
'''


@app.route('/materials', methods=['GET'])
@requires_auth('read:materials')
def get_all_materials():
    try:
        allMats = materials.getAllMaterials()
        return jsonify({
            "success": True,
            "materials": allMats,
            "materials_count": len(allMats)
        })
    except:
        print(sys.exc_info()[0], "occured.")
        abort(404)


@app.route('/materials', methods=['POST'])
@requires_auth('add:materials')
def insert_materials():
    body = request.get_json()
    search = body.get('search')
    if search is None:
        try:
            material = materials()
            material.mat_name = body.get('material_name')
            material.mat_desc = body.get('material_description')
            material.insert()
            return jsonify({
                    "success": True,
                    "inserted_material_id": material.id
                    })
        except:
            abort(400)
    else:
        try:
            allMats = materials.searchByName(search)
            if allMats is None:
                abort(404)
            return jsonify({
                "success": True,
                "materials_count": len(allMats),
                "materials": allMats
            })
        except:
            abort(500)


@app.route('/materials/<material_id>', methods=['PATCH'])
@requires_auth('update:materials')
def update_materials(material_id):
    body = request.get_json()
    material = materials()
    material = materials.query.get(material_id)
    if material is None:
        abort(404)
    try:
        material.mat_name = body.get('material_name')
        material.mat_desc = body.get('material_description')
        material.update()
        return jsonify({
            "success": True,
            "updated_material": material.format()
        })
    except:
        abort(500)


@app.route('/materials/<material_id>', methods=['DELETE'])
@requires_auth('delete:materials')
def delete_material(material_id):
    material = materials.query.get(material_id)
    details = orders_details.query.filter(orders_details.material_det == material).all()
    print ('💊 💊 💊 💊{}'.format(details))
    for detail in details:
        detail.delete()
    if material is None:
        abort(404)
    material.delete()
    return jsonify({
        "success": True,
        "deleted_material_id": material.id
    })


@app.route('/orders', methods=['GET'])
@requires_auth('read:orders')
def get_all_orders():
    allOrders = orders.query.all()
    formatted_orders = [order.format() for order in allOrders]
    return jsonify({
        "success": True,
        "orders": formatted_orders
    })


@app.route('/orders/<order_id>', methods=['GET'])
@requires_auth('read:orders')
def get_order_details(order_id):
    order = orders.query.get(order_id)
    formatted_order = order.format()
    return jsonify({
        "success": True,
        "order_details": formatted_order.get("order_details")
    })


@app.route('/orders', methods=['POST'])
@requires_auth('add:orders')
def insert_order():
    body = request.get_json()
    details = body.get('details')
    order = orders()
    order.order_notes = body.get('order_notes')
    allDetails = []
    order.insert()
    id = order.id
    print ('🍞 🍞 🍞{}'.format(id))
    if id is None:
        abort(500)
    for d in details:
        detail = orders_details()
        print (d.get('material_id'))
        material = materials.query.get(d.get('material_id'))
        detail.material_det = material
        detail.quantity = d.get('quantity')
        detail.price = d.get('price')
        detail.order_det = order
        print ('🧀 🧀 ')
        print (detail.format())
        try:
            detail.insert()
        except:
            abort(500)

    return jsonify({
        "success": True,
        "inserted_order": order.format()
                })


@app.route('/orders/<order_id>', methods=['DELETE'])
@requires_auth('delete:orders')
def delete_order(order_id):
    order = orders.query.get(order_id)
    details = orders_details.query.filter(orders_details.order_det == order).all()
    print ('💊 💊 💊 💊{}'.format(details))
    for detail in details:
        detail.delete()
    if order is None:
        abort(404)
    order.delete()
    return jsonify({
        "success": True,
        "deleted_order_id": order.id
    })


@app.route('/orders/<order_id>', methods=['PATCH'])
@requires_auth('update:orders')
def update_order(order_id):
    order = orders.query.get(order_id)
    if order is None:
        abort(404)
    body = request.get_json()
    order.order_notes = body.get("order_notes")
    try:
        order.update()
    except:
        abort(500)
    details = body.get("details")
    detail = orders_details()
    detail.delete_order_details(order_id)
    for d in details:
        detail = orders_details()
        material = materials.query.get(d.get('material_id'))
        detail.material_det = material
        detail.quantity = d.get('quantity')
        detail.price = d.get('price')
        detail.order_det = order
        try:
            detail.insert()
        except:
            abort(500)
    order = orders.query.get(order_id)
    return jsonify({
        "success": True,
        "modified_order": order.format()
    })


@app.route('/')
def index():
    return "Hello, and Welcome to delivery me API"


'''
Error Handling
'''


@app.errorhandler(404)
def not_found(error):
    error = ErrorModel(404, 'Page not found')
    return jsonify({
        "error": error.format()
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    error = ErrorModel(500, 'Internal server error')
    return jsonify({
        "error": error.format()
    }), 500


@app.errorhandler(401)
def not_found(error):
    error = ErrorModel(401, 'You are unauthorized')
    return jsonify({
        "error": error.format()
    }), 401


@app.errorhandler(400)
def not_authorized(error):
    error = ErrorModel(400, 'Authorization error')
    return jsonify({
        "error": error.format()
    }), 400


@app.errorhandler(403)
def not_authorized(error):
    error = ErrorModel(403, 'You do not have access to this feature')
    return jsonify({
        "error": error.format()
    }), 403


@app.errorhandler(405)
def not_authorized(error):
    error = ErrorModel(405, 'Method is not allowed, check your request you may passing wrong parameters')
    return jsonify({
        "error": error.format()
    }), 405
