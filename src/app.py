import json

from db import db
from db import User, Workspace, Channel

from flask import Flask
from flask import request

import dao

app = Flask(__name__)
db_filename = "slack.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/")
def welcome():
    return "Welcome to Slack Backend :)"

# ------------------------- USER ROUTES --------------------------------------------
@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("email")
    username = body.get('username')

    if name is None or email is None or username is None:
        return failure_response("Empty name, username, or username")
    user_exists, msg = dao.user_already_exists(email, username)
    if user_exists:
        return failure_response(msg)
    
    user = User(name=name, email=email, username=username)
    db.session.add(user)
    db.session.commit()

    return success_response(user.serialize())

@app.route("/users/<int:user_id>/workspaces/")
def get_users_workspaces(user_id):
    user_exists = dao.get_user_by_id(user_id)
    if not user_exists:
        return failure_response("User not found")
    return dao.get_workspaces_of_user(user_id)


# ------------------------- WORKSPACE ROUTES --------------------------------------------
@app.route("/workspaces/")
def create_workspace():
    body = json.loads(request.data)
    name = body.get("name")
    url = body.get("url")

    if name is None or url is None:
        return failure_response("Empty name or url")
    workspace_exists, msg = dao.does_workspace_exist(name, url)
    if workspace_exists:
        return failure_response(msg)

    workspace = Workspace(name=name, url=url)
    db.session.add()
    db.session.commit()
    return workspace.serialize()

@app.route("/workspaces/")
def get_workspaces():
    return success_response([w.serialize() for w in Workspace.query.all()])

@app.route("/workspaces/<int:worksp_id>/")
def get_workspace_by_id(worksp_id):
    workspace = dao.get_workspace_by_id(worksp_id)
    if workspace is None:
        return failure_response("Workspace not found")
    return success_response(workspace.serialize())

@app.route("/workspaces/<int:worksp_id>/channels/")
def get_channels_of_workspace(worksp_id):
    workspace = dao.get_workspace_by_id(worksp_id)
    if workspace is None:
        return failure_response("Workspace not found")
    channels = dao.get_workspaces_channels(worksp_id)
    return success_response(channels)

# ------------------------- CHANNEL ROUTES --------------------------------------------

