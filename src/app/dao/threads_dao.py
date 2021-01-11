from . import *
from app.dao.users_dao import get_user_by_id
from app.dao.workspaces_dao import get_workspace_by_id
from app.dao.channels_dao import get_channel_by_id
from app.dao.messages_dao import get_message_by_id
from app.dao.images_dao import *

import datetime


def get_thread_by_id(thread_id):
    return Thread.query.filter_by(id=thread_id).first()

def create_thread(message_id, sender_id, content, image_data):
    if sender_id is None or content is None:
        return None, "Empty user_id or content"
    
    message = get_message_by_id(message_id)
    if message is None:
        raise Exception("Message is not found")
    user = get_user_by_id(sender_id)
    if user is None:
        raise Exception("User is not found")

    channel = get_channel_by_id(message.channel_id)
    if not user in channel.users:
        raise Exception("User is not in the channel")
    
    timestamp = datetime.datetime.now()
    thread = Thread(
        sender_id=sender_id,
        content=content,
        timestamp=timestamp,
        message_id=message_id
    )
    db.session.add(thread)
    message.threads.append(thread)
    message.users_following.append(user)

    # create and image image obj if there's one
    if image_data is not None:
        workspace = get_workspace_by_id(channel.workspace_id)
        image = create_image(
            image_data=image_data,
            sender_id=sender_id, 
            source="thread", 
            source_id=thread.id,
            channel_id=message.channel_id,
            workspace_id=workspace.id)
        if image is None:
            return None
        user.images.append(image)
        channel.images.append(image)
        workspace.images.append(image)

        thread.image_id = image.id

    db.session.commit()
    return thread

def update_thread_by_id(thread_id, sender_id, content):
    if sender_id is None or content is None:
        raise Exception("Empty input: user ID and or content")
    thread = get_thread_by_id(thread_id)
    if thread is None:
        raise Exception("Thread not found")
    if thread.sender_id != sender_id:
        raise Exception("Invalid user ID - must be the creator of thread reply")
    
    if content:
        thread.content = content
    thread.updated = True
    db.session.commit()
    return thread

def delete_thread_by_id(thread_id, sender_id):
    thread = get_thread_by_id(thread_id)
    if thread is None:
        raise Exception("Thread not found")
    message = thread.message
    sender_id = thread.sender_id

    if thread.sender_id != sender_id:
        raise Exception("Can't delete thread: user did not create thread")

    if thread.image_id:
        delete_image_by_id(thread.image_id)

    sender = get_user_by_id(sender_id)
    if sender is None:
        return None
    message.users_following.remove(sender)
    
    db.session.delete(thread)
    db.session.commit()
    return thread
