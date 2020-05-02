from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

database_name = "deliverme"
database_path = "postgres://{}@{}/{}".format('postgres', 'localhost:5432', database_name)


db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    print('🍗 🍗 🍗')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


class materials(db.Model):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    mat_name = Column(String)
    mat_desc = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.mat_name,
            'description': self.mat_desc
        }

    def getAllMaterials():
        mats = materials.query.all()
        formatted_materials = [mat.format() for mat in mats]
        return formatted_materials

    def searchByName(matName):
        mats = materials.query.filter(materials.mat_name.ilike("%{}%".format(matName))).all()
        formatted_materials = [mat.format() for mat in mats]
        return formatted_materials


class orders(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_notes = Column(String)
    materials = db.relationship('orders_details', backref='order_materials', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_order_details(self):
        order = orders.query.get(self.id)
        allmats = order.materials
        formatted_allmats = [m.material_det.format() for m in allmats]
        return formatted_allmats

    def format(self):
        details = self.get_order_details()
        return {
            "order_id": self.id,
            "order_notes": self.order_notes,
            "order_details": details
        }

    def get_all_orders():
        allorders = orders.query.all()
        allformated = [o.format() for o in allorders]
        return {
            "orders": allformated
        }

    def insert_order(self, all_details=[]):
        self.insert()
        id = self.id
        print (all_details)
        #  formatted = [d.format() for d in all_details]
        #  print ('🍟 🍟 🍟 🍟')
        #  print (formatted)
        #  for d in formatted:
        #      detail = orders_details()
        #      detail.orders  = self.id
        #      detail.quantity  = d.get("quantity")
        #      detail.price = d.get("price")
        #      detail.materials = d.get("material_id")
        #     #  db.session.add(detail)
        #     #  db.session.commit()
        #      print ('🍪 🍪 🍪 🍪')
        #      print (detail.format())


class orders_details(db.Model):
    __tablename__ = 'orders_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    price = Column(Integer)
    orders = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    materials = db.Column(db.Integer, db.ForeignKey('materials.id'), primary_key=True)
    order_det = db.relationship('orders', backref='materials1')
    material_det = db.relationship('materials', backref='orders1')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def delete_order_details(self, order_id):
        allDetails = orders_details.query.filter(orders_details.orders == order_id).all()
        for d in allDetails:
            d.delete()

    def format(self):
        material = self.material_det
        order = self.order_det
        return {
            "details_id": self.id,
            "quantity": self.quantity,
            "price": self.price,
            "material_id": self.materials,
            "order_id": self.orders,
            "material": self.material_det,
            "order": self.order_det
        }


class ErrorModel:
    errorCode = 0
    errorMsg = ''

    def __init__(self, code, message):
        self.errorCode = code
        self.errorMsg = message

    def format(self):
        return {
            "success": False,
            "error_code": self.errorCode,
            "message": self.errorMsg
        }
