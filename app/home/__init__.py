from flask import Blueprint

home: Blueprint = Blueprint("home", __name__)

import app.home.views