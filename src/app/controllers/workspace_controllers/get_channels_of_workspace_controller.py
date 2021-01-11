from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class GetChannelsOfWorkspaceController(Controller):
    def get_name(self):
        return "get-workspace-channels"

    def get_path(self):
        return "/workspaces/<int:workspace_id>/channels/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, workspace_id, **kwargs):
        user = kwargs.get("user")
        in_workspace, _ = workspaces_dao.is_user_in_workspace(user.id, workspace_id)
        if not in_workspace:
            raise Exception("User not in workspace")

        channels = workspaces_dao.get_channels_of_workspace(workspace_id)
        return [channel.serialize() for channel in channels]
        