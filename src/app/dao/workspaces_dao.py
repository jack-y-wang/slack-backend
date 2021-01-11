from . import *
from app.dao.users_dao import get_user_by_id

def create_workspace(name, url):
    if name is None or url is None:
        raise Exception("Empty name or url")
    workspace_exists, msg = does_workspace_exist(name, url)
    if workspace_exists:
        raise Exception(msg)

    workspace = Workspace(name=name, url=url)
    db.session.add(workspace)
    db.session.commit()
    return workspace

def get_workspaces():
    return Workspace.query.all()

def get_workspace_by_id(id):
    workspace = Workspace.query.filter_by(id=id).first()
    if workspace is None:
        raise Exception("Workspace with ID not found")
    return workspace

def get_workspace_by_name(name):
    workspace = Workspace.query.filter_by(name=name).first()
    if workspace is None:
        raise Exception("Workspace with name not found")
    return workspace

def get_workspace_by_url(url):
    workspace = Workspace.query.filter_by(url=url).first()
    if workspace is None:
        raise Exception("Workspace with url not found")
    return workspace

def does_workspace_exist(name, url):
    try:
        workspace = get_workspace_by_name(name)
        if workspace:
            return True, f"Workspace with name already exists: {workspace.name}"

        workspace = get_workspace_by_url(url)
        if workspace:
            return True, f"Workspace with url already exists: {workspace.url}"
    except Exception as e:
        return False, None

def add_user_to_workspace(user_id, workspace_id):
    workspace = get_workspace_by_id(workspace_id)
    user = get_user_by_id(user_id)
    if user in workspace.users:
        raise Exception("User already in channel")

    workspace.users.append(user)
    for channel in workspace.channels:
        if channel.public:
            user.channels.append(channel)

    db.session.commit()
    return workspace

def is_user_in_workspace(user_id, workspace_id):
    workspace = get_workspace_by_id(workspace_id)
    user = get_user_by_id(user_id)
    if user in workspace.users:
        return True, workspace
    return False, None

def delete_user_from_workspace(workspace_id, user_id):
    workspace = get_workspace_by_id(workspace_id)
    if workspace is None:
        raise Exception("Workspace not found")
    user = get_user_by_id(user_id)
    if user is None:
        raise Exception("User not found")
    
    workspace.users.remove(user)
    db.session.commit()
    return workspace

def get_channels_of_workspace(workspace_id):
    workspace = get_workspace_by_id(workspace_id)
    return workspace.channels

def get_images_of_workspace(workspace_id):
    workspace = get_workspace_by_id(workspace_id)
    return workspace.images

def delete_workspace_by_id(workspace_id):
    workspace = get_workspace_by_id(workspace_id)
    db.session.delete(workspace)
    db.session.commit()
    return workspace
    