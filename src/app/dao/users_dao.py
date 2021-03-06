from . import *
from app.dao.images_dao import *


def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        raise Exception("User not found")
    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise Exception("User not found")
    return user


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise Exception("User not found")
    return user


def get_user_by_session_token(session_token):
    user = User.query.filter(User.session_token == session_token).first()
    if user is None:
        raise Exception("User not found")
    return user


def get_user_by_update_token(update_token):
    user = User.query.filter(User.update_token == update_token).first()
    if user is None:
        raise Exception("User not found")
    return user


def create_user(name, email, username, password, image_data):
    if name is None or email is None or username is None or password is None:
        raise Exception("Empty name, username, or username")
    user_exists = does_user_exist(email, username)
    if user_exists:
        raise Exception("User with email or password already exists")

    user = User(name=name, email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()

    # add profile image if found in request data
    if image_data:
        image, _ = create_profile_image(user.id, image_data)
        user.profile_image_id = image.id

    db.session.commit()
    return user


def verify_credentials(email, password):
    optional_user = get_user_by_email(email)
    if optional_user is None:
        return False, None 
    
    return optional_user.verify_password(password), optional_user


def create_profile_image(user_id, image_data):
    if image_data is None:
        return None, "No base64 URL is found"
    
    profile_img = ProfileImage(user_id=user_id, image_data=image_data)
    db.session.add(profile_img)
    db.session.commit()
    return profile_img, ""


def update_profile_image(user_id, image_data):
    if image_data is None:
        return None, "No base64 URL is found"
    
    user = get_user_by_id(user_id)
    if user.profile_image_id:
        curr_image_id = user.profile_image_id
        delete_image_by_id(curr_image_id)

    profile_img = ProfileImage(user_id=user_id, image_data=image_data)
    db.session.add(profile_img)
    db.session.commit()
    user.profile_image_id = profile_img.id
    db.session.commit()
    return user


def get_workspaces_of_user(user_id):
    user = get_user_by_id(user_id)
    return user.workspaces


def get_users_channels_of_workspace(user_id, workspace_id):
    user = get_user_by_id(user_id)
    if user is None:
        raise Exception("User is not found")
    workspace = Workspace.query.filter_by(id=workspace_id).first()
    if workspace is None:
        raise Exception("Workspace is not found")
    if workspace not in user.workspaces:
        raise Exception("User is not in Workspace")
    
    channels = filter(lambda c : c.workspace_id == workspace_id, user.channels)
    return channels


def get_threads_of_user(user_id):
    return get_user_by_id(user_id).threads


def get_dms_of_user(user_id, workspace_id):
    user = get_user_by_id(user_id)
    workspace = Workspace.query.filter_by(id=workspace_id).first()
    if workspace is None:
        raise Exception("Workspace is not found")
    if workspace not in user.workspaces:
        raise Exception("User is not in Workspace")
    return user.dms


def get_images_of_user(user_id):
    return get_user_by_id(user_id).images


def does_user_exist(email, username):
    if get_user_by_email(email) or get_user_by_username(username):
        return True
    return False


def delete_user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user.profile_image_id:
        delete_image_by_id(user.profile_image_id)
        user.profile_image_id = None
    db.session.delete(user)
    db.session.commit()
    return user
