from . import *
from app.dao.users_dao import get_user_by_id
from app.dao.workspaces_dao import get_workspace_by_id


def create_channel_by_workspace_id(workspace_id, name, description, public):
    workspace = get_workspace_by_id(workspace_id)
    if workspace is None:
        raise Exception("Workspace not found")
    channel = get_channel_by_name(workspace, name)
    if channel is not None:
        raise Exception(f"Channel with name, {name}, already exists")
    channel = Channel(name=name, description=description, public=public, workspace_id=workspace_id)
    db.session.add(channel)
    if channel.public == True:
        for user in workspace.users:
            # channel.users.append(user)
            user.channels.append(channel)
    workspace.channels.append(channel)
    db.session.commit()
    return channel

def get_channel_by_id(channel_id):
    channel = Channel.query.filter_by(id=channel_id).first()
    if channel is None:
        raise Exception("Channel not found")
    return channel

def get_channel_by_name(workspace, channel_name):
    channel = list(filter(lambda c : c.name==channel_name, workspace.channels))
    print(f"this is the channel {channel}")
    if not channel:
        return None
    return channel[0]

def get_messages_of_channel(channel_id):
    return get_channel_by_id(channel_id).messages

def get_images_of_channel(channel_id):
    return get_channel_by_id(channel_id).images

def add_user_to_channel(channel_id, user_id):
    channel = get_channel_by_id(channel_id)
    user = get_user_by_id(user_id)
    workspace = get_workspace_by_id(channel.workspace_id)
    if not user in workspace.users:
        raise Exception(f"User is not in workspace: {workspace.serialize_name()}")
    if user in channel.users:
        return channel
    
    channel.users.append(user)
    db.session.commit()
    return channel

def is_user_in_channel(channel_id, user_id):
    channel = get_channel_by_id(channel_id)
    user = get_user_by_id(user_id)
    if user in channel.users:
        return True
    return False

def delete_user_from_channel(channel_id, user_id):
    channel = get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("Channel not found")
    user = get_user_by_id(user_id)
    if user is None:
        raise Exception("User not found")
    channel.users.remove(user)

    # if channel is private and has 0 users, then delete channel
    if channel.public is False and not channel.users:
        delete_channel(channel.id)
    db.session.commit()
    return channel

def delete_channel(channel_id):
    channel = get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("Channel not found")
    db.session.delete(channel)
    db.session.commit()
    return channel
