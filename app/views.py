from app import app


@app.route("/")
def home():
    return "Home"


@app.route("/products")
def products():
    return "Products"


@app.route("/locations")
def locations():
    return "Locations"


@app.route("/movements")
def movements():
    return "Movements"
