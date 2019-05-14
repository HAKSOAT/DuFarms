from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config.BaseConfig)

# Importing views last to prevent cyclic import errors
from app import views
