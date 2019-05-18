from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# Zip is needed for iteration in the jinja templating
app.jinja_env.filters['zip'] = zip
bootstrap = Bootstrap(app)

# Importing views last to prevent cyclic import errors
from app import views
