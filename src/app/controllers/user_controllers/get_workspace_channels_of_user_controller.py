from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserChannelsController(Controller):
    def get_path(self):
        return "/users/<user_id>/workspaces/<workspace_id>/channels/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        user_id = int(request.view_args["user_id"])
        workspace_id = int(request.view.args["workspace_id"])

        channels = users_dao.get_users_channels_of_workspace(user_id, workspace_id)
        return [c.serialize_name() for c in channels]
