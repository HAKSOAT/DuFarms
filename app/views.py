from app import app, models
from flask import request
from app.forms import AddForm


@app.route("/")
def home():
    return "Home"


@app.route("/products")
def products():
    return "Products"


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    form = AddForm()
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
    form = AddForm()
    if request.method == "POST" and form.validate_on_submit():
        location = models.Location(name=form.name.data, description=form.description.data)
        models.db.session.add(location)
        models.db.session.commit()
    return "Add Location"


@app.route("/movements")
def movements():
    return "Movements"
