import json
import os

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
@app.route("/users/<int:user_id>/")
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
    user_exists, msg = dao.does_user_already_exist(email, username)
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
    return success_response(dao.get_workspaces_of_user(user_id))


# ------------------------- WORKSPACE ROUTES --------------------------------------------
@app.route("/workspaces/", methods=["POST"])
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
    db.session.add(workspace)
    db.session.commit()
    return success_response(workspace.serialize())

@app.route("/workspaces/")
def get_workspaces():
    return success_response([w.serialize() for w in Workspace.query.all()])

@app.route("/workspaces/<int:worksp_id>/")
def get_workspace_by_id(worksp_id):
    workspace = dao.get_workspace_by_id(worksp_id)
    if workspace is None:
        return failure_response("Workspace not found")
    return success_response(workspace.serialize())

@app.route("/workspaces/<int:workspace_id>/add-user/", methods=["POST"])
def add_user_to_workspace(workspace_id):
    workspace = dao.get_workspace_by_id(workspace_id)
    if workspace is None:
        return failure_response("Workspace not found")

    body = json.loads(request.data)
    user_id = body.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    if user in workspace.users:
        return failure_response(f"User already in channel {workspace.name}")
    
    workspace.users.append(user)
    db.session.commit()
    return success_response(workspace.serialize())


# ------------------------- CHANNEL ROUTES --------------------------------------------

@app.route("/workspaces/<int:workspace_id>/channels/", methods=["POST"])
def create_channel(workspace_id):
    workspace = dao.get_workspace_by_id(workspace_id)
    if workspace is None:
        return failure_response("Workspace not found")

    body = json.loads(request.data)
    name = body.get("name")
    description = body.get("description", "")
    public = body.get("public", True)

    optional_channel = dao.get_channel_by_name(workspace, name)
    if optional_channel is not None:
        return failure_response(f"Channel with name {name} already exists")
    
    channel = Channel(name=name, description=description, public=public, workspace_id=workspace_id)
    db.session.add(channel)
    # workspace.channels.append(channel)
    db.session.commit()
    return success_response(channel.serialize())

@app.route("/channels/<int:channel_id>/")
def get_channel(channel_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    return success_response(optional_channel.serialize())

@app.route("/channels/<int:channel_id>/add-user/", methods=["POST"])
def add_user_to_channel(channel_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    
    body = json.loads(request.data)
    user_id = body.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    if not user in optional_channel.workspace.users:
        return failure_response(f"User is not in workspace: {optional_channel.workspace}")
    if user in optional_channel.users:
        return failure_response(f"User already in channel {optional_channel.name}")
    
    optional_channel.users.append(user)
    db.session.commit()
    return success_response(optional_channel.serialize())
    

@app.route("/workspaces/<int:worksp_id>/channels/")
def get_channels_of_workspace(worksp_id):
    workspace = dao.get_workspace_by_id(worksp_id)
    if workspace is None:
        return failure_response("Workspace not found")
    channels = dao.get_workspaces_channels(worksp_id)
    return success_response(channels)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
