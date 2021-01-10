import json
import os
import datetime

from db import db
import dao

from flask import Flask
from flask import request

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
@app.route("/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("email")
    username = body.get('username')
    profile_img = body.get('image')

    user, err = dao.create_user(name, email, username, profile_img)
    if user is None:
        return failure_response(err)
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/")
def get_user(user_id):
    user, err = dao.get_user_by_id(user_id)
    if user is None:
        return failure_response(err)
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/profile-img/", methods=["POST"])
def update_profile_image(user_id):
    user, err = dao.get_user_by_id(user_id)
    if user is None:
        return failure_response(err)

    body = json.loads(request.data)
    image_data = body.get("image")
    image, err = dao.update_profile_image(user_id, image_data)
    if err:
        return failure_response(err)
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/workspaces/")
def get_workspaces_of_user(user_id):
    workspaces, err = dao.get_workspaces_of_user(user_id)
    if workspaces is err:
        return failure_response(err)
    return success_response([w.serialize() for w in workspaces])

@app.route("/users/<int:user_id>/workspaces/<int:workspace_id>/channels/")
def get_channels_of_user_in_workspace(user_id, workspace_id):
    channels, message = dao.get_users_channels_of_workspace(user_id, workspace_id)
    if channels is False:
        return failure_response(message)
    return success_response([c.serialize_name() for c in channels])

@app.route("/users/<int:user_id>/threads/")
def get_followed_threads_of_user(user_id):
    threads, err = dao.get_threads_of_user(user_id)
    if threads is None:
        return failure_response(err)
    return success_response([m.serialize_content() for m in threads])

@app.route("/users/<int:user_id>/workspaces/<int:workspace_id>/dms/")
def get_dms_of_user_in_workspace(user_id, workspace_id):
    dms, err = dao.get_dms_of_user(user_id, workspace_id)
    if dms is None:
        return failure_response(err)
    return success_response([dm.serialize() for dm in dms])

@app.route("/users/<int:user_id>/images/")
def get_images_of_user(user_id):
    images, err = dao.get_images_of_user(user_id)
    if images is None:
        return failure_response(err)
    return success_response([i.serialize() for i in images])

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def remove_user(user_id):
    optional_user, err = dao.delete_user_by_id(user_id)
    if optional_user is None:
        return failure_response(err)
    return success_response(optional_user.serialize())

# ------------------------- WORKSPACE ROUTES --------------------------------------------
@app.route("/workspaces/", methods=["POST"])
def create_workspace():
    body = json.loads(request.data)
    name = body.get("name")
    url = body.get("url")

    workspace, err = dao.create_workspace(name, url)
    if workspace is None:
        return failure_response(err)
    return success_response(workspace.serialize(), 201)

@app.route("/workspaces/")
def get_workspaces():
    workspaces = dao.get_workspaces()
    return success_response([w.serialize() for w in workspaces])

@app.route("/workspaces/<int:workspace_id>/")
def get_workspace_by_id(workspace_id):
    workspace, err = dao.get_workspace_by_id(workspace_id)
    if workspace is None:
        return failure_response(err)
    return success_response(workspace.serialize())

@app.route("/workspaces/<int:workspace_id>/add-user/", methods=["POST"])
def add_user_to_workspace(workspace_id):
    body = json.loads(request.data)
    user_id = body.get("user_id")

    workspace, err = dao.add_user_to_workspace(user_id, workspace_id)
    if workspace is None:
        return failure_response(err)
    return success_response(workspace.serialize(), 201)

@app.route("/workspaces/<int:workspace_id>/", methods=["DELETE"])
def remove_workspace(workspace_id):
    workspace, err = dao.delete_workspace_by_id(workspace_id)
    if workspace is None:
        return failure_response(err)
    return success_response(workspace.serialize())

@app.route("/workspaces/<int:workspace_id>/channels/")
def get_channels_of_workspace(workspace_id):
    channels, err = dao.get_channels_of_workspace(workspace_id)
    if channels is None:
        return failure_response(err)
    return success_response([c.serialize() for c in channels])

@app.route("/workspaces/<int:workspace_id>/images/")
def get_images_of_workspace(workspace_id):
    images, err = dao.get_images_of_workspace(workspace_id)
    if images is None:
        return failure_response(err)
    return success_response([i.serialize() for i in images])


# ------------------------- CHANNEL ROUTES --------------------------------------------
@app.route("/workspaces/<int:workspace_id>/channels/", methods=["POST"])
def create_channel(workspace_id):
    body = json.loads(request.data)
    name = body.get("name")
    description = body.get("description", "")
    public = body.get("public", True)

    channel, err = dao.create_channel_by_workspace_id(workspace_id, name, description, public)
    if channel is None:
        return failure_response(err)
    return success_response(channel.serialize(), 201)

@app.route("/channels/<int:channel_id>/")
def get_channel(channel_id):
    optional_channel, err = dao.get_channel_by_id(channel_id)
    if optional_channel is None:
        return failure_response(err)
    return success_response(optional_channel.serialize())

@app.route("/channels/<int:channel_id>/users/", methods=["POST"])
def add_user_to_channel(channel_id):
    body = json.loads(request.data)
    user_id = body.get('user_id')

    optional_channel, err = dao.add_user_to_channel(channel_id, user_id)
    if optional_channel is None:
        return failure_response(err)
    return success_response(optional_channel.serialize(), 201)

@app.route("/channels/<int:channel_id>/users/<int:user_id>/", methods=["DELETE"])
def remove_user_from_channel(channel_id, user_id):
    optional_channel, err = dao.delete_user_from_channel(channel_id, user_id)
    if optional_channel is None:
        return failure_response(err)
    return success_response(optional_channel.serialize())

@app.route("/channels/<int:channel_id>/", methods=["DELETE"])
def remove_channel(channel_id):
    optional_channel, err = dao.delete_channel(channel_id)
    if optional_channel is None:
        return failure_response(err)
    return success_response(optional_channel.serialize())

@app.route("/channels/<int:channel_id>/messages/")
def get_messages_of_channel(channel_id):
    optional_messages, err = dao.get_messages_of_channel(channel_id)
    if optional_messages is None:
        return failure_response(err)
    return success_response([m.serialize_content() for m in optional_messages])

@app.route("/channels/<int:channel_id>/images/")
def get_images_of_channel(channel_id):
    channel, err = dao.get_channel_by_id(channel_id)
    if err:
        return failure_response(err)
    images = channel.images
    return success_response([i.serialize() for i in images])

# ------------------------- MESSAGE ROUTES --------------------------------------------
@app.route("/channels/<int:channel_id>/messages/", methods=["POST"])
def create_message(channel_id):
    body = json.loads(request.data)
    user_id = body.get("user_id")
    content = body.get("content")
    image = body.get("image")
    
    optional_message, err = dao.create_message(channel_id, user_id, content, image)
    if optional_message is None:
        return failure_response(err)
    return success_response(optional_message.serialize(), 201)

@app.route("/messages/<int:message_id>/")
def get_message(message_id):
    optional_message, err = dao.get_message_by_id(message_id)
    if optional_message is None:
        return failure_response(err)
    return success_response(optional_message.serialize())

@app.route("/messages/<int:message_id>/", methods=["POST"])
def update_message(message_id):
    body = json.loads(request.data)
    user_id = body.get("user_id")
    content = body.get("content")

    optional_message, err = dao.update_message(message_id, user_id, content)
    if optional_message is None:
        return failure_response(err)
    return success_response(optional_message.serialize(), 201)

@app.route("/messages/<int:message_id>/users/")
def get_users_following_thread(message_id):
    optional_users, err = dao.get_users_following_message(message_id)
    if optional_users is None:
        return failure_response(err)
    return success_response([u.serialize() for u in optional_users])

@app.route("/messages/<int:message_id>/", methods=["DELETE"])
def delete_message(message_id):
    optional_message, err = dao.delete_message_by_id(message_id)
    if optional_message is None:
        return failure_response(err)
    return success_response(optional_message.serialize_content())

@app.route("/messages/<int:message_id>/threads/")
def get_threads_of_message(message_id):
    optional_threads, err = dao.get_threads_of_message(message_id)
    if optional_threads is None:
        return failure_response(err)
    return success_response([t.serialize_content() for t in optional_threads])

# ------------------------- THREAD ROUTES --------------------------------------------
@app.route("/messages/<int:message_id>/threads/", methods=["POST"])
def create_thread(message_id):
    body = json.loads(request.data)
    user_id = body.get("user_id")
    content = body.get("content")
    image = body.get("image")

    optional_thread, err = dao.create_thread(message_id, user_id, content, image)
    if optional_thread is None:
        return failure_response(err)
    return success_response(optional_thread.serialize(), 201)
    
@app.route("/threads/<int:thread_id>/")
def get_thread(thread_id):
    optional_thread, err = dao.get_thread_by_id(thread_id)
    if optional_thread is None:
        return failure_response(err)
    return success_response(optional_thread.serialize())

@app.route("/threads/<int:thread_id>/", methods=["POST"])
def update_thread(thread_id):
    body = json.loads(request.data)
    sender_id = body.get("user_id")
    content = body.get("content")

    optional_thread, err = dao.update_thread_by_id(thread_id, sender_id, content)
    if optional_thread is None:
        return failure_response(err)
    return success_response(optional_thread.serialize())

@app.route("/threads/<int:thread_id>/", methods=["DELETE"])
def remove_thread(thread_id):
    optional_thread, err = dao.delete_thread_by_id(thread_id)
    if optional_thread is None:
        return failure_response(err)
    return success_response(optional_thread.serialize())

# ------------------------- DM ROUTES --------------------------------------------
@app.route("/workspaces/<int:workspace_id>/dms/", methods=["POST"])
def create_dm_group(workspace_id):
    body = json.loads(request.data)
    users = body.get("users")
    optional_dm_group, err = dao.create_dm_group(workspace_id, users)
    if optional_dm_group is None:
        return failure_response(err)
    return success_response(optional_dm_group.serialize())

@app.route("/dms/<int:dm_id>/")
def get_dm_group(dm_id):
    optional_dm_group, err = dao.get_dm_group_by_id(dm_id)
    if optional_dm_group is None:
        return failure_response(err)
    return success_response(optional_dm_group.serialize())

@app.route("/dms/<int:dm_id>/", methods=["DELETE"])
def delete_dm_group(dm_id):
    optional_dm_group, err = dao.delete_dm_group_by_id(dm_id)
    if optional_dm_group is None:
        return failure_response(err)
    return success_response(optional_dm_group.serialize())

@app.route("/dms/<int:dm_id>/users/")
def get_users_of_dm_group(dm_id):
    optional_users, err = dao.get_users_of_dm_group(dm_id)
    if optional_users is None:
        return failure_response(None)
    return success_response([u.serialize_name() for u in optional_users])

@app.route("/dms/<int:dm_id>/messages/")
def get_messages_of_dm_group(dm_id):
    optional_messages, err = dao.get_messages_of_dm_group(dm_id)
    if optional_messages is None:
        return failure_response(None)
    return success_response([m.serialize_dm() for m in optional_messages])

@app.route("/dms/<int:dm_id>/messages/", methods=["POST"])
def create_dm_message(dm_id):
    body = json.loads(request.data)
    sender_id = body.get("user_id")
    content = body.get("content")
    image = body.get("image")

    optional_dm_message, err = dao.create_dm_message(dm_id, sender_id, content, image)
    if optional_dm_message is None:
        return failure_response(err)
    
    return success_response(optional_dm_message.serialize())

@app.route("/dm-messages/<int:message_id>/")
def get_dm_message(message_id):
    optional_dm_message, err = dao.get_dm_message_by_id(message_id)
    if optional_dm_message is None:
        return failure_response(err)
    return success_response(optional_dm_message.serialize())

@app.route("/dm-messages/<int:message_id>/", methods=["POST"])
def update_dm_message(message_id):
    body = json.loads(request.data)
    sender_id = body.get("user_id")
    content = body.get("content")

    optional_dm_message, err = dao.update_dm_message(message_id, sender_id, content)
    if optional_dm_message is None:
        return failure_response(err)
    return success_response(optional_dm_message.serialize())

@app.route("/dm-messages/<int:message_id>/", methods=["DELETE"])
def delete_dm_message(message_id):
    optional_dm_message, err = dao.delete_dm_message_by_id(message_id)
    if optional_dm_message is None:
        return failure_response(err)
    return success_response(optional_dm_message.serialize())

# ------------------------- DM ROUTES --------------------------------------------
@app.route("/images/<int:image_id>/")
def get_image(image_id):
    optional_image, err = dao.get_image_by_id(image_id)
    if err:
        return failure_response(err)
    return success_response(optional_image.serialize())

@app.route("/images/<int:image_id>/", methods=["DELETE"])
def remove_image(image_id):
    optional_image, err = dao.delete_image_by_id(image_id)
    if err:
        return failure_response(err)
    return success_response(optional_image.serialize())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
