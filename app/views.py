from app import app, models
from app.forms import AddForm, EditForm, ProductMovementForm
from flask import abort, flash, redirect, request, render_template, url_for
import sqlalchemy as sa


@app.route("/")
def home():
    page_title = "DuFarms - Home"
    return render_template("home.html", page_title=page_title)


@app.route("/products")
def products():
    prods = models.Product.query.all()
    page_title = "DuFarms - Products"
    return render_template("products.html", page_title=page_title, products=prods)


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    """
    Receive product name and description from form
    Add to database
    Redirect to product listings page
    :return: add products page for GET requests
    """
    form = AddForm()
    if request.method == "POST" and form.validate_on_submit():
        product = models.Product(name=form.name.data, description=form.description.data)
        # Handle cases when a product's name already exists
        try:
            models.db.session.add(product)
            models.db.session.commit()
            flash("Product added successfully", "success")
            return redirect(url_for("products"))
        except sa.exc.IntegrityError:
            flash("Product name exists", "danger")
    page_title = "DuFarms - Add Product"
    form_type = "Product"
    return render_template("add.html", page_title=page_title, form=form, form_type=form_type)


@app.route("/products/<name>/edit", methods=["GET", "POST"])
def edit_product(name):
    """
    Edit information on the requested product
    :param name:
    :return: product info page
    """
    product = models.Product.query.filter(sa.func.lower(models.Product.name) == sa.func.lower(name)).first()
    if product:
        form = EditForm(obj=product)
        if request.method == "POST" and form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            # Handle cases when a product's name already exists
            try:
                models.db.session.commit()
                flash("Product edited successfully", "success")
                return redirect(url_for("products"))
            except sa.exc.IntegrityError:
                flash("Product name exists", "danger")
        page_title = "DuFarms - Edit Product"
        form_type = "Product"
        return render_template("edit.html", page_title=page_title, form=form, form_type=form_type)
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
    # sa.func.lower helps with finding the right matches regardless of the case used
    product = models.Product.query.filter(sa.func.lower(models.Product.name) == sa.func.lower(name)).first()
    if product:
        page_title = "DuFarms - {}".format(product.name)
        return render_template("view.html", page_title=page_title, product=product)
    else:
        abort(404)


@app.route("/locations")
def locations():
    locs = models.Location.query.all()
    page_title = "DuFarms - Locations"
    return render_template("locations.html", page_title=page_title, locations=locs)


@app.route("/locations/add", methods=["GET", "POST"])
def add_location():
    """
    Receive location name and description from form
    Add to database
    Redirect to location listings page
    :return: add locations page for GET requests
    """
    form = AddForm()
    if request.method == "POST" and form.validate_on_submit():
        location = models.Location(name=form.name.data, description=form.description.data)
        # Handle cases when a location's name already exists
        try:
            models.db.session.add(location)
            models.db.session.commit()
            flash("Location added successfully", "success")
            return redirect(url_for("locations"))
        except sa.exc.IntegrityError:
            flash("Location name exists", "danger")
    page_title = "DuFarms - Add Location"
    form_type = "Location"
    return render_template("add.html", page_title=page_title, form=form, form_type=form_type)


@app.route("/locations/<name>/edit", methods=["GET", "POST"])
def edit_location(name):
    """
    Edit information on the requested location
    :param name:
    :return: location info page
    """
    location = models.Location.query.filter(sa.func.lower(models.Location.name) == sa.func.lower(name)).first()
    if location:
        form = AddForm(obj=location)
        if request.method == "POST" and form.validate_on_submit():
            location.name = form.name.data
            location.description = form.description.data
            # Handle cases when a location's name already exists
            try:
                models.db.session.commit()
                flash("Location edited successfully", "success")
                return redirect(url_for("locations"))
            except sa.exc.IntegrityError:
                flash("Location name exists", "danger")
        page_title = "DuFarms - Edit Location"
        form_type = "Location"
        return render_template("edit.html", page_title=page_title, form=form, form_type=form_type)
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
    # sa.func.lower helps with finding the right matches regardless of the case used
    location = models.Location.query.filter(sa.func.lower(models.Location.name) == sa.func.lower(name)).first()
    # Ensure that location being requested for is in the database
    if location:
        results = models.Product.query.all()
        products = []
        quantity = []
        # Fetch the quantity remaining for each product in the provided location
        for product in results:
            incoming = models.db.session.query(sa.func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.to_location == location.id).filter(
                models.ProductMovement.product_id == product.id).scalar()
            outgoing = models.db.session.query(sa.func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.from_location == location.id).filter(
                models.ProductMovement.product_id == product.id).scalar()
            if incoming is None:
                incoming = 0
            if outgoing is None:
                outgoing = 0
            if incoming > 0:
                products.append(product)
                quantity.append(incoming - outgoing)
        page_title = "DuFarms - {}".format(location.name)
        return render_template("view.html", page_title=page_title, products=products, location=location, quantity=quantity)
    else:
        abort(404)


@app.route("/movements")
def movements():
    """
    Move product between created locations
    :return: movements page
    """
    movs = models.ProductMovement.query.all()
    page_title = "DuFarms - Movements"
    return render_template("movements.html", page_title=page_title, movements=movs)


@app.route("/movements/add", methods=["GET", "POST"])
def add_movement():
    """
    Receive product_name, from_location, to_location, description and quantity from form
    Add to database
    Redirect to movements listings page
    :return: add movements page for GET requests
    """
    form = ProductMovementForm()
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
        if form.from_location.data == form.to_location.data:
            flash("Failed attempt to move product to the same location", "danger")
        elif form.from_location.data != abroad:
            incoming = models.db.session.query(sa.func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.to_location == form.from_location.data).filter(
                models.ProductMovement.product_id == form.product.data).scalar()
            outgoing = models.db.session.query(sa.func.sum(models.ProductMovement.qty)).filter(
                models.ProductMovement.from_location == form.from_location.data).filter(
                models.ProductMovement.product_id == form.product.data).scalar()
            if incoming is None:
                incoming = 0
            if outgoing is None:
                outgoing = 0
            if outgoing + form.qty.data <= incoming:
                movement = models.ProductMovement(from_location=form.from_location.data, to_location=form.to_location.data,
                                                  description=form.description.data,
                                                  product_id=form.product.data, qty=form.qty.data)
                models.db.session.add(movement)
                models.db.session.commit()
                flash("Product moved successfully", "success")
                return redirect(url_for("movements"))
            elif incoming == 0:
                flash("Product doesn't exist in this location", "danger")
            else:
                remnant = incoming - outgoing
                flash("Only a maximum of {} can be moved from this location".format(remnant),
                      "danger")
        else:
            movement = models.ProductMovement(from_location=form.from_location.data, to_location=form.to_location.data,
                                              description=form.description.data,
                                              product_id=form.product.data, qty=form.qty.data)
            models.db.session.add(movement)
            models.db.session.commit()
            flash("Product moved successfully", "success")
            return redirect(url_for("movements"))
    page_title = "DuFarms - Add Movement"
    form_type = "Movement"
    return render_template("add.html", page_title=page_title, form=form, form_type=form_type)


@app.route("/movements/<int:number>/edit", methods=["GET", "POST"])
def edit_movement(number):
    """
    Edit product_name, from_location, to_location, description and quantity from form
    Add to database
    Redirect to movements listings page
    :return: specific edit movement page for GET requests
    """
    movement = models.ProductMovement.query.filter(models.ProductMovement.id == number).first()
    if movement:
        form = ProductMovementForm(obj=movement)
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
            if form.from_location.data == form.to_location.data:
                flash("Failed attempt to move product to the same location", "danger")
            elif form.from_location.data != abroad:
                incoming = models.db.session.query(sa.func.sum(models.ProductMovement.qty)).filter(
                    models.ProductMovement.to_location == form.from_location.data).filter(
                    models.ProductMovement.product_id == form.product.data).scalar()
                outgoing = models.db.session.query(sa.func.sum(models.ProductMovement.qty)).filter(
                    models.ProductMovement.from_location == form.from_location.data).filter(
                    models.ProductMovement.product_id == form.product.data).scalar()
                if incoming is None:
                    incoming = 0
                if outgoing is None:
                    outgoing = 0
                if outgoing + form.qty.data <= incoming:
                    movement = models.ProductMovement(from_location=form.from_location.data, to_location=form.to_location.data,
                                                      description=form.description.data,
                                                      product_id=form.product.data, qty=form.qty.data)
                    models.db.session.add(movement)
                    models.db.session.commit()
                    flash("Movement edited successfully", "success")
                    return redirect(url_for("movements"))
                elif incoming == 0:
                    flash("Product doesn't exist in this location", "danger")
                else:
                    remnant = incoming - outgoing
                    flash("Only a maximum of {} can be moved from this location".format(remnant),
                          "danger")
            else:
                movement = models.ProductMovement(from_location=form.from_location.data,
                                                  to_location=form.to_location.data,
                                                  description=form.description.data,
                                                  product_id=form.product.data, qty=form.qty.data)
                models.db.session.add(movement)
                models.db.session.commit()
                flash("Movement edited successfully", "success")
                return redirect(url_for("movements"))
        page_title = "DuFarms - Edit Movement"
        form_type = "Movement"
        return render_template("edit.html", page_title=page_title, form=form, form_type=form_type)
    else:
        abort(404)


@app.route("/movements/<int:number>/view")
def view_movement(number):
    """
    View product_name, from_location, to_location, description and quantity
    :return: specific view movement page
    """
    movement = models.ProductMovement.query.filter(models.ProductMovement.id == number).first()
    if movement:
        page_title = "DuFarms - Movement {}".format(movement.id)
        from_location = models.Location.query.filter(models.Location.id == movement.from_location).first()
        to_location = models.Location.query.filter(models.Location.id == movement.to_location).first()
        return render_template("view.html", page_title=page_title, movement=movement, from_location=from_location,
                               to_location=to_location)
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404
