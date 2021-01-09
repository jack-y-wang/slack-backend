from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserChannelsController(Controller):
    def get_path(self):
        return "/users/<int:user_id>/workspaces/<int:workspace_id>/channels/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, user_id, workspace_id):
        channels = users_dao.get_users_channels_of_workspace(user_id, workspace_id)
        return [c.serialize_name() for c in channels]
