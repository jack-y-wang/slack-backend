import json
import os
import datetime

from db import db
from db import User, Workspace, Channel, Message, Thread

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
    optional_user = dao.get_user_by_id(user_id)
    if not optional_user:
        return failure_response("User not found")
    return success_response(dao.get_workspaces_of_user(user_id))

@app.route("/users/<int:user_id>/workspaces/<int:workspace_id>/channels/")
def get_channels_of_user(user_id, workspace_id):
    channels, msg = dao.get_users_channels_of_workspace(user_id, workspace_id)
    if channels is False:
        return failure_response(msg)
    return success_response(channels)

@app.route("/users/<int:user_id>/threads/")
def get_followed_threads_of_user(user_id):
    optional_user = dao.get_user_by_id(user_id)
    if optional_user is None:
        return failure_response("User not found")
    return success_response(dao.get_threads_of_user(optional_user))

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def remove_user(user_id):
    optional_user = dao.get_user_by_id(user_id)
    if not optional_user:
        return failure_response("User not found")
    db.session.delete(optional_user)
    db.session.commit()
    return success_response(optional_user.serialize())

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
    for channel in workspace.channels:
        if channel.public:
            user.channels.append(channel)

    db.session.commit()
    return success_response(workspace.serialize())

@app.route("/workspaces/<int:workspace_id>/", methods=["DELETE"])
def remove_workspace(workspace_id):
    workspace = dao.get_workspace_by_id(workspace_id)
    if workspace is None:
        return failure_response("Workspace not found")
    db.session.delete(workspace)
    db.session.commit()
    return success_response(workspace.serialize())

@app.route("/workspaces/<int:worksp_id>/channels/")
def get_channels_of_workspace(worksp_id):
    workspace = dao.get_workspace_by_id(worksp_id)
    if workspace is None:
        return failure_response("Workspace not found")
    channels = dao.get_workspaces_channels(worksp_id)
    return success_response(channels)


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
    if channel.public == True:
        for user in workspace.users:
            # channel.users.append(user)
            user.channels.append(channel)
    workspace.channels.append(channel)
    db.session.commit()
    return success_response(channel.serialize())

@app.route("/channels/<int:channel_id>/")
def get_channel(channel_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    return success_response(optional_channel.serialize())

@app.route("/channels/<int:channel_id>/users/", methods=["POST"])
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

@app.route("/channels/<int:channel_id>/users/<int:user_id>/", methods=["DELETE"])
def remove_user_from_channel(channel_id, user_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    optional_user = dao.get_user_by_id(user_id)
    if optional_user is None:
        return failure_response("User not found")
    
    optional_channel.users.remove(optional_user)
    db.session.commit()
    return optional_channel.serialize()

@app.route("/channels/<int:channel_id>/", methods=["DELETE"])
def remove_channel(channel_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    db.session.delete(optional_channel)
    db.session.commit()
    return success_response(optional_channel.serialize())

@app.route("/channels/<int:channel_id>/messages/")
def get_messages_of_channel(channel_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    return success_response(dao.get_messages_of_channel(channel_id))


# ------------------------- MESSAGE ROUTES --------------------------------------------
@app.route("/channels/<int:channel_id>/messages/", methods=["POST"])
def create_message(channel_id):
    optional_channel = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response("Channel not found")
    
    body = json.loads(request.data)
    user_id = body.get("user_id")
    content = body.get("content")
    if user_id is None or content is None:
        return failure_response("Empty user_id or content")

    sender = dao.get_user_by_id(user_id)
    if sender is None:
        return failure_response("User is not found")
    if not sender in optional_channel.users:
        return failure_response("User is not in channel")

    timestamp = datetime.datetime.now()
    message = Message(
        sender_id = user_id,
        content = content,
        timestamp = timestamp,
        channel_id = channel_id
    )

    optional_channel.messages.append(message)
    sender.threads.append(message)
    db.session.commit()
    return success_response(message.serialize())

@app.route("/messages/<int:msg_id>/")
def get_message(msg_id):
    optional_message = dao.get_message_by_id(msg_id)
    if optional_message is None:
        return failure_response("Message not found")
    return success_response(optional_message.serialize())

@app.route("/messages/<int:msg_id>/", methods=["POST"])
def update_message(msg_id):
    optional_message = dao.get_message_by_id(msg_id)
    if optional_message is None:
        return failure_response("Message not found")
    
    body = json.loads(request.data)
    user_id = body.get("user_id")
    content = body.get("content")
    if content is None or user_id is None:
        return failure_response("Invalid content input or user ID")
    if optional_message.sender_id != user_id:
        return failure_response("Invalid user ID - must be the creator of message")
    
    optional_message.content = body.get("content", optional_message.content)
    optional_message.updated = True
    db.session.commit()
    return success_response(optional_message.serialize())

@app.route("/messages/<int:msg_id>/users/")
def get_users_following_thread(msg_id):
    optional_msg = dao.get_message_by_id(msg_id)
    if not optional_msg:
        return failure_response("Message not found")
    return success_response(dao.get_users_of_message(optional_msg))

@app.route("/messages/<int:msg_id>/", methods=["DELETE"])
def delete_message(msg_id):
    optional_message = dao.get_message_by_id(msg_id)
    if optional_message is None:
        return failure_response("Message not found")
   
    db.session.delete(optional_message)
    db.session.commit()
    return success_response(optional_message.serialize_content())

@app.route("/messages/<int:msg_id>/threads/")
def get_threads_of_message(msg_id):
    optional_message = dao.get_message_by_id(msg_id)
    if optional_message is None:
        return failure_response("Message not found")
    return success_response(dao.get_threads_of_message(optional_message))

# ------------------------- THREAD ROUTES --------------------------------------------
@app.route("/messages/<int:msg_id>/threads/", methods=["POST"])
def create_thread(msg_id):
    optional_message = dao.get_message_by_id(msg_id)
    if optional_message is None:
        return failure_response("Message not found")
    
    body = json.loads(request.data)
    user_id = body.get("user_id")
    content = body.get("content")
    if user_id is None or content is None:
        return failure_response("Empty user_id or content")
    
    user = dao.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found")
    if not user in optional_message.channel.users:
        return failure_response("User is not in the channel")
    
    timestamp = datetime.datetime.now()
    thread = Thread(
        sender_id=user_id,
        content=content,
        timestamp=timestamp,
        message_id=msg_id
    )
    db.session.add(thread)
    optional_message.threads.append(thread)
    optional_message.users_following.append(user)
    db.session.commit()
    return success_response(thread.serialize())
    
@app.route("/threads/<int:thread_id>/")
def get_thread(thread_id):
    optional_thread = dao.get_thread_by_id(thread_id)
    if optional_thread is None:
        return failure_response("Thread not found")
    return success_response(optional_thread.serialize())

@app.route("/threads/<int:thread_id>/", methods=["POST"])
def update_thread(thread_id):
    optional_thread = dao.get_thread_by_id(thread_id)
    if optional_thread is None:
        return failure_response("Thread not found")
    
    body = json.loads(request.data)
    optional_thread.content = body.get("content", optional_thread.content)
    optional_thread.updated = True

    db.session.commit()
    return success_response(optional_thread.serialize())

@app.route("/threads/<int:thread_id>/", methods=["DELETE"])
def remove_thread(thread_id):
    optional_thread = dao.get_thread_by_id(thread_id)
    if optional_thread is None:
        return failure_response("Thread not found")
    message, user_id = optional_thread.message, optional_thread.sender_id
    user = dao.get_user_by_id(user_id)

    message.users_following.remove(user)
    db.session.delete(optional_thread)
    db.session.commit()
    return success_response(optional_thread.serialize())


# ------------------------- DM GROUP ROUTES --------------------------------------------
@app.route("/workspaces/<int:workspace_id>/users/<int:user_id>/dms/", methods=["POST"])
def create_dm_group(workspace_id, user_id):
    workspace = dao.get_workspace_by_id(workspace_id)
    if workspace is None:
        return failure_response("Workspace not found")
    optional_user = dao.get_user_by_id(user_id)
    if not optional_user:
        return failure_response("User not found")   


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
