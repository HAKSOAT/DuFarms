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
    """
    Receive product name and description from form
    Add to database
    Redirect to product listings page
    :return: add products page for GET requests
    """
    form = AddForm(form_name="Add Product")
    if request.method == "POST" and form.validate_on_submit():
        product = models.Product(name=form.name.data, description=form.description.data)
        models.db.session.add(product)
        models.db.session.commit()
    return "Add Product"


@app.route("/products/<name>/edit", methods=["GET", "POST"])
def edit_product(name):
    """
    Edit information on the requested product
    :param name:
    :return: product info page
    """
    product = models.Product.query.filter(func.lower(models.Product.name) == func.lower(name)).first()
    if product:
        form = AddForm(form_name="Edit Product", submit="Edit", obj=product)
        if request.method == "POST" and form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            models.db.session.commit()
        return "{}".format(product)
    else:
        abort(404)


@app.route('/products/<name>')
def view_product(name):
    """
    Display information on the requested product
    :param name:
    :return: product info page
    """
    # Query the database for a product that matches the inputted value
    # func.lower helps with finding the right matches regardless of the case used
    product = models.Product.query.filter(func.lower(models.Product.name) == func.lower(name)).first()
    if product:
        return "{}".format(product)
    else:
        abort(404)


@app.route("/locations")
def locations():
    return "Locations"


@app.route("/locations/add", methods=["GET", "POST"])
def add_location():
    """
    Receive location name and description from form
    Add to database
    Redirect to location listings page
    :return: add locations page for GET requests
    """
    form = AddForm(form_name="Add Location")
    if request.method == "POST" and form.validate_on_submit():
        location = models.Location(name=form.name.data, description=form.description.data)
        models.db.session.add(location)
        models.db.session.commit()
    return "Add Location"


@app.route("/locations/<name>/edit", methods=["GET", "POST"])
def edit_location(name):
    """
    Edit information on the requested location
    :param name:
    :return: location info page
    """
    location = models.Location.query.filter(func.lower(models.Location.name) == func.lower(name)).first()
    if location:
        form = AddForm(form_name="Edit Location", submit="Edit", obj=location)
        if request.method == "POST" and form.validate_on_submit():
            location.name = form.name.data
            location.description = form.description.data
            models.db.session.commit()
        return "{}".format(location)
    else:
        abort(404)


@app.route('/locations/<name>')
def view_location(name):
    """
    Display information on the requested location
    :param name:
    :return: location info page
    """
    # Query the database for a location that matches the inputted value
    # func.lower helps with finding the right matches regardless of the case used
    location = models.Location.query.filter(func.lower(models.Location.name) == func.lower(name)).first()
    # Ensure that location being requested for is in the database
    if location:
        products = models.Product.query.all()
        report = {}
        # Fetch the quantity remaining for each product in the provided location
        for product in products:
            incoming = models.db.session.query(func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.to_location == location.id).filter(
                models.ProductMovement.product_id == product.id).scalar()
            outgoing = models.db.session.query(func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.from_location == location.id).filter(
                models.ProductMovement.product_id == product.id).scalar()
            if incoming is None:
                incoming = 0
            if outgoing is None:
                outgoing = 0
            report[product.name] = incoming - outgoing
        return "{}".format(report)
    else:
        abort(404)


@app.route("/product_movement", methods=["GET", "POST"])
def product_movement():
    """
    Move product between created locations
    :return: product_movement page
    """
    form = ProductMovementForm(form_name="Product Movement")
    # Create a dynamic select list for the forms
    # The first value in the tuple is returned by the form if selected
    # The second value in the tuple is displayed by the form
    form.product.choices = [(product.id, product.name) for product in models.Product.query.all()]
    form.from_location.choices = [(location.id, location.name) for location in models.Location.query.all()]
    form.to_location.choices = [(location.id, location.name) for location in models.Location.query.all()]
    if request.method == "POST" and form.validate_on_submit():
        # Ensure that products cannot be moved more than available
        # Example: Requests to move 5 quantities if there are only 3 are to be rejected
        # Except in cases where the product is coming from Abroad
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


@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404
