from db import db, User, Workspace, Channel, Message, Thread, DM_group, DM_message

import datetime

# --------------------- USER ----------------------------
def get_user_by_id(id):
    optional_user = User.query.filter_by(id=id).first()
    if optional_user:
        return optional_user, ""
    return None, "User with ID not found"

def get_user_by_email(email):
    optional_user = User.query.filter_by(email=email).first()
    if optional_user:
        return optional_user, ""
    return None, "User with email not found"

def get_user_by_username(username):
    optional_user = User.query.filter_by(username=username).first()
    if optional_user:
        return optional_user, ""
    return None, "User with username not found"

def create_user(name, email, username):
    if name is None or email is None or username is None:
        return None, "Empty name, username, or username"
    user_exists, err = does_user_exist(email, username)
    if user_exists:
        return None, err

    user = User(name=name, email=email, username=username)
    db.session.add(user)
    db.session.commit()
    return user, ""

def get_workspaces_of_user(user_id):
    optional_user, err = get_user_by_id(user_id)
    if optional_user is None:
        return None, err
    return optional_user.workspaces, ""

def get_users_channels_of_workspace(user_id, workspace_id):
    optional_user, err = get_user_by_id(user_id)
    if optional_user is None:
        return False, err
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return False, err
    if optional_workspace not in optional_user.workspaces:
        return False, "User is not in Workspace"
    
    channels = filter(lambda c : c.workspace_id == workspace_id, optional_user.channels)
    return channels, ""

def get_threads_of_user(user_id):
    optional_user, err = get_user_by_id(user_id)
    if optional_user is None:
        return None, err
    return optional_user.threads, ""

def get_dms_of_user(user_id, workspace_id):
    optional_user, err = get_user_by_id(user_id)
    if optional_user is None:
        return None, err
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return False, err
    if optional_workspace not in optional_user.workspaces:
        return False, "User is not in Workspace"
    return optional_user.dms, ""

def does_user_exist(email, username):
    optional_user, err = get_user_by_email(email)
    if optional_user is not None:
        return True, f"User with email already exists: {optional_user.serialize_name()}"
    optional_user, err = get_user_by_username(username)
    if optional_user is not None:
        return True, f"User with username already exists: {optional_user.serialize_name()}"

    return False, None

def delete_user_by_id(user_id):
    optional_user, err = get_user_by_id(user_id)
    if not optional_user:
        return None, err
    db.session.delete(optional_user)
    db.session.commit()
    return optional_user, ""

# --------------------- WORKSPACE ----------------------------
def create_workspace(name, url):
    if name is None or url is None:
        return None, "Empty name or url"
    workspace_exists, err = does_workspace_exist(name, url)
    if workspace_exists:
        return None, err

    workspace = Workspace(name=name, url=url)
    db.session.add(workspace)
    db.session.commit()
    return workspace, ""

def get_workspaces():
    return Workspace.query.all()

def get_workspace_by_id(id):
    optional_workspace = Workspace.query.filter_by(id=id).first()
    if optional_workspace:
        return optional_workspace, ""
    return None, "Workspace with ID not found"

def get_workspace_by_name(name):
    optional_workspace = Workspace.query.filter_by(name=name).first()
    if optional_workspace:
        return optional_workspace, ""
    return None, "Worskace with name not found"

def get_workspace_by_url(url):
    optional_workspace = Workspace.query.filter_by(url=url).first()
    if optional_workspace:
        return optional_workspace, ""
    return None, "Workspace with url not found"

def does_workspace_exist(name, url):
    optional_workspace, err = get_workspace_by_name(name)
    if optional_workspace:
        return True, f"Workspace with name already exists: {optional_workspace.serialize()}"

    optional_workspace, err = get_workspace_by_url(url)
    if optional_workspace:
        return True, f"Workspace with url already exists: {optional_workspace.serialize()}"
    
    return False, None

def add_user_to_workspace(user_id, workspace_id):
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return None, err
    optional_user, err = get_user_by_id(user_id)
    if optional_user is None:
        return None, err
    if optional_user in optional_workspace.users:
        return None, "User already in channel"

    optional_workspace.users.append(optional_user)
    for channel in optional_workspace.channels:
        if channel.public:
            optional_user.channels.append(channel)

    db.session.commit()
    return optional_workspace, ""

def get_channels_of_workspace(workspace_id):
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return None, err
    optional_workspace = Workspace.query.filter_by(id=workspace_id).first()
    return optional_workspace.channels, ""

def delete_workspace_by_id(workspace_id):
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return None, err
    db.session.delete(optional_workspace)
    db.session.commit()
    return optional_workspace, ""

# --------------------- CHANNEL ----------------------------
def create_channel_by_workspace_id(workspace_id, name, description, public):
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return None, err
    optional_channel, err = get_channel_by_name(optional_workspace, name)
    if optional_channel is not None:
        return None, f"Channel with name {name} already exists"
    
    channel = Channel(name=name, description=description, public=public, workspace_id=workspace_id)
    db.session.add(channel)
    if channel.public == True:
        for user in optional_workspace.users:
            # channel.users.append(user)
            user.channels.append(channel)
    optional_workspace.channels.append(channel)
    db.session.commit()
    return channel, ""

def get_channel_by_id(channel_id):
    optional_channel = Channel.query.filter_by(id=channel_id).first()
    if optional_channel:
        return optional_channel, ""
    return None, "Channel with ID not found"

def get_channel_by_name(workspace, channel_name):
    channel = list(filter(lambda c : c.name==channel_name, workspace.channels))
    if not channel:
        return None, f"Channel with name {channel_name} does not exist in the workspace"
    return channel[0], ""

def get_messages_of_channel(channel_id):
    optional_channel, err = get_channel_by_id(channel_id)
    if optional_channel is None:
        return None, err
    return optional_channel.messages, ""

def add_user_to_channel(channel_id, user_id):
    optional_channel, err = get_channel_by_id(channel_id)
    if optional_channel is None:
        return err
    user, err = get_user_by_id(user_id)
    if user is None:
        return err
    workspace, _ = get_workspace_by_id(optional_channel.workspace_id)
    if not user in workspace.users:
        return f"User is not in workspace: {workspace.serialize_name()}"
    if user in optional_channel.users:
        return f"User already in channel {optional_channel.name}"
    
    optional_channel.users.append(user)
    db.session.commit()
    return optional_channel, ""

def delete_user_from_channel(channel_id, user_id):
    optional_channel, err = get_channel_by_id(channel_id)
    if optional_channel is None:
        return None, err
    optional_user, err = get_user_by_id(user_id)
    if optional_user is None:
        return None, err
    
    optional_channel.users.remove(optional_user)
    db.session.commit()
    return optional_channel, ""

def delete_channel(channel_id):
    optional_channel, err = get_channel_by_id(channel_id)
    if optional_channel is None:
        return None, err
    db.session.delete(optional_channel)
    db.session.commit()
    return optional_channel, ""


# --------------------- MESSAGE ----------------------------
def create_message(channel_id, sender_id, content):
    optional_channel, err = get_channel_by_id(channel_id)
    if optional_channel is None:
        return None, err
    if sender_id is None or content is None:
        return None, "Empty user_id or content"
    sender, err = get_user_by_id(sender_id)
    if sender is None:
        return None, err
    if not sender in optional_channel.users:
        return None, "User is not in channel"

    timestamp = datetime.datetime.now()
    message = Message(
        sender_id = sender_id,
        content = content,
        timestamp = timestamp,
        channel_id = channel_id
    )

    optional_channel.messages.append(message)
    sender.threads.append(message)
    db.session.commit()
    return message, ""
    
def get_message_by_id(msg_id):
    optional_message = Message.query.filter_by(id=msg_id).first()
    if optional_message:
        return optional_message, ""
    return None, "Message is not found"

def update_message(msg_id, sender_id, content):
    optional_message, err = get_message_by_id(msg_id)
    if optional_message is None:
        return None, err
    if sender_id is None or content is None:
        return None, "Invalid input: user ID and or content"
    if optional_message.sender_id != sender_id:
        return None, "Invalid user ID - must be the creator of message"

    if content:
        optional_message.content = content
    optional_message.updated = True
    db.session.commit()
    return optional_message, ""

def get_users_following_message(msg_id):
    optional_message, err = get_message_by_id(msg_id)
    if not optional_message:
        return None, err
    return optional_message.users, ""

def get_threads_of_message(msg_id):
    optional_message, err = get_message_by_id(msg_id)
    if not optional_message:
        return None, err
    return optional_message.threads, ""

def delete_message_by_id(message_id):
    optional_message, err = get_message_by_id(message_id)
    if optional_message is None:
        return None, err
   
    db.session.delete(optional_message)
    db.session.commit()
    return optional_message, ""

# --------------------- THREAD ----------------------------
def create_thread(message_id, sender_id, content):
    optional_message, err = get_message_by_id(message_id)
    if optional_message is None:
        return None, err
    if sender_id is None or content is None:
        return None, "Empty user_id or content"
    
    user, err = get_user_by_id(sender_id)
    if user is None:
        return None, err
    if not user in optional_message.channel.users:
        return None, "User is not in the channel"
    
    timestamp = datetime.datetime.now()
    thread = Thread(
        sender_id=sender_id,
        content=content,
        timestamp=timestamp,
        message_id=message_id
    )
    db.session.add(thread)
    optional_message.threads.append(thread)
    optional_message.users_following.append(user)
    db.session.commit()
    return thread, ""

def get_thread_by_id(thread_id):
    optional_thread = Thread.query.filter_by(id=thread_id).first()
    if optional_thread:
        return optional_thread, ""
    return None, "Thread not found"

def update_thread_by_id(thread_id, sender_id, content):
    optional_thread, err = get_thread_by_id(thread_id)
    if optional_thread is None:
        return None, err
    if sender_id is None or content is None:
        return None, "Invalid input: user ID and or content"
    if optional_thread.sender_id != sender_id:
        return None, "Invalid user ID - must be the creator of thread reply"
    
    if content:
        optional_thread.content = content
    optional_thread.updated = True
    db.session.commit()

    return optional_thread, ""

def delete_thread_by_id(thread_id):
    optional_thread, err = get_thread_by_id(thread_id)
    if optional_thread is None:
        return None, err
    message = optional_thread.message
    sender_id = optional_thread.sender_id

    sender, err = get_user_by_id(sender_id)
    if sender is None:
        return None, err

    message.users_following.remove(sender)
    db.session.delete(optional_thread)
    db.session.commit()
    return optional_thread, ""

# --------------------- DMS - DIRECT MESSAGES ----------------------------
def create_dm_group(workspace_id, users):
    optional_workspace, err = get_workspace_by_id(workspace_id)
    if optional_workspace is None:
        return None, err
    if len(users) > 10:
        return None, "Can't create messaging group of more than 10 people"

    dm_group = DM_group(workspace_id=workspace_id)
    db.session.add(dm_group)

    for user_json in users:
        user_id = user_json.get("user_id")
        user, _ = get_user_by_id(user_id)
        if user and user in optional_workspace.users:
            dm_group.users.append(user)

    db.session.commit()
    return dm_group, ""

def get_dm_group_by_id(dm_id):
    optional_dm_group = DM_group.query.filter_by(id=dm_id).first()
    if optional_dm_group is None:
        return None, "DM group not found"
    return optional_dm_group, ""

def delete_dm_group_by_id(dm_id):
    optional_dm_group, err = get_dm_group_by_id(dm_id)
    if optional_dm_group is None:
        return None, err
    
    db.session.delete(optional_dm_group)
    db.session.commit
    return optional_dm_group, ""

def get_users_of_dm_group(dm_id):
    optional_dm_group, err = get_dm_group_by_id(dm_id)
    if optional_dm_group is None:
        return None, err
    return optional_dm_group.users, ""

def get_messages_of_dm_group(dm_id):
    optional_dm_group, err = get_dm_group_by_id(dm_id)
    if optional_dm_group is None:
        return None, err
    return optional_dm_group.messages, ""

def create_dm_message(dm_id, sender_id, content):
    optional_dm_group, err = get_dm_group_by_id(dm_id)
    if optional_dm_group is None:
        return None, err
    if sender_id is None or content is None:
        return None, "Empty user_id or content"
    
    user, err = get_user_by_id(sender_id)
    if user is None:
        return None, err
    if not user in optional_dm_group.users:
        return None, "User is not in DM group"
    
    timestamp = datetime.datetime.now()
    dm_message = DM_message(
        sender_id=sender_id,
        content=content,
        timestamp=timestamp,
        dm_group_id=dm_id
    )

    db.session.add(dm_message)
    db.session.commit()
    return dm_message, ""

def get_dm_message_by_id(message_id):
    optional_message = DM_message.query.filter_by(id=message_id).first()
    if optional_message:
        return optional_message, ""
    return None, "DM message not found"

def update_dm_message(message_id, sender_id, content):
    optional_dm_message, err = get_dm_message_by_id(message_id)
    if optional_dm_message is None:
        return None, err
    optional_user, err = get_user_by_id(sender_id)
    if optional_user is None:
        return None, err
    if optional_dm_message.sender_id != sender_id:
        return None, "User did not create DM message"
    
    if not content is None:
        optional_dm_message.content = content
    optional_dm_messsage.updated = True
    db.session.commit()
    return optional_dm_message, ""

def delete_dm_message_by_id(message_id):
    optional_dm_message, err = get_dm_message_by_id(message_id)
    if optional_dm_message is None:
        return None, err
    db.session.delete(optional_dm_message)
    db.session.commit()
    return optional_dm_message, ""
