from app import app, models
from flask import abort, request
from sqlalchemy import func
from app.forms import AddForm, ProductMovementForm


@app.route("/")
def home():
    return "Home"


@app.route("/products")
def products():
    return "Products"


@app.route("/products/add", methods=["GET", "POST"])
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


@app.route("/locations/add", methods=["GET", "POST"])
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
    # Create a dynamic select list for the forms
    # The first value in the tuple is returned by the form if selected
    # The second value in the tuple is displayed by the form
    form.product.choices = [(product.id, product.name) for product in models.Product.query.all()]
    form.from_location.choices = [(location.id, location.name) for location in models.Location.query.all()]
    form.to_location.choices = [(location.id, location.name) for location in models.Location.query.all()]
    if request.method == "POST" and form.validate_on_submit():
        abroad = 1
        if form.from_location.data != abroad:
            incoming = models.db.session.query(func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.to_location == form.from_location.data).filter(
                models.ProductMovement.product_id == form.product.data).scalar()
            outgoing = models.db.session.query(func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.from_location == form.from_location.data).filter(
                models.ProductMovement.product_id == form.product.data).scalar()
            if incoming is None:
                incoming = 0
            if outgoing is None:
                outgoing = 0
            if outgoing + form.qty.data > incoming:
                return "Error"
        movement = models.ProductMovement(from_location=form.from_location.data, to_location=form.to_location.data,
                                          description=form.description.data,
                                          product_id=form.product.data, qty=form.qty.data)
        models.db.session.add(movement)
        models.db.session.commit()
    return "Add Location"


@app.route('/products/<name>')
def view_product(name):
    # Query the database for a product that matches the inputted value
    # func.lower helps with finding the right matches regardless of the case used
    product = models.Product.query.filter(func.lower(models.Product.name) == func.lower(name)).first()
    if product:
        return "{}".format(product)
    else:
        abort(404)


@app.route('/locations/<name>')
def view_location(name):
    # Query the database for a location that matches the inputted value
    # func.lower helps with finding the right matches regardless of the case used
    location = models.Location.query.filter(func.lower(models.Location.name) == func.lower(name)).first()
    if location:
        products = models.Product.query.all()
        report = {}
        for product in products:
            incoming = models.db.session.query(func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.to_location == location.id).filter(models.ProductMovement.product_id == product.id).scalar()
            outgoing = models.db.session.query(func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.from_location == location.id).filter(models.ProductMovement.product_id == product.id).scalar()
            report[product.name] = incoming - outgoing
        return "{}".format(report)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404
