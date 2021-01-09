from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import environ, path

base_dir = path.abspath(path.dirname(__file__)) + path.sep

app = Flask(__name__)
db_filename = "slack.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

slack = Blueprint("slack", __name__, url_prefix="/api")

from app.controllers._all import controllers as controllers
for controller in controllers:
  slack.add_url_rule(
      controller.get_path(),
      controller.get_name(),
      controller.response,
      methods=controller.get_methods()
  )

app.register_blueprint(slack)
