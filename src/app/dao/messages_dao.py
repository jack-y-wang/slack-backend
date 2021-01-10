from . import *
from app.dao.users_dao import get_user_by_id
from app.dao.workspaces_dao import get_workspace_by_id
from app.dao.channels_dao import get_channel_by_id
from app.dao.images_dao import *

import datetime

def create_message(channel_id, sender_id, content, image_data):
    if sender_id is None or content is None:
        raise Exception("Empty user_id or content")

    channel = get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("Channel not found")
    sender = get_user_by_id(sender_id)
    if sender is None:
        raise Exception("User not found")
    if not sender in channel.users:
        raise Exception("User is not in channel")
    
    # create message obj
    timestamp = datetime.datetime.now()
    message = Message(
        sender_id = sender_id,
        content = content,
        timestamp = timestamp,
        channel_id = channel_id
    )

    channel.messages.append(message)
    sender.threads.append(message)

    # create and add image obj if there's one
    if image_data is not None:
        workspace = get_workspace_by_id(channel.workspace_id)
        image = create_image(
            image_data=image_data,
            sender_id=sender_id, 
            source="message", 
            source_id=message.id,
            channel_id=channel.id,
            workspace_id=workspace.id)
        if image is None:
            return None
        sender.images.append(image)
        channel.images.append(image)
        workspace.images.append(image)

        message.image_id = image.id

    db.session.commit()
    return message
    
def get_message_by_id(msg_id):
    message = Message.query.filter_by(id=msg_id).first()
    if message is None:
        raise Exception("Message not found")
    return message

def update_message(msg_id, sender_id, content):
    if sender_id is None or content is None:
        raise Exception("Invalid input: user ID and or content")

    message = get_message_by_id(msg_id)
    if message is None:
        raise Exception("Message not found")
    if message.sender_id != sender_id:
        raise Exception("Invalid user ID - must be the creator of message")

    if content:
        message.content = content
    message.updated = True
    db.session.commit()
    return message

def get_users_following_message(msg_id):
    return get_message_by_id(msg_id).users

def get_threads_of_message(msg_id):
    return get_message_by_id(msg_id).threads

def delete_message_by_id(message_id, sender_id):
    message = get_message_by_id(message_id)
    if message is None:
        raise Exception("Message not found")

    if message.sender_id != sender_id:
        raise Exception("Can't delete message: user did not create message")

    if message.image_id:
        delete_image_by_id(message.image_id)

    # channel = message.channel
    # channel.messages.remove(message)
    db.session.delete(message)
    db.session.commit()
    return message
