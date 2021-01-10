from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserChannelsController(Controller):
    def get_path(self):
        return "/user/workspaces/<int:workspace_id>/channels/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, workspace_id, **kwargs):
        user = kwargs.get("user")
        channels = users_dao.get_users_channels_of_workspace(user.id, workspace_id)
        return [c.serialize_name() for c in channels]
