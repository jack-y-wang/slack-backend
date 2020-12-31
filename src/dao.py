from db import User, Workspace, Channel, Message, Thread

# --------------------- USER ----------------------------
def get_user_by_id(id):
    optional_user = User.query.filter_by(id=id).first()
    if optional_user:
        return optional_user
    return None

def get_user_by_email(email):
    optional_user = User.query.filter_by(email=email).first()
    if optional_user:
        return optional_user
    return None

def get_user_by_username(username):
    optional_user = User.query.filter_by(username=username).first()
    if optional_user:
        return optional_user
    return None

def get_workspaces_of_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None
    return [w.serialize() for w in user.workspaces]

def get_threads_of_user(user):
    return [m.serialize_content() for m in user.threads]

def does_user_already_exist(email, username):
    optional_user = get_user_by_email(email)
    if optional_user is not None:
        return True, f"User with email already exists: {optional_user.serialize_name()}"

    optional_user = get_user_by_username(username)
    if optional_user is not None:
        return True, f"User with username already exists: {optional_user.serialize_name()}"

    return False, None

# --------------------- WORKSPACE ----------------------------
def get_workspace_by_id(id):
    optional_workspace = Workspace.query.filter_by(id=id).first()
    if optional_workspace:
        return optional_workspace
    return None

def get_workspace_by_name(name):
    optional_workspace = Workspace.query.filter_by(name=name).first()
    if optional_workspace:
        return optional_workspace
    return None

def get_workspace_by_url(url):
    optional_workspace = Workspace.query.filter_by(url=url).first()
    if optional_workspace:
        return optional_workspace
    return None

def does_workspace_exist(name, url):
    optional_worksp =get_workspace_by_name(name)
    if optional_worksp:
        return True, f"Workspace with name already exists: {optional_worksp.serialize}"

    optional_worksp = get_workspace_by_url(url)
    if optional_worksp:
        return True, f"Workspace with url already exists: {optional_worksp.serialize}"
    
    return False, None

# --------------------- CHANNEL ----------------------------
def get_workspaces_channels(workspace_id):
    workspace = Workspace.query.filter_by(id=workspace_id).first()
    if workspace is None:
        return None, "Workspace not found"
    return [c.serialize() for c in workspace.channels]

def get_channel_by_id(channel_id):
    optional_channel = Channel.query.filter_by(id=channel_id).first()
    if optional_channel:
        return optional_channel
    return None

def get_channel_by_name(workspace, channel_name):
    channel = list(filter(lambda c : c.name==channel_name, workspace.channels))
    if not channel:
        return None
    return channel[0]

# --------------------- MESSAGE ----------------------------
def get_messages_of_channel(channel_id):
    optional_channel = Channel.query.filter_by(id=channel_id).first()
    if optional_channel is None:
        return None
    return [m.serialize_content() for m in optional_channel.messages] 

def get_message_by_id(msg_id):
    optional_message = Message.query.filter_by(id=msg_id).first()
    if optional_message:
        return optional_message
    return None

def get_users_of_message(msg):
    return [u.serialize() for u in msg.users]

# --------------------- THREAD ----------------------------
def get_thread_by_id(thread_id):
    optional_thread = Thread.query.filter_by(id=thread_id).first()
    if optional_thread:
        return optional_thread
    return None

def get_threads_of_message(msg):
    return [t.serialize() for t in msg.threads]
