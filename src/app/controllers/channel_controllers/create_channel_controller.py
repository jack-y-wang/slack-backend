from app.controllers import *
from flask import request
from app.dao import channels_dao

class CreateChannelController(Controller):
    def get_name(self):
        return "create-channel"

    def get_path(self):
        return "/workspaces/<int:workspace_id>/channels/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self, workspace_id):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        public = data.get('public', True)
        channel = channels_dao.create_channel_by_workspace_id(workspace_id, name, description, public)
        return channel.serialize()
        