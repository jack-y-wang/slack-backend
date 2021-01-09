from . import *
from app.dao.users_dao import get_user_by_id
from app.dao.workspaces_dao import get_workspace_by_id
from app.dao.channels_dao import get_channel_by_id
from app.dao.messages_dao import get_message_by_id
from app.dao.images_dao import *

import datetime


def create_dm_group(workspace_id, users):
    workspace = get_workspace_by_id(workspace_id)
    if workspace is None:
        raise Exception("Workspace not found")
    if len(users) > 10:
        raise Exception("Can't create messaging group of more than 10 people")

    dm_group = DM_group(workspace_id=workspace_id)
    db.session.add(dm_group)

    for user_json in users:
        user_id = user_json.get("user_id")
        user = get_user_by_id(user_id)
        if user and user in workspace.users:
            dm_group.users.append(user)

    db.session.commit()
    return dm_group

def get_dm_group_by_id(dm_id):
    return DM_group.query.filter_by(id=dm_id).first()

def delete_dm_group_by_id(dm_id):
    dm_group = get_dm_group_by_id(dm_id)
    if dm_group is None:
        return None
    
    db.session.delete(dm_group)
    db.session.commit
    return dm_group

def get_users_of_dm_group(dm_id):
    return get_dm_group_by_id(dm_id).users

def get_messages_of_dm_group(dm_id):
    return get_dm_group_by_id(dm_id).messages

def create_dm_message(dm_id, sender_id, content):
    dm_group = get_dm_group_by_id(dm_id)
    if dm_group is None:
        raise Exception("DM group not found")
    if sender_id is None or content is None:
        raise Exception("Empty user_id or content")
    user = get_user_by_id(sender_id)
    if user is None:
        raise Exception("User not found")
    if not user in dm_group.users:
        raise Exception("User is not in DM group")
    
    timestamp = datetime.datetime.now()
    dm_message = DM_message(
        sender_id=sender_id,
        content=content,
        timestamp=timestamp,
        dm_group_id=dm_id
    )

    db.session.add(dm_message)
    db.session.commit()
    return dm_message

###########################################################################
# -------------------------- DM MESSAGES -------------------------------- #
###########################################################################

def get_dm_message_by_id(message_id):
    return DM_message.query.filter_by(id=message_id).first()

def update_dm_message(message_id, sender_id, content):
    dm_message = get_dm_message_by_id(message_id)
    if dm_message is None:
        raise Exception("DM Message not found")
    user = get_user_by_id(sender_id)
    if user is None:
        raise Exception("User not found")
    if dm_message.sender_id != sender_id:
        raise Exception("User did not create DM message")
    
    if not content is None:
        dm_message.content = content
    dm_messsage.updated = True
    db.session.commit()
    return dm_message

def delete_dm_message_by_id(message_id):
    dm_message = get_dm_message_by_id(message_id)
    if dm_message is None:
        return None
    db.session.delete(dm_message)
    db.session.commit()
    return dm_message
