from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class GetChannelsOfWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/<workspace_id>/channels/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        workspace_id = int(request.view_args["workspace_id"])
        channels = workspaces_dao.get_channels_of_workspace(workspace_id)
        return [channel.serialize() for channel in channels]
        