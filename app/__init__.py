from flask import Flask
from flask_bootstrap import Bootstrap
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Importing views last to prevent cyclic import errors
from app import views
