import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return "<{} : {}>".format(self.name, self.description)


class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return "<{}>".format(self.name)


class ProductMovement(db.Model):
    __tablename__ = "ProductMovement"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.String)
    from_location = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.Column(db.Integer, db.ForeignKey('location.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    qty = db.Column(db.Integer)

    def __repr__(self):
        return "<{} : {} : {} : {}>".format(self.from_location, self.to_location, self.product_id, self.qty)
