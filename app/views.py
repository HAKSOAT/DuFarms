from app import app, models
from flask import abort, request
from app.forms import AddForm, ProductMovementForm


@app.route("/")
def home():
    return "Home"


@app.route("/products")
def products():
    return "Products"


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = AddForm(form_name="Add Product")
    if request.method == "POST" and form.validate_on_submit():
        product = models.Product(name=form.name.data, description=form.description.data)
        models.db.session.add(product)
        models.db.session.commit()
    return "Add Product"


@app.route("/locations")
def locations():
    return "Locations"


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    form = AddForm(form_name="Add Location")
    if request.method == "POST" and form.validate_on_submit():
        location = models.Location(name=form.name.data, description=form.description.data)
        models.db.session.add(location)
        models.db.session.commit()
    return "Add Location"


@app.route("/product_movement", methods=["GET", "POST"])
def product_movement():
    form = ProductMovementForm(form_name="Product Movement")
    form.product.choices = [(product.id, product.name) for product in models.Product.query.all()]
    form.from_location.choices = [(location.id, location.name) for location in models.Location.query.all()]
    form.to_location.choices = [(location.id, location.name) for location in models.Location.query.all()]
    if request.method == "POST" and form.validate_on_submit():
        movement = models.ProductMovement(from_location=form.from_location.data, to_location=form.to_location.data,
                                          product_id=form.product.data, qty=form.qty.data)
        models.db.session.add(movement)
        models.db.session.commit()
    return "Add Location"


@app.route('/product/<name>')
def view_product(name):
    product = models.Product.query.filter(models.Product.name == name).first()
    if product:
        return "{}".format(product)


@app.route('/location/<name>')
def view_location(name):
    location = models.Location.query.filter(models.Location.name == name).first()
    if location:
        return "{}".format(location)

